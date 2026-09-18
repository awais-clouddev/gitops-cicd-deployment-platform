# ADR 0006: Kubernetes Runtime

## Status
Accepted

## Decision
Use kind as the Kubernetes runtime for Project 5.

## Reasons
- Provides a real Kubernetes API and controller environment.
- Supports Argo CD and GitOps reconciliation.
- Disposable and reproducible.
- No continuous cloud infrastructure cost.
- Keeps advanced Kubernetes infrastructure for Project 6.

## Limitation
This is a local portfolio/lab Kubernetes environment and is not presented as a production highly available cluster.

## Rejected
- Amazon EKS: unnecessary cost and Kubernetes infrastructure complexity for the Project 5 objective.
