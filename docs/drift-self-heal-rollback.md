# Drift, Self-Healing, and Rollback

## Purpose

This document records how the platform detects configuration drift, restores desired state, recovers deleted resources, exposes failed releases, and performs Git-native rollback.

Git is the authoritative deployment state. Argo CD continuously compares the live Kubernetes cluster with the desired state stored in the GitOps repository.

## Drift Experiment

A controlled drift experiment was performed against the development API Deployment.

Desired state in Git:

```text
replicas: 1
```

The live Kubernetes Deployment was manually changed to:

```text
replicas: 3
```

Self-healing was temporarily disabled so the mismatch could be observed clearly.

## Drift Detection

After the live Deployment was changed, Argo CD detected the difference between Git and the cluster.

Observed Argo CD status:

```text
SYNC STATUS: OutOfSync
HEALTH STATUS: Healthy
```

Argo CD identified the exact drifted resource:

```text
Deployment / helpdesk-api => OutOfSync
```

## Self-Healing

Self-healing was re-enabled after drift detection.

Argo CD automatically restored the API Deployment from 3 replicas back to the Git-defined value of 1.

Verified final state:

```text
helpdesk-api   1/1 Ready
Argo CD        Synced / Healthy
selfHeal       true
```

## Deleted Resource Recovery

A managed frontend Deployment was deliberately deleted from the Kubernetes cluster.

Because the resource still existed in Git desired state, Argo CD recreated it automatically.

The recovered Deployment returned to:

```text
1/1 Ready
```

Argo CD returned to:

```text
Synced / Healthy
```

## Bad Release Scenario

A controlled bad release was introduced through Git by replacing the development API image digest with an invalid SHA256 digest.

The invalid desired state used:

```text
sha256:0000000000000000000000000000000000000000000000000000000000000000
```

Kubernetes attempted to deploy the new release.

## Failure Behavior

The new API pod could not pull the invalid artifact.

Observed Kubernetes states included:

```text
ErrImagePull
ImagePullBackOff
```

The existing healthy API replica remained available while the new rollout failed.

## Failure Visibility

The failed release was visible through:

- Argo CD application health
- Kubernetes rollout status
- pod readiness and state
- Kubernetes events
- image pull error details

## Git-Native Rollback

Rollback was performed by reverting the bad desired-state commit in Git.

No direct cluster rollback command was used.

```text
Bad GitOps commit
    ↓
git revert
    ↓
Push revert to GitOps main
    ↓
Argo CD detects restored desired state
    ↓
Argo CD reconciles Kubernetes
    ↓
Previous known-good image digest restored
```

## Rollback Verification

After the Git revert, Argo CD returned to:

```text
Synced / Healthy
```

The running API image matched the Git desired image exactly:

```text
sha256:d0e5362a68e06846429aae6fda6020a7e2f94d74bc9cfc4325b4a2d229a2e4b3
```

Application health returned:

```json
{"status":"healthy","database":"connected","redis":"connected"}
```

## Operational Model

```text
Drift
    ↓
Argo CD detects OutOfSync
    ↓
Self-heal restores Git state

Deleted managed resource
    ↓
Argo CD detects missing resource
    ↓
Argo CD recreates it from Git

Bad release
    ↓
Kubernetes exposes rollout failure
    ↓
Git revert restores known-good desired state
    ↓
Argo CD reconciles automatically
```

## Core Principle

**Do not repair Git-managed application state by making permanent manual cluster changes. Change or revert Git, then allow Argo CD to reconcile the cluster.**
