# ADR 0007: Immutable Artifact Strategy

## Status
Accepted

## Decision
Deploy immutable container versions based on source commit SHA and container image digest.

## Rules
- Do not use latest as the deployment source of truth.
- Every release must be traceable to a source revision.
- Environment promotion must reuse the same built artifact.
- Do not rebuild an artifact when promoting it between environments.

## Reason
Immutable artifacts improve reproducibility, traceability, rollback, and supply-chain integrity.
