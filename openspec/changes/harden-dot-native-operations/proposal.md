# Harden Dot-native operations

Status: IMPLEMENTED_REPOSITORY_LAYER; runtime integration pending.

The existing architecture has real CLI/PR/CI evidence, but most hardening checks validate document tokens and YAML field presence. Add strict executable task/authorization/evidence contracts and failure tests without creating another agent runtime. Preserve native/provider safeguards and historical evidence.

Success: schemas and deterministic adversarial tests pass; missing CLI is never PASS; current status reports reconcile earlier execution blockers. Completion of this change still requires trusted adapter integration, repeated provider/Dot scenarios, revocation during a real task, and independent review.

Risk: R2 (authorization/schema/security-sensitive). External delivery is branch/PR only; no merge, production action, account/permission change or R3 approval is part of this change.
