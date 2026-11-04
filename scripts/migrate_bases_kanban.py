#!/usr/bin/env python3
"""Idempotently add the native writable lane and concise authored preview to tasks."""
import re
from plan import ROOT, Vault, dump_value, kanban_summary, view_state

def migrate(root=ROOT):
    vault = Vault(root).load()
    changed = []
    for task in sorted(vault.tasks.values(), key=lambda t: str(t["path"])):
        path = task["path"]
        original = path.read_text(encoding="utf-8")
        insert = []
        if not re.search(r"(?m)^kanban_lane:", original):
            insert.append("kanban_lane: " + view_state(vault, task))
        if not re.search(r"(?m)^kanban_summary:", original):
            insert.append("kanban_summary: " + dump_value(kanban_summary(task)))
        if not insert:
            continue
        result = re.sub(r"(?m)^(kanban_status:.*)$",
                        lambda m: m.group(1) + "\n" + "\n".join(insert),
                        original, count=1)
        if result == original:
            raise ValueError(f"missing kanban_status in {path}")
        path.write_text(result, encoding="utf-8")
        changed.append(str(path.relative_to(root)))
    print(f"migrated {len(changed)} tasks with native Ready lanes and summaries")
    return changed

if __name__ == "__main__":
    migrate()
