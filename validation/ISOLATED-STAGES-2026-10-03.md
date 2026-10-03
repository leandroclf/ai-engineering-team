# Isolated stage evolution — repository evidence

Base: main `92633e8c3bf658a58a7e79503452261427538777`. Change: `isolated-agent-stages`, local CLI 0.2.0. Existing merged marketplace/evaluation work was preserved before starting this branch.

## Implemented

Atlas/OpenAI planning, Argus/Claude implementation, Sentinel/OpenAI validation, Atlas/Claude isolated review. Explicit models/efforts, four auth contexts, fresh sessions, host-owned canonical plan/OpenSpec handoff, offline checks, exact plan/HEAD acceptance coverage, bounded repair/replanning, legacy config upgrade with backup and delivery-time evidence revalidation. No new service, gateway, model selector or dependency.

## Local verification

- 83 unit tests and 23 harness tests pass (106 total); includes full workflow and failure/recovery cases with controlled providers, not real inference.
- Framework, hardening, native-operation schemas (8), skill catalog and evaluation validators pass.
- Markdown links/fences and consolidated docs verification pass.
- Python compilation, shell syntax, CLI help and diff whitespace checks pass.

## Runtime verification

Docker/provider CLIs are unavailable in this workspace. CI is configured to build pinned runtime, probe CLI capabilities without auth, run installer/offline check canaries and exercise read/write mounts for all four stages without account volumes or inference. CI outcome must be recorded after execution.

## Limits and remaining operator acceptance

No authenticated run is claimed. Model access, actual requested-model execution, native Codex sandbox compatibility, real Claude file tool permissions and a complete task on the operator's Linux remain unverified here. `resolved_model` is deliberately unknown. Login volumes do not establish account independence. Historical Dot/CLI results were not relabeled as evidence for this new flow. Merge and deployment are separate actions.
