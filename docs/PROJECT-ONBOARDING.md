# Project Onboarding

## Local Linux — current entry point

Install the framework once using the [Linux guide](LOCAL-LINUX-WORKFLOW.md). In the target repository, inspect AGENTS/OpenSpec and real setup/test/lint/build commands. Prepare a trusted offline test image, commit configuration files, and use a clean named branch with origin configured. Run `ai-team init --test-image IMAGE --check 'REAL COMMAND'`, repeating checks in execution order. Configuration is external to the target; init neither copies templates nor registers a Dot.

Use [PROJECT-AGENTS](../templates/PROJECT-AGENTS.md) only if instructions are missing. Start with a small task, inspect both reviews and offline evidence, then deliver a branch/PR and observe CI. Complete live account/host acceptance before expanding scope. Do not import project secrets into test images or cross-project prompts.

## Dot / portfolio registration

1. Add a project-registry entry.
2. Read the repository's current AGENTS.md and engineering docs.
3. Adapt templates/PROJECT-AGENTS.md only when the target lacks adequate instructions.
4. Record default branch, OpenSpec location, environments and read/write boundaries.
5. Identify native setup/test/lint/typecheck/build commands.
6. Identify sensitive paths and R2/R3 operations.
7. Start read-only; enable writes only when required and authorized.
8. Run a harmless R0/R1 calibration task before material work.
9. Record evidence and discrepancies between remembered and current repository state.

Cross-project context must not be copied unless required for the task. Revalidate each repository independently before mutation.
