# Objectives and acceptance tasks

## L01 — Install once and configure targets
- [x] Linux installer, version/help, doctor and role login.
- [x] External project config, explicit offline image/checks, safe defaults and strict validation.
- [x] Reject non-Git/dirty targets and preserve existing files/branches.

## L02 — Execute one request
- [x] Independent clone, stable task ID/base/config, Atlas planning and changes.
- [x] Host-owned commit and no-effect detection.
- [x] Separate offline test container with no credentials and resource limits.
- [x] Exact-head Sentinel/Argus JSON review and bounded repair loop.

## L03 — Recover safely
- [x] Private atomic state, project/run locks, evidence hashes and bounded logs.
- [x] Status/list, verified stop, stale process reconciliation and checkpoint resume.
- [x] No implicit replay after ambiguous external effects.

## L04 — Deliver explicitly
- [x] Reviewed clean SHA, unchanged target/origin, local artifact/branch.
- [x] Explicit push/PR, no auto merge/deploy, no destructive branch update.
- [x] Reconcile repeated local delivery and stop on unknown push/PR outcome; remote reconciliation remains manual.

## L05 — Verify and document
- [x] Adversarial unit/integration tests with controlled executors.
- [ ] CI offline boundary canary, failure/review/timeout/lock cases.
- [x] Linux setup, first task, diagnostics, recovery and limitations documented.
- [ ] Publish branch/PR and observe exact-head CI.
- [ ] LIVE: real logins and first task on operator Linux host.
- [ ] LIVE: distinct Atlas/Sentinel accounts, stop/revoke and provider failure scenarios.

Do not mark LIVE tasks completed based on deterministic tests or container help probes.
