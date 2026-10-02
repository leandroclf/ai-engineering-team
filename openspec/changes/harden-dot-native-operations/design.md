# Design

Keep native Dot coordination and existing CLI harnesses. Add a small repository-side library and JSON Schema contracts, plus a read-only CLI preflight and mandatory CI checks. Native/runtime adapters must supply trusted fresh state, reserve budgets, invoke the checks before operations and reconcile GitHub evidence. This change does not install such an adapter or claim mechanical enforcement over the native Dot.

New schemas are versioned v1 contracts alongside existing YAML templates; historical manifests are not migrated. Exact-match identity/revisions and literal path-prefix scope prevent cross-project and sibling-prefix authorization. Revocation/expiry stop the next checked action. R3 is always handed off. Evidence validation detects contradictory PASS, missing/tampered artifacts and stale CI; it cannot authenticate a runner by itself.

Details and limitations: `docs/DOT-NATIVE-OPERATION-GATES.md`. Keep D8 and live H6 open. CLI behavior already preserved in `validation/FINAL-REPORT.md` must not be rerun conceptually or relabeled as live Dots.

## Transport hardening (integrated from PR #10)

Reuse `provider_run.py`, `pr_chain.sh` and the existing manifest statuses (PASS, FAIL, BLOCKED, INCONCLUSIVE). Missing executable maps to BLOCKED with exit 127; timeout maps to INCONCLUSIVE with exit 124. Ordinary provider/setup/check failures map to FAIL. A successful process remains INCONCLUSIVE until evaluated. All failed checks return a nonzero harness exit.

`review_status.py` requires schema-validated JSON in the PR chain, validates reviewer role and the declared head SHA against the run and expected PR SHA, and verifies provider exit and exact-head check evidence. Quality and security gates must pass, and HIGH/CRITICAL findings must be resolved and verified. Only PASS/PASS_WITH_FINDINGS with acceptable runtime evidence can map to GitHub success. FAIL/BLOCKED are terminal failure; invalid/missing evidence is terminal error. The plain/fenced YAML parser remains available only for historical audits; strict reviews never fall back to prose or YAML.

CI polling defaults to 600 seconds (`CI_TIMEOUT_SECONDS`), then stops. A failed CI does not start reviewers. Each background reviewer PID is awaited separately; either failure produces a nonzero chain exit even when the other succeeds. Existing validation-only PR closure is retained. On earlier failure after PR creation, the PR may remain draft and the operator must inspect recorded transport evidence before cleanup. No automatic production rollback or permission changes are introduced.

These are transport controls, not proof of review correctness, authorized tool execution, account independence, live revocation, or an authenticated Codex/Claude session. Timeout of a CLI client does not prove a remote provider task has stopped; live cancellation must be verified separately.
