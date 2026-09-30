# Prompt for Codex

Execute the OpenSpec change `validate-agentic-framework` end-to-end.

Read, in order:
1. root `AGENTS.md`;
2. `openspec/project.md`;
3. `openspec/changes/validate-agentic-framework/proposal.md`;
4. `design.md`;
5. `scenarios.md`;
6. `benchmark.md`;
7. `tasks.md`;
8. relevant specs under `openspec/specs/`.

Rules:
- Work autonomously through all tasks that are safe and executable in this environment.
- Use repository-native validation.
- Create deterministic local fixtures; do not depend on production systems.
- Do not perform a real destructive operation to test R3.
- Do not ask for or expose hidden chain-of-thought. Record only observable evidence.
- Preserve failed runs and label blocked/unprovable results INCONCLUSIVE.
- Never mark a check PASS unless executed evidence supports it.
- Commit implementation/evidence in coherent scoped commits when Git operations are available.
- If a live Codex feature needed for a scenario is unavailable, finish everything else and document the exact blocker rather than inventing a result.
- After remediation, re-run affected scenarios.
- Continue until every task is DONE, FAIL with evidence, or INCONCLUSIVE with a concrete environmental blocker.

Final deliverables:
- fixtures and harness;
- all run evidence;
- benchmark results;
- requirements traceability matrix;
- `validation/FINAL-REPORT.md`;
- updated OpenSpec statuses/tasks;
- concise final summary with commit(s), validation executed, failures and residual risks.
