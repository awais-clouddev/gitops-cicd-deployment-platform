# GitOps Deployment

## Purpose

This project uses GitOps for Continuous Delivery.

GitHub Actions builds and publishes immutable artifacts, but it does not deploy application workloads directly to Kubernetes.

Git is the desired-state source of truth and Argo CD performs reconciliation.

## GitOps Repository

Repository:

`awais-clouddev/gitops-environments`

The repository contains:

- Kubernetes base manifests
- Kustomize development overlay
- Kustomize staging overlay
- immutable API and frontend image digests
- Argo CD Application configuration
- environment promotion scripts
- Git-native deployment history

## Desired-State Model

The Kubernetes base contains reusable workload definitions.

Environment overlays define environment-specific configuration such as:

- namespace
- labels
- replica counts
- immutable image digests

Development and staging share the same workload base while maintaining independent desired state.

## Argo CD Application

The development Argo CD Application watches:

- repository: `https://github.com/awais-clouddev/gitops-environments.git`
- revision: `main`
- path: `apps/helpdesk/overlays/development`
- destination namespace: `helpdesk-development`

## Reconciliation Policy

The development Application uses:

- automatic synchronization
- pruning
- self-healing
- namespace creation

Current policy:

```text
autoSync=true
prune=true
selfHeal=true
```

## Deployment Flow

```text
GitHub Actions release
    ↓
GHCR immutable image digests
    ↓
Automated GitOps deployment branch
    ↓
GitOps pull request
    ↓
Merge to GitOps main
    ↓
Argo CD detects desired-state change
    ↓
Argo CD reconciles Kubernetes
    ↓
Application becomes Synced / Healthy
```

## Immutable Deployments

Application images are deployed by SHA256 digest.

The deployment does not depend on a mutable `latest` tag.

## Release Traceability

The development overlay records:

- immutable API digest
- immutable frontend digest
- source release SHA

The release SHA is propagated into Kubernetes resources through:

`gitops.platform/release-sha`

This creates a trace from source commit to running workload.

## Automated Deployment Proposal

After a successful release, the CI pipeline:

1. clones the GitOps repository
2. updates the development overlay with new image digests
3. records the source release SHA
4. creates a deployment branch
5. commits the desired-state change
6. pushes the branch
7. opens a GitOps pull request

CI does not run `kubectl apply` for application deployment.

## Environment Promotion

Promotion uses the build-once/promote-same-artifact model.

A release is promoted from development to staging by copying the approved immutable image digests.

No container image is rebuilt during promotion.

## Drift Detection

A controlled drift test changed the live API replica count from the Git-desired value of 1 to 3.

With self-healing temporarily disabled, Argo CD reported:

`OutOfSync`

The exact drifted resource was:

`Deployment / helpdesk-api`

## Self-Healing

After self-healing was re-enabled, Argo CD restored the API Deployment from 3 replicas back to the Git-desired value of 1.

The Application returned to:

`Synced / Healthy`

## Deleted Resource Recovery

A managed frontend Deployment was deliberately deleted from the cluster.

Argo CD recreated the resource automatically from Git desired state.

The recovered Deployment returned to:

`1/1 Ready`

## Bad Release Test

A controlled GitOps failure was created by committing an invalid API image digest.

Kubernetes attempted the new rollout and the new pod failed with:

`ErrImagePull`

and then:

`ImagePullBackOff`

The previous healthy API replica remained available during the failed rollout.

## Failure Visibility

The bad release was visible through:

- Argo CD health state
- Kubernetes Deployment rollout status
- pod status
- Kubernetes events
- image pull error details

## Git-Native Rollback

Rollback is performed through Git.

The bad desired-state commit was reverted and pushed to the GitOps `main` branch.

Argo CD reconciled the cluster back to the previous known-good immutable digest.

No direct `kubectl rollout undo` was used.

## Secrets Strategy

Application credentials are not stored in the GitOps repository.

Workloads reference the runtime Kubernetes Secret:

`helpdesk-secrets`

using `secretKeyRef`.

No Kubernetes `Secret` manifest is committed to Git.

## Argo CD Security Baseline

The local lab applies:

- anonymous access disabled
- exec functionality disabled
- Argo CD server exposed only as `ClusterIP`
- admin account retained for local bootstrap

## GitOps Security Boundary

```text
GitHub Actions
    → build, validate, scan, publish, propose

Git
    → authoritative desired state

Argo CD
    → deploy, reconcile, prune, self-heal

Kubernetes
    → run the declared workload
```

This prevents the CI system from becoming the Kubernetes deployment authority.

## Operational Principle

**Change Git to change the environment. Argo CD reconciles the cluster to that declared state.**
