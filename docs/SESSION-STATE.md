# Session / Persistence Abstraction
Persistent runtimes should store useful resumable state: objective, decisions, plan status, evidence, blockers and repository revision. Conversation history is not authoritative over current repository state. On resume, revalidate revision and instructions before mutation. Apply context budgets and compact stale detail.

## Local CLI state

`ai-team` stores private atomic state under `$XDG_STATE_HOME/ai-team` (default `~/.local/state/ai-team`). Statuses: RUNNING, REVIEWED, FAILED, STOPPED, DELIVERY_PENDING, DELIVERED. `status` reports INTERRUPTED when the recorded process is stale; this is an observation, not permission to replay.

`resume TASK` accepts only RUNNING with a known checkpoint and no active recorded process. Partial staging or interrupted stages require inspection; FAILED/STOPPED require a new task after resolving the cause. The original deadline remains in force. DELIVERY_PENDING requires manual remote reconciliation. Preserve state/logs/SHAs; do not edit state to force a retry. See [commands and recovery](LOCAL-LINUX-WORKFLOW.md).
