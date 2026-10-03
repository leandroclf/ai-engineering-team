import unittest

from scripts import validate_skill_evaluations


class SkillEvaluationTests(unittest.TestCase):
    def test_repository_evaluation_contract_is_valid(self):
        self.assertEqual(validate_skill_evaluations.main(), 0)
