# Design — Atlas + Sentinel

## Topology
Operator -> Atlas -> Codex A -> branch/PR/CI -> shared evidence -> Sentinel -> Codex B/read-only analysis -> review verdict/findings -> Atlas/operator.

## Atlas
Owns intake, architecture, planning, prioritization, project coordination, OpenSpec, delegation to Codex, remediation and delivery orchestration. Atlas MUST NOT convert its own implementation evidence into independent quality/security approval.

## Sentinel
Owns independent QA, security, architecture-conformance and evidence review. Sentinel starts read-only for repositories and production systems. It may create review artifacts/comments only when explicitly permitted. It does not implement the reviewed change by default.

## Independence
Sentinel SHOULD inspect objective evidence and the changed surface before consuming Atlas's conclusions where practical. Atlas's rationale is then used for comparison, not as ground truth.

## Shared protocol
A review request binds to project, PR/change, base/head SHA, acceptance criteria, risk, evidence locations and requested gates. Sentinel returns PASS, PASS_WITH_FINDINGS, BLOCKED or INCONCLUSIVE plus severity-tagged findings.

## Authority
Native/platform/provider controls remain highest. Operator owns final risk acceptance. Sentinel can block framework completion for unresolved CRITICAL/HIGH findings when the project's gate requires independent review. Atlas can remediate but cannot silently waive Sentinel findings.

## Disagreement
1. Record disputed claim and evidence.
2. Reproduce/validate independently where possible.
3. Atlas may remediate and request re-review.
4. A waiver requires operator identity, rationale, scope and expiry/revisit condition.
5. Security-critical disagreement never becomes PASS by majority vote.

## Privileges
Atlas: project-scoped engineering write as authorized; no blanket production rights.
Sentinel: read/review by default; no production write; no self-expansion of permissions.
Both: separate credentials/connections where supported.

## Concurrency
Atlas owns implementation lease. Sentinel review is non-mutating and may run concurrently after a stable head SHA. If Sentinel is granted remediation write access, it must acquire a separate lease and Atlas pauses overlapping mutation.

## Future native multi-Dot
If OpenAI later exposes native Dot collaboration, it may replace transport/orchestration mechanics, but authority, evidence, independence and gate contracts remain.
