# Tasks

## Repository preparation (CHAT-GITHUB)
- [x] Audit current main and existing manifests/PR chain.
- [x] Reconcile superseded execution blockers without altering historical runs.
- [x] Add strict task, lease, current-state and execution-evidence JSON schemas.
- [x] Implement bounded authorization and evidence consistency checks.
- [x] Add read-only, timeout-bounded Codex CLI preflight.
- [x] Add failure tests for revocation, expiry, stale base, cross-project scope, R3, budgets, artifacts and false PASS.
- [x] Run repository validators, unit tests and documentation checks.
- [x] Require schema/unit/documentation checks in CI configuration.

## Operational integration (not satisfied by unit tests)
- [ ] Integrate trusted fresh authorization source and before-operation adapter.
- [ ] Implement atomic reservations/lease concurrency and replay-safe idempotency transport.
- [ ] Execute CODEX-PRE-DOT using the authenticated OPENAI-CLI-A runtime with new contracts.
- [ ] Independently review this R2 implementation through Sentinel and Argus.
- [ ] Validate AS07 waiver flow and separate Atlas/Sentinel accounts (W-001).
- [ ] Execute live expiry/revocation, isolation, retry/outage and native R3 approval scenarios.
- [ ] Complete live H01/H03-H10, D8 and DOT-NATIVE-FINAL-REPORT only with runtime evidence.

Repository implementation is reviewable. The OpenSpec change is not operationally DONE.
