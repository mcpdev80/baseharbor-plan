"""Read-only prototype for resolving an already published CI evidence archive.

This is NOT a trusted run/provenance verifier and never grants qualification.
"""
import argparse
import hashlib
import json
import pathlib
import re

HEX64 = re.compile(r"[0-9a-f]{64}\Z")
SAFE = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}\Z")
MAX_MANIFEST = 1024 * 1024
MAX_PAYLOAD = 8 * 1024 * 1024


class ArchiveError(ValueError):
    pass


def _read(path, maximum):
    if path.is_symlink() or not path.is_file():
        raise ArchiveError("missing or unsafe archive file")
    if path.stat().st_size > maximum:
        raise ArchiveError("archive file exceeds size bound")
    with path.open("rb") as stream:
        data = stream.read(maximum + 1)
    if len(data) > maximum:
        raise ArchiveError("archive file exceeds size bound")
    return data


def resolve(root, release, candidate_id, run_id, expected_digest):
    """Check archive byte integrity; no CI trust or current policy assessment."""
    if not all(SAFE.fullmatch(x) and x not in (".", "..") for x in (release, candidate_id, run_id)):
        raise ArchiveError("unsafe archive identity")
    if not HEX64.fullmatch(expected_digest):
        raise ArchiveError("invalid expected manifest digest")
    root = pathlib.Path(root)
    directory = root / "evidence" / release / candidate_id / run_id
    if any(part.is_symlink() for part in (root, root / "evidence", root / "evidence" / release,
                                         root / "evidence" / release / candidate_id, directory)):
        raise ArchiveError("unsafe archive directory")
    raw = _read(directory / "manifest.json", MAX_MANIFEST)
    if hashlib.sha256(raw).hexdigest() != expected_digest:
        raise ArchiveError("manifest digest mismatch")
    try:
        manifest = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise ArchiveError("invalid manifest JSON") from exc
    if not isinstance(manifest, dict) or manifest.get("schema") != "baseharbor.ci-evidence-archive/v1":
        raise ArchiveError("invalid manifest schema")
    if manifest.get("release") != release or not isinstance(manifest.get("checks"), list):
        raise ArchiveError("manifest identity or checks missing")
    if len(manifest["checks"]) > 128:
        raise ArchiveError("too many evidence checks")
    seen = set()
    for check in manifest["checks"]:
        if not isinstance(check, dict) or not isinstance(check.get("payload"), str):
            raise ArchiveError("invalid evidence entry")
        name = check["payload"]
        if (not name.startswith("payloads/") or name.count("/") != 1 or
                not SAFE.fullmatch(name.split("/")[1]) or name in seen):
            raise ArchiveError("unsafe or duplicate payload path")
        seen.add(name)
        digest = check.get("sha256")
        if not isinstance(digest, str) or not HEX64.fullmatch(digest):
            raise ArchiveError("invalid payload digest")
        content = _read(directory / name, MAX_PAYLOAD)
        if check.get("bytes") != len(content) or hashlib.sha256(content).hexdigest() != digest:
            raise ArchiveError("payload length or digest mismatch")
    return manifest


def main():
    parser = argparse.ArgumentParser(description="Read-only archive integrity check (not CI qualification)")
    parser.add_argument("root")
    parser.add_argument("release")
    parser.add_argument("candidate_id")
    parser.add_argument("run_id")
    parser.add_argument("expected_digest")
    args = parser.parse_args()
    try:
        manifest = resolve(args.root, args.release, args.candidate_id, args.run_id, args.expected_digest)
    except ArchiveError as exc:
        parser.exit(2, f"archive invalid: {exc}\n")
    print(json.dumps({"status": "integrity-only", "checks": len(manifest["checks"])}))


if __name__ == "__main__":
    main()
