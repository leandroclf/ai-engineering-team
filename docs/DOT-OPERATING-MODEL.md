# Engineering Dot Operating Model

Scope: native persistent Dots. The implemented local `ai-team` command runs bounded tasks on the Linux host; it does not install schedules or instantiate Dots. See [local workflow](LOCAL-LINUX-WORKFLOW.md).
## Loop
Observe approved project context -> identify bounded useful work -> classify/route -> delegate when needed -> collect evidence -> report -> incorporate feedback -> update specs/rules when justified.

This is a behavioral model, not a custom scheduler. Native Dot proactive facilities provide scheduling/execution when available.

## Routing
- Conversation: clarification, prioritization, small analysis.
- Work: substantial research/document/artifact workflow.
- Codex: repository code, commands, tests and review.
- Plugin/app: external source/action required.

## Failure
A failed Codex task returns evidence to the Dot. Bounded remediation/retry is allowed when failure is understood and permissions allow. Repeated or ambiguous failure stops and escalates.

## Feedback
Feedback may update adapters, OpenSpec, skills or Custom Rules. Permission expansion remains explicit.
