# Environment Promotion Evidence

## Promotion Commit

- GitOps commit: `e1e53a3af4fe7cb9261072cbcdc0951f2d0a5c80`
- Promotion path: `development → staging`

## API Artifact

- Development digest: `sha256:47e0c71aa16efbfc5307a484f929caf0519b4fc682a2faa8955c68a7deb15d63`
- Staging digest: `sha256:47e0c71aa16efbfc5307a484f929caf0519b4fc682a2faa8955c68a7deb15d63`
- Result: **MATCH**

## Frontend Artifact

- Development digest: `sha256:275c29fa31da85f242aba222d84e968d3c1f670ac86663ce718de34ad8c47f92`
- Staging digest: `sha256:275c29fa31da85f242aba222d84e968d3c1f670ac86663ce718de34ad8c47f92`
- Result: **MATCH**

## Promotion Model

The application images were built once by CI and promoted between environments by changing GitOps desired state.

No container rebuild occurred during promotion.

**Artifact promotion integrity: PASS**
