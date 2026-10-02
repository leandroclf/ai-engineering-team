# Design

Reuse `provider_run.py`, `pr_chain.sh` and the existing manifest statuses (PASS, FAIL, BLOCKED, INCONCLUSIVE). Missing executable maps to BLOCKED with exit 127; timeout maps to INCONCLUSIVE with exit 124. Ordinary provider/setup/check failures map to FAIL. A successful process remains INCONCLUSIVE until evaluated. All failed checks return a nonzero harness exit.

`review_status.py` parses a single plain YAML result or a single fenced YAML result, validates the declared head SHA against the run and expected PR SHA, and verifies the provider exit and exact-head check evidence. Only PASS/PASS_WITH_FINDINGS with acceptable runtime evidence can map to GitHub success. FAIL/BLOCKED are terminal failure; invalid/missing evidence is terminal error.

CI polling defaults to 600 seconds (`CI_TIMEOUT_SECONDS`), then stops. A failed CI does not start reviewers. Each background reviewer PID is awaited separately; either failure produces a nonzero chain exit even when the other succeeds. Existing validation-only PR closure is retained. On earlier failure after PR creation, the PR may remain draft and the operator must inspect recorded transport evidence before cleanup. No automatic production rollback or permission changes are introduced.

These are transport controls, not proof of review correctness, authorized tool execution, account independence, live revocation, or an authenticated Codex/Claude session. Timeout of a CLI client does not prove a remote provider task has stopped; live cancellation must be verified separately.
