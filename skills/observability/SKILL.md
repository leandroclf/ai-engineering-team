---
name: observability
description: Ensures changes are diagnosable and operationally measurable.
---
# Observability
Evaluate logs, metrics, traces, correlation, health signals, SLO impact and alertability when relevant. Avoid noisy or high-cardinality telemetry. Prefer existing instrumentation conventions.

## Inputs
Change request, runtime signals, service objectives and existing telemetry conventions.

## Outputs
Signals, correlation fields, dashboard/alert changes and SLO impact.

## Boundaries
Avoid high-cardinality or sensitive telemetry; do not create noisy alerts without an operator response.

## Validation
Confirm diagnosability, useful correlation, bounded cardinality, alertability and failure visibility.
