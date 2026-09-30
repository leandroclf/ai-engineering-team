from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "AGENTS.md",
    "skills/tech-lead/SKILL.md",
    "skills/architect/SKILL.md",
    "skills/backend/SKILL.md",
    "skills/qa/SKILL.md",
    "skills/security/SKILL.md",
    "skills/code-review/SKILL.md",
    "skills/observability/SKILL.md",
    "skills/java-spring/SKILL.md",
    "skills/node-typescript/SKILL.md",
    "skills/python-fastapi/SKILL.md",
    "skills/aws/SKILL.md",
    "skills/kubernetes/SKILL.md",
    "skills/github-workflow/SKILL.md",
    "docs/QUALITY-GATES.md",
    "templates/PROJECT-AGENTS.md",
    "templates/COMPLETION-REPORT.md",
    "tests/scenarios.md",
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

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: framework structure validated ({len(required)} required artifacts)")
