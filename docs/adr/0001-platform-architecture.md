# ADR 0001: Platform Architecture

## Status
Accepted

## Decision

Project 5 will use:

- GitHub Actions for CI
- GitHub Container Registry (GHCR) for container images
- A separate GitOps repository for deployment state
- Argo CD for GitOps continuous delivery
- Kustomize for Kubernetes configuration
- Kubernetes as the runtime platform
- kind for the local Kubernetes lab environment

## Delivery Model

Application Repository
→ GitHub Actions
→ Test / Validate / Scan
→ Build Container Image
→ Push Immutable Image to GHCR
→ Update GitOps Repository
→ Argo CD Detects Change
→ Argo CD Reconciles Kubernetes
→ Application Deployment

## Core Principle

CI will not deploy directly to Kubernetes.

Git will represent the desired deployment state, and Argo CD will reconcile that state into Kubernetes.

## Scope

Project 5 focuses on:

- CI/CD
- GitOps
- Software supply chain
- Immutable artifacts
- Environment promotion
- Drift detection
- Self-healing
- Rollback
- Release traceability

Advanced Kubernetes and platform-engineering topics remain primarily in Project 6.