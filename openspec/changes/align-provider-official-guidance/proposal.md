# Align provider integrations with official guidance

## Why
PRs #10 and #11 add complementary controls but overlap in CI and OpenSpec. The harness still requests free-form reviewer YAML, loads project Claude settings, omits explicit unattended permission handling and can leave local descendants after timeout. Container validation dependencies diverge from CI. Provider documentation now supplies applicable structured-output, restricted-mode and approval interfaces.

## Scope
Consolidate both PRs without merging main; harden provider command construction, review parsing, runtime failure handling, preflight and CI. Record official source URLs and review date in `docs/PROVIDER-GUIDANCE-REVIEW.md`. Extend the existing hardening plan rather than declaring Dot acceptance complete.

## Acceptance
All previous suites and new adversarial cases pass; invalid structured output cannot become success; CLI authentication data is not emitted by probes; GitHub transport credentials are not inherited by provider children; current official Actions are pinned and CI passes. No claim of live provider/Dot/container validation without execution evidence.
