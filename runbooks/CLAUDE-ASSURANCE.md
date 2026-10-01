# Claude Assurance Runbook

## Initial setup
1. Use a Claude account/subscription eligible for Claude Code.
2. Install/authenticate Claude Code using Anthropic's current official instructions.
3. Start with repository read/review permissions only.
4. Give Claude this repository's governance, the assurance request, and the immutable target revision.
5. Do not copy secrets, production credentials or unrestricted account context into prompts.
6. For GitHub automation, prefer the official Claude Code GitHub Action and the least-privilege authentication mode available to the account. Keep credentials in GitHub secrets/provider identity, never in source.
7. Do not enable an Agent SDK/custom service for V1 unless CLI/Action cannot meet measured requirements.

## Review procedure
1. Verify repository + base/head SHA.
2. Read nearest AGENTS/OpenSpec/project rules.
3. Inspect diff and objective evidence before relying on Atlas/Sentinel conclusions where practical.
4. Execute only allowed read/review checks.
5. Record findings and exact evidence.
6. Return CLAUDE-ASSURANCE-RESULT.
7. If head SHA changes, mark prior result stale and re-review.

## Disagreement
Claude is an evidence-producing third perspective. It does not decide by vote. For a disputed HIGH/CRITICAL finding, reproduce the claim independently and return evidence. Operator risk acceptance and native approvals remain authoritative.

## Promotion
Only automate Claude on every applicable PR after pilot measurements show useful defect discovery/reduced review risk without unacceptable latency, cost or false positives.
