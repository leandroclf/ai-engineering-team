---
name: node-typescript
description: Node.js and TypeScript engineering extension.
---
# Node / TypeScript
Detect package manager from lockfiles. Preserve tsconfig, module and runtime conventions. Keep types strict. Respect async error handling and resource lifecycle. Use existing lint, typecheck, test and build scripts.

## Inputs
Node repository, lockfile/package manager, runtime version and existing scripts.

## Outputs
Stack-aligned change, tests, type-check and build results.

## Boundaries
Preserve module/runtime conventions, lockfiles and asynchronous resource lifecycle.

## Validation
Run native lint, strict type-check, tests and build; report unavailable scripts explicitly.
