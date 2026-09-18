# ADR 0005: Repository Model

## Status
Accepted

## Decision
Use two Git repositories.

1. Application repository
2. GitOps environment repository

## Responsibility

Application repository:
- Source code
- Docker build
- CI workflows
- Tests
- Security scanning
- Artifact publication

GitOps repository:
- Kubernetes desired state
- Kustomize configuration
- Development environment
- Staging environment
- Deployment image revisions

## Reason
Application source and deployment state have different responsibilities and lifecycles.
