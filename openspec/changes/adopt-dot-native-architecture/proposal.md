# Proposal: Adopt Dot-Native Engineering Architecture

Status: PLANNED
Priority: HIGH
Depends on: bootstrap-agentic-engineering-team
Supersedes assumptions in: validate-agentic-framework where persistence/orchestration was modeled as repository-owned runtime behavior.

## Objective
Align ai-engineering-team with its final purpose: bootstrap, govern and continuously improve an Engineering Dot that coordinates software-engineering work and delegates deep repository execution to Codex.

## Product boundary
- Dot: persistent coordinator, proactive work, feedback-driven context and plugin-mediated access.
- Codex: repository-focused implementation, testing, review and command execution.
- ai-engineering-team: portable engineering policy, OpenSpec, skills, project adapters, quality gates, evidence contracts and validation suites.
- Plugins/apps: external data/actions under platform/provider permissions.
- Human operator: objectives, feedback and approvals where required.

## Architectural decision
The repository MUST NOT reimplement native Dot capabilities merely to simulate persistence, cloud-computer ownership or always-on scheduling. Repository abstractions MAY define portable state/evidence contracts where they improve auditability and interoperability.

## Outcomes
1. A deterministic bootstrap package for configuring an Engineering Dot.
2. Clear Dot-to-Codex delegation contracts.
3. Plugin permission and approval policy.
4. Project onboarding contract.
5. Dot-native behavioral validation.
6. Migration path from logical specialist skills to specialized dots when supported/appropriate.

## Non-goals
- Building a custom agent runtime.
- Circumventing native OpenAI approvals/safeguards.
- Granting production access by default.
- Assuming all Dot capabilities/interfaces are available in every plan/workspace.

## Exit criteria
Dot bootstrap documentation, rules, delegation protocol, project registry template, plugin policy, onboarding workflow, validation scenarios and migration of prior validation plan are implemented and traceable.
