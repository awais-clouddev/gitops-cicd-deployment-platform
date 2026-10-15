# Setup and Reproduction Guide

## Purpose

This guide explains how to reproduce the local GitOps CI/CD platform from a clean Ubuntu/WSL2 environment.

The platform uses a three-node kind Kubernetes cluster, GitHub Actions for CI, GHCR for immutable container artifacts, a separate GitOps repository for desired state, and Argo CD for continuous reconciliation.

## Repositories

Application repository:

`https://github.com/awais-clouddev/gitops-cicd-deployment-platform.git`

GitOps repository:

`https://github.com/awais-clouddev/gitops-environments.git`

Recommended local layout:

```text
~/projects/
├── gitops-cicd-deployment-platform/
└── gitops-environments/
```

## Prerequisites

Required tools:

- Ubuntu or WSL2
- Git
- Docker
- kubectl
- kind
- GitHub CLI
- Trivy
- OpenSSL
- Python 3

Verify:

```bash
git --version
docker --version
kubectl --context kind-gitops-platform version --client
kind version
gh --version
trivy --version
openssl version
python3 --version
```

Docker must be running before the kind cluster is created.

## Clone the Repositories

```bash
mkdir -p ~/projects
cd ~/projects

git clone https://github.com/awais-clouddev/gitops-cicd-deployment-platform.git
git clone https://github.com/awais-clouddev/gitops-environments.git
```

Verify both repositories:

```bash
cd ~/projects/gitops-cicd-deployment-platform
git status --short

cd ~/projects/gitops-environments
git status --short
```

Both should be clean.

## GitHub Authentication

Authenticate GitHub CLI without storing credentials in repository files:

```bash
gh auth login
gh auth status
```

Never commit access tokens, passwords, `.env` files, or Kubernetes Secret manifests.

## Create the kind Cluster

From the application repository:

```bash
cd ~/projects/gitops-cicd-deployment-platform

kind create cluster   --name gitops-platform   --config platform/kind/cluster.yaml
```

Verify:

```bash
kubectl --context kind-gitops-platform config current-context
kubectl --context kind-gitops-platform get nodes -o wide
```

Expected context:

```text
kind-gitops-platform
```

The project cluster contains three Kubernetes nodes.

## Install Argo CD

Create the namespace:

```bash
kubectl --context kind-gitops-platform create namespace argocd
```

Read the project version:

```bash
cd ~/projects/gitops-cicd-deployment-platform
ARGO_VERSION="$(cat platform/argocd/version.txt)"
echo "$ARGO_VERSION"
```

Install that version:

```bash
kubectl --context kind-gitops-platform apply -n argocd   -f "https://raw.githubusercontent.com/argoproj/argo-cd/${ARGO_VERSION}/manifests/install.yaml"
```

Wait for the server:

```bash
kubectl --context kind-gitops-platform wait   --for=condition=Available   deployment/argocd-server   -n argocd   --timeout=300s
```

Check components:

```bash
kubectl --context kind-gitops-platform get pods -n argocd
```

## Apply the Argo CD Lab Security Baseline

```bash
cd ~/projects/gitops-cicd-deployment-platform
kubectl --context kind-gitops-platform apply -f platform/argocd/security-baseline.yaml
```

Verify important settings:

```bash
kubectl --context kind-gitops-platform get configmap argocd-cm   -n argocd   -o jsonpath='anonymous={.data.users\.anonymous\.enabled}{"\n"}exec={.data.exec\.enabled}{"\n"}'

kubectl --context kind-gitops-platform get service argocd-server -n argocd
```

The lab baseline keeps anonymous access disabled, exec disabled, and the Argo CD server as ClusterIP.

## Create the Development Namespace

```bash
kubectl --context kind-gitops-platform create namespace helpdesk-development   --dry-run=client   -o yaml | kubectl --context kind-gitops-platform apply -f -
```

## Create Runtime-Only Secrets

Generate a local database password:

```bash
DB_PASSWORD="$(openssl rand -base64 32)"
```

Create the runtime secret:

```bash
kubectl --context kind-gitops-platform create secret generic helpdesk-secrets -n helpdesk-development --from-literal=database-name=helpdesk --from-literal=database-user=helpdesk --from-literal=database-password="$DB_PASSWORD" --dry-run=client -o yaml | kubectl --context kind-gitops-platform apply -f -
```

Remove the shell variable:

```bash
unset DB_PASSWORD
```

Do not export this Secret manifest into Git.

## Validate GitOps Manifests

```bash
cd ~/projects/gitops-environments

kubectl --context kind-gitops-platform kustomize apps/helpdesk/overlays/development > /tmp/helpdesk-development.yaml
kubectl --context kind-gitops-platform kustomize apps/helpdesk/overlays/staging > /tmp/helpdesk-staging.yaml

test -s /tmp/helpdesk-development.yaml
test -s /tmp/helpdesk-staging.yaml

rm -f /tmp/helpdesk-development.yaml /tmp/helpdesk-staging.yaml
```

## Register the Development Application

```bash
cd ~/projects/gitops-environments
kubectl --context kind-gitops-platform apply -f argocd/helpdesk-development.yaml
```

Verify:

```bash
kubectl --context kind-gitops-platform get application helpdesk-development -n argocd
```

Argo CD should begin reconciling the development overlay automatically.

## Wait for Workloads

```bash
kubectl --context kind-gitops-platform get pods -n helpdesk-development -w
```

When all workload pods are Ready, stop the watch with `Ctrl+C`.

Then verify:

```bash
kubectl --context kind-gitops-platform get deployments,statefulsets -n helpdesk-development
kubectl --context kind-gitops-platform get pods -n helpdesk-development
kubectl --context kind-gitops-platform get services -n helpdesk-development
```

## Validate Argo CD Health

```bash
kubectl --context kind-gitops-platform get application helpdesk-development   -n argocd   -o jsonpath='sync={.status.sync.status} health={.status.health.status}{"\n"}'
```

Expected steady state:

```text
sync=Synced health=Healthy
```

## Validate Reconciliation Controls

```bash
kubectl --context kind-gitops-platform get application helpdesk-development   -n argocd   -o jsonpath='autoSync={.spec.syncPolicy.automated.enabled} prune={.spec.syncPolicy.automated.prune} selfHeal={.spec.syncPolicy.automated.selfHeal}{"\n"}'
```

Expected:

```text
autoSync=true prune=true selfHeal=true
```

## Validate Immutable Images

```bash
kubectl --context kind-gitops-platform get pods   -n helpdesk-development   -o jsonpath='{range .items[*]}{.metadata.name}{" => "}{range .spec.containers[*]}{.image}{" "}{end}{"\n"}{end}'
```

The API and frontend application images should use immutable SHA256 digests rather than `latest`.

## Validate Release Traceability

```bash
kubectl --context kind-gitops-platform get deployment helpdesk-api   -n helpdesk-development   -o jsonpath='{.metadata.annotations.gitops\.platform/release-sha}{"\n"}'
```

The value should correspond to the source Git commit associated with the deployed release.

## Validate Application Health

Start a port-forward:

```bash
kubectl --context kind-gitops-platform port-forward   -n helpdesk-development   service/helpdesk-gateway   18090:80
```

In another terminal:

```bash
curl -fsS http://127.0.0.1:18090/api/health
```

Expected structure:

```json
{"status":"healthy","database":"connected","redis":"connected"}
```

Stop the port-forward with `Ctrl+C`.

## Verify CI Workflows

From the application repository:

```bash
cd ~/projects/gitops-cicd-deployment-platform
gh workflow list
gh run list --limit 10
```

The repository contains separate workflows for pull-request validation, the main release pipeline, and the reusable GitOps desired-state update.

## Verify GitOps Desired State

```bash
cd ~/projects/gitops-environments
cat apps/helpdesk/overlays/development/kustomization.yaml
```

The development overlay should contain immutable image digests and the source release SHA annotation.

## Repository Cleanliness

Application repository:

```bash
cd ~/projects/gitops-cicd-deployment-platform
git status --short
```

GitOps repository:

```bash
cd ~/projects/gitops-environments
git status --short
```

Both should return no output.

## Reproduction Success Criteria

The environment is successfully reproduced when:

- the kind cluster has three Ready nodes
- all Argo CD components are running
- the development Application is registered
- Argo CD reports Synced and Healthy
- all helpdesk workloads are Ready
- the gateway health endpoint reports healthy
- PostgreSQL and Redis report connected
- API and frontend use immutable image digests
- the source release SHA is present
- automatic sync, prune, and self-heal are enabled
- no application credentials are stored in Git

## Reproduction Principle

Bootstrap the local platform once, then let Git define application desired state and let Argo CD reconcile Kubernetes.

Normal application delivery should flow through CI -> GHCR -> GitOps pull request -> Argo CD rather than direct Kubernetes deployment from CI.

## Current Verification Scope

Eight API regression tests passed using an isolated container with mocked
database/cache dependencies. They cover input validation, filter casing,
cache-key collisions, malformed cache responses and Redis failure handling.

Both GitOps overlays rendered and passed namespace, image-digest and
Secret-key checks. Promotion integrity passed in a disposable repository copy.

Development is configured for Argo CD reconciliation. Staging remains
desired-state-only; promotion does not establish a running staging environment.

The existing local cluster could not start because of Docker storage errors.
Clean installation and current reconciliation remain unverified. Historical
evidence describes earlier runs, not validation of these revised images.

Use the GitOps repository's docs/validation-scope.md for environment scope.
