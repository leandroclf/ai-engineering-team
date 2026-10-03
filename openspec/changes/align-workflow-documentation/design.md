# Design

Three explicit operation modes: local bounded CLI, native persistent Dots and historical scenario/PR harness. Link each entry point to its own setup and evidence rules. Local reviews precede delivery; GitHub CI follows delivery and does not imply merge/deploy authorization.

Installer preflight checks Linux, Python/venv/ensurepip, Git, readlink, Docker daemon and destination conflict before package/image mutation. Compose is required only by the legacy harness. Preserve files/directories/foreign or broken links; permit the existing link to the same framework. Build before publishing; recheck the destination after build and create a new link without force. Failed install may retain venv/image layers and is not a transactional rollback. `--check` is read-only; `AI_TEAM_BIN_DIR` selects a user destination.

Consolidated numbered documents retain baseline identifiers, generated traceability and historical analysis; current operational navigation and overview explicitly supersede obsolete installation/runtime facts. Dated execution reports remain immutable. A bounded Markdown checker scans repository-owned local targets and fences without fetching external sources or claiming full Markdown parsing.
