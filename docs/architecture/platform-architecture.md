# GitOps CI/CD Platform Architecture

```mermaid
flowchart LR

    DEV[Developer]
    APP[Application Repository<br/>gitops-cicd-deployment-platform]

    subgraph CI[GitHub Actions CI]
        VALIDATE[Validation & Tests]
        BUILD[Container Build]
        TRIVY[Trivy Security Scan]
        SBOM[SBOM Generation]
        ATTEST[Build Provenance]
    end

    GHCR[(GitHub Container Registry)]

    PR[Automated GitOps<br/>Deployment PR]

    GITOPS[GitOps Repository<br/>gitops-environments]

    subgraph ARGO[Argo CD]
        WATCH[Watch Git Desired State]
        RECONCILE[Reconcile / Self-Heal / Prune]
    end

    subgraph K8S[Kubernetes - kind]
        API[Helpdesk API]
        FRONTEND[Frontend]
        GATEWAY[Nginx Gateway]
        POSTGRES[(PostgreSQL)]
        REDIS[(Redis)]
    end

    DEV -->|Git push| APP

    APP --> VALIDATE
    VALIDATE --> BUILD
    BUILD --> TRIVY
    TRIVY --> SBOM
    SBOM --> ATTEST

    BUILD -->|Immutable SHA tag| GHCR
    ATTEST --> GHCR

    CI -->|Image digests + source SHA| PR
    PR -->|Merge| GITOPS

    GITOPS --> WATCH
    WATCH --> RECONCILE

    RECONCILE -->|Pull desired state| K8S
    GHCR -->|Pull image by digest| K8S

    GATEWAY --> FRONTEND
    GATEWAY --> API
    API --> POSTGRES
    API --> REDIS


```

## Deployment Control Flow

```text
Developer
   ↓
Application Git Repository
   ↓
GitHub Actions CI
   ├── validation
   ├── container build
   ├── Trivy scanning
   ├── SBOM
   └── provenance
   ↓
GHCR immutable artifacts
   ↓
Automated GitOps Pull Request
   ↓
GitOps Repository
   ↓
Argo CD
   ↓
Kubernetes
```

## Core Principle

CI builds and publishes artifacts but does **not** deploy directly to Kubernetes.

Git defines the desired deployment state, while Argo CD continuously reconciles the Kubernetes cluster with that state.
