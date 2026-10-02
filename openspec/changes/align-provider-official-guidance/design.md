# Design

Use one provider-review JSON schema with quality, security, architecture, observability, findings, role and exact SHA. Codex receives `--output-schema`; Claude receives `--json-schema` and JSON output, extracted from `structured_output`. The host validates independently. New PR-chain runs require `review.json`; legacy YAML remains readable only for historical audits.

Require quality/security PASS or PASS_WITH_FINDINGS; reject explicit failed gates and unresolved/unverified HIGH/CRITICAL findings. No automatic waiver flow is added. These checks constrain the claim, not its factual truth or the account identity.

Codex host Sentinel uses read-only sandbox and never prompts; containers retain their documented external isolation boundary. Claude uses restricted mode, explicit tools, deny for MCP, dontAsk and denied interactive prompts. Managed settings remain authoritative. Thirty turns bound an Argus invocation; timeouts remain separate. Required flags are probed without executing a model or auto-installing updates.

On POSIX, local process groups are terminated after timeout. Remote sessions, detached containers and delegated Dot tasks require separate cancellation/reconciliation. GitHub/SSH transport environment variables are removed from provider subprocesses; credentials stored on disk are not thereby isolated.

Both test suites remain separate CI commands so unittest discovery does not silently miss tests/unit. CI uses read-only token permissions, no persistent git credentials, pinned Actions v7, a timeout and concurrency cancellation. The Docker build uses root context only to copy pinned validation requirements, with dockerignore preventing unrelated files/credentials from entering the build.

No migration to API billing, new accounts, privileged rulesets, production or custom orchestration runtime occurs in this change.
