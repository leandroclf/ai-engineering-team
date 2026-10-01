Completed `s02-backend` via Codex; risk R1.

- Changed `app.py` and `test_app.py`: DELETE returns 204 with no payload on removal, and 404 for missing items.
- Fixed ID allocation so creation after deletion preserves surviving items.
- Executed `python3 -m unittest discover -s validation/fixtures/s02-backend`: all 6 tests passed.
- Executed `git diff --check`: passed. Reviewed the final diff; only the two fixture files changed.
- No external mutations or additional approvals. No known residual issues.