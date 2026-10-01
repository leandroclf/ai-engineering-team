# Tasks

## Mandatory execution rule
Every unchecked executable item below MUST be carried out through the applicable provider's official CLI using the operator's already-configured subscription account. OpenAI work uses the official OpenAI/Codex CLI; Anthropic work uses Claude Code CLI. Do not replace these steps with API-key/API execution unless a future explicit architectural exception is approved and documented.

## C0 Architecture
- [x] Define Claude as vendor-diverse assurance, not coordinator.
- [x] Define GitHub/OpenSpec/evidence transport.
- [x] Define authority and mutation boundaries.
- [x] Define provider CLI as the mandatory execution plane for next steps.
- [x] Define subscription-account authentication as the default; no API-key billing dependency.

## C1 Contracts
- [x] Add Claude assurance request.
- [x] Add Claude assurance result.
- [x] Add setup/review runbook.
- [x] Add behavioral scenarios.

## C2 Safety
- [x] Preserve R3 operator/native approvals.
- [x] Default Claude reviewer to read-only.
- [x] Invalidate verdict after revision change.
- [x] Prohibit majority-vote resolution for critical disagreement.
- [x] Preserve provider CLI/native permission boundaries.

## C3 Validation — execute via provider CLIs
- [x] Using Claude Code CLI with the configured Claude subscription, execute Claude assurance against a controlled fixture. (`validation/runs/20261001-ca02-r1`)
- [x] Using Claude Code CLI, execute CA01-CA08 and preserve evidence. (18 runs, all PASS; CA04/CA05/CA07 3/3+)
- [x] Using the official OpenAI/Codex CLI with the configured OpenAI subscription, execute the corresponding Atlas/Codex validation steps and preserve evidence (`validation/FINAL-REPORT.md`, atlas-cli container). Earlier note: BLOCKED 2026-10-01: Codex CLI authenticated but its bwrap sandbox cannot start on this host (AppArmor restricts unprivileged user namespaces); evidence `validation/runs/20261001-s01-r1`; see `validation/ARGUS-ASSURANCE-REPORT.md`.
- [x] Confirm actual CLI account authentication and permission behavior for both providers without storing credentials in the repository. Containers: Codex ChatGPT login in atlas-cli/sentinel-cli (same user, W-001), Claude claude.ai login in argus-cli; Codex sandbox unavailable, container/`:ro` boundary used. Earlier: Claude CLI subscription auth (`apiKeySource: none`) and read-only tool allow-list confirmed; Codex CLI login confirmed (`Logged in using ChatGPT`) but sandbox permission behavior BLOCKED.
- [x] Measure latency, useful findings and false positives from CLI executions. (Argus side; OpenAI side BLOCKED)
- [ ] Validate Atlas -> GitHub/OpenSpec -> Sentinel -> Claude CLI handoff end-to-end. PARTIAL: CLI-layer chain AS01->AS03->Argus PASS 3/3 over local git (`validation/FINAL-REPORT.md`); GitHub PR/CI transport, live Sentinel Dot and distinct accounts (W-001) pending.
- [x] Produce the final Claude assurance report from observable CLI evidence. (`validation/ARGUS-ASSURANCE-REPORT.md`; cross-provider chain remains PARTIALLY_VALIDATED)

## C4 Future providers
- [ ] Onboard any future provider only through its official CLI and configured subscription account where supported.
- [ ] Add provider-specific permission, evidence and failure contracts before execution.
- [ ] Require explicit architectural approval for any API-key/API fallback.

## Completion
Static implementation may be COMPLETE after CI. Operational status remains PARTIALLY_VALIDATED until C3 has observable CLI execution evidence. A step unavailable through the required CLI remains BLOCKED/INCONCLUSIVE rather than being silently rerouted through an API.

## Execution environment binding
See `docs/EXECUTION-ENVIRONMENTS.md`. Claude runtime tasks are **CLAUDE-CLI** using the configured Claude subscription account. OpenAI-side execution is **OPENAI-CLI-A**. End-to-end handoff is **CROSS-ENV**. **CHAT-GITHUB** may prepare fixtures/contracts and compile observable evidence, but cannot substitute for provider CLI execution.
