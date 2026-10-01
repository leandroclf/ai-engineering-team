# Adopt Atlas + Sentinel Dual-Dot Model

Status: IN_PROGRESS

## Decision
Use two intentionally asymmetric Engineering Dots across two OpenAI accounts.

- **Atlas** — primary Engineering Lead Dot on the primary account.
- **Sentinel** — independent Quality & Security Dot on the secondary account.

GitHub/OpenSpec/evidence are the shared coordination substrate. Direct Dot-to-Dot communication is not required for correctness.

## Goals
- Separate creation from independent assurance.
- Prevent self-approval of material engineering work.
- Make disagreement explicit, evidence-based and auditable.
- Keep Sentinel lower-privilege and independent by default.
- Preserve the existing Dot -> Codex execution model.
- Remain compatible with future native multi-Dot capabilities without depending on them.

## Non-goals
- Two general-purpose Dots doing duplicate work.
- Consensus by conversation alone.
- Giving Sentinel production mutation rights by default.
- Replacing native OpenAI, GitHub or provider protections.
- Building a custom Dot-to-Dot transport.

## Exit criteria
Atlas/Sentinel roles, authority matrix, handoff/review contracts, disagreement protocol, bootstrap/runbooks, validation scenarios and CI structural checks are version-controlled and pass CI. Live cross-account behavior remains pending until both Dots exist.
