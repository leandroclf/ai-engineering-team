# Capability: Quality and Evidence

### QUAL-001 Repository-native validation
Use the repository's existing test, lint, typecheck, build and static-analysis commands when available.

### QUAL-002 Change-focused tests
Behavioral changes MUST add or update appropriate automated tests unless infeasible; infeasibility MUST be reported.

### QUAL-003 Diff review
Before completion, inspect the final diff for regressions, accidental changes, secrets and requirement coverage.

### QUAL-004 Evidence
The completion report MUST name validation commands/checks actually performed and their outcomes.

### QUAL-005 Failure transparency
Failed or skipped validation MUST remain visible in the completion report.
