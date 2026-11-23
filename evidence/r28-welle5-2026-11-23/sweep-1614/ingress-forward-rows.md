# PR-SWEEP #1614 ENTBLOCKER — ingress catalog rows (QUESTION posted, awaiting answer)

Lane: w076-0428-076-1789rest (sitz 9b7683b5), mission /tmp/opencode/m_9b7_1614ing.md.g.
Develop-only ingress PR per pattern #1792/#1794; worktree
`/home/marcel/dev/baseharbor-ecosystem/workers/sweep-1614-ingress-wt`, branch
`lane-0428-ingress-1614-catalog` cut fresh from fcccf7a2. Nothing pushed yet.

## PLAN

1. Resolve remotes; attest develop tip via ls-remote + rev-parse; extract TP failure path list from run 45121263807 log as row source.
2. Verify each named path exists on develop; check catalog schema/precedent.
3. Decision point: scope impossible literally (5 of 12 rows name non-develop files) -> QUESTION posted, no silent choice.
4. On answer: add rows (additive only), JSON + validator checks, push + PR + ls-remote witness + ready.
5. Watch exact PR run to terminal (TP + selected green); END with PR number + head + run-id + gates.

## Remote resolution (REMOTE GUARD)

`git remote -v` in the ingress worktree (first git action):

```
origin	https://github.com/mcpdev80/baseharbor.git (fetch)
origin	https://github.com/mcpdev80/baseharbor.git (push)
```

## BASE ATTESTATION

`git ls-remote origin refs/heads/develop` and `git fetch origin develop; git rev-parse origin/develop` (both agree):

```
fcccf7a2059fa862f921ed58fda3f8248932c60d	refs/heads/develop
```

Branch cut point (mission says rev-parse belegen): worktree HEAD = fcccf7a2 after
`git worktree add ... -b lane-0428-ingress-1614-catalog fcccf7a2`; fcccf7a2 == first commit parent trivially (no commit made yet).

## TP log extraction (row source, run 45121263807 PR · Trusted Plan)

The `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change...` line names
exactly these 12 paths (deduplicated from the job log; extract saved at /tmp/opencode/tplog.txt):

| # | Path | Planner-suggested id | Exists on develop (fcccf7a2)? |
| --- | --- | --- | --- |
| 1 | cmd/baha/app_observe.go | source.cmd_baha_app_observe_go | YES |
| 2 | cmd/baha/app_status_versions_test.go | source.cmd_baha_app_status_versions_test_go | NO (PR-new) |
| 3 | cmd/baha/app_tls.go | source.cmd_baha_app_tls_go | YES |
| 4 | cmd/baha/app_version_unified_test.go | source.cmd_baha_app_version_unified_test_go | NO (PR-new) |
| 5 | cmd/baha/app_version_view.go | source.cmd_baha_app_version_view_go | YES |
| 6 | cmd/baha/app_versions_backend_test.go | source.cmd_baha_app_versions_backend_test_go | NO (PR-new) |
| 7 | cmd/baha/app_versions_command.go | source.cmd_baha_app_versions_command_go | YES |
| 8 | cmd/baha/app_versions_view.go | source.cmd_baha_app_versions_view_go | NO (PR-new) |
| 9 | cmd/baha/app_versions_view_parity_test.go | source.cmd_baha_app_versions_view_parity_test_go | NO (PR-new) |
| 10 | cmd/baha/app_workspace_source_model.go | source.cmd_baha_app_workspace_source_model_go | YES |
| 11 | cmd/baha/management_core_git_candidate_test.go | source.cmd_baha_management_core_git_candidate_test_go | YES |
| 12 | internal/machinereadmodels/release.go | source.internal_machinereadmodels_release_go | YES |

All 12 confirmed UNCOVERED in the develop catalog (234 component rows vs 2524 cmd/internal go
files; the catalog covers hot paths only, so uncovered-but-existing files are the norm and no
path-existence precedent could be relied on either way).

## Blocker + QUESTION (step 3)

Mission scope says rows "genau die rows fuer die im TP-log GENANNTEN pfade" — but 5 of the 12
paths exist only on the #1614 branch. A 7-row-only ingress PR would still fail TP for the other 5
once #1614's diff lands them. Options put to coordinator (post sent): (a) all 12 rows incl.
forward-rows for PR-new files; (b) only 7 develop-existing rows, #1614 carries its 5 as
candidate-added; (c) other intended row-source. Awaiting answer; nothing pushed, no PR yet.

## cleanliness

- No containers, compose projects, networks, volumes or VM work started; no files pushed.
- `docker ps -a` on this host (pid 3995264): zero containers; ambient untouched.
- Worktree lives in workers/ (allowed zone); extracts under /tmp/opencode only.

## Evidence-on-origin/main verification (second-to-last actions)

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep sweep-1614/ingress-forward-rows
 * branch                main       -> FETCH_HEAD
evidence/r28-welle5-2026-11-23/sweep-1614/ingress-forward-rows.md
```

Planning repo remote verified before first evidence commit:
`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` →
`origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

QUESTION w076-0428-076-1789rest: #1614 ingress row-scope decision needed (a/b/c above); candidate SHA none yet, branch lane-0428-ingress-1614-catalog prepared at fcccf7a2 (base attested).
