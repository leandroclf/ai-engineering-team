# Dot-Native Implementation Plan
Status: IN_PROGRESS — pre-Codex preparation implemented.

## D0 — Architecture
- [x] Dot-native architecture document.
- [x] ADR for Dot coordinator / Codex executor boundary.
- [x] README final objective.
- [x] Persistence/runtime documents reframed as portability/governance contracts.

## D1 — Dot bootstrap
- [x] Engineering Dot bootstrap.
- [x] Custom Rules template.
- [x] Mission, boundaries, escalation and reporting.
- [x] Initial calibration and project onboarding procedure.

## D2 — Delegation
- [x] Dot -> Codex task envelope.
- [x] Codex -> Dot result/evidence contract.
- [x] Retry/remediation/stop model.
- [x] Conversation vs Work vs Codex routing.

## D3 — Plugins and permissions
- [x] Plugin/access matrix template.
- [x] Least-privilege defaults.
- [x] GitHub policy.
- [x] CI/observability policy.
- [x] Production approval policy.
- [x] Native safeguards explicitly authoritative.

## D4 — Portfolio/project context
- [x] Project registry template and self-registration.
- [x] Project onboarding checklist.
- [x] Stale-context revalidation.
- [x] Cross-project isolation guidance.

## D5 — Dot-native validation
- [x] Define Dot -> Codex validation requirement.
- [x] Define repository routing scenario requirement.
- [x] Define no-unnecessary-delegation requirement.
- [x] Define stale-context scenario.
- [x] Define permission-denial scenario.
- [x] Define R3/native approval scenario.
- [x] Define Codex failure/remediation scenario.
- [x] Preserve Codex-layer S01-S06.
- [ ] Execute live Dot-native scenarios.

## D6 — Operational model
- [x] Native operating-loop concept without custom scheduler.
- [x] Evidence ledger and portfolio status template.
- [x] Feedback -> rule/spec improvement loop.
- [x] Failure/escalation model.

## D7 — Future specialized dots
- [x] Promotion criteria from Skill to specialized Dot.
- [x] Inter-dot delegation constraints.
- [x] Singular integration ownership by default.

## D8 — Validation and closure
- [x] Run structural validator in an execution environment.
- [x] Confirm GitHub CI execution.
- [ ] Execute Codex-layer behavioral scenarios.
- [ ] Execute live Dot bootstrap when available.
- [ ] Execute live Dot-native behavioral scenarios.
- [ ] Remediate failures and rerun affected scenarios.
- [x] Produce pre-Dot execution report (`validation/PRE-DOT-EXECUTION-REPORT.md`); Codex-specific behavioral report remains pending.
- [ ] Produce validation/DOT-NATIVE-FINAL-REPORT.md.
- [ ] Mark proposal/roadmap DONE only with evidence.

## Handoff
Codex should begin with `codex-handoff.md`. Everything above that can be prepared statically is implemented. D8 intentionally remains open because it requires actual execution evidence.

## Mandatory gates
No repository rule weakens native safeguards. Delegation is bounded/evidence-backed. Repository state is re-read before mutation. Permission denial is never authorization. No real destructive production operation is required for validation.

## Execution environment binding
See `docs/EXECUTION-ENVIRONMENTS.md`. D8 Codex-layer execution is **OPENAI-CLI-A**; live bootstrap/routing/native approval is **OPENAI-DOT-A** (+ **HUMAN** where approval/account action is required); repository preparation/final report compilation is **CHAT-GITHUB** after runtime evidence exists.
