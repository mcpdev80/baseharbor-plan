# 0427-128 — round-1: bug reproduction (container_name replica)

**Task:** `t-20261108-bughunt-0427-container-name-replica` (card 0427-128)
**Owner:** lane-0427-128-contname
**Shift:** r27-welle5-folge-2026-11-08
**Model/session:** worker-ornith1.5-laptop, session `594fd2f5-4e80-43b6-9841-92879146a85e`

## PLAN

- Reproduce the bug on develop (`db06f01e9`; current remote HEAD `f9e207ac0`) with a minimal repro: a compose workload that uses an explicit `container_name` for a service and `replicas: 2`, and drive `StopOwnedProjectServices` (the backup quiesce path). Confirm the "selected stop has an unplanned service replica" failure.
- Decide the fix with the Owner (not a string heuristic): canonicalize the expected container name from the deployment plan (container_name / scale per service) so both identity classes match.
- If confirmed: canonicalize the expected container name in the affected identity functions (`ContainerMatchesProjectResource`, `StopOwnedProjectServices`, service_retirement) from the effective Compose service config so both identity classes (`<project>-<service>-1` default and explicit `container_name`) match. Add error-text remedy on name collision.
- Add unit tests for both identity classes (positive selection for a relevant change, negative for an unrelated change); wire into the compose/backup CI group; run locally; observe CI run.
- Drift-merge, push PR (`0427-128` in title), CODEX review/merge, planning publish, evidence on origin/main.

## Base attestation

- Planning repo HEAD (origin/main): `a302e6165843b70c3aa16437ad3ce80da0cfa311` (`git ls-remote origin main`)
- Branch base: cut from `origin/develop` at `f9e207ac0d0b4c983fbb01d4357a8784c41c92de`
- `db06f01e9` (mission's develop ref) IS an ancestor of current remote develop `f9e207ac0` (owner merged #1446 after the mission was written).
- Branch: `bughunt/0427-128-container-name-replica` at `7717f4505`. Only my commits will be ancestors after this round.

## repo-rule compliance

- Scope: `baseharbor`, owned files `cmd/baha/app_workload.go`, `internal/runtime/service_stop.go`, `internal/runtime/container_identity.go`, plus `service_retirement.go:63` and `control_plane_stop_observation.go:49`. Not touching `#1430/#1443` write-set (access/target).
- No `.github/**` edits (Owner scope). No subagents (AGENTS 4.8). No runner infra. No products-repo evidence. No `git add -A` in worktrees.

## Reproduction result (round-1 verdict)

VERDICT: CONFIRMED. Minimal repro in worktree `/tmp/opencode/0427-128-contname-wt`:

- Compose workload with an explicit `container_name` (`linkding-web`) for service `web`, project `linkding`. Quiesce path builds the canonical expected name `project+"-"+service+"-1" = "linkding-web-1"`.
- `ContainerMatchesProjectResource` (internal/runtime/container_identity.go) compares the actual container name (`linkding-web`) against `resource.Name` (`linkding-web-1`); they differ, so the match returns false.
- `StopOwnedProjectServices` (internal/runtime/service_stop.go:79-82) therefore returns the terminal error `selected stop has an unplanned service replica` — exactly the defect reported for `baha app backup`.
- Confirmed by running the repro against the unpatched code; error text matches.

## Root cause (decision-driven)

The canonical identity for a service is the default ordinal `<project>-<service>-1`. A workload that pins a `container_name` names its container outside that scheme, so the quiesce identity check rejects it. The fix must accept the pinned name as a valid identity — but per Owner directive 2026-11-08 this identity must be derived from the DEPLOYMENT PLAN (container_name / scale per service), NOT from a string heuristic on `container.Name` (pinned-base vs ordinal-replica is not string-decidable, and the existing test `container_identity_test.go` case 4 `owned-keycloak-db-0-2 → false` forbids a naive suffix heuristic).

## Blocker (QUESTION posted)

The plan schema carries only service NAMES, not container_name or scale, so the canonical target-name set is not derivable without a schema change:

- `internal/application/workload.go:26` — `WorkloadFiles.Services []string`
- `internal/application/manifest.go:49` — `Services []string`
- manifest `Services` list at `internal/application/manifest.go:42-50`

The three quiesce identity checks compare against a single computed ordinal:

- `internal/runtime/service_stop.go:79`
- `internal/runtime/service_retirement.go:63`
- `cmd/baha/control_plane_stop_observation.go:49`

POSTED QUESTION to Owner: derive canonical identity from plan; if the plan/manifest schema must gain per-service `container_name`/`scale`, that is a schema change the Owner must scope (file:line above). Waiting on Owner response before implementing.

## END status

END_BLOCKED mission-128.md: bug CONFIRMED (backup quiesce fails with "selected stop has an unplanned service replica" for explicit `container_name`); blocked on Owner scope decision whether the plan schema exposes per-service container_name/scale before identity can accept pinned names without string guessing. QUESTION posted.
