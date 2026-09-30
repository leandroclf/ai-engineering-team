# ai-engineering-team

Engineering operating system and bootstrap source for an OpenAI Engineering Dot.

## Final architecture
Human -> Engineering Dot -> ai-engineering-team governance -> Codex / Plugins -> target repositories -> evidence / PR -> approval where required.

The Dot is the persistent coordinator. Codex is the default executor for non-trivial repository engineering. This repository supplies OpenSpec, AGENTS rules, skills, project adapters, quality gates, delegation contracts and validation.

## Start here
- `docs/DOT-NATIVE-ARCHITECTURE.md`
- `templates/ENGINEERING-DOT-BOOTSTRAP.md`
- `templates/DOT-CUSTOM-RULES.md`
- `templates/DOT-CODEX-TASK.md`
- `templates/PROJECT-REGISTRY.yaml`
- `openspec/changes/adopt-dot-native-architecture/`

## Skills
Core: tech-lead, architect, backend, qa, security, code-review, observability.
Stack: java-spring, node-typescript, python-fastapi, aws, kubernetes.
Workflow: github-workflow.

## Governance
R0 read-only; R1 reversible local; R2 dependency/schema/infrastructure/security-sensitive; R3 production/destructive/irreversible. Native platform/plugin/provider safeguards remain authoritative; repository policy may be stricter, never weaker.

## Principle
Do not build a competing agent runtime. Use native Dot capabilities for persistent/proactive coordination and Codex for repository execution while keeping engineering policy portable and version-controlled here.
