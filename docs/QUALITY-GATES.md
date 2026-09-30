# Quality Gates
Apply proportionally to risk.
1. Requirements: acceptance conditions covered.
2. Build/static: native build, lint, formatting, typing or static analysis where configured.
3. Tests: focused tests; broader suite for higher-risk changes where practical.
4. Security: required for R2/R3 and trust-boundary changes.
5. Diff: review final diff for scope and regressions.
6. Evidence: record executed checks and outcomes.
A missing tool is not a passing gate: mark it NOT RUN with reason.
