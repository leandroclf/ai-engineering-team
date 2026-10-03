# ADDED Requirements

## Requirement: Linux repository entry point
The system SHALL accept a bounded engineering request from a clean named-branch Git repository and SHALL preserve the operator's checkout. Configuration SHALL be explicit, host-owned and frozen per task.

### Scenario: Dirty target
- WHEN the target has tracked or untracked changes
- THEN execution is blocked without stash, checkout replacement or deletion.

## Requirement: Verified local delivery
The system SHALL require successful host-controlled offline checks and schema-valid Sentinel/Argus reviews on the same final SHA before delivery. The system SHALL NOT automatically merge or deploy.

### Scenario: Stale review or open critical finding
- WHEN review SHA differs or an unverified HIGH/CRITICAL finding exists
- THEN the run cannot reach REVIEWED or publish delivery.

## Requirement: Failure and recovery
The system SHALL preserve observable nonzero exit, timeout and interruption evidence, bound correction cycles and reject concurrent ownership. Unknown external outcomes SHALL block automatic replay.

### Scenario: Interrupted external write
- WHEN push or PR acknowledgement is uncertain
- THEN state remains DELIVERY_PENDING and requires remote reconciliation.

## Requirement: Separate test authority
Repository checks SHALL run without provider account volumes, inherited API/transport credentials, host sockets or outbound network. Git metadata SHALL be read-only to agents; trusted host owns commits and evidence.

### Scenario: Credential/network canary
- WHEN arbitrary check code attempts account lookup or network access
- THEN provider account volume is absent and outbound connection fails.
