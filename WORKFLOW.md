# Planning workflow

How tasks are written, claimed, handed off and closed in this repository. Product engineering rules (branching, review, CI, release gates) stay in the product repository: [DEVELOPMENT_GUIDELINES](https://github.com/mcpdev80/baseharbor/blob/develop/docs/DEVELOPMENT_GUIDELINES.md), [CONTRIBUTING](https://github.com/mcpdev80/baseharbor/blob/develop/CONTRIBUTING.md), [release audit](https://github.com/mcpdev80/baseharbor/blob/develop/docs/internal/pre-release-documentation-audit.md). This file does not repeat them.

> Planning authority is this repository from the activation commit on `main` ([migration/README.md](migration/README.md)). Source GitHub issues are historical/discussion references, not a second task-status authority.

## Files

| Path | Holds |
| --- | --- |
| `tasks/<id>-<slug>.md` | One executable task: frontmatter metadata, one card line, goal, scope, acceptance, checks, dependencies/file ownership, handoff |
| `releases/<release>.md` | Release (or series) scope, acceptance, ordering and the release's own `status` |
| `epics/<id>-<slug>.md` | Coordination for a group of tasks; children point to it with `parent` |
| `decisions/<date>-<slug>.md` | Short decisions and rationale |
| `views/` | **Generated** read-only summaries; never edit by hand |
| `migration/` | Source inventory, snapshot, manifest, coverage and cutover material |

## Task notes

```markdown
---
id: core-912
areas: [wizard]       # optional topic slugs, shown as badges
type: task            # task | bug | feature | maintenance | acceptance | architecture | review
release: v0.4.26      # a file in releases/
version: ""           # optional patch version inside a series release
parent: v0.4.26       # an epic id or a release id
priority: ""          # optional: critical | high | normal | low; empty means not set
owner: ""             # who holds the claim; free text such as "name (session 2)"
depends_on: [core-910]
repos: [mcpdev80/baseharbor]
prs: []               # owner/repo#number
sources: ["mcpdev80/baseharbor#912"]
aliases: []           # optional: duplicate source issues this task also answers
early: false          # optional: true if explicitly pulled ahead of its release
blocker: ""           # required while #status/blocked
resolution: ""        # accepted | superseded | dropped, only on a checked card
evidence: []          # https links, required on a checked card
---

  - [ ] core-912 · Wizard: present a compact needs-first selection #task #release/v0-4-26 #status/planned   ← card line (not indented in a real note)

<!-- generated:links --> … <!-- /generated:links -->

## Goal / ## Scope / ## Acceptance / ## Required checks / ## Dependencies and file ownership / ## Handoff
```

Rules (enforced by `scripts/plan.py check`):

- Exactly **one checkbox per task note**, not indented: the card line. Write acceptance criteria as plain bullets.
- The **status tag on the card line is the only maintained lifecycle state**. Do not add a status to the frontmatter. The generated `#view/…` routing tag derives readiness; edit canonical fields and run `render`, never edit the view tag.
- The indented `generated:card` block is a read-only CardBoard preview of owner, optional priority, PRs, blocker and unfinished prerequisites. It is generated from the same task fields; it is not a second task record. Unset priority is omitted from cards; summaries retain an explicit unknown value.
- Refresh derived board content with `render` before assigning work; a checkbox edit in Obsidian does not execute Python automatically. CI rejects stale generated tags/previews.
- The card's `#release/…` tag equals the `release` field with dots replaced by dashes (CardBoard tags cannot contain dots).
- The block between `<!-- generated:links -->` markers is rendered from the frontmatter. Run `python3 scripts/plan.py render` after editing metadata.
- Use relative Markdown links (`[core-910](core-910-….md)`) so navigation works on GitHub too.
- New task: `python3 scripts/plan.py new --repo core --slug short-name --title "Area: outcome" --release v0.4.27`. IDs are never reused or renumbered ([decision](decisions/2026-10-15-stable-task-ids.md)).

## Lifecycle

| Card line | Meaning | Requirements |
| --- | --- | --- |
| `[ ]` `#status/backlog` | Explicitly unscheduled or awaiting triage | release `backlog` or `triage` |
| `[ ]` `#status/planned` | Scheduled. Derived: **waiting** (a dependency is not accepted), **queued** (dependencies accepted, release not yet `active`), **ready** (dependencies accepted and release `active`, or `early: true`) | — |
| `[ ]` `#status/active` | Claimed and being implemented | `owner` |
| `[ ]` `#status/blocked` | Cannot proceed | `blocker` text |
| `[ ]` `#status/review` | Implementation ready for review | `owner`, at least one PR |
| `[x]` `#status/closed` | Closed (checked ⇔ closed) | `resolution` and `evidence` |

- **Ready for review ≠ accepted ≠ release qualified.** A task is accepted only when the Maintainer has accepted the result and the required evidence is linked; a merged PR or an agent's summary alone is not acceptance. A release is qualified only when its release note says `status: qualified` with evidence — never because all its cards are checked.
- Ticking the checkbox in CardBoard appends `@completed(…)` but keeps the old status tag; the validator then fails until you change the tag to `#status/closed` and add `resolution` and `evidence`. That is intentional.
- `superseded` needs `superseded_by: <id>`; a superseded task counts as accepted only when its replacement is.
- CardBoard 0.7.9 cannot drag cards between columns. Change the status by editing the tag (or `scripts/plan.py claim`).

## Executable task slices

A task is assignable only when it can reach its own review handoff without unfinished work from another implementation session. A dependency graph is allowed; a task waiting for a predecessor is not assigned early.

- State the observable result, bounded owned paths, existing input authority, callable output interface and explicit exclusions. Use component-specific identifiers/tests; do not add competing shared state or helper files in parallel lanes.
- All required predecessor interfaces must already be reviewed, merged and accepted. Do not develop against another task branch or invent a temporary interface that another session must later reconcile.
- Include the full verification path in readiness: required fixtures, actual test discovery, trusted CI selection, supported executor/native gate, immutable consumer candidates when needed, and the available connector/CLI capabilities. Green generic tests that never execute the component are insufficient.
- If a trusted CI lane is missing, prepare it as an explicit predecessor before assigning product work. The CI owner delivers the plan, executor and final-check enforcement together. Product sessions must not each create a separate workflow or wait for another session to dispatch tests.
- Assign one end-to-end owner per task: implement, integrate, run the sufficient checks, diagnose real failures, collect exact-SHA evidence and publish the planning handoff. The owner reads current planning/PR status directly; Marcel does not relay updates among sessions.
- Parallel tasks must have disjoint write sets and consume the same accepted baseline. Shared registrations/help/goldens are owned by a later integration task. Review/acceptance is independent; an implementation owner may not waive unresolved coverage or approve its own trust policy.
- Before assignment, check the readiness inventory as well as the generated dependency state. Unknown executor/candidate gaps become explicit prerequisites, not hidden mid-task waits. A later unexpected real defect is reported honestly and repaired through normal review.

## Ownership protocol

A local `owner` field is not a lock: it only works when published before implementation starts.

1. `git pull` — read the current remote planning state.
2. Check the task: `python3 scripts/plan.py show <id>` (state and dependencies). Take only work the Maintainer assigned; one task per session.
3. Claim: `python3 scripts/plan.py claim <id> --owner "<name> (<session>)"`, then `git commit -am "claim <id>: <owner>"` and `git push`.
4. If the push is rejected: `git pull` (merge, no rebase of published commits), re-read the task. If someone else claimed it meanwhile, stop and resolve with them or the Maintainer before working. Never overwrite another claim.
5. Only after the claim is on `main`, start the product work (branch/PR in the product repository per its guidelines).
6. Keep planning edits to your task's file. Shared files (release notes, epics, roadmap) change in separate small commits after coordination.
7. Handoff: update the task's **Handoff** section (newest first: branch, PR, evidence, open points), set `#status/review` with the PR in `prs`, commit and push. Then **stop**; do not start another task on your own. Report blockers instead of switching tasks (`#status/blocked` + `blocker`).
8. The Maintainer accepts: check the box, set the tag to `#status/closed`, set `resolution: accepted` and `evidence`, run `render` and `check`, commit. Product merge completion includes publishing this accepted task state and refreshed generated Obsidian/CardBoard views to planning `main`; do not report the task fully complete while that closeout is missing. If acceptance is still pending, publish the actual review state instead.


Preserve other people's commits. **No force-push** on this repository.

## Planning repository vs product repositories

This is a live shared planning repository. All authorized planning updates go directly to `main`; do not create a branch or PR unless the Maintainer explicitly requests one. That includes claims, status, evidence, handoffs and coordinated shared planning changes. Keep commits coherent and small.

Pull current `main`, preserve concurrent updates, render and validate, then push normally (or update with an expected-SHA lease). If publication is rejected, integrate and re-check rather than overwriting or force-pushing. Existing planning branches should have their still-relevant content integrated promptly, without treating publication as task acceptance, and be deleted after integration. No accumulation of completed planning branches. Their only required check is the cheap validator ([.github/workflows/validate.yml](.github/workflows/validate.yml)). No product runtime matrix, Docker/Podman journey or release gate applies to planning edits. Product changes keep their own branch/PR/review/CI rules in the product repositories.

## Generated files

`views/*.md`, `migration/manifest.json` and `migration/coverage.md` are generated by `python3 scripts/plan.py render` and verified in CI. They are reproducible summaries, not maintained state.

## Intake of external bugs and feature requests

After the cutover, outside reporters still open GitHub issues in the product repositories.

1. The Maintainer (or a triage session) checks for an existing task: `python3 scripts/plan.py list` and a search in `tasks/`.
2. Duplicate: comment on the issue with a link to the existing task and add the issue to that task's `aliases`. Close the issue as duplicate if the reporter has nothing to add.
3. New work: create a task with `scripts/plan.py new` in release `triage` (or a release, if decided), add the issue to `sources`, and comment on the issue with the task link.
4. The GitHub issue stays for discussion with the reporter; scope, acceptance and status live only in the task note.

## Opening the vault

See [README.md](README.md).

## Derived visual planning

`#area/…` and `#kind/…` tags are generated from `areas` and `type`; edit the frontmatter, never a second copy of those tags. `roadmap/cards.md` is a generated read-only CardBoard projection of release scope/status and real task acceptance/blockers. Its presentation checkboxes are not task records and must not be checked; the validator rejects any edits. The Roadmap board uses only `#roadmap`, task boards use task/release tags.

The Current board separates scheduled work into **Planned** (unfinished prerequisites) and **Ready** (`#view/ready`, assignable prerequisites accepted). Both columns stay expanded. Ready uses `#view/ready`. Planned uses generated `#board/planned`, emitted only for waiting and closed cards. CardBoard routes checked matching cards to its Completed column and unchecked ones to Planned, so each card appears once. A checked card with only `#view/closed` would otherwise match no ordinary column and disappear from Closed. The routing tag never changes canonical status or acceptance. Closed is expanded and has capacity for 1,000 cards rather than silently limiting the current release to ten. The Next board continues to show ready, waiting and later-release work.

Ready is maintained from the authoritative task records, not by manually moving cards. After every dependency acceptance, task claim, blocker change or handoff, integrate current planning `main`, run `python3 scripts/plan.py render` and `check`, and publish all refreshed views. Accepted dependencies automatically promote eligible planned tasks to Ready; claims remove them from Ready. Do not add a second task list or mark unfinished prerequisites accepted to fill the column.

At each Maintainer acceptance/assignment review, inspect `python3 scripts/plan.py list --ready --release v0.4.26` (using the current release), the remaining waiting tasks and their real implementation/CI prerequisites. Keep genuinely independent slices documented with owned files, existing inputs, callable outputs and required checks before assignment. Record missing prerequisites explicitly. If no executable task is available, report that fact; never manufacture readiness or assign dependency work in progress. Implementation sessions maintain their assigned task and hand off without starting a new one.

## Every release has an executable closeout

[Release workflow](RELEASE_WORKFLOW.md) defines the six recurring cards and source checklist. Run `python3 scripts/release_cycles.py sync` when scheduling a concrete release or changing scope. Cleanup and Renovate intake precede future feature work; preparation waits for all scoped work; complete pre-release, promotion/tag commands and verified publication remain separate accepted stages. The already-running v0.4.26 has only the four completion cards; startup cleanup/intake is not retroactively added.
