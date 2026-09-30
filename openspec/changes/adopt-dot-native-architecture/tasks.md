# Dot-Native Implementation Plan

## D0 — Architecture
- [ ] Add Dot-native architecture document.
- [ ] Record ADR making Dot the persistent coordinator and Codex the repository executor.
- [ ] Update README architecture and final objective.
- [ ] Mark custom persistence/runtime components as portability contracts, not competing runtime.

## D1 — Dot bootstrap
- [ ] Create Engineering Dot bootstrap instructions.
- [ ] Create Custom Rules template.
- [ ] Define mission, boundaries, escalation and reporting.
- [ ] Define initial feedback/calibration procedure.
- [ ] Define project onboarding procedure.

## D2 — Delegation
- [ ] Create Dot -> Codex task envelope template.
- [ ] Create Codex -> Dot completion/evidence contract.
- [ ] Define retry, remediation and stop rules.
- [ ] Define when Dot should use chat, Work or Codex.

## D3 — Plugins and permissions
- [ ] Create plugin/access matrix template.
- [ ] Define least-privilege defaults.
- [ ] Define GitHub read/write policy.
- [ ] Define CI/observability access policy.
- [ ] Define production/deployment approval policy.
- [ ] Explicitly state that repository policy cannot override native safeguards.

## D4 — Portfolio/project context
- [ ] Add project registry schema/template.
- [ ] Add project adapter onboarding checklist.
- [ ] Define stale-context/revalidation rules.
- [ ] Define cross-project isolation rules.

## D5 — Dot-native validation
- [ ] Update live validation design to include Dot -> Codex handoff.
- [ ] Add scenario: Dot routes repository task to Codex.
- [ ] Add scenario: Dot does not delegate trivial conversational work.
- [ ] Add scenario: stale remembered project context is revalidated.
- [ ] Add scenario: plugin permission denial is surfaced, not bypassed.
- [ ] Add scenario: R3/native approval composition.
- [ ] Add scenario: Codex failure returns to Dot for bounded remediation.
- [ ] Preserve existing S01-S06 where still applicable.

## D6 — Operational model
- [ ] Define daily/continuous operating loop concept without duplicating native scheduler.
- [ ] Define evidence ledger and portfolio status report.
- [ ] Define feedback -> rule/spec improvement loop.
- [ ] Define incident/rollback/escalation path.

## D7 — Future specialized dots
- [ ] Define criteria for promoting a Skill into a specialized Dot.
- [ ] Define inter-dot delegation constraints.
- [ ] Keep Tech Lead ownership singular unless evidence supports another topology.

## D8 — Validation and closure
- [ ] Run structural validation.
- [ ] Execute live Dot bootstrap when the Dot surface is available to operator.
- [ ] Execute Dot-native behavioral scenarios.
- [ ] Remediate failures and rerun affected scenarios.
- [ ] Produce validation/DOT-NATIVE-FINAL-REPORT.md.
- [ ] Update OpenSpec statuses and roadmap.

## Mandatory gates
- No repository rule weakens native safeguards/approvals.
- Dot -> Codex delegation is bounded and evidence-backed.
- Target repository instructions are re-read before mutation.
- Permission denial is never treated as authorization.
- No real destructive production operation is required for validation.
