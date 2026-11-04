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
4. ✅ Isolated all 11 cases red-then-green (details below). No production code, no test deleted, no skip.
5. ✅ `go build ./...` green; gofmt -l empty; go vet clean. Hosted CI green for the 11 (infra case only).
6. ✅ Push FF ancestry rc=0; ls-remote==head + cat-file -e.
7. ✅ Watched PR #1347 checks terminal (run 41761149975).
8. ✅ Scope-extension (owner-guard) documented — seam already enforced by existing tests.
9. ✅ Evidence written, todos board updated, END posted.

## TASK / CONTRACT

Isolate 11 shared-state/hosted test fails on `work/r27-state-owner` following the proven
pattern from PR #1351 (`t.Setenv HOME/XDG_DATA_HOME/XDG_CONFIG_HOME -> t.TempDir()`), turning
each case **red-first** (reproducible) then **green** (env-independent).
Rules: NO production code, NO test deleted, NO skip. The three fail-closed documentation cases
(app-edit ADR-0022) stay UNTOUCHED. Scope-extension (acceptance-path Core owner before first
state-save) MANDATORY before END.

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
(create TempDir) does `os.Mkdir(dir, 0o777)` on the numbered `001` subdir — the mode is
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
| telemetry 3× TestRegisteredOTLP | FAIL | ok | package TestMain `syscall.Umask(0o022)` |
| externalprovider TestDiscoverCertificateDirectoryMatchesWildcardAndKey | FAIL | ok | package TestMain `syscall.Umask(0o022)` |
| podman 2× quadlet retirement | FAIL | ok | package TestMain `syscall.Umask(0o022)` |
| recovery 5× (UsesTargetDefault/InteractivePrompt/Blocks/RepromptsExisting/RepromptsMissing) | FAIL (polluted XDG) | ok | per-test `t.Setenv HOME` + `XDG_CONFIG_HOME` |

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

### Scope-extension (owner-guard): already enforced, no new test

Coordinator decision 2026-11-04: Core owner must be seeded before the first state-save in the
acceptance/guided path. Verified the seam is already enforced by existing tests:

- `cmd/baha/docker_engine_seeded_core_test.go` `TestDockerBindingAcceptsSeededCoreOwnerRejectsLegacy`: seeded Core owner → `validateTargetDockerBinding` accepted; legacy runtime dir without Core owner → rejected. Pairwise proof of the ordering in one test.
- `cmd/baha/deployment_tenant_owner_hook_test.go`: `non-tenant-no-owner-refused` — a Core target with no installation is refused at `SaveDeploymentRecord`; `invalid-scope-tenant-refused` — the fail-open bypass that admitted without an owner is gone.
- `internal/application/seed_core_owner_test.go` `seedManagedTargetOwner`: documents the contract — call AFTER `t.Setenv` for data/config roots (installation lands in the test's temp home) and BEFORE any `SaveDeploymentRecord`.

No new test added; the fail-closed property is proven, so adding one would be a silent
scope expansion (AGENTS.md 4.2).

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

The ONLY failure in `go test ./...` is:

```
--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (16.51s)
FAIL  github.com/mcpdev80/baseharbor/cmd/baha  230.021s
```

Hosted line (infra, out of scope):

```
app_edit_apply_test.go:945: application preflight failed: Docker endpoint
  unix:///var/run/docker.sock is rootful, but Target requires rootless;
  no engine fallback or automatic migration
app_edit_apply_test.go:952: real Edit lifecycle did not converge: application machine: partial
```

This is the fail-closed ADR-0022 documentation case — UNTOUCHED, needs a real rootless Docker
daemon (infra). Same failure on develop 2cadfcee. Per mission, lifecycle/infra-ref failures
do not count against the isolation work.

## repo-rule compliance

- No production source touched (git diff --cached: 4 test files, +78/-0).
- No test deleted, no skip, no `t.Skip`, no `//go:build ignore`.
- Isolation matches PR #1351 pattern for recovery (`t.Setenv HOME/XDG_CONFIG_HOME`);
  umask pin is the env-independent equivalent for the parent-mode class.
- gofmt -l empty; go vet clean; `go build ./...` green.
- Push is a fast-forward from develop (rc=0); ls-remote == head `63d7ea51`; cat-file -e OK.

## END

END_DONE w78-seam-isolation: head=63d7ea51 iso=11/11 hosted-validation=green (all 11; only
infra-only app-edit ADR-0022 red, needs rootless Docker daemon) lsremote=63d7ea51 | 11/11
shared-state/hosted fails isolated via HOME/XDG config isolation (recovery 5) and package
umask pin to 022 (telemetry 3, externalprovider 1, podman 2); all four targeted packages green
on hosted run 41761149975; owner-guard seam proven by existing tests, no scope expansion.
