# Git Workflow

## Branch Strategy

- main = protected stable branch
- feature/* = application and platform changes
- fix/* = bug fixes
- docs/* = documentation changes

## Commit Convention

Use Conventional Commit style:

- feat:
- fix:
- ci:
- docs:
- chore:
- refactor:
- test:
- security:

## Pull Request Policy

Changes should normally enter main through pull requests.

Pull requests must:

- pass required CI checks
- contain no secrets
- use reviewable commits
- describe the change clearly
- preserve GitOps separation

## Merge Policy

- No direct deployment from CI to Kubernetes
- No unvalidated change should reach main
- Deployment-state changes remain auditable in Git
- Prefer squash merge for focused feature branches
