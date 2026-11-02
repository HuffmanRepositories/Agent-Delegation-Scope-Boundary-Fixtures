# Fixture status

All entries below are **synthetic draft fixtures**. They have not been semantically reviewed against any specific implementation.

| ID | Scenario | Category | Status |
|---|---|---|---|
| DSB-001 | Child grant exceeds parent scope | authority-attenuation | draft |
| DSB-002 | Read-only restriction dropped at handoff | action-restriction | draft |
| DSB-003 | User delegation confused with app identity | principal-identity | draft |
| DSB-004 | Tenant/workspace boundary lost | resource-isolation | draft |
| DSB-005 | Sibling permissions implicitly unioned | sibling-isolation | draft |
| DSB-006 | Revoked or expired grant accepted | delegation-lifecycle | draft |
| DSB-007 | Nested delegation preserves restrictions | nested-delegation | draft |
| DSB-008 | Downstream authorization check bypassed | enforcement-point | draft |
| DSB-009 | Approval reused for different operation | approval-binding | draft |
| DSB-010 | Audit record loses delegation ancestry | audit-continuity | draft |
| DSB-011 | Missing scope treated as unrestricted | fail-closed-uncertainty | draft |
| DSB-012 | Child delegates beyond its own grant | nested-delegation | draft |

CI validates structure only; semantic review remains outstanding.
