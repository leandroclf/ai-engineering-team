# Design

One Python coordinator dispatches four fixed stages through the existing Docker runtime. Atlas has two independent execution contexts, not shared state: `plan/codex` and `review/claude`. Argus owns `implement/claude`; Sentinel owns `validate/codex`.

Defaults reviewed on 2026-10-03: `gpt-6-astra` with `xhigh` for plan/validate; `claude-opus-5-5` with `high` for implement/review. These are task-oriented documented choices, not benchmark-proven superiority. Explicit init overrides allow account-compatible models of the same provider without automatic fallback. Model availability and native policy remain provider-controlled.

CLONE -> PLAN -> IMPLEMENT -> TEST -> REVIEW (validate, review) -> COMPLETE. The original request is always included. The host validates planner JSON, canonical SHA256 plan identity and acceptance coverage, writes a task-scoped OpenSpec change and commits it before implementation. Reviews independently compare request, plan, diff and offline test evidence, with exact acceptance coverage. Replanning consumes the same correction budget.

Stage-specific staging and read-only handoff mounts expose only accepted artifacts. Persistent auth volumes differ per stage. Codex uses ephemeral read-only sessions; Claude uses restricted mode, no persistence, no MCP, no command tools, and file edits only in implementation. Container and native safeguards remain necessary; shared filesystem state and credentials mean isolation is not complete DLP or an independent reviewer identity guarantee.

Config/run version 2 prevents an old checkpoint from being interpreted using changed responsibilities. `init --upgrade` is explicit, backs up old config and requires explicit test image/checks. No running state is migrated. Delivery rechecks current tests and both assessments against plan and HEAD.

Official references: [OpenAI models](https://learn.chatgpt.com/docs/models), [reasoning configuration](https://learn.chatgpt.com/docs/config-file/config-reference), [Claude models](https://platform.claude.com/docs/en/models/overview), [Claude CLI](https://code.claude.com/docs/en/cli-reference).
