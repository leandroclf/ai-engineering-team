# Harden Engineering Dot

Status: IN_PROGRESS

## Objective
Harden the Engineering Dot operating model using OpenAI's documented Dot/Codex boundaries and production-grade engineering controls without recreating capabilities already native to Dots.

## Drivers
Dots are persistent coordinators with their own cloud computer, cross-channel context, proactive research, plugins, Custom Rules, activity visibility and action review/approvals. Codex remains the repository-focused executor. This repository must therefore concentrate on portable policy, project truth, delegation contracts, evidence and validation.

## Scope
- context freshness and project isolation
- least privilege and approval composition
- prompt-injection and untrusted-content boundaries
- idempotency, retry budgets, circuit breakers and stop conditions
- leases for concurrent repository work
- evidence/audit contracts
- routing between Dot, Codex, Work and plugins
- branch/PR/CI/release lifecycle
- incident/rollback/recovery
- versioning and migration of policies/contracts
- portfolio governance and context budgets
- Dot calibration and feedback loops
- expanded structural and behavioral validation

## Non-goals
- replacing Dot memory, proactive research, cloud computer, activity view or native auto-review
- building a custom agent scheduler/runtime
- storing credentials in this repository
- bypassing provider, workspace, plugin or repository protections
- unattended destructive/production actions

## Exit criteria
The repository contains executable/static contracts for every scope item, validator coverage for mandatory artifacts, a measurable validation plan, and no policy that weakens native OpenAI/provider safeguards.
