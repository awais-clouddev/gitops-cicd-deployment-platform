# ADR 0004: Deployment Configuration

## Status
Accepted

## Decision
Use Kustomize for Kubernetes deployment configuration.

## Reasons
- Declarative Kubernetes-native configuration.
- Supports reusable bases and environment overlays.
- Appropriate for development and staging environments.
- Keeps Project 5 focused.

## Rejected
- Helm: useful, but additional packaging complexity is better reserved for Project 6.
