# Tasks

- [x] Implement fixed stage profiles and explicit CLI model/effort flags.
- [x] Implement planning/implementation/assessment contracts and OpenSpec handoff.
- [x] Enforce stage-specific mounts, sessions, tools and login paths in command construction.
- [x] Implement bounded repair/replanning and evidence checks at delivery.
- [x] Cover new lifecycle, legacy migration and failures in controlled tests.
- [x] Update current local documentation and bootstrap; distinguish historical harness.
- [x] Run required repository checks and review final diff.
- [x] Run real offline Docker stage mount canaries and pinned CLI/install checks in CI (run 37107965577 on implementation commit 6c239b2).

## External acceptance

- [ ] On operator Linux, rebuild runtime, authenticate all four stage contexts, verify account model access, and execute a small real target task through all stages. This cannot be certified by mocked providers or offline checks.
