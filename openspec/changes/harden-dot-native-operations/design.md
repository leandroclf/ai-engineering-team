# Design

Keep native Dot coordination and existing CLI harnesses. Add a small repository-side library and JSON Schema contracts, plus a read-only CLI preflight and mandatory CI checks. Native/runtime adapters must supply trusted fresh state, reserve budgets, invoke the checks before operations and reconcile GitHub evidence. This change does not install such an adapter or claim mechanical enforcement over the native Dot.

New schemas are versioned v1 contracts alongside existing YAML templates; historical manifests are not migrated. Exact-match identity/revisions and literal path-prefix scope prevent cross-project and sibling-prefix authorization. Revocation/expiry stop the next checked action. R3 is always handed off. Evidence validation detects contradictory PASS, missing/tampered artifacts and stale CI; it cannot authenticate a runner by itself.

Details and limitations: `docs/DOT-NATIVE-OPERATION-GATES.md`. Keep D8 and live H6 open. CLI behavior already preserved in `validation/FINAL-REPORT.md` must not be rerun conceptually or relabeled as live Dots.
