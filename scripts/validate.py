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
    "docs/adr/0001-dot-native-runtime-boundary.md",
    "templates/PROJECT-AGENTS.md", "templates/COMPLETION-REPORT.md",
    "templates/ENGINEERING-DOT-BOOTSTRAP.md", "templates/DOT-CUSTOM-RULES.md",
    "templates/DOT-CODEX-TASK.md", "templates/CODEX-DOT-RESULT.md",
    "templates/PROJECT-REGISTRY.yaml", "templates/PLUGIN-ACCESS-MATRIX.yaml",
    "validation/README.md", "validation/EVIDENCE-TEMPLATE.md",
    "openspec/changes/adopt-dot-native-architecture/proposal.md",
    "openspec/changes/adopt-dot-native-architecture/design.md",
    "openspec/changes/adopt-dot-native-architecture/tasks.md",
    "openspec/changes/adopt-dot-native-architecture/codex-handoff.md",
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
for token in ["DISCOVER", "PLAN", "VERIFY", "REVIEW", "R3", "Definition of Done"]:
    if token not in agents:
        errors.append(f"AGENTS.md missing contract token: {token}")

dot_rules = (ROOT / "templates/DOT-CUSTOM-RULES.md").read_text(encoding="utf-8")
for token in ["Codex", "R3", "AGENTS.md"]:
    if token not in dot_rules:
        errors.append(f"DOT-CUSTOM-RULES missing: {token}")

registry = (ROOT / "templates/PROJECT-REGISTRY.yaml").read_text(encoding="utf-8")
if "leandroclf/ai-engineering-team" not in registry:
    errors.append("project registry does not self-register ai-engineering-team")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: framework and Dot-native structure validated ({len(required)} required artifacts)")
