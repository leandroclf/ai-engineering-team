#!/usr/bin/env python3
"""Convert a reviewer result to a GitHub status, bound to observable execution and SHA.

This validates transport evidence only; it does not prove reviewer/account independence.
"""
import json
import re
from pathlib import Path
import sys
import yaml
from jsonschema import ValidationError
try:
    from .review_contract import read_json, validate_review
except ImportError:
    from review_contract import read_json, validate_review


def review_status(run_dir, expected_sha, require_structured=False):
    try:
        manifest = yaml.safe_load((run_dir / 'manifest.yaml').read_text())
        structured = require_structured or manifest.get('structured_review', False) or (run_dir / 'review.json').exists()
        if structured:
            result = validate_review(read_json((run_dir / 'review.json').read_text()))
        else:
            # Historical records only. New PR chains require structured results.
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
        if structured:
            expected_reviewer = {'OPENAI-CLI-B': 'sentinel', 'CLAUDE-CLI': 'argus'}.get(manifest.get('environment'))
            if result['reviewer'] != expected_reviewer:
                return 'error', 'REVIEWER_MISMATCH'
            if any(result['gates'][key] not in ('PASS', 'PASS_WITH_FINDINGS') for key in ('quality', 'security')):
                return 'failure', 'REQUIRED_GATE_NOT_PASSED'
            if any(v in ('FAIL', 'BLOCKED') for v in result['gates'].values()):
                return 'failure', 'GATE_FAILED'
            if any(f['severity'] in ('HIGH', 'CRITICAL') and
                   (f['status'] != 'RESOLVED' or not f['verified']) for f in result['findings']):
                return 'failure', 'BLOCKING_FINDING'
        verdict = result.get('verdict')
        if verdict in ('PASS', 'PASS_WITH_FINDINGS'):
            return 'success', verdict
        if verdict in ('FAIL', 'BLOCKED'):
            return 'failure', verdict
        return 'error', 'NO_PASS_VERDICT'
    except (OSError, ValueError, TypeError, AttributeError, yaml.YAMLError, ValidationError):
        return 'error', 'INVALID_EVIDENCE'


if __name__ == '__main__':
    state, verdict = review_status(Path(sys.argv[1]), sys.argv[2], '--require-structured' in sys.argv[3:])
    print(json.dumps({'state': state, 'verdict': verdict}))
