#!/usr/bin/env python3
"""Capture or compare the read-only GitHub source snapshot used for the migration.

The snapshot is historical evidence, not maintained planning. Requires an
authenticated `gh` CLI.

    python3 scripts/snapshot.py capture   # rewrite migration/source-snapshot/
    python3 scripts/snapshot.py diff      # compare live GitHub with the snapshot
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SNAPSHOT = ROOT / "migration" / "source-snapshot"
OWNER = "mcpdev80"
REPOS = ["baseharbor", "baseharbor-demo", "baseharbor-console", "baseharbor-node-connector"]


def gh_paginate(path):
    out = subprocess.run(
        ["gh", "api", "--paginate", path, "--jq", ".[]"],
        check=True, capture_output=True, text=True,
    ).stdout
    decoder = json.JSONDecoder()
    items, idx = [], 0
    while idx < len(out):
        while idx < len(out) and out[idx].isspace():
            idx += 1
        if idx >= len(out):
            break
        obj, idx = decoder.raw_decode(out, idx)
        items.append(obj)
    return items


def issue_record(repo, issue):
    comments = []
    if issue["comments"]:
        for c in gh_paginate(f"repos/{OWNER}/{repo}/issues/{issue['number']}/comments?per_page=100"):
            comments.append({
                "author": c["user"]["login"],
                "created_at": c["created_at"],
                "updated_at": c["updated_at"],
                "url": c["html_url"],
                "body": c["body"],
            })
    return {
        "source": f"{OWNER}/{repo}#{issue['number']}",
        "number": issue["number"],
        "url": issue["html_url"],
        "title": issue["title"],
        "state": issue["state"],
        "author": issue["user"]["login"],
        "labels": [l["name"] for l in issue["labels"]],
        "milestone": (issue.get("milestone") or {}).get("title"),
        "assignees": [a["login"] for a in issue["assignees"]],
        "created_at": issue["created_at"],
        "updated_at": issue["updated_at"],
        "body": issue["body"] or "",
        "comments": comments,
    }


def live_inventory():
    issues, prs = {}, {}
    for repo in REPOS:
        for item in gh_paginate(f"repos/{OWNER}/{repo}/issues?state=open&per_page=100"):
            if "pull_request" in item:
                prs[f"{OWNER}/{repo}#{item['number']}"] = item
            else:
                issues[f"{OWNER}/{repo}#{item['number']}"] = (repo, item)
    return issues, prs


def pr_record(source, item):
    repo = source.split("/")[1].split("#")[0]
    pr = json.loads(subprocess.run(
        ["gh", "api", f"repos/{OWNER}/{repo}/pulls/{item['number']}"],
        check=True, capture_output=True, text=True).stdout)
    return {
        "source": source,
        "url": pr["html_url"],
        "title": pr["title"],
        "draft": pr["draft"],
        "base": pr["base"]["ref"],
        "head": pr["head"]["ref"],
        "head_sha": pr["head"]["sha"],
        "updated_at": pr["updated_at"],
    }


def capture():
    issues, prs = live_inventory()
    entries = []
    for source in sorted(issues, key=sort_key):
        repo, item = issues[source]
        record = issue_record(repo, item)
        path = SNAPSHOT / repo / f"{item['number']}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        data = json.dumps(record, indent=2, ensure_ascii=False) + "\n"
        path.write_text(data, encoding="utf-8")
        entries.append({
            "source": source,
            "title": record["title"],
            "updated_at": record["updated_at"],
            "comments": len(record["comments"]),
            "file": str(path.relative_to(ROOT)),
            "sha256": hashlib.sha256(data.encode("utf-8")).hexdigest(),
        })
    inventory = {
        "captured_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repositories": [f"{OWNER}/{r}" for r in REPOS],
        "open_issues": entries,
        "open_pull_requests": [pr_record(s, prs[s]) for s in sorted(prs, key=sort_key)],
    }
    (SNAPSHOT / "inventory.json").write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"captured {len(entries)} open issues and {len(prs)} open pull requests")


def diff():
    inventory = json.loads((SNAPSHOT / "inventory.json").read_text(encoding="utf-8"))
    known = {e["source"]: e for e in inventory["open_issues"]}
    known_prs = {p["source"]: p for p in inventory["open_pull_requests"]}
    issues, prs = live_inventory()
    changes = []
    for source in sorted(set(issues) - set(known), key=sort_key):
        changes.append(f"NEW issue      {source}  {issues[source][1]['title']}")
    for source in sorted(set(known) - set(issues), key=sort_key):
        changes.append(f"NO LONGER OPEN {source}  {known[source]['title']}")
    for source in sorted(set(known) & set(issues), key=sort_key):
        if issues[source][1]["updated_at"] != known[source]["updated_at"]:
            changes.append(f"UPDATED        {source}  {known[source]['updated_at']} -> {issues[source][1]['updated_at']}")
    for source in sorted(set(prs) - set(known_prs), key=sort_key):
        changes.append(f"NEW PR         {source}  {prs[source]['title']}")
    for source in sorted(set(known_prs) - set(prs), key=sort_key):
        changes.append(f"PR CLOSED      {source}  {known_prs[source]['title']}")
    for source in sorted(set(known_prs) & set(prs), key=sort_key):
        if prs[source]["updated_at"] != known_prs[source]["updated_at"]:
            changes.append(f"PR UPDATED     {source}  {known_prs[source]['updated_at']} -> {prs[source]['updated_at']}")
    print(f"snapshot captured_at {inventory['captured_at']}")
    print("\n".join(changes) if changes else "no changes since the snapshot")
    return 1 if changes else 0


def sort_key(source):
    repo, num = source.split("#")
    return (REPOS.index(repo.split("/")[1]), int(num))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["capture", "diff"])
    args = parser.parse_args()
    if args.command == "capture":
        capture()
        return 0
    return diff()


if __name__ == "__main__":
    sys.exit(main())
