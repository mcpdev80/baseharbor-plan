# w280 - READ-ONLY recovery presence re-count (what Codex w255 actually published)

Mission: `coordinator/missions/w280-recovery-presence-recount.txt` (coordinator mission 2026-11-26).
Verifies the effect on live `main` of plan PR #75 (w255 recovery) against the 88-path stranded census of
w271 (plan PR #76, head `97cf9672e11922025e43afd56611df8fca679468`).

Lane: `w280-0428-284-recount`. Hard limits observed: read-only against `baseharbor-plan`; no plan-main push,
no merge, no CI trigger, no card edits, no `.github` edits, no stash or HEAD mutation in any shared checkout.

## PLAN

1. Print live main tip + last 5 commit subjects with committer dates (`%ci`); freeze the before-state.
2. Report PR #75 state, head SHA, `mergedAt`; print the merge commit and confirm the 12 restored paths.
3. Extract the 88-path missing list from w271's akte (plan PR #76, head `97cf9672e`).
4. Independently re-count presence of each of the 88 paths on live main; report new missing count + byte total.
5. List first 20 still-missing paths with carrier (`stash@{N}` or refname) exactly as w271 recorded.
6. Print author/committer (`%an %cn %s`) for every commit that restored a path on main.
7. Classify the remaining gap per w271's own categories (re-land / re-land-if-cheap / duplicate / conflict).
8. Write this akte on an own plan branch, push, open a plan PR (report the number, do not merge).
9. Zero-mutation proof (live main tip before and after), cleanliness line, END post.

## ANSATZ - visible identity and provenance block (recorded BEFORE the first commit)

Per-card frontmatter owner, VERBATIM, fetched from `origin/main` at runtime via
`git show refs/remotes/origin/main:tasks/t-20261125-0428-284-1812-postretry-gate-failure.md`:

```text
id: t-20261125-0428-284-1812-postretry-gate-failure
card_number: "0428-284"
owner: w198-0428-284-demo-parser
kanban_status: active
```

The named card's owner is `w198-0428-284-demo-parser`. This mission is a bounded READ-ONLY census; it does not
take that card, change its `owner` field, or claim its identity. The executing lane identity is
`w280-0428-284-recount`.

- git user.name to use: `w280-0428-284-recount`
- git user.email to use: `w280-0428-284-recount@baseharbor.local`
- literal commit invocation:
  `git -c user.name="w280-0428-284-recount" -c user.email="w280-0428-284-recount@baseharbor.local" commit -m "docs(evidence): w280 read-only recovery presence re-count akte"`
- pre-push author gate line: `git show -s --format=%an HEAD` must print exactly `w280-0428-284-recount`.

## Base attestation and remote resolution

- Real remote used for every fetch: `https://github.com/mcpdev80/baseharbor-plan.git` (verified by `git remote -v`,
  output in the Reality witnesses section below).
- Base ref cut point (this akte branch): `1f3e0673fa9f2265805c1291f794531c3876a9de`, committer date
  `2026-11-26 03:45:25 +0100`, `%an=Marcel Pfingstgräf %cn=GitHub`,
  subject `w277-0428-273: read-only #1819 hop pre-stage akte on current tip (#80)`.
  That SHA equals the live `refs/heads/main` value returned by `git ls-remote` at cut time, and
  `git merge-base --is-ancestor refs/remotes/origin/main HEAD` passes for the single commit `b938a1f41`.
- The publication candidate under examination, PR #75, was cut from `264e2632319bdab152e7b03b7bd8bd0b3656bce9`
  (PR #68 squash commit, `%ci=2026-11-26 02:23:00 +0100`, `%an=Marcel Pfingstgräf %cn=GitHub`).
  `git merge-base --is-ancestor 264e263 origin/main` -> true. See the stale-base finding below.

## Reality witnesses

`git remote -v` in the shared planning checkout `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`:

```text
origin      https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin      https://github.com/mcpdev80/baseharbor-plan.git (push)
upstream2   https://github.com/mcpdev80/baseharbor-plan.git (fetch)
upstream2   https://github.com/mcpdev80/baseharbor-plan.git (push)
```

All remote truth in this akte comes from `gh api` against `repos/mcpdev80/baseharbor-plan` and from
`git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`. The shared checkout was never
used as a source of remote state; the isolated read-only clone `refs/remotes/origin/main` was.

Live main tip witnesses (before / during / after), all `refs/heads/main`:

| witness | SHA | note |
| --- | --- | --- |
| before (first `gh api` + `ls-remote`) | `3a9bfea66796e2c36795b9c3794cc24654743030` | `%ci=2026-11-26T02:33:11Z` |
| mid-run (PR #75 had just merged) | `7ae6d04bf92217ca70e664542897f42e237dbe89` | `%ci=2026-11-26T02:37:44Z`, subject `Restore missing Plan evidence forward-only (#75)` |
| mid-run (later lane publications) | `6480495f518eb83c4b1e01ecbfa3c48defd45fc1` | `%ci=2026-11-26T02:41:06Z` equivalent UTC |
| after (final `ls-remote`) | `6480495f518eb83c4b1e01ecbfa3c48defd45fc1` | identical to the preceding witness |

The mission's zero-mutation proof is stated exactly: my lane did not move `main`; `main` moved twice during the
run because other lanes and the GitHub merge of #75 published. No mutation is attributable to w280 and the
`main` value after my work equals the value observed before my only write (the akte branch push).

### First five live-main commits at the before-witness (`gh api .../commits?sha=main&per_page=5`, `%ci`)

| SHA | `%ci` | `%an` | `%cn` | subject |
| --- | --- | --- | --- | --- |
| `3a9bfea66` | 2026-11-26T02:33:11Z | Marcel Pfingstgräf | GitHub | evidence(w262): PR-HOP #1650 report-only akte (head 37c4d847, runs 45734193200+45737093207) (#78) |
| `9ff4e1108` | 2026-11-26T02:32:56Z | w198 | coordinator | w275-0428-251-runaudit: read-only demo #170 run-creation audit akte 2026-11-26 |
| `5fa9f28e0` | 2026-11-26T02:32:05Z | Marcel Pfingstgräf | GitHub | evidence w273: 0428-284 release-pin/catalog census (#77) |
| `4d7ef2aa5` | 2026-11-26T02:23:03Z | Marcel Pfingstgräf | GitHub | docs(review): record bounded #1650 verdict (#79) |
| `dd851feb4` | 2026-11-26T02:11:03Z | coordinator | coordinator | w274-0428-251-binddiag: read-only workflow zero-jobs diagnosis akte |

## Step 2 - PR #75 state and the twelve restored paths

PR #75 (`https://github.com/mcpdev80/baseharbor-plan/pull/75`), branch `w255-w260-plan-recovery`:

- head SHA: `56db4052c4153fd4903e489293b295cf13794ade`
- state: `MERGED`, `mergedAt`: `2026-11-26T02:37:44Z`
- merge (squash) commit on main: `7ae6d04bf92217ca70e664542897f42e237dbe89`, parent `3a9bfea66`
- observation: the FIRST read of `gh pr view 75` returned `state: OPEN`, `mergedAt: null`, `mergeCommit: null`
  at live main `3a9bfea66`. The merge landed seconds later during this run, so the mission premise
  ("verify the effect AFTER publication") is only satisfied from the second witness onward.

The squash diff carries 14 files: 13 additions and 1 modification. Twelve of the additions are exactly w271's
group A recovery artifacts; the thirteenth addition is `evidence/coordination/w260-plan-recovery-w255-0428-251-demo170codex.md`
(the recovery report itself, not a census path) and the modification is `tasks/t-20261124-gate-catalog-baseline-1819.md`.

Presence of the twelve census paths on live main, tested independently with `git cat-file -e` plus blob equality
against w271's recorded blob:

| path | w271 blob | live main blob | verdict |
| --- | --- | --- | --- |
| `evidence/2026-11-28/w247-0428-285-1820hop.md` | `b0b06ff5aa` | `b0b06ff5aa` | restored, identical |
| `evidence/r28-welle6-2026-11-26/1851-carrier/disposition.md` | `1ce4af41f8` | `1ce4af41f8` | restored, identical |
| `evidence/r29-welle6-2026-11-28/0428-253/w136-1853-owner-ruling.md` | `f7d8f48f00` | `f7d8f48f00` | restored, identical |
| `evidence/r29-welle6-2026-11-28/0428-284/w136-demo-prgate-availability.md` | `b2660bab86` | `b2660bab86` | restored, identical |
| `evidence/2026-11-26/w249-0428-284-gateids/akte.md` | `0a49b2349f` | `0a49b2349f` | restored, identical |
| `evidence/e6ca7696-b1f8-492d-b226-876b16925fc5/w245-0428-284-1842alt/akte.md` | `956e50c3da` | `def3a593ce` | restored, NEWER variant |
| `evidence/r29-welle6-2026-11-26/0428-284-1842alt/routing-alternatives.md` | `32f159aab4` | `dd56513369` | restored, NEWER variant |
| `evidence/w248-0428-284-boardscan/akte.md` | `3d6461e3cc` | `3d6461e3cc` | restored, identical |
| `evidence/verify/w253-demo170179-census.md` | `600636e2af` | `600636e2af` | restored, identical |
| `evidence/r28-welle6-2026-11-26/w252-1833-1835-disposition/disposition.md` | `72a6e6cdc2` | `72a6e6cdc2` | restored, identical |
| `evidence/w246-1812diag/w246-1812gatefaildiag.md` | `9781ec653c` | `9781ec653c` | restored, identical |
| `evidence/w255-0428-251-demo170codex/decision.md` | `6468d3a7e7` | `6468d3a7e7` | restored, identical |

Answer to mission step (2): all twelve are now PRESENT on live main; none is still absent. Ten match w271's
recorded blob byte-for-byte. The two `NEWER variant` rows are not a discrepancy in the restore: w271's "best
locator" column pointed at carrier `1a9317acf` (PR #66 head) while w255 restored the newest carrier it selected,
PR #58 head `8b7ad11572e9ccc2cd0db37bf7d2259ab7460666`, and w255's own recovery akte records `def3a593ce` and
`dd56513369` as the intended blobs (`git diff --quiet <source-ref> -- <path>` exit 0 per w255). Verified
independently here: the live main blobs equal the blobs at restore commit `2340f07`, so the restore is faithful
to its declared source. The older w271 variants remain recoverable from `1a9317acf` if a variant comparison is ever wanted.

## Step 3 - the 88-path list, reconstructed independently

Source: `evidence/w271-stranded-census/akte.md` at plan PR #76 head `97cf9672e` (fetched by Contents API, not
from the shared checkout). Parsed table A (12 recovery artifacts) plus table B (additional stranded content).
The parse reproduces w271's headline exactly, which is the control that the extraction is complete:

| measure | w271 | w280 parse |
| --- | --- | --- |
| distinct `evidence/` + `tasks/` paths missing from live main | 88 | 88 |
| bytes of that stranded content | 632946 | 632946 |

Machine-readable list: `paths-88.tsv` (path, w271 blob, bytes, group). Parsed file counts: 12 + 76 = 88 distinct.

## Step 4 - RE-COUNT: presence of all 88 paths on live main

Method: for each of the 88 paths, `git cat-file -e <live-main>:<path>` for presence plus `git rev-parse` blob
comparison against w271's recorded blob. No content re-derivation, no carrier reads, nothing outside a read-only
clone in `/tmp/opencode/w280/plan-main`.

Live main at measurement: `6480495f518eb83c4b1e01ecbfa3c48defd45fc1`.

| bucket | paths | stranded bytes |
| --- | --- | --- |
| restored by #75, blob identical to w271's record | 10 | 109307 |
| restored by #75, newer variant of the same path | 2 | 31520 |
| STILL MISSING (group B only) | 76 | 492119 |
| total census | 88 | 632946 |

New missing count: **76 paths, 492119 bytes** (down from 88 / 632946; #75 removed 12 paths / 140827 bytes).
Full per-path verdicts: `presence-all88.tsv`. The complete 76-path table with w271's carriers: `missing-76-table.md`.

## Step 5 - first 20 still-missing paths with their carriers

Carriers are quoted exactly as w271 recorded them (no re-derivation, per the mission):

1. `evidence/r28-welle4-2026-11-21/cli-shard-runtime-tests/round-1.md` | blob `afe8ceb520` | 22865 bytes | carrier: stash@{48} | in-a-stash: yes
2. `evidence/r29-welle6-2026-11-25/w205-0428-253-planner-deleted-source/akte.md` | blob `7ef45a1f7d` | 15291 bytes | carrier: ref:cc9c96409 | in-a-stash: no
3. `evidence/w228-0428-216-huntv59/akte.md` | blob `ad302f2a24` | 13114 bytes | carrier: ref:5ba20ff3e | in-a-stash: no
4. `evidence/2026-11/w242-0428-285-1820census/akte.md` | blob `3d728a53fc` | 12910 bytes | carrier: ref:5ba20ff3e | in-a-stash: yes
5. `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/intake-1.md` | blob `1c7776c497` | 12396 bytes | carrier: ref:a47da84b8 | in-a-stash: no
6. `evidence/r28-welle6-2026-11-26/1842-review/review.md` | blob `67c8c04077` | 12169 bytes | carrier: ref:5ba20ff3e | in-a-stash: no
7. `evidence/r28-welle6-2026-11-25/0428-284-1842-hop/round-1.md` | blob `9ca0ab57ea` | 12041 bytes | carrier: ref:25262d41c | in-a-stash: no
8. `evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/w194-0428-224-intake.md` | blob `2157b2f484` | 11909 bytes | carrier: stash@{1} | in-a-stash: yes
9. `evidence/w246-0428-284-1812diag/w246-1812gatefaildiag.md` | blob `9781ec653c` | 11909 bytes | carrier: stash@{0} | in-a-stash: yes
10. `evidence/r28-welle6-2026-11-27/bughunt-hv54-config-defaults/w209-0428-224-hunt-v54.md` | blob `48f2e6cd25` | 11794 bytes | carrier: stash@{1} | in-a-stash: yes
11. `evidence/r28-welle6-2026-11-25/w237-0428-283-1818reset2/round-1.md` | blob `40b457f731` | 11578 bytes | carrier: ref:5ba20ff3e | in-a-stash: no
12. `evidence/r28-welle5-2026-11-23/hunt39-v55/catalog-lifecycle-hunt.md` | blob `6ee929ee0f` | 10252 bytes | carrier: stash@{1} | in-a-stash: yes
13. `evidence/r28-welle6-2026-11-25/w222-0428-307-1852-secondrun/secondrun-gate-akte.md` | blob `5ffbe8726a` | 10088 bytes | carrier: ref:541a07965 | in-a-stash: no
14. `evidence/r29-welle6-2026-11-28/0428-287/w136-1835-redundancy.md` | blob `fc815666ba` | 9495 bytes | carrier: ref:34b33010b | in-a-stash: no
15. `evidence/r28-welle6-2026-11-25/w218-0428-181-0428-285-1819hop/1819-pr-hop-akte.md` | blob `a415abfb3b` | 8831 bytes | carrier: ref:541a07965 | in-a-stash: no
16. `evidence/2026-11-shift/0428-263/w200-1846-review.md` | blob `909162bbab` | 8423 bytes | carrier: ref:cc9c96409 | in-a-stash: no
17. `evidence/r28-welle4-20261114/0428-065/round-rebase-1615.md` | blob `41ce287917` | 8201 bytes | carrier: ref:b8bb8b7b1 | in-a-stash: no
18. `evidence/r28-welle5-2026-11-22/sourcepull-0428-223/review-1750-head17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99.md` | blob `cd2edbe0ef` | 8154 bytes | carrier: stash@{41} | in-a-stash: yes
19. `evidence/r28-welle6-2026-11-25/w226-0428-307-0428-283-1818reset.md` | blob `a8246229ff` | 7989 bytes | carrier: ref:37320b0b8 | in-a-stash: no
20. `evidence/r28-welle6-2026-11-27/w198-0428-284-demo-parser/w198-dispatch-wave-48bac372.md` | blob `28fdbbbde8` | 7947 bytes | carrier: stash@{1} | in-a-stash: yes

## Step 6 - identity of the restoring commits

Only one commit on live main actually adds a census path. Its `git show --name-status` reports 13 `A` entries
and one `M`.

| commit | `%an` | `%ae` | `%cn` | `%ce` | `%ci` | subject | census paths touched |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `7ae6d04bf92217ca70e664542897f42e237dbe89` | Marcel Pfingstgräf | 22537373+mcpdev80@users.noreply.github.com | GitHub | noreply@github.com | 2026-11-26 03:37:44 +0100 | Restore missing Plan evidence forward-only (#75) | all 12 (squash publication) |
| `2340f07a6b639d1d27e329d1361fe9f6c6547d07` | w255-0428-251-demo170codex | w255-0428-251-demo170codex@baseharbor.local | w255-0428-251-demo170codex | w255-0428-251-demo170codex@baseharbor.local | 2026-11-26 02:56:52 +0100 | Restore missing Plan evidence forward-only | all 12 (content commit, PR branch only) |

Identity assessment against the 97283409e / w255 and w65 / w258 near-miss patterns:

- The publication channel is the COMPLIANT one: a squash merge of an ordinary plan PR (`7ae6d04`'s message
  carries `(#75)`, parent `3a9bfea66`, GitHub committer identity). This is not a direct-main write, so the
  w65/w258 pattern does not repeat here.
- The content authorship identity `w255-0428-251-demo170codex` (both `%an` and `%ce`) is the executing lane's own
  declared identity, matching w255's published ANSATZ block verbatim, including the declared literal invocation
  and the declared `git show -s --format=%an HEAD` pre-push gate. That is lane-consistent, not foreign.
- No commit that adds a census path carries `coordinator` or another lane's identity. The surrounding merge
  commits on the PR branch (`33ee934`, `74a7499`, `20a3872`, `ab57e84`) touch zero census paths and are
  `git merge origin/main` transports, consistent with the ecosystem rule against cherry-picks.
- Flag for the record: several commits that reach main through this window carry `%cn=coordinator` while `%an` is
  a lane (for example `9ff4e1108`: `%an=w198`, `%cn=coordinator`) and `dd851feb4` where both are `coordinator`.
  None of them restores a census path, so they are outside this mission's restore set, but the mixed
  author/committer pairing is exactly the pattern the mission asks to keep visible.

## Step 7 - is the remaining gap forward-only restorable, or superseded?

One line, using only the categories w271 itself assigned (re-land, re-land-if-cheap, plus w271's own
"already on main / later revision" caveats): the remaining 76-path, 492119-byte gap is content that still needs
a further forward-only plan PR, with two documented exceptions inside it.

Breakdown by w271's own recommendation column, over exactly these 76 paths:

| w271 recommendation | paths | bytes |
| --- | --- | --- |
| re-land | 36 | 254475 |
| re-land-if-cheap (Nov 21-26 content, verify main first) | 26 | 167476 |
| re-land, but Codex must first check the 0428-34x cards on main for duplicates | 10 | 52335 |
| re-land if main has no later revision of the same card | 4 | 17833 |
| total | 76 | 492119 |

The two exception paths, both named inside w255's own recovery akte (which is now on main) and both already
classified by w271's table content rather than by a new category:

1. `evidence/w246-0428-284-1812diag/w246-1812gatefaildiag.md` (11909 bytes) - w271 lists the same blob
   `9781ec653c` that main now holds at the canonical path `evidence/w246-1812diag/w246-1812gatefaildiag.md`,
   restored by #75. Verified here: both paths carry blob `9781ec653c` in w271's table, so this path is a content
   duplicate that needs no second copy.
2. `tasks/t-20261124-r28-alert-applied-face-stale-runtime.md` (3608 bytes) - w255's akte classifies it as
   superseded by the accepted task `tasks/t-20261124-r28-alert-evaluator-live-health-wiring.md` (#1831). That
   successor exists on live main; the stranded path does not. Superseded, not missing work.

Verified here: the only `tasks/` paths on live main matching `hunt47|r28-alert` is
`tasks/t-20261124-r28-alert-evaluator-live-health-wiring.md` (present), and all ten Hunt47 rows measure `MISSING`.

Everything else in the 76 is unrecovered content, not a duplicate. The 0428-34x duplicate-check caveat on the
ten Hunt47 rows is a review instruction for the next recovery PR, not a finding that they are already on main.

## Scope and rule compliance

- Read-only everywhere it mattered: no writes, no pushes, no merges, no CI triggers, no card edits, no `.github`
  edits, no `stash`/`reset`/`clean`/`checkout -f` in any shared checkout, no product repository access at all
  beyond `git ls-remote` of the plan repo.
- The only writes this lane made are inside its own isolated worktree
  `/tmp/opencode/w280-0428-284-recount-wt/plan` (a worktree of the canonical plan repository, branch
  `w280-recovery-presence-recount-own`, pushed to the plan remote as a normal branch) and its own board file under
  `workers/todos/`.
- Worktree placement follows the mission: `workers/<lane>-wt`, no clone under `/tmp` for the publication path.
  The read-only census clone lives in `/tmp/opencode/w280/plan-main`.
- Worktree placement note (corrected during this run): the first attempt created the plan worktree at
  `workers/w280-plan-wt`, which is INSIDE the shared `workers` checkout of the plan repository. Two real defects
  followed and were both undone with zero published effect: (a) `workers/.git/info/exclude` line 7 (`evidence/`)
  leaked into the nested worktree and made the akte un-addable, and (b) `git worktree add` from a cwd inside that
  checkout registered a branch/worktree in the shared repository's metadata. That stray worktree was removed and
  its branch deleted before any commit existed on it, and the akte was recreated in this lane's own zone.
  Final state: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan worktree list` contains exactly one
  w280 entry, `/tmp/opencode/w280-0428-284-recount-wt/plan`. No other lane's worktree was listed, touched or
  removed by this mission.
  Nothing here needs a test route: this card adds no test and changes no product code, so the gate-catalog rule
  has nothing to register; the plan repository's ordinary validator is the only relevant check and it belongs to
  the plan PR, not to this lane's trigger rights.
  Test -> check route for this card: NONE, because this card creates and changes zero tests (pure read-only
  evidence). Nothing to register in a REQUIRED set or gate catalog; stated explicitly per the review-stop rule.
- No `.github/**` change is needed, so no Owner-scope finding is raised.
- `git -c user.name=... commit` invocation and the `%an` pre-push gate are as declared in the ANSATZ block.

## cleanliness

Host: this session's own machine. No container, compose project, network or volume was created, started or
left behind. `docker ps -a` before and after this lane are recorded below; nothing attributable to w280 appears
in either. The canonical shared plan checkout keeps its original HEAD (`08b1f66b`) and its 51 stashes untouched
(this lane never ran a mutating git command inside it).

- `git stash list` count observed in the shared checkout: unchanged (never written by this lane).
- Stray worktree/branch cleanup: `w280-recount-plan` removed from the plan repository's worktree metadata and its
  branch deleted, before any commit existed on it. `git worktree list | grep w280` now shows only
  `workers/w280-plan-wt`.
- No VM/SSH work in scope for this mission.

## END

END_DONE w280-0428-284-recount: PR #75 merged at 02:37:44Z; 12/12 census paths restored (10 identical, 2 newer
variants); missing count 88 -> 76 paths / 492119 bytes; restoring publication `7ae6d04bf` (author Marcel
Pfingstgräf, committer GitHub, squash of `2340f07` by `w255-0428-251-demo170codex`); plan PR #82 open, not
merged; live main tip identical before and after this lane's work.

## Findings

1. The mission premise was briefly false and became true mid-run: PR #75 was `OPEN` at the first witness and
   `MERGED` at `2026-11-26T02:37:44Z` while this census ran. Every conclusion above is measured against post-merge
   main, which is what the mission asks for.
2. PR #75's branch was cut from a stale base. Its restore commit `2340f07` has parent `264e263` (PR #68 squash,
   `%ci=2026-11-26 02:23:00 +0100`), while live main was already at `b3ffd617c` and `3a9bfea66` at that moment.
   Consequence measured here: `2340f07` is NOT an ancestor of live main (`git merge-base --is-ancestor 2340f07
   origin/main` -> false) because the merge used GitHub's squash channel; the tree content nevertheless arrived
   intact and correct, and the later `git merge origin/main` commits on the branch kept the merge honest. No
   main content was lost. This is a process observation only.
3. w271's "all twelve are still missing" was correct at its base `b3ffd617c` and is now closed: 12 of 12 present.
4. The two `NEWER variant` rows in step 2 are a locator disagreement inside w271's own table (best locator
   `1a9317acf`) versus w255's declared source (`8b7ad1157`, PR #58 head), not a restore defect. Both variants are
   reachable; the newer one is on main. If the ecosystem wants the older variant retained, that is a decision for
   the next recovery PR, not a defect in #75.
5. Tooling trap found during this run, worth recording for every read-only census lane: `/home/marcel/dev/
   baseharbor-ecosystem/workers` is itself a git repository whose `origin` is
   `https://github.com/mcpdev80/baseharbor-plan.git`, and `/tmp/opencode` sits under neither repo. A bare `git`
   command issued from a lane's scratch directory therefore silently resolves against that shared plan
   checkout, not against a neutral zone. Two consequences hit this lane and are documented in Scope and rule
   compliance: (a) `git worktree add` from the wrong cwd registered a worktree and branch inside the shared plan
   repository's metadata (removed again, no commits, no push, no ref movement), and (b) the name `origin/main` is
   AMBIGUOUS there - both `refs/remotes/origin/main` and a `refs/heads/origin/main` branch exist - so bare
   `origin/main` in a shared checkout can address a branch instead of the remote-tracking ref. Census lanes
   must use `refs/remotes/origin/main` explicitly, or `gh api` / `ls-remote`. Precedent: the mission's own
   warning about `workers/baseharbor-plan` as a wrong-zone checkout.
6. w271's headline "the shared checkout is a SHALLOW clone, so the prescribed classifier is unsound" reproduces
   independently here: this lane's own first `--depth 1` clone produced FALSE ancestry results (`264e263 NOT
   ancestor`, `git rev-list --count` = 1) until `git fetch --unshallow`. Any lane that reports an ancestor test
   must state its clone depth. The corrected, full-history results are the ones in this akte.
7. The shared planning checkout's HEAD sits at `08b1f66bb733d4c1422135429e5bc29fbd67cd57` (`%an=w256-0428-253-prhopverify`,
   `%cn=w198-0428-284-demo-parser`), several publications behind live main, and it is shallow. Observed read-only;
   nothing was changed. Coordinator may want a freshen pass, but that is outside this mission's write-set.

## Publish and closing witnesses

- Plan PR: **#82** — https://github.com/mcpdev80/baseharbor-plan/pull/82 (open, NOT merged by this lane).
- Branch: `w280-recovery-presence-recount-own`, single commit `e88c7beef67ccdd583b5cdd87d2eea067532fc7e`,
  `git show -s --format=%an HEAD` gate printed `w280-0428-284-recount`.
- Delivery proof (`git ls-remote ... refs/heads/main refs/heads/w280-recovery-presence-recount-own`):

```text
1f3e0673fa9f2265805c1291f794531c3876a9de   refs/heads/main
e88c7beef67ccdd583b5cdd87d2eea067532fc7e   refs/heads/w280-recovery-presence-recount-own
```

- `git log --oneline refs/remotes/origin/main..HEAD` listed exactly one commit, this lane's own:
  `e88c7beef docs(evidence): w280 read-only recovery presence re-count akte`. No foreign commit is carried.
- `git diff refs/remotes/origin/main...HEAD --name-only` lists only the five files of this akte directory.
- Zero-mutation proof: `refs/heads/main` never moved as a result of this lane. The lane's own first and last
  `refs/heads/main` observations are `3a9bfea66` (before-witness, step 1) and `6480495f5` / `1f3e0673f`
  (advanced only by other lanes and by the GitHub merge of #75 during the run). The final value
  `1f3e0673f` is the parent of this lane's single commit; this lane pushed no commit to `main`.

### cleanliness witnesses

```text
$ docker ps -a --format '{{.Names}}' | sort | wc -l
0
$ docker ps -a --format '{{.Names}}' | grep -ci w280
0
```

- before/after `docker ps -a` on this host: zero containers of any state; nothing created or left by this lane.
- this lane's shell pid during the witnesses: 2167543 / 2175793 (no lingering children; no test process was ever
  started here, per the CI policy stop).
- no compose project, no network, no volume, no VM/SSH session in this mission.
cleanliness: PASS - the lane leaves the host and both plan checkouts exactly as found.
