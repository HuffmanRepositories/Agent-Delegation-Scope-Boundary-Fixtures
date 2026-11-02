# Fixture format

Each fixture is a JSON object with these fields:

| Field | Meaning |
|---|---|
| `id` | Stable identifier, e.g. `DSB-001` |
| `title` | Short scenario title |
| `category` | Boundary category |
| `status` | `draft` or `reviewed` |
| `description` | Synthetic scenario |
| `policy_assumptions` | Rules needed to interpret the case |
| `delegation_chain` | Parent/child/sibling identity and grant snapshots, with explicit actions and resource scope |
| `request` | Action, resource, and contextual request |
| `expected` | Expected decision and rationale |
| `review_notes` | Questions or implementation-specific caveats |

## Interpretation

- `allow` means the request is within the stated synthetic policy assumptions.
- `deny` means it violates at least one stated boundary.
- `indeterminate` means the information is insufficient and the implementation should not silently assume authorization.
- Fixture assertions are conceptual. They do not prescribe a universal policy language or token format.

## Grant and scope representation

- Each chain member should identify a principal and a non-empty list of abstract grants (e.g. `read:project-x/*`). These are fixture vocabulary, not a real token or policy syntax.
- `scope` should be explicit and scenario-specific. Do not copy a generic `resource-A` grant into unrelated tenant, approval, project, or dataset scenarios.
- `delegated_from` identifies the delegator. Sibling branches may share a parent; the list is not necessarily a single linear path.
- A fixture with an intentionally missing scope must use `scope_missing: true` and `scope: null` so omission is not confused with accidental underspecification.
- The chain represents the authority presented/attempted in the scenario. `expected.decision` expresses the policy outcome that should be reviewed; an overbroad child grant can therefore be represented while the expected decision remains deny.
- Include lifecycle state, approval binding, audit ancestry, tenant, and application-vs-user identity details in the relevant fixture context when they affect the expected decision.
