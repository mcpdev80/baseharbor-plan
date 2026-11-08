# 0427-128 — round-1: bug reproduction (container_name replica)

**Task:** `t-20261108-bughunt-0427-container-name-replica` (card 0427-128)
**Owner:** lane-0427-128-contname
**Shift:** r27-welle5-folge-2026-11-08
**Model/session:** worker-ornith1.5-laptop, session `594fd2f5-4e80-43b6-9841-92879146a85e`

## PLAN

- Reproduce the bug on develop (`db06f01e9`; current remote HEAD `f9e207ac0`) with a minimal repro: a compose workload that uses an explicit `container_name` for a service and `replicas: 2`, and drive `StopOwnedProjectServices` (the backup quiesce path). Confirm the "selected stop has an unplanned service replica" failure.
- If confirmed: canonicalize the expected container name in the affected identity functions (`ContainerMatchesProjectResource`, `StopOwnedProjectServices`, service_retirement) from the effective Compose service config so both identity classes (`<project>-<service>-1` default and explicit `container_name`) match. Add error-text remedy on name collision.
- Add unit tests for both identity classes (positive selection for a relevant change, negative for an unrelated change); wire into the compose/backup CI group; run locally; observe CI run.
- Drift-merge, push PR (`0427-128` in title), CODEX review/merge, planning publish, evidence on origin/main.

## Base attestation

- Planning repo HEAD (origin/main): `a302e6165843b70c3aa16437ad3ce80da0cfa311` (`git ls-remote origin main`)
- Branch base: cut from `origin/develop` at `f9e207ac0d0b4c983fbb01d4357a8784c41c92de`
- `db06f01e9` (mission's develop ref) IS an ancestor of current remote develop `f9e207ac0`: `git merge-base --is-ancestor db06f01e9 origin/develop` → yes (owner merged #1446 after the mission was written).
- Branch: `bughunt/0427-128-container-name-replica` at `7717f4505`. Only my commits will be ancestors after this round.

## repo-rule compliance

- Scope: `baseharbor`, owned files `cmd/baha/app_workload.go`, `internal/runtime/service_stop.go`, `internal/runtime/container_identity.go`, plus `service_retirement.go:63` and `control_plane_stop_observation.go:49`. Not touching `#1430/#1443` write-set (access/target).
- No `.github/**` edits (Owner scope). No subagents (AGENTS 4.8). No runner infra. No products-repo evidence. No `git add -A` in worktrees.

## Reproduction result (round-1 verdict)

VERDICT: CONFIRMED. See detailed repro below.
