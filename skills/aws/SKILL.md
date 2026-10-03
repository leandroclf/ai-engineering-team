---
name: aws
description: AWS architecture and implementation extension.
---
# AWS
Identify environment assumptions before changes. Apply least privilege, encryption, retry/backoff, idempotency and DLQ patterns where relevant. Treat IAM, networking, data deletion and production changes as elevated risk. Prefer infrastructure as code.

## Inputs
AWS repository, environment, data classification, IAM scope and recovery requirements.

## Outputs
Infrastructure change, permission model, resilience controls and rollback plan.

## Boundaries
IAM, networking, data deletion and production changes are R3; never apply them without explicit/native approval.

## Validation
Check least privilege, encryption, retry/idempotency, failure isolation, observability and reversible deployment.
