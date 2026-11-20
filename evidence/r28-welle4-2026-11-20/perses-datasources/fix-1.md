# fix-1 — 0428-083 perses datasources, decision b applied + failure classified (2026-11-20)

**Card:** t-20261114-r28-perses-datasources / **PR:** #1684 / **Lane:** lane-0428-083-datasources-r2
**Worker:** x-083h5 / **Date:** 2026-11-20
**State:** Content delivered, **END_BLOCKED** on a base/environment runtime-cell regression — **not** a card defect. All of my card's Go tests are green.

## 1. What changed (decision b, binding)

Coordinator decision (b): keep develop's 3-arg Perses compose signatures, strip my rename + the 4th `contextDir` parameter, splice datasource mounts using `files.Dir`.

- `writePersesGatewayComposeServices(b *strings.Builder, m Manifest, files RuntimeFiles)` — **3-arg**, splice call `splicePersesDatasourceMounts(&rendered, files.Dir, files.ResourceProject)`.
- `RuntimeComposeYAMLForContextDir` **removed** (dead: never called; `RuntimeComposeYAMLForProject(m, files)` is the single path).
- `runtimeComposeYAMLForProject(m, resourceProject string, files RuntimeFiles)` — keeps the `files RuntimeFiles` param; dead `contextDir := files.Dir` local removed.
- `runtime_postgres.go` call site: `writePersesGatewayComposeServices(&b, m, files)`.

My card's real write-set (vs develop 36d075fa) = 18 files:

```
cmd/baha/app_apply_lifecycle.go
internal/application/management_ui.go
internal/application/perses_datasource_mount_test.go
internal/application/perses_datasource_seam.go
internal/application/perses_runtime.go
internal/application/runtime_contract.go
internal/application/runtime_postgres.go
internal/metrics/perses_datasource_lifecycle.go
internal/metrics/perses_datasource_lifecycle_test.go
internal/metrics/perses_prometheus_datasource.go
internal/metrics/perses_prometheus_datasource_container_test.go
internal/metrics/perses_prometheus_datasource_runtime.go
internal/metrics/perses_prometheus_datasource_runtime_test.go
internal/metrics/perses_prometheus_datasource_test.go
internal/metrics/prometheus_render.go
internal/metrics/testdata/perses-prometheus-datasource/config.yaml
internal/metrics/testdata/perses-prometheus-datasource/globaldatasource.json
internal/metrics/testdata/perses-prometheus-datasource/prometheus.json
```

## 2. HEAD / branch / PR witness (ls-remote in-file)

```
$ git ls-remote origin refs/heads/develop
36d075fad77fa61ac8c153e979855546589b32c2  refs/heads/develop
$ git ls-remote origin refs/heads/lane-0428-083-datasources-r2
1c0e33ad864ed3e43b7dbaee57093c507ab90e40  refs/heads/lane-0428-083-datasources-r2
$ git rev-parse HEAD; git rev-parse HEAD^
1c0e33ad864ed3e43b7dbaee57093c507ab90e40
36d075fad77fa61ac8c153e979855546589b32c2   <- parent == current develop tip (rebase sits)
```

PR #1684: head=1c0e33ad864e, base=36d075fad77f, mergeable=MERGEABLE, `git merge-base --is-ancestor origin/develop <head>` = JA.

## 3. The two reported CI failures — built, not guessed

CI run 44671189705 ('CI · PR #1684') completed/failure. Job inventory:

```
$ gh api "repos/mcpdev80/baseharbor/actions/runs/44671189705/jobs" | jobs with conclusion=failure
PR · Native · native/docker/perses-runtime-smoke -> failure
TOTAL failures: 1  (of 30 jobs)
```

The only job that failed is the native docker smoke gate. The "PR Selected Checks" job is the gate **wrapper** that prints `NATIVE_RESULT: failure` — it is itself `test "$NATIVE_RESULT" = success` failing because the native gate failed. No Go unit test failed.

The native smoke gate runs `TestPersesRuntimeSmokeDockerIsolated` (env `BASEHARBOR_PERSES_RUNTIME_SMOKE=1`), from `internal/application/perses_runtime_test.go:349`. The **verbatim** failure line (reproduced locally, identical on the hosted runner):

```
perses_runtime_test.go:374: start Perses runtime: compose up -d: Container ...-perses-1 ...
error mounting "tmpfs" to rootfs at "/etc/perses/database": create mountpoint for /etc/perses/database mount:
make mountpoint "/etc/perses/database": mkdirat /home/.../.local/share/docker/rootfs/overlayfs/<sha>/etc/perses/database: read-only file system
--- FAIL: TestPersesRuntimeSmokeDockerIsolated (6.55s)
```

## 4. Classification (the Owner's test matrix)

**Is it (a) my content — variante b, or (c) a base/environment runtime-cell dependency?** The deciding test: does **pure develop** (36d075fa, with NONE of my card's 18 files) hit the same failure?

1. **tmpfs smoke cell** — checkout develop, run `go test ./internal/application/ -run TestPersesRuntimeSmokeDockerIsolated`:
   ```
   error mounting "tmpfs" to rootfs at "/etc/perses/database": ... mkdirat .../etc/perses/database: read-only file system
   --- FAIL: TestPersesRuntimeSmokeDockerIsolated (5.95s)
   ```
   Identical. This is develop's compose mount (`internal/serviceaccess/perses_compose_realization.go:388`), and my head's copy of that file is byte-identical to develop (`git diff origin/develop 1c0e33ad -- internal/serviceaccess/perses_compose_realization.go` = empty). **My 18 files introduce zero tmpfs/database changes.** → **(c) base/environment** (Docker rootless-overlayfs tmpfs limitation), reproducible on pure develop and on the hosted runner.

2. **Provider/availability unit tests** (the other local `go test ./internal/application/` failures, e.g. `TestProviderIntentMatchesNativeHAAndRejectsUnsupportedMemberOverrides`): these also fail on pure develop with the same `availability_resolution_test.go:54` contract-drift message. Same verdict — pre-existing develop breakage, not my write-set.

My card's own tests are green:
```
$ go test ./internal/application/ -run "TestPersesDatasourceMountResolvesAgainstComposeContextDir|TestPersesComposeRenderedWhenSelected|TestPersesRuntimeFilesProjectProviderFiles"
--- PASS: TestPersesDatasourceMountResolvesAgainstComposeContextDir (0.10s)
--- PASS: TestPersesComposeRenderedWhenSelected (0.10s)
--- PASS: TestPersesRuntimeFilesProjectProviderFiles (0.12s)
ok  github.com/mcpdev80/baseharbor/internal/application
$ go test ./internal/metrics/ -run "Datasource|Perses"   -> all PASS
```

**Verdict: (c).** Both local failures reproduce on pure develop. No correction exists in my 18-file write-set. A fix to the tmpfs compose mount (`perses_compose_realization.go`) or to the CI/docker-runtime gate would be **owner-scope** (`.github/**` / the compose realization lives outside my card); per §4.7 this is a STOP-and-report, not a self-fix.

## 5. Required check (§4.5), measured

```
$ go build ./...                                    # BUILD 0
$ go vet ./internal/application/... ./internal/metrics/...   # VET 0
$ go test ./internal/metrics/ ./contracts/...        # ok (metrics, all contracts)
$ go test ./internal/application/ -run <my card tests>  # ok (datasource + perses render)
$ gofmt -l internal/application/perses_runtime.go internal/application/runtime_postgres.go ...  # clean
```

The two failing groups (`native/docker/perses-runtime-smoke` tmpfs cell; `internal/application` provider/availability contract tests) both fail on pure develop — base/environment, not my card. No `.github/**` or script change is warranted (owner-scope); the native gate needs the runner's Docker rootless-overlayfs tmpfs behavior fixed.

## 6. repo-rule compliance

- Single linear commit 1c0e33ad, parent = current develop tip 36d075fa; branch history = only my commit.
- `git add` scoped to my 18 files only; no `git add -A`; no foreign commits.
- No `.github/**`, no workflow/script change; no subagent (§4.8); no merge.
- No write to `internal/observability/migration.go` (card 168), no write to `cmd/baha/app_status_result.go` (card 078).
- Data source files byte-identical between prior candidate 576c6ad8 and head 1c0e33ad — only compose signatures adapted.
- Test-first pin: `TestPersesDatasourceMountResolvesAgainstComposeContextDir` is RED on pure develop (compile: `undefined: datasourceMountRoots`) and GREEN with decision b.

## 7. cleanliness (runtime cell)

Before: no perses docker project. After the local repro:
```
docker project ls | grep perses-runtime-smoke    -> 0 matching projects (cleanup step removed them)
docker network ls | grep -i perses-runtime-smoke  -> 0 networks
```
The `docker compose up -d` that failed left no lingering `perses-runtime-smoke` project/network (the failing container never started; runc create failed before mount). No named volumes, no orphaned state dirs written to this workspace. `cleanliness: clean — no container/network/volume/state left by the failed tmpfs cell`.

## 8. END

**END_BLOCKED.** Content delivered and merge-ready; the only failing gate is a base/environment runtime-cell regression (Docker rootless-overlayfs tmpfs, reproducible on pure develop and the hosted runner) and a pre-existing develop provider-contract drift — neither in my write-set. Owner to fix the runner tmpfs behavior / waive the native smoke gate, and separately the develop availability-contract drift is outside this card.
