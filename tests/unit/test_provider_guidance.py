import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import yaml
from scripts.preflight import probe, REQUIRED_FLAGS
from scripts.provider_run import provider_cmd, provider_environment, keep, run_observed
from scripts.review_contract import read_json
from scripts.review_status import review_status

SHA = 'a' * 40


def review():
    return dict(schema_version='1.0.0', reviewer='argus', head_sha=SHA, verdict='PASS',
                gates=dict(quality='PASS', security='PASS', architecture='NOT_REQUESTED', observability='NOT_REQUESTED'),
                findings=[], checks_executed=['controlled check'], residual_risks=[])


class ProviderGuidanceTests(unittest.TestCase):
    def test_codex_reviewer_host_is_read_only_and_never_prompts(self):
        cmd = provider_cmd('OPENAI-CLI-B', 'review', Path('/evidence'), structured_review=True)
        self.assertEqual(cmd[cmd.index('--sandbox') + 1], 'read-only')
        self.assertEqual(cmd[cmd.index('--ask-for-approval') + 1], 'never')
        self.assertIn('--output-schema', cmd)

    def test_container_retains_explicit_external_isolation_contract(self):
        cmd = provider_cmd('OPENAI-CLI-B', 'review', Path('/evidence'), container=True, structured_review=True)
        self.assertEqual(cmd[cmd.index('--output-schema') + 1], '/evidence/provider-review.schema.json')
        self.assertEqual(cmd[cmd.index('--sandbox') + 1], 'danger-full-access')

    def test_claude_unattended_structured_review(self):
        cmd = provider_cmd('CLAUDE-CLI', 'review', Path('/evidence'), structured_review=True)
        for flag, expected in [('--output-format', 'json'), ('--permission-mode', 'dontAsk'),
                               ('--permission-prompts', 'none'), ('--max-turns', '30')]:
            self.assertEqual(cmd[cmd.index(flag) + 1], expected)
        self.assertEqual(json.loads(cmd[cmd.index('--mcp-config') + 1]), {'mcpServers': {}})
        self.assertTrue(json.loads(cmd[cmd.index('--settings') + 1])['disableAllHooks'])
        self.assertIn('--json-schema', cmd)
        self.assertIn('--restricted', cmd)
        self.assertIn('mcp__*', cmd)
        self.assertNotIn('--setting-sources', cmd)
        self.assertNotIn('--dangerously-skip-permissions', cmd)

    def test_github_authority_is_not_inherited(self):
        with patch.dict(os.environ, {'GH_TOKEN': 'secret', 'GITHUB_TOKEN': 'secret', 'SSH_AUTH_SOCK': '/agent', 'PATH': '/bin'}, clear=True):
            self.assertEqual(provider_environment(), {'PATH': '/bin'})

    def test_init_and_nested_thinking_and_tokens_sanitized(self):
        self.assertEqual(keep(dict(type='system', subtype='init', apiKey='secret', model='model')),
                         dict(type='system', subtype='init', model='model'))
        value = keep({'type': 'assistant', 'message': {'content': [
            {'type': 'thinking', 'thinking': 'private'}, {'type': 'text', 'text': 'visible'}]},
            'metadata': {'access_token': 'secret'}})
        self.assertEqual(value['message']['content'], [{'type': 'text', 'text': 'visible'}])
        self.assertEqual(value['metadata']['access_token'], '[REDACTED]')

    def test_duplicate_result_key_rejected(self):
        with self.assertRaises(ValueError):
            read_json('{"verdict":"FAIL","verdict":"PASS"}')

    @unittest.skipUnless(os.name == 'posix', 'POSIX process groups')
    def test_timeout_stops_descendant_with_inherited_pipes(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / 'child-finished'
            child = f'import time; from pathlib import Path; time.sleep(1.2); Path({str(marker)!r}).touch()'
            parent = f'import subprocess,time,sys; subprocess.Popen([sys.executable,"-c",{child!r}]); time.sleep(10)'
            result = run_observed([sys.executable, '-c', parent], tmp, timeout=0.2)
            self.assertEqual(result.returncode, 124)
            time.sleep(1.3)
            self.assertFalse(marker.exists())


class ProbeTests(unittest.TestCase):
    def responses(self, provider, help_text=None, auth_code=0):
        return [subprocess.CompletedProcess([], 0, 'cli 1.2.3', ''),
                subprocess.CompletedProcess([], 0, help_text if help_text is not None else ' '.join(REQUIRED_FLAGS[provider]), ''),
                subprocess.CompletedProcess([], auth_code, '{"access_token":"DO_NOT_PERSIST","email":"private"}', '')]

    def test_both_provider_auth_commands_and_redaction(self):
        for provider, command in [('codex', ['login', 'status']), ('claude', ['auth', 'status'])]:
            with self.subTest(provider=provider), patch('scripts.preflight.shutil.which', return_value='/cli'), \
                 patch('scripts.preflight.subprocess.run', side_effect=self.responses(provider)) as run:
                result = probe(provider)
                self.assertEqual(result['status'], 'INCONCLUSIVE')
                self.assertFalse(result['version_matches_reviewed'])
                self.assertEqual(run.call_args.args[0], ['/cli', *command])
                self.assertNotIn('DO_NOT_PERSIST', json.dumps(result))
                self.assertNotIn('private', json.dumps(result))

    def test_missing_feature_blocks_before_auth(self):
        with patch('scripts.preflight.shutil.which', return_value='/cli'), \
             patch('scripts.preflight.subprocess.run', side_effect=self.responses('claude', help_text='--help')) as run:
            self.assertEqual(probe('claude')['status'], 'INCOMPATIBLE')
            self.assertEqual(run.call_count, 2)

    def test_failed_auth_is_blocked(self):
        with patch('scripts.preflight.shutil.which', return_value='/cli'), \
             patch('scripts.preflight.subprocess.run', side_effect=self.responses('claude', auth_code=1)):
            self.assertEqual(probe('claude')['status'], 'BLOCKED_PERMISSION')


class StructuredReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)
        self.value = review()
        self.manifest = dict(environment='CLAUDE-CLI', head_sha=SHA, status='INCONCLUSIVE', failures=[],
                             structured_review=True, checks=[{'command': '<provider exit>', 'exit_code': 0},
                             {'command': 'git rev-parse HEAD', 'exit_code': 0}])
        (self.path / 'check.txt').write_text(f'$ git rev-parse HEAD\nexit=0\n{SHA}\n')

    def check(self):
        (self.path / 'manifest.yaml').write_text(yaml.safe_dump(self.manifest))
        (self.path / 'review.json').write_text(json.dumps(self.value))
        return review_status(self.path, SHA, require_structured=True)

    def test_valid_review(self):
        self.assertEqual(self.check(), ('success', 'PASS'))

    def test_required_gate_inconclusive_blocks(self):
        self.value['gates']['security'] = 'INCONCLUSIVE'
        self.assertEqual(self.check(), ('failure', 'REQUIRED_GATE_NOT_PASSED'))

    def test_blocking_finding_cannot_hide_under_pass(self):
        self.value['findings'] = [dict(id='critical', severity='CRITICAL', status='OPEN', verified=False, summary='defect')]
        self.assertEqual(self.check(), ('failure', 'BLOCKING_FINDING'))
        self.value['findings'][0]['status'] = 'RESOLVED'
        self.assertEqual(self.check(), ('failure', 'BLOCKING_FINDING'))
        self.value['findings'][0]['verified'] = True
        self.assertEqual(self.check(), ('success', 'PASS'))

    def test_schema_and_reviewer_identity(self):
        self.value['reviewer'] = 'sentinel'
        self.assertEqual(self.check(), ('error', 'REVIEWER_MISMATCH'))
        self.value = review(); self.value['extra_authority'] = True
        self.assertEqual(self.check(), ('error', 'INVALID_EVIDENCE'))

    def test_cannot_fallback_to_prose_if_json_missing(self):
        (self.path / 'manifest.yaml').write_text(yaml.safe_dump(self.manifest))
        (self.path / 'last-message.md').write_text('verdict: PASS\nhead_sha: ' + SHA)
        self.assertEqual(review_status(self.path, SHA, True), ('error', 'INVALID_EVIDENCE'))
