# integrate-wave — Evidence (mechanical execution, NO product code)

## PLAN

1. [x] Step 0: Merge PR #1256 — DONE, develop == db138ecd (verified ls-remote)
2. [x] Step 1a: Re-qualify PR #1245 — rebased OK (no conflicts, product commit 1:1), BUT force-push blocked by server guard
3. [x] Step 1b: Re-qualify PR #1255 — NOT STARTED (same guard class)
4. [ ] Post END_DONE/END_BLOCKED to lane 35cdb02e-a3b3-4e6d-86f9-1cbb35822587

## repo-rule compliance

- Mechanical execution only. NO product code changes. NO merges of 1245/1255 (Coordinator does that).
- Force-push ONLY onto the same PR branches. No workflow/script changes.

## Run log

- Step 0 — PR #1256 merge:
  - Local develop was 7 commits behind develop; merged origin/work/gatemap-r2-v2 (db138ecd) into develop (fast-forward).
  - Pushed develop. Verified with `git ls-remote origin develop` -> `db138ecd...` == merge SHA. ✅ DONE.

- Step 1a — PR #1245 (work/docker-endpoint-context):
  - Fetch work/docker-endpoint-context + origin/develop.
  - Rebase onto new develop (db138ecd): `git rebase origin/develop` -> SUCCESS, no conflicts (7 commits replayed cleanly).
  - Original product commit `5e298aaa "fix(runtime): resolve the ACTIVE Docker context..."` preserved 1:1 in rebased history.
  - Force-push rejected by server-side guard: `! [rejected] ... (non-fast-forward)` on both
    refs/heads/work/docker-endpoint-context AND .../docker-endpoint-context-ornith.
  - Authoritative `git ls-remote origin work/docker-endpoint-context` still == fc621b8d (original tip). Push never landed.
  - Root cause: server-side (spokes-receive-pack) guard on work/* PR refs forbids force-push of rewritten history.
    Confirmed even pushing the ORIGINAL commit fc621b8d back is refused when forced. Not a local cache/config issue
    (fresh ls-remote, fetch --prune, SSH/HTTPS all agree; local remote-tracking ref correct).

- Step 1b — PR #1255: NOT STARTED — blocked by same force-push guard as 1245 (same class of work/* PR ref).

## END

BLOCKED integrate-wave: 1256-merge=db138ecd 1245=blocked (force-push guard) 1255=not-started (same guard) | server-side non-fast-forward guard blocks force-push of rebased work/* PR refs
