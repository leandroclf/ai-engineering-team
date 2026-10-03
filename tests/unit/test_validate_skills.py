import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from scripts import validate_skills


class SkillCatalogTests(unittest.TestCase):
    def test_current_catalog_is_publishable(self):
        self.assertEqual(validate_skills.main(), 0)

    def test_cycle_and_unknown_dependency_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skills = root / "skills"
            for name, dependency in (("one", "two"), ("two", "one")):
                folder = skills / name
                folder.mkdir(parents=True)
                (folder / "SKILL.md").write_text(
                    f"---\nname: {name}\ndescription: test\n---\n# Skill\n"
                    "## Inputs\n- request\n## Outputs\n- result\n"
                    "## Boundaries\n- bounded\n## Validation\n- check\n"
                )
            (skills / "catalog.yaml").write_text(
                "catalog_version: 1.0.0\nskills:\n"
                "  - id: one\n    path: skills/one\n    version: 1.0.0\n"
                "    status: stable\n    category: implementation\n    risk: R1\n"
                "    tags: [x]\n    owner: test\n    requires: [two, missing]\n"
                "    composes_with: []\n    supported_surfaces: [codex]\n"
                "    inputs: [x]\n    outputs: [x]\n    quality_gates: [x]\n"
                "  - id: two\n    path: skills/two\n    version: 1.0.0\n"
                "    status: stable\n    category: implementation\n    risk: R1\n"
                "    tags: [x]\n    owner: test\n    requires: [one]\n"
                "    composes_with: []\n    supported_surfaces: [codex]\n"
                "    inputs: [x]\n    outputs: [x]\n    quality_gates: [x]\n"
            )
            with patch.object(validate_skills, "ROOT", root), patch.object(validate_skills, "CATALOG", skills / "catalog.yaml"):
                self.assertEqual(validate_skills.main(), 1)
