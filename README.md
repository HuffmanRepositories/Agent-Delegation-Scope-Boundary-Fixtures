# Agent Delegation Scope Boundary Fixtures

A small, implementation-neutral corpus of **synthetic draft fixtures** for reviewing authority boundaries when AI agents delegate work to subagents and tools.

The corpus focuses on whether delegated authority stays within the parent's permitted scope across nested delegation, identity changes, tenant boundaries, approvals, expiry/revocation, and audit records.

## Status

- Synthetic, offline fixtures; draft and illustrative.
- Structural validation only. No live authorization checks or runtime integrations.
- Not an authorization protocol, token format, SDK, policy engine, runtime, benchmark, or certification suite.
- Passing the validator does **not** establish security, correctness, or conformance.

## Contents

- `fixtures/`: test cases and expected review outcomes
- `docs/fixture-format.md`: fixture structure and interpretation
- `docs/scope-boundary-taxonomy.md`: threat and boundary categories
- `docs/fixture-status.md`: inventory and review status
- `docs/review-checklist.md`: human review guidance
- `scripts/validate_fixtures.py`: offline structural validator
- `tests/`: validator tests

## Core review principle

Delegation should not silently expand authority. A child agent's effective permissions should remain constrained by the applicable parent authority, explicit delegation grant, target/resource boundaries, and any time or approval constraints. The exact enforcement model is implementation-specific and must be reviewed against its own policy semantics.

## Run

```bash
python -m unittest discover -s tests -v
python scripts/validate_fixtures.py
python scripts/validate_semantics.py
```

## References

- [Microsoft Agent Governance Toolkit — delegation chains](https://microsoft.github.io/agent-governance-toolkit/tutorials/23-delegation-chains/)
- [Attenu](https://attenu.io/)
- [Agent Delegation Control Standard (ADCS)](https://github.com/kahalewai/adcs)
- [Microsoft — least privilege for AI agents](https://learn.microsoft.com/en-us/security/zero-trust/sfi/least-privilege-for-ai-agents)
- [NIST NCCoE — Agent Identity and Authorization Concept Paper](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf)

These references are background material, not endorsements or proof that this corpus is complete.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please do not submit real credentials, user data, production policy, or exploit payloads.
