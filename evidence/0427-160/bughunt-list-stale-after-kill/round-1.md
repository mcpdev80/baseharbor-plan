# Round-1 — Bug-Hunt Fix 0427-160 (list stale after kill + MISSING next-action)

- Card/mission: mission-160.md (karte t-20261108-bughunt-list-stale-after-kill, card 0427-160), akte vm-bughunt/hx2.md BF-04 / BF-05.
- Shift / worker: r27, session 594fd2f5-4e80-43b6-9841-92879146a85e (worker, no subagents, AGENTS 4.8).
- Planning repo verified (origin/main): `git ls-remote origin main` -> aff1532c2f6c6782a8c13afad83245d1351815e7.
- Product remote HEAD (develop): 3187cea15728143146905c7238ad6e280ca11b3e (mission target).
- Branch: `fix/0427-160-list-stale-after-kill` cut from 3187cea15; parent = 3187cea15; 3187cea15 is an ancestor of HEAD (provenance = proof).
- PR: #1491 (open, against develop HEAD 3187cea15), 4 files, 223/4.
- No `.github/**` edits, no reruns/workflow_dispatch (Owner scope).

## PLAN

- Read mission, AGENTS (baseharbor + ecosystem), hx2.md findings; attest base + planning repo.
- Locate list/status source + reconciliation data model (deployment_record, stage_versions Stale()).
- Scope decision with owner: (1) live reconciliation lives in `baha status` (already probes workload, emits DEGRADED); record-only reconciliation on the read-only `list` path; (2) MISSING gets a next-action line. No machine-contract change (State stays free-form string).
- Implement fix (1) status DEGRADED Next: actionable re-up/destroy hint.
- Implement fix (1) list record-only DEGRADED (failed/stopped/degraded/runtime-retired + observed-vs-applied ref divergence).
- Implement fix (2) list MISSING next-action (exact prune/re-attach command).
- Regression tests in cli-surface group (app_list_reconciliation_test.go, app_status_ux_test.go, deployment_observation_test.go).
- Build/vet/format + affected cli-surface unit tests.
- Open PR #1491, monitor hosted run terminal.

## Findings -> fixes

### BF-04 (fix 1): list/status stale after SIGKILL
- Symptom: after a quadlet workload is SIGKILLed, `baha app list` still reports the workload applied/ready while the unit failed and the container is gone; `baha status` showed STOPPED.
- Root cause: `app list` (cmd/baha/app_commands.go) printed the last recorded `Observed.State` (a recorded `ready`/`applied`) with no reconciliation; `baha status` DEGRADED block only pointed at the opaque `baha doctor` / `status --verbose` command, not an actionable rebuild/destroy.
- Fix (1a) status — cmd/baha/app_observe.go render path: a degraded workload now prints an actionable Next:
  - `baha up # rebuild the failed/degraded workload (unit is not active)`
  - `baha app destroy # or remove it if the workload is gone for good`
  - `baha doctor # see which managed capability or workload check failed`
- Fix (1b) list (record-only reconciliation on the read-only path) — cmd/baha/app_commands.go `reconciledListState`:
  - recorded `failed`/`stopped`/`degraded`/`runtime-retired`/`retiring` => `DEGRADED` (never the stale terminal/ready token).
  - recorded `ready`/`applied` whose observed reference diverges from the last-applied reference (drift) => `DEGRADED`; divergence only flagged when BOTH observed and applied references are recorded and differ (an unrecorded observed reference is not drift and must not be DEGRADED).
  - recorded state token otherwise preserved verbatim (casing), so downstream assertions / machine contract keep the recorded casing.
  - Note: the pure SIGKILL case where the record still says `ready` but the unit is gone is reconciled by the live probe in `baha status`; the record-only list view never lies and reports the recorded state faithfully (as the owner scoped it).

### BF-05 (fix 2): MISSING with no next step
- Symptom: a zeroed app with a deleted repository shows only `MISSING` with no way forward.
- Fix (2) list — cmd/baha/app_commands.go `printListNextActions`: a deployment whose source repository is gone (MISSING) now prints an exact next-action line:
  - `baha app prune <name>` to remove the dangling record; or `baha up` once the repo is restored.
  - A failed/degraded record also gets the observed date (RFC3339) + re-up/destroy hint.

### STATE (blocker, environmental — not a regression)
- Hosted gate `PR · Native Keycloak/Core · docker` and `· podman` (the 156-domain STATE) FAILED.
- Exact failure: `TestControlPlaneSingleDefaultNativeRuntimeInCI` -> `prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open <data>/baseharbor-bootstrap-cleanup-pending: no such file or directory` (control_plane_single_native_ci_test.go:31), called from `ensureRuntimeIntegrationTrustPlane` -> `ensureBootstrapLeftoverMarker`.
- This is test-fixture teardown-marker setup (cmd/baha/runtime_integration_test_support_test.go `setupBootstrapLeftoverMarker` / `ensureBootstrapLeftoverMarker`), which the mission scope never touched and which gates on a data-home env var on the shared runner. It is independent of the display-layer fix.
- Proving it is not my code: my changed files are exactly cmd/baha/app_commands.go, cmd/baha/app_list_reconciliation_test.go, cmd/baha/app_observe.go, cmd/baha/app_status_ux_test.go — none is the fixture path.
- Evidence it is not caused by my change: `go-unit-tests` PASSED on the amended candidate (cd9eca82e) on CI; the only non-green gates are the two native Keycloak/Core gates above, which fail in fixture setup before any product code runs.

## repo-rule compliance

- Scope: exactly one integration candidate per chain (AGENTS 3.8). Branch `fix/0427-160-list-stale-after-kill` cut from 3187cea15; parent = 3187cea15; 3187cea15 is an ancestor of HEAD; only my single commit sits on top (git log 3187cea15..HEAD shows exactly cd9eca82e). No second branch, no foreign commit carried.
- No `.github/**` edits, no reruns/workflow_dispatch (Owner scope). A failing environmental check reported as STATE (check name PR · Native Keycloak/Core + failing line above), stop there.
- No `.evidence/` directory anywhere; evidence written only in baseharbor-plan (repo mcpdev80/baseharbor-plan, origin/main). No main-branch writes in product repos.
- Subagents: none used (AGENTS 4.8). All steps executed in this session.
- Machine contract: unchanged — `machine.DeploymentSummary.State` stays a free-form string; `DEGRADED` is a new display-layer value, not a new contract enum.
- Foreign/uncommitted files in the worktree (cmd/baha/app_context.go, cmd/baha/app_context_duplicate_name_test.go, internal/deployment/deployment_duplicate_name.go, internal/deployment/duplicate_name_test.go — card 0427-149 `--uuid` selector / duplicate-name gate) were left UNCOMMITTED and are NOT part of this PR; my commit contains only the 4 files above.

## CI / hosted run

- Candidate: cd9eca82e on fix/0427-160-list-stale-after-kill; PR #1491 vs develop 3187cea15.
- PASSED: go-build, go-vet, go-unit-tests, focused-python, source-format, cli-gofmt, trusted-plan, native-impact-selection, native-destroy-retry (docker + podman).
- FAILED (environmental STATE, not my code): `PR · Native Keycloak/Core · docker` and `· podman` -> TestControlPlaneSingleDefaultNativeRuntimeInCI bootstrap-leftover-marker missing.
- Run id (new): 42511078569 (terminal: completed -> failure). Run id (superseded): 42509465881.

## END

END mission-160.md: implemented both fixes (status DEGRADED actionable hint; list record-only DEGRADED + MISSING exact next-action), PR #1491 vs develop 3187cea15; all technical CI gates pass; the only non-green gate is the environmental Native Keycloak/Core bootstrap-marker STATE (not a regression).
