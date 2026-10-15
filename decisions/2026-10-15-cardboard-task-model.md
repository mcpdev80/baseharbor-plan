---
id: 2026-10-15-cardboard-task-model
status: proposed
sources: []
---

# One CardBoard card per task note, lifecycle on the card line

## Context

CardBoard 0.7.9 (settings format 0.13.0) shows non-indented Markdown checkboxes anywhere in the vault as cards and builds columns from `#tags`. Indented items become card subtasks/notes; frontmatter `tags` apply to every task in a note; tags may not contain `.`; cards cannot be dragged between columns (drag and drop exists only for board tabs and column headers). Marking a card done appends `@completed(<timestamp>)` and does not touch other tags. CardBoard does not evaluate dependencies.

## Decision

- Each task note has exactly one top-level checkbox, the **card line**: `- [ ] <id> · <title> #task #release/<r> #status/<s>`. No other checkboxes in task notes; acceptance criteria are plain bullets. Releases, epics, decisions, templates, views, migration and scripts are excluded from CardBoard by global path filters.
- **The status tag on the card line is the only lifecycle state.** Open states: `#status/backlog`, `#status/planned`, `#status/active` (claimed, being implemented), `#status/blocked`, `#status/review` (implementation ready for review). The terminal state is `#status/closed`; CardBoard additionally needs the box checked to show the card as completed, so the validator enforces *checked ⇔ `#status/closed`* — one state, mirrored once, never two independent values. A closed card requires `resolution` (`accepted`, `superseded`, `dropped`) and `evidence` links in the frontmatter. YAML holds metadata (owner, release, dependencies, PRs, sources), never a second status.
- Why a terminal tag instead of "checked and untagged": CardBoard's Completed column only shows a completed card that would otherwise belong to one of the board's columns (`Column/Completed.elm`), so an untagged closed card would vanish from status boards.
- **Ready**, **queued** and **waiting** are derived by `scripts/plan.py` from `#status/planned`, whether all dependencies are accepted and whether the task's release is `active` (or the task has `early: true`); they are shown in generated views, not stored.
- Three distinct facts: *ready for review* (`#status/review`), *task accepted* (checked + `resolution: accepted` + evidence), *release qualified* (release note `status: qualified` + evidence). Checking a box is not proof of acceptance; the validator rejects a checked card without evidence or with any status tag other than `#status/closed`.
- The `#release/<r>` tag on the card mirrors the `release` field so release boards work; the validator keeps both equal.

## Consequences

Moving a card means editing its status tag in the note (CardBoard has no drag and drop for cards). Readiness needs `python3 scripts/plan.py list --ready` or the generated [overview](../views/overview.md).
