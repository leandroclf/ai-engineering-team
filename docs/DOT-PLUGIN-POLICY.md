# Dot Plugin and Permission Policy
## Principles
Least privilege, explicit scope, observable side effects and native approvals.
## Access matrix
For each plugin/app record purpose, data scope, read/write capability, approval behavior, environments and owner.
## GitHub
Read access supports discovery. Writes follow repository workflow. Merge, protected-branch, settings and release/deployment actions follow applicable authorization.
## CI / observability
Prefer read-only inspection by default. Mutating pipelines, alerts or production configuration is elevated risk.
## Production
No bootstrap grants production mutation by default. Native approvals remain in force and R3 adds an engineering approval boundary.
## Denial
If access is denied/unavailable, report BLOCKED or INCONCLUSIVE. Do not seek an alternate path intended to bypass denied permission.
