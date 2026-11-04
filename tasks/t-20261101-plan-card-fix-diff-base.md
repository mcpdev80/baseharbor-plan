---
id: t-20261101-plan-card-fix-diff-base
type: task
areas: [ci]
release: backlog
version: ""
parent: ""
owner: worker-ornith (session 35cdb02e)
kanban_lane: closed
kanban_summary: "Repair the planning card tasks/diff-base.md that commit 6cc2371 (PR#1251-Merge-Epoche) introduced by hand instead of via…"
kanban_status: closed
kanban_title: "Regenerate diff-base planning card to valid schema (mechanical, no content rewrite)"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1251"]
sources: ["mcpdev80/baseharbor#1251"]
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1251", "https://github.com/mcpdev80/baseharbor/actions/runs/41311582975"]
---

- [x] t-20261101-plan-card-fix-diff-base · Regenerate diff-base planning card to valid schema (mechanical, no content rewrite) #task #release/backlog #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** worker-ornith (session 35cdb02e)  
    **PR:** [baseharbor#1251](https://github.com/mcpdev80/baseharbor/pull/1251)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1251), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/41311582975)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [backlog](../releases/backlog.md)  
**Depends on:** none  
**Owner:** worker-ornith (session 35cdb02e)  
**Priority:** not set  
**PRs:** [baseharbor#1251](https://github.com/mcpdev80/baseharbor/pull/1251)  
**Source:** [baseharbor#1251](https://github.com/mcpdev80/baseharbor/issues/1251)
<!-- /generated:links -->

## Goal

Repair the planning card `tasks/diff-base.md` that commit `6cc2371` (PR#1251-Merge-Epoche) introduced by hand instead of via `scripts/plan.py new`, so `python3 scripts/plan.py check` passes on it. Mechanical schema fix only — the task meaning (PR #1251 merged the diff-base resolver fix to develop) is preserved verbatim, not rewritten.

## Scope

- In scope: regenerate the `diff-base` card as a valid closed card (`type: task`, `#status/closed`, `#release/backlog`, `resolution: accepted`, https evidence links, tool-generated filename/id, generated card + links blocks), remove the old hand-written file, `render`, `check`, commit, push origin main.
- Out of scope: rewriting the task content/meaning, editing scripts or generated views by hand, touching other cards, the product repository, or CI.

## Acceptance

- `python3 scripts/plan.py check` reports 0 errors (modulo the pre-existing inventory-snapshot `sources` constraint on #1240, see Handoff).
- The new closed card carries exactly one `[x]` checkbox, `#status/closed`, `#view/closed #board/planned`, `resolution: accepted`, and https evidence links.
- The old `tasks/diff-base.md` is gone (`git rm`); no content is lost — it is carried by the regenerated card.

## Required checks

- `python3 scripts/plan.py render` then `python3 scripts/plan.py check` => 0 errors before commit/push.

## Dependencies and file ownership

- Exclusive write set: `tasks/diff-base.md` (removed), the new `tasks/t-*.md`, and the evidence addendum `evidence/board-2026-11-01/plan-card-fix/`.
- Do not touch scripts, generated views, other task cards, or the product repository.

## Handoff

- 2026-11-01: Card `diff-base` was regenerated mechanically because `6cc2371` hand-wrote it (invalid id, unsupported tags `#fix`, missing `#release` tag, conflicting lifecycle markers `accepted` vs `closed`, illegal type, non-https evidence links, broken links). New card id `t-20261101-plan-card-fix-diff-base`, `type: task`, `release: backlog`, `#status/closed`, `resolution: accepted`, evidence links to PR #1251 and CI run 41311582975. Old file removed with `git rm`. Content preserved verbatim (PR #1251 merged the diff-base resolver fix to develop).
- Remaining: 2 `sources` inventory errors (#1240 not in snapshot `migration/source-snapshot/inventory.json`, captured 2026-10-15; #1251 not inventoried). These are schema-external snapshot-staleness, not card-schema defects; out of this mechanical-repair scope.
