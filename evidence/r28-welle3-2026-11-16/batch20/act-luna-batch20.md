# CODEX-REVIEW — Luna batch20

Date: 2026-11-17. Role: CODEX-REVIEW (Luna). Read-only review; no merge.

## Candidate and exact-head witnesses

- PR #1665: `e580d32414565442376f23ace9a4a2dd7ed03838`, base `w083-perses-datasources`, OPEN, DRAFT.
- Prior reviewed head: `dda073da4a495f61d2f754ae37a0262225f68df8`.
- Exact-head `workflow_dispatch` run `43999100666`, completed on `e580d3241`.
- The `Run unit and package tests` step succeeded. Its log contains `ok github.com/mcpdev80/baseharbor/internal/metrics 0.249s`; the package step runs `go test ./...`, so the unchanged `TestPersesPrometheusDatasourceFailClosedWhenUnpinned` executes in this pass. The round-6 evidence also records its exact-head verbose local PASS.
- The workflow as a whole concluded FAILURE later at `Run runtime integration tests serially`. The log shows five ORAS setup failures plus `TestMultiInstanceComposeLifecycleInCI` failing its postgres `Config.User` check. Round-4 evidence documents the same runner-owned failure set on unrelated heads. This full-run failure is retained as a failure, not relabeled green; it is separate from the successful package step and the one-file candidate diff.

## Verdict — #1665 / 0428-082: APPROVE CONTENT, with window caveats

The exact diff from `dda073da4` to `e580d3241` changes only `internal/metrics/perses_prometheus_datasource.go` (+10/−3). `buildPersesPrometheusDatasourceWithProbe` now forwards the supplied `release` to `buildPersesPrometheusDatasourceAtWithRelease`, restoring fail-closed validation for an invalid/unpinned release. The Target-bound default helper explicitly supplies `capability.PersesDefaultRelease`, preserving the intended default pin for the dashboard face. This directly fixes the batch19 regression; no unrelated scope was added.

The 0428-080 `perses_selection` files/tests are not in this diff. Target-root changes from `dda073da4` remain unchanged and were separately tested in round 5. The current planning note for 0428-100 has `prs: []` and explicitly records the workload-only source-registration issue. Round 6 does not claim that issue is fixed or that a real Prometheus query already ran; it says the cell witness will be rerun after 0428-100 supplies a materialized source. That is a transparent dependency, not a hidden acceptance claim.

**Window caveats:** merge order remains behind the 0428-080 selection and 0428-083 datasource predecessors (PRs #1590 and #1608); both are still OPEN/DRAFT and target `lane-0428-075-perses-seam`. Do not merge #1665 ahead of those prerequisites. The live per-panel query qualification remains pending the 0428-100 source-registration fix and a successful rerun of the cell witness. This verdict approves the current content and pin-fix; it does not claim that the live-witness acceptance is complete.

## Turn-start coordination flags

`basics-check.py` reported: worker pool 2/3 with `ornith:2` held as `NO_ELIGIBLE_WORK` (candidate-count=0); idle lane 0428-082 awaiting END/inbox handling; missing GUI TODO file `workers/todos/0428-100-.json`; and 40 open PRs. These coordinator-owned flags are reported for follow-up; this review did not create worker work or alter TODO state.

## END

END_DONE mission-luna-batch20 — #1665 APPROVE CONTENT with the predecessor-order and 0428-100 live-witness caveats above. Exact-head package job passed; later runtime integration step failed on the documented ORAS/runner set. No GitHub approval, product change, or merge.
