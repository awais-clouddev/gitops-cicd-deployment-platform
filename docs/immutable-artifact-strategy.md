# Immutable Artifact Strategy

## Version Source

Every application release is associated with the Git commit SHA that produced it.

Example:

sha-4f9c2a8...

## Container Tags

CI publishes traceable SHA-based tags:

- ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-api:sha-<git-sha>
- ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-frontend:sha-<git-sha>

The `latest` tag is not used for deployment.

## Deployment Identity

Kubernetes desired state will ultimately reference the immutable container digest:

ghcr.io/awais-clouddev/<image>@sha256:<digest>

Tags provide human-readable traceability.
Digests provide deployment immutability.

## Promotion Rule

An artifact is built once.

development -> staging

Promotion changes only GitOps desired state and reuses the exact same image digest.

The image is never rebuilt during promotion.

## Rollback Rule

Rollback is performed by reverting GitOps desired state to a previous known-good immutable image digest.

Argo CD then reconciles the cluster back to that version.
