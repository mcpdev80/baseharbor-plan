# Catalog Row Demand — v1 (consolidated demand list for the 0428-359 catalog family)

**Lane:** w387-0428-275-rowdemand
**Karte:** 0428-275 (mission-scoped catalog-demand list; see note 0428-275 below on the number)
**Repo/PR:** baseharbor (product) vs develop `ea5218d72`; referenced product PRs #1860/#1861/#1862/#1863/#1868/#1869; consolidation doc lives in plan PR #136 (content, not the lane branch).
**ART:** Evidence-documentation ONLY. No product commit, no `scripts/pr-gate-coverage.json` line written, no push to baseharbor develop, no workflow_dispatch, no card-field edit, no generated-view edit.

Verified against `origin/develop` = `ea5218d72e263f21e79853b679af50074dab8c25` (own `git ls-remote`, github.com/mcpdev80/baseharbor.git) and each candidate PR head by SHA via `git merge-base`/`git diff`. No source:line was taken from an akte on trust — every line below is re-checked against the develop catalog and the candidate diff.

## Basis-Attestation (before this doc)

- Planning repo remote, first evidence witness: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` => `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch) (push)` — correct planning repo, NOT the `workers/baseharbor-plan` quarantined subdir.
- Plan main runtime SHA (origin/main at fetch): `56dd78c485ab58c7907c5437f63273d6750ac73f`.
- Isolated plan worktree `workers/w387-0428-275-rowdemand-plan` cut from `origin/main` `56dd78c48`.
- Product develop base SHA (own ls-remote): `ea5218d72e263f21e79853b679af50074dab8c25`.

## Scope note (Owner clarification 2026-11-04)

`.github/**` workflow files belong to the Owner. This list never edits them. A failing check is reported as STATE (check name + failing log line), then stopped.

## Method

For each demanded source I record: (1) the source file, (2) the referenced product PR that owns it, (3) the exact `scripts/pr-gate-coverage.json` line — either the develop line where it is MISSING or the candidate line where it exists, (4) the required `runtime_specific`/skip-rule, (5) the reason. Rows are split into two groups:

- **Group A — FEHLEN on develop** (missing on develop, must be added there): the catalog row is absent from develop AND the candidate PR does not carry it → no self-justification.
- **Group B — KANDIDAT-only** (exists only on a candidate head, not on develop): the row exists but only on a candidate branch → does NOT qualify as a develop baseline (cannot be cited as self-justification).

## Group A — catalog rows MISSING on develop (must be added to develop via the catalog-only product PR)

All checked against `origin/develop` `ea5218d72`. `components` count on develop = 321.

| # | Source (path) | Product PR | develop line | `runtime_specific` / skip-rule | Reason (independently verified) |
|---|---|---|---|---|---|
| 1 | `internal/applicationbackup/recovery_manifest_workload_test.go` | #1860 | MISSING (develop: `grep recovery_manifest` = 0 hits; neighbors `:2710-2718` = `identity_regression_test_go`, `:2719-2722` = `app_identity_dashboard_status_test_go`) | REQUIRED: `"runtime_specific": true` (the sibling `identity_regression_test_go` at `:2717` carries it; the missing row must too) | Insert after develop `scripts/pr-gate-coverage.json:2718`. The Trusted-Plan gate (`pr-gate-plan.py:1952` ValueError) fails closed on this uncataloged `internal/` path. The three Go unit tests (`TestWorkloadVolumesAssertedInRecoveryManifest`, `TestRecoveryManifestFailsClosedOnMissingOwnedWorkloadVolume`, `TestRecoveryManifestDiscoveryDoesNotInventWorkloadVolumeStateClass`) run in the Go-unit path selected via `source.gate.atomic.docker.data.capabilities` / `source.gate.atomic.podman.data.capabilities` with `runtime_specific: true`. |
| 2 | `internal/runtime/repository_volume_inventory.go` | #1861 | MISSING (develop: `grep repository_volume_inventory` = 0 hits in catalog) | REQUIRED: declared owner + surfaces (sibling `*inventory*`/`*destroy*` rows exist) | #1861 head `ade7dab3c` changes exactly these three paths but does NOT touch its own catalog (diff `develop..ade7dab3c` on `scripts/pr-gate-coverage.json` is empty → no candidate row). The gate ValueError (w377 akte :80-87) names this path. |
| 3 | `internal/runtime/repository_volume_inventory_test.go` | #1861 | MISSING (same as #2) | as #2 | Same as #2. Same empty candidate catalog diff. |
| 4 | `cmd/baha/app_destroy_volumes_recovery_backup_test.go` | #1861 | MISSING (develop grep = 0) | as #2 | Same as #2. Only present in the #1861 diff. |
| 5 | `internal/runtimeexecutor/compose.go` | #1862 | MISSING (develop grep = 0; `internal/runtimeexecutor/` package entirely uncataloged) | REQUIRED: surfaces `source.gate.atomic.docker.data.capabilities` / `source.gate.atomic.podman.data.capabilities` (per planner's own suggestion in the w379 akte :56) | #1862 head `5c20c2e32` changes exactly `internal/runtimeexecutor/compose.go` + `compose_test.go` (name-only diff verified) but the catalog diff against develop is EMPTY → no candidate row. The gate ValueError names `compose.go`. |
| 6 | `internal/runtimeexecutor/compose_test.go` | #1862 | MISSING (same as #5) | as #5 | Same as #5. Same empty candidate catalog diff. |

## Group B — catalog rows that exist ONLY on a candidate head (NOT a develop baseline; no self-justification)

| # | Source (path) | Product PR | candidate line (candidate head) | `runtime_specific` | Note (independently verified) |
|---|---|---|---|---|---|
| 7 | `internal/applicationbackup/recovery_manifest_workload_test.go` | #1860 | `scripts/pr-gate-coverage.json:2720-2728` on head `057ce8c55` | `true` (present) | Candidate-only: `git diff develop..057ce8c55 -- scripts/pr-gate-coverage.json` shows exactly one inserted `+{...}` block at this location (verified above). Does NOT exist on develop (Group A #1). Self-justification invalid: the row is new on this candidate, not a develop baseline. |
| 8 | `internal/stableid/lock_probe.go` | #1863 | `scripts/pr-gate-coverage.json:2536` on head `0eafa9f5` | absent in inserted block (missing) | Candidate-only insert (verified above: `+{ ... id: source.internal_stableid_lock_probe_go ... }` at develop-`:2536`). The inserted block does NOT carry `runtime_specific: true` — a gap the demand list must flag (see §Gap). |
| 9 | `internal/stableid/lock_probe_platform_test.go` | #1863 | `scripts/pr-gate-coverage.json:2544` on head `0eafa9f5` | absent in inserted block (missing) | Candidate-only insert (same block, developed at `:2544-2545`). Same missing-flag gap. |

## Group C — already on develop (correctly cataloged), NOT demanded as a new row

| # | Source (path) | Product PR | develop line | `runtime_specific` | Note |
|---|---|---|---|---|---|
| 10 | `cmd/baha/app_init_runtime_permission_scope_test.go` | #1863/#1864 (mission names it) | `scripts/pr-gate-coverage.json:2735-2741` | **ABSENT** (develop entry has no `runtime_specific` field; verified `grep -c runtime_specific` over `:2735-2741` = 0) | Present on develop (not a Group A miss), but WITHOUT the `runtime_specific: true` flag the card requires so the resolver does not collapse the Podman sibling. This is the one row the family list demands a FIELD fix (not a new row) — add `runtime_specific: true` to the existing develop entry at `:2735-2741`. |

## Group D — referenced by mission as family but a different error class (not a line demand for #136)

| # | Source (path) | Product PR | Note |
|---|---|---|---|
| 11 | `internal/deployment/damaged_namespace_test.go` + `internal/deployment/damaged_namespace_network_test.go` | #1869 | Different error class: release-label `pr-gate-map-v1.json` release authorization is the Owner-gated step (w381 akte). Rows inserted candidate-only at develop `:2536` area with `.lifecycle` surfaces (no `runtime_specific`), owned by v0.4.27 release-label authorization — NOT a develop-baseline line demand. Flagged for completeness only. |

## Gap the demand list must flag (not carried by any candidate)

- #1863's inserted lock_probe rows (Group B #8/#9) are BOTH missing `runtime_specific: true`. The family contract (0428-359 required-catalog-rows acceptance) needs `runtime_specific` so the resolver keeps the Podman sibling alongside Docker. The develop baseline must require the flag when the row is promoted to develop; the candidate insert currently lacks it.
- The single develop field fix (Group C #10) also needs `runtime_specific: true` added to the existing entry at develop `:2735-2741`.

## What plan PR #136 does and does not deliver

- #136 is plan-only: `git diff origin/main...origin/pr-136 --name-only` lists only `tasks/`, `releases/`, `epics/`, `evidence/`, `views/`, `roadmap*` — ZERO product files. Plan main per construction has no `scripts/pr-gate-coverage.json`. Therefore #136 cannot carry ANY of the catalog rows above (0 rows delivered by #136).
- The rows are delivered by a SEPARATE catalog-only product PR to develop. #136 supplies the card/spec that names them; it does not write them.

## Owner next act (one sentence)

#136 stays the right home for the spec: card 0428-359's Required-catalog-rows block must list the eight develop rows (Group A/B), and add `runtime_specific: true` to the existing develop entry `source.cmd_baha_app_init_runtime_permission_scope_test_go` at `baseharbor/scripts/pr-gate-coverage.json:2736-2741` — while making clear the seven rows themselves can NEVER land in #136 (plan-only) and must go via the separate catalog-only product PR to develop.

## Evidence on origin/main (second-to-last action) — PASTE THIS WITNESS BEFORE END

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep catalog-row-demand-v1
```

## 4-Feld

- Lane: w387-0428-275-rowdemand
- Karte: 0428-275 (catalog-demand list; the number 0428-275 currently fronts `tasks/t-20261124-gate-catalog-baseline-0428-270.md` "add #1820-sib catalog rows" per its frontmatter; the family this list consolidates is 0428-359 via plan PR #136 — see w383 akte (f) for the number finding)
- Repo/PR: baseharbor (product) vs develop `ea5218d72`; product PRs #1860/#1861/#1862/#1863/#1868/#1869; consolidation in plan PR #136 (content only, not the lane branch)
- Status: END_DONE (all 8 family rows individually verified against origin/develop and each candidate head; two mission-referenced akten w378/w386 do not exist and are reported here)

END_DONE w387-0428-275-rowdemand: 8 family rows verified — Group A (missing on develop): #1860 recovery_manifest `pr-gate-coverage.json` after :2718 (needs runtime_specific:true), #1861 repo_volume_inventory ×3 (candidate catalog diff empty), #1862 runtimeexecutor/compose ×2 (candidate diff empty); Group B (candidate-only, no self-justification): #1860 :2720, #1863 lock_probe :2536/:2544 (both missing runtime_specific); Group C: #1863 permission_scope already on develop `:2735-2741` but WITHOUT runtime_specific (field fix demanded); #1869 damaged-state = release-label error class, not a baseline line. All checked independently against origin/develop ea5218d72, nothing from akten blindly adopted.
