#!/usr/bin/env python3

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--api-digest", required=True)
    parser.add_argument("--frontend-digest", required=True)
    args = parser.parse_args()

    path = Path(args.file)

    if not path.exists():
        raise SystemExit(f"GitOps file not found: {path}")

    text = path.read_text()

    marker = "\nimages:\n"

    if marker in text:
        text = text.split(marker)[0].rstrip() + "\n"

    text += f"""
images:
  - name: ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-api
    newName: ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-api
    digest: {args.api_digest}

  - name: ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-frontend
    newName: ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-frontend
    digest: {args.frontend_digest}
"""

    path.write_text(text)

    print(f"Updated: {path}")
    print(f"API digest: {args.api_digest}")
    print(f"Frontend digest: {args.frontend_digest}")


if __name__ == "__main__":
    main()
