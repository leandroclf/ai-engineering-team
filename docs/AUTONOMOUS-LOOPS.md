# Controlled Autonomous Loops
Every loop needs an objective, budget, measurable stop condition, failure threshold and approval policy. Repeated failure stops rather than retrying indefinitely. External or production side effects remain governed by risk class. Event-driven triggers should process work idempotently.

For local `ai-team`, `init` sets per-stage timeout, repair cycles and total task deadline (defaults 900 seconds, 3 cycles, 7200 seconds; maximum 3600, 5, 28800). Background mode is a local process, not a persistent scheduler. Checks and both reviews gate REVIEWED; failure or ambiguity stops the task. Delivery, merge and deployment remain separate. See [local workflow](LOCAL-LINUX-WORKFLOW.md).
