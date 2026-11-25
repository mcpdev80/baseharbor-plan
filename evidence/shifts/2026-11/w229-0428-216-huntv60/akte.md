# w229-0428-216-huntv60 — STACK-CONSISTENCY DESK (ancestry-test only)

## Lane identity / visible Ansatz block

- card: 0428-216 (t-20261121-stale-pr-hop-and-baserefs)
- git author name used for plan evidence commits: `w229-0428-216-huntv60`
- git author email: `w229-0428-216-huntv60@baseharbor.local`
- commit invocation: `git -c user.name=w229-0428-216-huntv60 -c user.email=w229-0428-216-huntv60@baseharbor.local commit`
- pre-push gate line: `git show -s --format=%an HEAD` must equal `w229-0428-216-huntv60`
- owner-verbatim frontmatter owner (fetched from origin/main at runtime): `w233-0428-216-prsweep` (from tasks/t-20261121-stale-pr-hop-and-baserefs.md)

## Evidence repo attestation

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:
```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
upstream2	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
upstream2	https://github.com/mcpdev80/baseharbor-plan.git (push)
```
Planning repo confirmed as `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY (not workers/baseharbor-plan).

## Base attestation (fetch witnesses)

`git ls-remote origin/develop` on /tmp/opcode_hunt (fresh clone, github remote = origin):
```
fcd449117e189c555c7530b9527cd22d3f6f25ff	refs/heads/develop
```
All PR heads fetched into /tmp/opcode_hunt via `git fetch origin pull/N/head:refs/pull/N/head`.

## PR metadata (fetched live via github API /pulls/N)

| PR | title | state | base_ref | base_sha | head_sha | head_label |
| --- | --- | --- | --- | --- | --- | --- |
| 1842 | chore(release): bump demo_ref pin | open | develop | 3a2ae6b1139570c98b8924e3b19975c56a289400 | 48bac372f9f006c964309fab958e569a7ce076a0 | w177-0428-284-demo-pin-1812 |
| 1812 | fix(ci): re-load missing runtime image | open | develop | 28296a2e6e920592741c9397486358deac7e95b2 | f166a49f2634cbcbda3a513bfe4e9085059fb408 | lane-0428-249-runtime-image-fix |
| 1819 | 0428-181 wire Perses identity dashboard | open | develop | 28296a2e6e920592741c9397486358deac7e95b2 | b3c5055ad2566b639c2b0d4f4c2848b045221ebf | w54-0428-181-export |
| 1820 | fix(0428-271): prove exact runtime broker commit | open | develop | 28296a2e6e920592741c9397486358deac7e95b2 | 34142a2a0a81d8932e23ce00920bb8c39758a097 | fix/broker-build-identity |
| 1818 | fix(0428-078): consume real Perses probe | open | develop | 3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd | 20fc1cb7d49602dc7f8aa0004a7562a81311d78c | lane-0428-078-cf-fix |
| 1833 | fix(0428-288): preserve Compose service IDs | open | develop | f7540e591609e0db6453e9b690fbb5d6686448a2 | a7b0a48048c11d20234160eede941532ddc33156 | lane-0428-288-compose-ids |
| 1650 | fix(0428-078): wire Perses identity-keycloak | open | develop | 3a2ae6b1139570c98b8924e3b19975c56a289400 | 1c33e910070a07a6d4105f0d38e3c89988a788a3 | lane-0428-078-perses-identity-on-resolver |

## depends_on (declared base card per PR, from task-note frontmatter)

| card | PR(s) | depends_on (task-note) |
| --- | --- | --- |
| 0428-249 | 1812 | t-20261124-r28-release-candidate-testonly-binary |
| 0428-181 | 1819 | t-20261114-r28-identity-dashboard-catalog-consumer |
| 0428-271 | 1820 | t-20261124-r28-broker-build-identity-commit |
| 0428-078 | 1818, 1650 | t-20261114-r28-perses-dashboard-selection |
| 0428-284 | 1842 | [] |
| 0428-288 | 1833 | [] |

The operative chain from the mission: #1812 → #1819 → #1820 (stacked; successor base must equal predecessor head).

## Ancestry test — per PR vs its declared base SHA

Command: `git merge-base --is-ancestor <base_sha> refs/pull/N/head` (via refs/pull/N/head fetches).

| PR | base_sha | head_sha | base is ancestor of head? | merge-base(base,head) |
| --- | --- | --- | --- | --- |
| 1842 | 3a2ae6b1… | 48bac372… | YES | 3a2ae6b1… (== base) |
| 1812 | 28296a2e… | f166a49f… | YES | 28296a2e… (== base) |
| 1819 | 28296a2e… | b3c5055a… | YES | 28296a2e… (== base) |
| 1820 | 28296a2e… | 34142a2a… | YES | 28296a2e… (== base) |
| 1818 | 3ebfb90d… | 20fc1cb7… | YES | 3ebfb90d… (== base) |
| 1833 | f7540e59… | a7b0a480… | YES | f7540e59… (== base) |
| 1650 | 3a2ae6b1… | 1c33e910… | YES | 3a2ae6b1… (== base) |

All 7 PRs are internally consistent with their declared base SHA: the base is reachable in the head.

## Ancestry test — vs current develop (staleness)

Command: `git merge-base --is-ancestor <origin/develop> refs/pull/N/head`; `origin/develop = fcd449117e189c555c7530b9527cd22d3f6f25ff`.

| PR | head_sha | head at/after current develop? | commits ahead of develop | shared-ancestor w/ develop |
| --- | --- | --- | --- | --- |
| 1842 | 48bac372… | NO — BEHIND develop | 5 | 3a2ae6b1… (stale develop tip) |
| 1812 | f166a49f… | NO — BEHIND develop | 8 | 28296a2e… (stale) |
| 1819 | b3c5055a… | NO — BEHIND develop | 11 | 28296a2e… (stale) |
| 1820 | 34142a2a… | NO — BEHIND develop | 5 | 28296a2e… (stale) |
| 1818 | 20fc1cb7… | NO — BEHIND develop | 4 | 3ebfb90d… (stale) |
| 1833 | a7b0a480… | NO — BEHIND develop | 6 | f7540e59… (stale) |
| 1650 | 1c33e910… | NO — BEHIND develop | 9 | 3a2ae6b1… (stale) |

All 7 PR heads are NOT descendants of current develop; each was cut from an older develop tip (shared-ancestor != fcd44911). Each needs a rebase onto current develop before acceptance.

## Cross-PR stack ancestry (the disease model)

Command: `git merge-base --is-ancestor refs/pull/PRED/head refs/pull/SUCC/head` for all PRED ≠ SUCC.

Result: NO PR head is an ancestor of any other PR head. The 7 heads are 7 disjoint subtrees off 4 distinct develop tips.

| successor | is descendant of any predecessor head? |
| --- | --- |
| 1820 | NO (not of 1819, 1812, 1818, 1833, 1650, 1842) |
| 1819 | NO |
| 1833 | NO |
| 1818 | NO |
| 1812 | NO |
| 1842 | NO |
| 1650 | NO |

## The #1819→#1820 disease (pre-hop build off a PRE-HOP branch)

Mission disease ref: #1820@28803d11 vs #1819@b3c5055. `28803d11` resolves to a real commit in the repo:
`28803d11 fix(0428-271): add dev/edge + empty-commit acceptance criterion 2 regression`, parent `514084f3`.

Findings:

- `28803d11` (pre-hop #1820) is NOT a descendant of #1819 head `b3c5055`. `git merge-base --is-ancestor b3c5055 28803d11` → NO. Pre-hop #1820 was cut off a branch that predates #1819.
- Pre-hop #1820 base was `514084f3` (its parent), a develop tip that does NOT contain #1819.
- Current #1820 head `34142a2a` carries the pre-hop commits forward (`git merge-base --is-ancestor 28803d11 34142a2a` → YES) but its top commit is a rebase: `34142a2a hop(0428-271): merge develop into 1820 candidate after #1819 stack (guarded-forward-diamond)`.
- Despite the "after #1819 stack" message, current #1820 head `34142a2a` does NOT contain #1819 head `b3c5055`: `git merge-base --is-ancestor b3c5055 34142a2a` → NO. merge-base(1820head, 1819head) = `28296a2e` (the old develop base), i.e. the two share the OLD base and are still siblings, not stacked.
- 0 of the 1819 unique commits are reachable from current 1820 head; they share only the base `28296a2e`.

Conclusion: #1820 was originally built off a pre-1819 branch (pre-hop `28803d11`), then re-based onto develop. The rebase put 1820 back at develop level (base 28296a2e), so it is a SIBLING of #1819, not a successor. The stack link #1819→#1820 is broken: 1820 must be rebuilt so its base is #1819 head `b3c5055` (or #1812 head if the stack root is 1812) before it can be accepted as the chain successor.

## Restack required per flag

- #1820: NOT a descendant of #1819 → must cut a fresh 0428-271 candidate whose base is #1819 head `b3c5055ad2566b639c2b0d4f4c2848b045221ebf` (current), rebased onto current develop `fcd449117e189c555c7530b9527cd22d3f6f25ff` tip, carrying forward the 0428-271 implementation (current 34142a2a already carries 28803d11). This is the one flag that needs an active restack. Feeds w231 (#1820 restack, already drafted).
- #1819, #1812, #1818, #1833, #1650, #1842: clean per-PR base, internally consistent; only develop-staleness. Each needs a rebase onto current develop `fcd44911` before acceptance; no cross-PR restack required (no successor relationship proven).

## No product commits, no card writes, no pushes

- No edits to product code, .github/**, or cards. No PR opened. No force-push.
- Evidence lives only in baseharbor-plan (plan-PR flow), never in a product repo.

## Plan-PR publish flow (ENDING)

- Publish akte via plan-PR flow: create a plan-PR with this akte, squash-merge, then verify the path exists on origin/main via ls-tree.
- BRANCH-ONLY akte does not release the seat — must confirm ls-tree witness.

## Cleanliness

`docker ps -a` before: (no docker run)
`docker ps -a` after: (no docker run)
Cleanliness: no containers, networks, volumes, or state directories created. No compose project started. No ambient-core images touched. Reverted /tmp/opcode_hunt is a throwaway clone under /tmp (outside the ecosystem root), no changes committed to any product repo.

## END

END_DONE w229-0428-216-huntv60: ancestry-test table complete. #1820 flagged as the pre-hop disease (built off pre-1819 branch, now a sibling of #1819, needs restack onto #1819 head); other 6 PRs clean-per-base + develop-stale. Feeds w231.
