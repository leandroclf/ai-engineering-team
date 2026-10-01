# Tasks

## H0 Architecture
- [x] Define native/governance/execution/repository control planes.
- [x] Define routing boundaries.
- [x] Define freshness and isolation model.

## H1 Reliability
- [x] Add reliability policy: idempotency, retries, budgets, circuit breakers and stop conditions.
- [x] Add concurrency lease contract.
- [x] Add context freshness contract.

## H2 Security
- [x] Add untrusted-content/prompt-injection policy.
- [x] Strengthen least-privilege and approval composition.
- [x] Add data-boundary rules.

## H3 Delivery
- [x] Add branch/PR/CI/release policy.
- [x] Add incident/rollback/recovery playbook.
- [x] Add policy/schema versioning and migration contract.

## H4 Portfolio
- [x] Add routing matrix.
- [x] Add context/cost budget policy.
- [x] Add portfolio governance model.
- [x] Add Dot calibration and feedback loop.

## H5 Contracts
- [x] Add task envelope.
- [x] Add lease template.
- [x] Add evidence record schema.
- [x] Add incident record.
- [x] Add policy manifest.

## H6 Validation
- [x] Extend structural validator.
- [x] Add hardening validation scenarios and acceptance criteria.
- [ ] Execute live Dot/Codex behavioral scenarios and preserve evidence.
- [ ] Confirm native approval behavior in the user's actual Dot environment.
- [ ] Run portfolio concurrency scenario with two real/sandbox repository tasks.

## Completion rule
Implementation is structurally complete when H0-H5 and static H6 pass. The change becomes VALIDATED/DONE only after the three live H6 items have real evidence; unavailable runtime capabilities must remain INCONCLUSIVE, never PASS.

## Execution environment binding
See `docs/EXECUTION-ENVIRONMENTS.md`. H6 live Dot/Codex scenarios require **OPENAI-DOT-A + OPENAI-CLI-A**. Native approval additionally requires **HUMAN**. Portfolio concurrency requires the live Dot plus two controlled CLI/repository tasks. **CHAT-GITHUB** prepares fixtures and audits evidence only.
