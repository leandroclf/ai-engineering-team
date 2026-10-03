# ai-engineering-team — OpenSpec Project

## Implemented operation

The Linux `ai-team` CLI supplies a bounded local coordinator around official Codex/Claude CLIs, isolated checks and explicit branch/PR delivery. It is not a persistent proprietary model runtime. See [local operation change](changes/local-linux-workflow/tasks.md) and [Linux guide](../docs/LOCAL-LINUX-WORKFLOW.md). Native Dot/portfolio behavior and authenticated operator-host acceptance remain separate goals.

## Vision
Create a reusable agentic software-engineering operating model for Codex. A Tech Lead coordinates specialized capabilities and applies repository-local context, quality gates, evidence-based validation, and controlled autonomy.

## Goals
- Reusable across repositories and technology stacks.
- Minimize repeated prompting.
- Separate durable project instructions from specialized skills.
- Support progressive autonomy: advisory -> implementation -> validation -> delivery.
- Make every completion evidence-based.
- Remain usable without paid API dependencies in V1.
- Provide an evolution path toward persistent sessions, MCP integrations and multi-agent orchestration.

## Non-goals (V1)
- A proprietary agent runtime.
- Unattended production deployment.
- Replacing repository-specific engineering standards.
- Pretending that role prompts are independent persistent agents.

## Architecture principles
1. Context before action.
2. Small AGENTS.md; detailed procedures live in skills/specs.
3. Progressive disclosure of context.
4. Least privilege for tools.
5. Human gates for irreversible/high-risk operations.
6. Tests and validation are evidence, not ceremony.
7. Specialist roles are capabilities; orchestration is owned by Tech Lead.
8. Repository-local rules override generic defaults when compatible with safety.

## Primary personas
- Tech Lead / operator
- Architect
- Backend engineer
- QA engineer
- Security reviewer
- Code reviewer
- Observability engineer

## Success criteria
A user can attach the framework to a repository, issue a concise engineering objective, and receive a planned, implemented, tested and reviewed change with traceable evidence and explicit residual risks.
