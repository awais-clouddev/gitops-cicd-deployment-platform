# Environment Promotion

## Purpose

This project uses a build-once, promote-the-same-artifact model.

Container images are built once by CI, published to GHCR, resolved to immutable SHA256 digests, and then promoted between environments by changing GitOps desired state.

Promotion does not rebuild the application.

## Environment Model

The GitOps repository contains separate overlays for:

- development
- staging

Both environments share the same Kubernetes base configuration while maintaining independent desired state.

## Development Release

A successful application release creates a GitOps pull request that updates the development overlay with:

- API image digest
- frontend image digest
- source release SHA

After the pull request is merged, Argo CD reconciles the development cluster state.

## Promotion to Staging

Promotion is performed by copying the already-approved development image digests into the staging overlay.

The promotion script is:

`scripts/promote-development-to-staging.py`

The script reads the immutable API and frontend digests from development and writes the same digests into staging.

## Build Once, Promote Same Artifact

The intended flow is:

```text
Source commit
    ↓
CI builds images once
    ↓
GHCR immutable digests
    ↓
Development desired state
    ↓
Development validation
    ↓
Promotion
    ↓
Same immutable digests
    ↓
Ctaging desired state
```

No second container build occurs during promotion.

## Promotion Integrity Verification

The GitOps repository contains:

`scripts/verify-promotion-integrity.py`

This script compares the development and staging digests and fails if the promoted artifacts differ.

The verified promotion test produced:

```text
API:      PASS - identical immutable artifact
Frontend: PASS - identical immutable artifact
PROMOTION INTEGRITY: PASS
```

## Verified Promotion Evidence

The recorded promotion commit is:

`e1e53a3af4fe7cb9261072cbcdc0951f2d0a5c80`

At that promotion point:

### API

Development:

`sha256:47e0c71aa16efbfc5307a484f929caf0519b4fc682a2faa8955c68a7deb15d63`

Staging:

`sha256:47e0c71aa16efbfc5307a484f929caf0519b4fc682a2faa8955c68a7deb15d63`

Result: MATCH

### Frontend

Development:

`sha256:275c29fa31da85f242aba222d84e968d3c1f670ac86663ce718de34ad8c47f92`

Staging:

`sha256:275c29fa31da85f242aba222d84e968d3c1f670ac86663ce718de34ad8c47f92`

Result: MATCH

## Why Immutable Digests Matter

A mutable tag can point to different image content over time.

A SHA256 digest identifies exact image content.

Using digests ensures that the artifact validated in development is the same artifact promoted to staging.

## Promotion Boundary

Development can receive automated deployment proposals from CI.

Staging changes are explicit promotion operations.

This separates rapid development delivery from controlled environment promotion.

## Rollback Relationship

Because environments store immutable digests in Git, rollback is also Git-native.

A previous known-good digest can be restored by reverting the desired-state change and allowing Argo CD to reconcile.

## Operational Principle

The promotion rule for this project is:

**Build once. Verify the artifact. Promote the same immutable digest. Never rebuild during environment promotion.**
