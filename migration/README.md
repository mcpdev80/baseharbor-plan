# Migration from GitHub issues

## Executed cutover — 2026-10-15

- Planning PR #1 merged and authority activated at `47474109ea69475e60be4f065ad17476c71665bb`.
- Entry-point PRs merged: BaseHarbor #937 (`1b2f57e063ae4d1c691af087c697d54df885507b`), Console #5 (`1d014c0b1eb5fd3be79b1ea859abecd59ec3d504`), Demo #114 (`85c0db5a6f078c0331e802765d018939caaf07f4`), Connector #6 (`c33ef10fdebd4833193dee66fb0a4894e0d5b058`).
- BaseHarbor #938 merged at `242a01bb398e35ad2dc5a803c9831fd3751b6eb1`: remove contradictory old planning statements and update the existing roadmap audit assertion. The independently merged runner #932 was preserved.
- 86 planning issues relocated and closed as `not_planned`, each with `planning/moved`, all destination links, activation SHA and explicit “migrated, not implemented/accepted/cancelled” notice. Original bodies were verified against the immutable source snapshot; discussions remain available.
- Final authenticated verification: all 86 closed issues have the expected state/reason/label/notice/destinations; original bodies retained. Only Renovate #889 remains an open source issue. No migration errors or concurrent source changes were encountered.
- The 87-issue inventory and its source snapshots remain frozen migration evidence. Do not recapture them merely to erase intentional closures. Per-issue outcomes: [cutover-operations.json](cutover-operations.json).
- Planning unit tests: 24 PASS. Plan validator: 0 errors, 4 retained preparatory-dependency warnings. Core documentation audit and strict EN/DE builds passed for both documentation changes; no runtime matrix or production Pages deployment.
- Real Obsidian/CardBoard/Git UI acceptance remains **unverified and explicitly deferred**, not PASS.
- BaseHarbor Project #4 retirement remains **not executed**: the connector has no Projects write capability. This stale view is no longer a planning authority. Leave unrelated ai-coding-system Project #1 untouched.
- Product task branches, PRs and ownership remain intact; a relocated/closed source issue is never evidence that a task is accepted.


**Status: activated when this commit reaches `main`.** The Maintainer authorized merging and switching on 2026-10-15 with the actual Obsidian UI explicitly unverified. This repository is then the sole planning authority. See the [cutover record](cutover-checklist.md) for entry-point merges, issue relocation and outstanding Project retirement. Historical source snapshots are immutable migration evidence, not maintained planning.

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
