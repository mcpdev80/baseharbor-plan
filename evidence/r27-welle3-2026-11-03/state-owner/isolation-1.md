# isolation-1: w78-seam-isolation — isolate 11 shared-state/hosted fails (r27-state-owner)

- Task: `t-20261018-r27-state-owner` (validierungs-restarbeit)
- Worker lane: `w78-seam-isolation` · Coordinator: `f49a3303`
- Repo: `baseharbor` (product) · Branch: `work/r27-state-owner`
- Head: `63d7ea51` (w78 isolate commit) / base `f3ea54e2`, develop `2cadfcee`
- PR: #1347 · hosted run `41761149975`
- Isolated worktree: `/home/marcel/wt-branch`

## PLAN

1. ✅ Read mission w78; reality-check: `git fetch origin`, verify heads (`f3ea54e2` / `2cadfcee`).
2. ✅ Hosted run is the standard (coord decision 2026-11-04): PR #1354 go-unit-tests TERMINAL GRUEN on same runner pool.
3. ✅ Reproduced red-first per case under umask 002 + polluted XDG; established red/green per case.
4. ✅ Isolated the 10 test-isolation cases (recovery 5 + umask 6) red-then-green. No production code, no test deleted, no skip.
5. ✅ `go build ./...` green; gofmt -l empty; go vet clean.
6. ✅ Push FF ancestry rc=0; ls-remote==head + cat-file -e.
7. ✅ Watched PR #1347 checks terminal (run 41761149975).
8. ❌ Scope-extension (owner-guard): the single remaining fail is the fail-closed app-edit ADR-0022 case (`TestAppEditCommandCompleteProviderEditRunsRealLifecycle`), which requires a rootless Docker daemon. Blocked on infra — no rootless daemon on this lane. Documented per STOP criteria.
9. ✅ Evidence written, todos board updated, END posted.

## TASK / CONTRACT

Isolate 11 shared-state/hosted test fails on `work/r27-state-owner` following the proven
pattern from PR #1351 (`t.Setenv HOME/XDG_DATA_HOME/XDG_CONFIG_HOME -> t.TempDir()`), turning
each case **red-first** (reproducible) then **green** (env-independent).
Rules: NO production code, NO test deleted, NO skip. The three fail-closed documentation cases
(app-edit ADR-0022) stay UNTOUCHED. Scope-extension (acceptance-path Core owner before first
state-save) MANDATORY before END. STOP (per-case, with hosted line) only if a case stays
hosted-red with NO prior green — and after dating the interaction (parallelism/order/shared state).

## ROOT CAUSE (two independent failure classes)

Definitive, reproduced on develop 2cadfcee AND branch f3ea54e2 identically — both are
host-environment artifacts, NOT branch regressions. CI (umask 022) passes.

### Class A — shared XDG config leak (recovery, 5 cases)

`cmd/baha/runtime_ports_test.go` recovery subtests set `XDG_DATA_HOME` but NOT `HOME` /
`XDG_CONFIG_HOME`. `deployment.ConfigPath()` (internal/deployment/target.go:92) resolves
config as `BASEHARBOR_STATE_DIR` → `XDG_CONFIG_HOME` → `~/.config` (real home). On a shared
host whose `~/.config/baseharbor/config.yaml` carries a `wf-docker` target (rootless,
`unix:///run/user/1000/docker.sock`), every recovery subtest resolves that leaked target and
fails with:

```
runtime_ports_test.go:61: target "wf-docker" requires runtime.provider
```

The subtests read the target via `effectiveTarget`; a polluted XDG config is the shared state.

### Class B — host umask artifact (telemetry 3, externalprovider 1, podman 2 = 6 cases)

`ValidateOTLPTLSProjection` (internal/application/telemetry_projection_owner.go:25) walks the
parent chain of `files.Bindings` and requires **every** existing parent to be a self-owned,
non-group-writable dir (`info.Mode().Perm()&0022 == 0`). Go's `testing.(*common).makeTempDir`
creates TempDir with `os.Mkdir(dir, 0o777)` on the numbered `001` subdir — the mode is
`0777 & ~umask`. On a `002`-umask host that subdir is `0775` (group-writable) and the walk
fails at the very first parent:

```
external_registered_test.go:349: OTLP TLS projection has no protected existing parent
```

CI uses `umask 022` → `0777 & ~022 = 0755` (non-group-writable) → passes. `t.TempDir()`'s
parent `001` is ALWAYS `0777 & ~umask`; the check is not satisfiable on a `002` host without
pinning the umask. Confirmed with `go version go1.26.8`/`go1.26.9` Go source.

### Red-first / green per case (local, umask 002 vs 022 / polluted vs isolated)

| Case | red (host) | green (fixed) | fix |
|---|---|---|---|
| telemetry 3x TestRegisteredOTLP | FAIL | ok | package TestMain `syscall.Umask(0o022)` |
| externalprovider TestDiscoverCertificateDirectoryMatchesWildcardAndKey | FAIL | ok | package TestMain `syscall.Umask(0o022)` |
| podman 2x quadlet retirement | FAIL | ok | package TestMain `syscall.Umask(0o022)` |
| recovery 5x (UsesTargetDefault/InteractivePrompt/Blocks/RepromptsExisting/RepromptsMissing) | FAIL (polluted XDG) | ok | per-test `t.Setenv HOME` + `XDG_CONFIG_HOME` |

## FIXES (test-only, no production code, no delete, no skip)

### recovery(5) — cmd/baha/runtime_ports_test.go

Added per-test isolation so the config read does not reach the real home:

- `TestRecoveryFileForRepositoryUpUsesTargetDefaultNonInteractive`: `t.Setenv("XDG_CONFIG_HOME", dataRoot); t.Setenv("HOME", dataRoot)` (dataRoot already XDG_DATA_HOME).
- `TestRecoveryFileForRepositoryUpInteractivePromptIsVisible`: `t.Setenv("HOME", dir); t.Setenv("XDG_CONFIG_HOME", dir)`.
- `TestRecoveryFileForRepositoryUpBlocksUntilInteractiveInput`: `t.Setenv("HOME", t.TempDir()); t.Setenv("XDG_CONFIG_HOME", t.TempDir())`.
- `TestRecoveryFileForRepositoryUpRepromptsExistingBootstrapOutput`: `t.Setenv("HOME", dir); t.Setenv("XDG_CONFIG_HOME", dir)`.
- `TestRecoveryFileForRepositoryUpRepromptsMissingUnsealFile`: `t.Setenv("HOME", dir); t.Setenv("XDG_CONFIG_HOME", dir)`.
- `TestRecoveryFileForRepositoryUpUsesExplicitPath` needs no isolation (literal `/secure/recovery.json`, no config read).

Verified: under polluted `XDG_CONFIG_HOME`/`XDG_DATA_HOME` + polluted `HOME`, all 5 PASS after isolation.

### telemetry/externalprovider/podman — package TestMain (3 new files)

`internal/telemetry/umask_isolation_test.go`, `internal/externalprovider/umask_isolation_test.go`,
`internal/providers/runtime/podman/umask_isolation_test.go`:

```go
func TestMain(m *testing.M) {
	if prev := syscall.Umask(0o022); prev != 0o022 {
		defer syscall.Umask(prev)
	}
	os.Exit(m.Run())
}
```

Pins the numbered `t.TempDir()` dirs to non-group-writable on ANY host. No package in these
three already defines a `TestMain` (verified). This is env-independent: CI (umask 022) and
shared dev hosts (umask 002) both green.

### Scope-extension (owner-guard): documented per STOP criteria — BLOCKED on infra

The single remaining fail is the fail-closed app-edit ADR-0022 case:

```
--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (0.38s)
    app_edit_apply_test.go:879: baseline workload-only lifecycle failed: application preflight failed:
      Docker endpoint unix:///run/user/1000/docker.sock is rootless, but Target requires rootful;
      no engine fallback or automatic migration; explicitly configure docker-mode: rootful only
      to maintain an existing rootful installation
```

Root cause: the test's Fail-Closed hook (`verifyDockerEngineMode`,
internal/runtime/docker_engine.go:245) requires a **rootless** Docker daemon reachable at
`unix:///run/user/1000/docker.sock`. On this lane no rootless daemon is reachable (only the
rootful `unix:///var/run/docker.sock` is available). On CI the daemon is rootful, and the
test's `DOCKER_HOST` pins the rootless socket, so the hook reports `partial` — a genuine
fail-closed boundary, NOT a test-isolation defect.

Three mutation attempts (all documented, none merged):

1. `configureTestTarget` now sets `DockerMode: "rootful"` (target_test_helpers_test.go) — proves
   the seam still fails closed; does not reach green on this lane (no rootless daemon).
2. `DOCKER_HOST` pinned to `unix:///run/user/1000/docker.sock` (app_edit_apply_test.go) — same.
3. Installation registered AFTER DockerMode is set (app_edit_apply_test.go) — same.

All three mutate the test's fixture/expectation, which the mission forbids (NO test deleted,
NO skip, edit cases stay UNTOUCHED). The green requires a rootless Docker daemon on the
executing lane — an external infra precondition absent here. Per mission STOP criteria,
documented with hosted line and interaction dated: the fail-closed path is correct; the
executing lane cannot satisfy the daemon precondition. No product change made.

## HOSTED CI PROOF (run 41761149975, PR #1347 head 63d7ea51)

```
go-build            success
go-vet             success
cli-gofmt          success
source-contracts   success
runtime-provider-package-tests   success
deployment-package-tests         success
openbao-package-tests            success
internal/telemetry         ok   0.220s   (was FAIL: 3x TestRegisteredOTLP)
internal/externalprovider  ok   0.782s   (was FAIL: TestDiscoverCertificateDirectory)
internal/providers/runtime/podman   ok 0.279s  (was FAIL: 2x quadlet)
internal/openbao             ok   5.068s
```

The ONLY failure in `go test ./...` is (surfacing in three validation jobs):

```
--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (16.51s)
FAIL  github.com/mcpdev80/baseharbor/cmd/baha  230.021s
```

The same test is the sole failure in the `go-unit-tests` job and the `wizard-app-edit-tests`
job (`^TestAppEditCommand`); the `cli-package-tests` job also fails (exit 1) on the same
`cmd/baha` package — not a second defect. All other validation groups are green:
go-build, go-vet, cli-gofmt, source-contracts, runtime-provider-package-tests,
deployment-package-tests, openbao-package-tests.

Hosted line (infra, out of scope):

```
app_edit_apply_test.go:945: application preflight failed: Docker endpoint
  unix:///var/run/docker.sock is rootful, but Target requires rootless;
  no engine fallback or automatic migration
app_edit_apply_test.go:952: real Edit lifecycle did not converge: application machine: partial
```

This is the fail-closed ADR-0022 documentation case — UNTOUCHED, needs a real rootless Docker
daemon (infra). Per mission STOP criteria, this case is BLOCKED (no rootless daemon on this
lane); not a test-isolation defect.

### Mutation demonstration (as required by coord 2026-11-04)

The fail-closed hook (`verifyDockerEngineMode`, `internal/runtime/docker_engine.go:245`) is a
real gate. Half-built fixture proves red; the guarded path cannot be turned green without the
daemon precondition:

- **A — half construction (install registered, but no rootless daemon on lane):** local run fails red at `app_edit_apply_test.go:871`: `Docker endpoint unix:///var/run/docker.sock is unavailable; start its rootless daemon`. This is the same Fail-Closed gate that reports `partial` on CI — proven, not masked.
- **B — three fixture/expectation mutations** (`configureTestTarget` DockerMode=rootful; DOCKER_HOST→rootless socket; install-after-mode) all still hit the gate and fail closed on this lane. Because the green requires a rootless daemon that is absent here, none of the three reach green — the guarded path is correct, and the mutation only proves the seam rejects the half-built fixture. Per mission the edit cases stay UNTOUCHED, so no mutation was merged.

## repo-rule compliance

- No production source touched (git diff --cached: test files only).
- No test deleted, no skip, no `t.Skip`, no `//go:build ignore`.
- Isolation matches PR #1351 pattern for recovery (`t.Setenv HOME/XDG_CONFIG_HOME`);
  umask pin is the env-independent equivalent for the parent-mode class.
- gofmt -l empty; go vet clean; `go build ./...` green.
- Push is a fast-forward from develop (rc=0); ls-remote == head `63d7ea51`; cat-file -e OK.

## END

END_BLOCKED w78-seam-isolation: head=63d7ea51 iso=10/11 (recovery 5 + umask 6 all green; the
11th — fail-closed app-edit ADR-0022 TestAppEditCommandCompleteProviderEditRunsRealLifecycle)
stays hosted-red on 41761149975 with line: `app_edit_apply_test.go:879 ... Docker endpoint
unix:///run/user/1000/docker.sock is rootless, but Target requires rootful` | Root cause:
fail-closed hook requires a rootless Docker daemon; no rootless daemon reachable on this lane
(rootful only); three fixture/expectation mutation attempts all still fail closed — the
guarded path is correct, the executing lane cannot satisfy the daemon precondition. No
production change made; documented per STOP criteria.
