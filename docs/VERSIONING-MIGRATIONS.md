# Governance Versioning and Migrations

Policy schemas use semantic versions. Templates include schema_version. Backward-compatible additions increment MINOR; incompatible field/meaning changes increment MAJOR.

A breaking governance change requires: migration note, affected artifacts/projects, compatibility window, rollback path, validator update and project-registry compatibility declaration.

The Dot must not silently reinterpret an older task/evidence envelope under a newer incompatible schema. Rehydrate or migrate it explicitly.
