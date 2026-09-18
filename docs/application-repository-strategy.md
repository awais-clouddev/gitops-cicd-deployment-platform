# Application and Repository Strategy

## Application Workload

Project 5 will reuse the existing Containerized Help Desk Platform workload.

The application will be brought into the Project 5 application repository and used as the workload for CI/CD and GitOps automation.

## Repository 1 — Application Repository

Name:

gitops-cicd-deployment-platform

Responsibilities:

- Application source
- Dockerfiles
- Tests
- GitHub Actions CI
- Container build
- Security scanning
- SBOM generation
- Artifact attestation
- GHCR publication
- GitOps deployment update automation
- Project documentation

## Repository 2 — GitOps Repository

Name:

gitops-environments

Responsibilities:

- Kubernetes desired state
- Kustomize base
- Development overlay
- Staging overlay
- Immutable image revisions
- Argo CD reconciliation source

## Separation Rule

Application Repository = what we build.

GitOps Repository = what should be running.

CI must never deploy directly to Kubernetes.
