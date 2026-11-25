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
- PR #38 originally contained exactly two paths: this owner-ruling evidence file and `tasks/t-20261123-planner-deleted-source-advisory.md`. This forward re-land restores those same two paths; the task change is only the requested sentence, with no metadata or status changes.
- Pre-publication evidence-path check: `git ls-tree -r --name-only origin/main | grep 'evidence/r29-welle6-2026-11-28/0428-253/w136-1853-owner-ruling.md'` produced no output because this evidence file is introduced by this PR; after merge, verify the exact path on origin/main.

## PLAN — forward re-land from live main

1. Verify the actual latest plan origin/main SHA and exact card/evidence paths before editing; do not rely on previously reported 261667467 or cc244d7ef tips.
2. Restore the exact 0428-253 task note line and the PR #38 owner-ruling evidence from commit 5b8c4d57 into a detached worktree at live main.
3. Before creating the plan branch or first commit, record the exact base, card owner, evidence identity, literal commit invocation, and author gate here.
4. Create one forward-only plan branch/PR from that base, verify the two-path diff and plan validation, then merge per the owner-requested plan-PR path.
5. Verify the owner line and evidence file on live origin/main; preserve unrelated current plan changes.

## Live-main re-land facts

- Latest live plan `refs/heads/main` at re-land preparation: `bc4689919f2cf8a1c7fdd7ddc817b39c14495fde`; `git ls-remote` and fetched `origin/main` both returned this exact SHA. The owner-provided 261667467 and later cc244d7ef were no longer current by this fresh read.
- The current frontmatter owner is verbatim `w205 (lane w205-0428-253)`; current main had no exact ruling line under Handoff. The task file at PR #38 merge commit `5b8c4d57fec94887731928dbdc6f95027f618bc2` differs from the live-main task only by the requested two-line Handoff addition.
- PR #38 is closed/merged with reported merge commit `5b8c4d57fec94887731928dbdc6f95027f618bc2`, but that commit is not an ancestor of live origin/main (`git merge-base --is-ancestor 5b8c4d57... origin/main` exits 1). Current main lacks the prior evidence path `evidence/r29-welle6-2026-11-28/0428-253/w136-1853-owner-ruling.md`; GitHub Contents API returned 404. This is the payload-loss fact that necessitates a new forward PR.
- Re-land paths are exactly the owner-ruling evidence file and task note. `evidence/r28-welle6-2026-11-25/0428-284-1842-hop/round-1.md` is absent, but the later `w238-1842-hop.md` exists and documents the accepted hop plus both exact-head runs; treat it as superseded. `evidence/2026-11-25/w234-0428-307-1850run2.md` is absent, while later `evidence/2026-11-26/w227-0428-307-1850hop-hop.md` exists with the newer two-run hop record; treat the old run2 note as superseded. Neither extra path is in this re-land diff.
- Identity source correction: `dispatch-lane.sh:45` is prompt text instructing the canonical author rule, not executable git configuration. `dispatch-lane.sh:28-33` calls `lane-name.py`; that helper (`coordinator/scripts/lane-name.py:16-21`) retrieves the Codeman session name. The lane-name rule in the prompt extracts the value inside `(lane X)`, yielding `w205-0428-253`; that is the canonical rule, though the shell does not itself configure `git user.name`.

## Current re-land identity and base

- Card owner VERBATIM from fetched plan origin/main: `w205 (lane w205-0428-253)`.
- Evidence commit identity: `user.name=w136-pr1836-rowsreview`; `user.email=w136-pr1836-rowsreview@baseharbor.local`.
- Literal commit invocation for this re-land: `git -c user.name='w136-pr1836-rowsreview' -c user.email='w136-pr1836-rowsreview@baseharbor.local' commit -m 'docs(plan): reland 0428-253 owner ruling'`.
- Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w136-pr1836-rowsreview`.
- Exact branch base before branch creation: `bc4689919f2cf8a1c7fdd7ddc817b39c14495fde`; this detached worktree is at that SHA. Verify `git merge-base --is-ancestor bc4689919f2cf8a1c7fdd7ddc817b39c14495fde HEAD` after the first commit.

## Re-land validation and delivery

- The two selected paths were recovered from `5b8c4d57fec94887731928dbdc6f95027f618bc2` with `git checkout 5b8c4d57fec94887731928dbdc6f95027f618bc2 -- tasks/t-20261123-planner-deleted-source-advisory.md evidence/r29-welle6-2026-11-28/0428-253/w136-1853-owner-ruling.md` in this isolated worktree. The live main task differed from that commit only by the missing requested Handoff sentence; no other current task content was overwritten.
- `python3 scripts/plan.py check` passed: 776 tasks, 7 epics, 13 releases, 24 decisions; 0 errors and 10 existing dependency warnings. No metadata/status fields changed, so render was not needed.
- `git diff --check` passed. Evidence contains no markdown checkbox lines.
- The additional deleted evidence paths were not restored: current main contains the newer `w238-1842-hop.md` and `w227-0428-307-1850hop-hop.md` records described above.
- The `49708002...` base block earlier in this file is historical evidence for original PR #38. The forward re-land branch is instead based only on current plan main `bc4689919f2cf8a1c7fdd7ddc817b39c14495fde`.
