# Implementation Plan

## Phase 0 — Foundation
- [x] Define repository conventions.
- [x] Create concise root AGENTS.md.
- [x] Document instruction precedence and autonomy boundaries.
- [x] Define risk classes R0-R3.

## Phase 1 — Core orchestration
- [x] Implement Tech Lead skill.
- [x] Add context-discovery contract.
- [x] Add task classification and planning contract.
- [x] Add specialist-selection rules.
- [x] Define structured completion report.

## Phase 2 — Specialist capabilities
- [x] Architect skill.
- [x] Backend skill.
- [x] QA skill.
- [x] Security skill.
- [x] Code-review skill.
- [x] Observability skill.
- [x] Define bounded specialist interface.

## Phase 3 — Engineering workflows
- [x] Feature workflow.
- [x] Bugfix workflow.
- [x] Refactoring workflow.
- [x] Architecture-review workflow.
- [x] Dependency-change workflow.
- [x] Incident/investigation workflow.

## Phase 4 — Quality system
- [x] Definition of Done.
- [x] Quality gates.
- [x] Test/validation strategy.
- [x] Security/autonomy guidance.
- [x] Architecture decision template.
- [x] Evidence/report template.

## Phase 5 — Project portability
- [x] PROJECT-AGENTS template.
- [x] Stack-selection guidance.
- [x] Java/Spring extension.
- [x] Node/TypeScript extension.
- [x] Python/FastAPI extension.
- [x] AWS/Kubernetes extensions.

## Phase 6 — Automation/integration
- [x] GitHub workflow skill.
- [x] MCP/tool integration contract.
- [x] CI validation workflow.
- [x] PR/branch operating guidance.
- [x] Safe commit/delivery policy.

## Phase 7 — Advanced agentic operation
- [x] Define subagent delegation protocol.
- [x] Parallel-work and reconciliation rules.
- [x] Session/persistence abstraction.
- [x] Budget/context guidance.
- [x] Loop termination and failure recovery.

## Phase 8 — Validation
- [x] Create acceptance scenarios.
- [x] Add executable structural validator.
- [x] Add CI workflow for structural validation.
- [x] Execute live Codex benchmark: simple vs complex tasks (`validation/FINAL-REPORT.md`; S02 FAIL 2/3 preserved). Earlier note: BLOCKED 2026-10-01: Codex CLI authenticated but its bwrap sandbox cannot start on this host (AppArmor restricts unprivileged user namespaces); evidence `validation/runs/20261001-s01-r1`; see `validation/ARGUS-ASSURANCE-REPORT.md`.
- [x] Execute behavioral instruction-precedence scenario (S03 PASS 3/3 after fixture fix).
- [x] Execute behavioral failure-transparency scenario (S04 PASS 3/3).
- [x] Execute behavioral R3 approval-gate scenario (S05 FAIL 3/3, remediated in 2ccd7a3, rerun PASS 3/3).
- [x] Document limitations and supported validation modes.

## Exit criteria
Static framework implementation is complete. Final behavioral validation remains open until the scenarios are executed in a live Codex runtime and evidence is recorded. No unexecuted behavioral check may be marked passing.

## Execution environment for remaining Phase 8 work
See `docs/EXECUTION-ENVIRONMENTS.md`. The unchecked live Codex benchmark and behavioral scenarios are **OPENAI-CLI-A** tasks using the configured OpenAI subscription account; R3 approval additionally requires **HUMAN**. This ChatGPT/GitHub environment may prepare fixtures and inspect evidence, but must not mark those runtime scenarios PASS.
