# Git History Evidence

## Application Repository

```text
10a3698 (HEAD -> main, origin/main) docs: add environment promotion evidence
19aee1a docs: add Kubernetes runtime evidence
98034e6 docs: add GitOps deployment evidence
61e492e docs: add container registry evidence
752a5cb docs: add CI pipeline evidence
299a401 docs: add verified release evidence
3bf1dff feat: add release SHA traceability to GitOps state
cf4e0da fix: grant reusable GitOps workflow read permission
645d5f4 feat: automate development GitOps deployment proposals
2875c4d feat: add local Kubernetes and Argo CD platform configuration
48694fc feat: add GitOps deployment pull request workflow
2b7d2a4 ci: harden release security and supply chain controls
f07649d feat: add signed build provenance attestations
f85f319 fix: use valid pinned Trivy image version
1c8568d feat: add secure application build and release pipelines
```

## GitOps Repository

```text
23050bd (HEAD -> main, origin/main) Revert "Merge pull request #4 from awais-clouddev/test/bad-release"
4f57de7 Merge pull request #4 from awais-clouddev/test/bad-release
eb9e955 (origin/test/bad-release, test/bad-release) test: simulate bad development release
1c4b20a Merge pull request #2 from awais-clouddev/deploy/development-3bf1dffef919c85a7a74399ea16cacc403ce9f0b
94a26bc deploy: development 3bf1dffef919c85a7a74399ea16cacc403ce9f0b
4b26afa Merge pull request #1 from awais-clouddev/deploy/development-cf4e0dab5643627fef155a59e2914c98a6489c7c
b644364 feat: verify immutable artifact promotion integrity
e1e53a3 feat: promote development release to staging
b40a7a7 deploy: development cf4e0dab5643627fef155a59e2914c98a6489c7c
6306c7e feat: enable GitOps prune and self-healing
e6e99c0 feat: enable automatic Argo CD synchronization
11a921c feat: deploy immutable helpdesk release to development
d5c4271 feat: add helpdesk Kubernetes GitOps configuration
3a63641 chore: establish gitops environment repository foundation
```

## GitOps Pull Requests

```text
9	deploy: development 10a3698f7269857ab3863d07acedd8b130535a98	deploy/development-10a3698f7269857ab3863d07acedd8b130535a98	OPEN	2026-09-23T09:04:31Z
8	deploy: development 19aee1adf820483161aff17aba0281f98e002db1	deploy/development-19aee1adf820483161aff17aba0281f98e002db1	OPEN	2026-09-23T09:02:40Z
7	deploy: development 98034e6a1fb8eed54a099f206d6958d1b0004ba4	deploy/development-98034e6a1fb8eed54a099f206d6958d1b0004ba4	OPEN	2026-09-23T09:00:49Z
6	deploy: development 61e492ef387db3266615b8424f61282c645e3885	deploy/development-61e492ef387db3266615b8424f61282c645e3885	OPEN	2026-09-23T08:58:31Z
5	deploy: development 752a5cb014eb84e3fbd5daa97139dbd382b36a62	deploy/development-752a5cb014eb84e3fbd5daa97139dbd382b36a62	OPEN	2026-09-23T08:56:13Z
4	test: simulate bad development release	test/bad-release	MERGED	2026-09-23T08:03:52Z
3	deploy: development 299a4010f29a3ffbdd1bb1981a18b07391f0bfda	deploy/development-299a4010f29a3ffbdd1bb1981a18b07391f0bfda	OPEN	2026-09-23T08:00:18Z
2	deploy: development 3bf1dffef919c85a7a74399ea16cacc403ce9f0b	deploy/development-3bf1dffef919c85a7a74399ea16cacc403ce9f0b	MERGED	2026-09-23T07:41:23Z
1	deploy: development cf4e0dab5643627fef155a59e2914c98a6489c7c	deploy/development-cf4e0dab5643627fef155a59e2914c98a6489c7c	MERGED	2026-09-23T07:30:13Z
```

## Evidence Summary

- Application and GitOps changes are recorded as Git commits.
- Automated deployment proposals are represented as GitOps pull requests.
- The bad-release test and Git-native rollback are preserved in Git history.
- Environment promotion is recorded as a GitOps commit.
