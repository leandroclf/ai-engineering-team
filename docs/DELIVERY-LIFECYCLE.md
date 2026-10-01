# Branch, PR, CI and Release Lifecycle

Default mutation strategy: feature branch/worktree -> focused commits -> PR -> required CI -> review -> merge. Direct main writes are reserved for explicitly permitted low-risk repository policy and must still be validated.

Required before merge: fresh base, no unresolved lease conflict, diff review, required tests/checks actually executed, security impact assessed, evidence record updated and repository protection satisfied.

Release/deployment is a distinct action from merge. Production release is R3 unless a stricter project policy says otherwise; it requires explicit authorization plus all native/provider approvals. After release, observe health signals and retain rollback coordinates.

Never treat a successful commit or PR creation as successful deployment.
