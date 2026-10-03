---
name: github-workflow
description: Safe GitHub branch, commit, pull-request and CI workflow.
---
# GitHub Workflow
Inspect repository contribution rules. Keep commits scoped and messages descriptive. Do not merge, delete branches, change protections or bypass checks without explicit authorization. Summarize CI evidence and unresolved checks before delivery.

## Inputs
Repository state, branch policy, change scope and validation results.

## Outputs
Scoped branch/commits, pull request, CI evidence and delivery status.

## Boundaries
Do not merge, delete branches, change protections or bypass checks without explicit authorization.

## Validation
Revalidate base/head SHA, inspect diff, confirm required checks and report merge/deploy as separate actions.
