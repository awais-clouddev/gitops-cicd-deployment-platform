# ADR 0003: Container Registry

## Status
Accepted

## Decision
Use GitHub Container Registry (GHCR).

## Reasons
- Integrates directly with GitHub Actions.
- Keeps Project 5 focused on CI/CD and GitOps.
- Supports OCI container images and immutable digests.
- Avoids unnecessary AWS infrastructure and authentication.

## Rejected
- Amazon ECR: already demonstrated in previous AWS projects and adds no major new learning objective here.
