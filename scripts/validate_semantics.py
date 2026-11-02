#!/usr/bin/env python3
"""Scenario-level semantic consistency checks for synthetic DSB fixtures.

This is a deliberately small, documented policy model for the fixture format.
It is not an authorization engine or implementation conformance test.
"""
from __future__ import annotations

import fnmatch
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
DECISIONS = {"allow", "deny", "indeterminate"}


def _permission(value: Any) -> tuple[str, str | None] | None:
    if not isinstance(value, str) or not value.strip():
        return None
    action, sep, resource = value.partition(":")
    return (action, resource if sep and resource else None)


def _matches(pattern: str, value: str) -> bool:
    return fnmatch.fnmatchcase(value, pattern)


def _scope_matches(scope: str, resource: str) -> bool:
    return _matches(scope, resource) or _matches(scope.rstrip("/") + "/*", resource)


def _grant_allows(grants: Any, action: str, resource: str) -> bool:
    if not isinstance(grants, list):
        return False
    for item in grants:
        parsed = _permission(item)
        if parsed is None:
            continue
        grant_action, grant_resource = parsed
        if grant_action in {action, "*"} and grant_resource is not None:
            if _matches(grant_resource, resource):
                return True
    return False


def _actor_path(chain: list[dict[str, Any]], actor: str) -> list[dict[str, Any]] | None:
    by_principal = {member.get("principal"): member for member in chain
                    if isinstance(member, dict) and isinstance(member.get("principal"), str)}
    if actor not in by_principal:
        return None
    path = []
    current = by_principal[actor]
    seen = set()
    while current:
        principal = current.get("principal")
        if principal in seen:
            return None
        seen.add(principal)
        path.append(current)
        parent = current.get("delegated_from")
        if not parent:
            break
        current = by_principal.get(parent)
        if current is None:
            return None
    path.reverse()
    return path


def evaluate(data: dict[str, Any]) -> str:
    """Return allow/deny/indeterminate under this fixture's simplified model."""
    request = data.get("request", {})
    chain = data.get("delegation_chain", [])
    actor = request.get("actor")
    action = request.get("action")
    resource = request.get("resource")
    context = request.get("context", {})
    if not isinstance(actor, str) or not isinstance(action, str) or not isinstance(resource, str):
        return "indeterminate"
    if not isinstance(chain, list) or not isinstance(context, dict):
        return "indeterminate"

    path = _actor_path(chain, actor)
    if not path:
        return "indeterminate"

    for member in path:
        if member.get("scope_missing") is True or member.get("scope") is None:
            return "indeterminate"
        if member.get("grant_state") in {"revoked", "expired"}:
            return "deny"
        scope = member.get("scope")
        if not isinstance(scope, str) or not _scope_matches(scope, resource):
            return "deny"
        if not _grant_allows(member.get("grant"), action, resource):
            return "deny"

    approval = context.get("approval_id")
    if approval and (context.get("approved_action") != action
                     or context.get("approved_resource") != resource):
        return "deny"

    audit = context.get("audit_record")
    if isinstance(audit, dict) and (
        audit.get("missing_parent_chain") is True
        or not audit.get("delegation_ancestry")
    ):
        return "indeterminate"

    return "allow"


def validate_file(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path.name}: cannot parse fixture: {exc}"]
    if not isinstance(data, dict):
        return [f"{path.name}: root must be object"]
    expected = data.get("expected")
    if not isinstance(expected, dict) or expected.get("decision") not in DECISIONS:
        return [f"{path.name}: expected.decision must be one of {sorted(DECISIONS)}"]
    actual = evaluate(data)
    if actual != expected["decision"]:
        return [f"{path.name}: semantic model predicted {actual!r}, fixture expects {expected['decision']!r}"]
    return []


def validate() -> tuple[list[str], int]:
    paths = sorted(FIXTURES.glob("*.json"))
    errors = []
    if not paths:
        errors.append("No fixture JSON files found")
    for path in paths:
        errors.extend(validate_file(path))
    return errors, len(paths)


def main() -> int:
    errors, count = validate()
    if errors:
        print("Semantic consistency check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Semantic consistency model matched expected decisions for {count} draft fixtures.")
    print("This is a simplified fixture model—not runtime authorization or conformance evidence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
