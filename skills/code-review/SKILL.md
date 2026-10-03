---
name: code-review
description: Performs evidence-based final review of a change.
---
# Code Review
Review the diff, not intent alone. Look for correctness defects, regressions, accidental scope, contract changes, missing tests, unsafe assumptions and secret leakage. Rank findings by impact and cite concrete locations. Do not manufacture findings to fill a checklist.

## Inputs
Immutable diff, objective, acceptance criteria and validation evidence.

## Outputs
Concrete findings, severity, disposition, residual risks and evidence references.

## Boundaries
Review the change surface; do not silently modify it or infer correctness from intent.

## Validation
Check correctness, regressions, scope, contracts, tests, security and accidental secret leakage at concrete locations.
