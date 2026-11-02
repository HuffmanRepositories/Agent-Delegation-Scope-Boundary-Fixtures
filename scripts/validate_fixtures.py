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
    paths = sorted(FIXTURES.glob("*.json"))
    if not paths:
        errors.append("No fixture JSON files found.")
    for path in paths:
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: invalid JSON: {exc}")
            continue
        if not isinstance(obj, dict):
            errors.append(f"{path.name}: top-level JSON must be an object")
            continue
        missing = REQUIRED - obj.keys()
        if missing:
            errors.append(f"{path.name}: missing keys: {sorted(missing)}")
        fid = obj.get("id")
        if not isinstance(fid, str) or not fid.strip():
            errors.append(f"{path.name}: id must be a non-empty string")
        elif fid in seen:
            errors.append(f"{path.name}: duplicate id {fid}")
        else:
            seen.add(fid)
        status = obj.get("status")
        if not isinstance(status, str) or status not in {"draft", "reviewed"}:
            errors.append(f"{path.name}: status must be draft or reviewed")
        chain = obj.get("delegation_chain")
        if not isinstance(chain, list) or not chain:
            errors.append(f"{path.name}: delegation_chain must be a non-empty list")
        else:
            principals = set()
            for index, member in enumerate(chain):
                if not isinstance(member, dict):
                    errors.append(f"{path.name}: delegation_chain[{index}] must be an object")
                    continue
                principal = member.get("principal")
                if not isinstance(principal, str) or not principal.strip():
                    errors.append(f"{path.name}: delegation_chain[{index}].principal must be non-empty")
                else:
                    principals.add(principal)
                grant = member.get("grant")
                if not isinstance(grant, list) or not grant or any(not isinstance(item, str) or not item.strip() for item in grant):
                    errors.append(f"{path.name}: delegation_chain[{index}].grant must be a non-empty list of strings")
                if member.get("scope_missing") is True:
                    if member.get("scope") is not None:
                        errors.append(f"{path.name}: explicit missing scope must use scope: null")
                elif not isinstance(member.get("scope"), str) or not member["scope"].strip():
                    errors.append(f"{path.name}: delegation_chain[{index}].scope must be non-empty unless scope_missing is true")
            for index, member in enumerate(chain):
                if isinstance(member, dict) and member.get("delegated_from") and member["delegated_from"] not in principals:
                    errors.append(f"{path.name}: delegation_chain[{index}].delegated_from must name a principal in the fixture")
        if not isinstance(obj.get("policy_assumptions"), list) or not obj.get("policy_assumptions"):
            errors.append(f"{path.name}: policy_assumptions must be a non-empty list")
        request = obj.get("request")
        if not isinstance(request, dict):
            errors.append(f"{path.name}: request must be an object")
        else:
            for key in ("actor", "action", "resource"):
                if not isinstance(request.get(key), str) or not request[key].strip():
                    errors.append(f"{path.name}: request.{key} must be a non-empty string")
        expected = obj.get("expected")
        if not isinstance(expected, dict) or expected.get("decision") not in DECISIONS:
            errors.append(f"{path.name}: expected.decision must be allow, deny, or indeterminate")
        if not isinstance(obj.get("review_notes"), list):
            errors.append(f"{path.name}: review_notes must be a list")
    return errors, len(seen)

if __name__ == "__main__":
    errors, count = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    print(f"Validated {count} delegation boundary fixture(s) (structure only).")
