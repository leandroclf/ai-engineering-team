# Execution Plan

Status: SUPERSEDED IN PART by `../adopt-dot-native-architecture/`.

The original Codex-only scenarios remain useful for validating the repository execution layer, but final acceptance MUST also validate the Engineering Dot coordination layer.

## Existing Codex-layer validation
- [x] Baseline structural validation.
- [x] Fixtures for simple, backend, precedence, failing-validation, R3 and reconciliation scenarios.
- [x] Evidence harness (`scripts/provider_run.py`).
- [ ] Execute S01-S06 and preserve failures. BLOCKED 2026-10-01: Codex CLI authenticated but its bwrap sandbox cannot start on this host (AppArmor restricts unprivileged user namespaces); evidence `validation/runs/20261001-s01-r1`; see `validation/ARGUS-ASSURANCE-REPORT.md`.
- [ ] Benchmark proportional orchestration.
- [ ] Remediate and rerun defects.

## Required Dot-native extension
- [ ] Complete `adopt-dot-native-architecture` D0-D4 before final behavioral acceptance.
- [ ] Validate Dot routes non-trivial repository work to Codex with a bounded task envelope.
- [ ] Validate trivial conversational work is not unnecessarily delegated.
- [ ] Validate target repository state is re-read when remembered context is stale.
- [ ] Validate plugin permission denial is surfaced rather than bypassed.
- [ ] Validate native approval + R3 composition.
- [ ] Validate Codex failure returns evidence to Dot for bounded remediation/escalation.
- [ ] Produce Dot-native final report in addition to Codex-layer evidence.

## Acceptance
No false PASS, no unauthorized R3 side effect, no permission bypass, and all claims traceable to observable evidence.

## Execution environment binding
See `docs/EXECUTION-ENVIRONMENTS.md`. Repository fixtures/harness/structural preparation are **CHAT-GITHUB** work. S01-S06 and Codex behavior are **OPENAI-CLI-A**. Dot routing/approval behavior is **OPENAI-DOT-A** plus the applicable CLI; cross-account assurance is handled by the Atlas/Sentinel plan. Missing runtime evidence remains INCONCLUSIVE.
