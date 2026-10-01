Task `ca02-admin-only`, project `ai-engineering-team`, Atlas/Codex route, R2.

- Fixed the helper to authorize only exact `"admin"`; added regression tests, fixture documentation and validation evidence.
- Four tests passed after reproducing 12 denial failures before the fix. Both repository validation scripts, YAML handoff checks and diff checks passed. The unavailable `python` alias was replaced with `python3`.
- Committed on `main`: remediation `48097b4`; handoff `67fb5a7`. Working tree is clean.
- [Sentinel request](/work/validation/requests/review-request.yaml) and [Claude assurance request](/work/validation/requests/assurance-request.yaml) both bind to full remediation SHA `48097b4f8698b5054c2a6ca38da034bfb9b20478`.

**Governance status: REMEDIATED / PENDING INDEPENDENT REVIEW.** R2 completion remains gated by Sentinel review; the prior HIGH/CRITICAL finding has not been independently closed. No waiver, push, merge or release occurred. Historical defect-detection runs must use the original revision.