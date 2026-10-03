# Design

CLI configuration and runs live under XDG state directories, indexed by canonical repository path. Each run pins base SHA, config and request. Git cloning avoids modifying the user's checkout and exposing its Git authority; only the disposable clone is mounted into agents. Dirty target input is rejected, not stashed or overwritten.

Provider containers run as non-root with read-only rootfs, no capabilities/socket/host token, bounded output and timeouts. Each role has a separate named login volume; Sentinel/Argus checkout is read-only. Agent output staging is distinct from trusted host evidence. Tests run in a separate container without login volumes or network, copying the snapshot into a temporary writable work directory. Images must be prepared for offline dependencies.

The host owns commits, validation exit status and final hashes. Exact-head JSON reviews use the existing schema, mandatory quality/security gates and blocking finding policy. Corrections have bounded cycles. Configuration is frozen; target HEAD and origin are rechecked before delivery. Only clean, reviewed final HEAD can be delivered. Default behavior is local; push and PR are a separate explicit command. There is no automatic merge/deploy.

Per-run and per-target flock prevent concurrent execution; atomic rename/fsync protects state. Resume continues completed checkpoints but interrupted processes block for operator inspection, rather than silently replaying effects. Stop requests are polled while running, verified process groups are terminated, and named containers are removed. This establishes local stop only, not remote provider cancellation.

The native CLI policy governs individual agent tool calls. This coordinator authorizes its own stages, not every internal tool operation; a trusted native adapter remains separate follow-up. Evidence protection assumes trusted host/user and Docker daemon. Same-account role separation is not account independence.
