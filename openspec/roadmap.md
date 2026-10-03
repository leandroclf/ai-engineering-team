# Roadmap

## Current local workflow — isolated stages (0.2.0)

Atlas/OpenAI planning -> Argus/Claude implementation -> offline host checks -> Sentinel/OpenAI validation -> isolated Atlas/Claude review. Fixed explicit models per stage; existing three agents/coordinator; no gateway, model router or extra service. Track implementation and separate operator acceptance in [isolated stage tasks](changes/isolated-agent-stages/tasks.md). The milestones below retain their original historical evidence.

## M0 — Specification baseline
OpenSpec project and governance baseline. Implemented.

## M1 — Codex-native engineering core
AGENTS.md, skills, workflows, gates and project adapter. Implemented.

## M2 — Stack packs
Java/Spring, Node/TypeScript, Python/FastAPI, AWS and Kubernetes. Implemented baseline.

## M3 — Dot-native alignment
Engineering Dot as persistent coordinator; Codex as repository executor; bootstrap, Custom Rules, delegation, project registry and plugin policy. Implemented baseline.

## M4 — Production hardening
Freshness/isolation, untrusted-content defense, idempotency/retry/circuit controls, leases, routing, delivery lifecycle, recovery, versioning, portfolio governance and context budgets. Implemented structurally; live validation pending.

## M5 — Dot-native behavioral validation
Validate routing, Dot -> Codex handoff, repository revalidation, permission denial, prompt injection, R3/native approval composition, idempotent retry, lease conflict, failure remediation and engineering scenarios with preserved evidence.

## M6 — Portfolio operation
Operate multiple registered projects with isolated context, leases, evidence ledger, feedback-to-spec loop and status reporting. Measure rework, false completion, stale-context incidents and unnecessary delegation.

## M7 — Specialized dots
Evaluate promotion of proven specialist Skills into specialized dots only when platform support and measured recurring benefit justify it. Preserve bounded delegation and isolated permissions.

## M8 — Continuous engineering
Use native proactive/always-on Dot capabilities for controlled portfolio monitoring and bounded work. Do not recreate a competing scheduler/runtime.

## M9 — Atlas + Sentinel independent assurance
Operate Atlas on the primary account as Engineering Lead and Sentinel on the secondary account as independent Quality/Security reviewer. Coordinate through immutable GitHub/OpenSpec/evidence contracts, asymmetric permissions and explicit disagreement/waiver handling. Structural model implemented; live two-account validation pending.

## M10 — Execution environment enforcement
Bind every remaining task to its authorized runtime: CHAT-GITHUB for repository governance/preparation/evidence inspection, OPENAI-CLI-A for Codex execution with the configured OpenAI subscription, OPENAI-DOT-A/B for live Atlas/Sentinel behavior, CLAUDE-CLI for Claude Code with the configured Claude subscription, CROSS-ENV for end-to-end scenarios, and HUMAN for explicit account/approval actions. No silent environment substitution; unavailable runtime evidence remains BLOCKED/INCONCLUSIVE.
Status 2026-10-01: CLAUDE-CLI/Argus executed and validated (validation/ARGUS-ASSURANCE-REPORT.md); OPENAI-CLI-A blocked by host sandbox restriction; OPENAI-DOT-A/B pending operator.
Update 2026-10-01: all three CLIs run in per-account containers; Atlas/Sentinel/Argus CLI-layer validation recorded in validation/FINAL-REPORT.md (S02 open, W-001 shared OpenAI user).

## Current reconciliation — 2026-10-01

Earlier OPENAI-CLI-A blockers and the open S02 defect above have been superseded: containers enabled CLI execution, S02 reran 3/3 PASS after invariant checks, and GitHub PR/CI transport ran 3/3. W-001, AS07 and live Dots remain open. `harden-dot-native-operations` adds executable repository contracts; trusted adapter integration and live validation remain pending. See `validation/PROJECT-EVOLUTION-2026-10-01.md`.

## Official provider guidance alignment
Repository implementation and tests are prepared in `changes/align-provider-official-guidance/`. Follow the P0/P1 acceptance criteria there for trusted action adapters, credential-free tests, immutable evidence, actual CLI compatibility and distinct Dot cancellation/revocation behavior. D8 remains open.

## M11 — Local Linux workflow (2026-10-03)

Implemented and merged via PR #12 (`68f7f60`): install once, role logins, external target config, independent clone, host commits, isolated offline checks, two exact-head reviews, bounded repair/recovery and explicit delivery. Real credential-free Docker/installation canaries passed in CI. Authenticated operator-host acceptance and account independence remain open in [local tasks](changes/local-linux-workflow/tasks.md). This does not close live Dot or trusted per-tool adapter gates.

## M12 — Documentation and bootstrap alignment

Reconcile current local operation with native Dot templates and historical validation harness; update installation from main, onboarding, recovery, delivery and documentation navigation. Harden bootstrap preflight/destination/build ordering and include executable regression/link checks. Track acceptance in [documentation alignment](changes/align-workflow-documentation/tasks.md).
