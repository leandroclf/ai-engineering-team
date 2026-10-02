# Tasks
Status: PARTIALLY IMPLEMENTED — repository controls validated; operational integration open.

## Repository contracts and transport
- [x] Audit current main and existing manifests/PR chain; preserve original artifacts.
- [x] Add strict task, authorization lease/current-state and execution-evidence schemas.
- [x] Implement bounded authorization and evidence consistency checks with adversarial tests.
- [x] Add timeout-bounded version/capability/auth preflight for Codex and Claude.
- [x] Preserve unavailable executor/timeout manifests and propagate failed setup/provider/check execution.
- [x] Bound CI polling, require successful CI and await both reviewer processes.
- [x] Require structured provider review, exact SHA, critical gates and no unresolved HIGH/CRITICAL findings.
- [x] Preserve historical audit qualification for pr1/pr3 without rewriting old statuses.
- [x] Run both test suites, schemas, structural validators and documentation checks in CI.
- [x] Reconcile provider guidance and CI/runtime policies in `align-provider-official-guidance`.

## Operational integration
- [ ] Integrate trusted fresh authorization source and before-operation adapter.
- [ ] Implement atomic reservations/lease concurrency and replay-safe idempotency transport.
- [ ] Keep arbitrary test execution and writable evidence outside credential-bearing agent environments.
- [ ] Execute CODEX-PRE-DOT with actual authenticated runtimes and new flags/schemas.
- [ ] Repeat pr1/pr3 and revised PR chain with independently corroborated evidence.
- [ ] Independently review this R2 implementation through Sentinel and Argus.
- [ ] Separate Atlas/Sentinel accounts (W-001), validate AS07 and native approvals.
- [ ] Test expiry/revocation, active versus future operations, project isolation, retries and outages on real Dots.
- [ ] Configure merge protection only with specific operator authorization.
- [ ] Complete live H01/H03-H10, D8 and DOT-NATIVE-FINAL-REPORT only with runtime evidence.

The repository does not grant native permissions. Pause/revocation/cancellation have distinct provider-specific effects. Details and acceptance criteria: `openspec/changes/align-provider-official-guidance/tasks.md`.
