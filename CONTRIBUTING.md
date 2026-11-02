# Contributing

Thanks for contributing. This project is a review fixture corpus, not a production authorization system.

## Requirements

- Use synthetic identities, tenants, resources, policies, and actions only.
- Describe expected behavior as a review assertion, not a claim about a particular product.
- State assumptions and policy semantics explicitly.
- Keep fixtures minimal, deterministic, and offline.
- Include both positive and negative controls when useful.
- Do not claim certification, complete coverage, or guaranteed security.

## Workflow

1. Copy `docs/fixture-template.json`.
2. Add a unique fixture ID and concise scenario.
3. Describe the policy context and delegation chain.
4. Record the expected boundary outcome and rationale.
5. Add the fixture to `docs/fixture-status.md`.
6. Run `python scripts/validate_fixtures.py` and `python -m unittest discover -s tests -v`.

## Review

Reviewers should check the threat model, expected decision, and whether the fixture accidentally assumes a universal policy semantics. Structural CI is not semantic security review.
