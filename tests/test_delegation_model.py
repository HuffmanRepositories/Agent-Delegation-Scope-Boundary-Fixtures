import unittest
from datetime import datetime, timedelta, timezone

from delegation_model import DelegationDenied, Grant, authorize, issue_child


class DelegationModelTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2030, 1, 1, tzinfo=timezone.utc)
        self.expiry = self.now + timedelta(hours=2)
        self.parent = Grant("g-parent", "tenant-1", "user", "agent-A",
                            frozenset({"read", "write"}),
                            frozenset({"doc:1", "doc:2"}), self.expiry)

    def child(self, **overrides):
        args = dict(grant_id="g-child", issuer="agent-A", subject="agent-B",
                    tenant_id="tenant-1", actions={"read"}, resources={"doc:1"},
                    expires_at=self.now + timedelta(hours=1), now=self.now)
        args.update(overrides)
        return issue_child(self.parent, **args)

    def test_child_scope_is_attenuated_and_authorized(self):
        g = self.child()
        self.assertTrue(authorize(g, actor="agent-B", tenant_id="tenant-1",
                                  action="read", resource="doc:1", now=self.now))
        self.assertFalse(authorize(g, actor="agent-B", tenant_id="tenant-1",
                                   action="write", resource="doc:1", now=self.now))
        self.assertFalse(authorize(g, actor="agent-B", tenant_id="tenant-1",
                                   action="read", resource="doc:2", now=self.now))

    def test_child_cannot_expand_actions_or_resources(self):
        with self.assertRaises(DelegationDenied):
            self.child(actions={"read", "admin"})
        with self.assertRaises(DelegationDenied):
            self.child(resources={"doc:1", "doc:3"})

    def test_tenant_and_issuer_mismatch_denied(self):
        with self.assertRaises(DelegationDenied):
            self.child(tenant_id="tenant-2")
        with self.assertRaises(DelegationDenied):
            self.child(issuer="agent-attacker")

    def test_child_expiry_cannot_outlive_parent(self):
        with self.assertRaises(DelegationDenied):
            self.child(expires_at=self.expiry + timedelta(seconds=1))

    def test_parent_revocation_invalidates_child(self):
        child = self.child()
        self.parent.revoked = True
        self.assertFalse(authorize(child, actor="agent-B", tenant_id="tenant-1",
                                   action="read", resource="doc:1", now=self.now))

    def test_expired_ancestor_fails_closed(self):
        child = self.child()
        later = self.expiry + timedelta(seconds=1)
        self.assertFalse(authorize(child, actor="agent-B", tenant_id="tenant-1",
                                   action="read", resource="doc:1", now=later))

    def test_wrong_actor_cannot_use_child_grant(self):
        child = self.child()
        self.assertFalse(authorize(child, actor="agent-C", tenant_id="tenant-1",
                                   action="read", resource="doc:1", now=self.now))


if __name__ == "__main__":
    unittest.main()
