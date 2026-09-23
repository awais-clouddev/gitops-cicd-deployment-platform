# CI Pipeline

## Purpose

The CI pipeline validates source code, builds container images, performs security checks, publishes immutable artifacts, generates software supply-chain evidence, and proposes deployment changes to the GitOps repository.

CI does not deploy directly to Kubernetes.

## Trigger

The main release workflow runs on:

- pushes to `main`
- manual workflow dispatch

Pull requests use a separate validation workflow.

## Pull Request Validation

The pull request workflow validates:

- required repository structure
- accidental `.env` tracking
- Python syntax
- Docker Compose configuration
- immutable image version generation
- API container build
- frontend container build

The required status check is:

`Repository Validation`

## Release Pipeline

The main release pipeline performs:

```text
Source push
    ↓
Generate immutable version
    ↓
Validate application
    ↓
Build API image
    ↓
Build frontend image
    ↓
Trivy security gates
    ↓
Generate CycloneDX SBOMs
    ↓
Upload SBOM evidence
    ↓
Authenticate to GHCR
    ↓
Publish API image
    ↓
Publish frontend image
    ↓
Resolve immutable image digests
    ↓
Generate build provenance attestations
    ↓
Propose GitOps deployment PR
```

## Immutable Versioning

Images are tagged using the full source Git SHA:

`sha-<source-commit>`

The platform does not use `latest` for application releases.

## Container Security

The API and frontend images are scanned for:

- HIGH vulnerabilities
- CRITICAL vulnerabilities

Trivy is used as the vulnerability scanner.

The release pipeline fails when the configured security gate is violated.

## SBOM

CycloneDX SBOMs are generated for:

- API image
- frontend image

The SBOMs are uploaded as GitHub Actions artifacts for release evidence.

## Build Provenance

GitHub build attestations are generated for both application images.

The release job has the required:

- `id-token: write`
- `attestations: write`

permissions.

## Registry Publication

Images are published to GitHub Container Registry.

The release workflow resolves the actual registry digest after publication.

The deployment process uses the immutable digest rather than relying only on the human-readable tag.

## GitOps Handoff

After the images are published and their digests are known, the pipeline invokes the GitOps deployment workflow.

The workflow:

1. checks out the application repository
2. clones the GitOps repository
3. updates development desired state with the new immutable digests
4. records the source release SHA
5. creates a deployment branch
6. pushes the branch
7. creates a GitOps pull request

## CI/CD Separation

The application pipeline never runs commands such as:

- `kubectl apply`
- `kubectl patch`
- `kubectl delete`
- `helm install`
- `helm upgrade`

This keeps deployment responsibility with Argo CD.

## Release Traceability

Each release connects:

```text
Source SHA
    ↓
GitHub Actions run
    ↓
GHCR image tag
    ↓
GHCR image digest
    ↓
GitOps pull request
    ↓
GitOps commit
    ↓
Argo CD reconciliation
    ↓
Running Kubernetes workload
```

## Failure Handling

CI failures stop artifact publication or deployment proposals.

GitOps deployment failures remain visible through:

- Argo CD application health
- Kubernetes rollout status
- pod events
- image pull errors

## Concurrency

Release concurrency prevents overlapping release operations from corrupting deployment state.

Pull request validation uses separate concurrency behavior and cancels superseded validation runs.

## Security Model

The CI pipeline applies:

- least-privilege workflow permissions
- GitHub Secrets for credentials
- immutable GitHub Action commit pinning
- Trivy vulnerability gates
- SBOM generation
- build provenance attestations
- immutable artifact digests
- no direct Kubernetes deployment
