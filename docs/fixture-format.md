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
| `delegation_chain` | Parent/child identity and grant snapshots |
| `request` | Action, resource, and contextual request |
| `expected` | Expected decision and rationale |
| `review_notes` | Questions or implementation-specific caveats |

## Interpretation

- `allow` means the request is within the stated synthetic policy assumptions.
- `deny` means it violates at least one stated boundary.
- `indeterminate` means the information is insufficient and the implementation should not silently assume authorization.
- Fixture assertions are conceptual. They do not prescribe a universal policy language or token format.
