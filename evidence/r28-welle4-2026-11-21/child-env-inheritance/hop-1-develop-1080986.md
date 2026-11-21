# Card 0428-222 / PR #1749 — hop BLOCKED: remote lane contaminated + develop advanced (scope decision required)

**Lane:** `w21-pr1702-0428-142-compat`
**Worktree:** `/home/marcel/dev/baseharbor-ecosystem/workers/0428-222-childenv-wt`
**State:** END_BLOCKED. Cannot push. Remote `lane-0428-222-child-env` carries FOREIGN commits from other lanes; my clean candidate merge was rejected (non-fast-forward). No write pushed. No force. No amend. No rebase.

## PLAN
- Bullet 1: Evidence file `evidence/r28-welle4-2026-11-21/child-env-inheritance/hop-1-develop-1080986.md` (own plan-worktree; shared checkout forbidden — tooling-issue #29).
- Bullet 2: Read `devhop2.g.md` (new guard): develop now `513488eeb6d` (merge-commit, 21:28:21Z); old target `1080986fe73` superseded. Hop must land on `513488eeb6d`, not `1080986fe73`.
- Bullet 3: ls-remote reality check at hop start: develop=`1080986fe73`, PR#1749 head + lane branch=`78cd7d3c078`.
- Bullet 4: Did hop locally: `git merge --no-ff origin/develop` 1080986fe73 => merge commit `bdb4aeb40` (parents `a3129b580` + `1080986fe73`); my 4 candidate commits unchanged.
- Bullet 5: PUSH REJECTED non-fast-forward. Investigated: remote branch is CONTAMINATED with foreign card commits.
- Bullet 6: SCOPE DECISION NEEDED from owner before any further write.
- Bullet 7: END_BLOCKED, no candidate fix, no push, no force.

## Reality witnesses (git ls-remote, the only trusted source)
- Planning remote: `git -C baseharbor-plan remote -v` => `origin https://github.com/mcpdev80/baseharbor-plan.git`.
- Remote guard: `git remote -v` in worktree => `lane-origin https://github.com/mcpdev80/baseharbor.git` (github.com/mcpdev80 URL, the authoritative remote).
- Hop-start ls-remote (at measurement time):
  - `refs/heads/develop` = `1080986fe73cb3d6e283fd9ef61c05c02b9260af`
  - `refs/pull/1749/head` = `78cd7d3c0788a181fbeb97fd9eebaccabc9f01e4`
  - `refs/heads/lane-0428-222-child-env` = `78cd7d3c0788a181fbeb97fd9eebaccabc9f01e4`
- Current authoritative develop (via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`) = `513488eeb6d788f0e5eec054be89807505f05e08` (ADVANCED past 1080986fe73, per guard devhop2.g.md).

## The blocker: remote branch is contaminated with FOREIGN commits
I did the hop locally and pushed. Push rejected as non-fast-forward. Investigating the remote ref (fetched to a temp mapping) shows:

- Remote `lane-0428-222-child-env` head = `78cd7d3c0788a181fbeb97fd9eebaccabc9f01e4`.
- My local pre-merge head `a3129b580` is NOT an ancestor of the remote (`git merge-base --is-ancestor a3129b580 refs/temp/remote-branch` => NO).
- My merge-base with the remote is `68f48754b` (my own gofmt commit).
- Between `68f48754b` and remote head `78cd7d3c078`, the remote carries commits that are NOT part of my card 0428-222 candidate:
  - `d1acf3f31` Merge pull request #1585 from mcpdev80/lane-0428-fix-bf01-v2 — "fix(cli): state-dir override owns target-selection state (BF-01, 0427-189)" — FOREIGN card (0427-189 / lane-0428-fix-bf01-v2).
  - `bc936d245` fix(cli): isolate target selection per state root — FOREIGN (belongs to the PR#1585 chain, not 0428-222).
- The remote's version of my 0428-222 commits is RE-ORDERED on top of those foreign commits: remote chain is `68f48754b -> d1acf3f31(foreign merge) -> 8fb122109 -> 2bd79a28d -> 87bc6a69c -> 78cd7d3c0`, whereas my clean chain is `68f48754b -> b32eae707 -> 3df3cb8be -> a3129b580`.

So other lanes (0428-060-updown via PR#1747, 0427-169-ci via PR#1748, lane-0428-fix-bf01-v2 via PR#1585) have all written commits onto this branch named `lane-0428-222-child-env`. It is no longer my clean card-0428-222 candidate. This is a multi-lane branch-write collision.

## What I did NOT do (guardrails held)
- No force-push, no force update. Forcing would splice foreign commits onto the candidate and create a double-write.
- No rebase, no amend, no filter-branch. Verified commits must stay SHA-identical (card 0428-224).
- No local suite test run (coordinator runner rule 2026-11-21; bare `go test ./cmd/baha/` starts real lifecycle containers).
- No `.github/**` or `scripts/**` edit. No subagents. No merge/close of the PR.
- No evidence written into a product repo.

## The develop-advanced problem (guard devhop2.g.md)
Even setting aside the contamination, the hop target has moved. The original hop landed on `1080986fe73`. The current authoritative develop is `513488eeb6d` (a merge-commit, 21:28:21Z). A correct hop now must land on `513488eeb6d`. This is a second independent reason the original `bdb4aeb40` hop is stale and must be redone against the new head — but ONLY once the branch ownership/collision is resolved.

## Why this needs an owner scope decision (not a self-fix)
- The remote `lane-0428-222-child-env` is currently a shared/collided branch carrying other lanes' work. I cannot safely reset, force, or re-derive it without risk of destroying foreign commits that may belong to live lanes — a write-set I do not own.
- AGENTS 3.8 (one integration candidate per chain) and 5.6 (OWNER STOP / foreign write-set protection). A corrupted shared branch is exactly the "newer explicit Owner decision" case.
- The two correct paths (both owner decisions):
  1. Owner/coordination re-points or recreates `lane-0428-222-child-env` as a clean card-0428-222 branch (deleting the foreign commits), then I redo the hop against `513488eeb6d`; OR
  2. A fresh lane/branch is commissioned for card 0428-222, and the collided branch is reconciled separately.

## END
END_BLOCKED w21-pr1702-0428-142-compat: hop BLOCKED, no write pushed. Remote `lane-0428-222-child-env` (`78cd7d3c078`) carries FOREIGN commits from lanes 0428-060 (PR#1747), 0427-169 (PR#1748), lane-0428-fix-bf01-v2 (PR#1585, `d1acf3f31`/`bc936d245`); my clean candidate merge `bdb4aeb40` (parents `a3129b580` + `1080986fe73`) was rejected non-fast-forward (merge-base `68f48754b`). No force/rebase/amend/filter-branch. ALSO: develop advanced `1080986fe73` -> `513488eeb6d` (guard devhop2.g.md), so hop must land on the new head once the branch is clean. Needs owner scope decision on the collided branch. Evidence: `evidence/r28-welle4-2026-11-21/child-env-inheritance/hop-1-develop-1080986.md`.
