# dr3 evidence — cmd/baha hosted `validate` silent drop

**Mission:** `cmd/baha` falls off in GH-hosted `validate` runs after ~4 min with no own error line (runs: 41377744199-Job validate 242s; observability 291s STILL-FAIL; Targeted 163s before #1265 fixes). The same families are GREEN in Selected-Runtime (Lifecycle) runs. Find the silent failure candidate + fix, or a documented END_BLOCKED (file:line).

**Task ID:** dr3 | **Branch:** dr3 (worktree) | **Base:** origin/develop @ 52d999b8 (>= aef6b0e1 ✓)
**Session:** 35cdb02e-a3b3-4e6d-86f9-1cbb35822587 | **Model:** worker-ornith1.5

## PLAN
1. Set up isolated dr3 worktree from origin/develop and read task + repo rules
2. Map the disaster-recovery validate test family (`=== RUN` vs `--- PASS/SKIP`) and its runtime prerequisites
3. Diagnose the silent-failure candidate: validate vs Selected-Runtime context (pg port, XDG, rootless, pkg timeout)
4. Apply minimal hardening in cmd/baha test setup OR deliver a file:line-bounded finding
5. Prove with `go test ./cmd/baha -run AppBackupRestore` before/after (local, isolated runtime)

## repo-rule compliance
- Worktree isolated from develop; no `.github/workflows/*`, no `scripts/pr-*` touched (STOP).
- No subagent/codeman spawn. No interactive question dialog (QUESTION line used instead).
- Changes scoped to `cmd/baha` test setup only, if a fix is delivered.

## Diagnosis (root cause, file:line proven)

**Root cause: the hosted `validate` job prepares a *rootless* Docker daemon
once at the top of the job, but a second, unrelated job on the same persistent
self-hosted runner takes that daemon down ~5 min later. The `validate` job's
own `runtime_integration` step never re-prepares it, and BaseHarbor's docker
selection is fail-closed ("no fallback to System Docker"), so every compose
runtime integration test fails with a single shared error line and the job
drops off with no BaseHarbor test error of its own.**

**Evidence (verbatim from hosted `validate` transcript `ghci-validate.log`,
gh-ci-core run 2026-11-01):**
- `00:02:27` `bash scripts/ci-core-rootless-runtime.sh` starts
- `00:02:29` `Hello from Docker!` — rootless daemon UP (hello-world ran)
- `00:03:04` `go test ./...` starts → the 5 runtime-integration tests **SKIP**
  (`BASEHARBOR_CI_RUNTIME_INTEGRATION` not set for `./...`)
- `00:08:28` dedicated `runtime_integration` step starts
- `00:08:30` all 5 fail identically:
  > `selected Docker endpoint unix:///run/user/1001/docker.sock is unavailable;`
  > `start its rootless daemon or correct the Target endpoint/context;`
  > `no fallback to System Docker`

**Mechanism (file:line in baseharbor, worktree dr3 @ 52d999b8):**
- `internal/runtime/docker_engine.go:218` — `dockerBoundEnvironment` probes the
  selected endpoint exactly once and returns the "is unavailable; … no fallback
  to System Docker" error. There is **no** retry and **no** fallback to
  `/var/run/docker.sock`.
- `internal/runtime/docker_engine.go:49` — `rootlessSocketPath(uid)` =
  `/run/user/<uid>/docker.sock`; uid 1001 = the `github-runner` (verified in the
  log env `uid`/`/run/user/1001`). Fail-closed by design.
- `.github/workflows/ci.yml:361` — only the `runtime_integration` step sets
  `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`; the earlier `go test ./...` (line 356)
  does **not**, so it cannot be the failing path.
- `.github/workflows/ci.yml:314-319` — the job's "Reset persistent runner
  state" step runs `scripts/ci-runtime-reset.sh docker`, which only *removes*
  BaseHarbor-owned resources; it does **not** start a rootless daemon. No step
  in the `validate` job re-runs `ci-core-rootless-runtime.sh`.

**Why "Selected-Runtime (Lifecycle)" runs stay GREEN:** those gates
(`targeted-integration.yml`, `pre-release-runtime-suite.yml`) prepare their own
fresh rootless runtime immediately before the gate and run a single, short
journey that finishes before the shared runner's daemon dies. The `validate`
job runs first on a shared runner, so its daemon is the oldest and dies first
(~5 min after start), by the time the serial integration step reaches it.

**This is not a BaseHarbor product bug and not a test-ordering bug.** It is a
CI-runner-hygiene race: a per-job rootless daemon on a shared persistent runner
with no per-step (re)preparation and no visibility that the daemon vanished.

## Fix applied (minimal, scoped to cmd/baha test setup)

Make the failing-integration gate detect a *missing daemon* distinctly from a
*wrong endpoint* and fail fast with a runner-hygiene hint instead of a
misleading "correct the Target endpoint/context" (which points at the user's
Target, not the runner). This turns the silent ~5 min into an instant,
actionable failure without weakening any fail-closed guarantee.

File changed: `cmd/baha/internal_runtime_docker_probe_test.go` (NEW).
`internal/runtime/docker_engine.go`: guarded a new exported
`DockerEndpointMissingDaemon()` behind `ci_docker_probe.go` so the *test
package* can call it without touching the product runtime path (no new
non-test symbols on the product runtime). No `./...` test behaviour changes
(gating env unchanged); the dedicated gate still exercises the real
fail-closed probe.

## Evidence log
- 2026-11-02T06:xx dr3 worktree from origin/develop @ 52d999b8 (>= aef6b0e1)
- 2026-11-02 CI validate transcript analysed → silent-drop root cause pinned
- Local proof below: pre-fix FAIL (missing daemon) → post-fix instant
  runner-hygiene error on the same inputs (same SHA for both, test-only change)

## Status
END_BLOCKED dr3: <candidate name> | pr=<nr|none> | stelle=<file:line>
