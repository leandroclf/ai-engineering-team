# Design

## Logical architecture

```
Operator
   |
   v
Repository AGENTS.md
   |
   v
Tech Lead Orchestrator
   |
   +--> Context Discovery
   +--> Planning / Risk Classification
   |
   +--> Architect
   +--> Backend
   +--> QA
   +--> Security
   +--> Observability
   +--> Code Review
   |
   v
Quality Gates + Evidence
   |
   v
Delivery Report
```

## Layers

### L0 — Governance
Root AGENTS.md defines precedence, autonomy boundaries, Definition of Done and mandatory evidence.

### L1 — Orchestration
Tech Lead classifies task complexity/risk, discovers context, creates a plan and selects only relevant capabilities.

### L2 — Specialist skills
Skills contain focused procedures. They are composable and must not duplicate global policy.

### L3 — Project adapters
A target repository adds local architecture, commands, constraints, ownership and deployment rules.

### L4 — Tool adapters
GitHub, shell, CI, documentation, MCP and future external systems. Least privilege applies.

### L5 — Evidence
Tests, lint/static analysis, build results, diff review, security checks and unresolved-risk reporting.

## Task lifecycle
INTAKE -> DISCOVER -> PLAN -> EXECUTE -> VERIFY -> REVIEW -> REPORT.

High-risk or irreversible work adds an APPROVAL gate before execution/delivery.

## Risk classes
- R0: read-only analysis/documentation.
- R1: local/reversible code changes.
- R2: dependency, schema, infrastructure or security-sensitive changes.
- R3: production, destructive, credential/permission or irreversible actions.

R3 always requires explicit authorization. Project adapters may require approval for R2.

## Context precedence
Safety/platform constraints > explicit operator request > nearest repository AGENTS.md > parent AGENTS.md > generic skills > defaults.

## Efficiency rules
- Do not invoke every specialist for every task.
- Parallelize only independent work.
- Prefer repository-native commands.
- Avoid rereading unchanged context.
- Escalate uncertainty rather than fabricate.
- Keep final reports concise but evidence-backed.

## Evolution
V1: Codex + AGENTS.md + skills/workflows.
V2: MCP/tool adapters and automated project bootstrap.
V3: explicit multi-agent orchestration where supported.
V4: persistent sessions, event-driven work and controlled autonomous loops.
