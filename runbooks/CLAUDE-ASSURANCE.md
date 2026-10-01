# Claude Assurance Runbook

## Mandatory execution model
All Anthropic assurance/engineering steps in this architecture are executed through **Claude Code CLI using the operator's already-configured Claude subscription account**. OpenAI/Codex engineering steps are executed through the **official OpenAI/Codex CLI using the operator's already-configured OpenAI subscription account**.

GitHub/OpenSpec/evidence are the shared coordination layer between provider CLIs. Do not introduce API keys, API billing, a custom provider runtime or an alternate execution path merely to automate a step that the official CLI can perform. If the required CLI cannot perform a step, stop and record BLOCKED/INCONCLUSIVE until an explicit architectural exception is approved.

## Initial setup
1. Verify Claude Code CLI is installed and authenticated with the intended Claude subscription account.
2. Verify the OpenAI/Codex CLI is installed and authenticated with the intended OpenAI subscription account before OpenAI-side execution.
3. Never commit authentication tokens, cookies, credentials or subscription secrets.
4. Start Claude with repository read/review permissions only.
5. Give Claude this repository's governance, the assurance request and immutable target revision.
6. Do not copy secrets, production credentials or unrestricted account context into prompts.
7. Keep provider-specific authentication outside source control.
8. Do not enable an Agent SDK/custom service or API-key integration unless CLI execution proves insufficient and a future explicit architecture decision approves the exception.

## Review procedure
1. Verify the CLI/provider/account being used and record only non-secret execution metadata.
2. Verify repository + base/head SHA.
3. Read nearest AGENTS/OpenSpec/project rules.
4. Inspect diff and objective evidence before relying on Atlas/Sentinel conclusions where practical.
5. Execute only allowed read/review checks through Claude Code CLI.
6. Record findings and exact evidence.
7. Return CLAUDE-ASSURANCE-RESULT.
8. If head SHA changes, mark prior result stale and re-review through the CLI.

## Cross-provider workflow
Atlas/OpenAI CLI -> repository/OpenSpec/evidence -> Sentinel/OpenAI account review -> Claude Code CLI -> structured assurance result -> Atlas/operator.

The repository is the protocol; provider sessions do not need direct model-to-model messaging.

## Disagreement
Claude is an evidence-producing third perspective. It does not decide by vote. For a disputed HIGH/CRITICAL finding, reproduce the claim independently through Claude Code CLI and return evidence. Operator risk acceptance and native approvals remain authoritative.

## Promotion
Automate additional CLI-driven review only after pilot measurements show useful defect discovery/reduced review risk without unacceptable latency, cost or false positives. Any move from subscription CLI to API/SDK is a separate architecture decision, not a transparent fallback.
