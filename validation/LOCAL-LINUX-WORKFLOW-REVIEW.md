# Local Linux workflow — review and evidence

Date: 2026-10-02 America/Sao_Paulo. Base main c8e8330. Risk R2; external delivery branch/PR only.

## Delivered repository capabilities
Installed entry point, explicit project config, role login/doctor, foreground/background tasks, independent clone, host-owned Git metadata, offline validation container, exact-head structured reviews, bounded correction cycles, atomic private state, exclusive locks, checkpoint resume, local stop, local branch import and explicit push/draft PR.

## Verification scope
Deterministic tests exercise actual Git clone/commits/import and subprocess failure/timeout; providers are controlled fixtures. They verify target preservation, phase transition/repair exhaustion, stale role/SHA/gate rejection, non-replay of interrupted delivery, private atomic records, locking, parser behavior and credential environment removal. They do not execute a live model or validate subscriptions.

The CI runtime job builds real pinned provider CLIs, probes help/login state without login, and runs a real container canary asserting non-root execution, no account file/API environment/socket, blocked outbound network, writable temporary checkout and unchanged mounted source. CI completion must be observed on the published SHA before reporting PASS.

## Limits that must remain visible
LIVE acceptance on the operator host is open. Account independence, subscription availability, real structured-output transport, native revocation and remote cancellation cannot be inferred from mocks. Interrupted or ambiguous external writes require manual reconciliation. Native before-tool enforcement remains follow-up; Atlas can execute commands under provider policy, despite the instruction that host owns test execution. Host/user/Docker daemon are trusted. No automatic merge/deploy or guarantee of autonomous production readiness.

Guide: docs/LOCAL-LINUX-WORKFLOW.md. Objectives and acceptance: openspec/changes/local-linux-workflow/.
