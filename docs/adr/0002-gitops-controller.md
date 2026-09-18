# ADR 0002: GitOps Controller

## Status
Accepted

## Decision
Use Argo CD as the GitOps continuous delivery controller.

## Reasons
- Git remains the source of truth.
- Argo CD continuously reconciles Kubernetes with Git.
- Supports automatic sync, pruning, self-healing, health status, and deployment history.
- Provides strong visual and CLI evidence for portfolio validation.

## Rejected
- GitHub Actions running kubectl apply: not true GitOps.
- Flux: capable, but using two GitOps controllers adds unnecessary complexity.
