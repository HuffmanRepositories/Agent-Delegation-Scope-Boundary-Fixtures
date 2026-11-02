import importlib.util
import json
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


    def test_fixture_grants_and_scopes_are_scenario_specific_and_explicit(self):
        for path in sorted((ROOT / "fixtures").glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            for member in data["delegation_chain"]:
                self.assertIsInstance(member.get("principal"), str)
                self.assertTrue(member["principal"])
                self.assertIsInstance(member.get("grant"), list)
                self.assertTrue(member["grant"])
                if member.get("scope_missing") is True:
                    self.assertIsNone(member.get("scope"))
                else:
                    self.assertIsInstance(member.get("scope"), str)
                    self.assertTrue(member["scope"])
            request = data["request"]
            self.assertTrue(request.get("actor"))
            self.assertTrue(request.get("action"))
            self.assertTrue(request.get("resource"))

    def test_expected_decision_domain_is_limited(self):
        self.assertEqual(validator.DECISIONS, {"allow", "deny", "indeterminate"})

if __name__ == "__main__":
    unittest.main()
