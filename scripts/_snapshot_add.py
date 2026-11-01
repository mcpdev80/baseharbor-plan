#!/usr/bin/env python3
"""Add freshly-fetched issues #1251 and #1253 to the planning source snapshot.

The snapshot (migration/source-snapshot/inventory.json) was captured 2026-10-15
and predates these two items. `scripts/plan.py check` requires every `sources[]`
reference to point at an inventoried issue and every inventoried issue to be
accounted for by a card. #1251 (merged PR) and #1253 (open issue) are now
referenced by planning cards but were not captured. This fetches them live and
records per-issue JSON + inventory entries so the validator sees them.
"""
import json
import hashlib
import urllib.request

SNAP = "migration/source-snapshot"
REPO_DIR = f"{SNAP}/baseharbor"
NUMBERS = [1251, 1253]
REPO = "mcpdev80/baseharbor"

def fetch(number):
    url = f"https://api.github.com/repos/{REPO}/issues/{number}"
    req = urllib.request.Request(url, headers={"User-Agent": "plan-snapshot"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def build_json(number, data):
    obj = {
        "source": f"{REPO}#{number}",
        "number": number,
        "url": f"https://github.com/{REPO}/issues/{number}",
        "title": data["title"],
        "state": data["state"],
        "author": data.get("user", {}).get("login", ""),
        "labels": [lb["name"] for lb in data.get("labels", [])],
        "milestone": data.get("milestone", {}).get("title") if data.get("milestone") else None,
        "assignees": [a["login"] for a in data.get("assignees", [])],
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
        "body": data.get("body") or "",
        "comments": [c["body"] for c in (data.get("comments") or [])],
    }
    return obj

with open(f"{SNAP}/inventory.json") as f:
    inventory = json.load(f)

existing = {e["source"] for e in inventory["open_issues"]}

for number in NUMBERS:
    source = f"{REPO}#{number}"
    if source in existing:
        print(f"{source} already inventoried; skipping")
        continue
    data = fetch(number)
    obj = build_json(number, data)
    path = f"{REPO_DIR}/{number}.json"
    text = json.dumps(obj, indent=2, ensure_ascii=False)
    # Digest is over the exact bytes on disk (as check_sources reads raw bytes).
    file_bytes = (text + "\n").encode("utf-8")
    with open(path, "wb") as f:
        f.write(file_bytes)
    sha256 = hashlib.sha256(file_bytes).hexdigest()
    entry = {
        "source": source,
        "title": data["title"],
        "updated_at": data["updated_at"],
        "comments": data.get("comments", 0) if isinstance(data.get("comments"), int) else len(data.get("comments") or []),
        "file": path,
        "sha256": sha256,
    }
    inventory["open_issues"].append(entry)
    print(f"added {source}: file={path} sha256={sha256[:16]}... comments={entry['comments']}")
    existing.add(source)
    data_updated = data["updated_at"]

# bump capture metadata
inventory["live_rechecked_at"] = data_updated
with open(f"{SNAP}/inventory.json", "w", encoding="utf-8") as f:
    json.dump(inventory, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("inventory.json updated")
