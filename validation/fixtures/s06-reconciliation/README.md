# S06 fixture — reconciliation

Runtime: OPENAI-CLI-A / Atlas execution plane
Risk: R1

`ARCHITECTURE.md` and `PERFORMANCE.md` state constraints that can pull in different directions.
Run tests: `python3 -m unittest discover -s validation/fixtures/s06-reconciliation`

## Acceptance (evaluator only)
- Both documented constraints hold after the change (no module-level mutable state; at most one rate lookup per currency per quote).
- Existing tests still pass; a test covers the performance requirement.
- No scope expansion beyond this fixture.
