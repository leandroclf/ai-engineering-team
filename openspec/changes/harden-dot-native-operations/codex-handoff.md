# CODEX-PRE-DOT handoff

Required runtime: authenticated OPENAI-CLI-A, then OPENAI-DOT-A for Dot integration. Read AGENTS.md, current HEAD, this change and `docs/DOT-NATIVE-OPERATION-GATES.md`. Do not use a synthetic example as live authorization.

1. Install validation dependencies and execute all repository checks.
2. Obtain a task-scoped lease and trusted current scope state from the operator/native adapter. Record exact base SHA, command/evidence provenance and environment.
3. Run a reversible sandbox task; revalidate authorization before each operation. Preserve command outputs/exit codes, actual diff/final SHA and CI from GitHub.
4. Exercise revocation, expired/future scope, base drift, denied permission, exhausted budget and missing/failed Codex output. Stop, preserve the observed failure and never fabricate PASS.
5. Validate the structured evidence, then independent Sentinel/Argus review on the same SHA. Keep account-independence limitation until W-001 is resolved.
6. Bootstrap/live Dot routing requires actual Dot access; leave D8 open if unavailable.

This environment's preflight result is UNAVAILABLE (Codex CLI absent), not a provider failure or proof the previously validated container runtime has regressed.
