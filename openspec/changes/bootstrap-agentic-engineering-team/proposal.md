# Proposal: Bootstrap Agentic Engineering Team

Status: PLANNED

## Problem
Codex can execute engineering work, but repeated ad-hoc prompts create inconsistent planning, testing, review and architectural behavior across repositories.

## Proposed change
Build a portable engineering-agent framework centered on a Tech Lead orchestrator, reusable skills, repository instructions, quality gates and explicit workflows.

## Scope
- Root AGENTS.md contract.
- Tech Lead orchestration skill.
- Architect, backend, QA, security, review and observability skills.
- Feature, bugfix, refactor and architecture-review workflows.
- Definition of Done and risk model.
- Project adapter template.
- Validation strategy.
- Documentation and examples.

## Outcomes
Operators should be able to request a task with a short instruction while the framework consistently discovers repository context, plans work, selects specialist capabilities, executes validation and reports evidence.

## Risks
- Excessive role decomposition can waste context/tokens.
- Generic rules can conflict with local project conventions.
- False autonomy can encourage unsafe writes/deployments.
- Large instruction sets can dilute important constraints.

## Mitigations
- Tech Lead selects only necessary capabilities.
- Local repository instructions have explicit precedence.
- High-risk actions require explicit authorization.
- Keep root instructions concise and load detail on demand.
