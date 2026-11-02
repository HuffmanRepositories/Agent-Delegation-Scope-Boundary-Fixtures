# Agent Delegation Scope Boundaries: Constrained Authority

**Author:** Robert Huffman  
**Status:** Research whitepaper, version 0.1

## Abstract

P13 is a synthetic fixture corpus for reviewing authority boundaries when an agent delegates work to child agents or tools. The core design principle is that delegation should not silently expand the authority granted by the parent.

## Problem statement

Multi-agent systems can introduce new identities, nested tasks, resource access, and asynchronous work. Without explicit constraints, a child may receive broader permissions than intended, continue after expiry, act across tenant boundaries, or retain authority after revocation.

## Approach

P13 models parent authority, delegation grants, child requests, ancestry, resource scope, identity transitions, approval requirements, expiry, revocation, and audit records. Fixtures describe expected invariants while leaving the actual enforcement mechanism to each implementation.

## How to use P13

Read [START-HERE.md](START-HERE.md), [docs/scope-boundary-taxonomy.md](docs/scope-boundary-taxonomy.md), [docs/fixture-format.md](docs/fixture-format.md), and [docs/review-checklist.md](docs/review-checklist.md). Inspect [fixtures/](fixtures/). Run python scripts/validate_fixtures.py, python scripts/validate_semantics.py, and python -m unittest discover -s tests -v.

## Boundaries

P13 is not an authorization protocol, token format, policy engine, runtime, benchmark, or certification suite. Validators do not execute a real authorization system or prove security.

## Outlook

Delegation should be explicit, attenuated, time-bounded, auditable, and revocable. The fixture corpus provides a vocabulary for reviewing those properties without claiming one universal enforcement design.

— Robert Huffman