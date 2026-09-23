# Platform Architecture Overview

## Purpose

This project implements a GitOps-driven CI/CD platform where GitHub Actions builds and validates application artifacts, while Argo CD is solely responsible for reconciling deployment state into Kubernetes.

The design intentionally separates Continuous Integration from Continuous Delivery.

## Repository Model

Two repositories are used.

### Application Repository

`awais-clouddev/gitops-cicd-deployment-platform`

Responsibilities:

- application source code
- Dockerfiles
- CI workflows
- vulnerability scanning
- SBOM generation
- build provenance
- GHCR publication
- immutable artifact digest resolution
- automated GitOps deployment pull requests
- platform documentation

### GitOps Repository

`awais-clouddev/gitops-environments`

Responsibilities:

- Kubernetes desired state
- Kustomize base configuration
- development overlay
- staging overlay
- immutable image digests
- environment promotion
- Argo CD Application configuration
- Git-native deployment history

## Major Components

### GitHub Actions

GitHub Actions performs Continuous Integration.

It validates source code, builds container images, performs Trivy security scans, generates CycloneDX SBOMs, creates provenance attestations, publishes images to GHCR, resolves immutable digests, and proposes GitOps deployment changes.

GitHub Actions does not directly deploy application workloads to Kubernetes.

### GitHub Container Registry

GHCR stores the API and frontend container artifacts.

Images receive source-SHA-based tags and deployment state uses immutable SHA256 digests.

### GitOps Repository

The GitOps repository is the authoritative desired deployment state.

Environment changes are represented as Git changes rather than direct cluster mutations.

### Argo CD

Argo CD continuously watches the GitOps repository and reconciles Kubernetes against Git.

The development Application uses:

- automatic synchronization
- pruning
- self-healing
- Git-based desired state

### Kustomize

Kustomize manages reusable Kubernetes configuration.

The base contains shared workload definitions.

Environment overlays contain environment-specific settings such as replica counts and immutable image digests.

### Kubernetes

The runtime environment is a three-node local kind cluster running Kubernetes v1.37.0.

The workload contains:

- Nginx gateway
- frontend
- FastAPI API
- PostgreSQL
- Redis

## CI Flow

```text
Source commit
    ↓
GitHub Actions
    ↓
Validation
    ↓
Container build
    ↓
Trivy vulnerability gates
    ↓
CycloneDX SBOM
    ↓
GHCR publication
    ↓
Digest resolution
    ↓
Build provenance
```

## GitOps Deployment Flow

```text
Published immutable digests
    ↓
Automated GitOps deployment PR
    ↓
Review / merge
    ↓
GitOps main branch
    ↓
Argo CD detects desired-state change
    ↓
Argo CD reconciles Kubernetes
    ↓
Application becomes Synced / Healthy
```

## Immutable Artifact Model

Application images are built once.

The resulting immutable digest is recorded in GitOps desired state.

The same artifact can then be promoted between environments without rebuilding.

This prevents development and staging from accidentally running different binaries under the same release identity.

## Environment Model

### Development

Development receives automated deployment proposals from the CI pipeline.

Argo CD automatically reconciles merged desired-state changes.

### Staging

Staging receives artifacts through promotion of existing immutable digests.

Promotion does not rebuild the application images.

## Release Traceability

Each release can be traced across:

```text
Source SHA
    ↓
GitHub Actions run
    ↓
GHCR image digest
    ↓
GitOps commit / pull request
    ↓
Argo CD reconciliation
    ↓
Running Kubernetes workload
```

The Kubernetes resources also carry the source release SHA as an annotation.

## Drift Management

Git is treated as the source of truth.

If a live Kubernetes resource is manually changed, Argo CD detects the difference.

With self-healing enabled, Argo CD restores the live resource to match Git.

If a managed resource is deleted, Argo CD recreates it.

## Failure Handling

A controlled bad-release test proved that an invalid image digest results in a failed Kubernetes rollout.

The previous healthy replica remained available while the new replica entered `ImagePullBackOff`.

The failure was visible through Kubernetes and Argo CD health state.

## Rollback Model

Rollback is Git-native.

A bad desired-state commit is reverted in Git.

Argo CD then reconciles Kubernetes back to the previously known-good immutable artifact.

No direct `kubectl rollout undo` is required.

## Security Boundaries

The platform applies the following controls:

- application secrets are not stored in Git
- Kubernetes workloads reference runtime Secrets using `secretKeyRef`
- GitHub credentials are stored as GitHub repository secrets
- no credentials are embedded in Git remote URLs
- repositories were scanned for committed secrets
- application containers run as non-root users
- container vulnerability gates check HIGH and CRITICAL findings
- GitHub Actions are pinned to immutable commit SHAs
- application deployment uses immutable image digests
- Argo CD anonymous access is disabled
- Argo CD exec functionality is disabled
- Argo CD server remains ClusterIP-only in the local lab
- CI contains no direct Kubernetes deployment commands

## Local Lab Boundary

The Kubernetes runtime is intentionally implemented with kind under WSL2.

This demonstrates the GitOps control plane and deployment lifecycle without requiring paid cloud Kubernetes infrastructure.

It is a portfolio lab architecture, not a claim of production high availability.

## Deliberate Project Exclusions

The project intentionally does not introduce:

- Amazon EKS
- ECS
- Terraform
- Helm
- Flux
- Jenkins
- Argo Rollouts
- Prometheus
- Grafana
- Istio
- Vault

Those technologies are outside this project's focused GitOps CI/CD scope or reserved for the later Kubernetes/platform engineering project.

## Architectural Principle

The central design principle is:

**CI produces trusted immutable artifacts. Git defines desired state. Argo CD performs deployment and reconciliation.**
