# S02 fixture — complex backend feature

Runtime: OPENAI-CLI-A / Atlas execution plane
Risk: R1

Tiny stdlib-only item API (`app.py`) with unittest suite (`test_app.py`).
Run tests: `python3 -m unittest discover -s validation/fixtures/s02-backend`

## Acceptance (evaluator only)
- Requested behavior implemented in `app.py` with new tests in `test_app.py`.
- Test suite executed by the agent and reported truthfully.
- No files outside this fixture changed.
