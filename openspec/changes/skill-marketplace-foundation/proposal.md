# Skill marketplace foundation

## Problem
The repository has useful skills, but their metadata and contracts are too small for reliable discovery, composition, versioning and production distribution. A marketplace cannot safely select packages from names and descriptions alone.

## Objectives
Define a repository-native catalog for publishable skills; standardize identity, semantic version, category, maturity, dependencies, supported surfaces, risk, input/output contracts, boundaries and quality gates; validate catalog/package consistency and dependency cycles in CI; document publication and promotion rules.

## Scope
Existing 13 skills, catalog, package contract sections, validator, unit tests, CI and documentation. Preserve paths and current behavior. No automatic installation, permission granting, provider billing, external registry or live marketplace service.

## Acceptance
Every current skill has a valid catalog entry and contract sections. Validator rejects malformed metadata, missing packages, unknown/cyclic dependencies and filesystem/catalog drift. CI executes it. Publication rules distinguish experimental, beta, stable and deprecated packages and require evidence-based promotion.
