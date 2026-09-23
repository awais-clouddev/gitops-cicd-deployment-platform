# GitOps Deployment Evidence

## GitOps Repository

- Repository: `awais-clouddev/gitops-environments`
- GitOps commit: `23050bd49e701dee164fc5843c4cd48446048b8b`
- Environment: `development`
- Kustomize path: `apps/helpdesk/overlays/development`

## Argo CD State

- Sync status: `Synced`
- Health status: `Healthy`
- Auto-sync: `true`
- Prune: `true`
- Self-heal: `true`

## Development Desired State

- API: `ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-api@sha256:d0e5362a68e06846429aae6fda6020a7e2f94d74bc9cfc4325b4a2d229a2e4b3`
- Frontend: `ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-frontend@sha256:d3d2169eb6e7a5e385a78c31ef7395c9ccfacc84b3ac9d039b42bea97f5313d4`

## Release Traceability

- Source release SHA: `3bf1dffef919c85a7a74399ea16cacc403ce9f0b`

## GitOps Control Model

Application CI does not deploy directly to Kubernetes.

Deployment flow:

```text
GitHub Actions
    ↓
GitOps pull request
    ↓
GitOps main branch
    ↓
Argo CD
    ↓
Kubernetes
```

Argo CD continuously reconciles the live cluster against Git and is configured for automatic synchronization, pruning, and self-healing.
