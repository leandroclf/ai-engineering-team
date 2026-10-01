# Atlas/Sentinel Disagreement and Waiver Protocol

A disagreement is a first-class engineering artifact.

Sentinel findings contain claim, severity, affected revision/path, reproduction/evidence, expected property and remediation guidance when known. Atlas responds with FIXED, DISPUTED, ACCEPTED_RISK or NOT_APPLICABLE and evidence.

For DISPUTED findings, prefer an independent reproducible check over argument. Sentinel re-reviews the new immutable head SHA after remediation.

CRITICAL/HIGH findings cannot disappear through silence, timeout, new PR revision or majority vote. They close only as FIXED + verified, NOT_APPLICABLE + verified, or an explicit operator waiver where policy permits.

A waiver records operator, finding IDs, rationale, exact revision/scope, expiration/revisit trigger and compensating controls. R3 still requires native/platform approval; a waiver never bypasses it.
