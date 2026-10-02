# Harden Dot-native operations

Status: IMPLEMENTED_REPOSITORY_LAYER; runtime integration pending.

## Problem
The architecture has real CLI/PR/CI evidence, but earlier checks mostly validated document tokens and YAML field presence. The transport also trusted textual verdicts without reconciling SHA or runtime failure, and did not consistently preserve failed-launch evidence or bound CI waits.

## Scope
Add strict task, authorization, state and evidence contracts, deterministic adversarial checks, a read-only provider preflight, and a structured reviewer transport gate. Reconcile the work from PR #10 and PR #11 without changing the Dot-native architecture or replacing historical evidence. Provider-specific hardening and follow-up acceptance are tracked in `align-provider-official-guidance`.

## Success
Missing executors and launch/check/transport failures cannot produce success. Timeouts preserve observable evidence, failed setup never launches a provider, and reviews are bound to the exact PR head. Schemas and deterministic tests pass. Completing the repository layer does not mark D8 or live Dot scenarios DONE.

## Remaining acceptance
Trusted before-action adapters, atomic budget reservations, repeated authenticated provider/Dot scenarios, revocation during a real task, and independent review remain required. Schema validation alone does not enforce authorization over a native runtime.

Risk: R2 (authorization/schema/security-sensitive). External delivery is branch/PR only; merge, production actions and account/permission changes are outside this change.
