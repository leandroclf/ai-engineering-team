# Tasks

## Implemented in this review
- [x] Consult current official OpenAI, Anthropic and GitHub guides and record sources/date.
- [x] Reconcile PR #10 and #11 changes, preserving historical artifacts and both suites.
- [x] Add and validate structured provider-review schema; require it in the PR chain.
- [x] Block stale SHA, wrong reviewer role, required gate failure and unverified HIGH/CRITICAL findings.
- [x] Adopt explicit unattended permissions and restricted Claude review configuration.
- [x] Extend capability/auth preflight to both providers without logging authentication output.
- [x] Terminate local POSIX process groups on timeout; reject provider error events despite exit zero.
- [x] Remove GitHub/SSH transport credentials from provider child environment and filter sensitive event fields.
- [x] Align container validation dependencies; limit Docker build context.
- [x] Add CI container build and offline/no-login smoke for actual CLI versions and required flags.
- [x] Pin official Actions v7, reduce CI token permissions, add timeout/concurrency and update proposals via Dependabot.
- [x] Run deterministic validation and adversarial tests; record unavailable live executors.

## Follow-up with explicit acceptance
- [ ] P0: Integrate a trusted before-action adapter, atomic reservations, deduplication and revocation checks. Verify no stale lease can reserve a new operation.
- [ ] P0: Separate arbitrary repository tests from provider credentials; enforce egress constraints and prove a controlled canary cannot leave the test environment.
- [ ] P0: Store runner evidence outside agent-writeable paths and corroborate final SHA/CI from GitHub.
- [ ] P1: Run both preflights inside their real authenticated services; report versions/flags and zero leaked auth output.
- [ ] P1: Repeat structured CLI review chain, including pr1/pr3 replacement evidence and one intentionally invalid result.
- [ ] P1: Test Dot pause, child-task stop, schedule disable and admin revocation separately; reconcile in-flight authorized actions and prevent new ones.
- [ ] P1: Resolve W-001 and test AS07/native approval using real accounts and Dots.
- [ ] P1: Configure merge checks/origin with separate authorization; demonstrate a failed or stale review prevents merge.
- [ ] P2: Evaluate Codex App Server and Claude SDK/native hooks as thin adapters; do not assume every operation emits an approval or that a hook is a sandbox.
- [ ] P2: Add release/channel inventory and canary promotion for CLI pins; reject unsupported capabilities without silently upgrading or changing billing.
- [ ] P2: Publish metrics by project/executor: duration, retries, errors, intervention and observable usage.

Repository checks are evidence for the code only. D8 and live hardening remain open.
