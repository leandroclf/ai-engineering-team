# Capability: Orchestration

## Requirements

### ORCH-001 Context discovery
Before non-trivial modification, the system MUST inspect repository instructions, relevant source, tests, build tooling and local conventions.

### ORCH-002 Planning
The Tech Lead MUST produce an internal actionable plan for non-trivial tasks and identify dependencies and risk class.

### ORCH-003 Selective delegation

The local Linux capability defines two mandatory independent review gates (Sentinel and Argus). These fixed acceptance gates do not mean invoking all specialist skills; specialist selection remains proportional to the task. See [local operation contract](../../changes/local-linux-workflow/specs/local-operation/spec.md).

The orchestrator MUST select only capabilities that materially improve the task. It MUST NOT invoke all specialist roles by default.

### ORCH-004 Verification
Completion MUST be based on executed validation where execution is available. The system MUST NOT report an unexecuted test as passing.

### ORCH-005 Residual risk
The final report MUST identify unresolved failures, assumptions and material risks.

### ORCH-006 Stop conditions
The system MUST stop/escalate when required credentials, authorization, destructive approval, critical context or reliable validation is unavailable.
