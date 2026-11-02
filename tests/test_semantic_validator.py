import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("semantic_validator", ROOT / "scripts" / "validate_semantics.py")
semantic = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(semantic)


class SemanticValidatorTests(unittest.TestCase):
    def test_all_draft_fixtures_match_the_simplified_policy_model(self):
        errors, count = semantic.validate()
        self.assertEqual(errors, [])
        self.assertEqual(count, 12)

    def test_child_permission_is_attenuated_by_parent(self):
        fixture = {
            "delegation_chain": [
                {"principal": "parent", "grant": ["read:resource-1"], "scope": "resource-1"},
                {"principal": "child", "delegated_from": "parent",
                 "grant": ["read:resource-1", "write:resource-1"], "scope": "resource-1"}
            ],
            "request": {"actor": "child", "action": "write", "resource": "resource-1", "context": {}}
        }
        self.assertEqual(semantic.evaluate(fixture), "deny")

    def test_scope_wildcard_is_supported(self):
        fixture = {
            "delegation_chain": [
                {"principal": "parent", "grant": ["read:tenant-a/*"], "scope": "tenant-a"},
                {"principal": "child", "delegated_from": "parent",
                 "grant": ["read:tenant-a/*"], "scope": "tenant-a"}
            ],
            "request": {"actor": "child", "action": "read", "resource": "tenant-a/file", "context": {}}
        }
        self.assertEqual(semantic.evaluate(fixture), "allow")

    def test_missing_scope_fails_closed_as_indeterminate(self):
        fixture = {
            "delegation_chain": [
                {"principal": "parent", "grant": ["read:r"], "scope": "r"},
                {"principal": "child", "delegated_from": "parent",
                 "grant": ["read:r"], "scope": None, "scope_missing": True}
            ],
            "request": {"actor": "child", "action": "read", "resource": "r", "context": {}}
        }
        self.assertEqual(semantic.evaluate(fixture), "indeterminate")

    def test_approval_cannot_be_reused_for_another_action(self):
        fixture = {
            "delegation_chain": [
                {"principal": "parent", "grant": ["delete:r"], "scope": "r"}
            ],
            "request": {"actor": "parent", "action": "delete", "resource": "r",
                        "context": {"approval_id": "ap1", "approved_action": "read",
                                    "approved_resource": "r"}}
        }
        self.assertEqual(semantic.evaluate(fixture), "deny")


if __name__ == "__main__":
    unittest.main()
