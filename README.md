# ai-engineering-team

A portable, evidence-driven agentic software-engineering operating model for Codex.

## What it provides
A Tech Lead orchestration contract, reusable specialist skills, stack packs, engineering workflows, controlled-autonomy rules, quality gates, templates and an OpenSpec roadmap.

## Quick start
1. Adapt `templates/PROJECT-AGENTS.md` into the target repository as `AGENTS.md`.
2. Use the Tech Lead skill for complex work.
3. State the engineering objective rather than repeating a large procedural prompt.
4. The workflow discovers context, classifies risk, selects relevant skills, executes, validates, reviews and reports evidence.

Example: `Use the Tech Lead workflow. Implement <objective>, preserve existing contracts, run repository-native validation and report evidence.`

## Architecture
Operator -> AGENTS.md -> Tech Lead -> selected specialist/stack skills -> quality gates -> evidence-backed report.

## Skills
Core: tech-lead, architect, backend, qa, security, code-review, observability.
Stack packs: java-spring, node-typescript, python-fastapi, aws, kubernetes.
Workflow: github-workflow.

## OpenSpec
See `openspec/project.md`, `openspec/changes/bootstrap-agentic-engineering-team/`, and `openspec/roadmap.md`.

## Safety model
R0 read-only; R1 reversible local code; R2 dependency/schema/infrastructure/security-sensitive; R3 production/destructive/irreversible. R3 requires explicit authorization.

## Current scope
The repository is runtime-light: Markdown contracts and skills can be consumed by Codex without requiring an additional agent runtime. Persistence and explicit multi-agent execution are specified as evolutions rather than simulated.
