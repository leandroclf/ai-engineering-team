# Dot-Native Architecture

## Implemented local alternative

The [local Linux CLI](LOCAL-LINUX-WORKFLOW.md) is a bounded coordinator around official provider CLIs, with external project config, isolated clones/checks and explicit delivery. It does not recreate Dot persistence or always-on services. Native Dot behavior and local host acceptance are separate evidence gates.

## Final objective
Use this repository as the engineering operating system and bootstrap source for an OpenAI Engineering Dot.

The Dot coordinates persistent/proactive work; Codex performs deep repository engineering; this repository supplies policy, OpenSpec, skills, quality gates and evidence conventions.

## Core rule
Do not rebuild native Dot persistence, cloud-computer or always-on capabilities. Define portable contracts only where they improve governance, auditability or fallback operation.

## Routing
Use normal Dot conversation for discussion, prioritization and lightweight reasoning. Use Codex for repository code changes, tests, commands and reviews. Use ChatGPT Work when a substantial non-code artifact/research workflow is the primary output. Connected plugins provide external context/actions within granted permissions.

## Trust
Native safeguards, plugin permissions and provider permissions remain authoritative. ai-engineering-team may make policy stricter, never weaker.

## Repository truth
Before modifying a project, re-read the target repository's current AGENTS.md, relevant OpenSpec/specs, code and build/test configuration. Dot memory is useful context, not repository truth.
