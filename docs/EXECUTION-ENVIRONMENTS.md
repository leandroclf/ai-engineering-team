# Execution Environment Matrix

Status: ACTIVE

## Purpose
Bind every remaining executable task to the environment that is actually authorized to execute it. A task MUST NOT be silently moved to another environment merely because that environment is convenient.

## Named agent roster
The names identify responsibilities. In the native Dot architecture:

- **Atlas** — primary OpenAI Engineering Lead Dot, running in the operator's primary OpenAI account.
- **Sentinel** — secondary OpenAI Quality & Security Dot, running in the operator's second OpenAI account.
- **Argus** — Anthropic Claude assurance bot, executed through Claude Code CLI with the operator's configured Claude subscription. Argus is the cross-vendor independent reviewer and does not replace Atlas or Sentinel.

Canonical flow: **Atlas -> Codex -> GitHub/OpenSpec/CI -> Sentinel -> Argus (Claude) -> Atlas/operator**.

The implemented local CLI uses Atlas/Sentinel as Codex CLI roles and Argus as a Claude Code role; it does not create live Dots. Local flow: independent clone -> Atlas -> host commit -> offline tests -> Sentinel/Argus -> bounded repair -> explicit branch/PR delivery. Both reviews precede delivery, with GitHub CI afterwards.

Names MUST be used consistently in OpenSpec, runbooks, evidence and final reports. Generic terms such as "Claude bot", "primary Dot" or "secondary Dot" may explain the provider/runtime, but do not replace the canonical agent name.

## Environment labels
- **CHAT-GITHUB** — this ChatGPT environment using the connected GitHub app. Allowed: inspect repository state, edit governance/docs/contracts/scripts, create branches/commits/PRs, inspect CI evidence and merge when repository policy permits.
- **OPENAI-CLI-A / Atlas execution plane** — official OpenAI/Codex CLI authenticated with the operator's configured primary OpenAI subscription account. Required for Atlas/Codex repository-execution behavioral work.
- **OPENAI-CLI-B / Sentinel execution plane** — official OpenAI/Codex CLI authenticated with the operator's secondary OpenAI account. Used for Sentinel's independent repository checks; it does not replace the live Sentinel Dot.
- **LOCAL-LINUX** — operator Linux host running `ai-team`; Docker isolates provider roles and offline checks. Installation and login follow [LOCAL-LINUX-WORKFLOW](LOCAL-LINUX-WORKFLOW.md). Live host acceptance requires LOCAL-LINUX + the three CLI environments + HUMAN.
- Provider CLIs use separate account containers. `ai-team` uses `ai-team-<role>-home`; the historical Compose harness uses project-prefixed `atlas-home`, `sentinel-home`, `argus-home` volumes. See [CONTAINER-RUNTIMES](../runbooks/CONTAINER-RUNTIMES.md). These logins are not automatically shared.
- **OPENAI-DOT-A / Atlas** — live Atlas Dot in the primary OpenAI account. Required for native Dot coordination, memory/context, native approval and Dot->Codex behavior.
- **OPENAI-DOT-B / Sentinel** — live Sentinel Dot in the secondary OpenAI account. Required for independent cross-account review and real Sentinel permission behavior.
- **CLAUDE-CLI / Argus** — official Claude Code CLI authenticated with the operator's configured Claude subscription account. Required for Anthropic assurance execution.
- **CROSS-ENV** — scenario requires evidence from two or more of the environments above.
- **HUMAN** — explicit operator action/approval that cannot be delegated, especially account sign-in, permission grant, risk acceptance or native R3 approval.

## Hard rule
Provider execution is CLI/account-bound. CHAT-GITHUB may prepare, inspect, validate repository artifacts and coordinate GitHub, but MUST NOT mark a provider-runtime task PASS unless evidence from the required provider environment exists.

If an environment is unavailable, record BLOCKED/INCONCLUSIVE. Do not substitute API-key/API execution for OPENAI-CLI-A or CLAUDE-CLI without an explicit approved architecture exception.

## Remaining-task mapping

| Task | Required environment | CHAT-GITHUB contribution | Completion evidence |
|---|---|---|---|
| Bootstrap Phase 8 live Codex benchmark | OPENAI-CLI-A | Prepare fixtures/contracts; inspect commits/CI | CLI run evidence + immutable SHA |
| Behavioral instruction precedence | OPENAI-CLI-A | Prepare fixture; verify repository result | CLI transcript/result artifact |
| Behavioral failure transparency | OPENAI-CLI-A | Prepare controlled failure; inspect evidence | Failure preserved, no false PASS |
| Behavioral R3 approval gate | OPENAI-CLI-A + HUMAN | Prepare non-destructive fixture | CLI stops for explicit approval |
| S01-S06 Codex-layer validation | OPENAI-CLI-A | Prepare harness and inspect outputs | Per-scenario evidence |
| Live Dot-native scenarios | OPENAI-DOT-A + OPENAI-CLI-A | Prepare scenarios/contracts; inspect GitHub effects | Dot activity + CLI/repo evidence |
| Live Atlas bootstrap | OPENAI-DOT-A + HUMAN | Keep bootstrap/runbook current | Atlas configured + observed run |
| H01-H10 live Dot/Codex hardening | CROSS-ENV | Prepare fixtures/evidence ledger | Scenario records |
| Native approval behavior | OPENAI-DOT-A + HUMAN | Prepare safe R3 fixture | Observed native approval/denial |
| Portfolio concurrency | OPENAI-DOT-A + OPENAI-CLI-A | Prepare two sandbox tasks; inspect leases/PRs | Two-task concurrency evidence |
| Instantiate Atlas | OPENAI-DOT-A + HUMAN | Supply bootstrap/runbook | Live Dot identity/config evidence |
| Instantiate Sentinel | OPENAI-DOT-B + HUMAN | Supply bootstrap/runbook | Live Dot identity/config evidence |
| Atlas/Sentinel AS01-AS10 | OPENAI-DOT-A + OPENAI-DOT-B + OPENAI-CLI-A | Prepare immutable review artifacts; inspect PR/CI | Cross-account evidence |
| Confirm Atlas/Sentinel permissions | OPENAI-DOT-A + OPENAI-DOT-B + HUMAN | Verify repo-side permissions where visible | Native/provider permission evidence |
| Argus (Claude) controlled fixture | CLAUDE-CLI / Argus | Prepare request/fixture; inspect resulting GitHub evidence | Claude CLI evidence |
| Argus (Claude) CA01-CA08 | CLAUDE-CLI / Argus | Prepare scenarios; validate SHA/evidence artifacts | Per-scenario Claude result |
| OpenAI side of Claude handoff | OPENAI-CLI-A | Prepare contracts and GitHub transport | OpenAI CLI evidence |
| Confirm CLI authentication/permissions | OPENAI-CLI-A + CLAUDE-CLI + HUMAN | Never handle secrets; record non-secret metadata only | Authenticated CLI behavior |
| End-to-end Atlas->Sentinel->Argus | CROSS-ENV | GitHub/OpenSpec transport and evidence inspection | Revision-bound handoff chain |
| Final reports | CHAT-GITHUB after runtime evidence exists | Compile evidence, update OpenSpec/status, PR/merge | Reports traceable to observed evidence |
| Future provider onboarding | provider official CLI + HUMAN | Add contracts/runbook after approval | Provider-specific evidence |
| API fallback exception | HUMAN + architecture change | Document/implement only after explicit approval | Approved ADR/OpenSpec |

## What this environment can execute now
CHAT-GITHUB can complete repository-side preparation, consistency audits, structural validators, fixture creation, OpenSpec/task mapping, evidence templates, branch/PR/CI inspection, remediation of repository-only defects, and final report generation once external runtime evidence exists.

CHAT-GITHUB cannot authenticate as the operator inside local provider CLIs, instantiate a Dot in another account, manufacture live Dot behavior, or convert missing provider evidence into PASS.

## Closure discipline
Every final report must state which environment produced each piece of evidence. CI exercises repository contracts, bootstrap and real credential-free Docker canaries, including CLI version/help probes. It does not prove authenticated model behavior, account independence, live Dots or operator-host acceptance.
