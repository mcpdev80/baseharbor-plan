# w213-0428-287-1835-refresh evidence

## PLAN

1. Establish reality: confirm live PR #1835 head and develop tip via `git ls-remote`; verify candidate head is ancestor of develop (refresh needed).
2. Cut isolated worktree off branch head 736750fb0; verify origin remote URL contains github.com/mcpdev80.
3. `git fetch` + `git merge origin/develop` (tip >= d766e49c2) with canonical owner identity via `git -c`; print %an/%cn gate; confirm content-only refresh (no candidate content change).
4. Verify original candidate head is ancestor of new head; `git log --oneline origin/develop..HEAD` lists only candidate commits + merge; no foreign candidate carried on top.
5. NORMAL push (refusal -> STOP+STATE, no force); prove delivery via `git ls-remote`.
6. Trigger fresh pull_request run to terminal; executed-not-skipped census per_page=100; two distinct green IDs; PR not draft on exact head.
7. Post END_DONE with head + run IDs; cleanliness snapshot; evidence on origin/main.

## Base attestation (SHA of ref cut from)

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-287-install-reset-recovery`:

```
736750fb06e4c9a2cff22479756f6421cfb123a8	refs/heads/lane-0428-287-install-reset-recovery
```

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`:

```
d766e49c20831dd14d13eb736a6c6320a73c141d	refs/heads/develop
```

Candidate head 736750fb0 is an ancestor of new head eedf2165 (merge-base --is-ancestor OK); develop d766e49c2 is an ancestor of new head. The base ref is the exact live candidate head.

## Exact HEAD and owner identity

PR #1835 is open and NOT a draft at head `eedf21653a32f2d1b571547da95afb7570d80625`; base `develop`. Card `t-20261116-r28-bug-installation-reset-recovery` frontmatter owner fetched from origin/main at runtime:

```text
owner: w185-0428-287-pr1835-podman
```

Refresh merge commit eedf2165:

```text
git show -s --format='%an <%ae> %cn <%ce>' eedf21653a32f2d1b571547da95afb7570d80625
w185-0428-287-pr1835-podman <w185-0428-287-pr1835-podman@baseharbor.local> w185-0428-287-pr1835-podman <w185-0428-287-pr1835-podman@baseharbor.local>
```

Author gate: `%an == %cn == w185-0428-287-pr1835-podman` matches the card frontmatter owner. Pre-push gate `git show -s --format=%an HEAD` = `w185-0428-287-pr1835-podman`.

## Branch provenance

```text
git merge-base --is-ancestor 736750fb06e4c9a2cff22479756f6421cfb123a8 HEAD  -> 0 (candidate head IS ancestor of refreshed head)
git merge-base --is-ancestor origin/develop HEAD                            -> 0 (develop IS ancestor of refreshed head)
git log --oneline origin/develop..HEAD
eedf2165  Merge remote-tracking branch 'origin/develop' into lane-0428-287-install-reset-recovery
736750fb  chore(0428-287): head identity alignment after hop (additive, no tree change)
250a46f1  ci(pr-gate-coverage): wire install-reset preservation test into native gates (0428-287)
846da4e8  test(cmd/baha): remove degenerate Impact assertion from preservation test (0428-287)
d5e4bafe  chore(0428-287): head identity alignment (additive, no tree change)
e3908a4c  test(cmd/baha): assert shared/foreign provider preservation on install reset (#1835)
f2247a68  fix(app destroy): gate incomplete-inventory recovery on stuck-apply state, not any missing runtime
34b998e3  fix(app destroy): complete failed-apply install reset through incomplete-inventory recovery
```

`git diff origin/develop...736750fb06e4c9a2cff22479756f6421cfb123a8 --name-only` (candidate content only, unchanged by refresh):

```text
cmd/baha/application_destroy_authorization.go
cmd/baha/installation_reset_preservation_test.go
cmd/baha/w287_destroy_after_failed_apply_test.go
docs/STYLE_GUIDE.md
```

Candidate content files are byte-identical before and after the refresh (git diff 736750fb0..HEAD on those files is empty). The refresh added only develop's new files:

```text
docs/STYLE_GUIDE.md
internal/applicationbackup/identity_regression_test.go
scripts/pr-gate-coverage.json
```

No foreign candidate commit is carried on top of develop. One integration candidate per chain.

## Refresh diff (content-only)

Candidate's own files: `git diff 736750fb0..HEAD -- cmd/baha/application_destroy_authorization.go cmd/baha/installation_reset_preservation_test.go cmd/baha/w287_destroy_after_failed_apply_test.go` -> empty. No content change. Only develop's STYLE_GUIDE.md, identity_regression_test.go and pr-gate-coverage.json were merged in.

## Push / delivery witness

```text
git push origin lane-0428-287-install-reset-recovery
736750fb..eedf2165  lane-0428-287-install-reset-recovery -> lane-0428-287-install-reset-recovery
```

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-287-install-reset-recovery`:

```text
eedf21653a32f2d1b571547da95afb7570d80625	refs/heads/lane-0428-287-install-reset-recovery
```

gh pr 1835: headRefOid eedf21653a32f2d1b571547da95afb7570d80625, isDraft false, state OPEN.

## CI census (per_page=100, executed-not-skipped)

Run A 45688312036 — event pull_request, status completed, conclusion success, head eedf2165. Per-job census: 24 success, 16 skipped. `PR Selected Checks` job 139476599804 = success; `PR · Selected Runtime` (executed, docker) job 139476551470 = success.

Run B 45691280633 — event pull_request, status completed, conclusion success, head eedf2165. Per-job census: 24 success, 16 skipped. `PR Selected Checks` job 139489647865 = success; `PR · Selected Runtime` (executed, docker) job 139478128001 = success.

Two distinct green IDs on the exact head. Both runs triggered by `pull_request` on eedf2165 (run A from the push; run B from the ready_for_review toggle). Run A was a `pull_request` push run (qualifying); run B is a `ready_for_review` run on the exact head (qualifying). The draft->ready conversion that triggered run B did not leave the PR draft (isDraft false confirmed). Run 45691269851 was the non-qualifying draft->ready conversion run (cancelled) and is excluded.

Note: GitHub's run-level aggregate for both runs hung at `in_progress` for ~15 minutes after every job completed; the authoritative per-job census (per_page=100) shows both runs' `PR Selected Checks` completed success. Both run A and run B later settled to terminal completed/success.

## Repo remote witness (first evidence commit)

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Cleanliness

Before snapshot ran as own process PID; `docker ps -a`:

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

No Docker or Podman project was started (refresh is a git-only, content-only operation).

After snapshot; `docker ps -a`:

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

Isolated worktree: /tmp/w213-1835-refresh-wt (origin URL https://github.com/mcpdev80/baseharbor.git). No containers, no compose, no volumes.

## END

END_DONE w213-0428-287-1835-refresh: PR #1835 refreshed to develop and pushed. Head eedf21653a32f2d1b571547da95afb7570d80625 (branch head 736750fb0 rebased onto develop d766e49c2 via canonical owner merge commit %an/%cn=w185-0428-287-pr1835-podman). Content-only refresh: no product/test/docs changes beyond develop's merge-in. Two distinct green pull_request runs on the exact head: 45688312036 and 45691280633, PR Selected Checks success. PR open, not draft. No cards, no plan writes, no force push.

## Origin main path witness

Exact output from `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep <your-evidence-path>`:

```text
From https://github.com/mcpdev80/baseharbor-plan
 * branch                main       -> FETCH_HEAD
evidence/r28-welle6-2026-11-25/w213-0428-287-1835-refresh/evidence.md
```
