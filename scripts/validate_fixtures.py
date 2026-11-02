#!/usr/bin/env python3
"""Offline structural validation for synthetic delegation boundary fixtures."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
REQUIRED = {"id", "title", "category", "status", "description", "policy_assumptions",
            "delegation_chain", "request", "expected", "review_notes"}
DECISIONS = {"allow", "deny", "indeterminate"}

def validate():
    errors = []
    seen = set()
    for path in sorted(FIXTURES.glob("*.json")):
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.name}: invalid JSON: {exc}")
            continue
        missing = REQUIRED - obj.keys()
        if missing:
            errors.append(f"{path.name}: missing keys: {sorted(missing)}")
        fid = obj.get("id")
        if not isinstance(fid, str) or not fid:
            errors.append(f"{path.name}: id must be a non-empty string")
        elif fid in seen:
            errors.append(f"{path.name}: duplicate id {fid}")
        else:
            seen.add(fid)
        if obj.get("status") not in {"draft", "reviewed"}:
            errors.append(f"{path.name}: status must be draft or reviewed")
        if not isinstance(obj.get("delegation_chain"), list) or not obj.get("delegation_chain"):
            errors.append(f"{path.name}: delegation_chain must be a non-empty list")
        if not isinstance(obj.get("policy_assumptions"), list) or not obj.get("policy_assumptions"):
            errors.append(f"{path.name}: policy_assumptions must be a non-empty list")
        if not isinstance(obj.get("request"), dict):
            errors.append(f"{path.name}: request must be an object")
        expected = obj.get("expected")
        if not isinstance(expected, dict) or expected.get("decision") not in DECISIONS:
            errors.append(f"{path.name}: expected.decision must be allow, deny, or indeterminate")
        if not isinstance(obj.get("review_notes"), list):
            errors.append(f"{path.name}: review_notes must be a list")
    if not seen:
        errors.append("No fixture JSON files found.")
    return errors, len(seen)

if __name__ == "__main__":
    errors, count = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    print(f"Validated {count} delegation boundary fixture(s) (structure only).")
