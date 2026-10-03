# Claude Independent Assurance Layer

## Implemented local path

In [ai-team](LOCAL-LINUX-WORKFLOW.md), Argus is mandatory for each task, uses restricted Claude Code with Read/Grep/Glob, and returns the JSON review schema enforced by the coordinator. Host checks run separately without credentials. The selected-risk routing and optional Action/SDK modes below describe native/future architecture; they are not activated by local installation. CLI structured output is not proof of account identity or a correct review.

## Decision
Add Claude as a **third, vendor-diverse assurance layer**, not as another general-purpose coordinator.

Topology:

Operator -> Atlas -> Codex -> branch/PR/CI -> Sentinel -> Claude assurance -> Atlas/operator.

Atlas remains Engineering Lead. Sentinel remains the OpenAI-account-independent Quality/Security gate. Claude supplies an additional independent model/vendor perspective for selected high-risk or ambiguous changes.

## Why this role
Anthropic's official Claude Code model supports repository work, custom subagents with isolated context and tool restrictions, hooks/skills, and a GitHub Action. The Agent SDK also exposes Claude Code-style agent capabilities programmatically.

We do not depend on a native OpenAI Dot <-> Claude direct messaging protocol. GitHub, immutable revisions, OpenSpec and evidence remain the interoperability substrate.

## Default routing
- R0/R1: Claude optional, sampled or requested.
- R2: Claude recommended for security/auth, architecture, migrations, dependencies, infrastructure, sensitive data and disputed Sentinel findings.
- R3: Claude may review evidence but **cannot authorize** production/destructive action. Operator + native/provider approvals remain mandatory.
- Sentinel HIGH/CRITICAL dispute: route to Claude as independent evidence generator, never as a majority-vote tie breaker.

## Integration modes
1. **Claude Code interactive/CLI** — preferred initial path when the operator already has an eligible Claude subscription.
2. **Claude Code GitHub Action** — optional automation. Official Anthropic setup supports API-key auth or a Claude Code OAuth token for eligible Pro/Max users. Secrets/tokens are never stored in this repository.
3. **Claude Agent SDK** — future programmatic path when orchestration value justifies a custom runtime. Not required for V1.

## Independence rules
Claude receives the immutable change surface and acceptance criteria before Atlas/Sentinel conclusions where practical. It must distinguish observed evidence from supplied claims. A Claude result is revision-bound and becomes stale when the head SHA changes.

Claude cannot:
- self-expand permissions;
- turn a permission denial into authorization;
- waive Sentinel findings;
- bypass R3/native approvals;
- claim tests/checks without evidence;
- silently mutate a reviewed change while acting as independent reviewer.

## Failure containment
Start read-only/review-only. If Claude later receives write capability for remediation, the review must be invalidated and a fresh independent review requested after the new head SHA.

## Evidence
Every Claude assurance result records provider/tool, project, repository, head SHA, requested gates, checks executed, findings, evidence, permission limits, residual risks and timestamp. Results are PASS, PASS_WITH_FINDINGS, BLOCKED or INCONCLUSIVE.

## Evolution
Do not add a custom cross-vendor agent runtime until the GitHub/OpenSpec transport shows measurable limitations. Prefer native Claude Code/Action primitives and keep the governance contracts portable.
