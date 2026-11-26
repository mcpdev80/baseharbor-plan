# w290 residual-recovery audit — card 0428-251

READ-ONLY PLAN-RECOVERY RESIDUAL AUDIT. Coordinator commission 2026-11-26. No new cards, no product writes.

## Visible identity block (per mission VISIBLE ANSATZ requirement)

Exact per-card frontmatter owner VERBATIM, fetched from origin/main at runtime. Card `t-20261123-demo-digest-consent-adaptation` (0428-251) owner line on `origin/main` at `2eb677c1e994f0e79ffe5f6061863e553177664f`:

```
owner: Coordinator (merge 1450) / 9b7683b5
```

Git identity used for this lane's commit (canonical, full form — no shortening, never 'coordinator', never another lane):

```
user.name  = w290-0428-251-recoveryverify
user.email = w290-0428-251-recoveryverify@baseharbor.local
```

Literal commit invocation (to be used on the plan PR, never on shared checked-out main):

```
git -c user.name=w290-0428-251-recoveryverify -c user.email=w290-0428-251-recoveryverify@baseharbor.local commit -m "docs(evidence): residual audit of stranded-evidence recovery 0428-251 (w290)"
```

Pre-push author gate (must print this exact line before push; stop on any mismatch):

```
git -C <plan-wt> show -s --format='%an' HEAD   -> w290-0428-251-recoveryverify
git -C <plan-wt> show -s --format='%an <%ae>' HEAD  -> w290-0428-251-recoveryverify <w290-0428-251-recoveryverify@baseharbor.local>
```

## Reality witnesses

Planning-repo remote (before first evidence commit):

```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Base attestation (live remote main at start of audit):

```
git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main -> 2eb677c1e994f0e79ffe5f6061863e553177664f
```

baseharbor (product) remote heads:

```
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop -> ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/main    -> cddc81b34fe13d8befdde4c487b365a0309ba428
```

Base-ancestry: this audit used only a detached read-only worktree under /var/tmp (branch origin/main) plus `gh api` / `git cat-file` reads. No branch was cut, no commit made in any live checkout.

## Method

1. Rebuilt the original w271 loss list from the merged akte `evidence/coordination/w271-stranded-recovery-w255-0428-251-demo170codex.md` (present on origin/main) and Plan PR #76's census akte `evidence/w271-stranded-census/akte.md` (PR #76, head 2957b9144, merged 2026-11-26T04:01:58Z).
2. Classified each of the 88 census paths against live `origin/main` (`2eb677c1e`) via `git cat-file -e origin/main:<path>` and cross-checked with `gh api repos/mcpdev80/baseharbor-plan/git/trees/<main-tip>?recursive=1`.
3. Residual figure computed from the original loss list, not from the 12-item inventory.
4. Identity provenance read via `git cat-file -p` per commit (no checkout of shared worktrees).

## (1) Loss list reconstruction

Source: w271 PR #76 census (PR #76 head `2957b91448babb6af5a546827e2d383f3bba8dac`). The census stated **88 missing evidence/task paths totalling 632,946 bytes**. I rebuilt all 88 rows by combining the census's two tables: section A (12 recovery artifacts, 140,827 bytes) + table B (76 unique needs-land rows, 492,119 bytes) = 88 rows, 632,946 bytes. Byte total matches the census figure exactly (difference 0). The 2 paths the census explicitly excluded as non-loss (content duplicates: `evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/w194-0428-224-intake.md` dup of root `w194-0428-224-intake.md`; `evidence/w246-0428-284-1812diag/w246-1812gatefaildiag.md` dup of the canonical `w246-1812diag` blob `9781ec65`) are among the 88 but classified as non-loss. The path `tasks/t-20261124-r28-alert-applied-face-stale-runtime.md` that the original w271 list also tagged "superseded by accepted 0428-268 via #1831" is NOT in fact dispositioned: it is absent at its census path on live main `1b9b2bc70`, never in main's history, and has no 0428-268 successor card; it is therefore a genuine class-(c) residual, not a class-(d) non-loss (see the w298 correction in the class-(c) section).

## (2) Per-path presence classification on live main (2eb677c1e)

- PRESENT on main: 78 paths
- ABSENT on main: 10 paths (61,211 bytes)

Of the 10 absent:

Class (d) — deliberately excluded by Codex disposition / non-loss, NOT residual:

- `evidence/w186/0428-186-hop.md` (5,046 B) — parked checkbox exception (TOP_CHECKBOX lines at source lines 31-34 trip `check_stray_checkboxes` at scripts/plan.py:563-570); carrier blob b1540def552cad23e6bb0997ce9f93762527a679 preserved at source ref, not restored.
- `evidence/w266-0428-285-1820pre/PLAN.md` (1,343 B) — parked checkbox exception (TOP_CHECKBOX lines 7-13); carrier blob e41b0dac261342505f5c8b550e51f3ef40dbcb39 preserved at source ref, not restored.
- `evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/w194-0428-224-intake.md` (11,909 B) — exact content duplicate of root `w194-0428-224-intake.md` (blob 2157b2f484), present on main under the canonical path.
- `evidence/w246-0428-284-1812diag/w246-1812gatefaildiag.md` (11,909 B) — exact content duplicate of the canonical `evidence/w246-1812diag/w246-1812gatefaildiag.md` (blob 9781ec65), present on main under the canonical path.

These 4 (30,207 bytes) are dispositioned non-loss, not residual.

Class (c) — genuinely still missing on main, the residual figure: 6 paths, 31,004 bytes. None is present at its census path, none is in main's history (`git log origin/main -- <path>` and `git log --find-object=<blob> --origin/main` both empty), none is covered by a successor card number, and none survives on main's own refs:

CORRECTION (w298 2026-11-26, plan PR #95): the r28-alert task
`tasks/t-20261124-r28-alert-applied-face-stale-runtime.md` was listed in class (d) above as "superseded /
non-loss" in the section-(1) loss list (line 66) and here in class (d), yet the same path also appears in the
6-path class (c) residual list. Resolved by evidence on live main `1b9b2bc70`:
`git ls-tree -r --name-only origin/main | grep -F tasks/t-20261124-r28-alert-applied-face-stale-runtime.md` →
ABSENT at the census path; `git log --oneline origin/main -- <path>` → never in main's history; no card 0428-268
exists under any 0428-268 path on main (no successor card). The class-(d) definition ("deliberately excluded by
Codex disposition / non-loss") does NOT apply — no such disposition exists on main. The path is therefore NOT a
class-(d) dispositioned non-loss; it stays correctly in class (c) (genuinely residual). The 4 class-(d) non-loss
paths are now exactly the four listed above, and class (c) remains the 5 Hunt47 cards + this r28-alert task.

Corrected residual figure (consistent everywhere in this file):
Class (c) genuinely residual: 6 paths / 31,004 bytes
  - tasks/t-20261125-hunt47-destroystep-v1-warning-kind.md             5,745 B
  - tasks/t-20261125-hunt47-provider-registry-v1-migration.md         5,659 B
  - tasks/t-20261125-hunt47-recover-preflight-and-flag-route.md       5,395 B
  - tasks/t-20261125-hunt47-deployment-record-v1-wall.md              5,376 B
  - tasks/t-20261125-hunt47-keycloak-migration-docs.md                5,221 B
  - tasks/t-20261124-r28-alert-applied-face-stale-runtime.md          3,608 B
Class (d) dispositioned non-loss (do NOT re-land): 4 paths / 30,207 B (2 checkbox-parked, 2 content-dup).

- `tasks/t-20261125-hunt47-destroystep-v1-warning-kind.md` (5,745 B)
- `tasks/t-20261125-hunt47-provider-registry-v1-migration.md` (5,659 B)
- `tasks/t-20261125-hunt47-recover-preflight-and-flag-route.md` (5,395 B)
- `tasks/t-20261125-hunt47-deployment-record-v1-wall.md` (5,376 B)
- `tasks/t-20261125-hunt47-keycloak-migration-docs.md` (5,221 B)
- `tasks/t-20261124-r28-alert-applied-face-stale-runtime.md` (3,608 B)

The 5 Hunt47 cards survive only in carrier `a47da84b82f2fd10294c934944566d4d935c61a1` (`refs/heads/lane-0428-224-hunt47-intake-w193`, the Hunt47 intake ref), which is not main. Their card numbers 0428-341..344 and 0428-346 collide on main with Hunt48 cards (`tasks/t-20261128-hunt48-*.md`) that are a different subject; no renumbered successor carrying the same text exists. The r28-alert task (0428-268) is not present under any 0428-268 path.

## (3) Residual figure

- Class (c) count: **6 paths**
- Class (c) byte total: **31,004 bytes**
- Recovery-line verdict: **NOT CLOSED** — residual class (c) is non-zero. 78 of 88 census paths (601,735 bytes of the original list) are now on main; 6 paths (31,004 B) remain genuinely missing, plus 4 dispositioned non-loss paths that must not be re-landed.

## (4) Identity provenance of the recovery commits

Recovery commits carried the restores onto main via squash-merge commit `27aff0b938df76bd4a7d0116a9b320e5d84123e3` (PR #83, merge 2026-11-26 03:55:41Z). Identity census via `git cat-file`:

| commit | an | cn | verdict |
| --- | --- | --- | --- |
| `27aff0b938df` (PR83 squash merge) | Marcel Pfingstgräf | GitHub | GitHub squash-merge; owner identity, not a lane identity — expected for a squash merge |
| `f0109585` (PR89 post-merge witness) | Marcel Pfingstgräf | GitHub | GitHub squash-merge; owner identity — expected |
| `267a6033852088` (w255 record recovery candidate provenance) | w255-0428-251-demo170codex | w255-0428-251-demo170codex | canonical lane identity, clean |
| `ed73b155a` (record recovery provenance, reallocate Hunt47) | w255-0428-251-demo170codex | w255-0428-251-demo170codex | canonical lane identity, clean |
| `cd10e57e6` (record final recovery scope) | w255-0428-251-demo170codex | w255-0428-251-demo170codex | canonical lane identity, clean |
| `232355ab298bf7` (merge origin/main) | w255-0428-251-demo170codex | w255-0428-251-demo170codex | canonical lane identity, clean |
| `9d3da6c1d` (w271 census) | w271-0428-284-stranded | w271-0428-284-stranded | lane identity, clean |
| `f07ba6e06` (w271 closing witnesses) | w271-0428-284-stranded | w271-0428-284-stranded | lane identity, clean |
| `d2e22069b` (w271 SHA correction) | w271-0428-284-stranded | w271-0428-284-stranded | lane identity, clean |

No commit uses a shortened wNNN form, nor the bare `coordinator` lane-authoring identity for a lane-owned commit. The one `coordinator`-identity anomaly the w271 akte disclosed (commit `4870ae147`, PR #76, fell back to repo-local `coordinator` via a bare `--amend`) is NOT part of this recovery chain and is not reachable from main (PR #76 was squash-merged; the branch is gone).

## (5) Generated-view diff verdict

Rendered in throwaway worktree `/var/tmp/w290-planwt` (detached origin/main, read-only), `python3 scripts/plan.py render` exited 0. Diff against origin/main:

```
roadmap/cards.md    : IDENTICAL to origin/main
views/overview.md   : IDENTICAL to origin/main
views/ready.md      : IDENTICAL to origin/main
views/kanban-dashboard.md : IDENTICAL to origin/main
```

No hand-edited generated drift. No generated file on main deviates from `scripts/plan.py render` output.

## (6) Zero-mutation proof

This audit performed no commit, branch, push, rebase, stash, checkout, reset, merge, or workflow event. All reads ran from a detached read-only worktree under /var/tmp plus `gh api`. No `.git` object in the shared primary checkout was written.

baseharbor-plan shared checkout BEFORE vs AFTER (the one pre-existing foreign uncommitted file and two foreign untracked dirs were created by OTHER lanes, never by this read-only audit; left exactly as found):

| witness | BEFORE | AFTER |
| --- | --- | --- |
| `git rev-parse HEAD` | `08b1f66bb733d4c1422135429e5bc29fbd67cd57` | `08b1f66bb733d4c1422135429e5bc29fbd67cd57` |
| `git stash list | wc -l` | 51 | 51 |
| `git status --short` | ` M tasks/t-20261122-runtime-broker-health-unhealthy.md` (foreign) | same + 2 foreign untracked dirs (w274, w281) not created by this audit |

No w290 branch exists on GitHub: `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/*w290*` returns empty.

baseharbor (product) remote heads unchanged during audit: develop `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`, main `cddc81b34fe13d8befdde4c487b365a0309ba428`.

## (7) Akte / plan PR

This audit is read-only; per the mission I do NOT create a PR or push anything. The residual findings are a report, not a fix. Per mission rule 6 ("DO NOT FIX ANYTHING you find") and the zero-mutation constraint, there is no plan PR to open and no merge. The 6 class-(c) paths are disposition candidates for a future recovery lane, not work for this read-only audit.

## END

END_DONE w290-0428-251-recoveryverify: residual class (c) = 6 paths / 31,004 bytes; recovery line NOT closed (class c != 0). 78 of 88 census paths present on main 2eb677c1e; 4 absent paths are dispositioned non-loss (2 checkbox parked, 2 content-dup). Identity census clean (only GitHub squash-merge owner identity on 27aff0b9/f0109585, lane identities on the w255/w271 work). Generated views identical to `plan.py render`. Zero-mutation proof: HEAD/stash/refs unchanged, no w290 branch, product heads unchanged. Read-only audit; no PR created, no merge.

END w290-0428-251-recoveryverify: DONE, residual = 6 paths / 31,004 bytes (class c), recovery line OPEN.

## cleanliness

No containers, compose projects, VM sessions or network namespaces created. No product writes. Scratch under /var/tmp (read-only detached worktree `w290-planwt`, no writes into it) and /tmp (parsed census akte + tree lists). No leftover worktrees beyond the read-only /var/tmp/w290-planwt (removed at END). No docker ps witness needed (no containers).
