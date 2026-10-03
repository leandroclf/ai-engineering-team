# Objectives and tasks

## D01 — Current operation
- [x] Audit entry points and compare commands with local implementation.
- [x] Document local/Dot/harness distinctions, roles, installation from main and onboarding.
- [x] Update recovery, delivery, version/update and evidence boundaries.

## D02 — Resilient bootstrap
- [x] Read-only preflight, explicit diagnostics and optional user destination.
- [x] Preserve foreign files/directories/broken links and recheck after build.
- [x] Publish a new command only after dependencies/build succeed; wrapper explains missing venv.
- [x] Regression tests for failure and destination interactions.

## D03 — Documentation maintenance
- [x] Refresh consolidated overview/navigation while preserving baseline traceability and historical reports.
- [x] Reconcile roadmap/local acceptance and provide host checklist/prompt template.
- [x] Add local Markdown link/fence validator and CI preflight.
- [x] Run all relevant validators/tests and inspect final diff (91 tests; 116 Markdown documents; consolidated links/IDs; shell syntax and actual help).
- [x] Publish branch/PR #13 and observe exact-head CI real install/isolation canary (`2d4bcf1`; push 37084628900 and PR 37084631354 both SUCCESS).

Repository documentation/bootstrap objectives D01-D03 are validated. Merge remains a separate action; no live account/host gate is closed by this change.

LIVE account/host tasks stay in [local-linux-workflow](../local-linux-workflow/tasks.md); this change does not close them.
