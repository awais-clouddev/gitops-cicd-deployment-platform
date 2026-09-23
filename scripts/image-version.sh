#!/usr/bin/env bash
set -euo pipefail

SHA="${GITHUB_SHA:-$(git rev-parse HEAD)}"

echo "IMAGE_TAG=sha-${SHA}"
echo "API_IMAGE=ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-api:sha-${SHA}"
echo "FRONTEND_IMAGE=ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-frontend:sha-${SHA}"
