import unittest

from scripts.validate_pr_paths import allowed_change, violations


class ValidatePlanningPRPathsTests(unittest.TestCase):
    def test_evidence_and_card_work_paths_are_allowed(self):
        self.assertTrue(allowed_change("A", "evidence/lane/akte.md"))
        self.assertTrue(allowed_change("M", "tasks/t-example.md"))
        self.assertTrue(allowed_change("M", "releases/v0.4.28.md"))

    def test_validator_implementation_paths_are_narrowly_allowed(self):
        self.assertTrue(allowed_change("M", ".github/workflows/validate.yml"))
        self.assertTrue(allowed_change("A", "scripts/validate_pr_paths.py"))
        self.assertTrue(allowed_change("A", "scripts/tests/test_validate_pr_paths.py"))
        self.assertFalse(allowed_change("M", "scripts/plan.py"))

    def test_root_akte_can_only_be_deleted_during_collision_cleanup(self):
        self.assertTrue(allowed_change("D", "akte.md"))
        self.assertFalse(allowed_change("A", "akte.md"))
        self.assertFalse(allowed_change("M", "akte.md"))

    def test_unrelated_paths_are_rejected(self):
        self.assertEqual(
            violations([("A", "README.md"), ("M", "docs/guide.md")]),
            [("A", "README.md"), ("M", "docs/guide.md")],
        )


if __name__ == "__main__":
    unittest.main()
