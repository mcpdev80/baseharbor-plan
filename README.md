# baseharbor-plan

Planning for [BaseHarbor](https://github.com/mcpdev80/baseharbor): roadmap, releases, epics, tasks, decisions and handoffs as plain Markdown. Code, PRs, reviews, CI, evidence and releases stay in the product repositories.

> **Status: migration candidate.** Until the Maintainer approves the cutover, the GitHub issues in the product repositories remain authoritative. See [migration/README.md](migration/README.md).

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

1. Clone this repository and open the folder as a vault ("Open folder as vault").
2. Settings → Community plugins → turn off Restricted mode → Browse, then install and enable:
   - **CardBoard** (`card-board`, by roovo) — verified with 0.7.9.
   - **Git** (`obsidian-git`, by Vinzent03) — verified with 2.41.1.
3. The shared settings are already in the repository: CardBoard boards (`.obsidian/plugins/card-board/data.json`) and Obsidian Git with **manual** commit/pull/push only (`.obsidian/plugins/obsidian-git/data.json`). Plugin binaries, workspace layout and personal settings are not committed (see `.gitignore`).
4. Open CardBoard from the ribbon icon. Boards: **Current · v0.4.26**, **Attention** (blocked/review/active), **Releases** (one column per release), **Backlog**.
5. Commit and push deliberately with the Git plugin's commands (or the command line). Pull before you start; never force-push.

CardBoard reads only top-level checkboxes in `tasks/`. To move a card to another column, edit its `#status/…` tag in the note; CardBoard 0.7.9 has no card drag and drop.

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
