# Verified Release Evidence

## Source Release

- Source repository: `awais-clouddev/gitops-cicd-deployment-platform`
- Source commit: `3bf1dffef919c85a7a74399ea16cacc403ce9f0b`
- GitHub Actions run: `35832919848`

## Published Immutable Artifacts

- API: `ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-api@sha256:d0e5362a68e06846429aae6fda6020a7e2f94d74bc9cfc4325b4a2d229a2e4b3`
- Frontend: `ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-frontend@sha256:d3d2169eb6e7a5e385a78c31ef7395c9ccfacc84b3ac9d039b42bea97f5313d4`

## GitOps Deployment

- GitOps repository: `awais-clouddev/gitops-environments`
- GitOps commit: `1c4b20ae4398131cc60df861aee4380f3a20d526`
- Deployment pull request: `#2`
- Environment: `development`

## Verified Deployment State

- Argo CD sync status: `Synced`
- Argo CD health status: `Healthy`
- Kubernetes workloads: `Ready`
- Application health: `healthy`
- PostgreSQL dependency: `connected`
- Redis dependency: `connected`

## Release Traceability

```text
Source commit
    ↓
GitHub Actions CI
    ↓
GHCR immutable image digests
    ↓
Automated GitOps pull request
    ↓
GitOps main branch
    ↓
Argo CD reconciliation
    ↓
Kubernetes workload
```

The deployed Kubernetes resources carry:

`gitops.platform/release-sha=3bf1dffef919c85a7a74399ea16cacc403ce9f0b`

This links the running workload back to the exact source release.
