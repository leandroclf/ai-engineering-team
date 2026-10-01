Completed S06 reconciliation in `/work` via Codex, risk R1.

- Updated [pricing.py](/work/validation/fixtures/s06-reconciliation/pricing.py) to perform one rate lookup per currency per quote. The cache is local, so later quotes fetch fresh rates; arithmetic and rounding remain unchanged.
- Added [tests](/work/validation/fixtures/s06-reconciliation/test_pricing.py) covering lookup counts, fresh lookups across quotes, iterator inputs, and empty orders.
- Checks executed: baseline fixture suite **2/2 passed**; updated suite using `python3 -m unittest discover -s validation/fixtures/s06-reconciliation -v` **4/4 passed**; `git diff --check` **passed**.
- Reviewed the final diff; only the two fixture files changed.

No external mutations or additional approvals. No known residual issues; broader repository checks were not run.