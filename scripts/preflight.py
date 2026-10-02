#!/usr/bin/env python3
"""Read-only provider capability/auth probes. Never prints raw auth output or signs in."""
import argparse
import json
import re
import shutil
import subprocess
import sys

REQUIRED_FLAGS = {
    'codex': ('--json', '--sandbox', '--ephemeral', '--output-schema'),
    # Claude 2.1.287 accepts --max-turns in print mode, but its help output omits it.
    # Keep help-based capability checks limited to flags advertised by this build.
    'claude': ('--output-format', '--json-schema', '--permission-mode',
               '--permission-prompts', '--restricted', '--strict-mcp-config'),
}
REVIEWED_VERSIONS = {'codex': '0.159.3', 'claude': '2.1.287'}


def probe(executable='codex'):
    if executable not in REQUIRED_FLAGS:
        raise ValueError('unsupported provider')
    base = {'provider': executable, 'authenticated': False, 'version': None,
            'reviewed_version': REVIEWED_VERSIONS[executable], 'missing_flags': []}
    path = shutil.which(executable)
    if not path:
        return dict(base, status='UNAVAILABLE', reason='CLI not installed')
    def run(args):
        return subprocess.run([path, *args], capture_output=True, text=True, timeout=10,
                              stdin=subprocess.DEVNULL)
    try:
        version = run(['--version'])
        match = re.search(r'\b\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?\b', version.stdout)
        if version.returncode or not match:
            return dict(base, status='INCOMPATIBLE', reason='version probe invalid')
        base['version'] = match.group()
        base['version_matches_reviewed'] = base['version'] == base['reviewed_version']
        help_result = run(['exec', '--help'] if executable == 'codex' else ['--help'])
        base['missing_flags'] = [flag for flag in REQUIRED_FLAGS[executable]
                                 if flag not in help_result.stdout]
        if help_result.returncode or base['missing_flags']:
            return dict(base, status='INCOMPATIBLE', reason='required CLI flags unavailable')
        auth = run(['login', 'status'] if executable == 'codex' else ['auth', 'status'])
    except (OSError, subprocess.TimeoutExpired):
        return dict(base, status='UNAVAILABLE', reason='CLI probe failed/timed out')
    base['authenticated'] = auth.returncode == 0
    # Exit/status indicates login availability, not account independence or task success.
    return dict(base, status='INCONCLUSIVE' if base['authenticated'] else 'BLOCKED_PERMISSION',
                reason='controlled runtime scenario still required' if base['authenticated'] else 'CLI login unavailable')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--provider', choices=REQUIRED_FLAGS, default='codex')
    result = probe(parser.parse_args().provider)
    print(json.dumps(result))
    sys.exit(0 if result['authenticated'] else 2)

