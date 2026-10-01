# CLI Execution Queue

Status: READY_FOR_PROVIDER_RUNTIMES

## Atlas / OPENAI-CLI-A
- S01 simple task efficiency — fixture ready.
- S03 instruction precedence — fixture ready.
- S04 failure transparency — fixture ready.
- S05 R3 guard — harmless sentinel ready.
- S02 complex backend and S06 reconciliation — specification exists; deterministic code fixture still to be executed/prepared before provider run.
- H01-H10 — scenario definitions ready; selected reusable safety fixtures included.

## Sentinel / OPENAI-DOT-B
- AS01-AS10 definitions ready.
- AS02 known HIGH authorization fixture ready.
- Cross-account execution remains runtime-bound.

## Argus / CLAUDE-CLI
- CA01-CA08 definitions ready.
- CA02 known authorization defect fixture ready.
- CA07 may reuse h02-prompt-injection/untrusted.txt.
- Claude CLI execution remains runtime-bound.

## Evidence
Every provider run must copy validation/RUN-MANIFEST-TEMPLATE.yaml into validation/runs/<run-id>/manifest.yaml and attach only observable evidence. Never store secrets or hidden chain-of-thought.
