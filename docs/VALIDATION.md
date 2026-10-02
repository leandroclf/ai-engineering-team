# Validation Strategy
The repository uses lightweight executable validators because the framework is primarily declarative Markdown.

`python scripts/validate.py` checks mandatory artifacts, Skill frontmatter, core AGENTS contract markers, the provider-execution fixtures, and that every `validation/runs/*/manifest.yaml` carries exactly one allowed status (PASS, FAIL, BLOCKED or INCONCLUSIVE).

`python scripts/validate_hardening.py` checks the hardening contracts: required policy tokens, YAML validity of the task envelope, lease, evidence record, policy manifest and project registry, required envelope and lease fields, native-safeguard precedence in the policy manifest, and the H01-H10 scenario list.

GitHub Actions runs both validators on pushes and pull requests (`.github/workflows/validate.yml`, Python 3.12 with PyYAML installed by `pip install pyyaml`).

## What structural validation proves
Artifacts exist, parse and satisfy the checked constraints. It does not prove agent behavior, live Dot behavior, native approvals or independence between accounts. A green CI run must never be reported as behavioral validation.

## Behavioral validation
Scenario-level validation is defined in `tests/scenarios.md` and the scenario files under `validation/`. Runs execute through the provider CLIs with `scripts/provider_run.py` in disposable clones, normally inside the per-account containers described in `runbooks/CONTAINER-RUNTIMES.md`. Evidence is preserved under `validation/runs/<run-id>/`. `scripts/pr_chain.sh` exercises the Atlas -> Sentinel -> Argus chain over GitHub pull requests and CI. Results are summarized in `validation/FINAL-REPORT.md` and the per-agent reports.

Behavioral benchmarking requires a live provider runtime and is reported separately from static validation; it must never be marked passing without execution evidence.

## Executable operation contracts

`python scripts/validate_native_operations.py` validates four JSON schemas and concrete examples. `python -m unittest discover -s tests/unit -v` exercises authorization/evidence/preflight failure boundaries. `python docs/anexos/build/verificar_docs.py` checks the consolidated documentation links and identifiers. Dependencies are pinned in `requirements-validation.txt`; CI installs this file and runs these checks in addition to the original validators.

These tests validate repository functions only. Live adapter enforcement, native approvals and Dot behavior still require runtime evidence. See `DOT-NATIVE-OPERATION-GATES.md`.
