# podman-doctor — Evidence (native Podman-core run: baha doctor → READY on podman+Quadlet)

Mission `coordinator/missions/podman-doctor.txt` (lane `podman-doctor`, Worker: Ornith):
- Worktree `workers/worktrees/podman-doctor`, repo baseharbor, base `origin/develop` = aef6b0e1.
- Task: native **Podman core run** from GH-hosted sweep (ref `runtime-validation/podman/gh-hosted-sweep`, head `1d74a910`).
  Runner log: `Podman runner` Step success, but step **"Runtime detection: Doctor detects Podman and Quadlet and reports READY"** = FAILURE.
- Ziel: `baha doctor` (cmd/baha) erkennt Podman+Quadlet auf GH-hosted ubuntu-26 correctly and returns READY.

## PLAN (plain bullets)
- Step 0: worktree clean at aef6b0e1; branch `work/podman-doctor` + `workers/todos/podman-doctor.json` + Evidence ## PLAN. Todo GUI-Call + Board-Datei + PLAN. DONE.
- Step 1: Pull run 41383643779 (PR #1258 sha 1d74a910, gh-hosted-sweep, job `podman-quadlet`, conclusion `failure`). Doctor evidence (log 457-472): `[os OK] [Docker engine FAILED 'selected Docker endpoint ... unavailable'] [core-deployment OK]` → DEGRADED. Evidence table (log 501-511): `Podman runner=success`, `Runtime detection=failure`. DONE.
- Step 2: ROOT CAUSE. Doctor control-plane path `collectControlPlaneDoctorChecks` (cmd/baha/control_plane_operations.go:144) drops `health.Doctor()` legacy probes and NEVER emits a `podman`/`quadlet` check (those check names exist only in internal/health/doctor.go:64-97, which this path intentionally drops). Only emits: os, Docker engine, selected-runtime, core-deployment, runtime-config, Core Identity, target-access. The podman-acceptance.yml `runtime_detection` step (lines 114-122) greps `^  OK podman` / `^  OK quadlet` on terminal output → can never match. Reproduced locally with build /tmp/baha-base (base aef6b0e1). DONE.
- Step 3: FIX (Owner-authorized Option 2, Subproblem 1 only). Add `PodmanRuntimeDoctorChecks` (new cmd/baha/podman_doctor_checks.go): probes Podman engine authority (`VerifyLocalRuntimeAuthority`) + Quadlet generator (`QuadletAvailable`) and appends `podman` + `quadlet` checks BEFORE the core-deployment early return, ONLY when `target.RuntimeProvider == "podman"`. Verified: `OK podman`/`OK quadlet` now appear for podman targets; Docker-target doctor output untouched (no new checks). Build green, `go vet` green. Regression tests added (both pass). DONE.
- Step 3b: SECOND blocker (SUBPROBLEM 2 — SPLIT BY OWNER, 2026-11-02). Acceptance greps `^READY$`, but doctor prints `NOT DEPLOYED` (not READY) when podman+Quadlet are available but no Core is installed (fresh runner): `inspectControlPlaneDoctor` sets `ready = (all checks OK) AND NOT core-deployed`. Docker-acceptance requires `ready=False` when no Core, so `ready` cannot be changed unconditionally. Owner decision: DO NOT touch workflow (belongs to #1258) and DO NOT change doctor `ready` semantics. My PR delivers ONLY the podman/quadlet checks; the readiness/ordering patch is documented as "NOTE for 1258" below. Clean separation, no merge conflict. DONE.
- Step 4: Commit da848e04 (3 files, +102), branch `work/podman-doctor` pushed to origin. PR #1267 opened vs origin/develop. PRSC run 41388116883 watched to terminal: BLOCKED. Failure is CI gate-map (maintainer-owned), NOT my code:
  ```
  BLOCKED: coverage-unresolved: CLI runtime impact needs qualified targeted native coverage:
    cmd/baha/control_plane_operations.go; cmd/baha/podman_doctor_checks.go; cmd/baha/podman_doctor_checks_test.go
  ```
  `scripts/pr-gate-plan.py:~1518` fail-closed-maps any `cmd/baha/*.go` runtime change to `cli-unresolved-runtime-impact` UNLESS an explicit reviewed-source clause binds it to the existing `atomic/docker/lifecycle` + `atomic/podman/lifecycle` gates (db138ecd / `runtime_restart_integration_test.go` pattern). My change has no such clause. CANNOT resolve within write-set: mission forbids `scripts/pr-*` edits; the workflow that owns the fixed gate test-selection belongs to #1258. Code is correct; the CI wiring is a maintainer decision. Terminal state reached.
- Step 5: Evidence + HANDOFF. END_DONE with pr #1267 / head da848e04 / run 41388116883.

Write-Set (mission STOP): cmd/baha/*doctor*, internal/** detection files. No subagent/codeman spawn. No merge. No workflow edits. No scripts/pr-* edits.

## NOTE for #1258 (separate, NOT in PR #1267 — workflow file is #1258-owned)
The `runtime_detection` step in `.github/workflows/podman-acceptance.yml` (id `runtime_detection`, ~line 114) runs `baha doctor` BEFORE the Core bootstrap (line ~159 `baha target create ...` + line ~160 `baha up --control-plane-only --yes`). Two related gaps remain for #1258 to own (do NOT edit in this lane):
1. **Ordering / READY reachability:** on a fresh runner the doctor has no Core, so it prints `NOT DEPLOYED` (not READY) even with working podman+Quadlet. To make the `^READY$` grep reachable, bootstrap the Podman Core (target create + `baha up --control-plane-only --yes`) BEFORE the `baha doctor` probe; and/or relax the grep to accept `NOT DEPLOYED` alongside `READY` for this pre-bootstrap probe.
2. **Gate-map clause (maintainer):** add an explicit reviewed-source clause in `scripts/pr-gate-plan.py` binding `cmd/baha/podman_doctor_checks.go` + the `control_plane_operations.go` doctor path to the existing `atomic/docker/lifecycle` + `atomic/podman/lifecycle` gates, so PR Selected Checks stops fail-closing with `coverage-unresolved`. Without this the verified fix in #1267 cannot pass PRSC.

## Local verification
- Build: `go build -o /tmp/baha-doctor ./cmd/baha` → exit 0.
- `go vet ./cmd/baha` → clean (pre-existing `TestDoctorNotDeployedVersusIncomplete` fails identically on clean base aef6b0e1; unrelated to this change).
- `go test ./cmd/baha/ -run 'TestPodmanRuntimeDoctorChecksEmitsPodmanAndQuadlet|TestCollectControlPlaneDoctorChecksOmitsPodmanForDockerTarget'` → PASS.
- Manual: podman target with fake podman in PATH → doctor emits `  OK         podman`; with no podman → `  FAILED     podman  podman executable not found`. Docker default target → no podman/quadlet check emitted.
- PR #1267 head: da848e04. PRSC run 41388116883: BLOCKED (CI gate-map, maintainer-owned) — code path itself not the cause.
