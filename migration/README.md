# Migration from GitHub issues

**Status: migration candidate, not yet cut over.** The GitHub issues and any GitHub Projects remain the planning authority until the Maintainer approves the concrete [cutover checklist](cutover-checklist.md). Nothing in the product repositories has been closed, edited or re-linked by this migration.

## What is here

| File | Purpose |
| --- | --- |
| [source-snapshot/](source-snapshot/inventory.json) | **Source snapshot, not maintained planning.** Verbatim JSON of every open issue (body + all comments) at capture time, plus the open-PR inventory. Used for lossless verification. Original language kept (partly German). |
| [manifest.json](manifest.json) | Generated machine-readable mapping: one entry per inventoried open issue with disposition and destination(s). |
| [coverage.md](coverage.md) | Generated coverage report (counts per repository, dispositions, source → destination table). |
| [pull-requests.md](pull-requests.md) | Open PRs inspected separately; they stay in their code repositories. |
| [external-tooling.md](external-tooling.md) | Bot-owned issues that stay on GitHub (Renovate dashboard). |
| [conflicts.md](conflicts.md) | Conflicting or missing information found during migration, with the applied interpretation. |
| [notices.md](notices.md) | Proposed short notices for the old issues (not posted). |
| [entry-point-updates.md](entry-point-updates.md) | Proposed minimal changes to product-repository entry points (not applied). |
| [cutover-checklist.md](cutover-checklist.md) | Steps that need Maintainer approval, including the transition for running sessions and rollback. |

## Scope inspected

- In scope (all public, all accessible): `mcpdev80/baseharbor`, `mcpdev80/baseharbor-demo`, `mcpdev80/baseharbor-console`, `mcpdev80/baseharbor-node-connector`. These are the ecosystem repositories named in BaseHarbor's `AGENTS.md` and release-readiness rules.
- Not in scope: the other repositories of the `mcpdev80` account (unrelated projects such as MAILFLOW-AI_MAILING, terraform-aws-eks-blueprints, SafeMarket and older experiments). No inaccessible or private in-scope repository was found.
- BaseHarbor Project #4 is known from the Maintainer's authenticated CLI output. Its current settings cannot be inspected or changed through this connector. Only that project is in scope for retirement; unrelated projects remain untouched.

## How the mapping works

Every destination note lists its sources in `sources:` frontmatter (`owner/repo#number`). `scripts/plan.py check` fails if any inventoried open issue has no destination, if a destination cites an issue not in the inventory, or if a snapshot file does not match its recorded SHA-256. Dispositions: `task`, `split` (one source, several tasks — only baseharbor#893), `release` (release umbrellas and series parents), `epic`, `roadmap` (#155), `external-tooling` (#889), `duplicate` (a source listed in a task's `aliases`; none found in this migration). A note may list several sources; the first is primary, the others are marked additional.

Maintained notes are English. Where a source was German, the note is a translation of the planning content; archived third-party texts (the evaluations in #887) are not translated and stay in the snapshot. Long English sources were condensed only where noted, and every acceptance criterion was kept.

## Refreshing

```bash
python3 scripts/snapshot.py diff      # what changed on GitHub since the snapshot (needs gh auth)
python3 scripts/snapshot.py capture   # re-capture after updating the affected notes
python3 scripts/plan.py render && python3 scripts/plan.py check
```

Run `diff` immediately before proposing the cutover and reconcile every reported change in the notes first.

## Privacy

The in-scope repositories are public and the snapshot contains only content already published in their issues. A scan for credentials (tokens, keys, private-key blocks, password assignments) found none. Two LAN addresses of lab VMs (in node-connector#3) and a local backup path (in baseharbor#909) appear verbatim in the snapshot because they are in the public issues; the maintained notes omit them.
