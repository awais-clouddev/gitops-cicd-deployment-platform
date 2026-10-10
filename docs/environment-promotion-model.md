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
- The development overlay is actively reconciled by the committed Argo CD Application.
- Staging is maintained as a separate promotion target and validated Kustomize overlay; this repository does not currently define a staging Argo CD Application.
- CI does not deploy directly to Kubernetes.
