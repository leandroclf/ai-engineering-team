# Dot-native operation gates

Status: repository-side implementation; live integration pending.

The [Linux CLI](LOCAL-LINUX-WORKFLOW.md) now adds bounded task coordination and real offline test isolation. It does not connect `authorize()` to each internal provider tool call, so the trusted native adapter gap below remains open. Full current repository/CI commands are in [VALIDATION](VALIDATION.md).

This adds deterministic contract checks to the existing native Dot architecture. It is not a scheduler, authorization server or substitute for native/provider approvals. The canonical flow remains Atlas -> Codex -> GitHub/CI -> Sentinel -> Argus.

## Trust boundaries

The operator/native policy owns authorization. Git/GitHub and the controlled runner supply freshly observed state and execution evidence. Executor output, issue text, logs, webpages and remembered context are untrusted data: none may issue, revise or renew a lease. A task envelope is a request, not a permission grant.

`scripts/dot_contracts.py` accepts trusted state supplied by its caller. JSON/schema validation does not authenticate the issuer. Do not load the current authorization state from a Codex-writable checkout or accept executor-authored state as current permission. These functions must be invoked by a trusted adapter immediately before each bounded operation. Check and operation are not atomic; remote permission checks, branch protections and native approvals remain necessary to close that race. There is no live adapter in this change.

## Versioned contracts

- `schemas/dot-codex-task.schema.json`: concrete bounded task, exact repository/branch/base SHA, risk, required commands and budgets.
- `schemas/authorization-lease.schema.json`: task/project/scope/revision, time interval, action allow/deny lists and repository-relative path prefixes.
- `schemas/authorization-state.schema.json`: trusted current lease revision/revocation, observed repository, consumed budget and circuit state.
- `schemas/execution-evidence.schema.json`: outcome, immutable revisions, artifact hashes, command exits, CI revision, failures and external-write count.

All schemas reject unknown fields. These are v1 executable contracts alongside the existing editable YAML templates; historical manifests and evidence remain unchanged. Empty placeholder templates are not executable envelopes. The examples under `validation/examples/` are synthetic and expired, suitable for schema validation only.

## Authorization checks

Use `authorize(task, state, action, paths, now=..., external=...)` before a bounded operation. `PASS` here means **the repository policy check allows the proposed operation**, not task completion or provider permission. Invalid schemas raise an exception; callers must stop on that exception or any other result.

Revalidate task/project identity, exact repository/branch/base revision, current scope revision, revocation and lease validity on every call. Denials override allows. Paths are literal relative directory/file prefixes, not globs; traversal, absolute paths and sibling-prefix matches are rejected. Filesystem realpath/symlink containment must additionally be enforced by a mutation adapter. R0 cannot mutate. R3 returns `BLOCKED_APPROVAL` unconditionally and must be handed to the separate native/operator approval flow. Repository R2 keeps the existing dependency/schema/security definition in `AGENTS.md`; the attached research's alternative taxonomy is not silently adopted.

Budgets count total attempts (including the first), elapsed seconds and external writes. The trusted caller increments/reserves usage and persists circuit state. The checker does not implement counters, retries, locks, a circuit service or exactly-once delivery. Do not retry an ambiguous external write; reconcile its idempotency identifier first. The live adapter must enforce concurrency and budget reservation atomically.

## Evidence checks

`verify_evidence(task, evidence, artifact_root, observed_final_sha)` checks identity/base/final revisions, path scope, write budget, artifact containment and SHA-256. A PASS claim additionally requires every exact required command to have exit 0, no failures/duplicate commands, and successful CI on the independently observed final SHA. An R0 PASS cannot contain mutations. Non-PASS evidence can preserve failed checks honestly.

An artifact hash proves byte consistency, not authenticity or execution. The trusted evaluator must obtain exit/CI records from the runner/GitHub, independently verify changed files, and account for authorization at the time of each side effect. This validator does not upgrade a self-reported result to independent assurance. Historical manifests are audited, not retroactively certified under this schema. A repository JSONL file is not an immutable audit store.

## Preflight and execution

`python scripts/preflight.py` performs read-only CLI availability/version/auth probes with bounded timeouts. It never prints authentication output. Missing CLI returns UNAVAILABLE and exit 2. Successful login still returns INCONCLUSIVE: it does not prove shell execution, model availability, cloud environment routing or Dot->Codex delegation.

Repository checks:

```bash
python -m pip install -r requirements-validation.txt
python scripts/validate.py
python scripts/validate_hardening.py
python scripts/validate_native_operations.py
python -m unittest discover -s tests/unit -v
python docs/anexos/build/verificar_docs.py
```

The workflow runs these checks. They prove deterministic repository behavior, not live Dot behavior. See `validation/PROJECT-EVOLUTION-2026-10-01.md` and the OpenSpec change for runtime gates and remaining risks.
