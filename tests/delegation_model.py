"""Synthetic delegated-scope policy model for adversarial fixture tests.

Not an authentication protocol, token issuer, policy engine, or production runtime.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, FrozenSet


class DelegationDenied(Exception):
    pass


@dataclass
class Grant:
    grant_id: str
    tenant_id: str
    issuer: str
    subject: str
    actions: FrozenSet[str]
    resources: FrozenSet[str]
    expires_at: datetime
    parent: Optional["Grant"] = None
    revoked: bool = False


def _active_chain(grant: Grant, now: datetime) -> bool:
    current = grant
    seen = set()
    while current is not None:
        if current.grant_id in seen or current.revoked or now >= current.expires_at:
            return False
        seen.add(current.grant_id)
        current = current.parent
    return True


def issue_child(parent: Grant, *, grant_id: str, issuer: str, subject: str,
                tenant_id: str, actions: set[str], resources: set[str],
                expires_at: datetime, now: datetime) -> Grant:
    if not _active_chain(parent, now):
        raise DelegationDenied("parent grant is revoked, expired, or cyclic")
    if issuer != parent.subject:
        raise DelegationDenied("delegator is not the parent grant subject")
    if tenant_id != parent.tenant_id:
        raise DelegationDenied("tenant boundary mismatch")
    if not actions or not actions.issubset(parent.actions):
        raise DelegationDenied("child actions exceed parent scope")
    if not resources or not resources.issubset(parent.resources):
        raise DelegationDenied("child resources exceed parent scope")
    if expires_at > parent.expires_at or expires_at <= now:
        raise DelegationDenied("child grant expiry exceeds parent or is already expired")
    return Grant(grant_id, tenant_id, issuer, subject, frozenset(actions),
                 frozenset(resources), expires_at, parent)


def authorize(grant: Grant, *, actor: str, tenant_id: str, action: str,
              resource: str, now: datetime) -> bool:
    if not _active_chain(grant, now):
        return False
    if actor != grant.subject or tenant_id != grant.tenant_id:
        return False
    return action in grant.actions and resource in grant.resources
