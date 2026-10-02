# Validation matrix

| Requirement | Deterministic check | Runtime closure |
|---|---|---|
| Lease expiry/revocation | AuthorizationTests expiry/revocation/revision cases | Real revocation during Dot task; next side effect blocked |
| Freshness/isolation | Exact task/project/repository/branch/base and path tests | Two projects and concurrent tasks through trusted adapter |
| No implicit R3 | R3 returns BLOCKED_APPROVAL | Native approval flow observed without destructive action |
| Bounded execution | Attempts/time/writes/circuit tests | Persisted atomic budget reservation and bounded real retry |
| Honest evidence | Failed/missing command, stale CI, hash, symlink tests | Independent runner/GitHub reconciliation on new task |
| Executor availability | Missing/timeout/auth-only preflight tests | Authenticated controlled Codex execution, then Dot handoff |
| Independent assurance | Existing reports and W-001 audit | Second account plus Sentinel/Argus review of this implementation |

Unit-test PASS is scoped to the repository checker. It does not close runtime gates.
