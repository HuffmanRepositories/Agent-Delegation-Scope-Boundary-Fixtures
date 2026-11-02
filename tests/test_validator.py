import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("fixture_validator", ROOT / "scripts" / "validate_fixtures.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class ValidatorTests(unittest.TestCase):
    def test_repo_fixtures_are_structurally_valid(self):
        errors, count = validator.validate()
        self.assertEqual(errors, [])
        self.assertGreaterEqual(count, 1)

    def test_expected_decision_domain_is_limited(self):
        self.assertEqual(validator.DECISIONS, {"allow", "deny", "indeterminate"})

if __name__ == "__main__":
    unittest.main()
