# ai-engineering-team

Engineering operating system and bootstrap source for an OpenAI Engineering Dot.

## Architecture
Human -> Engineering Dot -> versioned governance -> Codex / Work / Plugins -> target repositories/systems -> evidence -> approval where required.

The Dot is the persistent coordinator. Codex is the default executor for repository engineering. Work handles deep research/artifact-heavy work. Plugins perform narrow external actions under native permissions. This repository owns portable OpenSpec, AGENTS rules, Skills, project adapters, quality gates, reliability/security controls, delegation contracts and validation.

## Start here
- `validation/PROJECT-EVOLUTION-2026-10-01.md` (current evidence and operational gaps)
- `docs/DOT-NATIVE-OPERATION-GATES.md` (executable contracts and limits)
- `openspec/changes/harden-dot-native-operations/`
- `docs/00-toc.md` (consolidated documentation: requirements, business rules, use cases, traceability)
- `docs/DOT-NATIVE-ARCHITECTURE.md`
- `docs/DOT-RELIABILITY.md`
- `docs/CONTEXT-FRESHNESS.md`
- `docs/UNTRUSTED-CONTENT.md`
- `docs/ROUTING-MATRIX.md`
- `docs/DELIVERY-LIFECYCLE.md`
- `templates/ENGINEERING-DOT-BOOTSTRAP.md`
- `templates/POLICY-MANIFEST.yaml`
- `templates/TASK-ENVELOPE.yaml`
- `templates/PROJECT-REGISTRY.yaml`
- `openspec/changes/harden-engineering-dot/`
- `docs/EXECUTION-ENVIRONMENTS.md`
- `runbooks/CONTAINER-RUNTIMES.md`
- `validation/FINAL-REPORT.md`
- `validation/PROJECT-EVOLUTION-REVIEW.md`
- `openspec/changes/harden-dot-native-operations/`

- `docs/PROVIDER-GUIDANCE-REVIEW.md`

## Skills
Core: tech-lead, architect, backend, qa, security, code-review, observability.
Stack: java-spring, node-typescript, python-fastapi, aws, kubernetes.
Workflow: github-workflow.

## Governance
R0 read-only; R1 reversible local; R2 dependency/schema/infrastructure/security-sensitive; R3 production/destructive/irreversible. Native platform/plugin/provider safeguards remain authoritative; repository policy may be stricter, never weaker.

## Reliability model
Mutable state is revision-bound and revalidated. External writes are idempotent where possible, retries are bounded, circuits stop repeated/ambiguous failure, overlapping mutations use leases, and every material task produces observable evidence.

## Principle
Do not build a competing agent runtime. Use native Dot capabilities for persistent/proactive coordination and Codex/Work/plugins for specialized execution while keeping engineering policy portable and version-controlled here.
