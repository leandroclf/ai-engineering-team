# Isolated stages with three existing agents

## Objective

Replace the local CLI's combined Atlas implementation and Sentinel/Argus reviews with Atlas/OpenAI planning, Argus/Claude implementation, Sentinel/OpenAI validation and an isolated Atlas/Claude review. Keep the existing coordinator and direct official CLIs. No gateway, dynamic routing, fourth agent or new service.

## Acceptance

- Explicit model and effort for each stage, frozen in task configuration.
- Planning before edits, bounded JSON plan, OpenSpec materialization and immutable handoff.
- Only implementation can edit the clone; Git metadata stays read-only to agents.
- Four separate login volumes and fresh sessions; no shared conversation history.
- Offline host checks and both SHA/plan-bound assessments before delivery.
- Failed checks/assessments cause bounded repair; invalid plans cause bounded replanning.
- Legacy configs require explicit upgrade; legacy tasks cannot silently execute/deliver under the new contract.
- Tests cover isolation, order, invalid output, stale evidence, repair and recovery.

## Scope boundary

Historical fixtures, Dot protocols and recorded live-provider results remain historical. Current local operations are documented separately. Real authenticated inference and operator Linux acceptance must be reported independently from controlled tests.
