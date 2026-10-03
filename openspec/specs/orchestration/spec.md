# Capability: Orchestration

## Requirements

### ORCH-001 Context discovery
Before non-trivial modification, the system MUST inspect repository instructions, relevant source, tests, build tooling and local conventions.

### ORCH-002 Planning
The Tech Lead MUST produce an internal actionable plan for non-trivial tasks and identify dependencies and risk class.

### ORCH-003 Selective delegation

The local Linux capability defines mandatory isolated planning (Atlas/OpenAI), implementation (Argus/Claude), validation (Sentinel/OpenAI) and review (Atlas/Claude) stages. These fixed acceptance gates do not mean invoking all specialist skills; specialist selection remains proportional to the task. The current contract is [isolated stages](../../../docs/ISOLATED-AGENT-STAGES.md); the [initial local contract](../../changes/local-linux-workflow/specs/local-operation/spec.md) describes version 0.1.

The orchestrator MUST select only capabilities that materially improve the task. It MUST NOT invoke all specialist roles by default.

### ORCH-004 Verification
Completion MUST be based on executed validation where execution is available. The system MUST NOT report an unexecuted test as passing.

### ORCH-005 Residual risk
The final report MUST identify unresolved failures, assumptions and material risks.

### ORCH-006 Stop conditions
The system MUST stop/escalate when required credentials, authorization, destructive approval, critical context or reliable validation is unavailable.
