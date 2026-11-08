# baseharbor-plan

**Native Obsidian Kanban:** [BaseHarbor.base](BaseHarbor.base) (Obsidian 1.14+) — [Bedienung und sichere Statuswechsel](BASES-KANBAN.md). CardBoard is no longer required.

Planning for [BaseHarbor](https://github.com/mcpdev80/baseharbor): roadmap, releases, epics, tasks, decisions and handoffs as plain Markdown. Code, PRs, reviews, CI execution and releases stay in the product repositories. Starting with v0.4.27, bounded sanitized CI evidence is also automatically archived under this planning repository's `evidence/` tree; source artifacts and trusted CI authorities remain in the product repositories.

> **Status: planning authority on `main`.** Maintain scope, dependencies, ownership and handoffs here. Source GitHub issues retain discussion/history. See the [activation record](migration/cutover-checklist.md); actual Obsidian UI behavior remains unverified.

## Start here

- [HOME.md](HOME.md) — current release, navigation and generated views.
- [ROADMAP.md](ROADMAP.md) — release sequence.
- [WORKFLOW.md](WORKFLOW.md) — task model, lifecycle, ownership protocol, intake.
- [AGENTS.md](AGENTS.md) — entry point for coding agents.
- [views/overview.md](views/overview.md) — read-only overview of all tasks (works on GitHub without Obsidian).

## Use without Obsidian

Everything is Markdown with relative links. Python 3.9+ (standard library only):

```bash
python3 scripts/plan.py check            # validate the vault (CI runs this)
python3 scripts/plan.py list --ready     # tasks whose dependencies are accepted
python3 scripts/plan.py show core-912    # one task with derived state
python3 scripts/plan.py render           # refresh generated links and views
python3 -m unittest discover -s scripts/tests
```

## Open the vault in Obsidian

1. Clone the repository and open its directory as an Obsidian vault.
2. Use **BaseHarbor.base** (native Obsidian Bases Kanban, Obsidian 1.15+). This is the current board; the historical CardBoard plugin is not needed.
3. Move a card by editing/dragging the native Kanban property `kanban_lane` in Obsidian. The canonical lifecycle is `kanban_status`; see [BASES-KANBAN.md](BASES-KANBAN.md) for conflict reconciliation, Wait vs Blocked, ownership and acceptance rules.
4. Run `python3 scripts/plan.py render && python3 scripts/plan.py check` after changes, review the diff, then commit and push. Generated views, card previews and compatibility tags are not maintained by hand.
5. The optional Obsidian Git plugin can synchronize changes; it is not a workflow/acceptance gate. The old CardBoard configuration is rollback-only.

## Repository map

| Path | Content |
| --- | --- |
| `releases/` | One note per release or release series |
| `epics/` | Coordination notes |
| `tasks/` | One note per executable task |
| `decisions/` | Short decisions with rationale |
| `templates/` | Note templates (`scripts/plan.py new` uses `templates/task.md`) |
| `views/` | Generated summaries — do not edit |
| `migration/` | Source inventory, snapshot, manifest, coverage, cutover checklist |
| `scripts/` | Validator/generator, snapshot tool and tests |

## Roadmap and topic badges

CardBoard **Roadmap** shows one generated card per release/series: current, next, later and qualified/published. Cards link to scope and tasks; accepted-task counts never qualify a release. Markdown equivalent: [roadmap/cards.md](roadmap/cards.md). No dates are invented.

Task cards show `#area/…` and `#kind/…` badges with the `baseharbor-board` CSS snippet enabled. Maintain `areas: [ci]` (lowercase slugs) and the existing `type` in task frontmatter, then run `python3 scripts/plan.py render`. Routing tags stay hidden. Pull with CardBoard disabled, then enable it again to reload shared board settings without overwriting them with cached settings.
