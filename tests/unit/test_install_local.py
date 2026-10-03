"""Exercise bootstrap filesystem effects without installing packages or Docker."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.framework = self.root / 'framework'
        for name in ('scripts', 'bin', 'runtimes'):
            (self.framework / name).mkdir(parents=True)
        for name in ('scripts/install-local.sh', 'bin/ai-team'):
            shutil.copy2(ROOT / name, self.framework / name)
        self.commands = self.root / 'commands'
        self.commands.mkdir()
        self.log = self.root / 'effects'
        self.destination = self.root / 'user-bin'
        self.env = dict(os.environ, AI_TEAM_BIN_DIR=str(self.destination),
                        PATH=str(self.commands) + ':' + os.environ['PATH'],
                        EFFECTS=str(self.log), BUILD_FAIL='0', DAEMON_FAIL='0')
        self.executable('docker', '''#!/bin/bash
if [ "$1" = info ]; then exit "$DAEMON_FAIL"; fi
echo build >> "$EFFECTS"
exit "$BUILD_FAIL"
''')
        # Delegate real preflight imports; emulate only venv/pip mutations.
        self.executable('python3', f'''#!{sys.executable}
import os, pathlib, subprocess, sys
if sys.argv[1:3] == ['-m', 'venv']:
    with open(os.environ['EFFECTS'], 'a') as f: f.write('venv\\n')
    p = pathlib.Path(sys.argv[3]) / 'bin' / 'python'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('#!/bin/bash\\necho pip >> "$EFFECTS"\\n')
    p.chmod(0o755)
else:
    sys.exit(subprocess.call([{sys.executable!r}, *sys.argv[1:]]))
''')

    def executable(self, name, content):
        path = self.commands / name
        path.write_text(content)
        path.chmod(0o755)

    def run_install(self, *args):
        return subprocess.run(['bash', str(self.framework / 'scripts/install-local.sh'), *args],
                              env=self.env, capture_output=True, text=True)

    def test_preflight_and_help_do_not_publish_or_install(self):
        for option in ('--help', '--check'):
            result = self.run_install(option)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(self.log.exists())
            self.assertFalse(self.destination.exists())
            self.assertFalse((self.framework / '.venv').exists())

    def test_foreign_file_directory_and_broken_symlink_are_preserved(self):
        self.destination.mkdir()
        path = self.destination / 'ai-team'
        for kind in ('file', 'directory', 'broken-link'):
            with self.subTest(kind=kind):
                if kind == 'file': path.write_text('operator command')
                elif kind == 'directory': path.mkdir()
                else: path.symlink_to(self.root / 'missing')
                result = self.run_install()
                self.assertEqual(result.returncode, 2)
                self.assertFalse(self.log.exists())
                self.assertTrue(path.exists() or path.is_symlink())
                if path.is_dir(): path.rmdir()
                else: path.unlink()

    def test_failed_build_does_not_publish_command(self):
        self.env['BUILD_FAIL'] = '1'
        result = self.run_install()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.destination / 'ai-team').is_symlink())
        self.assertEqual(self.log.read_text().splitlines(), ['venv', 'pip', 'build'])

    def test_success_publishes_last_and_own_link_can_be_reinstalled(self):
        for _ in range(2):
            result = self.run_install()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((self.destination / 'ai-team').resolve(), self.framework / 'bin/ai-team')
        self.assertEqual(self.log.read_text().splitlines(), ['venv', 'pip', 'build'] * 2)

    def test_destination_created_during_build_is_preserved(self):
        self.executable('docker', '''#!/bin/bash
if [ "$1" = info ]; then exit 0; fi
mkdir -p "$AI_TEAM_BIN_DIR/ai-team"
echo operator > "$AI_TEAM_BIN_DIR/ai-team/owned"
''')
        result = self.run_install()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual((self.destination / 'ai-team/owned').read_text(), 'operator\n')
        self.assertFalse((self.destination / 'ai-team/ai-team').exists())

    def test_unavailable_daemon_and_invalid_arguments_have_no_effects(self):
        self.env['DAEMON_FAIL'] = '1'
        for args in ((), ('--check',), ('--unknown',), ('install', 'extra'), ('--help', 'extra')):
            result = self.run_install(*args)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertFalse(self.log.exists())

    def test_wrapper_explains_missing_environment(self):
        result = subprocess.run(['bash', str(self.framework / 'bin/ai-team'), '--version'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('scripts/install-local.sh', result.stderr)
