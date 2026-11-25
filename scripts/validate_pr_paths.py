#!/usr/bin/env python3
"""Reject planning PR changes outside evidence and card-work paths."""

from __future__ import annotations

import re
import subprocess
import sys


POLICY_IMPLEMENTATION_PATHS = {
    ".github/workflows/validate.yml",
    "scripts/validate_pr_paths.py",
    "scripts/tests/test_validate_pr_paths.py",
}
CONTENT_PREFIXES = ("evidence/", "tasks/", "releases/")


def allowed_change(status: str, path: str) -> bool:
    """Allow evidence, card work, exact validator files, and root cleanup deletes."""
    if path.startswith(CONTENT_PREFIXES):
        return True
    if path in POLICY_IMPLEMENTATION_PATHS:
        return True
    # One-time cleanup is safe: it removes the collision source and cannot add
    # another root artifact. New or modified root files are always rejected.
    return status == "D" and path == "akte.md"


def changed_files(base_sha: str) -> list[tuple[str, str]]:
    if not re.fullmatch(r"[0-9a-f]{40}", base_sha):
        raise ValueError("base SHA must be a full 40-character lowercase Git SHA")
    have = subprocess.run(
        ["git", "cat-file", "-e", f"{base_sha}^{{commit}}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if have.returncode:
        subprocess.run(["git", "fetch", "--no-tags", "origin", base_sha], check=True)
    result = subprocess.run(
        ["git", "diff", "--name-status", "--no-renames", f"{base_sha}...HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    changes: list[tuple[str, str]] = []
    for line in result.stdout.splitlines():
        status, path = line.split("\t", 1)
        changes.append((status, path))
    return changes


def violations(changes: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return [(status, path) for status, path in changes if not allowed_change(status, path)]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_pr_paths.py <base-sha>", file=sys.stderr)
        return 2
    try:
        changes = changed_files(sys.argv[1])
    except (ValueError, subprocess.CalledProcessError) as error:
        print(f"planning PR path validation could not inspect diff: {error}", file=sys.stderr)
        return 2

    bad = violations(changes)
    if bad:
        print("planning PR changed files outside evidence/ and card-work paths:", file=sys.stderr)
        for status, path in bad:
            print(f"{status}\t{path}", file=sys.stderr)
        return 1

    print(f"planning PR path scope accepted: {len(changes)} changed paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
