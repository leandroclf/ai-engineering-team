# Context Freshness and Isolation

Before a mutation capture: project_id, repository, target branch, base SHA, nearest AGENTS.md, OpenSpec/change id, policy manifest version and relevant external-state timestamp.

Revalidate after long-running work and immediately before PR merge, release or external write. A changed base SHA or materially changed requirement invalidates assumptions and requires diff/rebase plus re-verification.

Project context is isolated by default. Do not let instructions, credentials, customer data, environment names or remembered decisions from one project become authority in another. The project registry is an index, not a substitute for re-reading repository truth.

Treat memory as a convenience signal, never the source of truth for mutable repository state, permissions, production configuration or current requirements.
