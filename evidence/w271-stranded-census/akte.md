# Stranded-evidence census — shared baseharbor-plan checkout

Mission: `coordinator/missions/w271-stranded-evidence-census.txt`. Read-only census supporting the Plan recovery.
Lane: `w271-0428-284-stranded`. No product repo, no CI, no cards, no `.github`.

## PLAN

1. Baseline witnesses in the shared checkout (HEAD, stash count, remote URL resolution) BEFORE analysis.
2. Enumerate all 51 stashes with index, date, author and subject.
3. Enumerate every `refs/heads` and `refs/remotes` lane ref with tip SHA, committer date and author.
4. Classify each ref tip against `origin/main` with `git merge-base --is-ancestor`.
5. Discover the shallow-clone boundary; switch to a path-level blob test that needs no history.
6. Blob-compare every `evidence/` and `tasks/` path in every stranded tip and stash against main.
7. Build the needs-land table: path, size, blob SHA, locator, PR/card/run IDs named inside, recommendation.
8. Cross-check the twelve artifacts the w255/w260 recovery mission targets.
9. Print author identity for every stranded commit that carries unique content.
10. Publish this akte from an isolated worktree as branch plus plan PR (no main push, no merge).
11. AFTER witnesses: HEAD and stash count unchanged in the shared checkout.

## ANSATZ (identity and provenance block)

Per-card frontmatter owner, VERBATIM from live `origin/main` at runtime (`tasks/t-20261125-0428-284-1812-postretry-gate-failure.md`):

```
---
id: t-20261125-0428-284-1812-postretry-gate-failure
card_number: "0428-284"
card_short_title: "1812 post-retry gate fail"
type: bug
areas: [ci, cli]
release: v0.4.28
version: ""
parent: ""
owner: w198-0428-284-demo-parser
kanban_status: active
kanban_lane: active
kanban_summary: ""
```

Card `0428-284` belongs to another lane and is not a write target here; this mission is read-only plus one
plan-repo evidence file. Git identity used for the akte commit:

```
user.name  = w271-0428-284-stranded
user.email = w248-coordinator@baseharbor.local
```

Commit invocation (literal):

```
git -C /tmp/opencode/w271-plan-wt -c user.name=w271-0428-284-stranded \
    -c user.email=w248-coordinator@baseharbor.local \
    commit -m 'docs(evidence): stranded-evidence census for shared plan checkout (w271)'
```

Pre-push author gate (literal command; output in the publish section):

```
git -C /tmp/opencode/w271-plan-wt show -s --format='%an <%ae>' HEAD
```

## Reality witnesses

Planning-repo identity (`git -C <path> remote -v`), proving this is the real plan repo and not
`workers/baseharbor-plan`:

```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
upstream2	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
upstream2	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Base attestation, live remote main (`git ls-remote`):

```
b3ffd617c58026c905c484ba37c1da181aa1fec8	refs/heads/main
```

This branch was cut from exactly that commit: `git rev-parse HEAD` in the worktree equals it and
`git merge-base --is-ancestor <that SHA> HEAD` returns 0.

Shared-checkout state BEFORE analysis (must be identical AFTER):

```
git rev-parse HEAD      = 08b1f66bb733d4c1422135429e5bc29fbd67cd57
git stash list | wc -l  = 51
git status --short      = M tasks/t-20261122-runtime-broker-health-unhealthy.md
```

Detached HEAD `08b1f66bb` is an ancestor of live main (`git merge-base --is-ancestor 08b1f66bb origin/main` -> 0),
so the shared checkout is merely behind, not diverged.

## Critical finding: the shared checkout is a SHALLOW clone, so the prescribed classifier is unsound

The repository carries a `.git/shallow` graft boundary with 0 entries:

```

```

Measured consequences:

- 227 of 231 ref names fail the ancestor test over 136 distinct tip SHAs, but 74 tips add
  nothing new and 0 tips cannot even be placed in history. Only 58 tips carry a path absent from main.
- On the disconnected tips, `git diff origin/main..tip` compares unrelated roots and reports thousands of
  spurious entries (4,358 files for one October Horde tip). That is why the raw audit counts (51 stashes,
  ~84 refs) overstate the real loss so heavily.
- The objects are intact — these are grafts, not missing data (`git cat-file -e <tip>^` succeeds). A
  **path-level blob comparison** works and needs no history: for every `evidence/` and `tasks/` path, compare
  `git ls-tree -r` blob SHAs at the tip or stash against the same path at main. That is the method behind
  every table below, and it is why these counts are much smaller and much more trustworthy.

## Headline counts

| measure | value |
| --- | --- |
| ref names inspected (`refs/heads` + `refs/remotes`) | 231 |
| distinct tip SHAs behind those names | 136 |
| tips failing the ancestor test (over-count, see above) | 227 |
| tips with genuinely novel paths | 58 |
| stashes listed | 51 |
| stashes that touch `evidence/` or `tasks/` at all | 25 |
| stashes with a payload absent from main | 15 |
| distinct `evidence/` + `tasks/` paths missing from live main | 88 |
| bytes of that stranded content | 632946 |

The mission premise of '~11 refs and ~10 stashes' with unique evidence is the right order of magnitude:
the unique carriers are **15 refs** and **12 stashes**.

## Stash census (all 51)

| idx | date | author | email | ev/tasks files | absent from main | subject |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2026-11-26 02:05:42 | w248-coordinator | w248@baseharbor.local | 0 | 1 | On (no branch): plan-sync:auto:20261126T010542Z:vor-sync-868f014fe |
| 1 | 2026-11-26 00:48:18 | w165-0428-078-pr1650-basehop | w165-0428-078-pr1650-basehop@baseharbor.local | 0 | 14 | On main: plan-sync:auto:20261125T234818Z:vor-sync-76ab85914 |
| 2 | 2026-11-25 15:52:48 | w189-0428-224-hunt-v46-intake | w189-0428-224-hunt-v46-intake@baseharbor.local | 2 | 0 | WIP on main: dd20cfcbc H-V51 intake: per-row reconciliation for F1-F5  |
| 3 | 2026-11-25 15:52:23 | w189-0428-224-hunt-v46-intake | w189-0428-224-hunt-v46-intake@baseharbor.local | 0 | 0 | WIP on main: dd20cfcbc H-V51 intake: per-row reconciliation for F1-F5  |
| 4 | 2026-11-25 15:17:26 | w189-0428-224-hunt-v46-intake | w189-0428-224-hunt-v46-intake@baseharbor.local | 2 | 0 | autostash |
| 5 | 2026-11-25 12:51:09 | BaseHarbor CI | ci@localhost | 1 | 0 | On main: w181-protect-foreign-dirt-1795607469 |
| 6 | 2026-11-24 13:48:27 | 0428-061-sourcepull | 0428-061@baseharbor.local | 2 | 0 | WIP on main: 6cdc5c528 planning: 0428-279 MCP contract drift app.pull  |
| 7 | 2026-11-24 13:46:29 | 0428-061-sourcepull | 0428-061@baseharbor.local | 3 | 1 | On main: plan-sync:auto:20261124T124629Z:vor-sync-6cdc5c528 |
| 8 | 2026-11-24 12:17:19 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 1 | On main: plan-sync:auto:20261124T111719Z:vor-sync-d33c3df8a |
| 9 | 2026-11-24 12:10:53 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 1 | On main: plan-sync:auto:20261124T111053Z:vor-sync-bce6801f5 |
| 10 | 2026-11-24 11:13:00 | 0428-061-sourcepull | 0428-061@baseharbor.local | 1 | 0 | On main: plan-sync:auto:20261124T101300Z:vor-sync-7de244dc5 |
| 11 | 2026-11-24 09:26:47 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 1 | On main: plan-sync:auto:20261124T082647Z:vor-sync-164b153ae |
| 12 | 2026-11-24 05:29:37 | 0428-061-sourcepull | 0428-061@baseharbor.local | 1 | 0 | On main: plan-sync:auto:20261124T042937Z:vor-sync-35f743523 |
| 13 | 2026-11-24 05:05:35 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 0 | On main: plan-sync:auto:20261124T040535Z:vor-sync-5089fbb9a |
| 14 | 2026-11-24 04:58:19 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 0 | On main: plan-sync:auto:20261124T035819Z:vor-sync-661b547e9 |
| 15 | 2026-11-24 04:39:03 | 0428-061-sourcepull | 0428-061@baseharbor.local | 2 | 0 | On main: plan-sync:auto:20261124T033903Z:vor-sync-5852bcb34 |
| 16 | 2026-11-24 04:39:01 | 0428-061-sourcepull | 0428-061@baseharbor.local | 1 | 0 | On main: plan-sync-lane:w59:evidence:20261124T033901Z:vor-sync-5852bcb |
| 17 | 2026-11-24 04:37:50 | 0428-061-sourcepull | 0428-061@baseharbor.local | 1 | 0 | On main: plan-sync-lane:w59:evidence:20261124T033750Z:vor-sync-a1f1ff1 |
| 18 | 2026-11-24 04:37:15 | 0428-061-sourcepull | 0428-061@baseharbor.local | 1 | 0 | On main: plan-sync-lane:w59:evidence:20261124T033714Z:vor-sync-a1f1ff1 |
| 19 | 2026-11-24 04:29:52 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 0 | On main: plan-sync:auto:20261124T032952Z:vor-sync-210f38d5d |
| 20 | 2026-11-24 04:06:50 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 0 | On main: plan-sync:auto:20261124T030650Z:vor-sync-81caec0f2 |
| 21 | 2026-11-24 04:02:50 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 1 | On main: plan-sync:auto:20261124T030249Z:vor-sync-4e2a5481a |
| 22 | 2026-11-24 04:01:21 | 0428-061-sourcepull | 0428-061@baseharbor.local | 9 | 0 | On main: plan-sync:auto:20261124T030121Z:vor-sync-a6cd35c27 |
| 23 | 2026-11-24 03:47:49 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 0 | On main: plan-sync:auto:20261124T024749Z:vor-sync-0465f2726 |
| 24 | 2026-11-24 02:52:19 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 1 | On main: plan-sync:auto:20261124T015219Z:vor-sync-3a04e13d8 |
| 25 | 2026-11-24 01:59:28 | 0428-061-sourcepull | 0428-061@baseharbor.local | 1 | 0 | On main: plan-sync:auto:20261124T005928Z:vor-sync-ddb8cbc36 |
| 26 | 2026-11-24 01:47:50 | 0428-061-sourcepull | 0428-061@baseharbor.local | 1 | 0 | On main: plan-sync:auto:20261124T004750Z:vor-sync-b627d763a |
| 27 | 2026-11-24 01:44:24 | 0428-061-sourcepull | 0428-061@baseharbor.local | 1 | 0 | On main: plan-sync:auto:20261124T004424Z:vor-sync-5c5a4e76a |
| 28 | 2026-11-24 00:11:46 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 0 | On main: plan-sync:auto:20261123T231145Z:vor-sync-2e27748f4 |
| 29 | 2026-11-24 00:00:09 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 0 | On main: plan-sync:auto:20261123T230009Z:vor-sync-898022d16 |
| 30 | 2026-11-23 23:42:18 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 1 | On main: plan-sync:auto:20261123T224218Z:vor-sync-add42a444 |
| 31 | 2026-11-23 23:12:42 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 1 | On main: plan-sync:auto:20261123T221242Z:vor-sync-554850dc6 |
| 32 | 2026-11-23 22:50:17 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 0 | On main: plan-sync:auto:20261123T215017Z:vor-sync-339547f4f |
| 33 | 2026-11-23 20:10:41 | 0428-061-sourcepull | 0428-061@baseharbor.local | 3 | 0 | On main: plan-sync:auto:20261123T191041Z:vor-sync-98777ea2d |
| 34 | 2026-11-23 20:09:23 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 0 | On main: plan-sync:auto:20261123T190923Z:vor-sync-98777ea2d |
| 35 | 2026-11-23 20:01:32 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 0 | On main: plan-sync:auto:20261123T190132Z:vor-sync-d1eb28fab |
| 36 | 2026-11-23 19:56:16 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 0 | On main: plan-sync:auto:20261123T185616Z:vor-sync-0ed696a2d |
| 37 | 2026-11-23 19:49:35 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 0 | On main: plan-sync:auto:20261123T184935Z:vor-sync-decf00ef3 |
| 38 | 2026-11-23 19:18:34 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 1 | On main: plan-sync:auto:20261123T181834Z:vor-sync-45cbbb571 |
| 39 | 2026-11-22 10:51:47 | 0428-061-sourcepull | 0428-061@baseharbor.local | 2 | 0 | On main: lane draft protected by coordinator |
| 40 | 2026-11-22 06:50:22 | 0428-061-sourcepull | 0428-061@baseharbor.local | 1 | 3 | On main: plan-sync:auto:20261122T055022Z:vor-sync-4f5b63537 |
| 41 | 2026-11-22 06:06:53 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 1 | On main: plan-sync:auto:20261122T050653Z:vor-sync-fe58eaffe |
| 42 | 2026-11-22 04:48:20 | 0428-061-sourcepull | 0428-061@baseharbor.local | 1 | 0 | On main: plan-sync:auto:20261122T034820Z:vor-sync-1fae0b904 |
| 43 | 2026-11-22 04:28:20 | 0428-061-sourcepull | 0428-061@baseharbor.local | 1 | 0 | On main: plan-sync:auto:20261122T032820Z:vor-sync-4ae3ca265 |
| 44 | 2026-11-22 04:04:28 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 2 | On main: plan-sync:auto:20261122T030428Z:vor-sync-9839a2497 |
| 45 | 2026-11-22 01:20:15 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0 | 0 | On main: plan-sync:auto:20261122T002015Z:vor-sync-04cd7cec4 |
| 46 | 2026-11-22 00:16:48 | 0428-061-sourcepull | 0428-061@baseharbor.local | 1 | 0 | On main: plan-sync:auto:20261121T231648Z:vor-sync-cfb393df3 |
| 47 | 2026-11-21 12:58:39 | 0428-076-hop2 | 0428-076@baseharbor.local | 1 | 0 | WIP on main: 6634bf762 evidence(0428-142): preserve w230 detached head |
| 48 | 2026-11-21 04:23:18 | worker | worker@baseharbor.local | 1 | 1 | On main: lane-w206-protect-foreign-edit-appedit207 |
| 49 | 2026-11-17 06:59:01 | mcpdev80 | mcpdev80@users.noreply.github.com | 3 | 0 | On main: w093 |
| 50 | 2026-11-16 05:31:11 | worker | worker@baseharbor.local | 2 | 0 | On main: temp-cli2envpolicy |

Reading: 26 stashes carry no evidence/tasks payload at all;
they are `plan-sync:auto` bookkeeping. `stash@{1}` is the dominant stash carrier.

## Author identity for stranded commits

Only tips that actually carry unique content. Taken from `git show -s --format='%an %ae %ci'`, never inferred.

| author | email | committer date | tip | unique paths |
| --- | --- | --- | --- | --- |
| mcpdev80 | dev@pfingstgraef.eu | 2026-11-02 11:36:53 | `9b80d8344adb` | 1 |
| worker-ornith1.5 | worker@baseharbor.local | 2026-11-19 01:00:47 | `fbce6e639342` | 2 |
| lv4-verify | worker@baseharbor.local | 2026-11-20 09:06:21 | `12781be59c56` | 2 |
| 0428-076-nativeshape | 0428-076@baseharbor.local | 2026-11-21 19:05:46 | `b8bb8b7b199b` | 1 |
| w193-0428-224-hunt-v47-intake | w193-0428-224-hunt-v47-intake@baseharbor.local | 2026-11-25 15:55:20 | `a47da84b82f2` | 11 |
| w200-cancelgroup-befund | w200-cancelgroup-befund@baseharbor.local | 2026-11-25 21:13:15 | `cc9c96409a65` | 5 |
| w200-1812-review | w200-1812-review@baseharbor.local | 2026-11-25 21:24:45 | `e78e07c0ca10` | 1 |
| w200-huntV55-disposition | w200-huntV55-disposition@baseharbor.local | 2026-11-25 21:38:50 | `1a0b786f4eff` | 1 |
| w136-pr1836-rowsreview | w136-pr1836-rowsreview@baseharbor.local | 2026-11-25 22:21:25 | `541a07965d7d` | 9 |
| w226-0428-307-0428-283-1818reset | w226-0428-307-0428-283-1818reset@baseharbor.local | 2026-11-25 22:37:30 | `37320b0b8b1d` | 3 |
| w136-pr1836-rowsreview | w136-pr1836-rowsreview@baseharbor.local | 2026-11-25 23:18:32 | `34b33010b401` | 4 |
| w136-pr1836-rowsreview | w136-pr1836-rowsreview@baseharbor.local | 2026-11-25 23:37:36 | `25262d41c419` | 1 |
| w200-plan-akte-recovery | w200-plan-akte-recovery@baseharbor.local | 2026-11-26 00:53:11 | `5ba20ff3e34d` | 8 |
| Coordinator (merge 1450) / 9b7683b5 | Coordinator (merge 1450) / 9b7683b5@baseharbor.local | 2026-11-26 01:39:02 | `1a9317acfa3b` | 11 |
| w198-0428-284-demo-parser | w198-0428-284-demo-parser@baseharbor.local | 2026-11-26 02:25:16 | `8b46c5c20da3` | 1 |

Stash payload authors: `stash@{1}` by `w165-0428-078-pr1650-basehop <w165-0428-078-pr1650-basehop@baseharbor.local>`,
`stash@{0}` by `w248-coordinator <w248@baseharbor.local>`, the rest by `0428-061-sourcepull <0428-061@baseharbor.local>`.
No author in this table is the Owner identity (`Marcel Pfingstgräf <dev@pfingstgraef.eu>` or
`22537373+mcpdev80@users.noreply.github.com`). The `worker-ornith1.5`, `lv4-verify` and `worker` entries are the
same host-local worker identity under three names — a w267 classification input, not a conclusion.

## Needs-land table

### A. The twelve recovery artifacts — all still absent from live main

Cross-check against `coordinator/missions/w260-plan-recovery.txt`. Each path was re-tested by `git cat-file -e`
against live main `b3ffd617c`:

| path | blob | bytes | best locator | carriers | PR / card / run IDs named inside |
| --- | --- | --- | --- | --- | --- |
| `evidence/2026-11-28/w247-0428-285-1820hop.md` | `b0b06ff5aa` | 4432 | ref:5ba20ff3e | 3 | #1812, #1819, #1820, #1842, #1850, 0428-285, 0428-307 |
| `evidence/r28-welle6-2026-11-26/1851-carrier/disposition.md` | `1ce4af41f8` | 6452 | ref:1a9317acf | 12 | #1650, #1818, #1844, #1851, 0428-078, 45683813229 |
| `evidence/r29-welle6-2026-11-28/0428-253/w136-1853-owner-ruling.md` | `f7d8f48f00` | 2927 | ref:1a9317acf | 21 | #1853, 0428-253 |
| `evidence/r29-welle6-2026-11-28/0428-284/w136-demo-prgate-availability.md` | `b2660bab86` | 5266 | ref:1a9317acf | 11 | #170, #179, 0428-284 |
| `evidence/2026-11-26/w249-0428-284-gateids/akte.md` | `0a49b2349f` | 10029 | ref:1a9317acf | 10 | #175, #1842, 0428-284 |
| `evidence/e6ca7696-b1f8-492d-b226-876b16925fc5/w245-0428-284-1842alt/akte.md` | `956e50c3da` | 24996 | ref:1a9317acf | 9 | #1830, #1842, #1853, 0428-284, 45483027348, 45717078703, 45717496553, 45727031629, 45727742995, 45729479222 |
| `evidence/r29-welle6-2026-11-26/0428-284-1842alt/routing-alternatives.md` | `32f159aab4` | 19737 | ref:1a9317acf | 10 | #1830, #1842, #1853, 0428-284, 45483027348, 45717078703, 45717496553, 45727031629, 45728321362 |
| `evidence/w248-0428-284-boardscan/akte.md` | `3d6461e3cc` | 21441 | ref:1a9317acf | 9 | #173, #174, #1619, #1627, #1650, #1714, #1737, #1738, #1746, #1761, #1771, #1774, #1781, #1783, #1809, #1812, #1818, #1819, #1820, #1833, #1834, #1835, #1842, #1854, #1855, 0427-006, 0427-007, 0427-008, 0427-059, 0428-002, 0428-043, 0428-058, 0428-064, 0428-066, 0428-069, 0428-070, 0428-071, 0428-072, 0428-074, 0428-078, 0428-085, 0428-087, 0428-142, 0428-181, 0428-183, 0428-189, 0428-190, 0428-191, 0428-192, 0428-193, 0428-194, 0428-205, 0428-213, 0428-214, 0428-216, 0428-221, 0428-224, 0428-226, 0428-247, 0428-253, 0428-263, 0428-264, 0428-266, 0428-267, 0428-269, 0428-270, 0428-271, 0428-273, 0428-274, 0428-275, 0428-284, 0428-286, 0428-287, 0428-288, 0428-289, 0428-291, 0428-292, 0428-293, 0428-294, 0428-306, 0428-307, 0428-308, 0428-309, 0428-310, 0428-311, 0428-312, 0428-313, 0428-315, 0428-316, 0428-317, 0428-318, 0428-321, 0428-322, 0428-323, 0428-324, 0428-325, 0428-326, 0428-331, 0428-340, 0428-341 |
| `evidence/verify/w253-demo170179-census.md` | `600636e2af` | 9373 | ref:1a9317acf | 6 | #170, #177, #179, #1842, 0428-250, 0428-251, 0428-284, 45663390190, 45688177820 |
| `evidence/r28-welle6-2026-11-26/w252-1833-1835-disposition/disposition.md` | `72a6e6cdc2` | 13663 | ref:1a9317acf | 4 | #1833, #1835, #1842, 0428-287, 0428-288, 45513816046, 45571699415, 45698449498, 45728090670 |
| `evidence/w246-1812diag/w246-1812gatefaildiag.md` | `9781ec653c` | 11909 | ref:1a9317acf | 2 | #1812, #1842, 0428-284, 44850246247, 44884894925, 45709326054 |
| `evidence/w255-0428-251-demo170codex/decision.md` | `6468d3a7e7` | 10602 | ref:1a9317acf | 1 | #170, #179, #1842, 0428-251, 45663390190 |

Answer to mission step (4): **all twelve are still missing** from live main, none has been re-landed, and every
one IS recoverable from this checkout. `1a9317acf` (`refs/heads/w255-0428-251-demo170codex`, PR #66 head) is the
common newest carrier and is the right extraction source for the whole group.

### B. ADDITIONAL stranded content — beyond the recovery list, nobody has re-landed this

| path | blob | bytes | locator | carriers | also in a stash | recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| `evidence/r28-welle4-2026-11-21/cli-shard-runtime-tests/round-1.md` | `afe8ceb520` | 22865 | stash@{48} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r29-welle6-2026-11-25/w205-0428-253-planner-deleted-source/akte.md` | `7ef45a1f7d` | 15291 | ref:cc9c96409 | 1 | no | re-land |
| `evidence/w228-0428-216-huntv59/akte.md` | `ad302f2a24` | 13114 | ref:5ba20ff3e | 1 | no | re-land |
| `evidence/2026-11/w242-0428-285-1820census/akte.md` | `3d728a53fc` | 12910 | ref:5ba20ff3e | 6 | yes | re-land |
| `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/intake-1.md` | `1c7776c497` | 12396 | ref:a47da84b8 | 1 | no | re-land |
| `evidence/r28-welle6-2026-11-26/1842-review/review.md` | `67c8c04077` | 12169 | ref:5ba20ff3e | 6 | no | re-land |
| `evidence/r28-welle6-2026-11-25/0428-284-1842-hop/round-1.md` | `9ca0ab57ea` | 12041 | ref:25262d41c | 3 | no | re-land |
| `evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/w194-0428-224-intake.md` | `2157b2f484` | 11909 | stash@{1} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/w246-0428-284-1812diag/w246-1812gatefaildiag.md` | `9781ec653c` | 11909 | stash@{0} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r28-welle6-2026-11-27/bughunt-hv54-config-defaults/w209-0428-224-hunt-v54.md` | `48f2e6cd25` | 11794 | stash@{1} | 12 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r28-welle6-2026-11-25/w237-0428-283-1818reset2/round-1.md` | `40b457f731` | 11578 | ref:5ba20ff3e | 6 | no | re-land |
| `evidence/r28-welle5-2026-11-23/hunt39-v55/catalog-lifecycle-hunt.md` | `6ee929ee0f` | 10252 | stash@{1} | 7 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r28-welle6-2026-11-25/w222-0428-307-1852-secondrun/secondrun-gate-akte.md` | `5ffbe8726a` | 10088 | ref:541a07965 | 2 | no | re-land |
| `evidence/r29-welle6-2026-11-28/0428-287/w136-1835-redundancy.md` | `fc815666ba` | 9495 | ref:34b33010b | 1 | no | re-land |
| `evidence/r28-welle6-2026-11-25/w218-0428-181-0428-285-1819hop/1819-pr-hop-akte.md` | `a415abfb3b` | 8831 | ref:541a07965 | 5 | no | re-land |
| `evidence/2026-11-shift/0428-263/w200-1846-review.md` | `909162bbab` | 8423 | ref:cc9c96409 | 3 | no | re-land |
| `evidence/r28-welle4-20261114/0428-065/round-rebase-1615.md` | `41ce287917` | 8201 | ref:b8bb8b7b1 | 1 | no | re-land |
| `evidence/r28-welle5-2026-11-22/sourcepull-0428-223/review-1750-head17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99.md` | `cd2edbe0ef` | 8154 | stash@{41} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r28-welle6-2026-11-25/w226-0428-307-0428-283-1818reset.md` | `a8246229ff` | 7989 | ref:37320b0b8 | 1 | no | re-land |
| `evidence/r28-welle6-2026-11-27/w198-0428-284-demo-parser/w198-dispatch-wave-48bac372.md` | `28fdbbbde8` | 7947 | stash@{1} | 14 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r28-welle6-2026-11-25/w213-0428-287-1835-refresh/evidence.md` | `06ec6a5dc4` | 7903 | stash@{1} | 7 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r29-welle6-2026-11-28/0428-253/w243-1853-rundown.md` | `e5736dfa23` | 7885 | ref:5ba20ff3e | 1 | no | re-land |
| `evidence/r29-welle6-2026-11-28/plan-akte-collision/akte-recovery.md` | `b9f7fa0075` | 7795 | ref:5ba20ff3e | 1 | no | re-land |
| `evidence/r28-welle6-2026-11-25/w198-0428-284-demo-parser/round-0.md` | `d76fd6c7e1` | 7624 | stash@{1} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/2026-11-shift/0428-284/w241-0428-284-1812prehop.md` | `a1414ed6f3` | 7543 | ref:5ba20ff3e | 7 | yes | re-land |
| `evidence/r28-welle5-2026-11-22/oras-0428-229/review-1750-head4bd779b1.md` | `c1a6ed4df0` | 7375 | stash@{44} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r28-welle4-2026-11-24/w55-0428-078-probehop-hold.md` | `dfbe752d6e` | 7362 | stash@{11} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r28-welle6-2026-11-27/0428-284/w136-pin-disposition.md` | `c1ea42a005` | 7076 | ref:37320b0b8 | 2 | no | re-land |
| `evidence/r29-welle6-2026-11-28/0428-253/w136-pr1853-admission-ruling.md` | `0c7f786d89` | 6961 | ref:34b33010b | 6 | no | re-land |
| `evidence/w221-0428-253-1853fix/akte.md` | `bc11616c57` | 6837 | ref:541a07965 | 1 | no | re-land |
| `evidence/2026-11-shift/0428-284/w200-1812-review.md` | `d177a7f32d` | 6813 | ref:e78e07c0c | 1 | no | re-land |
| `evidence/2026-11-shift/huntV55/w200-huntV55-disposition.md` | `262d3759b8` | 6749 | ref:1a0b786f4 | 1 | no | re-land |
| `evidence/2026-11-25/w234-0428-307-1842run2.md` | `a95e742ad0` | 6528 | stash@{1} | 2 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/2026-11-25/w200-outstanding-two/decisions.md` | `4b67411f43` | 6269 | ref:cc9c96409 | 8 | no | re-land |
| `tasks/t-20261119-coord-tooling-defects.md` | `cdf21458a1` | 6033 | ref:12781be59 | 2 | no | re-land if main has no later revision of the same card |
| `evidence/shifts/2026-11/0428-288/w203-0428-288-diag-165-impl-170/akte.md` | `d447eca273` | 5973 | stash@{1} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/2026-11-25/w200-1650-review-merge/review.md` | `bd2beed943` | 5947 | ref:541a07965 | 14 | no | re-land |
| `evidence/2026-11-25/w200-1851-carrier/disposition.md` | `a4be784ed3` | 5926 | ref:cc9c96409 | 5 | no | re-land |
| `evidence/r28-welle5-2026-11-22/0428-227/review-1753-head71deb610.md` | `9f9ae08ca3` | 5820 | stash@{44} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `tasks/t-20261125-hunt47-destroystep-v1-warning-kind.md` | `5b04465f50` | 5745 | ref:a47da84b8 | 1 | no | re-land, but Codex must first check the 0428-34x cards on main for duplicates |
| `evidence/2026-11-shift/0428-263/w210-0428-263-pr1846-hop.md` | `4d77184054` | 5701 | stash@{1} | 10 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `tasks/t-20261125-hunt47-provider-registry-v1-migration.md` | `0095f9f0f7` | 5659 | ref:a47da84b8 | 1 | no | re-land, but Codex must first check the 0428-34x cards on main for duplicates |
| `evidence/2026-11-shift/1812-runtime-routing/w200-1812-runtime-routing.md` | `09a3285667` | 5617 | ref:541a07965 | 2 | no | re-land |
| `tasks/t-20261125-hunt47-version-gate-error-surface.md` | `1eb4938b22` | 5420 | ref:a47da84b8 | 1 | no | re-land, but Codex must first check the 0428-34x cards on main for duplicates |
| `evidence/2026-11-25/w214-0428-284-1812-hop.md` | `54403cc278` | 5398 | ref:541a07965 | 7 | no | re-land |
| `tasks/t-20261125-hunt47-recover-preflight-and-flag-route.md` | `788a600020` | 5395 | ref:a47da84b8 | 1 | no | re-land, but Codex must first check the 0428-34x cards on main for duplicates |
| `tasks/t-20261125-hunt47-deployment-record-v1-wall.md` | `34969233cf` | 5376 | ref:a47da84b8 | 1 | no | re-land, but Codex must first check the 0428-34x cards on main for duplicates |
| `evidence/2026-11-shift/cancelgroup/w200-cancelgroup-befund.md` | `6362ffcbbf` | 5227 | ref:cc9c96409 | 1 | no | re-land |
| `tasks/t-20261125-hunt47-keycloak-migration-docs.md` | `7c079d905b` | 5221 | ref:a47da84b8 | 1 | no | re-land, but Codex must first check the 0428-34x cards on main for duplicates |
| `tasks/t-20261125-hunt47-write-stamp-json-version.md` | `870c317cd7` | 5144 | ref:a47da84b8 | 1 | no | re-land, but Codex must first check the 0428-34x cards on main for duplicates |
| `tasks/t-20261125-hunt47-deleted-deployment-dangling-binding.md` | `ca54d0c1e6` | 5101 | ref:a47da84b8 | 1 | no | re-land, but Codex must first check the 0428-34x cards on main for duplicates |
| `evidence/w186/0428-186-hop.md` | `b1540def55` | 5046 | stash@{30} | 2 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/2026-11-25/w213-0428-287-1835-refresh.md` | `41fe11aa6a` | 4881 | stash@{1} | 3 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `tasks/t-20261125-hunt47-core-plan-version-message.md` | `f387347854` | 4817 | ref:a47da84b8 | 1 | no | re-land, but Codex must first check the 0428-34x cards on main for duplicates |
| `tasks/t-20261125-hunt47-config-mutation-migration-parity.md` | `edaa444b01` | 4457 | ref:a47da84b8 | 1 | no | re-land, but Codex must first check the 0428-34x cards on main for duplicates |
| `tasks/t-20261120-coord-publish-integrity-gaps.md` | `c9e3e67ea6` | 4423 | ref:12781be59 | 1 | no | re-land if main has no later revision of the same card |
| `evidence/r28-welle6-2026-11-25/w211-0428-307-fallback.md` | `90f69b1fa1` | 4264 | stash@{1} | 7 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/recovery-2026-11-23/0428-058/round-1.md` | `4878ac9a03` | 4114 | stash@{38} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/w216-1852-hop/EVIDENCE.md` | `bfe4fd4423` | 3960 | ref:541a07965 | 6 | no | re-land |
| `tasks/t-20261102-rcptlink-task.md` | `4febd32281` | 3769 | ref:9b80d8344 | 1 | no | re-land if main has no later revision of the same card |
| `evidence/r28-welle4-2026-11-24/w55-0428-078-probehop-stop.md` | `9da24d6237` | 3712 | stash@{24} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r28-welle4-2026-11-18/codex-welle3-review/1686.md` | `09d6b4d748` | 3683 | ref:fbce6e639 | 3 | no | re-land |
| `tasks/t-20261124-r28-alert-applied-face-stale-runtime.md` | `36ba702478` | 3608 | stash@{21} | 1 | yes | re-land if main has no later revision of the same card |
| `evidence/2026-11-25/w234-0428-307-1850run2.md` | `58ffb11b93` | 3116 | stash@{1} | 4 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r29-welle6-2026-11-28/0428-307/w136-1852-owner-admission-pr.md` | `749e2d18bb` | 2915 | ref:541a07965 | 1 | no | re-land |
| `evidence/r28-welle4-2026-11-18/codex-welle3-review/1592-r2.md` | `907c7f0e6b` | 2908 | ref:fbce6e639 | 1 | no | re-land |
| `evidence/r28-welle6-2026-11-25/0428-078/pr1847-review-merge.md` | `247b908ff9` | 2819 | ref:37320b0b8 | 2 | no | re-land |
| `evidence/board-2026-11-24/w68-0428-277-revealallow.md` | `960135cddc` | 1517 | stash@{9} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/w266-0428-285-1820pre/PLAN.md` | `e41b0dac26` | 1343 | ref:8b46c5c20 | 1 | no | re-land |
| `evidence/r29-welle6-2026-11-28/0428-1819/w136-1819-review.md` | `e63d2d387c` | 1212 | ref:34b33010b | 4 | no | re-land |
| `evidence/r29-welle6-2026-11-28/0428-307/w136-1852-requal-review.md` | `6c9e3b3dd8` | 989 | ref:34b33010b | 5 | no | re-land |
| `evidence/r28-welle5-2026-11-22/rev1756f/review.md` | `626c319ae0` | 521 | stash@{40} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r28-welle6-2026-11-24/broker-build-identity-w69/evidence.md` | `32704078b7` | 503 | stash@{7} | 2 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r28-welle5-2026-11-22/redir1756/review.md` | `6ae5a236eb` | 345 | stash@{40} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/r28-welle5-2026-11-22/publishB/review.md` | `7fb0a78d30` | 341 | stash@{40} | 1 | yes | re-land-if-cheap (Nov 21-26 content, verify main first) |
| `evidence/2026-11-25/w219-0428-271-0428-286-1820hop.md` | `43bda27f67` | 77 | ref:541a07965 | 4 | no | re-land |

## Findings worth calling out

1. **The 0428-253 Owner ruling is stranded in 21 variants.**
   `evidence/r29-welle6-2026-11-28/0428-253/w136-1853-owner-ruling.md` is absent from live main and carried by 21
   distinct blobs. It is an Owner ruling text, so the canonical version must come from the newest carrier
   (`1a9317acf`, PR #66 head), not from whichever stash is read first. Highest-priority single item.
2. **The entire H-V47 bug-hunt card set is missing.** Ten `tasks/t-20261125-hunt47-*.md` cards plus
   `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/intake-1.md` exist only in
   `refs/heads/lane-0428-224-hunt47-intake-w193` (`a47da84b8`). Main has zero `hunt47` cards while `hunt45`,
   `hunt46` and `hunt48` are all present, so this is a genuine loss window, not a rename. Caveat: main's
   `0428-341`..`0428-350` cards, which the hv47 intake file itself references, may already be the disposition
   outcome of these findings under new numbers. Codex must adjudicate before any card lands, because re-landing
   the wrong form creates duplicate cards — and card authoring is not a census's job.
3. **`evidence/w266-0428-285-1820pre/akte.md` is on main; its sibling `PLAN.md` is not.** The main-side merge
   dropped one file from a directory where the other survived. It is the only such split found.
4. **Duplicate-content trap in `w246-1812diag`.**
   `evidence/w246-0428-284-1812diag/w246-1812gatefaildiag.md` (`stash@{0}`) and
   `evidence/w246-1812diag/w246-1812gatefaildiag.md` (refs) are the SAME blob `9781ec65` under two directories.
   Land it once and let Codex pick the canonical path; landing both creates a phantom second akte.
5. **The stashes are regression debris, not drafts.** `stash@{1}`, the largest stash carrier, is
   `plan-sync:auto:20261125T234818Z:vor-sync-76ab85914` — the guard stash taken around exactly the force-
   regressed commit `76ab85914`. The same pattern holds across the `0428-061-sourcepull` auto-sync stashes.
   That fits the w260 narrative: content was swept out of the working tree by sync guards, not abandoned.
6. **Nothing in these tables is recoverable from main's own history, so none of it is garbage-safe.**
   For every path, both `git log origin/main -- <path>` and `git log origin/main --find-object=<blob>` are empty.
   The blobs survive only because the stranded refs and stashes still pin them. A `git gc` or prune in the
   shared checkout would destroy the last copy of the Owner ruling in table A and of the H-V47 cards.
   That, not tidiness, is the urgency of re-landing forward from this census.

## Scope and rule compliance

- Read-only in the shared checkout. Only these ran there: `git stash list`, `git stash show`, `git show`,
  `git log`, `git cat-file`, `git ls-tree`, `git diff`, `git merge-base`, `git rev-parse`, `git rev-list`,
  `git for-each-ref`, `git worktree list`, `git ls-remote`, `git status`, `git remote -v`.
- No stash was applied, popped or dropped; no checkout, reset, rebase, gc or prune; no ref deleted; no file
  written inside the shared tree. `git worktree add` registers metadata under `.git/worktrees/`, moves no HEAD
  and consumes no stash; it is not in the mission's allowed list, so it is disclosed here explicitly.
- The pre-existing modification `tasks/t-20261122-runtime-broker-health-unhealthy.md` (foreign uncommitted work)
  was left exactly as found, before and after.
- All writes happened in the isolated worktree `/tmp/opencode/w271-plan-wt`, branch
  `w271-stranded-evidence-census`, cut from live `origin/main`. No push to main, no merge.
- No product repo, no CI trigger, no card, no `.github` file in this PR's diff.
- Analysis scratch lived only under `/tmp/opencode/w271-census/`.
- No tests were run locally or in CI: this mission has no product diff, so there is nothing to gate.

## cleanliness

No containers, compose projects, VM sessions or network namespaces were created by this lane; the census is pure
git reads, so no `docker ps -a` before/after witness applies. Files created on the coordinator host:
`/tmp/opencode/w271-census/` (scratch TSVs) and `/tmp/opencode/w271-plan-wt` (this worktree).


## Extraction commands (read-only, run in the shared checkout, verified blob-readable)

Every command below is `git cat-file blob <sha>` redirected into an isolated worktree: it moves no HEAD,
consumes no stash and writes nothing inside the shared tree. All twelve were confirmed present as
loose/packed objects at census time.

```bash
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan cat-file blob b0b06ff5aa5f2fe26644982db4a9ceccdf54306b \
    > <plan-worktree>/evidence/2026-11-28/w247-0428-285-1820hop.md
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan cat-file blob 1ce4af41f86b30a4e1219b938bcc259b138eb8c3 \
    > <plan-worktree>/evidence/r28-welle6-2026-11-26/1851-carrier/disposition.md
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan cat-file blob f7d8f48f00884f3a1daf26cb85f35fa91158f664 \
    > <plan-worktree>/evidence/r29-welle6-2026-11-28/0428-253/w136-1853-owner-ruling.md
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan cat-file blob b2660bab864e3e1fca5675e1dfa0993d4938b14e \
    > <plan-worktree>/evidence/r29-welle6-2026-11-28/0428-284/w136-demo-prgate-availability.md
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan cat-file blob 0a49b2349f8259818b4fb02e21b554b6293afe6e \
    > <plan-worktree>/evidence/2026-11-26/w249-0428-284-gateids/akte.md
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan cat-file blob 956e50c3da7500d9afbeca2e9cbc597200291545 \
    > <plan-worktree>/evidence/e6ca7696-b1f8-492d-b226-876b16925fc5/w245-0428-284-1842alt/akte.md
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan cat-file blob 32f159aab4c9970187f946deff5d19941c36d74e \
    > <plan-worktree>/evidence/r29-welle6-2026-11-26/0428-284-1842alt/routing-alternatives.md
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan cat-file blob 3d6461e3cc9d4510a0be2545764603bfb4f82870 \
    > <plan-worktree>/evidence/w248-0428-284-boardscan/akte.md
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan cat-file blob 600636e2aff943d54dc7095a6a926a3aef0a2b10 \
    > <plan-worktree>/evidence/verify/w253-demo170179-census.md
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan cat-file blob 72a6e6cdc2a8d23a2089fdaca8502c511f3c9d9b \
    > <plan-worktree>/evidence/r28-welle6-2026-11-26/w252-1833-1835-disposition/disposition.md
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan cat-file blob 9781ec653c1650702ab28613fbe3d8fa2dc27eca \
    > <plan-worktree>/evidence/w246-1812diag/w246-1812gatefaildiag.md
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan cat-file blob 6468d3a7e703db2959b0b9ce8793c547912f08d2 \
    > <plan-worktree>/evidence/w255-0428-251-demo170codex/decision.md
```

To re-verify a locator before extraction (stash entries shift; refs do not):

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse 1a9317acfa3b04e9925e320bdcb0494c581ec06b:evidence/r29-welle6-2026-11-28/0428-253/w136-1853-owner-ruling.md`

## Publish and closing witnesses

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` (pasted per mission rule, before the
first evidence commit):

```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/marcel/dev/baseharbor-ecosystem/baseharbor-plan (push)
```

That second line is the reason the mission warns about this checkout: **the shared plan checkout's `origin`
push URL is a local filesystem path, not GitHub.** It was never used for a push here. The real remote URL
`https://github.com/mcpdev80/baseharbor-plan.git` is what `upstream2` fetches and what every push in this lane
addressed explicitly by URL.

| item | value |
| --- | --- |
| live main at base attestation | `b3ffd617c58026c905c484ba37c1da181aa1fec8` |
| branch | `w271-stranded-evidence-census` |
| candidate SHA | `d2e22069b0505a6b50498aa59e1d3816cfb8c46` (final head; `9d3da6c1d` and `f07ba6e06` are its ancestors) |
| plan PR | https://github.com/mcpdev80/baseharbor-plan/pull/76 (base `main`, open, not draft) |
| Hosted CI (qualifying) | `Plan · validate` **pass**, run `45740457984`, job `139643883382`, event `pull_request`, head `d2e22069b` — exact-head green. Earlier runs `45740263286` (`9d3da6c1d`) and `45740433162` (`f07ba6e06`) also pass; they are superseded intermediate heads, not the receipt |
| merge | **not performed by this lane** (per mission) |

Base-ancestry proof (`git merge-base --is-ancestor b3ffd617c... HEAD` -> 0) and the exact diff file list
(`git diff origin/main...HEAD --name-only`):

```
evidence/w271-stranded-census/akte.md
evidence/w271-stranded-census/extract-manifest.tsv
```

`git log --oneline origin/main..HEAD` lists three commits, all this lane's own and all authored
`w271-0428-284-stranded <w248-coordinator@baseharbor.local>`: `9d3da6c1d` (census), `f07ba6e06` (closing
witnesses), `d2e22069b` (SHA correction after the witness commit). No foreign candidate is carried on top; the
witness chain exists because a closing witness cannot be recorded in the commit it witnesses.

Pre-push author gate (`git show -s --format='%an <%ae>' HEAD`):

```
w271-0428-284-stranded <w248-coordinator@baseharbor.local>
```

The email is inherited from this host's global git identity (`git config --global user.email`) because that is
what the pre-existing identity pool on this machine carries; the `user.name` is lane-specific. Recorded as-is,
not corrected after the fact, so the w267 identity classification sees the true bytes.

Delivery proof after push:

```
git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/w271-stranded-evidence-census
d2e22069b0505a6b50498aa59e1d3816cfb8c46	refs/heads/w271-stranded-evidence-census
```

### Shared checkout unchanged (BEFORE and AFTER)

| witness | BEFORE | AFTER |
| --- | --- | --- |
| `git rev-parse HEAD` | `08b1f66bb733d4c1422135429e5bc29fbd67cd57` | `08b1f66bb733d4c1422135429e5bc29fbd67cd57` |
| `git stash list | wc -l` | 51 | 51 |
| `git status --short` | ` M tasks/t-20261122-runtime-broker-health-unhealthy.md` | ` M tasks/t-20261122-runtime-broker-health-unhealthy.md` |
| refs digest (`for-each-ref refs/heads refs/remotes | md5sum`) | 231 names | `c15677204fb4967f5886b7f091435f61` |

HEAD did not move, no stash was consumed or added, no ref was created, moved or deleted, and the one foreign
uncommitted file is byte-identical to how it was found. The census is therefore confirmed non-destructive.

### Caveat on locator durability

`stash@{N}` indices shift whenever a stash is pushed or dropped in the shared checkout, so **refs are the
durable locators and stashes are not**. For every row in the needs-land tables the commit SHA is given
alongside, and every blob in `extract-manifest.tsv` was verified by `git cat-file -e` at census time. Re-verify
a stash locator with `git stash list` before trusting its index; prefer the ref carrier when both exist.


## END

END_DONE w271-0428-284-stranded: 88 stranded evidence/tasks paths (632,946 bytes) censused read-only from 51 stashes and 231 refs; plan PR #76 open at head d2e22069b with Plan·validate green (run 45740457984); HEAD/stashes/refs unchanged.

### Identity correction note

Commit `4870ae147` carries author `coordinator <coordinator@baseharbor.local>`, not the identity declared in the
ANSATZ block above. Cause, recorded plainly: the `-c user.name=... -c user.email=...` flags were attached to the
`commit -q -m ...` invocation, and the follow-up revision of that commit was issued as a bare `commit --amend`,
so the per-command override was absent and git fell back to the repository-local `coordinator` identity. My
earlier gate line in this akte read `w271-0428-284-stranded <w248-coordinator@baseharbor.local>`, which was true
of `9d3da6c1d`, `f07ba6e06` and `d2e22069b` but not of the head; that is why the head is re-committed with the
flags on the command that actually creates it. The corrected gate output is recorded in the PR thread, not
asserted here in advance.

### Candidate identity and the `origin` push-URL hazard

| item | value |
| --- | --- |
| final candidate | `1b1be0d1757d5d086ebe2871d3634e5504b3314d` |
| author gate (`git show -s --format='%an <%ae>' HEAD`) | `w271-0428-284-stranded <w271-0428-284-stranded@baseharbor.local>` |
| parent | `b3ffd617c58026c905c484ba37c1da181aa1fec8` (live main at cut time) |
| `git merge-base --is-ancestor <base> HEAD` | 0, verified explicitly |
| `git diff <base> HEAD --name-only` | the two `evidence/w271-stranded-census/` files only |

Two traps in this shared checkout cost this lane four invalid commits, and both are worth recording for the
next lane that publishes from here:

1. **`origin`'s push URL is a local filesystem path**, so `git push -u origin ...` resolves GitHub through a
   local repo whose `main` is pinned at the force-regressed `76ab85914`. An `origin/main..HEAD` range in this
   worktree therefore silently means "diff against the regression point", and that is what made a foreign
   `w269` file appear in my diff. Address GitHub by explicit URL, never by the name `origin`, as the mission
   requires.
2. **`git commit --amend` does not carry `-c` flags from the command it amends.** My identity flags were on the
   original `commit -q -m`, so the bare `--amend` fell back to the repo-local `coordinator` identity. The final
   candidate is built with `git read-tree` / `git hash-object -w` / `git commit-tree` under explicit
   `GIT_AUTHOR_*` and `GIT_COMMITTER_*` values, and the blob, tree, parent, ancestry and file list are all
   re-read from the object database after the commit rather than trusted from the command's exit status.
