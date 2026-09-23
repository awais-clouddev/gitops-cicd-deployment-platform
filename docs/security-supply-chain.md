# Security and Software Supply Chain

## Purpose

This document summarizes the security controls applied across source control, CI, container build, registry publication, GitOps delivery, and Kubernetes runtime.

The goal is to reduce credential exposure, prevent mutable deployment references, detect vulnerable artifacts, preserve release traceability, and keep deployment authority separated from CI.

## Repository Security

The application and GitOps repositories were audited for accidental secret exposure.

Controls include:

- no tracked `.env` files
- no committed Kubernetes `Secret` manifests
- GitHub token pattern scans across tracked files
- Trivy repository secret scans
- clean Git remotes with no embedded credentials

Both repositories completed secret scans with zero detected secrets.

## GitHub Credentials

The deployment workflow uses GitHub repository secrets rather than hard-coded credentials.

The application repository stores:

- `GITOPS_TOKEN`

GitHub Actions also uses the built-in:

- `GITHUB_TOKEN`

Workflow files reference these secrets through GitHub Actions secret expressions.

No GitHub token values are committed to either repository.

## Workflow Permissions

The release workflow follows least-privilege permissions.

The release job receives only the permissions required for:

- repository read access
- GHCR package publication
- OIDC token issuance
- provenance attestations

The reusable GitOps workflow receives only the permissions required for its operation.

## GitHub Actions Pinning

Third-party and first-party GitHub Actions are pinned to immutable commit SHAs rather than mutable version tags.

This reduces the risk that a workflow dependency changes unexpectedly after review.

## Container Build Security

The API and frontend container images use pinned base image digests.

The API image:

- uses a pinned Python slim base image
- upgrades OS packages during build
- validates Python dependencies with `pip check`
- runs as non-root UID `10001`
- copies application files with explicit ownership

The frontend image:

- uses a pinned Nginx Alpine base image
- upgrades Alpine packages during build
- runs as non-root user `nginx` / UID `101`
- copies static assets with explicit ownership

## Vulnerability Scanning

Trivy is used as the container vulnerability scanner.

The CI release workflow scans both API and frontend images for:

- HIGH vulnerabilities
- CRITICAL vulnerabilities

The verified release audit showed zero HIGH/CRITICAL findings for both application images.

## Software Bill of Materials

CycloneDX SBOMs are generated for:

- API image
- frontend image

The SBOMs are uploaded as GitHub Actions artifacts and retained as release evidence.

## Build Provenance

GitHub build provenance attestations are generated for both published application images.

The release workflow uses:

- `id-token: write`
- `attestations: write`

The attestation subjects are the published GHCR image names and immutable digests.

## Immutable Release Identity

Application releases use source-SHA-based tags:

`sha-<source-commit>`

After registry publication, the workflow resolves the actual GHCR SHA256 digest.

GitOps desired state records the immutable digest rather than relying on a mutable tag.

The project does not use `latest` for application releases.

## Registry Integrity

Release evidence verifies that the source-SHA tags in GHCR resolve to the same immutable digests recorded in GitOps desired state.

This connects:

```text
source commit
    ↓
release tag
    ↓
registry digest
    ↓
GitOps desired state
```

## GitOps Security Boundary

CI does not directly deploy workloads to Kubernetes.

The application workflow contains no direct deployment commands such as:

- `kubectl apply`
- `kubectl patch`
- `kubectl delete`
- `helm install`
- `helm upgrade`

CI builds, scans, publishes, and proposes desired-state changes.

Argo CD remains the Kubernetes deployment and reconciliation authority.

## Kubernetes Secrets Strategy

Application credentials are not stored in Git.

Kubernetes manifests reference runtime secret values using `secretKeyRef`.

The referenced runtime Secret is:

`helpdesk-secrets`

No Kubernetes `Secret` manifest is committed to the GitOps repository.

## Argo CD Security Baseline

The local lab applies these Argo CD controls:

- anonymous access disabled
- exec functionality disabled
- server exposed as `ClusterIP`
- admin account retained only for local bootstrap

The admin decision is documented as a local-lab bootstrap choice rather than a production identity model.

## Reconciliation Controls

The development Argo CD Application uses:

- automatic synchronization
- pruning
- self-healing

These controls were validated through deliberate drift and deleted-resource recovery tests.

## Drift Protection

A live API replica count was deliberately changed from the Git-desired value of 1 to 3.

Argo CD detected the resource as `OutOfSync`.

After self-healing was enabled, Argo CD restored the Deployment to the Git-declared replica count.

## Deleted Resource Recovery

A managed frontend Deployment was deliberately deleted.

Argo CD recreated the Deployment from Git desired state and returned the application to `Synced / Healthy`.

## Failed Release Containment

A controlled bad release used an invalid immutable API digest.

Kubernetes reported:

- `ErrImagePull`
- `ImagePullBackOff`

The previous healthy API replica remained available while the new rollout failed.

This demonstrated failure visibility without bypassing GitOps.

## Git-Native Rollback

Rollback is performed by reverting the bad desired-state commit in Git.

Argo CD then reconciles Kubernetes back to the previous known-good immutable artifact.

No direct cluster rollback command is required.

## Supply Chain Control Summary

The implemented controls include:

- immutable GitHub Action SHA pinning
- least-privilege workflow permissions
- GitHub Secrets for credentials
- repository secret scanning
- non-root application containers
- pinned base image digests
- Trivy HIGH/CRITICAL vulnerability gates
- CycloneDX SBOM generation
- build provenance attestations
- source-SHA release tags
- immutable GHCR digest resolution
- digest-based GitOps deployment
- no direct CI-to-Kubernetes deployment
- Git-native promotion and rollback
- Argo CD self-healing and pruning

## Security Principle

**CI produces verified immutable artifacts. Git records deployment intent. Argo CD reconciles the cluster. Secrets and credentials remain outside committed desired state.**
