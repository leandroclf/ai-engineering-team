import copy
import hashlib
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from jsonschema import ValidationError
from scripts.dot_contracts import authorize, validate, verify_evidence
from scripts.preflight import probe

NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)
BASE = 'a' * 40
FINAL = 'b' * 40


def fixture():
    repo = dict(full_name='leandroclf/ai-engineering-team', branch='feature/test', base_sha=BASE)
    lease = dict(scope_id='scope-1', task_id='task-1', project_id='team', revision=1,
                 repository=repo.copy(), issued_at='2026-10-01T23:00:00Z', expires_at='2026-10-02T01:00:00Z',
                 allowed_actions=['read_repo', 'modify_branch', 'run_tests', 'create_commit', 'create_pr'],
                 denied_actions=['deploy'], allowed_paths=['scripts', 'tests'])
    task = dict(schema_version='1.0.0', task_id='task-1', project_id='team', objective='controlled task',
                risk='R1', repository=repo, authorization=lease,
                budgets=dict(max_attempts=2, max_elapsed_seconds=600, max_external_writes=1),
                required_validation=['python -m unittest'])
    state = dict(scope_id='scope-1', task_id='task-1', project_id='team', revision=1, revoked=False, repository=repo.copy(),
                 attempts_used=0, elapsed_seconds=0, external_writes_used=0, circuit_open=False)
    return task, state


class AuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.task, self.state = fixture()

    def check(self, action='modify_branch', paths=('scripts/check.py',), **kw):
        return authorize(self.task, self.state, action, paths, now=NOW, **kw)

    def test_valid_bounded_write(self):
        self.assertEqual(self.check(), 'PASS')

    def test_mid_task_revocation_stops_next_write(self):
        self.assertEqual(self.check(), 'PASS')
        self.state['revoked'] = True
        self.assertEqual(self.check(), 'EXPIRED_SCOPE')

    def test_foreign_current_state(self):
        self.state['project_id'] = 'foreign'
        self.assertEqual(self.check(), 'EXPIRED_SCOPE')

    def test_revision_conflict(self):
        self.state['revision'] = 2
        self.assertEqual(self.check(), 'EXPIRED_SCOPE')

    def test_expiry_boundary_and_future_lease(self):
        for field, value in [('expires_at', '2026-10-02T00:00:00Z'), ('issued_at', '2026-10-02T00:00:01Z')]:
            with self.subTest(field=field):
                task, state = fixture(); task['authorization'][field] = value
                self.assertEqual(authorize(task, state, 'read_repo', now=NOW), 'EXPIRED_SCOPE')

    def test_stale_branch_base_and_repository(self):
        for field, value in [('base_sha', FINAL), ('branch', 'main'), ('full_name', 'other/repo')]:
            with self.subTest(field=field):
                self.state = fixture()[1]; self.state['repository'][field] = value
                self.assertEqual(self.check(), 'INCONCLUSIVE')

    def test_cross_project_or_task_lease(self):
        for field in ['project_id', 'task_id']:
            with self.subTest(field=field):
                self.task = fixture()[0]; self.task['authorization'][field] = 'foreign'
                self.assertEqual(self.check(), 'BLOCKED_PERMISSION')

    def test_path_escape_sibling_and_empty_scope(self):
        for path in ['../scripts/a.py', '/scripts/a.py', 'scripts/../AGENTS.md', 'scripts2/a.py', 'scripts\\a.py', 'scripts//a.py']:
            with self.subTest(path=path):
                self.assertEqual(self.check(paths=[path]), 'BLOCKED_PERMISSION')
        self.assertEqual(self.check(paths=[]), 'BLOCKED_PERMISSION')

    def test_denial_overrides_allowlist(self):
        self.task['authorization']['denied_actions'].append('modify_branch')
        self.assertEqual(self.check(), 'BLOCKED_PERMISSION')

    def test_r0_and_r3(self):
        self.task['risk'] = 'R0'
        self.assertEqual(self.check(), 'BLOCKED_PERMISSION')
        self.task['risk'] = 'R3'
        self.assertEqual(self.check(), 'BLOCKED_APPROVAL')

    def test_unsupported_actions_not_authorized(self):
        for action in ['deploy', 'merge', 'access_secrets']:
            self.assertEqual(self.check(action=action), 'BLOCKED_PERMISSION')

    def test_budgets_and_circuit(self):
        for field, value, expected in [('attempts_used', 2, 'CANCELLED'), ('elapsed_seconds', 600, 'CANCELLED'), ('circuit_open', True, 'UNAVAILABLE')]:
            with self.subTest(field=field):
                self.state = fixture()[1]; self.state[field] = value
                self.assertEqual(self.check(), expected)
        self.state = fixture()[1]; self.state['external_writes_used'] = 1
        self.assertEqual(self.check(action='create_pr'), 'CANCELLED')
        self.assertEqual(self.check(external=True), 'CANCELLED')

    def test_schema_rejects_unknown_authority_and_negative_budget(self):
        self.task['authorization']['operator_approved'] = True
        with self.assertRaises(ValidationError): self.check()
        self.task = fixture()[0]; self.task['budgets']['max_attempts'] = 0
        with self.assertRaises(ValidationError): self.check()

    def test_timezone_required(self):
        self.task['authorization']['expires_at'] = '2026-10-02T01:00:00'
        with self.assertRaises(ValidationError): self.check()


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.task, _ = fixture()
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        artifact = self.root / 'check.txt'; artifact.write_text('actual check output\n')
        self.evidence = dict(schema_version='1.0.0', task_id='task-1', project_id='team', status='PASS',
                             observed_base_sha=BASE, final_sha=FINAL, changed_files=['scripts/check.py'],
                             checks=[dict(command='python -m unittest', exit_code=0, artifact='check.txt',
                                          sha256=hashlib.sha256(artifact.read_bytes()).hexdigest())],
                             ci=dict(head_sha=FINAL, status='success'), failures=[], external_writes=0)

    def check(self):
        return verify_evidence(self.task, self.evidence, self.root, FINAL)

    def test_valid_record(self): self.assertEqual(self.check(), [])

    def test_missing_failed_duplicate_command(self):
        for mode in ['missing', 'failed', 'duplicate']:
            with self.subTest(mode=mode):
                original = copy.deepcopy(self.evidence)
                if mode == 'missing': self.evidence['checks'] = []
                if mode == 'failed': self.evidence['checks'][0]['exit_code'] = 1
                if mode == 'duplicate': self.evidence['checks'] *= 2
                self.assertTrue(self.check()); self.evidence = original

    def test_stale_final_and_ci(self):
        for field in ['final_sha', 'ci']:
            original = copy.deepcopy(self.evidence)
            self.evidence[field] = BASE if field == 'final_sha' else dict(head_sha=BASE, status='success')
            self.assertTrue(self.check()); self.evidence = original

    def test_artifact_tampering_and_missing(self):
        (self.root / 'check.txt').write_text('altered')
        self.assertIn('artifact hash mismatch', self.check())
        (self.root / 'check.txt').unlink()
        self.assertIn('missing/unsafe check artifact', self.check())

    def test_artifact_escape_and_symlink(self):
        self.evidence['checks'][0]['artifact'] = '../elsewhere.txt'
        self.assertIn('missing/unsafe check artifact', self.check())
        (self.root / 'link').symlink_to('/etc/hostname')
        self.evidence['checks'][0]['artifact'] = 'link'
        self.assertIn('missing/unsafe check artifact', self.check())

    def test_failures_scope_r0_and_budget(self):
        self.evidence['failures'] = ['unresolved failure']; self.assertTrue(self.check())
        self.evidence['failures'] = []; self.evidence['changed_files'] = ['AGENTS.md']; self.assertTrue(self.check())
        self.evidence['changed_files'] = ['scripts/check.py']; self.task['risk'] = 'R0'; self.assertTrue(self.check())
        self.task['risk'] = 'R1'; self.evidence['external_writes'] = 2; self.assertTrue(self.check())

    def test_nonpass_preserves_failure(self):
        self.evidence['status'] = 'FAIL'; self.evidence['checks'][0]['exit_code'] = 1
        self.evidence['failures'] = ['test failed']; self.evidence['ci']['status'] = 'failure'
        self.assertEqual(self.check(), [])

    def test_cross_project_identity(self):
        self.evidence['project_id'] = 'other'; self.assertTrue(self.check())


class PreflightTests(unittest.TestCase):
    def test_unavailable_cli(self):
        with patch('scripts.preflight.shutil.which', return_value=None):
            self.assertEqual(probe()['status'], 'UNAVAILABLE')

    def test_authentication_never_proves_execution(self):
        import subprocess
        with patch('scripts.preflight.shutil.which', return_value='/codex'), patch('scripts.preflight.subprocess.run', side_effect=[subprocess.CompletedProcess([], 0, 'codex-cli 0.159.3', ''), subprocess.CompletedProcess([], 0, '--json --sandbox --ephemeral --output-schema', ''), subprocess.CompletedProcess([], 0, '', '')]):
            self.assertEqual(probe()['status'], 'INCONCLUSIVE')

    def test_probe_timeout(self):
        import subprocess
        with patch('scripts.preflight.shutil.which', return_value='/codex'), patch('scripts.preflight.subprocess.run', side_effect=subprocess.TimeoutExpired('codex', 10)):
            self.assertEqual(probe()['status'], 'UNAVAILABLE')


if __name__ == '__main__': unittest.main()
