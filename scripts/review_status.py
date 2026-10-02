#!/usr/bin/env python3
"""Convert a reviewer result to a GitHub status, bound to observable execution and SHA.

This validates transport evidence only; it does not prove reviewer/account independence.
"""
import json
import re
from pathlib import Path
import sys
import yaml


def review_status(run_dir, expected_sha):
    try:
        manifest = yaml.safe_load((run_dir / 'manifest.yaml').read_text())
        text = (run_dir / 'last-message.md').read_text()
        blocks = re.findall(r'^```(?:yaml|yml)\s*\n(.*?)^```\s*$', text, re.M | re.S)
        if len(blocks) > 1:
            return 'error', 'AMBIGUOUS_RESULT'
        result = yaml.safe_load(blocks[0] if blocks else text)
        check = (run_dir / 'check.txt').read_text().splitlines()
        if not isinstance(manifest, dict) or not isinstance(result, dict):
            raise ValueError('invalid result or manifest')
        if manifest.get('head_sha') != expected_sha or result.get('head_sha') != expected_sha:
            return 'error', 'SHA_MISMATCH'
        checks = manifest.get('checks', [])
        if not checks or any(c.get('exit_code') != 0 for c in checks):
            return 'error', 'EXECUTION_FAILED'
        if not any(c.get('command') == '<provider exit>' for c in checks):
            return 'error', 'MISSING_PROVIDER_EXIT'
        if not any(c.get('command') == 'git rev-parse HEAD' for c in checks):
            return 'error', 'MISSING_SHA_CHECK'
        if check != ['$ git rev-parse HEAD', 'exit=0', expected_sha]:
            return 'error', 'INVALID_SHA_CHECK'
        if manifest.get('status') not in ('PASS', 'INCONCLUSIVE') or manifest.get('failures'):
            return 'error', 'INVALID_RUN_STATUS'
        verdict = result.get('verdict')
        if verdict in ('PASS', 'PASS_WITH_FINDINGS'):
            return 'success', verdict
        if verdict in ('FAIL', 'BLOCKED'):
            return 'failure', verdict
        return 'error', 'NO_PASS_VERDICT'
    except (OSError, ValueError, TypeError, AttributeError, yaml.YAMLError):
        return 'error', 'INVALID_EVIDENCE'


if __name__ == '__main__':
    state, verdict = review_status(Path(sys.argv[1]), sys.argv[2])
    print(json.dumps({'state': state, 'verdict': verdict}))
