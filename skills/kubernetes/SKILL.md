---
name: kubernetes
description: Kubernetes workload and platform engineering extension.
---
# Kubernetes
Respect existing manifests, Helm or Kustomize conventions. Review requests/limits, probes, disruption, rollout, security context and service exposure. Production or destructive cluster actions are R3. Prefer declarative changes and dry-run/template validation.

## Inputs
Cluster manifests, Helm/Kustomize conventions, environment and service objectives.

## Outputs
Manifest change, rollout plan, health gates and resource/security impact.

## Boundaries
Cluster, production and destructive actions are R3; do not mutate a live cluster from a review-only workflow.

## Validation
Run render/schema checks and dry-run where authorized; inspect resources, probes, rollout, security context and exposure.
