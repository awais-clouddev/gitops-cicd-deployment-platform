# Cleanup Guide

## Purpose

This guide explains how to safely clean up the local GitOps CI/CD lab after testing while preserving the Git repositories and project evidence.

## Stop Port Forwarding

If a kubectl port-forward session is still running, return to that terminal and press Ctrl+C.

Verify that no project port-forward process remains:

```bash
ps aux | grep "[k]ubectl port-forward"
```

## Remove Temporary Rendered Manifests

Delete temporary Kustomize output files created during validation:

```bash
rm -f /tmp/helpdesk-development.yaml
rm -f /tmp/helpdesk-staging.yaml
```

These files are generated validation artifacts and are not part of the Git repositories.

## Remove Temporary Shell Variables

Unset temporary values that may have been created during setup or validation:

```bash
unset DB_PASSWORD
unset TRIVY_USERNAME
unset TRIVY_PASSWORD
```

## Delete the Local Kubernetes Cluster

The main local runtime is the kind cluster named gitops-platform.

Confirm the existing clusters:

```bash
kind get clusters
```

Delete the project cluster:

```bash
kind delete cluster --name gitops-platform
```

Verify removal:

```bash
kind get clusters
```

Deleting the kind cluster removes the local Kubernetes runtime, including Argo CD, application workloads, namespaces, services, and runtime-only Kubernetes Secrets stored inside that cluster.

## Docker Cleanup

List local containers and images before removing anything:

```bash
docker ps -a
docker images
```

Optional cleanup of unused Docker resources:

```bash
docker system prune
```

Do not use aggressive cleanup options unless removal of unused local images, containers, networks, and build cache is intentional.

## Preserve Git Repositories

The following repositories should normally remain on disk:

```text
~/projects/gitops-cicd-deployment-platform
~/projects/gitops-environments
```

They contain project source code, Git history, documentation, evidence, workflows, and GitOps desired state.

## Verify Application Repository Cleanliness

```bash
cd ~/projects/gitops-cicd-deployment-platform
git status --short
```

Expected result: no output.

## Verify GitOps Repository Cleanliness

```bash
cd ~/projects/gitops-environments
git status --short
```

Expected result: no output.

## Preserve Remote Evidence

Local cluster deletion does not remove GitHub-hosted project history.

The following remain available remotely:

- Git commits
- pull requests
- GitHub Actions history
- GHCR artifacts
- SBOM workflow artifacts while retained by GitHub
- build attestations
- project documentation
- evidence files committed to Git

## Recreate the Lab

After cleanup, the environment can be rebuilt using:

`docs/setup-reproduction.md`

The intended lifecycle is:

```text
Create local cluster
    ->
Install Argo CD
    ->
Create runtime-only secrets
    ->
Register GitOps Application
    ->
Argo CD reconciles desired state
    ->
Validate platform
    ->
Delete local cluster when finished
```

## Cleanup Principle

**Destroy disposable runtime infrastructure while preserving Git, immutable release history, documentation, and evidence required to reproduce and explain the platform.**
