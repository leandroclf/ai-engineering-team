# Concurrency, Leases and Conflict Control

Mutating tasks SHOULD acquire a logical lease.

Lease key: project_id + repository + change_surface.
Fields: task_id, owner, base_sha, paths/scope, acquired_at, expires_at, heartbeat_at, conflict_policy.

A lease is advisory governance, not a replacement for Git branch protection. If another active task overlaps files, schema, infrastructure or release surface, stop and reconcile. Expired leases require state revalidation before takeover.

Parallel work is preferred only when scopes are demonstrably independent. Merge order is explicit; the later task rebases/revalidates against the new base.
