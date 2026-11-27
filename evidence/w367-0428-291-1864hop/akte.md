# w367-0428-291-1864hop — Re-hop PR #1864 (card 0428-291) onto current develop + fresh exact-head CI

## PLAN
- Attest live develop base SHA (ancestor of first hop commit) in evidence; PR head b9675cc0b6dc8fee0d96015c778d0645365acc5a, branch w333-0428-291-capperms-fix; card 0428-291 owner unassigned, canonical lane identity w367-0428-291-1864hop
- Own worktree workers/worktrees/w367-0428-291-1864hop from the PR branch (single writer; show git log --oneline origin/develop..HEAD lists ONLY my commits; no foreign commit)
- git merge origin/develop forward-only (no force/cherry-pick); resolve conflicts ONLY in card write-set (cap perms fix scope), else STOP+file:line
- Canonical identity w367-0428-291-1864hop (env GIT_* unset, 4-field an/ae/cn/ce), pre-push gate
- EIN normal push (no force/proxy); prove delivery via ls-remote
- Fresh Hosted run to terminal (per_page=100 against first-30 trap); watch Trusted Plan + BOTH native paths
- Class Podman-skip as baseline family #136/0428-359 prerequisite (develop row source.cmd_baha_app_init_runtime_permission_scope_test_go needs runtime_specific:true)
- PR comment head + run ID; akte on plan main; END with head+parents+run IDs+4-field; docker/podman down

## Visible SATSZ block (visible-ansatz-block, attested at origin/main runtime)
- per-card frontmatter owner VERBATIM: unassigned (card 0428-291, tasks/t-20261116-r28-bug-capability-permissions.md); canonical lane identity from mission: w367-0428-291-1864hop
- git user.name I use: w367-0428-291-1864hop
- git user.email I use: w367-0428-291-1864hop@users.noreply.github.com
- literal commit/merge invocation: git -c user.name=w367-0428-291-1864hop -c user.email=w367-0428-291-1864hop@users.noreply.github.com merge origin/develop
- pre-push gate: git show -s --format='%an an=%an ae=%ae cn=%cn ce=%ce' -1

## Reality witnesses
- Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (verified first evidence commit path)
- Product remote origin: https://github.com/mcpdev80/baseharbor.git (verified before any push)

## STOP — single-writer provenance violation + unmerged base (no work performed)

I STOPPED before creating the worktree or touching git. The branch HEAD does not satisfy the mission's single-writer / base-ancestry contract:

1. FOREIGN COMMITS ON HEAD (scope violation). `git log --oneline origin/develop..w333-0428-291-capperms-fix` lists THREE commits:
   - `c945b2fcb` fix(0428-291) — author `w333-0428-291-capperms@baseharbor.local` (an earlier lane)
   - `9712023ed` Merge ... into w358-hop-1864 — author `w358-0428-291-1864hop@...` (a PRIOR hop lane)
   - `b9675cc0b` Merge ... into w358-hop-1864 — author `w358-0428-291-1864hop@...` (a PRIOR hop lane)
   Two of three commits are foreign-authored. The mission states: "a single foreign commit in that list is a scope violation" and "single writer". Building a hop on this shared branch would either (a) rewrite/absorb another session's commits (forbidden: no force-push, never overwrite another session), or (b) carry the foreign merge commits on a new hop branch (foreign commit on HEAD — same violation).

2. BRANCH HEAD NEVER MERGED INTO LIVE DEVELOP (base not an ancestor). live develop = `ea5218d72e263f21e79853b679af50074dab8c25`; `merge-base(b9675cc0b, develop)` = `c167fa5d` != develop tip. The card fix `c945b2fcb` was cut from an old develop base and 18 develop commits advanced before the branch was ever merged. `git merge-base --is-ancestor develop b9675cc0b` => NO. A forward-only hop from this HEAD is NOT a clean re-hop onto live develop; it would weave 18 unreviewed develop commits into a branch whose card content was never merged in.

3. NOTHING TO FORWARD-HOP — the card fix content is absent from live develop:
   - `git diff --stat c945b2fcb develop -- cmd/baha/app_init_detection.go ...` = 28 + 174 + 10 changed (card content NOT in develop).
   - No `app_init_runtime_permission_scope_test.go` on develop.
   So live develop does not yet carry card 0428-291.

## Why this is a transport/coordinator fact, not a worker fault
- Card 0428-291 is `blocked` in plan main (not accepted/merged; PR #1864 still OPEN).
- Card blocker (w267 exact-head HOLD 7206173319 on b9675cc0): develop catalog row `source.cmd_baha_app_init_runtime_permission_scope_test_go` lacks `runtime_specific:true` => only the Docker native gate executes; the card requires BOTH native paths (card lines 59-69). Fix = the baseline family #136/0428-359 landing the catalog row. This is a product-side/Owner baseline action, not a worker transport.
- The PRIOR lane w358-0428-291-1864hop ALREADY performed the forward hop + fresh exact-head CI (run 45907132239, all required checks SUCCESS including Trusted Plan + Native gate plan). HEAD b9675cc0b is newer than w358's hop 9712023ed — the branch has been touched by another session after w358's clean hop.

## What a correct handoff needs (for the Coordinator / Maintainer)
- A single-writer candidate for card 0428-291: cut a fresh branch from the card fix `c945b2fcb`, rebase/transport onto live develop `ea5218d72`, push as a new clean hop head (NOT a rewrite of the shared w333-0428-291-capperms-fix).
- Then fresh exact-head Hosted CI and watch BOTH native Docker + Podman gates (the baseline-family prerequisite is what gates the Podman path).

## END
END_BLOCKED w367-0428-291-1864hop: branch HEAD b9675cc0b is not a single-writer hop base (two foreign merge commits by w358-0428-291-1864hop on top of card fix c945b2fcb by w333) AND HEAD is unmerged into live develop (merge-base c167fa5d != ea5218d72, 18 commits advanced). No worktree created, no git touched. Card 0428-291 blocker is the baseline family #136/0428-359 catalog prerequisite (source.cmd_baha_app_init_runtime_permission_scope_test_go needs runtime_specific:true) — a product-side/Owner action, not a worker transport. Prior lane w358 already hop+CI (run 45907132239, all required checks SUCCESS).
