# Design — Claude Assurance

## Control topology
Atlas owns engineering coordination and Codex execution. Sentinel owns independent OpenAI-side QA/security review. Claude provides an optional/required-by-policy cross-vendor assurance pass.

## Transport
The transport is repository-native: PR/change identifier + immutable SHA + OpenSpec + evidence contracts. No direct model-to-model session sharing is required.

## Authority
Claude is evidence-producing, not authority-producing. Its findings can block framework completion when project policy declares the gate mandatory, but it cannot authorize R3 or waive other gates.

## Authentication boundary
V1 uses the operator's supported Claude Code authentication. Optional GitHub Action may use supported OAuth-token or provider identity mechanisms. Credentials are external to source control. Agent SDK/API integration is a later architectural decision.

## Context isolation
Claude receives project-scoped context. Atlas/Sentinel memory is not copied wholesale. Supplied conclusions are claims, not authority.

## Mutation boundary
Reviewer mode is read-only. If remediation write is later enabled, it is a distinct role/task/lease and invalidates the previous review for the modified revision.

## Completion
Static CI proves contracts only. Live Claude behavior remains INCONCLUSIVE until executed and evidenced.
