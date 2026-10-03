# OpenSpec

This directory is the source of truth for planned changes.

Current implemented local capability: [local-linux-workflow](changes/local-linux-workflow/tasks.md). Current documentation/bootstrap maintenance: [align-workflow-documentation](changes/align-workflow-documentation/tasks.md). Consult [roadmap](roadmap.md) for reconciliation; completed static tasks do not close pending LIVE acceptance.

## Lifecycle
1. Read `project.md` and relevant specs.
2. Create a change under `changes/<change-id>/`.
3. Write `proposal.md`, `design.md`, and `tasks.md`.
4. Add spec deltas under `specs/` when behavior/capabilities change.
5. Implement tasks in dependency order.
6. Validate acceptance criteria and record evidence.
7. Archive completed changes instead of silently rewriting history.

## Status vocabulary
PLANNED, IN_PROGRESS, BLOCKED, VALIDATED, DONE.

## Change naming
Use kebab-case, outcome-oriented names, e.g. `bootstrap-agentic-engineering-team`.
