# Design — Production Hardening

## Control planes
1. **Native Dot plane** — identity, memory/context, proactive research, computer/browser, plugins, activity view, Custom Rules and native action review.
2. **Engineering governance plane** — this repository: OpenSpec, AGENTS, Skills, registry, routing, risk, evidence and policies.
3. **Execution plane** — Codex for repository engineering; Work for research/artifacts; plugins for external systems.
4. **Repository plane** — target repo instructions, branch protections, CI, tests and deployment controls.

A lower plane may add stricter controls but never weaken a higher/native control.

## Freshness protocol
Every mutating task MUST bind to project id, repository, branch/base SHA, relevant instruction version and observed state. Re-read before mutation and again before merge/release. Stale or conflicting state invalidates the lease and requires re-planning.

## Isolation
Context is project-scoped by default. Cross-project facts are references, not implicit instructions. Secrets, customer data and environment-specific details never flow across projects unless explicitly authorized and necessary.

## Concurrency
Mutating work uses a logical lease keyed by repository + change surface. Lease contains owner/task, base SHA, scope, expiry and conflict policy. Conflicting leases stop or rebase/re-plan; never silently overwrite.

## Reliability
External actions require an idempotency key when supported. Retries are bounded, exponential where applicable, and only for retryable failures. Authentication/authorization, validation, policy denial and destructive ambiguity are non-retryable. Circuit breakers stop repeated failing automation.

## Routing
- Dot: persistent coordination, portfolio state, proactive triage, user interaction.
- Codex: code, tests, commands, reviews, repository changes.
- Work: deep research and deliverable-heavy knowledge work.
- Plugin: narrow external read/write action under its native permissions.
Use the least-capable surface that can safely complete the task.

## Change lifecycle
INTAKE -> FRESHNESS -> CLASSIFY -> LEASE -> PLAN -> EXECUTE -> VERIFY -> REVIEW -> PR -> CI -> APPROVAL -> MERGE -> RELEASE -> OBSERVE -> CLOSE.
Not every task reaches release. R3 and provider-sensitive actions require explicit/native approval.

## Evidence
Every material task records task id, project, base/head SHA, policy versions, risk, route, commands/checks, outcomes, approvals, external mutations, failures, residual risk and final state. Evidence never claims hidden reasoning.

## Recovery
Failure after mutation triggers: freeze further mutations, capture evidence, assess blast radius, rollback/revert when safe, validate recovery, report residual impact and create regression coverage.

## Versioning
Policies/templates/contracts carry schema_version. Breaking changes require migration notes and compatibility strategy. Project registry entries declare compatible governance version.
