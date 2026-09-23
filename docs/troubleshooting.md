# Troubleshooting Guide

## Purpose

This guide documents the main failure modes validated while building the GitOps CI/CD platform and the commands used to diagnose them.

## 1. GitHub Actions Startup Failure

### Symptom

The `Main Release Pipeline` finishes immediately with `startup_failure` and no job steps run.

### Cause

A reusable workflow requested permissions that were not granted by the caller workflow.

### Fix

Grant the reusable job the required permission in the calling workflow:

```yaml
permissions:
  contents: read
```

Then push the change and verify the next release run succeeds.

## 2. Trivy Local Image Layer Error

### Symptom

A local image scan fails with an error similar to:

```text
unable to get uncompressed layer
file blobs/sha256/... not found in tar
```

### Meaning

This is an image-layer access problem, not a vulnerability finding.

### Fix

Scan the immutable image directly from GHCR:

```bash
TRIVY_USERNAME="awais-clouddev" \
TRIVY_PASSWORD="$(gh auth token)" \
trivy image \
  --image-src remote \
  --scanners vuln \
  --severity HIGH,CRITICAL \
  --ignore-unfixed \
  IMAGE_REFERENCE
```

The verified API and frontend scans returned zero HIGH/CRITICAL vulnerabilities.

## 3. Argo CD OutOfSync

### Symptom

Argo CD reports:

```text
SYNC STATUS: OutOfSync
```

### Diagnosis

```bash
kubectl get application helpdesk-development -n argocd

kubectl get application helpdesk-development \
  -n argocd \
  -o jsonpath='{range .status.resources[?(@.status=="OutOfSync")]}{.kind}{" / "}{.name}{" => "}{.status}{"\n"}{end}'
```

### Expected Recovery

When self-healing is enabled, Argo CD restores live Kubernetes state to match Git.

## 4. ImagePullBackOff

### Symptom

A new pod enters:

```text
ErrImagePull
ImagePullBackOff
```

### Diagnosis

```bash
kubectl get pods -n helpdesk-development

kubectl describe pod POD_NAME -n helpdesk-development

kubectl get events \
  -n helpdesk-development \
  --sort-by=.lastTimestamp \
  | tail -n 30
```

### Recovery

Revert the bad desired-state commit in Git:

```bash
git revert BAD_COMMIT
git push origin main
```

## 5. Rollout Timeout

### Diagnosis

```bash
kubectl get deployment helpdesk-api -n helpdesk-development
kubectl get pods -n helpdesk-development | grep helpdesk-api
kubectl get events -n helpdesk-development --sort-by=.lastTimestamp | tail -n 30
```

## 6. Application Health Failure


```bash
kubectl get deployments,statefulsets -n helpdesk-development
kubectl get pods -n helpdesk-development
```

## 7. Missing Runtime Secret

```bash
kubectl get secret helpdesk-secrets -n helpdesk-development
```

The project does not commit Kubernetes Secret manifests to Git.

## 8. Argo CD Not Refreshing Immediately

```bash
kubectl annotate application helpdesk-development \
  -n argocd \
  argocd.argoproj.io/refresh=hard \
  --overwrite
```

## 9. Documentation-Only Pushes Triggering Deployment PRs

The release workflow currently runs on every push to `main`. During final regression, restrict release execution to release-relevant paths or add equivalent change detection.

## 10. Branch Protection Bypass Message

Branch protection exists, but the repository owner/admin can currently bypass it. This should be reviewed during the final security audit.

## Useful Health Commands

```bash
kubectl get application helpdesk-development -n argocd
kubectl get deployments,statefulsets -n helpdesk-development
kubectl get pods -n helpdesk-development
kubectl get services -n helpdesk-development
kubectl get events -n helpdesk-development --sort-by=.lastTimestamp | tail -n 30
```

## Core Troubleshooting Principle

Start with Git desired state, then inspect Argo CD reconciliation, Kubernetes rollout state, pod state, and events.

For Git-managed application state, fix or revert Git and allow Argo CD to reconcile.
