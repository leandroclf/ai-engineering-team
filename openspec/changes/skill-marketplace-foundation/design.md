# Design

`skills/catalog.yaml` is a versioned discovery index. Each entry has immutable `id`/path identity, SemVer, lifecycle status, category, tags, owner, risk, dependencies, composition hints, supported surfaces, inputs, outputs and quality gates. `SKILL.md` remains the normative procedure and adds Inputs, Outputs, Boundaries and Validation sections.

`scripts/validate_skills.py` parses the catalog and front matter, validates allowed values and SemVer, checks package/catalog parity, checks required sections, verifies dependency references and detects cycles. It is deterministic and offline. The validator does not certify model compliance, license compatibility or security of arbitrary third-party packages.

The marketplace is repository-native in this phase: discovery and review happen through Git/PR/CI. A future external registry must preserve immutable artifacts, provenance/checksums, license metadata, compatibility constraints, revocation/deprecation and least-privilege installation. Automatic installation and permission expansion remain out of scope.
