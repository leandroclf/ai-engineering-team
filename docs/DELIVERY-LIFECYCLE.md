# Branch, PR, CI and Release Lifecycle

Default mutation strategy: feature branch/worktree -> focused commits -> PR -> required CI -> review -> merge. Direct main writes are reserved for explicitly permitted low-risk repository policy and must still be validated.

Required before merge: fresh base, no unresolved lease conflict, diff review, required tests/checks actually executed, security impact assessed, evidence record updated and repository protection satisfied.

Release/deployment is a distinct action from merge. Production release is R3 unless a stricter project policy says otherwise; it requires explicit authorization plus all native/provider approvals. After release, observe health signals and retain rollback coordinates.

Never treat a successful commit or PR creation as successful deployment.

## Local CLI delivery

`ai-team run` implements in an independent clone, commits on the host, executes offline checks and requires Sentinel/OpenAI validation and isolated Atlas/Claude review on the exact SHA before REVIEWED. `ai-team deliver TASK` imports a new branch into the target without changing its checkout; `--push` publishes and `--pr` publishes/opens a draft PR through the operator's Git/gh. Revalidate target/base/origin and run GitHub CI on the delivered SHA. No automatic merge or deployment is implemented.

DELIVERY_PENDING means an external write may have happened: inspect remote branch/PR before proceeding; no automatic replay. Follow the [local recovery guide](LOCAL-LINUX-WORKFLOW.md). The historical `pr_chain.sh` validates transport and closes its fixture PR unmerged; it is not the local delivery command.
