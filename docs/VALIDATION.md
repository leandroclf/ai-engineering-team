# Validation Strategy
The repository uses a lightweight executable validator because the framework is primarily declarative Markdown.

`python scripts/validate.py` checks mandatory artifacts, Skill frontmatter and core AGENTS contract markers. GitHub Actions runs it on pushes and pull requests.

Scenario-level validation is defined in `tests/scenarios.md`. Behavioral benchmarking against live Codex executions requires a Codex runtime and is intentionally reported separately from static repository validation; it must never be marked passing without execution evidence.
