# Cost and Deliberate Exclusions

## Purpose

This project demonstrates a production-oriented GitOps CI/CD operating model while keeping the portfolio lab inexpensive and focused.

The architecture intentionally uses a local Kubernetes runtime instead of paid managed Kubernetes infrastructure.

## Core Runtime Cost

The Kubernetes runtime is a local three-node kind cluster running under WSL2.

Therefore, the core Kubernetes compute cost for this lab is:

`$0`

The project does not require Amazon EKS worker nodes, NAT Gateways, Application Load Balancers, RDS, or other continuously billed AWS infrastructure.

## External Services

The project uses GitHub-hosted services for:

- source repositories
- GitHub Actions
- GitHub Container Registry
- pull requests
- workflow evidence
- build attestations

Actual GitHub usage limits or charges depend on the account and plan. This project does not claim that every external service is universally free.

## Why kind Was Chosen

kind provides a real Kubernetes API and multi-node local cluster while avoiding unnecessary cloud cost during portfolio development.

It is sufficient to demonstrate:

- Kubernetes workloads
- Argo CD reconciliation
- automated synchronization
- pruning
- self-healing
- deleted-resource recovery
- immutable image deployment
- Git-native rollback
- development and staging desired-state management

## Local Lab Boundary

The project is a portfolio lab and does not claim production high availability.

The local cluster does not provide the same resilience, networking, managed control plane, storage guarantees, identity integration, or operational service-level objectives as a managed production Kubernetes platform.

## Deliberate Exclusions

The following technologies are intentionally excluded from this project.

### Amazon EKS

EKS is not required to demonstrate the GitOps control model and would introduce cloud cost and additional infrastructure complexity.

A later Kubernetes/platform engineering project can demonstrate managed Kubernetes at greater depth.

### ECS and Fargate

ECS and Fargate were already covered in the AWS deployment project.

This project is specifically Kubernetes and GitOps focused.

### Terraform

Terraform was covered deeply in the Infrastructure as Code project.

This project keeps infrastructure provisioning separate from the GitOps application delivery lifecycle.

### Helm

Kustomize is used for environment configuration in this project.

Adding Helm would duplicate configuration-management concerns without improving the core GitOps learning objective.

### Flux

Argo CD is the selected GitOps controller.

Using two GitOps controllers in the same portfolio project would add duplication rather than architectural value.

### Jenkins

GitHub Actions is the selected CI system for this project.

Jenkins is reserved for the later Kubernetes/platform engineering project where dynamic Kubernetes build agents can be demonstrated.

### Argo Rollouts

Progressive delivery is valuable but outside the scope of this project.

The current project focuses on standard Kubernetes Deployments, GitOps reconciliation, failure visibility, and Git-native rollback.

### Prometheus and Grafana

Observability platforms are intentionally excluded from this CI/CD project.

They are better demonstrated in a dedicated Kubernetes/platform engineering context.

### Istio

A service mesh is not required for the project's CI/CD and GitOps objectives.

Introducing Istio would add networking and traffic-management complexity unrelated to the primary scope.

### Vault

The project demonstrates a runtime-only Kubernetes Secret strategy and keeps secrets out of Git.

A production-grade external secret-management platform such as Vault is intentionally outside this project's scope.

## Architectural Focus

The project is intentionally centered on:

- GitHub Actions for CI
- GHCR for immutable artifacts
- Trivy for vulnerability scanning
- CycloneDX SBOM generation
- build provenance attestations
- a separate GitOps desired-state repository
- Kustomize for environment configuration
- Argo CD for deployment and reconciliation
- kind for the local Kubernetes runtime
- Git-native promotion and rollback

## Scope Discipline

A senior architecture is not defined by the number of technologies included.

Each component should solve a clear problem and have a defined responsibility.

This project avoids adding tools only for resume keyword count.

## Cost Principle

The cost principle for this portfolio project is:

**Demonstrate the complete GitOps delivery and reconciliation lifecycle with real Kubernetes behavior while avoiding infrastructure spend that does not materially improve the learning objective.**
