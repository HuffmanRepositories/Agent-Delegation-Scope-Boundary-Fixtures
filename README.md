# Agent Delegation Scope Boundary Fixtures

[Start here](START-HERE.md) · [Whitepaper](WHITEPAPER.md) · [AI agent guidance](AGENTS.md)


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

## Experimental policy-model tests

A [simplified synthetic delegation model](docs/synthetic-delegation-model.md) tests action/resource attenuation, tenant and issuer boundaries, expiry and parent revocation. This is a model test—not an identity system, production policy engine, or security conformance proof.

## Companion projects (when a scenario crosses boundaries)

- [P12 — Tool Retry & Idempotency Fixtures](https://github.com/HuffmanRepositories/Agent-Tool-Retry-Idempotency-Fixtures) for tool effects, ambiguous outcomes, and retry/reconciliation behavior.
- [P14 — Delegated Budget Enforcement Fixtures](https://github.com/HuffmanRepositories/Agent-Delegated-Budget-Enforcement-Fixtures) for child budget allocations and settlement constraints.
- [P15 — User-Controlled Stop Reference Model](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root/tree/main/p15) for stop propagation and containment semantics.

These are related synthetic fixture sets, not runtime dependencies. Use only the companion cases relevant to the authority scenario.

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

## Ecosystem directory

This project is part of the [HuffmanRepositories public ecosystem](https://github.com/HuffmanRepositories/Huffman-Ecosystem-Root). Use the directory for project routing, human and AI onboarding, shared terminology, governance, and related workstreams. This repository's own README and specifications remain authoritative for its scope, maturity, and validation status.
