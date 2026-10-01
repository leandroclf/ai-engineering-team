# Adopt Claude Independent Assurance

Status: IN_PROGRESS

## Decision
Integrate Anthropic Claude as a vendor-diverse assurance layer behind the existing Atlas + Sentinel architecture.

## Goals
- Add independent cross-vendor review for selected engineering risk.
- Reuse GitHub/OpenSpec/evidence rather than inventing Dot-to-Claude transport.
- Support Claude Code first, optional official GitHub Action second, Agent SDK only when justified.
- Preserve Atlas ownership, Sentinel independence, operator risk acceptance and native approvals.
- Keep Claude read/review-only by default.

## Non-goals
- Replacing Atlas, Sentinel or Codex.
- Consensus by model vote.
- Giving Claude production authority.
- Requiring API-key billing for V1.
- Building a custom multi-agent runtime before evidence demands it.

## Exit criteria
Architecture, contracts, runbook and scenarios are version-controlled and structurally validated. Operational completion requires a real Claude account/Claude Code execution against immutable repository fixtures and preserved evidence.
