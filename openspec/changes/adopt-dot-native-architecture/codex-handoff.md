# Codex Handoff

After the pre-Codex repository preparation is complete, execute the remaining tasks in this change.

## Codex objective
Validate the repository itself, implement any gaps revealed by executable checks, and prepare live Dot integration without inventing Dot execution evidence.

## Required sequence
1. Read root AGENTS.md and this OpenSpec change.
2. Run python scripts/validate.py.
3. Inspect CI and repository diff/history.
4. Fix structural/consistency failures.
5. Build/validate behavioral fixtures that can execute locally.
6. Execute Codex-layer scenarios with evidence.
7. Do not mark live Dot scenarios PASS until run through an actual Dot surface.
8. Produce validation/CODEX-PRE-DOT-REPORT.md.
9. Commit/push coherent changes if authorized.

## Stop boundary
Live Dot bootstrap, Dot routing behavior and native Dot approval behavior remain INCONCLUSIVE until a real Dot is available.
