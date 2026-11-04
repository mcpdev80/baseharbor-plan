#!/usr/bin/env python3
"""One-time, repeatable migration of canonical tasks to native Obsidian Bases.

Only adds the writable kanban_status property and derived kanban_title.
Existing tasks, lifecycle markers, and agent ownership remain intact.
"""
from pathlib import Path
import re

from plan import ROOT, Vault, dump_value

def migrate(root=ROOT):
    vault = Vault(root).load()
    updated = []
    for task in sorted(vault.tasks.values(), key=lambda t: str(t["path"])):
        path = task["path"]
        text = path.read_text(encoding="utf-8")
        if re.search(r"(?m)^kanban_status:", text):
            continue
        status = task["status"]
        if status not in ("backlog", "planned", "active", "review", "blocked", "closed"):
            raise ValueError(f"invalid source status in {path}: {status!r}")
        new = re.sub(
            r"(?m)^(owner:.*)$",
            lambda match: (
                match.group(1) + "\n"
                + "kanban_status: " + status + "\n"
                + "kanban_title: " + dump_value(task["title"])
            ),
            text,
            count=1,
        )
        if new == text:
            raise ValueError(f"missing owner frontmatter: {path}")
        path.write_text(new, encoding="utf-8")
        updated.append(str(path.relative_to(root)))
    print(f"migrated {len(updated)} task notes to native Bases")
    return updated

if __name__ == "__main__":
    migrate()
