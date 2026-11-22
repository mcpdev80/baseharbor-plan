# PR #1753 exact-head review preparation

## PLAN

1. Verify product and Planning remotes, then refresh live PR #1753 head and current develop refs from the real GitHub remote.
2. Proceed with candidate review only if the live PR head is an ancestor of current develop and `git rev-list --count <head>..develop` is zero; otherwise keep the prior candidate on hold.
3. For a current head, inspect the exact diff for canonical `app footprint show -o json` admission and fail-closed behavior, then verify positive and negative test lines.
4. Verify the exact hosted run and executed data-capabilities job for that full head SHA; issue a verdict only with terminal evidence.
5. Write the exact-head evidence at the requested `review-1753-head<sha>.md` path, publish it to Planning origin/main, update the board, and post END; do not merge or close.

## Status

Awaiting live-ref check. No verdict issued.

## Live hold state

Verified product remote: `origin https://github.com/mcpdev80/baseharbor.git` (fetch and push). Fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1753/head refs/heads/develop` returned:

```text
6209874428f08dc3e90d6e29a42b30683ce9932a refs/heads/develop
03ef125e610f3a3db60042b70784d8e463f11500 refs/pull/1753/head
```

`gh pr view 1753 --repo mcpdev80/baseharbor --json number,state,isDraft,baseRefName,headRefName,headRefOid,mergeStateStatus` reported open, non-draft, base `develop`, head `03ef125e610f3a3db60042b70784d8e463f11500`, and `mergeStateStatus=BEHIND`. This is not the post-hop exact candidate. No code or test inspection, verdict, CI action, merge, or close was performed. Resume only when a fresh live head is current with develop (back=0), then inspect the canonical admission, fail-closed behavior, positive/negative regression, and terminal data-capabilities job for that exact SHA.

## Planning remote witness

Verified before committing evidence:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## cleanliness

Shell PID `1317826`: `docker ps -a` before and after showed the same eight pre-existing exited containers (IDs `268b7d8b4612`, `34cf9576dc2b`, `e88b00795b5c`, `1451a7b5b3c6`, `d7ba821c0e08`, `957a80e73b57`, `45bddf32278e`, `9d3f1a2b1e0e`). No container or compose project was started or changed.

END_BLOCKED codex-rev-1747: #1753 remains on hold pending a current exact head and executed data-capabilities qualification; no verdict.

## Final origin/main path witness

After `git -C baseharbor-plan fetch origin main`, `git -C baseharbor-plan ls-tree -r --name-only origin/main | grep 'evidence/r28-welle5-2026-11-22/footprint-gate-admission/review-1753-pending.md'` returned exactly:

`evidence/r28-welle5-2026-11-22/footprint-gate-admission/review-1753-pending.md`


## PLAN — qualification hold update

1. Preserve the existing #1753 hold; do not review or verdict the stale candidate.
2. Record the owner-reported Targeted Atomic Gate startup failure and distinguish zero executed jobs from a failing test.
3. Verify the cited develop routing locations and add precise file:line findings for the missing data-capabilities selection.
4. Wait for the post-hop exact head and run; inspect the trusted plan for an actually executed data-capabilities job before deciding acceptance.
5. Publish this evidence update to Planning origin/main, update the board, and post END without merge or close.


## Updated owner finding and qualification hold

Fresh product remote witnesses confirm develop `6209874428f08dc3e90d6e29a42b30683ce9932a` and PR #1753 head `03ef125e610f3a3db60042b70784d8e463f11500`; `git rev-list --count <head>..<develop>` is `3`. The PR is still behind develop. The owner has ordered a hop on current develop; no post-hop head or run has been supplied yet.

The owner-issued Targeted Atomic Gate run `44966919945` was independently queried with `gh run view`. It is `workflow_dispatch`, head `6209874428f08dc3e90d6e29a42b30683ce9932a`, workflow `Targeted Atomic Gate`, status `completed`, conclusion `startup_failure`, and has an empty `jobs` array. Its requested target was Docker `data-capabilities` with demo pin `5d1cf312e18d`. This is a gate startup failure with zero executed jobs, not a test failure and not evidence that the gate ran. The owner-reported PR run `44966211481` is green, but it does not qualify this gate.

The current develop source confirms the boundary behavior and routing gap:

- `cmd/baha/ci_integration_operator_enabled.go:135` admits guided footprint show only when `gate == "guided"`. The exact command predicate at `:232-233` requires `app footprint show -o json`. Other commands remain fail-closed at `:180` with `command-not-in-managed-workload-set`.
- `scripts/pr-gate-plan.py:172-175` maps `cmd/baha/app_edit.go` and `cmd/baha/app_edit_test.go` to Docker and Podman `data-capabilities`; it has no entry for `cmd/baha/ci_integration_operator_enabled.go`.
- `scripts/pre-release-runtime-impact.json:30-31` maps only `cmd/baha/app_machine_adapters.go` and its test to Docker and Podman `data-capabilities`; it has no entry for the operator-boundary file.

Acceptance remains on hold. When the post-hop candidate arrives, verify its exact diff and positive/negative tests, then inspect the trusted plan and exact run for a data-capabilities job that is actually executed, not skipped. If that required gate is absent, the verdict must be REQUEST CHANGES for missing qualification, not for the behavior itself. No verdict, merge, close, CI rerun, or workflow dispatch was performed here.

## cleanliness — qualification update

Shell PID `1327076`: `docker ps -a` before and after showed the same eight pre-existing exited containers (IDs `268b7d8b4612`, `34cf9576dc2b`, `e88b00795b5c`, `1451a7b5b3c6`, `d7ba821c0e08`, `957a80e73b57`, `45bddf32278e`, `9d3f1a2b1e0e`). No container or compose project was started or changed.

END_BLOCKED codex-rev-1747: #1753 remains held at stale head 03ef125e610f3a3db60042b70784d8e463f11500; owner gate run 44966919945 ended startup_failure with zero jobs; await hopped head and executed data-capabilities evidence.

## Final origin/main path witness after qualification update

After `git -C baseharbor-plan fetch origin main`, `git -C baseharbor-plan ls-tree -r --name-only origin/main | grep 'evidence/r28-welle5-2026-11-22/footprint-gate-admission/review-1753-pending.md'` returned exactly:

`evidence/r28-welle5-2026-11-22/footprint-gate-admission/review-1753-pending.md`
