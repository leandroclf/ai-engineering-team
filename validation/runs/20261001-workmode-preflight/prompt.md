# Harden Dot-native operations

## Problem
The attached research recommends executable authorization and evidence controls before D8. Existing `harden-engineering-dot` implements policy documents and structural checks, but the CLI transport trusts a textual verdict without validating the result SHA or runtime failure state. A missing executor raises before writing a run manifest, a failed pre-command does not stop execution, CI polling has no deadline, and bare `wait` does not propagate all reviewer failures.

## Scope
Harden the existing validation harness and audit current evidence. Preserve the Dot-native architecture; do not introduce another agent runtime. Add a machine-readable reviewer transport gate and regression coverage. Keep authorization leases, full delegation/evidence schemas and live Dot acceptance as explicit remaining work.

## Success
Known launch/check/transport failures cannot produce success; timeout and missing executors leave observable evidence; failed pre-commands never launch a provider; reviewers are bound to the PR head. Passing deterministic tests does not mark D8 or live Dot scenarios DONE.
