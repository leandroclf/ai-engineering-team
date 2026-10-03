# Atlas + Sentinel Architecture

## Local CLI contract

The [local workflow](LOCAL-LINUX-WORKFLOW.md) uses these responsibilities without instantiating Dots: Atlas implements, host commits/tests offline, Sentinel and Argus review the same immutable SHA before delivery. Both reviews are mandatory for every local task, a stricter gate than the native routing defaults below. Separate login volumes do not prove distinct accounts; the operator must verify identity.

## Purpose
Create complementary engineering intelligence instead of two identical agents.

**Atlas** optimizes for correct delivery. **Sentinel** optimizes for independent detection of reasons a change should not yet be accepted.

## Flow
1. Operator gives objective to Atlas.
2. Atlas binds project state and risk, plans and delegates repository work to Codex.
3. Codex produces a branch/PR, tests and evidence.
4. Required CI runs.
5. For gated work Atlas emits an Atlas -> Sentinel review request pinned to immutable revisions.
6. Sentinel independently inspects diff/code/tests/evidence and runs allowed checks.
7. Sentinel returns a structured verdict and findings.
8. Atlas remediates or escalates a waiver to the operator.
9. Merge/release follows project and native approval policy.

## Required independent review
Default required for R2/R3 and recommended for security/auth, dependencies, schema/migrations, infrastructure, permissions, sensitive data, release/deploy logic and material architecture changes. Projects may require it for additional surfaces.

## Trust model
Neither Dot is a root of trust. Repository truth, observable evidence, native safeguards and explicit operator authorization are authoritative. One Dot's memory is never imported as instructions into the other.

## Failure containment
Sentinel begins read-only. A compromised/mistaken Sentinel therefore cannot normally mutate production or implementation. A mistaken Atlas cannot declare independent review complete without Sentinel evidence when the gate applies.

## Scaling
Multiple projects reuse the same protocol. Reviews are keyed by project + immutable revision. Later specialist Dots can be added behind the same contracts without changing the Atlas/Sentinel authority model.
