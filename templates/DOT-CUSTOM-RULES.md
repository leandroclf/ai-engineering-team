# Suggested Engineering Dot Custom Rules

- Use ai-engineering-team as the default engineering governance source.
- Before changing a repository, read its current applicable AGENTS.md and OpenSpec/project instructions.
- Use Codex for non-trivial repository implementation, tests, command execution and code review.
- Do not bypass plugin/provider/platform permission or approval requirements.
- Treat production/destructive/irreversible engineering operations as R3 and require explicit authorization in addition to any native approval.
- Do not claim tests, CI, deployment or validation passed unless observable evidence confirms it.
- Prefer pull requests and reversible changes to direct production/protected-branch mutation.
- If repository state conflicts with remembered context, repository state wins and the discrepancy must be reported.
- Keep specialist delegation bounded; do not fan out merely because specialists exist.
