# Codex review 3 — t-20261121-all-targets-config-loss (0428-210)

ROLLE: REVIEW

Timestamp: 2026-11-21 11:19 UTC
Backend/model: Codex API, GPT-6

## PLAN

1. Record the numbered re-review plan in the live board and this evidence file.
2. Resolve the GitHub remote and verify current `develop`, PR #1739 head/base, ancestry, and head freeze.
3. Inspect the exact diff against measured `develop` and verify only authorized tolerance/test changes remain.
4. Verify authorization-before-tolerance, the anonymous denial regression, and selected-target strictness.
5. Verify exact-head `PR Selected Checks`, `PR Trusted Plan`, and all required CLI shards.
6. Record the verdict and merge order; publish only `review-3.md` and verify it on `origin/main`.

## Verdict

**APPROVE CONTENT — exact candidate `bb98e22599ab1f77edc056de73c682fdfdedd88a`.**

The exact diff from current `develop` changes only `cmd/baha/app_commands.go` and `cmd/baha/app_list_all_targets_test.go`. In `app_commands.go`, the authorization block is unchanged from the base: the all-targets route calls `authorizeMCPOperation(ctx, "app.list", "", "dev", "", "")`, the selected-target route calls `authorizeCurrentMCPContext`, and either authorization error returns before inventory work. The only `deployment.ErrConfigMissing` tolerance is below that gate, in the inventory result handling; no authorization check was removed or weakened by this candidate diff.

The new anonymous regression removes the config, invokes `--all-targets` without an operator context, rejects a nil error and `ErrConfigMissing`, requires the exact operator-auth gate text (case-insensitive comparison, including the final period), and requires no output. The installed-then-destroyed positive regression remains present. This addresses the previously raised authorization-bypass concern in the current-base diff.

## SHA and scope witnesses

Product remote first resolved in the product checkout: `origin git@github.com:mcpdev80/baseharbor.git` (fetch/push). Planning repository remote, verified before evidence publication: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push).

Fresh remote refs:

```text
77c1e60f51b91003ac3ddc391008c15e4a713a5c refs/heads/develop
bb98e22599ab1f77edc056de73c682fdfdedd88a refs/pull/1739/head
```

PR API witness: `state=open`, `draft=false`, `mergeable=true`, `mergeable_state=clean`, base `develop` at `77c1e60f51b91003ac3ddc391008c15e4a713a5c`, head branch `0428-210-alltargets` at `bb98e22599ab1f77edc056de73c682fdfdedd88a`.

GitHub compare witness for `77c1e60f51b91003ac3ddc391008c15e4a713a5c...bb98e22599ab1f77edc056de73c682fdfdedd88a`: `status=ahead`, `ahead_by=2`, `behind_by=0`, `merge_base=77c1e60f51b91003ac3ddc391008c15e4a713a5c`; changed paths are exactly:

```text
cmd/baha/app_commands.go
cmd/baha/app_list_all_targets_test.go
```

The two commits above base are `ba46249f007a` (post-auth `ErrConfigMissing` tolerance and anonymous regression) and `bb98e22599ab` (final hop retaining the develop authorization path). The exact compare patch shows ten added lines in `app_commands.go` after the selected/all-target inventory calls; it does not modify authorization. The test patch adds the anonymous no-config gate case.

## Required hosted checks

Run [44897396931](https://github.com/mcpdev80/baseharbor/actions/runs/44897396931) completed successfully on exact head `bb98e22599ab1f77edc056de73c682fdfdedd88a`, event `pull_request`, with base `77c1e60f51b91003ac3ddc391008c15e4a713a5c`. `PR Selected Checks` passed; `PR · Trusted Plan` passed; required Go unit coverage passed for `cli-0`, `cli-1`, `cli-2`, `cli-3`, `packages`, and `owner`. `Workflow policy`, `PR · Native gate plan`, `PR · Source format`, `PR · Focused Python`, `PR · Validation · go-build`, `go-vet`, and `cli-gofmt` also passed. The run had 15 successful jobs, 20 skipped jobs, and no failed jobs; skipped release/runtime/other non-selected jobs are not counted as passes.

This was a read-only review; no local product tests were run. The card's required Go unit shards were executed in the exact-head GitHub run above.

## Findings and merge instruction

No remaining findings in the reviewed diff. Merge PR #1739 first in this window: its base is `develop` and no stack depends on it. The verified final hop and successful exact-head required aggregate satisfy the prior review condition. No merge was performed in this REVIEW session; CODEX-MERGE owns that action.

## Repo-rule compliance

Read-only product review; no product files, workflows, or PR state were changed. Only this review evidence file is to be published. No stash was used. Evidence is in the actual planning repository, whose verified remote is recorded above.

Origin publication path witness, from `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep 'evidence/r28-welle4-2026-11-21/all-targets-config-loss/review-3.md'`:

```text
evidence/r28-welle4-2026-11-21/all-targets-config-loss/review-3.md
```

## cleanliness

Before review, PID 2131643 recorded `docker ps -a` at 2026-11-21 11:13:49 UTC; output contained only the table header and no containers. After review, PID 2161545 recorded `docker ps -a` at 2026-11-21 11:20:41 UTC; output contained only the table header and no containers. No containers or compose projects were started for this review.

END REVIEW DONE
