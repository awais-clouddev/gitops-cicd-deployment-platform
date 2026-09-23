# GitOps-Driven CI/CD Deployment Platform

> Senior-oriented Cloud/DevOps portfolio project demonstrating secure CI, immutable container delivery, GitOps continuous deployment, environment promotion, drift recovery, failure handling, Git-native rollback, and end-to-end release traceability.

## Overview

This project implements a complete GitOps-driven software delivery platform around a containerized help desk application.

The architecture deliberately separates **Continuous Integration** from **Continuous Delivery**:

- **GitHub Actions** validates, builds, scans, attests, and publishes artifacts.
- **GitHub Container Registry (GHCR)** stores immutable container artifacts.
- **Git** stores authoritative Kubernetes desired state.
- **Argo CD** detects desired-state changes and reconciles Kubernetes.
- **Kustomize** manages reusable base manifests and environment overlays.
- **kind** provides a three-node local Kubernetes runtime for the portfolio lab.

CI never directly deploys the application with `kubectl apply`. Deployment authority belongs to Argo CD.

---

## Architecture

```text
Developer / Source Commit
          |
          v
   GitHub Actions CI
          |
          +--> validation
          +--> container builds
          +--> Trivy security gates
          +--> CycloneDX SBOMs
          +--> build provenance
          |
          v
         GHCR
   immutable SHA256 digests
          |
          v
 Automated GitOps Pull Request
          |
          v
   gitops-environments repo
 authoritative desired state
          |
          v
       Argo CD
 reconcile / prune / self-heal
          |
          v
 Kubernetes kind Cluster
          |
          v
 Help Desk Application
 frontend + API + PostgreSQL + Redis + gateway
```

Detailed architecture: [Platform Architecture](docs/architecture/platform-architecture.md)

Architecture overview: [Architecture Overview](docs/architecture/architecture-overview.md)

---

## Core Engineering Highlights

- Separate CI and GitOps CD responsibilities
- Two-repository application / desired-state model
- Pull-request validation before merge
- Immutable source-SHA release identity
- GHCR publication with SHA256 digest resolution
- Trivy HIGH / CRITICAL vulnerability gates
- CycloneDX SBOM generation
- Build provenance attestations
- GitHub Actions pinned to immutable commit SHAs
- Least-privilege workflow permissions
- Kustomize base + development + staging overlays
- Argo CD automatic synchronization
- Argo CD pruning and self-healing
- Build-once / promote-the-same-artifact model
- Release SHA propagation into Kubernetes metadata
- Controlled drift experiment and recovery
- Deleted-resource recovery validation
- Controlled bad-release experiment
- Git-native rollback validation
- Runtime-only Kubernetes Secrets
- Repository secret scanning
- Reproducible local three-node Kubernetes environment

---

## Technology Stack

| Area | Technology | Responsibility |
| --- | --- | --- |
| CI | GitHub Actions | Validate, build, scan, publish and attest |
| Registry | GHCR | Store immutable API and frontend artifacts |
| CD | Argo CD | Reconcile Git desired state into Kubernetes |
| Runtime | Kubernetes / kind | Run the application platform |
| Config Management | Kustomize | Base and environment overlays |
| Containers | Docker | Build API and frontend runtime images |
| Security | Trivy | Vulnerability and secret scanning |
| SBOM | CycloneDX | Software component inventory |
| Supply Chain | GitHub Attestations | Build provenance |
| Source Control | Git / GitHub | Source, review and deployment history |
| Application | FastAPI + Nginx | API and frontend workload |
| Data | PostgreSQL + Redis | Persistent database and cache |

---

## Repository Model

### Application Repository

`awais-clouddev/gitops-cicd-deployment-platform`

Contains:

- application source code
- Dockerfiles
- GitHub Actions workflows
- container security controls
- GitOps automation scripts
- platform bootstrap configuration
- architecture documentation
- evidence and operational documentation

### GitOps Repository

[awais-clouddev/gitops-environments](https://github.com/awais-clouddev/gitops-environments)

Contains:

- Kubernetes desired state
- Kustomize base configuration
- development overlay
- staging overlay
- immutable image digests
- Argo CD Application definition
- promotion automation
- Git-native deployment history

---

## CI Pipeline

The release pipeline follows this control flow:

```text
Source commit
    |
    v
Repository validation
    |
    v
API + frontend builds
    |
    v
Trivy vulnerability gates
    |
    v
CycloneDX SBOM generation
    |
    v
GHCR publication
    |
    v
Immutable digest resolution
    |
    v
Build provenance attestations
    |
    v
GitOps deployment proposal
```

CI documentation: [CI Pipeline](docs/ci-pipeline.md)

---

## GitOps Continuous Delivery

The application pipeline does **not** perform direct Kubernetes deployment.

After CI publishes trusted artifacts:

1. The immutable API and frontend digests are resolved.
2. The automation updates the development GitOps overlay.
3. The source release SHA is recorded in desired state.
4. A dedicated deployment branch is created.
5. A GitOps pull request is opened.
6. The desired-state change is merged.
7. Argo CD detects the Git change.
8. Argo CD reconciles Kubernetes.
9. The application returns to `Synced / Healthy`.

GitOps documentation: [GitOps Deployment](docs/gitops-deployment.md)

---

## Immutable Artifact Strategy

Application releases do not depend on mutable `latest` tags.

CI creates a source-based release identity and GHCR resolves the exact artifact digest.

Deployment state ultimately references:

```text
ghcr.io/.../api@sha256:<immutable-digest>
ghcr.io/.../frontend@sha256:<immutable-digest>
```

This allows the exact container artifact to be traced, promoted and restored.

---

## Environment Promotion

Development and staging have independent GitOps overlays.

Promotion follows the rule:

**Build once. Validate once. Promote the same immutable artifact.**

```text
CI Build
   |
   v
Immutable GHCR Digest
   |
   v
Development
   |
   v
Validation
   |
   v
Promotion
   |
   v
Same Digest in Staging
```

No application image is rebuilt during promotion.

Promotion documentation: [Environment Promotion](docs/environment-promotion.md)

---

## Release Traceability

The platform establishes a trace across the delivery lifecycle:

```text
Source SHA
    |
    v
GitHub Actions Run
    |
    v
GHCR Image Tag
    |
    v
GHCR SHA256 Digest
    |
    v
GitOps Pull Request / Commit
    |
    v
Argo CD Reconciliation
    |
    v
Running Kubernetes Workload
```

The source release SHA is also propagated into Kubernetes resource annotations.

---

## Drift Detection and Self-Healing

A controlled drift test manually changed the live API replica count while Git remained unchanged.

Argo CD detected:

```text
Deployment / helpdesk-api => OutOfSync
```

After self-healing was enabled, Argo CD automatically restored the Git-defined replica count and returned the Application to:

```text
Synced / Healthy
```

---

## Deleted Resource Recovery

A Git-managed frontend Deployment was deliberately deleted from the live cluster.

Argo CD recreated the missing resource from Git desired state and restored the workload to Ready state.

This validates reconciliation beyond simple configuration drift.

---

## Controlled Bad Release

A deliberately invalid API image digest was committed through GitOps.

Kubernetes exposed the failure through:

```text
ErrImagePull
ImagePullBackOff
```

The previous healthy API replica remained available while the new rollout failed.

The failed release was visible through both Kubernetes and Argo CD.

---

## Git-Native Rollback

Rollback is performed by reverting the bad desired-state commit in Git.

```text
Bad GitOps Commit
       |
       v
    git revert
       |
       v
GitOps main branch
       |
       v
    Argo CD
       |
       v
Previous Known-Good Digest
```

The project does not use direct `kubectl rollout undo` as the normal rollback mechanism for Git-managed application state.

Drift and rollback documentation: [Drift, Self-Healing and Rollback](docs/drift-self-heal-rollback.md)

---

## Security and Supply Chain

The project applies multiple controls across source, CI, container build, registry and deployment boundaries:

- no application credentials committed to Git
- runtime Kubernetes Secrets referenced through `secretKeyRef`
- GitHub repository secrets for workflow credentials
- Git remotes without embedded credentials
- repository secret scanning
- non-root API and frontend containers
- pinned base-image digests
- HIGH and CRITICAL vulnerability gates
- CycloneDX SBOM generation
- build provenance attestations
- GitHub Actions pinned to immutable SHAs
- least-privilege workflow permissions
- immutable application deployment digests
- Argo CD anonymous access disabled
- Argo CD exec functionality disabled
- Argo CD server kept ClusterIP-only in the local lab
- CI prevented from acting as the Kubernetes deployment authority

Security documentation: [Security and Supply Chain](docs/security-supply-chain.md)

---

## Kubernetes Workload

The deployed help desk platform contains:

- Nginx gateway
- frontend
- FastAPI API
- PostgreSQL
- Redis

The Kubernetes configuration includes:

- resource requests and limits
- readiness probes
- liveness probes
- Services
- Deployments
- StatefulSet-based data services
- ConfigMaps
- runtime Secret references
- development and staging overlays

---

## Project Structure

```text
gitops-cicd-deployment-platform/
|
+-- .github/workflows/
|   +-- pr-validation.yml
|   +-- release.yml
|   +-- gitops-update.yml
|
+-- app/
|   +-- api/
|   +-- frontend/
|   +-- gateway/
|
+-- platform/
|   +-- kind/
|   +-- argocd/
|
+-- scripts/
|   +-- image-version.sh
|   +-- update-gitops-development.py
|
+-- docs/
|   +-- adr/
|   +-- architecture/
|   +-- evidence/
|   +-- ci-pipeline.md
|   +-- gitops-deployment.md
|   +-- environment-promotion.md
|   +-- security-supply-chain.md
|   +-- drift-self-heal-rollback.md
|   +-- troubleshooting.md
|   +-- setup-reproduction.md
|   +-- cleanup.md
|   +-- skills-demonstrated.md
|
+-- README.md
```

---

## Evidence

The repository contains evidence collected from the implemented platform rather than architecture claims alone.

- [CI Evidence](docs/evidence/ci-evidence.md)
- [Registry Evidence](docs/evidence/registry-evidence.md)
- [GitOps Evidence](docs/evidence/gitops-evidence.md)
- [Kubernetes Evidence](docs/evidence/kubernetes-evidence.md)
- [Promotion Evidence](docs/evidence/promotion-evidence.md)
- [Git History Evidence](docs/evidence/git-history-evidence.md)
- [Release Evidence](docs/evidence/release-evidence.md)

---

## Architecture Decisions

The project records major design decisions as ADRs, including:

- platform architecture
- GitOps controller selection
- container registry selection
- deployment configuration strategy
- repository model
- Kubernetes runtime selection
- immutable artifact strategy

See: [`docs/adr/`](docs/adr/)

---

## Documentation

| Document | Purpose |
| --- | --- |
| [Architecture Overview](docs/architecture/architecture-overview.md) | End-to-end component model |
| [Platform Architecture](docs/architecture/platform-architecture.md) | Architecture diagram and control flow |
| [CI Pipeline](docs/ci-pipeline.md) | CI design and release pipeline |
| [GitOps Deployment](docs/gitops-deployment.md) | Desired state and Argo CD reconciliation |
| [Environment Promotion](docs/environment-promotion.md) | Build-once promotion strategy |
| [Security and Supply Chain](docs/security-supply-chain.md) | Security architecture and artifact trust |
| [Drift / Self-Healing / Rollback](docs/drift-self-heal-rollback.md) | Failure and recovery validation |
| [Troubleshooting](docs/troubleshooting.md) | Operational troubleshooting guide |
| [Setup and Reproduction](docs/setup-reproduction.md) | Clean-environment bootstrap |
| [Cleanup](docs/cleanup.md) | Local environment cleanup |
| [Skills Demonstrated](docs/skills-demonstrated.md) | Engineering capabilities demonstrated |
| [Cost and Exclusions](docs/cost-and-exclusions.md) | Scope and cost decisions |

---

## Quick Start

Prerequisites include Docker, kubectl, kind, Git, GitHub CLI, Trivy, OpenSSL and Python 3.

Clone both repositories:

```bash
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/awais-clouddev/gitops-cicd-deployment-platform.git
git clone https://github.com/awais-clouddev/gitops-environments.git
```

Then follow the complete reproduction guide:

[Setup and Reproduction](docs/setup-reproduction.md)

---

## Local Lab Boundary

The runtime intentionally uses a local three-node kind cluster under WSL2.

This is designed to demonstrate the complete GitOps delivery and reconciliation lifecycle without requiring paid managed Kubernetes infrastructure.

It is a portfolio engineering lab and is **not presented as a production high-availability Kubernetes deployment**.

---

## Deliberate Exclusions

The following technologies are intentionally outside this project scope:

- Amazon EKS
- ECS / Fargate
- Terraform
- Helm
- Flux
- Jenkins
- Argo Rollouts
- Prometheus
- Grafana
- Istio
- Vault

Several are covered in other portfolio projects or reserved for a deeper Kubernetes / Platform Engineering project.

The goal here is architectural depth around **CI + immutable artifacts + GitOps + reconciliation**, not maximum tool count.

See: [Cost and Deliberate Exclusions](docs/cost-and-exclusions.md)

---

## Skills Demonstrated

This project demonstrates hands-on capability across:

- CI/CD architecture
- GitOps
- Kubernetes
- Docker
- GitHub Actions
- Argo CD
- Kustomize
- GHCR
- supply-chain security
- vulnerability management
- SBOM generation
- build provenance
- immutable artifact management
- release traceability
- environment promotion
- failure engineering
- drift detection
- self-healing
- Git-native rollback
- secrets hygiene
- troubleshooting
- technical documentation
- architecture decision-making

Full capability summary: [Skills Demonstrated](docs/skills-demonstrated.md)

---

## Core Engineering Principle

**CI produces trusted immutable artifacts. Git defines desired deployment state. Argo CD performs deployment and reconciliation.**
