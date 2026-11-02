# Synthetic Delegation Scope Harness

This test-only model makes a narrow assumption explicit: a delegated grant must be a subset of the parent grant in tenant, actions, resource identifiers and expiry. Revocation or expiry of an ancestor invalidates descendants. A subject must match the grant recipient to exercise it.

Run the harness and existing validators:

```bash
python -m unittest discover -s tests -v
python scripts/validate_fixtures.py
python scripts/validate_semantics.py
```

## Model test cases
- child action/resource attenuation
- attempted action/resource expansion
- tenant and delegator identity mismatch
- expiry beyond parent grant
- ancestor revocation propagation
- expired ancestor fail-closed behavior
- wrong principal cannot exercise child grant

## Limitations
This is a simplified exact-resource test model. It does not define wildcard, hierarchical resource, deny-rule, policy-combination, delegation-token, cryptographic, identity-provider, cache, network, multi-process, or production semantics. Real systems must define these explicitly and test their own policy engine and credential boundaries. This is not an authorization standard or certification.
