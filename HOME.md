# BaseHarbor planning home

> **Temporary development pause:** [Horde/Codex handover pause](decisions/2026-10-18-horde-codex-handover-pause.md). Exact PR snapshots, unresolved native failures, paused ownership and restart requirements are recorded there. No automatic task takeover or implementation during the handover test.

**Current release:** [v0.4.26](releases/v0.4.26.md) — app wizard, capability editing and development/CI V1 (epic [core-888](epics/core-888-development-and-ci.md)). Next: [v0.4.27](releases/v0.4.27.md). Sequence: [ROADMAP.md](ROADMAP.md).

> Planning authority: this repository on `main`. Source GitHub issues retain discussion/history. [Activation and remaining cleanup](migration/cutover-checklist.md).

## Current work and blockers

The live state is generated from the task notes, so it is never maintained by hand here:

- [views/ready.md](views/ready.md) — tasks whose actual prerequisites are accepted; ready is not assignment.
- [views/overview.md](views/overview.md) — active, review, blocked and ready tasks; counts per release.
- [views/releases/v0.4.26.md](views/releases/v0.4.26.md) — the current release's tasks with derived state.
- [views/epics.md](views/epics.md) — tasks per epic.
- Command line: `python3 scripts/plan.py list --status active`, `--status blocked`, `--ready`.

In Obsidian: CardBoard boards **Current · v0.4.26**, **v0.4.27**, **Next** and **Attention**. Current now has separate **Planned** (waiting for prerequisites) and **Ready** (available to assign) columns. Ready is generated from task dependencies and release status on every planning render; it is not a manually maintained list.

## Navigation

| Release | Note | Tasks |
| --- | --- | --- |
| v0.4.26 | [release](releases/v0.4.26.md) | [view](views/releases/v0.4.26.md) |
| v0.4.27 | [release](releases/v0.4.27.md) | [view](views/releases/v0.4.27.md) |
| v0.4.28 | [release](releases/v0.4.28.md) | [view](views/releases/v0.4.28.md) |
| v0.4.29 | [release](releases/v0.4.29.md) | [view](views/releases/v0.4.29.md) |
| v0.4.30 | [release](releases/v0.4.30.md) | [view](views/releases/v0.4.30.md) |
| v0.4.31 | [release](releases/v0.4.31.md) | [view](views/releases/v0.4.31.md) |
| v0.4.x (unscheduled) | [series](releases/v0.4.x.md) | [view](views/releases/v0.4.x.md) |
| v0.5.x | [series](releases/v0.5.x.md) | [view](views/releases/v0.5.x.md) |
| v0.7.x | [series](releases/v0.7.x.md) | [view](views/releases/v0.7.x.md) |
| v0.8.x | [series](releases/v0.8.x.md) | [view](views/releases/v0.8.x.md) |
| Backlog | [note](releases/backlog.md) | [view](views/releases/backlog.md) |
| Maintenance | [note](releases/maintenance.md) | [view](views/releases/maintenance.md) |
| Triage (no release decision) | [note](releases/triage.md) | [view](views/releases/triage.md) |

Decisions: [decisions/](decisions/). Process: [WORKFLOW.md](WORKFLOW.md). Product rules: [BaseHarbor development guidelines](https://github.com/mcpdev80/baseharbor/blob/develop/docs/DEVELOPMENT_GUIDELINES.md).

## Roadmap and topic badges

CardBoard **Roadmap** shows one generated card per release/series: current, next, later and qualified/published. Cards link to scope and tasks; accepted-task counts never qualify a release. Markdown equivalent: [roadmap/cards.md](roadmap/cards.md). No dates are invented.

Task cards show `#area/…` and `#kind/…` badges with the `baseharbor-board` CSS snippet enabled. Maintain `areas: [ci]` (lowercase slugs) and the existing `type` in task frontmatter, then run `python3 scripts/plan.py render`. Routing tags stay hidden. Pull with CardBoard disabled, then enable it again to reload shared board settings without overwriting them with cached settings.

Current shows **all Planned tasks**, including tasks waiting for prerequisites. Readiness is a card detail; **Next** remains the filtered assignment view. Planning completeness and execution readiness are distinct.

## Release operations

Every concrete scheduled version has visible [release lifecycle cards](RELEASE_WORKFLOW.md): cleanup → Renovate intake → complete preparation → authorized pre-release → promotion/tagging commands → verified publication. Cards appear in the existing release boards; no second lifecycle board or duplicate state.

The already-running v0.4.26 has only preparation, pre-release approval, publication/tagging and post-release verification; its startup is not replayed. All six stages apply to subsequent releases.

The dedicated **v0.4.27** board includes every release task and recurring release card. Columns separate Planned (unfinished prerequisites), Queued (prerequisites accepted, release not started), Ready, Active, Review, Blocked and Closed. It does not change assignment or release status.
