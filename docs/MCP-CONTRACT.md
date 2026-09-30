# MCP / Tool Adapter Contract
Tools extend capability; they do not override governance.
- Discover/read before mutation.
- Request minimum permissions.
- Treat external side effects according to R0-R3.
- Verify resulting state instead of inferring success from submission.
- Keep provider-specific behavior outside generic skills when possible.
