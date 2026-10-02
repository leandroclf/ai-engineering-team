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

## Harness failure and transport gates

`python -m unittest discover -s tests -p 'test_*.py' -v` tests launch failures, timeout, setup/check failures, background exits, bounded CI and exact-head review results. CI runs these tests and `bash -n scripts/pr_chain.sh`.

`provider_run.py --timeout-seconds` defaults to 1800 per setup/provider/check command. Missing executable is BLOCKED (exit 127); provider timeout is INCONCLUSIVE (124); ordinary failures and failed required checks are FAIL. Successful execution stays INCONCLUSIVE pending evaluator review. The harness exits nonzero for unsuccessful provider/check execution and never launches a provider after failed setup.

`pr_chain.sh` bounds CI polling with `CI_TIMEOUT_SECONDS` (default 600), requires successful CI and awaits each reviewer PID. `review_status.py` accepts one plain or fenced YAML result and verifies the declared result SHA against manifest, expected head and successful exact-head check. Missing/malformed/stale evidence is error, not success. This transport gate does not validate full finding semantics or reviewer identity. Earlier runs need the qualification in `validation/PROJECT-EVOLUTION-REVIEW.md`.

CI failure/timeout after opening a PR can leave a draft PR for inspection and manual cleanup. A CLI timeout alone does not prove that a remote task was cancelled.
