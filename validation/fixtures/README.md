# Provider CLI Execution Fixture Pack

These fixtures are prepared in CHAT-GITHUB and executed only in the runtime assigned by docs/EXECUTION-ENVIRONMENTS.md.

## Rules
- Never contain real credentials, customer data, production targets or destructive operations.
- Every execution binds the current repository SHA and scenario ID.
- Provider runtime output is evidence only when observable and preserved under validation/runs/.
- Missing CLI/Dot capability is BLOCKED/INCONCLUSIVE, never PASS.
- Safety scenarios use harmless sentinel files or text fixtures.

## Execution order
1. OPENAI-CLI-A: S01-S06 and applicable H scenarios.
2. OPENAI-DOT-A: Dot routing/handoff and H01-H10.
3. OPENAI-DOT-B: AS01-AS10 with Atlas.
4. CLAUDE-CLI / Argus: CA01-CA08.
5. CROSS-ENV: end-to-end immutable revision handoff.

Use validation/RUN-MANIFEST-TEMPLATE.yaml for every run.
