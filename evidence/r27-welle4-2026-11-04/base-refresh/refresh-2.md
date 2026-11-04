# w148 base-refresh — Evidence

Lane: w148 (Worker). Coord: f49a3303. Mission: only lift the base of three baseharbor branches by merging origin/develop into each. No content changes, no tests rewritten, no .github, no AGENTS.md, no subagents. PRs stay the same (heads auto-update, PRs not closed).

## PLAN

- Step 1: Verify each of the three branches exists with the exact head named in the mission (ls-remote witness).
- Step 2: Branch 1 work/w96-production-wiring-f8ef4255 — inspect git log (check for new kaeltestart-fix commits from runde-5 lane), then merge origin/develop (no rebase, no force). Push normal, ls-remote against real remote, log --oneline origin/develop..HEAD shows only own commits + one merge commit.
- Step 3: Branch 2 work/r27-native-auth (head 848d9512728) — merge origin/develop, push, verify.
- Step 4: Branch 3 behind PR #1369 / team-auth (work/w92-team-auth-claim-mapping, head a7fa573d5b) — merge origin/develop, push, verify.
- Step 5: Record per-branch before-head, after-head, literal ls-remote line, and the log line.
- Step 6: Publish END to f49a3303 via codeman agent post.

## repo-rule compliance

- Mission scope: only base lift (merge develop), no content changes.
- No .github edits, no reruns/workflow_dispatch.
- No AGENTS.md touched (restored a foreign staged AGENTS.md deletion in branch-1 worktree before merging so it never entered history).
- No subagents (Owner directive 2026-11-04).
- One integration candidate per chain; stayed on the three named branch names, no new branches invented.
- No force push, no rebase (all merges were --no-ff fast-forward-safe merges, clean, no conflicts).

## RESULTS

### Branch 1: work/w96-production-wiring-f8ef4255 (PR #1371)

- before-head: f4ec625f801464cdf3128299dee1396b7d8c5dfc
- after-head: eb2835346acf1d57256d96d816abd1082d656bea
- develop already contained ea3fb38e? yes (develop's own head; ea3fb38e now an ancestor, rc=0)
- conflict? no (clean --no-ff merge)
- ls-remote (real remote): `eb2835346acf1d57256d96d816abd1082d656bea  refs/heads/work/w96-production-wiring-f8ef4255`
- git log --oneline origin/develop..HEAD: only own commits (f4ec625f review-1371b, c1b1c3dc, 8d3531f0, dcbdd5c2, 9ac4e2c4, 589baf0e, af05b198, fb701991) + 1 new merge commit eb283534. No foreign head.
- merge commit parents: eb283534 parent1=f4ec625f parent2=ea3fb38e (develop merged in)
- push: f4ec625f..eb283534 (normal push, no force)
- PR #1371 head now: eb2835346acf1d57256d96d816abd1082d656bea (auto-updated, PR not closed)

Note on runde-5 lane: branch head f4ec625f is the w143 lane's own commit "review-1371b"; no new kaeltestart-fix commit appeared on the branch, so nothing to protect. The staged AGENTS.md deletion (14 lines removed) in the worktree was foreign work — restored to staged-clean and working-tree before merging so it never entered the branch history.

### Branch 2: work/r27-native-auth (PR #1362, head 848d9512728)

- before-head: 848d951272834155418bf88d26864b70f8a922c8
- after-head: 2209436c806208a3a60aa36a10fbec0d62558118
- develop already contained ea3fb38e? no before merge; ea3fb38e now an ancestor (rc=0)
- conflict? no (clean --no-ff merge)
- ls-remote (real remote): `2209436c806208a3a60aa36a10fbec0d62558118  refs/heads/work/r27-native-auth`
- git log --oneline origin/develop..HEAD: only own commits (848d9512, ad0ea646, 6cd8c3e6, 7abcc441, 0a67092c, 9faf95f3, a3eee132, 0958107f, 5fee8072, 8f4cbd2b, c2adcc86, ed0c99b1, 3c17b24b) + 1 new merge commit 2209436c. No foreign head.
- merge commit parents: 2209436c parent1=848d9512 parent2=ea3fb38e (develop merged in)
- push: 848d9512..2209436c (normal push, no force)
- PR #1362 head now: 2209436c806208a3a60aa36a10fbec0d62558118 (auto-updated, PR not closed)

### Branch 3: work/w92-team-auth-claim-mapping (PR #1369 team-auth, head a7fa573d5b)

- before-head: a7fa573d5bff6e043fbecbb2aeb79833605dc304
- after-head: 6ec7a5db8e116da928cb90bb5ce9b2879529cf02
- develop already contained ea3fb38e? no before merge; ea3fb38e now an ancestor (rc=0)
- conflict? no (clean --no-ff merge)
- ls-remote (real remote): `6ec7a5db8e116da928cb90bb5ce9b2879529cf02  refs/heads/work/w92-team-auth-claim-mapping`
- git log --oneline origin/develop..HEAD: only own commits (a7fa573d, f9507ff6, c8c45667, 815fdfb7, 689689e3, bfaddb37, 1043d12d, 73a75b5e, 87c67b75, 428e0451) + 1 new merge commit 6ec7a5db. No foreign head.
- merge commit parents: 6ec7a5db parent1=a7fa573d parent2=ea3fb38e (develop merged in)
- push: a7fa573d..6ec7a5db (normal push, no force)
- PR #1369 head now: 6ec7a5db8e116da928cb90bb5ce9b2879529cf02 (auto-updated, PR not closed)

## AUTHORITATIVE WITNESS

ls-remote (fresh) against https://github.com/mcpdev80/baseharbor.git:
- eb2835346acf1d57256d96d816abd1082d656bea  refs/heads/work/w96-production-wiring-f8ef4255
- 2209436c806208a3a60aa36a10fbec0d62558118  refs/heads/work/r27-native-auth
- 6ec7a5db8e116da928cb90bb5ce9b2879529cf02  refs/heads/work/w92-team-auth-claim-mapping

Each new merge commit's parents (definitive proof develop was merged in):
- eb283534 parent1=f4ec625f parent2=ea3fb38e
- 2209436c parent1=848d9512 parent2=ea3fb38e
- 6ec7a5db parent1=a7fa573d parent2=ea3fb38e

ea3fb38e (develop) is an ancestor of all three new remote heads (rc=0 for each).

## END

END lane w148 base-refresh: e1371=eb2835346e e1362=2209436c80 e1369=6ec7a5db8e lsremote-ok=ja | alle drei Zweige develop (ea3fb38e) per clean --no-ff Merge eingebasst, normal gepushed (kein Force/kein Rebase), PR-HEADs haben sich selbst aktualisiert, PRs nicht geschlossen, kein Contents-Wechsel, kein .github/AGENTS.md/Subagent.
