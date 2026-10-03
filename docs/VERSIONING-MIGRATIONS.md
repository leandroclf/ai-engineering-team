# Governance Versioning and Migrations

Local CLI version 0.1.0 and governance schema versions are distinct. Updating the framework requires deliberate Git update/reinstallation while no tasks are active. Target config and task state have their own format checks; there is no automatic migration or image replacement for an existing task. See [installation/update](LOCAL-LINUX-WORKFLOW.md).

Policy schemas use semantic versions. Templates include schema_version. Backward-compatible additions increment MINOR; incompatible field/meaning changes increment MAJOR.

A breaking governance change requires: migration note, affected artifacts/projects, compatibility window, rollback path, validator update and project-registry compatibility declaration.

The Dot must not silently reinterpret an older task/evidence envelope under a newer incompatible schema. Rehydrate or migrate it explicitly.
