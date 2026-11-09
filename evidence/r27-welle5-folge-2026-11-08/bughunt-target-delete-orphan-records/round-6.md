# 0427-165 round 6 — landing-refresh onto develop (PR #1500, terminal SUCCESS)

**Card:** 0427-165 · `t-20261108-bughunt-target-delete-orphan-records`
**PR:** https://github.com/mcpdev80/baseharbor/pull/1500
**Branch (PR #1500 head):** `0427-165-target-delete-orphanrec`
**HEAD:** `f966505cda93aa35da60ad65afee5e885e4886c9`
**Driving review (r5):** APPROVE code delta; landing gated only by refresh onto current develop + terminal run (act-1500-review-r5.md, vm-bughunt/, plan)

## PLAN

- Rebase the 0427-165 orphan-refusal branch linearly onto the current develop tip and verify current develop is an ancestor of the resulting candidate.
- Keep the r5 content byte-for-byte; resolve any overlap with develop's #174 / #1505 changes in `deployment_list.go` and `deployment_store.go` side-by-side (orphan-abweis path untouched).
- Local: gofmt/vet/build + deployment + cmd/baha target/orphan/destroy green; readability audit PASS.
- Force-push with lease to PR #1500 head; observe hosted CI terminal on the exact head; publish round-6 evidence; END (terminal only).

## Reality witnesses (verbatim)

- `git ls-remote origin develop` → `e072e142ec9511f3cc86ffa67c7debd022d7760a`
- `git ls-remote origin refs/heads/0427-165-target-delete-orphanrec` → `f966505cda93aa35da60ad65afee5e885e4886c9`
- `git ls-remote origin refs/pull/1500/head` → `f966505cda93aa35da60ad65afee5e885e4886c9`
- `gh pr view 1500 --repo mcpdev80/baseharbor --json headRefOid` → `"headRefOid":"f966505cda93aa35da60ad65afee5e885e4886c9"` (state OPEN, base develop)
- Ancestry: `git merge-base --is-ancestor e072e142ec9511f3cc86ffa67c7debd022d7760a HEAD` ⇒ YES (develop `e072e142e` is an ancestor of the candidate).

## The base moved since r5

PR #1500 head was last at `64d621f4` (r5), based on develop `942111d5a`. Between r5 and this landing, develop advanced one feature:

```
$ git log --oneline 942111d5a..e072e142e
e072e142 fix(cmd/baha): safe 'baha app prune' for dangling deployment records (#1505)
```

`#1505` (the 0427-173 app-prune feature) modifies `deployment_store.go` — the same storage file the 0427-165 orphan refusal touches — so this landing was a genuine base-refresh with an overlap to resolve, not a no-op rebase.

## Rebase onto develop `e072e142e` — 6 linear commits, no conflicts

```
$ git rebase e072e142e
Rebasing (1/6)...Rebasing (6/6)
Successfully rebased and updated refs/heads/r6-landing2
$ git log --oneline 942111d5a..HEAD   # (old base, for reference of the chain)
f966505c refactor(internal/deployment): move ErrTargetDetachedWithOrphans to deployment_orphan_refusal.go
ea8ba312 test(0427-165 r5): exercise real app-destroy heal path in target-delete refusal test
decf25aa fix(0427-165 r4): exact orphan identity + honest healing (0427-173)
02790513 fix(0427-165 r3): blank-safe orphan identity + honest recovery guidance (0427-173)
36de50db fix(0427-165 r2): enforce decode-uuid==foldername in CollectableOrphans
b3870067 fix(cmd/baha, internal/deployment): refuse target delete while collectable orphan records attached
```

6 commits, single parent each, develop `e072e142e` the direct base. `#1505`'s changes to `deployment_store.go` (its `deployment_identity_drift.go` split + `DeleteDeploymentRecord` guard) and the `#174` access-denied/malformed blocks are disjoint from the 0427-165 orphan refusal — both land cleanly side-by-side.

## Overlap resolution — side-by-side, content preserved

- `deployment_list.go`: the 0427-165 `CollectableOrphans` function is **byte-identical** to the r5 head `64d621f4`. The only diff vs r5 is the `#1505`/`#174` `classifyOwnerWarning` block that develop introduced at the same seam — it coexists with `CollectableOrphans`, it does not replace it. The orphan-abweis path (fail-closed, no foreign/blank record advertised) is untouched.
- `deployment_store.go`: `ErrTargetDetachedWithOrphans` is unchanged in content; `#1505`'s drift-split content sits in the bottom half of the file (`assertOnDiskIdentityMatches`, `DeleteDeploymentRecord`), the orphan error sits in the top half — no textual overlap, both preserved.

## Readability-ratchet fix (self-inflicted, corrected)

The rebase applied develop's `#1505` growth on top of the already-full `deployment_store.go`, pushing it to **816 lines** (limit 800), which failed `PR · Source format` on the r5-era head `181f524b`. Resolution was a pure file move — no semantic change, no behaviour change:

- Extracted the cohesive `ErrTargetDetachedWithOrphans` named error (+ its doc comment) into a new file `internal/deployment/deployment_orphan_refusal.go`.
- `deployment_store.go` returns to **798 lines** (≤ 800). The `errors` import it used is the only one dropped; the symbol is unchanged and still referenced from `cmd/baha/target_definition_change_plan.go:168`.

This was a failure in my own candidate (not a foreign/develop fail), so it is not external STATE — it was corrected before the landing run, and the corrected head passes `PR · Source format`.

## Content proof (verbatim diffs)

```
$ for f in cmd/baha/target_definition_orphan_refusal_test.go \
           internal/deployment/collectable_orphans_test.go \
           cmd/baha/target_definition_change_plan.go; do
    git diff --quiet 64d621f4 HEAD -- "$f" && echo "IDENTICAL: $f"
  done
IDENTICAL: cmd/baha/target_definition_orphan_refusal_test.go
IDENTICAL: internal/deployment/collectable_orphans_test.go
IDENTICAL: cmd/baha/target_definition_change_plan.go

$ # CollectableOrphans identical vs r5 head
$ diff <(git show 64d621f4:internal/deployment/deployment_list.go | sed -n '/^func CollectableOrphans/,/^}$/p') \
       <(git show HEAD:internal/deployment/deployment_list.go | sed -n '/^func CollectableOrphans/,/^}$/p')
(no output = identical)
```

## Local verification (verbatim)

```
$ go build ./...
BUILD OK

$ gofmt -l internal/deployment/deployment_store.go \
           internal/deployment/deployment_orphan_refusal.go \
           internal/deployment/deployment_list.go \
           cmd/baha/target_definition_orphan_refusal_test.go
(gofmt clean)

$ go vet ./internal/deployment/... ./cmd/baha/...
(no output)

$ go test ./internal/deployment/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/deployment	0.055s

$ go test ./cmd/baha/ -run 'Target|Orphan|Destroy|Heal|Detach|Collectable' -count=1
ok  	github.com/mcpdev80/baseharbor/cmd/baha	17.259s

$ bash scripts/source-readability-audit.sh
Source readability
Go file size       PASS (<= 800 lines or no worse than explicit baseline)
Function span      PASS (<= 200 lines or no worse than explicit baseline)
Regression ratchet PASS
```

## Repo-rule compliance

- Changed files only: `.gitignore`, `cmd/baha/target_definition_change_plan.go`, `cmd/baha/target_definition_orphan_refusal_test.go`, `internal/deployment/collectable_orphans_test.go`, `internal/deployment/deployment_list.go`, `internal/deployment/deployment_orphan_refusal.go` (new). **No `.github/**`** file touched.
- No `workflow_dispatch`, no rerun, no manual runner: only the automatic PR-push trigger fired.
- No subagents (§4.8); every step run in this session.
- No containers/compose started; no containers of mine remain; worktree clean; no stray binary.
- Branch provenance: `git log --oneline` lists only my own commits; `git merge-base --is-ancestor e072e142e HEAD` ⇒ YES. One integration candidate per chain; no branch cut from another candidate.
- Only `git add` of the changed files; no `git add -A` in the worktree.

## Hosted run witness (exact head)

- Force-pushed: `git push --force-with-lease origin HEAD:refs/heads/0427-165-target-delete-orphanrec` → `181f524b...f966505c` (forced update; exit 0).
- `git ls-remote origin refs/pull/1500/head` → `f966505cda93aa35da60ad65afee5e885e4886c9` (confirmed via `gh pr view 1500 --json headRefOid` too; the `refs/pull/*/head` light ref had a short propagation lag after the push, then settled on `f966505c`).
- Hosted run **42598338207** (event `pull_request`) on exact head `f966505c`, terminal `completed/success`:
  - SUCCESS (all non-skipped jobs): PR · Workflow policy, PR · Native impact selection, PR · Trusted Plan, **PR · Source format**, PR · Native destroy retry · podman, PR · Native destroy retry · docker, PR · Focused Python, **PR · Native Keycloak/Core · podman**, **PR · Native Keycloak/Core · docker**, PR · Validation · deployment-package-tests, PR · Validation · go-vet, **PR · Validation · go-unit-tests**, PR · Validation · go-build, PR · Validation · cli-gofmt, **PR · Selected Checks**.
  - No job failed. `go-unit-tests` executed (not skipped); the two Native Keycloak/Core gates that failed on the r5 run now pass; `PR · Source format` (which failed on the 816-line pre-fix head) passes on the corrected 798-line head.

## END

END_DONE 0427-165-r6: landing-refresh complete and closed. Rebased the 0427-165 orphan-refusal branch (6 linear commits, only my own commits) onto the current develop `e072e142e` (proven ancestor); r5 content preserved byte-for-byte — `CollectableOrphans`, `target_definition_orphan_refusal_test.go`, `collectable_orphans_test.go`, `target_definition_change_plan.go` identical, `#174`/`#1505` overlap coexisting side-by-side in `deployment_list.go` and `deployment_store.go`. Readability-ratchet self-fix: moved `ErrTargetDetachedWithOrphans` to `deployment_orphan_refusal.go` (798 lines ≤ 800) so `PR · Source format` passes. Pushed `181f524b...f966505c` to PR #1500 head; hosted run **42598338207** on exact head `f966505c` terminal `completed/success` — every job green including both Native Keycloak/Core gates, `go-unit-tests`, `deployment-package-tests`, and `PR · Selected Checks`. No `.github/**` touched, no subagents, no containers. Evidence on planning `origin/main`.
