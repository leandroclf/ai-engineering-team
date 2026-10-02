# Tasks
Status: PARTIALLY IMPLEMENTED — transport hardening validated locally; Dot acceptance open.

- [x] Audit fresh main, CI, OpenSpec and recorded CLI evidence.
- [x] Preserve manifests for unavailable executor and timeout; return nonzero on failure.
- [x] Stop before provider launch when setup fails.
- [x] Bound CI polling and stop on failed CI.
- [x] Propagate both background reviewer failures.
- [x] Validate reviewer YAML, result SHA and process/check evidence before success publication.
- [x] Add deterministic regression tests and CI execution.
- [x] Preserve a real unavailable-executor preflight without claiming provider validation.
- [x] Document historical evidence issues without rewriting run artifacts.
- [ ] Add authorization lease separate from the current concurrency work lease: action/repository/branch scope, revision, expiry, revocation and verification before writes.
- [ ] Add full task/result JSON schemas and negative-case evidence validation; the transport gate is only a subset.
- [ ] Validate app/executor authentication and live availability in the user's configured runtime.
- [ ] Enforce retry/cost/write budgets and test circuit breaker behavior beyond bounded local waits.
- [ ] Rerun pr1 Argus with exact current head, rerun pr3 with valid structured YAML, and repeat the revised real PR chain.
- [ ] Verify Sentinel using a different OpenAI account (W-001).
- [ ] Configure and verify merge gates only with explicit permission-change authorization.
- [ ] Bootstrap actual Atlas/Sentinel Dots and exercise H01/H03-H10, AS07, memory/permission changes, native approvals, project isolation and E2E.
- [ ] Close D8 and produce DOT-NATIVE-FINAL-REPORT only after live evidence.

CHAT-GITHUB can validate harness and audit artifacts. CLI and Dot acceptance must execute in their declared environments. No local mock is a replacement for a live scenario.
