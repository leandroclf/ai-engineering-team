import contextlib
import importlib.util
import io
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    import importlib
    return importlib.import_module(f'scripts.{name}')


provider = load('provider_run')
reviewer = load('review_status')


class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'validation').mkdir()
        (self.root / 'validation' / 'RUN-MANIFEST-TEMPLATE.yaml').write_text(
            (ROOT / 'validation' / 'RUN-MANIFEST-TEMPLATE.yaml').read_text())
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', '-C', str(self.root), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(self.root), '-c', 'user.name=test',
                        '-c', 'user.email=test@invalid', 'commit', '-qm', 'fixture'], check=True)
        self.prompt = self.root / 'prompt.md'
        self.prompt.write_text('controlled test')

    def run_harness(self, command, *extra):
        argv = ['provider_run.py', '--run-id', 'test', '--scenario', 'HARNESS',
                '--env', 'OPENAI-CLI-A', '--prompt-file', str(self.prompt),
                '--workdir', str(self.root / 'clones'), *extra]
        with patch.object(provider, 'ROOT', self.root), patch.object(provider, 'provider_cmd', return_value=command), \
             patch.object(sys, 'argv', argv), contextlib.redirect_stdout(io.StringIO()), \
             contextlib.redirect_stderr(io.StringIO()):
            code = provider.main()
        run = self.root / 'validation' / 'runs' / 'test'
        return code, yaml.safe_load((run / 'manifest.yaml').read_text()), run

    def test_missing_executor_preserves_blocked_manifest(self):
        code, manifest, run = self.run_harness(['nonexistent-controlled-executor'])
        self.assertEqual(code, 1)
        self.assertEqual(manifest['status'], 'BLOCKED')
        self.assertEqual(manifest['checks'][0]['exit_code'], 127)
        self.assertTrue((run / 'stderr.txt').exists())

    def test_timeout_preserves_manifest(self):
        code, manifest, run = self.run_harness(
            [sys.executable, '-u', '-c', 'print("partial"); import time; time.sleep(5)'],
            '--timeout-seconds', '1')
        self.assertEqual(code, 1)
        self.assertEqual(manifest['status'], 'INCONCLUSIVE')
        self.assertEqual(manifest['checks'][0]['exit_code'], 124)
        self.assertIn('timed out', (run / 'stderr.txt').read_text())

    def test_pre_failure_never_starts_provider(self):
        marker = self.root / 'provider-started'
        code, manifest, _ = self.run_harness(
            [sys.executable, '-c', f'from pathlib import Path; Path({str(marker)!r}).touch()'],
            '--pre', 'exit 7')
        self.assertEqual(code, 1)
        self.assertEqual(manifest['status'], 'FAIL')
        self.assertFalse(marker.exists())

    def test_nonzero_provider_skips_check(self):
        marker = self.root / 'check-started'
        code, manifest, _ = self.run_harness([sys.executable, '-c', 'raise SystemExit(2)'],
                                            '--check', f'touch {marker}')
        self.assertEqual(code, 1)
        self.assertEqual(manifest['status'], 'FAIL')
        self.assertFalse(marker.exists())

    def test_failed_required_check_propagates(self):
        code, manifest, _ = self.run_harness([sys.executable, '-c', 'pass'], '--check', 'exit 3')
        self.assertEqual(code, 1)
        self.assertEqual(manifest['status'], 'FAIL')
        self.assertEqual(manifest['checks'][-1]['exit_code'], 3)

    def test_success_still_requires_evaluator(self):
        code, manifest, _ = self.run_harness([sys.executable, '-c', 'pass'])
        self.assertEqual(code, 0)
        self.assertEqual(manifest['status'], 'INCONCLUSIVE')

    def test_claude_structured_output_is_extracted_and_validated(self):
        from scripts.review_contract import SCHEMA_PATH
        value = dict(schema_version='1.0.0', reviewer='argus', head_sha='a' * 40, verdict='PASS',
                     gates=dict(quality='PASS', security='PASS', architecture='NOT_REQUESTED', observability='NOT_REQUESTED'),
                     findings=[], checks_executed=['test'], residual_risks=[])
        import json
        payload = json.dumps(dict(type='result', is_error=False, structured_output=value), indent=2)
        code, manifest, run = self.run_harness([sys.executable, '-c', f'print({payload!r})'],
                                             '--env', 'CLAUDE-CLI', '--structured-review')
        self.assertEqual(code, 0)
        self.assertTrue(manifest['structured_review'])
        self.assertEqual(json.loads((run / 'review.json').read_text()), value)

    def test_claude_missing_structured_output_is_failure(self):
        code, manifest, run = self.run_harness([sys.executable, '-c',
            'print(\'{"type":"result","result":"verdict: PASS"}\')'],
            '--env', 'CLAUDE-CLI', '--structured-review')
        self.assertEqual(code, 1)
        self.assertEqual(manifest['checks'][0]['exit_code'], 65)
        self.assertFalse((run / 'review.json').exists())

    def test_provider_error_event_cannot_hide_behind_zero_exit(self):
        code, manifest, _ = self.run_harness([sys.executable, '-c',
            'print(\'{"type":"turn.failed","error":{"message":"failed"}}\')'])
        self.assertEqual(code, 1)
        self.assertEqual(manifest['status'], 'FAIL')

    def test_path_traversal_rejected_before_run_creation(self):
        with patch.object(sys, 'argv', ['provider_run.py', '--run-id', '../escape', '--scenario', 'H',
                                       '--env', 'OPENAI-CLI-A', '--prompt-file', str(self.prompt)]), \
             patch.object(provider, 'ROOT', self.root), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                provider.main()
        self.assertFalse((self.root / 'validation' / 'runs').exists())


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name)
        self.sha = 'a' * 40
        self.manifest = {'head_sha': self.sha, 'status': 'INCONCLUSIVE', 'failures': [], 'checks': [
            {'command': '<provider exit>', 'exit_code': 0},
            {'command': 'git rev-parse HEAD', 'exit_code': 0}]}
        self.result = {'head_sha': self.sha, 'verdict': 'PASS'}
        self.check = f'$ git rev-parse HEAD\nexit=0\n{self.sha}\n'

    def status(self):
        for file, obj in [('manifest.yaml', self.manifest), ('last-message.md', self.result)]:
            (self.run / file).write_text(yaml.safe_dump(obj))
        (self.run / 'check.txt').write_text(self.check)
        return reviewer.review_status(self.run, self.sha)

    def test_verified_success(self):
        self.assertEqual(self.status(), ('success', 'PASS'))

    def test_stale_result_blocked_even_with_fresh_checkout(self):
        self.result['head_sha'] = 'b' * 40
        self.assertEqual(self.status(), ('error', 'SHA_MISMATCH'))

    def test_provider_failure_overrides_pass(self):
        self.manifest['checks'][0]['exit_code'] = 2
        self.assertEqual(self.status(), ('error', 'EXECUTION_FAILED'))

    def test_missing_provider_exit_is_error(self):
        self.manifest['checks'].pop(0)
        self.assertEqual(self.status(), ('error', 'MISSING_PROVIDER_EXIT'))

    def test_failed_sha_command_is_error(self):
        self.check = f'$ git rev-parse HEAD\nexit=1\n{self.sha}\n'
        self.assertEqual(self.status(), ('error', 'INVALID_SHA_CHECK'))

    def test_explicit_failure_terminal(self):
        self.result['verdict'] = 'FAIL'
        self.assertEqual(self.status(), ('failure', 'FAIL'))

    def test_inconclusive_terminal_error(self):
        self.result['verdict'] = 'INCONCLUSIVE'
        self.assertEqual(self.status(), ('error', 'NO_PASS_VERDICT'))

    def test_failed_manifest_cannot_be_published_as_success(self):
        self.manifest['status'] = 'FAIL'
        self.assertEqual(self.status(), ('error', 'INVALID_RUN_STATUS'))

    def test_missing_artifacts(self):
        self.assertEqual(reviewer.review_status(self.run, self.sha), ('error', 'INVALID_EVIDENCE'))

    def test_historical_evidence_audit(self):
        for tag in ('pr1', 'pr2', 'pr3'):
            for agent, verdict in (('sentinel', 'PASS'), ('argus', 'PASS_WITH_FINDINGS')):
                run = ROOT / f'validation/runs/20261001-{tag}-{agent}'
                manifest = yaml.safe_load((run / 'manifest.yaml').read_text())
                expected = {('pr1', 'argus'): ('error', 'SHA_MISMATCH'),
                            ('pr3', 'argus'): ('error', 'INVALID_EVIDENCE')}.get((tag, agent), ('success', verdict))
                with self.subTest(tag=tag, agent=agent):
                    self.assertEqual(reviewer.review_status(run, manifest['head_sha']), expected)


class ChainTests(unittest.TestCase):
    def run_chain(self, mode):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'scripts').mkdir()
            shutil.copy(ROOT / 'scripts/pr_chain.sh', root / 'scripts/pr_chain.sh')
            bin_dir = root / 'bin'
            bin_dir.mkdir()
            wrappers = {
                'git': '#!/bin/bash\nif [[ "$*" == *rev-parse* ]]; then printf "%040d\\n" 0; fi\n',
                'sleep': '#!/bin/bash\n/bin/sleep 0.1\n',
                'gh': '#!/bin/bash\necho "$*" >> "$CALLS"\n'
                      'if [[ "$1 $2" == "pr create" ]]; then echo https://github.com/test/repo/pull/1; fi\n'
                      'if [[ "$1 $2" == "run list" ]]; then\n'
                      '  [[ "$MODE" == timeout ]] && exit 0\n'
                      '  if [[ "$MODE" == ci-fail ]]; then echo "1 failure"; else echo "1 success"; fi\nfi\n',
                'python3': '#!/bin/bash\n'
                           'if [[ "$1" == scripts/provider_run.py ]]; then\n'
                           ' echo "$*" >> "$CALLS"\n'
                           ' [[ "$MODE" == reviewer-fail && "$*" == *OPENAI-CLI-B* ]] && exit 1\n'
                           ' exit 0\nfi\n'
                           'if [[ "$1" == scripts/review_status.py ]]; then\n'
                           " echo '{\"state\":\"success\",\"verdict\":\"PASS\"}'; exit 0\nfi\n"
                           f'exec {sys.executable} "$@"\n',
            }
            for name, script in wrappers.items():
                p = bin_dir / name
                p.write_text(script)
                p.chmod(0o755)
            calls = root / 'calls.txt'
            env = dict(os.environ, PATH=f'{bin_dir}:{os.environ["PATH"]}', GH_TOKEN='test-no-real-token',
                       CI_TIMEOUT_SECONDS='1', MODE=mode, CALLS=str(calls))
            proc = subprocess.run(['bash', str(root / 'scripts/pr_chain.sh'), 'test', 'a', 's', 'r'],
                                  env=env, text=True, capture_output=True, timeout=10)
            return proc.returncode, calls.read_text()

    def test_failed_ci_does_not_start_reviewers(self):
        code, calls = self.run_chain('ci-fail')
        self.assertNotEqual(code, 0)
        self.assertNotIn('OPENAI-CLI-B', calls)
        self.assertNotIn('CLAUDE-CLI', calls)

    def test_ci_polling_is_bounded(self):
        code, calls = self.run_chain('timeout')
        self.assertNotEqual(code, 0)
        self.assertNotIn('OPENAI-CLI-B', calls)

    def test_background_failure_propagates_even_with_pass_verdict(self):
        code, calls = self.run_chain('reviewer-fail')
        self.assertNotEqual(code, 0)
        self.assertIn('OPENAI-CLI-B', calls)
        self.assertIn('CLAUDE-CLI', calls)


if __name__ == '__main__':
    unittest.main()
