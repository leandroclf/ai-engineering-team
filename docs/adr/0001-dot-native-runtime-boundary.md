# ADR-0001: Dot-native runtime boundary
Status: Accepted

## Context
The project began as a Codex-native engineering framework. Its final objective is to bootstrap and govern an Engineering Dot while using Codex for deep repository execution.

## Decision
OpenAI Dot owns persistent/proactive coordination. Codex owns bounded repository engineering. ai-engineering-team owns portable governance, OpenSpec, skills, adapters, evidence and validation contracts.

We will not build a competing persistence/scheduler/runtime. Session and autonomous-loop documents are portability/governance contracts only.

## Consequences
Repository logic stays portable and auditable. Native platform capabilities are used where available. Native safeguards and provider permissions cannot be weakened by repository rules.
