---
name: python-fastapi
description: Python and FastAPI engineering extension.
---
# Python / FastAPI
Detect environment, package manager and supported Python version. Respect sync/async boundaries, Pydantic version and dependency injection. Validate API schemas and errors. Use repository formatting, typing and test tools.

## Inputs
Python repository, supported version, package manager, Pydantic version and sync/async conventions.

## Outputs
Stack-aligned change, schema/error behavior and test results.

## Boundaries
Preserve dependency-injection and sync/async boundaries; do not introduce unbounded network or blocking work.

## Validation
Run native formatting, typing, API schema and test commands for changed behavior and errors.
