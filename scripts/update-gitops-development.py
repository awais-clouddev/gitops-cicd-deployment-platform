#!/usr/bin/env python3

import argparse
import re
import yaml
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--api-digest", required=True)
    parser.add_argument("--frontend-digest", required=True)
    parser.add_argument("--release-sha", required=True)
    args = parser.parse_args()

    path = Path(args.file)

    if not path.exists():
        raise SystemExit(f"GitOps file not found: {path}")

    for value in (args.api_digest, args.frontend_digest):
        if not re.fullmatch(r"sha256:[a-f0-9]{64}", value):
            raise SystemExit(f"Invalid image digest: {value}")

    if not re.fullmatch(r"[a-f0-9]{40}", args.release_sha):
        raise SystemExit("Invalid release SHA")

    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise SystemExit("Invalid Kustomization YAML")

    images = data.get("images")
    if not isinstance(images, list):
        raise SystemExit("Missing images list")

    expected = {
        "ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-api": args.api_digest,
        "ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-frontend": args.frontend_digest,
    }
    found = set()
    for item in images:
        if item.get("name") in expected:
            name = item["name"]
            item["digest"] = expected[name]
            found.add(name)

    if found != set(expected):
        raise SystemExit("Missing expected API or frontend image")

    data.setdefault("commonAnnotations", {})[
        "gitops.platform/release-sha"
    ] = args.release_sha

    path.write_text(yaml.safe_dump(data, sort_keys=False))

    print(f"Updated: {path}")
    print(f"API digest: {args.api_digest}")
    print(f"Frontend digest: {args.frontend_digest}")
    print(f"Release SHA: {args.release_sha}")


if __name__ == "__main__":
    main()
