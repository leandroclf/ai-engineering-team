# Adopt Claude Independent Assurance

Status: IN_PROGRESS

## Decision
Integrate Anthropic Claude as a vendor-diverse assurance layer behind the existing Atlas + Sentinel architecture.

## Execution principle — subscription CLIs are mandatory
From this change forward, **all executable next steps for AI-provider engineering work MUST be performed through each provider's official CLI, authenticated with the operator's already-configured subscription account**.

- OpenAI engineering execution: official OpenAI/Codex CLI using the configured OpenAI subscription account.
- Anthropic engineering/assurance execution: official Claude Code CLI using the configured Claude subscription account.
- Future providers: their official CLI with the operator's configured subscription account, after governance/onboarding approval.
- The architecture MUST prefer subscription-authenticated CLI execution and MUST NOT introduce API-key billing, a custom API integration, or a replacement agent runtime when the provider CLI can perform the required step.
- GitHub/OpenSpec/evidence remain the shared interoperability and audit substrate across CLIs.
- Native provider safeguards, CLI permissions, repository policy and R0-R3 remain authoritative.
- If a required step cannot be executed through the applicable provider CLI, record it as BLOCKED/INCONCLUSIVE and propose the smallest justified exception; do not silently switch to an API.

## Goals
- Add independent cross-vendor review for selected engineering risk.
- Reuse GitHub/OpenSpec/evidence rather than inventing Dot-to-Claude transport.
- Use the providers' official subscription-authenticated CLIs as the execution plane.
- Support Claude Code first; automation/integration beyond the CLI only when measured evidence justifies it.
- Preserve Atlas ownership, Sentinel independence, operator risk acceptance and native approvals.
- Keep Claude read/review-only by default.

## Non-goals
- Replacing Atlas, Sentinel or Codex.
- Consensus by model vote.
- Giving Claude production authority.
- Requiring API-key billing for V1.
- Building a custom multi-agent runtime before evidence demands it.
- Reimplementing capabilities already available in official provider CLIs.

## Exit criteria
Architecture, contracts, runbook and scenarios are version-controlled and structurally validated. Operational completion requires execution through the applicable official CLIs using the operator's configured subscription accounts, against immutable repository fixtures, with preserved evidence.
