# Incident, Rollback and Recovery

For local `ai-team`, use `status TASK` and `stop TASK`, preserve the task directory and inspect Docker/provider activity separately. Resume only a safe RUNNING checkpoint; reconcile DELIVERY_PENDING against remote state manually. Do not delete login volumes or use broad Docker pruning as automatic recovery. See [local recovery](LOCAL-LINUX-WORKFLOW.md).

When automation may have caused harm:
1. Stop further mutations and open the circuit.
2. Capture task id, timestamps, project, commits/actions, approvals and observed impact.
3. Bound blast radius; protect evidence.
4. Choose safest reversible recovery: revert commit/PR, rollback release, disable automation or restore configuration using repository/provider-native mechanisms.
5. Validate recovery with objective health checks.
6. Communicate status and residual risk.
7. Add a regression scenario and update policy only when evidence identifies a systemic gap.

Never delete evidence to make a rerun look clean. Recovery actions inherit the original risk or higher.
