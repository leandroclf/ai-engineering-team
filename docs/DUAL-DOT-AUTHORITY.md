# Dual-Dot Authority Matrix

| Action | Atlas | Sentinel | Operator |
|---|---|---|---|
| Intake/prioritize | Owns | Advises | Overrides |
| Architecture proposal | Owns | Reviews | Resolves material dispute |
| Repository implementation | Delegates/owns | No by default | Authorizes scope |
| Tests/CI evidence | Produces/collects | Verifies | — |
| QA/security review | Supplies context | Owns independently | Accepts residual risk |
| R0/R1 completion | Owns subject to project gates | Optional review | May override |
| R2 completion | Remediates | Independent gate by default | May explicitly waive |
| R3 production/destructive | Cannot self-authorize | Cannot authorize | Explicit authorization + native approvals |
| Merge | Per project permission | Does not merge by default | Per project policy |
| Production release | Coordinates only when authorized | Verifies if requested | Explicit authorization |
| Permission expansion | Cannot self-grant | Cannot self-grant | Explicitly authorizes |

## Finding severities
CRITICAL: credible severe security/data/production risk; blocks.
HIGH: material defect/risk; blocks gated completion by default.
MEDIUM: should be fixed or explicitly tracked.
LOW: improvement/non-blocking.
INFO: observation.

A PASS means no blocking finding under the requested gates, not that the system is defect-free.
