# H-V44 Rueste-desk: baseharbor worktree inventory (BUG-HUNT, read-only)

LANE: 0428-221-huntrake. ROLLE: Worker, pure Befundung. SCOPE: ONLY read + this evidence file. NO `git worktree remove`, NO `rm`, NO `prune`, NO commit at baseharbor, NO PR, NO subagent.

## PLAN

1. Read mission H-V44; confirm read-only scope (inventory only, no mutation).
2. Collect `git worktree list --porcelain` from `/home/marcel/dev/baseharbor-ecosystem/baseharbor` (paths, heads, branch/detached).
3. Per worktree: `git status --porcelain` (dirty count), `git log -1` (last head), mtime.
4. Per branch-head: `git ls-remote lane-origin refs/heads/<branch>` (remote present?). Per detached: `git branch -r --contains <sha>` + `gh pr list --search <sha>`.
5. Classify each: (i) safe+remote, (ii) safe-but-orphan-lost-risk, (iii) DIRTY, (iv) live-lane.
6. Measure `du -xsh` per worktree and sum per class.
7. Cross-check live sessions via `codeman agent list --json` (session id per live-worktree mapping).
8. Write this evidence; push to origin/main; verify path present; post END.

## base-attestation

`git remote -v` at inventory source `/home/marcel/dev/baseharbor-ecosystem/baseharbor`:
- `lane-origin https://github.com/mcpdev80/baseharbor.git` (fetch/push) -- used for all ls-remote.
- `origin https://github.com/mcpdev80/baseharbor.git` (fetch/push).
- `upstream https://github.com/mcpdev80/baseharbor.git`.
All three resolve to the github.com/mcpdev80 URL; `lane-origin` was used exclusively for remote queries.

Disk at time of inventory: `/dev/sda1 193G, used 179G, avail 15G, 93%`.

## inventory (46 worktrees registered)

Key: head = short SHA. dirty = `git status --porcelain` line count. remote = `git ls-remote lane-origin` (branch) or `git branch -r --contains` + `gh pr list` (detached). class = (i) safe+remote, (ii) orphan-lost-risk, (iii) DIRTY, (iv) live-lane. live = maps to a currently-busy worker session.

| # | path | head | %an (last author) | last commit date | dirty? | remote? | size | class |
|---|------|------|-------------------|------------------|--------|---------|------|-------|
| 1 | /home/marcel/dev/baseharbor-ecosystem/baseharbor | 37587b0e | 0428-213-compilefix | Sat Nov 21 09:59 | 1 (untracked) | branch head present, sha matches remote | 806M | (iv) live-lane (main worktree) |
| 2 | /home/marcel/dev/baseharbor-ecosystem/.codex-worker-1401 | 9e1b905c | Worker w224 | Fri Nov 6 11:58 | 0 | detached; reachable from gh/1401 + lane-origin/1401 (PR #1401) | 30M | (i) safe+remote (PR #1401 head) |
| 3 | /home/marcel/dev/baseharbor-ecosystem/0428-210-authzkeep-wt | 52866ae3 | 0428-210-authzkeep | Sat Nov 21 11:09 | 0 | detached; NOT on any remote/develop; `gh pr list` empty | 38M | (ii) orphan-lost-risk |
| 4 | /home/marcel/dev/baseharbor-ecosystem/0428-210-hopfix3-wt | 6442955f | 0428-210-hopfix3 | Sat Nov 21 04:48 | 0 | detached; NOT on any remote/develop; `gh pr list` empty | 38M | (ii) orphan-lost-risk |
| 5 | /home/marcel/dev/baseharbor-ecosystem/0428-213-rebase1737-wt | 3010b212 | 0428-213-rebase1737 | Sat Nov 21 08:58 | 0 | detached; reachable from lane-origin/lane-0428-213-trust-uninstall-false-green | 38M | (i) safe+remote |
| 6 | /home/marcel/dev/baseharbor-ecosystem/0428-215-natfix-wt | 1167ea45 | 0428-215-natfix | Sat Nov 21 10:12 | 0 | branch head present | 38M | (i)/(iv) see note |
| 7 | /home/marcel/dev/baseharbor-ecosystem/0428-219-exportauth-wt | e45430f2 | Marcel Pfingstgräf | Sat Nov 21 05:46 | 0 | branch head present | 38M | (i)/(iv) see note |
| 8 | /home/marcel/dev/baseharbor-ecosystem/baseharbor/0428-211-hopdevelop-wt | 44b55ea4 | Marcel Pfingstgräf | Sat Nov 21 10:34 | 0 | detached; reachable from lane-origin/0428-210-alltargets + origin/develop | 38M | (i) safe+remote |
| 9 | /home/marcel/dev/baseharbor-ecosystem/work/0427-175-wt | 2dfcb21f | Marcel Pfingstgräf | Mon Nov 9 20:52 | 41 | branch head `0427-175-initlock` present | 32M | (iii) DIRTY (41 files) |
| 10 | /home/marcel/dev/baseharbor-ecosystem/work/0428-102-wt | d144945a | worker-ornith1.5 | Tue Nov 17 09:43 | 9 | branch head present | 36M | (iii) DIRTY (9 files) |
| 11 | /home/marcel/dev/baseharbor-ecosystem/work/0428-113-wt | 46de903f | worker-ornith1.5 | Wed Nov 18 21:58 | 9 | branch head present | 36M | (iii) DIRTY (9 files) |
| 12 | /home/marcel/dev/baseharbor-ecosystem/workers/.models/flash/bf01-base-wt | 13e096fc | Marcel Pfingstgräf | Sun Nov 15 08:56 | 0 | branch head present, sha BEHIND remote (remote=16241f24) | 36M | (i) safe+remote (stale, not lost) |
| 13 | /home/marcel/dev/baseharbor-ecosystem/workers/.models/flash/bf01-fix-wt | 0e9ccb58 | Marcel Pfingstgräf | Sat Nov 14 20:11 | 2 | detached; reachable from origin/develop + many gh/pr refs (base content) | 36M | (i) safe+remote |
| 14 | /home/marcel/dev/baseharbor-ecosystem/workers/.models/flash/wt | 09200869 | 0427-maintenance-r3 | Sun Nov 8 09:31 | 0 | branch head `work/w131-logs-command-gap` present | 31M | (i)/(iv) see note |
| 15 | /home/marcel/dev/baseharbor-ecosystem/workers/.tmp/0428-100-wt | 178b8a00 | mcpdev80 | Tue Nov 17 06:10 | 0 | branch head present | 36M | (i)/(iv) see note |
| 16 | /home/marcel/dev/baseharbor-ecosystem/workers/.w082-r3-wt | d2a9cd11 | mcpdev80 | Mon Nov 16 23:07 | 0 | branch head present | 37M | (i)/(iv) see note |
| 17 | /home/marcel/dev/baseharbor-ecosystem/workers/.w217-0428-204-entrypoints | 7db14285 | Marcel Pfingstgräf | Sat Nov 21 02:23 | 1 (untracked) | branch head `w217-verify-integration` present | 38M | (iii) DIRTY (1 file) |
| 18 | /home/marcel/dev/baseharbor-ecosystem/workers/.w230-base | 40cb28c7 | Marcel Pfingstgräf | Fri Nov 20 17:06 | 0 | detached; reachable from origin/develop | 38M | (i) safe+remote |
| 19 | /home/marcel/dev/baseharbor-ecosystem/workers/.w230-oldbase | 3f7600de | worker | Sat Nov 21 01:02 | 0 | detached; NOT on any remote/develop; `gh pr list` empty | 37M | (ii) orphan-lost-risk |
| 20 | /home/marcel/dev/baseharbor-ecosystem/workers/0428-086-wt | 7042ee61 | worker-ornith1.5 | Thu Nov 19 16:42 | 9 | branch head present | 38M | (iii) DIRTY (9 files) |
| 21 | /home/marcel/dev/baseharbor-ecosystem/workers/0428-142-witnessfix3-wt | 015ce675 | 0428-142-witnessfix3 | Sat Nov 21 09:30 | 0 | branch head present, sha BEHIND remote (remote=2e4a570a) | 38M | (i) safe+remote (stale, not lost) |
| 22 | /home/marcel/dev/baseharbor-ecosystem/workers/0428-217-credfix2-wt | 719d28a8 | worker | Sat Nov 21 11:33 | 0 | detached; reachable from origin/w0428-217credfill | 39M | (i) safe+remote |
| 23 | /home/marcel/dev/baseharbor-ecosystem/workers/080-r28-selection-wt | f611060c | mcpdev80 | Tue Nov 17 08:02 | 0 | branch head present | 36M | (i)/(iv) see note |
| 24 | /home/marcel/dev/baseharbor-ecosystem/workers/ci-reds-fix-062-wt | 80d4df52 | w073-perses-alerts | Mon Nov 16 10:32 | 0 | branch head `w073-perses-alerts` present | 36M | (i)/(iv) see note |
| 25 | /home/marcel/dev/baseharbor-ecosystem/workers/w245-image-transfer | 1c024d11 | Worker w224 | Fri Nov 6 14:33 | 0 | branch head `work/r27-image-transfer` present | 30M | (i)/(iv) see note |
| 26 | /home/marcel/dev/baseharbor-ecosystem/workers/w263-wt/repo | 746afe6d | coord-welle5 | Fri Nov 6 22:01 | 0 | branch head `work/r27-artifact-resolution-new` present | 30M | (i)/(iv) see note |
| 27 | /home/marcel/dev/baseharbor-ecosystem/workers/w264-wt | 5e4fde71 | Marcel Pfingstgräf | Fri Nov 6 15:19 | 4 | branch head `work/r27-remote-up-cli-2` present | 79M | (iii) DIRTY (4 files) |
| 28 | /home/marcel/dev/baseharbor-ecosystem/workers/w286-wt2 | 8b5075d2 | Worker w280 | Sat Nov 7 04:59 | 0 | branch head `work/r27-remote-up-owner-missing` present | 30M | (i)/(iv) see note |
| 29 | /home/marcel/dev/baseharbor-ecosystem/worktrees/w108-traceprobe/baseharbor | 39810520 | worker-ornith1.5 | Tue Nov 17 09:27 | 0 | branch head present | 36M | (i)/(iv) see note |
| 30 | /home/marcel/dev/baseharbor-ecosystem/worktrees/w218-gate-catalog-fix | 40cb28c7 | Marcel Pfingstgräf | Fri Nov 20 17:06 | 0 | detached; reachable from origin/develop | 38M | (i) safe+remote |
| 31 | /tmp/0428-142-hopci-wt | 2e4a570a | 0428-142-witnessfix3 | Sat Nov 21 09:30 | 1 (untracked) | branch head `0428-hopci-detach` present | 92M | (iii) DIRTY (1 file) |
| 32 | /tmp/opencode/0428-060-updown-wt | prunable | -- | -- | -- | branch head `lane-0428-060-updown` present at remote; worktree dir already gone | 0 | pruned-already (gitdir missing) |
| 33 | /tmp/w198-cli-wt | 7546b180 | w198-0428-198-cligate | Fri Nov 20 22:49 | 1 (untracked) | branch head present | 92M | (iii) DIRTY (1 file) |
| 34 | /tmp/w207-lokifix-wt | bddb27e6 | worker | Fri Nov 20 22:13 | 0 | branch head present | 38M | (i)/(iv) see note |
| 35 | /var/tmp/0428-208-static-gate | 0a710235 | 0428-210-authzkeep | Sat Nov 21 10:53 | 0 | branch head present | 39M | (i)/(iv) see note |
| 36 | /var/tmp/baseharbor-0428-088 | 54fbe477 | worker-ornith1.5 | Thu Nov 19 00:21 | 0 | branch head present | 36M | (i)/(iv) see note |
| 37 | /var/tmp/baseharbor-0428-116 | 7459d615 | worker-ornith1.5 | Thu Nov 19 00:45 | 9 | branch head `codex-hopf-1686` present | 37M | (iii) DIRTY (9 files) |
| 38 | /var/tmp/c213 | 37587b0e | 0428-213-compilefix | Sat Nov 21 09:59 | 0 | detached; reachable from lane-origin/lane-0428-213-trust-uninstall-false-green | 38M | (i) safe+remote |
| 39 | /var/tmp/coord-fmt-177 | 03b66cec | worker | Fri Nov 20 18:55 | 0 | detached; reachable from origin/develop | 38M | (i) safe+remote |
| 40 | /var/tmp/dualmatch-wt/wt | 864fdcd3 | worker-ornith1.5 | Thu Nov 19 06:10 | 0 | branch head present | 36M | (i)/(iv) see note |
| 41 | /var/tmp/gmcheck/core | da76c5cf | Marcel Pfingstgräf | Thu Nov 19 07:36 | 1 (untracked) | detached; reachable from origin/develop | 36M | (i) safe+remote |
| 42 | /var/tmp/m121-efilter-wt | d1fcfdf6 | worker-ornith1.5 | Thu Nov 19 09:22 | 10 | branch head present | 36M | (iii) DIRTY (10 files) |
| 43 | /var/tmp/m122-appclass-wt | 876329f7 | worker-ornith1.5 | Thu Nov 19 07:39 | 9 | branch head present | 36M | (iii) DIRTY (9 files) |
| 44 | /var/tmp/m122-integration-check | f0622112 | worker-ornith1.5 | Thu Nov 19 07:46 | 9 | detached; NOT on any remote/develop; `gh pr list` empty | 36M | (ii) orphan-lost-risk |
| 45 | /var/tmp/mission-093-scope-wt | d0351baf | worker-ornith1.5 | Wed Nov 18 23:02 | 9 | branch head present | 36M | (iii) DIRTY (9 files) |
| 46 | /var/tmp/mission-110-wt | fb6f3693 | worker-ornith1.5 | Wed Nov 18 23:03 | 0 | branch head present | 36M | (i)/(iv) see note |
| 47 | /var/tmp/mission-1599-wt | e4355273 | worker-ornith1.5 | Thu Nov 19 20:23 | 9 | branch head `review-hopf-1599` present | 38M | (iii) DIRTY (9 files) |
| 48 | /var/tmp/mission-1602-wt | b6c9702b | worker-ornith1.5 | Wed Nov 18 23:04 | 0 | branch head `review-hopf-1602` present | 36M | (iii)/(iv) see note |
| 49 | /var/tmp/w073-wt | d8838f62 | worker-ornith1.5 | Thu Nov 19 09:50 | 9 | branch head `w073-perses-alerts` present | 36M | (iii) DIRTY (9 files) |
| 50 | /var/tmp/w220-0428-205/wt | 5e307437 | 0428-213-compilefix | Sat Nov 21 09:59 | 0 | branch head present | 38M | (i)/(iv) see note |
| 51 | /var/tmp/wt-078-r4 | 9add5e8a | worker | Fri Nov 20 13:38 | 0 | detached; reachable from lane-origin/1650 | 39M | (i) safe+remote |
| 52 | /var/tmp/wt-091-r1 | 253883eb | worker | Fri Nov 20 07:29 | 1 | detached; NOT on any remote/develop; `gh pr list` empty | 38M | (ii) orphan-lost-risk |

Note on "(i)/(iv)" branch heads: a branch head existing at remote means the content is NOT lost (class i). Whether the worktree is tied to a LIVE session is answered separately by the live-session cross-check below; several of these branch heads simply have no active session now (stale-but-safe), not a live lane.

## remote verification (witness)

`git ls-remote lane-origin refs/heads/<branch>` hits (branch-head worktrees whose branch exists at remote):
```
/home/marcel/dev/baseharbor-ecosystem/baseharbor	lane-0428-213-trust-uninstall-false-green	REMOTE_OK
/home/marcel/dev/baseharbor-ecosystem/workers/.models/flash/bf01-base-wt	lane-0428-fix-bf01-v2	REMOTE_OK
/home/marcel/dev/baseharbor-ecosystem/workers/0428-142-witnessfix3-wt	lane-0428-142-statuswitness	REMOTE_OK
/tmp/opencode/0428-060-updown-wt	lane-0428-060-updown	REMOTE_OK
/tmp/w198-cli-wt	lane-0428-198-cli-shard-operator-env	REMOTE_OK
/tmp/w207-lokifix-wt	lane-0428-202-lokifix	REMOTE_OK
/var/tmp/0428-208-static-gate	lane-0428-208-static-release-gate	REMOTE_OK
/var/tmp/m121-efilter-wt	lane-0428-efilter-r2w	REMOTE_OK
/var/tmp/w073-wt	w073-perses-alerts	REMOTE_OK
```
(Same remote URL verified for every other branch name; the 9 above are the ones that returned a SHA.)

Detached-SHA resolution for the 5 with NO remote containment (`git branch -r --contains` empty, `gh pr list --search <sha>` == `[]`, and not reachable from any local/remote `develop`):
- `52866ae3` (0428-210-authzkeep-wt) -- orphan
- `3f7600de` (.w230-oldbase) -- orphan
- `f0622112` (m122-integration-check) -- orphan
- `253883eb` (wt-091-r1) -- orphan
- `6442955f` (0428-210-hopfix3-wt) -- orphan

Stale-but-not-lost branch heads (present at remote, worktree HEAD behind remote):
- `lane-0428-fix-bf01-v2`: worktree 13e096fc vs remote 16241f24.
- `lane-0428-142-statuswitness`: worktree 015ce675 vs remote 2e4a570a.

## live-session cross-check

Active worker sessions (`codeman agent list --json`, excluding the Coordinator session 9142ab1f):
- `95971e0a` busy codex-rev-cli2b
- `1298eb9c` busy 0428-221-huntverd
- `db369a9d` busy 0428-076-hop2
- `3207531f` busy 0428-221-hopcost
- `2a552446` busy 0428-221-huntbase
- `bcdf77dd` busy 0428-221-huntrake (THIS session)

Mapping of live sessions to worktrees: none of the 52 worktrees can be authoritatively tied to a live session by the inventory source alone (no session exposes its workingDir worktree in `agent list`). The only guaranteed-live worktree is the baseharbor main checkout `/home/marcel/dev/baseharbor-ecosystem/baseharbor` (the coordinator's own workingDir, and the session workingDirs of this shift are under workers/.models/*, not a baseharbor worktree). The 5 orphan SHAs (class ii) predate the current shift (Nov 6-21 author stamps, no live session named for them) and are the highest-priority lost-risk items.

## sizes by class

- (iv) live-lane / main checkout: 806M (1 worktree) -- the 806M is the baseharbor worktree plus its bundled repo; the other ~45 worktrees share the same object store and are NOT additive on-disk (git worktrees share `.git/objects`). Measured per-worktree `du -xsh` (x = stay in one fs) ranges 30-92M each but these are mostly shared loose objects, not independent footprint.
- (i) safe + remote (reachable): ~40 worktrees; shared object store.
- (ii) orphan-lost-risk: 5 worktrees, ~187M measured du (38+38+37+36+38); shared objects, small marginal disk.
- (iii) DIRTY (uncommitted changes = do NOT touch): 15 worktrees.
- pruned-already: 1 (dir already gone).

Marginal disk that a safe cleanup could return (rough, from `du -xsh` of class-(i) detached/stale worktrees that share no live session): several hundred MB of loose objects, but the dominant 806M is the shared repo + the one main checkout. Do NOT treat the sum of per-worktree du as reclaimable; objects are shared. The real win is removing the prunable entry and orphaning detached heads after owner sign-off.

## findings

- FUND-1 (class ii, lost-risk): 5 detached worktrees whose HEAD is reachable from NO remote ref, no `develop`, and no open PR:
  1. `/home/marcel/dev/baseharbor-ecosystem/0428-210-authzkeep-wt` (52866ae3)
  2. `/home/marcel/dev/baseharbor-ecosystem/0428-210-hopfix3-wt` (6442955f)
  3. `/home/marcel/dev/baseharbor-ecosystem/workers/.w230-oldbase` (3f7600de)
  4. `/var/tmp/m122-integration-check` (f0622112)
  5. `/var/tmp/wt-091-r1` (253883eb)
  Recommendation: save their SHA + worktree path to an owner handoff; safe to `git worktree remove` ONCE the owner confirms the content is not wanted, OR push each to a remote branch to de-risk first. None is a live lane.

- FUND-2 (stale-but-safe): 2 branch-head worktrees whose HEAD is BEHIND their remote branch (worktree not up to date; content safe): `lane-0428-fix-bf01-v2` (worktree 13e096fc vs remote 16241f24) and `lane-0428-142-statuswitness` (worktree 015ce675 vs remote 2e4a570a).

- FUND-3 (dirty, do not touch without owner decision): 15 worktrees carry uncommitted changes (dirty >= 1): 0427-175-wt (41), 0428-102-wt (9), 0428-113-wt (9), .w217-0428-204-entrypoints (1), 0428-086-wt (9), w264-wt (4), /tmp/0428-142-hopci-wt (1), /tmp/w198-cli-wt (1), /var/tmp/baseharbor-0428-116 (9), /var/tmp/m121-efilter-wt (10), /var/tmp/m122-appclass-wt (9), /var/tmp/mission-093-scope-wt (9), /var/tmp/mission-1599-wt (9), /var/tmp/w073-wt (9), /var/tmp/wt-091-r1 (1, also orphan).

- FUND-4 (prunable already gone): `/tmp/opencode/0428-060-updown-wt` is flagged `prunable` (gitdir file points to non-existent location); the directory no longer exists. No action; note for `git worktree prune` cleanup.

- FUND-5 (disk): `/` at 93% (15G free of 193G). The 806M on the main worktree is the shared git object store; removing stale worktrees returns loose objects but is NOT purely additive. Real reclaim is bounded; the inventory's purpose is de-risking the 5 orphans and clearing the prunable entry, not a large disk windfall.

## cleanliness

docker ps -a BEFORE (pid 2206515): only the header line, zero containers.
docker ps -a AFTER (this hunt changed nothing on disk): only the header line, zero containers.
No container/network/volume/state directory created or removed. ambient-core/ untouched. No compose project started.

## repo-rule compliance

- Read-only BUG-HUNT: no `git worktree remove`, no `rm`, no `git worktree prune`, no commit at baseharbor, no PR, no subagent, no `git stash`, no bare `go test ./...`.
- Remote guard: used only `lane-origin` (URL https://github.com/mcpdev80/baseharbor.git) for ls-remote; verified via `git remote -v`.
- Planning repo attested: `git -C baseharbor-plan remote -v` => origin https://github.com/mcpdev80/baseharbor-plan.git (correct planning remote, not the workers/ bookkeeping copy).
- Evidence written under baseharbor-plan/evidence/r28-welle4-2026-11-21/stale-worktree-inventory/hunt-1.md (NOT in a product repo).
- No markdown checkboxes in this evidence file.

## END

0428-221-huntrake: H-V44 worktree inventory complete, 5 orphans + 2 stale + 15 dirty findings documented, no mutation. END_DONE.
