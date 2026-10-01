Task `ca02-admin-only-remediation`, project `ai-engineering-team`; Atlas/Codex route, R2.

- Fixed the helper to allow only exact `"admin"`; added regression tests and updated fixture documentation.
- Tests reproduced eight non-admin failures before the fix; afterward, all nine role cases passed. Both repository validators passed. Diffs and request YAML/SHA bindings checked.
- Remediation commit: `49aa8d4cdefdb68907b65ba0a9063b0cd5c025bd`.
- Handoff commit: `6d8d806b09cdfd835efb6cfbde810cef1029e159`, containing [Sentinel request](/work/validation/requests/review-request.yaml) and [Claude assurance request](/work/validation/requests/assurance-request.yaml), both bound to the remediation SHA.
- Both commits are on `main`; working tree is clean. No push, merge, deployment, or external mutation occurred.

**Governance status: remediated and locally validated; R2 completion remains BLOCKED pending independent Sentinel review.** The prior HIGH/CRITICAL finding is not independently closed; Claude assurance is also pending. Evidence is [recorded here](/work/validation/ca02-remediation-evidence.md).