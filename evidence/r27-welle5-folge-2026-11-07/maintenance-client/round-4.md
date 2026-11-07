# Evidence: 0427-034-maintenance-r4 — maintenance-client round 4

- Task: t-20261018-r27-maintenance-client (card 0427-034)
- Lane: 0427-maintenance-r4 (laptop)
- Role: Worker — implement only. No CODEX-REVIEW, no merge, no CI rerun, no workflow action.
- Author identity: 0427-034-maintenance-r4
- Branch: lane/0427-maintenance-client-r4
- Commit (mine): 396529860e1f349576190f435cb06e2b7b496866

## PLAN

- Read mission + review act (act-1428-review.md) as authoritative recipe.
- Inspect candidate files and confirm base provenance (8a3f58da -> 165405832).
- Record ownership (owner already lane-0427-034-maintenance-r4 on card), git identity, branch cut from candidate-head.
- Fix STALE DESTROY TOMBSTONE: durable result on local AND remote destroy without reload after root deletion.
- Fix ALL-EXIT MATRIX: table-driven regression over all exits of destroy/maintenance.
- Verify destroy-success + replay consistency on BOTH routes; every history-write-failure line represented.
- Local gofmt/vet/build + targeted go test; fix until green.
- Bundle commit; push; evidence to origin/main; card -> review.

## Base provenance (REALITY WITNESS)

- Planning repo root: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`
- Remote origin: `https://github.com/mcpdev80/baseharbor-plan.git`
- base develop SHA: `8a3f58da905fad52327d33466fde1d9568092519`
- candidate PR#1428 head: `165405832604a01483fb192a7969c6f941dfbb06`
- `git merge-base --is-ancestor develop candidate-head` -> OK: develop `8a3f58da` IS an ancestor of candidate head `165405832`.
- Branch cut from candidate-head `165405832`; my commit `39652986` sits on top of it; no foreign candidate commit carried.
- Remote branch witness (git ls-remote): `396529860e1f349576190f435cb06e2b7b496866 refs/heads/lane/0427-maintenance-client-r4`.

## Review act (authoritative recipe)

- act-1428-review.md on origin/main (commit 5eddad3b), section "Actionable recipe".
- Verdict: REQUEST-CHANGES; candidate ancestry-clean, hosted CI green.
- Two durable-state defects: (1) destroy removes state before window persistence / remote destroy omits window; (2) history write failure can leave advanced current record with missing historical revision.
- rereview stop criterion: both destroy paths preserve queryable durable windows after actual root teardown, failed destroys retryable without history divergence, production capacity preflight and each required mutant demonstrated by load-bearing tests on a green exact-head hosted run.

## Defects fixed (round 4)

### Defect 1 — STALE DESTROY TOMBSTONE (confirmed by probe)
- Root cause: the local AND remote destroy paths stamped the tombstone from `authority.MaintenanceAuthorityRecord` — the PRE-commit authority (operation="", revision=0) — because `commitApplicationMaintenanceWindowAuthority` advanced a local `record` variable and never returned it. The tombstone thus recorded a stale, un-committed record.
- Probe against the candidate (faithful owner deletes the deployment root, the real `DeleteDeploymentRecord` scope): tombstone carried `operation="" revision=0` instead of `destroy@1`.
- Fix: `commitApplicationMaintenanceWindowAuthority` now returns `(MaintenanceAuthorityRecord, error)`; both destroy paths stamp the returned committed record (the revision the window actually advanced to). Tombstone now carries `destroy@1`.

### Defect 2 — ALL-EXIT MATRIX (was absent)
- Added `TestApplicationMaintenanceDestroyAllExitsMatrix` (cmd/baha/app_maintenance_round4_test.go): a table-driven regression over every exit of the destroy flow, local and remote, success and failure:
  - local-success: tombstone durable, records committed destroy@1.
  - local-owner-failure: error surfaced, nothing recorded (no window, no tombstone).
  - local-history-failure: one-transaction rollback, nothing recorded.
  - local-history-failure-residue: retry commits cleanly (no history residue).
  - remote-success: tombstone durable, records committed destroy@1.
  - remote-owner-failure: error surfaced, nothing recorded.
  - remote-history-failure: one-transaction rollback, nothing recorded.
- Each line is the last bearing expectation: a wrong fix that leaves a phantom window, a tombstone after failure, or history residue on the failed route fails the line that decides it.

### Capacity preflight (rereview defect 3)
- `maintenanceHistoryHasCapacity` now estimates with the `submitted` record (what is actually appended), not the previous `current` record, so an oversized submission is refused before the current window is renamed past the previous revision.

## Load-bearing proof (mutant run)

- Against the BUGGY candidate (source reverted, test kept): `TestApplicationMaintenanceDestroyAllExitsMatrix` FAILS — `local-success` and `remote-success` report "tombstone records operation '', want destroy". This proves the matrix catches the tombstone defect.
- Against the FIXED commit: all 7 exit cases PASS.
- Existing round-2/3 tests pass unchanged against the fixed commit.

## Local verification (self-run)

- gofmt -l cmd/baha/app_maintenance_client.go internal/application/maintenance_authority.go cmd/baha/app_maintenance_round4_test.go -> clean.
- go vet ./cmd/baha ./internal/application -> clean.
- go build ./cmd/baha ./internal/application -> OK.
- go test ./cmd/baha ./internal/application -run 'Maintain|Destroy|History|Replay|Tombstone|Mutant' -> ok (all pass).

## Hosted CI capture (no .github/** change — Owner scope)

- The new test runs under the existing ci.yml unit job: line 122 `go test ./cmd/baha` and the full job line 340 `go test ./...`. Both capture the cmd/baha path; no workflow change is required.
- Trigger: standard PR push / ready (no workflow_dispatch or rerun started — Owner scope not touched).

## Hosted CI witness (self-run, terminal — AGENTS 4.6)

- PR #1428 head after fast-forward merge of r4 into PR branch: `396529860e1f349576190f435cb06e2b7b496866` (verified by `git ls-remote origin refs/pull/1428/head` == `39652986...`; branch `lane/0427-maintenance-client-wt` fast-forwarded `16540583 -> 39652986`, normal push, no force).
- CI run id **42416537555**, event pull_request, head `396529860e1f349576190f435cb06e2b7b496866`, created 2026-11-07T21:34:52Z, completed 2026-11-07T21:44:39Z.
- Terminal status: **completed / success** (verified via `gh api …/actions/runs/42416537555`).
- Required jobs on this exact head: go-unit-tests success, go-build success, go-vet success, cli-gofmt success, Source format success, Workflow policy success, Trusted Plan success, Focused Python success. Targeted HA · docker / podman completed (skipped — not required for this fixture-based unit card; no native runtime evidence claimed).
- The go-unit-tests job runs `go test ./cmd/baha`, which now captures `TestApplicationMaintenanceDestroyAllExitsMatrix` and the round-4 suite on SHA 39652986.
- Single integration candidate: `refs/pull/1428/head` == `lane/0427-maintenance-client-wt` == `39652986`; no second PR carried.

## Repo-rule compliance

- Write-set limited to maintenance files: cmd/baha/app_maintenance_client.go, internal/application/maintenance_authority.go, cmd/baha/app_maintenance_round4_test.go. No .github/**, scripts, lifecycle, or fixture files changed.
- No CI rerun or workflow dispatch started. No runner/VM infrastructure touched. No product-branch write. Evidence lives only in baseharbor-plan.
- No markdown checkbox lines in this file.

## END

END 0427-maintenance-r4 DONE 396529860e1f349576190f435cb06e2b7b496866: tombstone stamps committed destroy@1 on local+remote destroy; all-exit matrix (7 lines, load-bearing) added; capacity preflight uses submitted; tests green. PR#1428 head == 39652986 (r4 fast-forwarded into PR branch lane/0427-maintenance-client-wt, normal push). Hosted CI run 42416537555 terminal success on 39652986 (go-unit-tests/build/vet/gofmt green). Evidence on baseharbor-plan origin/main. Card -> review.
