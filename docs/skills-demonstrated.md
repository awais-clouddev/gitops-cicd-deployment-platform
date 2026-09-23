# Skills Demonstrated

## Purpose

This document summarizes the engineering skills demonstrated by the GitOps-Driven CI/CD Deployment Platform.

The project focuses on practical delivery engineering rather than isolated tool usage.

## CI Engineering

- Designed separate pull-request validation and release workflows.
- Built container images through GitHub Actions.
- Added concurrency controls for CI execution.
- Used reusable workflows for GitOps deployment proposals.
- Implemented explicit workflow permissions.

## GitOps Continuous Delivery

- Separated Continuous Integration from Continuous Delivery.
- Prevented CI from directly deploying application workloads to Kubernetes.
- Used Git as the authoritative desired deployment state.
- Used Argo CD as the reconciliation and deployment controller.
- Implemented automated synchronization, pruning, and self-healing.

## Kubernetes Engineering

- Deployed a multi-service application to Kubernetes.
- Managed Deployments, StatefulSets, Services, ConfigMaps, namespaces, and runtime Secrets.
- Configured resource requests and limits.
- Configured readiness and liveness probes.
- Validated rollout status, pod state, events, and application health.

## Local Kubernetes Platform

- Created a three-node Kubernetes cluster with kind.
- Installed and validated Argo CD.
- Applied a lab security baseline to the Argo CD control plane.
- Maintained the Argo CD server as ClusterIP-only.

## Kustomize Configuration Management

- Created reusable Kubernetes base manifests.
- Created separate development and staging overlays.
- Managed environment-specific replica counts and immutable image references.
- Validated rendered configuration before deployment.

## Container Engineering

- Built separate API and frontend container images.
- Used pinned base-image digests.
- Applied package updates during image builds.
- Used non-root runtime users.
- Applied ownership controls during container builds.
- Validated containers locally before automated release.

## Immutable Artifact Management

- Used source-SHA-based release identity.
- Published application artifacts to GHCR.
- Resolved registry image digests after publication.
- Deployed API and frontend images using immutable SHA256 digests.
- Avoided `latest` for application releases.

## Software Supply-Chain Security

- Scanned images with Trivy.
- Enforced HIGH and CRITICAL vulnerability gates.
- Generated CycloneDX SBOMs.
- Generated build provenance attestations.
- Pinned third-party GitHub Actions to immutable commit SHAs.
- Used least-privilege GitHub Actions permissions.

## Release Traceability

- Connected source Git SHA to GitHub Actions execution.
- Connected CI output to GHCR image digests.
- Propagated release identity into GitOps desired state.
- Added source release SHA annotations to Kubernetes resources.
- Verified the release running in Kubernetes against Git desired state.

## Environment Promotion

- Implemented development-to-staging promotion.
- Used a build-once, promote-the-same-artifact model.
- Promoted existing immutable digests instead of rebuilding images.
- Added promotion-integrity verification.
- Preserved independent desired state for development and staging.

## GitOps Automation

- Automated development desired-state updates.
- Created deployment branches automatically.
- Created GitOps pull requests from successful releases.
- Passed immutable image digests and source release SHA between workflows.

## Drift Detection

- Performed a controlled live-cluster drift experiment.
- Verified that Argo CD detected the changed Kubernetes resource as OutOfSync.
- Identified the exact drifted Deployment.

## Self-Healing

- Re-enabled Argo CD self-healing after the drift experiment.
- Verified automatic restoration of the Git-defined replica count.
- Confirmed the Application returned to Synced and Healthy.

## Deleted Resource Recovery

- Deliberately deleted a Git-managed Deployment.
- Verified Argo CD recreated the resource automatically.
- Confirmed the recovered workload returned to Ready state.

## Failure Engineering

- Introduced a controlled bad release using an invalid image digest.
- Observed `ErrImagePull` and `ImagePullBackOff` behavior.
- Verified the previous healthy replica remained available during the failed rollout.
- Used Argo CD and Kubernetes status to expose the failure.

## Git-Native Rollback

- Reverted bad desired state through Git.
- Avoided direct `kubectl rollout undo` for Git-managed application state.
- Allowed Argo CD to reconcile the previous known-good artifact automatically.
- Verified the running digest after rollback.

## Secrets and Credential Hygiene

- Kept application Secrets out of Git.
- Used `secretKeyRef` from Kubernetes workloads.
- Created runtime-only Kubernetes Secrets.
- Stored workflow credentials in GitHub repository secrets.
- Verified Git remotes contained no embedded credentials.
- Scanned repositories for committed secrets.

## GitHub Repository Engineering

- Configured branch protection.
- Added required validation checks.
- Prevented force pushes and branch deletion.
- Used linear history controls.
- Tested a deliberate pull-request validation failure.

## Operational Troubleshooting

- Diagnosed GitHub Actions startup permission failures.
- Diagnosed Trivy local image-layer problems.
- Diagnosed Argo CD OutOfSync conditions.
- Diagnosed Kubernetes image-pull and rollout failures.
- Used Kubernetes events, pod state, rollout status, and Argo CD health for investigation.

## Architecture and Design

- Defined clear CI, registry, GitOps, controller, and Kubernetes responsibility boundaries.
- Used separate application and GitOps repositories.
- Documented architecture decisions through ADRs.
- Applied deliberate scope control rather than adding unnecessary technologies.

## Reproducibility

- Documented clean-environment setup.
- Documented cluster creation and Argo CD bootstrap.
- Documented runtime-only secret creation.
- Documented health, traceability, and reconciliation validation.
- Documented cleanup and recreation of the local platform.

## Evidence-Driven Engineering

- Captured CI evidence.
- Captured registry evidence.
- Captured GitOps evidence.
- Captured Kubernetes evidence.
- Captured promotion evidence.
- Captured Git history evidence.
- Validated behavior through deliberate failure and recovery experiments.

## Cost and Scope Awareness

- Used kind to demonstrate Kubernetes and GitOps behavior without paid managed-cluster infrastructure.
- Kept the project focused on GitHub Actions, GHCR, Kustomize, Argo CD, Kubernetes, and software supply-chain controls.
- Deliberately excluded technologies that did not materially improve the project objective.

## Professional Capability Summary

This project demonstrates the ability to design, implement, secure, troubleshoot, document, and validate an end-to-end GitOps delivery platform.

The demonstrated workflow is:

```text
Source change
    ->
CI validation and container build
    ->
Security scanning and supply-chain evidence
    ->
Immutable GHCR artifacts
    ->
GitOps desired-state pull request
    ->
Argo CD reconciliation
    ->
Kubernetes deployment
    ->
Health, drift, recovery, promotion, and rollback validation
```
