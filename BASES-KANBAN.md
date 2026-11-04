# BaseHarbor native Obsidian Kanban

Open [BaseHarbor.base](BaseHarbor.base) with Obsidian 1.15+ and the core Bases plugin.

Each task Markdown note is one card. `kanban_status` is the writable lifecycle source of truth. Dragging a card edits this property. The original task checkbox and `#status/...` tag are compatibility output updated by `python3 scripts/plan.py render`; don't edit the tag independently. Legacy notes without this property continue to work.

Columns: backlog, planned, active, review, blocked, closed. Dependency-derived ready/waiting/queued remain read-only; Ready is a separate table filtered through `#view/ready`.

Active requires owner. Review requires owner and prs. Blocked requires blocker text. Closed requires resolution (accepted, superseded, dropped) and real HTTPS evidence. Superseded requires superseded_by. Dragging to Closed alone is not acceptance.

After dragging, run `python3 scripts/plan.py render && python3 scripts/plan.py check`, then commit/push. Existing validation remains authoritative. To reopen a closed task, clear resolution before validating. Legacy CardBoard configuration is kept for rollback; native Bases does not depend on that plugin.

https://obsidian.md/help/bases/syntax
https://obsidian.md/help/bases/views/kanban
