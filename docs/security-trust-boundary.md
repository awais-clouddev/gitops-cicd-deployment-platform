# Security and Trust-Boundary Design

## CI Responsibilities

GitHub Actions may:

- Validate source code
- Run tests
- Build container images
- Run security scans
- Generate SBOM/provenance
- Publish images to GHCR
- Propose deployment-state changes to the GitOps repository

## CI Restrictions

GitHub Actions must not:

- Run kubectl apply
- Deploy directly to Kubernetes
- Bypass GitOps
- Store plaintext secrets in the repository

## GitOps Responsibilities

The GitOps repository stores approved desired deployment state.

Only approved Git changes may alter:

- development image version
- staging image version
- Kubernetes desired configuration

## Argo CD Responsibilities

Argo CD may:

- Read desired state from Git
- Reconcile Kubernetes
- Detect drift
- Self-heal managed resources
- Prune removed managed resources

## Trust Boundaries

Developer
→ GitHub Pull Request
→ CI validation
→ GHCR artifact
→ GitOps repository
→ Argo CD
→ Kubernetes

## Security Principles

- Least privilege
- No secrets committed to Git
- Immutable release artifacts
- Reviewable deployment changes
- Git as deployment source of truth
- CI separated from CD
