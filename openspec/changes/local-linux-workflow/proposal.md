# Local Linux workflow

Status: IN_IMPLEMENTATION; authenticated acceptance required before production readiness.

## Objective
From the root of an existing Git repository, an operator can issue one request and obtain a planned, implemented, tested and independently reviewed branch. Atlas and Sentinel use Codex; Argus uses Claude. A small deterministic CLI coordinates official executors, without replacing Dots or inventing provider agents.

## Scope
Install once on Linux; project configuration outside agent mounts; doctor/login/init/run/status/resume/stop/deliver; disposable independent Git clone; bounded corrections; credential-free offline tests; exact-head structured reviews; private atomic state and host evidence; exclusive execution; stale-process reconciliation; explicit delivery permission with uncertain writes blocked.

## Non-goals
Automatic merge/deploy, account provisioning, host package installation, hostile-code isolation from kernel vulnerabilities, guaranteed remote cancellation, provider spend guarantees, automatic API billing or model replacement. The operator chooses trusted target repositories, test images and providers.

## Production acceptance
Code/CI tests are necessary but insufficient. Validate real subscription logins, first target task, both independent reviews, cancellation and crash recovery on the operator's Linux host. Preserve failed results and never report mocks as live provider execution.
