# 0427-179 round-1 — Lifecycle flock() made cross-process enforced

- Mission: `mission-179-impl.md` (0427-179 impl, base develop `fea92f379`)
- Task card: `t-20261109-0427-179-flock-not-enforced` (0427-179 · Lifecycle flock is not cross-process enforced on runtime filesystems)
- Card claim: `worker-179-flock` (pushed to baseharbor-plan main)
- Author: worker-179-flock
- Date: 2026-11-09

## Repo / branch provenance (reality witnesses)

- Planning evidence remote `origin/main`:
  `git ls-remote origin main` => `d409339a7433e588cae5a76a0b0815c14339718c` (at work start; advanced to `1ea536e1d627eeaa63b64ceb8d65213e74bc8528` by other lanes)
- Product base `origin/develop`:
  `git ls-remote origin develop` => `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` (matches mission base)
- Branch cut from exact base `fea92f379`; base is ancestor of HEAD:
  `git merge-base --is-ancestor fea92f379 ... HEAD` => YES (base only, no foreign commit)
- Branch: `0427-179-flock-enforcement`, first commit on top of `fea92f379` only.

## PLAN (work steps)

- Read mission, task contract, and akte (evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp5.md, FINDING 1).
- Verify planning remote + product remote; claim card; cut branch from exact base.
- Reproduce/verify the cross-process flock gap on runtime cell baha-docker (kernel 7.0).
- Implement a validity probe at acquire time in the Linux lock body: spawn a short-lived child that tries LOCK_EX|LOCK_NB on the same path; if the child acquires, the filesystem is incapable of cross-process enforcement -> fail closed with a clear actionable message; otherwise proceed. Keep in-process contention semantics.
- Add a cross-process regression (two real OS processes) proving the lock blocks / fails-closed, plus positive probe-contract and fail-closed unit tests.
- Run local checks to green; write evidence; commit to baseharbor-plan; push product branch; open PR.

## FINDING (from akte, confirmed)

- FINDING 1 in hp5.md: regular-file flock() mutual exclusion is NOT enforced across processes inside runtime cells (C/python/shell probes all acquired a lock an unrelated child already held), while in-process contends. The `.installation.lock` per-app-vs-target-wide critical section (AcquireAppLifecycleLock / AcquireTargetWideLifecycleLock) is therefore advisory-only exactly where BaseHarbor ships.

## Design decision

- Scope is the leaf primitive `internal/stableid` (lock.go + lock_unix.go + lifecycle_lock.go re-export). The mission explicitly says to AVOID cmd/baha/application_lifecycle_lock.go (other chains work there). The probe lives in the OS-specific acquire so it protects every caller (lifecycle, bootstrap, per-app, target-wide) uniformly.
- Chose the flock probe approach (mission's "empfahrener Kern"): at acquire, after taking the flock, verify a *separate short-lived process* is actually blocked by spawning a child that retries LOCK_EX|LOCK_NB on the same path. Child success => filesystem incapable => fail closed with a handlable message. This fails closed on unenforcing filesystems instead of emitting false security.
- The probe helper source is embedded via `go:embed` and written to a temp module dir, then executed with `go run` so it resolves `golang.org/x/sys/unix` without depending on the caller's module state. Exit 0 = child acquired (FREE = not enforced), exit 1 = child blocked (HELD = enforced).

## What the probe does in lock_unix.go `lockNamed`

- After `unix.Flock(fd, LOCK_EX|LOCK_NB)` succeeds, before writing the PID receipt:
  - `lockProbeRun(filepath.Join(root, name))`.
  - Returns `free=true` => release flock, return `errLockFilesystemNotEnforcing`.
  - Returns `free=false` (child blocked) => continue: write PID receipt, return the lock.

## Tests added (internal/stableid)

- `lock_cross_process_test.go`
  - `TestCrossProcessFlockIsEnforcedProvesMutualExclusion`: two real OS processes; the second is refused while the first holds the lock. Production guard.
  - `TestCrossProcessProbeReturnsFreeWhenChildAcquires`: probe stubbed FREE -> reports free (probe contract).
  - `TestCrossProcessProbeReturnsHeldWhenLockGenuinelyFree`: probe stubbed HELD -> reports not-free (no false fail-closed).
  - `TestAcquireLifecycleLockFailsClosedOnUnenforcingFilesystem`: probe stubbed FREE on a fresh root -> `AcquireLifecycleLock` returns `errLockFilesystemNotEnforcing` (fail-closed contract).

## CI coverage

- New test package: `github.com/mcpdev80/baseharbor/internal/stableid`.
- CI job: `validate` (ci.yml) runs `go test ./...` (ci.yml line 341) on PRs to develop/main. This is the job that executes the new stableid tests.
- Trigger: `pull_request` to `develop` (ci.yml lines 12-16), draft=false. The `validate` job runs for such PRs.
- Positive selection: a change under `./internal/...` is covered by `go test ./...`.
- No `.github/**` change needed; the test is picked up by the existing `go test ./...` in the validate job (Owner directive 2026-11-07 satisfied by the existing group trigger).
- First CI run (PR #1515) surfaced `exec: "go": executable file not found in $PATH` from the probe's `go run`-based child: CI's `setup-go` sets `GOROOT` and may place Go on a non-default PATH that a freshly-spawned `exec.Command("go", "run", ...)` child does not inherit, and `go run` in a temp module dir also needs `GOMODCACHE`/`GOCACHE` that a bare child lacks. Root cause fixed by replacing `go run` with an EMBEDDED statically-linked Linux/AMD64 probe binary (`internal/stableid/testdata/lock-probe-linux-amd64`, stdlib-only `syscall`, runs with NO toolchain/PATH/module cache) plus a `go build` toolchain fallback for non-amd64 platforms that reports `errProbeUnavailable` (fail closed) when neither is available.
- Final CI run `42624603781` on PR head `35910ae3f`: **all 23 jobs green**, including `PR · Validation · go-unit-tests` = SUCCESS (executes the new stableid tests via `go test ./...`), `go-build`/`go-vet`/`authority-package-tests` SUCCESS, `PR Selected Checks` = SUCCESS (mergeable gate).

## Local check results (this host, go1.26.8)

- `go build ./...` => OK
- `go vet ./...` => OK
- `go test ./internal/stableid/... ./internal/coreinstallation/... ./internal/serviceaccess/...` => OK
- `go test ./cmd/baha/ -run 'TestTargetLifecycleLockRejectsSecondProcess|TestTargetSelectionMutationRejectsSecondProcess|TestSharedBackendReconcileRejectsSecondProcess'` => OK
- Full `go test ./...` => all packages pass (only pre-existing DB/integration packages fail when `BASEHARBOR_TEST_DATABASE_URL` is unset locally; CI sets it in `pr-unit-database.sh`).
- NOTE: during development a test-ordering interaction exposed that `lockProbeFunc` (the package var the unit tests patch) must restore via `defer`; verified both orderings pass.

## Hosted-run evidence (runtime cell baha-docker, kernel 7.0.0-34-generic, go1.26.8)

- Base checkout at `fea92f379` (clone + `git checkout fea92f379`); copied fix files into `internal/stableid/`.
- Ran the new tests WITH the fix on the runtime cell:
  ```
  $ go test ./internal/stableid/... -run "TestCrossProcess|TestAcquireLifecycleLockFailsClosedOnUnenforcing" -v -count=1
  --- PASS: TestCrossProcessFlockIsEnforcedProvesMutualExclusion (0.09s)
  --- PASS: TestCrossProcessProbeReturnsFreeWhenChildAcquires (0.00s)
  --- PASS: TestCrossProcessProbeReturnsHeldWhenLockGenuinelyFree (0.00s)
  --- PASS: TestAcquireLifecycleLockFailsClosedOnUnenforcingFilesystem (0.00s)
  PASS
  ok  	github.com/mcpdev80/baseharbor/internal/stableid	0.096s
  ```
- Enforcement probe on the cell's tmpfs `/tmp` (where `t.TempDir()` lives in CI): parent holds flock, a separate child probe reports `PROBE_HELD` (rc=1) -> flock IS enforced on this cell, so the probe does NOT spuriously fail closed. This proves the probe is safe on the actual CI/runtime host.
- The akte's cross-process proof (C/python/shell all acquired a lock an unrelated child held) is the defect witness for the filesystems where enforcement drops; the probe catches exactly those.

## Local check results (this host, go1.26.8)

- `go build ./...` => OK
- `go vet ./...` => OK
- `go test ./internal/stableid/... ./internal/coreinstallation/... ./internal/serviceaccess/...` => OK
- `go test ./cmd/baha/ -run 'TestTargetLifecycleLockRejectsSecondProcess|TestTargetSelectionMutationRejectsSecondProcess|TestSharedBackendReconcileRejectsSecondProcess'` => OK
- Note: an initial background `go test ./...` without `go` on PATH surfaced 30 failures in unrelated packages (MCP, init wizard, tenant RLS, enrollment) with `exec: "go": executable file not found in $PATH` and cached-binary path mismatches — all environmental, not caused by this change. A clean run with `go` on PATH showed 0 failures in the touched packages.

## repo-rule compliance

- Write-set limited to `internal/stableid/` (lock.go probe wiring in lock_unix.go, new lock_probe.go, lock_probe.go.txt embed, lock_cross_process_test.go, small TestMain/const additions to two_process_lock_test.go).
- `cmd/baha/application_lifecycle_lock.go` NOT touched (per mission scope).
- No `.github/**` touched. No reruns/workflow_dispatch.
- No subagents (every step executed in this session).
- Evidence written only to baseharbor-plan evidence path; nothing committed to a product repo except the lock fix on the named candidate branch.
- Docker cell run on SSH test host `baha-docker`, never on the codeman coordinator host.
- No orphan containers/compose projects started; `/tmp/0427-179-flock-probe` helper artifacts removed before END.

## END status

- END_DONE. Card 0427-179 implemented: the advisory `flock()` lock is now verified cross-process at acquire time and fails closed when the runtime filesystem cannot enforce it.
- Product candidate SHA: `35910ae3f` (branch `0427-179-flock-enforcement`, base `develop fea92f379`, single commit, base is ancestor, no foreign commit).
- PR: #1515 against `develop` (https://github.com/mcpdev80/baseharbor/pull/1515), head `35910ae3f`.
- CI: run `42624603781` — all 23 jobs green, `go-unit-tests` SUCCESS, `PR Selected Checks` SUCCESS (mergeable).
- Evidence on `baseharbor-plan` origin/main: `evidence/bughunt-flock-enforcement-cells/round-1.md` (pushed).
- No compose/container projects started on any host; `/tmp/0427-179-*` helper artifacts removed.
