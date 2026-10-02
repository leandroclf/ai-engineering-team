# Validation Strategy
The repository uses lightweight executable validators because the framework is primarily declarative Markdown.

`python scripts/validate.py` checks mandatory artifacts, Skill frontmatter, core AGENTS contract markers, the provider-execution fixtures, and that every `validation/runs/*/manifest.yaml` carries exactly one allowed status (PASS, FAIL, BLOCKED or INCONCLUSIVE).

`python scripts/validate_hardening.py` checks the hardening contracts: required policy tokens, YAML validity of the task envelope, lease, evidence record, policy manifest and project registry, required envelope and lease fields, native-safeguard precedence in the policy manifest, and the H01-H10 scenario list.

GitHub Actions runs both validators on pushes and pull requests (`.github/workflows/validate.yml`, Python 3.12 with dependencies from `requirements-validation.txt`).

## What structural validation proves
Artifacts exist, parse and satisfy the checked constraints. It does not prove agent behavior, live Dot behavior, native approvals or independence between accounts. A green CI run must never be reported as behavioral validation.

## Behavioral validation
Scenario-level validation is defined in `tests/scenarios.md` and the scenario files under `validation/`. Runs execute through the provider CLIs with `scripts/provider_run.py` in disposable clones, normally inside the per-account containers described in `runbooks/CONTAINER-RUNTIMES.md`. Evidence is preserved under `validation/runs/<run-id>/`. `scripts/pr_chain.sh` exercises the Atlas -> Sentinel -> Argus chain over GitHub pull requests and CI. Results are summarized in `validation/FINAL-REPORT.md` and the per-agent reports.

Behavioral benchmarking requires a live provider runtime and is reported separately from static validation; it must never be marked passing without execution evidence.

## Executable operation contracts

`python scripts/validate_native_operations.py` validates five JSON schemas and concrete examples. `python -m unittest discover -s tests/unit -v` exercises authorization/evidence/preflight failure boundaries. `python docs/anexos/build/verificar_docs.py` checks the consolidated documentation links and identifiers. Dependencies are pinned in `requirements-validation.txt`; CI installs this file and runs these checks in addition to the original validators.

These tests validate repository functions only. Live adapter enforcement, native approvals and Dot behavior still require runtime evidence. See `DOT-NATIVE-OPERATION-GATES.md`.

## Harness failure and transport gates

`python -m unittest discover -s tests -p 'test_*.py' -v` tests launch failures, timeout, setup/check failures, background exits, bounded CI and exact-head review results. CI runs these tests and `bash -n scripts/pr_chain.sh`.

`provider_run.py --timeout-seconds` defaults to 1800 per setup/provider/check command. Missing executable is BLOCKED (exit 127); provider timeout is INCONCLUSIVE (124); ordinary failures and failed required checks are FAIL. Successful execution stays INCONCLUSIVE pending evaluator review. The harness exits nonzero for unsuccessful provider/check execution and never launches a provider after failed setup.

`pr_chain.sh` bounds CI polling with `CI_TIMEOUT_SECONDS` (default 600), requires successful CI and awaits each reviewer PID. `review_status.py` verifies the declared result SHA against manifest, expected head and successful exact-head check. The current chain requires JSON; the historical audit mode accepts one plain or fenced YAML result. Missing/malformed/stale evidence is error, not success. The strict gate validates the declared reviewer role and blocking finding fields, but cannot authenticate the account or establish that the review is correct. Earlier runs need the qualification in `validation/PROJECT-EVOLUTION-REVIEW.md`.

CI failure/timeout after opening a PR can leave a draft PR for inspection and manual cleanup. A CLI timeout alone does not prove that a remote task was cancelled.

## Provider guidance integration

See `PROVIDER-GUIDANCE-REVIEW.md` and `openspec/changes/align-provider-official-guidance/`. New PR-chain reviewers receive `--structured-review` and must return `review.json`; historical YAML is supported only outside the strict chain. A JSON schema is not proof of correct review or account identity. Required quality/security gates and HIGH/CRITICAL findings are checked in addition to transport evidence.

Run preflights with `python scripts/preflight.py --provider codex` and `--provider claude`. These do not run a model or install/update CLIs. Capability detection does not establish protocol compatibility; run the controlled chain before promotion.
