from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "AGENTS.md", "README.md",
    "skills/tech-lead/SKILL.md", "skills/architect/SKILL.md", "skills/backend/SKILL.md",
    "skills/qa/SKILL.md", "skills/security/SKILL.md", "skills/code-review/SKILL.md",
    "skills/observability/SKILL.md", "skills/java-spring/SKILL.md",
    "skills/node-typescript/SKILL.md", "skills/python-fastapi/SKILL.md",
    "skills/aws/SKILL.md", "skills/kubernetes/SKILL.md", "skills/github-workflow/SKILL.md",
    "docs/QUALITY-GATES.md", "docs/DOT-NATIVE-ARCHITECTURE.md",
    "docs/DOT-PLUGIN-POLICY.md", "docs/DOT-OPERATING-MODEL.md",
    "docs/PROJECT-ONBOARDING.md", "docs/SPECIALIZED-DOTS.md",
    "docs/DOT-RELIABILITY.md", "docs/CONTEXT-FRESHNESS.md",
    "docs/UNTRUSTED-CONTENT.md", "docs/CONCURRENCY.md",
    "docs/DELIVERY-LIFECYCLE.md", "docs/INCIDENT-RECOVERY.md",
    "docs/VERSIONING-MIGRATIONS.md", "docs/ROUTING-MATRIX.md",
    "docs/CONTEXT-BUDGETS.md", "docs/PORTFOLIO-GOVERNANCE.md", "docs/DOT-CALIBRATION.md",
    "docs/adr/0001-dot-native-runtime-boundary.md",
    "docs/ATLAS-SENTINEL-ARCHITECTURE.md", "docs/DUAL-DOT-AUTHORITY.md",
    "docs/DUAL-DOT-DISAGREEMENT.md",
    "templates/PROJECT-AGENTS.md", "templates/COMPLETION-REPORT.md",
    "templates/ENGINEERING-DOT-BOOTSTRAP.md", "templates/DOT-CUSTOM-RULES.md",
    "templates/DOT-CODEX-TASK.md", "templates/CODEX-DOT-RESULT.md",
    "templates/PROJECT-REGISTRY.yaml", "templates/PLUGIN-ACCESS-MATRIX.yaml",
    "templates/TASK-ENVELOPE.yaml", "templates/WORK-LEASE.yaml",
    "templates/EVIDENCE-RECORD.yaml", "templates/INCIDENT-RECORD.md",
    "templates/POLICY-MANIFEST.yaml",
    "templates/ATLAS-BOOTSTRAP.md", "templates/SENTINEL-BOOTSTRAP.md",
    "templates/ATLAS-SENTINEL-REVIEW-REQUEST.yaml", "templates/SENTINEL-REVIEW-RESULT.yaml",
    "templates/RISK-ACCEPTANCE-WAIVER.yaml", "templates/DUAL-DOT-REGISTRY.yaml",
    "runbooks/ATLAS-PRIMARY-ACCOUNT.md", "runbooks/SENTINEL-SECONDARY-ACCOUNT.md",
    "validation/README.md", "validation/EVIDENCE-TEMPLATE.md",
    "validation/HARDENING-SCENARIOS.md", "validation/DUAL-DOT-SCENARIOS.md",
    "validation/CLAUDE-ASSURANCE-SCENARIOS.md", "validation/RUN-MANIFEST-TEMPLATE.yaml",
    "validation/CLI-EXECUTION-QUEUE.md", "validation/fixtures/README.md",
    "docs/EXECUTION-ENVIRONMENTS.md",
    "openspec/changes/adopt-dot-native-architecture/proposal.md",
    "openspec/changes/adopt-dot-native-architecture/design.md",
    "openspec/changes/adopt-dot-native-architecture/tasks.md",
    "openspec/changes/adopt-dot-native-architecture/codex-handoff.md",
    "openspec/changes/harden-engineering-dot/proposal.md",
    "openspec/changes/harden-engineering-dot/design.md",
    "openspec/changes/harden-engineering-dot/tasks.md",
    "openspec/changes/adopt-atlas-sentinel/proposal.md",
    "openspec/changes/adopt-atlas-sentinel/design.md",
    "openspec/changes/adopt-atlas-sentinel/tasks.md",
]
errors = []
for rel in required:
    p = ROOT / rel
    if not p.exists() or not p.read_text(encoding="utf-8").strip():
        errors.append(f"missing/empty: {rel}")

for p in (ROOT / "skills").glob("*/SKILL.md"):
    text = p.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\nname:" not in text or "\ndescription:" not in text:
        errors.append(f"invalid skill frontmatter: {p.relative_to(ROOT)}")

agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
for token in ["FRESHNESS", "DISCOVER", "PLAN", "VERIFY", "REVIEW", "R3", "Definition of Done", "idempotency"]:
    if token not in agents:
        errors.append(f"AGENTS.md missing contract token: {token}")

dot_rules = (ROOT / "templates/DOT-CUSTOM-RULES.md").read_text(encoding="utf-8")
for token in ["Codex", "R3", "AGENTS.md"]:
    if token not in dot_rules:
        errors.append(f"DOT-CUSTOM-RULES missing: {token}")

registry = (ROOT / "templates/PROJECT-REGISTRY.yaml").read_text(encoding="utf-8")
for token in ["leandroclf/ai-engineering-team", "schema_version", "compatible_governance", "bind_base_sha"]:
    if token not in registry:
        errors.append(f"project registry missing: {token}")

manifest = (ROOT / "templates/POLICY-MANIFEST.yaml").read_text(encoding="utf-8")
for token in ["schema_version", "untrusted_content", "concurrency", "recovery", "routing"]:
    if token not in manifest:
        errors.append(f"policy manifest missing: {token}")

scenarios = (ROOT / "validation/HARDENING-SCENARIOS.md").read_text(encoding="utf-8")
for token in ["stale context", "prompt injection", "idempotent retry", "lease conflict", "release separation"]:
    if token not in scenarios:
        errors.append(f"hardening scenarios missing: {token}")

dual = (ROOT / "templates/DUAL-DOT-REGISTRY.yaml").read_text(encoding="utf-8")
for token in ["atlas", "sentinel", "independent_approval: false", "production_write: false", "direct_dot_to_dot_required: false"]:
    if token not in dual:
        errors.append(f"dual-dot registry missing: {token}")

dual_scenarios = (ROOT / "validation/DUAL-DOT-SCENARIOS.md").read_text(encoding="utf-8")
for token in ["no self-approval", "independent blocking finding", "stale verdict", "permission asymmetry", "explicit waiver", "review independence"]:
    if token not in dual_scenarios:
        errors.append(f"dual-dot scenarios missing: {token}")

execution_env = (ROOT / "docs/EXECUTION-ENVIRONMENTS.md").read_text(encoding="utf-8")
for token in ["Atlas", "Sentinel", "Argus", "OPENAI-CLI-A", "OPENAI-DOT-A", "OPENAI-DOT-B", "CLAUDE-CLI", "HUMAN"]:
    if token not in execution_env:
        errors.append(f"execution environment matrix missing: {token}")

run_manifest = (ROOT / "validation/RUN-MANIFEST-TEMPLATE.yaml").read_text(encoding="utf-8")
for token in ["scenario_id", "environment", "agent_name", "head_sha", "status", "evidence_locations"]:
    if token not in run_manifest:
        errors.append(f"run manifest missing: {token}")

fixture_required = [
    "validation/fixtures/s01-doc-task/target.md",
    "validation/fixtures/s03-precedence/AGENTS.md",
    "validation/fixtures/s04-failure/README.md",
    "validation/fixtures/s05-r3/DO-NOT-TOUCH.sentinel",
    "validation/fixtures/h02-prompt-injection/untrusted.txt",
    "validation/fixtures/as02-known-high/authorization-policy.md",
    "validation/fixtures/ca02-known-defect/sample.py",
    "validation/fixtures/s02-backend/app.py",
    "validation/fixtures/s04-failure/check.py",
    "validation/fixtures/s06-reconciliation/pricing.py",
    "validation/fixtures/ca07-unlabeled-injection/permissions.py",
]
for rel in fixture_required:
    p = ROOT / rel
    if not p.exists() or not p.read_text(encoding="utf-8").strip():
        errors.append(f"missing/empty execution fixture: {rel}")

for manifest in sorted((ROOT / "validation/runs").glob("*/manifest.yaml")):
    statuses = [l.split(":", 1)[1].strip() for l in manifest.read_text(encoding="utf-8").splitlines() if l.startswith("status:")]
    if len(statuses) != 1 or statuses[0] not in {"PASS", "FAIL", "BLOCKED", "INCONCLUSIVE"}:
        errors.append(f"run manifest without single allowed status: {manifest.relative_to(ROOT)}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: framework, Dot-native and hardening structure validated ({len(required)} required artifacts)")
