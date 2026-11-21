# CODEX-REVIEW evidence: PR #1702, backend-witness boundary

## PLAN

1. Confirm the preceding #1736 review ended and its evidence was published.
2. Recheck the remote #1702 head and the assigned hosted run; stop this candidate if the head differs.
3. Review InfrastructureDashboards production output, witness semantics, restored test seams, and commit identity.
4. Check the named negative test's source and CLI-shard coverage, and inspect the exact hosted job logs for case receipts.
5. Record an exact-head verdict with actionable correction recipes and no product changes.
6. Render/check and publish this evidence to Planning origin/main, then verify the remote path.

## Preceding review

PR #1736 review ended with REQUEST CHANGES at head `10150ee7164bbc8767136e540eb966c3baab930b`. Its exact evidence is published at `evidence/r28-welle4-2026-11-21/pr1736-review/review-1-head10150ee.md`, remote Planning head at that verification `b6217d39b0ba4da01ce2f0f1bc08d3f5e79fcf7a`.

## Candidate, ancestry, and identity

Remote witness from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1702/head refs/heads/develop`:

```text
d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3 refs/heads/develop
e0613d9950a8caf3805c60c29b563ba8273230c5 refs/pull/1702/head
```

PR #1702 is OPEN, non-draft, base develop at `d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3`, and has four commits. The fetched `origin/develop` is an ancestor of `HEAD`; `git diff origin/develop...HEAD --name-only` produced:

```text
cmd/baha/app_status_result.go
cmd/baha/app_status_result_seam_restored_0428_142_test.go
cmd/baha/app_status_result_test.go
cmd/baha/app_status_result_witness_boundary_0428_142_test.go
cmd/baha/perses_lifecycle.go
```

`git log --oneline origin/develop..HEAD` lists only the four candidate commits:

```text
e0613d9950 fix(0428-142): keep InfrastructureDashboards producer alongside PersesBackendWitness
dfec73f65 chore(0428-142 r9 seam): wire perses witness tests onto new-develop runWithIOAsTestOperator seam (PR #1704)
a34861ce5 chore(0428-142 r9 seam): restore persesRunWithIO/persesTestCorelessTarget shims for new-develop transport seam
a17a00d5b fix(0428-142 r9): enforce negative backend-witness boundary + hop to fresh develop
```

`git log --format='%an %cn' origin/develop..HEAD | sort -u`:

```text
0428-142-genuine 0428-222-hop220
0428-142-statuswitness 0428-222-hop220
```

Thus the two author identities are `0428-142-genuine` and `0428-142-statuswitness`; all four commits use committer `0428-222-hop220`.

Product worktree remotes resolved to official GitHub URLs: `origin https://github.com/mcpdev80/baseharbor.git (fetch)` and `lane-origin https://github.com/mcpdev80/baseharbor.git (fetch)`. The exact worktree `HEAD` was `e0613d9950a8caf3805c60c29b563ba8273230c5` and had no local modifications.

## Production witness and dashboard inventory

`PersesInfraDashboardAvailability` returns no inventory when the Perses UI is not selected; when selected it calls `VerifyPersesInfraDashboard` and returns one entry per panel. Verification errors mark every panel unavailable with a reason; missing series mark only their own panel unavailable rather than reporting a silent zero (`internal/metrics/perses_infra_dashboards.go:203-231`). In `collectApplicationStatusResult`, the producer result is computed once and included in both remote-target and local result paths (`cmd/baha/app_status_result.go:303-314, 403-418`). This restores the four-panel inventory map alongside the separate backend witness.

The witness has three states: `not-configured` when a manifest source is absent, `configured` only when its own signal and provenance are proven, and `unreachable` when declared but its own backend answer is absent. Prometheus requires both `ObservabilitySupported` and `witness.PrometheusProven`; Loki and Tempo require their own proof bits (`app_status_result.go:86-165`). Production currently passes an empty `PersesBackendSignalWitness{}` to the helper in both output paths (`:313, :417`), so no production path claims a positive configured backend from the static catalog alone. A positive real backend answer remains the separately owned 0428-143 work. The human `perses status` and machine `app status` faces use the same helper (`perses_lifecycle.go:85-94, 221-236`).

The restored helpers are defined only in `app_status_result_seam_restored_0428_142_test.go`; they delegate to the existing develop test seams `configureTestTargetEmpty` and `runWithIOAsTestOperator` (`:37-58`). The production code does not use these test-only bridges. No production authority or transport path was added by the seam restoration.

## Negative test and hosted CI receipt

The negative boundary test exists at `cmd/baha/app_status_result_witness_boundary_0428_142_test.go:92-123`. The CLI shard selector assigns `TestPersesStatusWitnessRemovingSourceWitnessMakesUnreachableRed` to `cli-1` using its deterministic name hash; the other new boundary tests map to `cli-0` and `cli-2`. Run `44941446100` reports `PR · Go unit · cli-1` job `136959378019` successful with `440 passed / 10 intentionally skipped / 450 discovered; CLI inventory total=1837`. The companion shard jobs also passed: cli-0 `458 / 13 / 471`, cli-2 `455 / 20 / 475`, cli-3 `425 / 16 / 441`, each reporting inventory total 1837. No local suite tests were run.

The hosted logs expose only these per-shard aggregates; they do not expose the named test's individual execution result or duration. Therefore the requested per-case log receipt is not present. This is an `open item, owner-scope receipt-tooling` because `scripts/pr-go-unit-shard.py:60-82` selects and validates tests but only prints aggregate counts. The job log contains no `no tests to run` line; that absence does not substitute for per-case receipt.

There is also a test assertion defect: `TestPersesStatusWitnessEmptyResolvedSignalNeverResolvedProves` only logs if Prometheus is incorrectly `configured`, and passes when the Prometheus result is missing (`app_status_result_witness_boundary_0428_142_test.go:142-161`). Its stated boundary is therefore not protected against regression. Separately, `TestPersesStatusWitnessRemovingSourceWitnessMakesUnreachableRed` asserts that some unreachable verdict exists, but the comment says a mutation runs in a child when no child/mutation is present (`:114-122`). The test catches a wholly empty witness but does not prove the specific Prometheus result is present or enforce the claimed mutation scenario.

## Hosted run

Run `44941446100` is a `pull_request` run on exact head `e0613d9950a8caf3805c60c29b563ba8273230c5`, terminal `completed/success`. `PR Selected Checks` job `136960483510` succeeded. The run had 36 jobs: 15 successful, 21 skipped, 0 failed, 0 still running. Skipped jobs are not counted as passes. The trusted plan is exact-head, `coverage_status=resolved`, `broad_required=false`, base and merge-base `d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3`; its `pr-plan.json` SHA-256 (plan-sha) is `6eff61d9edf2d4442960d40973bf7662a5b031c9080989284af002e32587c18f`.

## Verdict and correction recipes

REQUEST CHANGES. The production result restores the infrastructure-dashboard inventory, the backend witness does not invent verified health, the test seams remain test-only, and the exact-head required run is green. However, the test `TestPersesStatusWitnessEmptyResolvedSignalNeverResolvedProves` can pass when the required Prometheus witness is absent or incorrectly configured; the named negative test also lacks its requested individual hosted receipt and its mutation comment overstates what it executes.

Recipe for the in-scope test: in `cmd/baha/app_status_result_witness_boundary_0428_142_test.go`, require that the Prometheus verdict is present and exactly `unreachable` for a supported signal with empty provenance, using `t.Fatalf` for both absence and `configured`; make the source-wiring test either directly assert the required backend/source mapping or accurately name/document its current assertion. Add a regression assertion that fails when the production result omits the Prometheus witness. Stop if the regression test passes with a missing or `configured` Prometheus entry.

Receipt recipe: the owner-scope runner output in `scripts/pr-go-unit-shard.py` must expose the named negative case and duration in its per-job log; rerun the exact CLI shard and stop if the case is absent, skipped, or not green. No changes were made by this reviewer.

## Cleanliness

`docker ps -a --no-trunc` before, shell pid 3264548: eight existing `bh-itest-*` containers, all exited. After, shell pid 3272078: the same eight container IDs and statuses, all exited. This review started no containers or compose projects.

## Planning remote

Output of `git -C /home/marcel/dev/baseharbor-ecosystem/workers/codex-rev-1747-plan-wt remote -v | head -n 1` before this evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

END codex-rev-1747 DONE — REQUEST CHANGES; head `e0613d9950a8caf3805c60c29b563ba8273230c5`; run `44941446100`; 36 jobs, 15 successful, 21 skipped, 0 failed; plan-sha `6eff61d9edf2d4442960d40973bf7662a5b031c9080989284af002e32587c18f`; identity: autoren=[0428-142-genuine, 0428-142-statuswitness].
