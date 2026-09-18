# Environment and Promotion Model

## Environments

Project 5 will use:

- development
- staging

## Promotion Flow

development
→ validate
→ promote approved immutable artifact
→ staging

## Rules

- Build the container artifact once.
- Do not rebuild when promoting between environments.
- Promote the same immutable image digest.
- Git controls environment state.
- Argo CD reconciles each environment from Git.
- CI does not deploy directly to Kubernetes.
