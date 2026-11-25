# Owner ruling record — card 0428-253 / PR #1853

## PLAN

1. Read the current plan-main card and owner decision.
2. Add the exact owner-authorized identity decision line to the task note without rewriting product history or changing status.
3. Render and check plan-derived files, inspect the write set, and publish through one plan PR.
4. Verify the merged plan SHA and exact line on origin/main; then resume queued product review work.

## Owner and evidence identity

- Card owner VERBATIM from current plan origin/main: `w205 (lane w205-0428-253)`.
- Evidence author: `user.name=w136-pr1836-rowsreview`; `user.email=w136-pr1836-rowsreview@baseharbor.local`.
- Literal commit invocation: `git -c user.name='w136-pr1836-rowsreview' -c user.email='w136-pr1836-rowsreview@baseharbor.local' commit -m 'docs(plan): record owner admission decision 0428-253'`.
- Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w136-pr1836-rowsreview`.
- Verified planning remote before branch creation: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` returned `49708002faa7ca1d81911e888a38c41b2b57a3d8 refs/heads/main`.
- The detached evidence worktree is at that exact SHA. `git merge-base --is-ancestor 49708002faa7ca1d81911e888a38c41b2b57a3d8 HEAD` succeeds. This evidence and the visible identity block were written before branch creation.

## Owner decision

Exact requested line to add to `tasks/t-20261123-planner-deleted-source-advisory.md`:

`Erste zwei Übernahmen als gekürzte Identität der eigenen Bahn übernommen (w205 ≙ w205-0428-253), Eigentümer-Erkenntnis 25.11., keine Umschreibung.`

The ruling admits only the two specified same-lane shortened-identity commits `90c8017b` and `3c1ebc6f`. It does not admit foreign-lane authorship, rewrite history, resolve code findings, qualify Hosted CI, or authorize merge.

## Validation and exact write set

- Added only the requested sentence to the task's Handoff section; no metadata or status changes.
- `python3 scripts/plan.py render` completed and reported an unrelated generated update to `tasks/t-20261122-runtime-broker-health-unhealthy.md`; that unrelated output was restored from this isolated worktree's base and is excluded.
- `python3 scripts/plan.py check` passed: 776 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 existing warnings.
- Task-note change: `tasks/t-20261123-planner-deleted-source-advisory.md` contains only the requested added decision sentence; the companion evidence file records the ruling and its publication trail.
- Pre-publication evidence-path check: `git ls-tree -r --name-only origin/main | grep 'evidence/r29-welle6-2026-11-28/0428-253/w136-1853-owner-ruling.md'` produced no output because this evidence file is introduced by this PR; after merge, verify the exact path on origin/main.

## Publication receipt

- Decision PR: https://github.com/mcpdev80/baseharbor-plan/pull/38
- PR #38 candidate: `b113bea1c04c23243e1a3036137138e5c66f124f`.
- Squash merge SHA: `5b8c4d57fec94887731928dbdc6f95027f618bc2`.
- Plan `main` tip after merge: `5b8c4d57fec94887731928dbdc6f95027f618bc2`.
- `git ls-tree -r --name-only origin/main | grep 'evidence/r29-welle6-2026-11-28/0428-253/w136-1853-owner-ruling.md'` returned the evidence path; the exact decision sentence was also read back from `origin/main`.
- END_DONE w136-pr1836-rowsreview: owner admission ruling published in plan PR #38 and verified on main; candidate `b113bea1c04c23243e1a3036137138e5c66f124f`.
