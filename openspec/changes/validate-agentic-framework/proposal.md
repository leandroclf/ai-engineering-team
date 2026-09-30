# Proposal: Validate Agentic Framework in Live Codex

Status: PLANNED

## Objective
Turn the current declarative framework into a behaviorally validated Codex engineering operating model using reproducible scenarios, measurable evidence and explicit pass/fail criteria.

## Why
Static repository validation proves structure, not agent behavior. We still need evidence that Codex:
- selects only relevant skills;
- obeys instruction precedence;
- reports failed/skipped checks truthfully;
- stops before R3 actions without explicit approval;
- handles simple work with less orchestration than complex work;
- reconciles specialist conclusions without uncontrolled scope expansion.

## Scope
Create a self-contained behavioral test harness, fixtures, prompts, expected outcomes, evidence ledger, benchmark method and final validation report. Execute scenarios in a live Codex environment.

## Non-goals
- Benchmarking model intelligence against other vendors.
- Performing real production/destructive actions.
- Requiring paid external infrastructure.
- Claiming deterministic behavior from a probabilistic model.

## Safety
R3 is tested with a simulated/designed destructive request. Passing means the agent stops before the side effect. Never create a real destructive production target merely to validate the guardrail.

## Exit criteria
All mandatory scenarios have execution evidence; failures are preserved; benchmark methodology and limitations are documented; OpenSpec requirements are traceable to scenarios; the bootstrap change can be closed only if mandatory acceptance criteria pass or remaining exceptions are explicitly accepted.
