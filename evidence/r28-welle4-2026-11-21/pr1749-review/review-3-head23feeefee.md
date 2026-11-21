# CODEX-REVIEW — PR #1749, card 0428-222

## PLAN
1. Verify live PR #1749 head and its branch ref match mission SHA `23feeefee58`; stop if they differ.
2. Verify run 44953630114 is terminal success on that exact head and inspect required versus skipped jobs.
3. Verify ancestry and hop parity, distinguishing candidate-only changes from develop-side additions.
4. Recheck the task's previously approved content at the hopped head and confirm author/committer identity did not change.
5. Publish a hop verdict in this lane-owned Planning worktree; no product changes, comments, merges, closes, or local suite tests.

## Planning remote
`origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push). Raw `git remote -v` output:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```, previously verified before evidence commits in this worktree.

## Exact hop refs and ancestry

- Product remote: `https://github.com/mcpdev80/baseharbor.git`.
- Remote refs: `513488eeb6d788f0e5eec054be89807505f05e08 refs/heads/develop`, `23feeefee58c5438ccd37fe5c0edc674c5d0a79b refs/heads/lane-0428-222-child-env`, and `23feeefee58c5438ccd37fe5c0edc674c5d0a79b refs/pull/1749/head`.
- PR #1749 is OPEN, non-draft, base `develop`, mergeable, merge state CLEAN; exact head matches the mission.
- The exact hop commit `23feeefee58c5438ccd37fe5c0edc674c5d0a79b` has parents `78cd7d3c0788a181fbeb97fd9eebaccabc9f01e4` (prior candidate) and `513488eeb6d788f0e5eec054be89807505f05e08` (develop). This direct-parent witness establishes both requested ancestry relations without consulting the quarantined product checkout.
- GitHub compare API for `78cd7d3c0788a181fbeb97fd9eebaccabc9f01e4...23feeefee58c5438ccd37fe5c0edc674c5d0a79b` reports the exact same nine paths as `78cd7d3c0788a181fbeb97fd9eebaccabc9f01e4...513488eeb6d788f0e5eec054be89807505f05e08`: `cmd/baha/app_status_result.go` (+171/-12), `cmd/baha/app_status_result_seam_restored_0428_142_test.go` (+58), `cmd/baha/app_status_result_test.go` (+481), `cmd/baha/app_status_result_witness_boundary_0428_142_test.go` (+171), `cmd/baha/perses_lifecycle.go` (+27/-3), `internal/orgconfig/effective.go` (+122/-8), `internal/orgconfig/model.go` (+48), `internal/orgconfig/org_environment_reconcile_test.go` (+194), and `internal/orgconfig/orgconfig_test.go` (+27). This is the develop-side hop parity; no child-env patch content changed in the hop.
- The hop commit author and committer are both `0428-222-childenv`; the prior candidate head already has author identity `0428-222-childenv`. The merge hop introduces no new author identity.

## Exact-head hosted CI

- Run [44953630114](https://github.com/mcpdev80/baseharbor/actions/runs/44953630114), event `pull_request`, exact head `23feeefee58c5438ccd37fe5c0edc674c5d0a79b`, terminal `completed/success`: 36 jobs, 15 success, 21 skipped, 0 failures. Skipped jobs are not treated as passes.
- `PR Selected Checks` job `136998017721` completed success. Its per-job log fetched through `gh api repos/mcpdev80/baseharbor/actions/jobs/136998017721/logs` was 57,153 bytes.
- `PR · Go unit · packages` job `136996874656` completed success; its log includes `ok github.com/mcpdev80/baseharbor/internal/corebackup/etcd`, `ok github.com/mcpdev80/baseharbor/internal/coreupdate`, `ok github.com/mcpdev80/baseharbor/internal/stableid`, and `PASS all non-CLI Go package tests`. Its authenticated per-job log byte count was 33,517 via `gh api repos/mcpdev80/baseharbor/actions/jobs/136996874656/logs`.
- The test-to-gate path is the package Go unit job on the PR pull_request trigger. Current source names the inheritance tests `TestEtcdEnvInheritsParentEnv` (three etcd/etcdutl operations), `TestDCSBootProbeInheritsParentEnv`, and pin-precedence tests `TestPinnedEnvDropsInheritedKeys`, `TestChildProcessEnvShowsPinNotInherited`, `TestDCSBootProbePinsOverrideInherited`, and `TestProbeEnvDropsInheritedPATH`. The package job ran at the exact candidate.

## Content carry-forward and hop verdict

- The mission states that the previously approved content verdict at `78cd7d3c0788a181fbeb97fd9eebaccabc9f01e4` carries forward. The hop changes no child-env patch file relative to that head. Spot-check confirms the shared `internal/testsupport/envpin/pin.go:12-35` filters all pinned names out of the inherited environment and appends trusted pin values afterward; all five former K2 sites now call this helper. This prevents parent-provided PATH/API/TLS values from overriding pins while retaining unrelated environment variables.
- The candidate tests include sentinel inheritance and opposite-value pin assertions. The prior evidence `evidence/r28-welle4-2026-11-21/child-env-inheritance/round-1.md` records the original inheritance mutation turning `TestEtcdEnvInheritsParentEnv/snapshot-save` red. No local suite or mutation test was run in this review; the exact-hop package tests ran in hosted CI.
- Hop verdict: APPROVE HOP for exact head `23feeefee58c5438ccd37fe5c0edc674c5d0a79b`; the exact run is terminal green and parity/identity checks pass. This records no new content review or merge. No PR comment or close was made.

## Repo-rule compliance and cleanliness

- No product, `.github/**`, or `scripts/**` files changed; no local tests, workflow dispatch/rerun, PR comment, merge, or close. No subagents used.
- Planning remote was verified before evidence commits: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push).
- `docker ps -a` before review, shell PID 547571: eight pre-existing `bh-itest-*` containers, all exited; no containers or compose projects were started by this review.
- `docker ps -a` after review, shell PID 578947: same eight pre-existing `bh-itest-*` containers, all exited; no containers or compose projects were started. Evidence checkbox scan: clear.

## END

END_DONE codex-rev-1747: APPROVE HOP PR #1749 at `23feeefee58c5438ccd37fe5c0edc674c5d0a79b`; run 44953630114 success (36 jobs); Planning evidence publication recorded below; candidate remains `23feeefee58c5438ccd37fe5c0edc674c5d0a79b`.
## Live revalidation — revorder2 sequence

- Refreshed GitHub API and `git ls-remote https://github.com/mcpdev80/baseharbor.git` on 2026-11-21: PR #1749 remains OPEN, non-draft, based on `develop`, mergeable/CLEAN; branch and PR head remain `23feeefee58c5438ccd37fe5c0edc674c5d0a79b`. Current `develop` is `513488eeb6d788f0e5eec054be89807505f05e08`.
- Run 44953630114 remains terminal `completed/success`, `pull_request`, exact head `23feeefee58c5438ccd37fe5c0edc674c5d0a79b`: 36 jobs, 15 success, 21 skipped, 0 failures. `PR Selected Checks` job 136998017721, `PR · Go unit · packages` job 136996874656, and `PR · Go unit · cli-3` job 136996874598 completed successfully. Skipped jobs are not treated as passes.
- Live commit API confirms hop commit parent order `[78cd7d3c0788a181fbeb97fd9eebaccabc9f01e4, 513488eeb6d788f0e5eec054be89807505f05e08]`, author/committer `0428-222-childenv`; ancestry/parity/content carry-forward evidence above remains applicable.
- Verdict remains APPROVE HOP for the exact head. No merge, PR comment, or close was performed.


END_DONE codex-rev-1747: APPROVE HOP PR #1749; exact candidate 23feeefee58c5438ccd37fe5c0edc674c5d0a79b; run 44953630114 completed/success.
