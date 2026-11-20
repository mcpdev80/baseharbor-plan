# 0428-177 — Perses runtime smoke gate: tmpfs mountpoint, advertised_address schema, shared-namespace gateway routing

## PLAN

- Fix the tmpfs mountpoint defect blocking `native/docker/perses-runtime-smoke` at the product location that emits the mount.
- Fix the invalid `advertised_address` schema key the pinned Perses release rejects.
- Fix the third latent defect found during smoke testing: shared-namespace gateway routes to the service alias which resolves to the gateway's own IP -> HTTP 503.
- Add/extend regression tests so the fixes are durable in CI (no touching `.github/**`).
- One commit, rebase onto develop head, push, open PR with three witnesses.

## first finding: tmpfs mountpoint / plugin extraction

Symptom on hosted runner (run 44717007640, PR #1684 head 43d3a8dc0c6c): `runc create failed ... error mounting "tmpfs" to rootfs at "/etc/perses/database": make mountpoint "/etc/perses/database": mkdirat ... ` — the distroless image has no such directory and the rootfs is read-only.

Root cause refined during smoke testing: Perses v0.55.1 extracts the 33 shipped plugin archives into `/etc/perses/plugins` at startup; a read-only rootfs blocks that extraction, which is the actual gate breaker. Empirically a named volume at `/etc/perses/database` does NOT fix extraction (plugins path still read-only); a named volume at `/etc/perses/plugins` DOES extract all 33 plugins cleanly; tmpfs at `/etc/perses/database` mounts fine (runc creates the mountpoint).

Fix at product locations:
- `internal/serviceaccess/perses_compose_realization.go`: tmpfs at `/etc/perses/database` (writable, ephemeral; runc creates the mountpoint) + named volume `perses-plugins` at `/etc/perses/plugins` (writable extraction target). `PersesServiceMounts` validation updated to accept both.
- `internal/application/runtime_postgres.go`: declare the `perses-plugins` named volume.
- `perses_runtime.go` compose realization validation accepts the corrected mount set.

## second finding: advertised_address schema key

`security.advertised_address` in `internal/serviceaccess/perses_config_render.go:85` is rejected by the pinned release: `field advertised_address not found in type config.Security`. Owner ruling 2026-11-20 confirmed the removal in-scope (card 0428-177 names this location). Removed the line; Perses starts cleanly.

Regression (verbatim, smoke RED): reintroducing the key -> `perses_runtime_test.go:494: perses plugin probe never succeeded ... HTTP 503`. Reverted.

## third finding: shared-namespace gateway routing (HTTP 503)

During smoke testing the gateway returned 503. Runtime proof captured inside the shared gateway namespace:
- `curl http://127.0.0.1:8080/api/v1/plugins` -> 200 (Perses listens on the namespace loopback inside the joined namespace).
- Gateway health checker dials `bh-dev-...-perses:8080` -> `172.18.0.3:8080: connect: connection refused` (the deployment alias resolves to the gateway's own container IP; Perses has no network of its own because `network_mode: service:<gateway>` joins the gateway namespace, so the alias points at the gateway itself).

Fix: in the shared-namespace form the gateway dials the namespace loopback `http://127.0.0.1:8080` (where Perses actually listens) instead of the routable alias.
- `internal/serviceaccess/perses_gateway.go`: `dialUpstream` rewritten to `http://127.0.0.1:<port>` when `sharedNetwork`; `Spec.Upstream` set from `dialUpstream`; added `isLoopbackLiteral` helper. `ServiceAddress` still carries the deployment alias for the certificate/contract identities.
- `internal/serviceaccess/perses_compose_realization.go`: updated the `shared` re-derivation and the self-consistency validation to accept the loopback upstream in the shared form (namespace-local form still routes to the routable alias by service name).
- `internal/application/perses_runtime.go`: compose realization validation accepts `http://127.0.0.1:<port>` as the dial upstream in the shared topology.

Regression (verbatim, smoke RED): reverting the mount (removing both tmpfs and the perses-plugins volume) ->
`level=error msg="unable to unzip the plugin archives" error="unable to unzip plugin archive \"StatusHistoryChart-0.14.1.tar.gz\": unable to extract the archive file: handling file: schemas/migrate/migrate.cue: unable to create directory \"schemas/migrate/\": mkdir /etc/perses/plugins/StatusHistoryChart-0.14.1: read-only file system"`. Reverted.

## smoke gate

Command: `export BASEHARBOR_PERSES_RUNTIME_SMOKE=1` then `go test ./internal/application/ -run 'TestPersesRuntimeSmokeDockerIsolated' -count=1`, invoked in CI by `scripts/ci-native-pr-gate.sh` under `native/docker/perses-runtime-smoke` (5m) -> `run_exact_test TestPersesRuntimeSmokeDockerIsolated`.

Result with the full fix: `--- PASS: TestPersesRuntimeSmokeDockerIsolated (58.20s)`. Host clean afterward.

## repo-rule compliance

- Fixes at product locations only: `perses_config_render.go`, `perses_compose_realization.go`, `runtime_postgres.go`, `perses_runtime.go`, `perses_gateway.go` (+ the two regression tests that assert the corrected contract).
- Smoke gate not deleted or skipped. `.github/**` not touched.
- One commit `03b66ceca53ce2f31c27732f47fd5a12e972e14c`, rebase onto develop head `40cb28c758b0` (ancestor verified via `git merge-base --is-ancestor 40cb28c75 HEAD`; `git log origin/develop..HEAD` lists only this commit; `git diff origin/develop...HEAD --name-only` lists only the 8 files).
- Force-pushed `--force-with-lease` to branch `perses-tmpfs-mountpoint-wt` (remote guard: `origin` = https://github.com/mcpdev80/baseharbor.git).
- `go build ./...` and `go vet ./internal/serviceaccess/ ./internal/application/` clean; full Perses unit/integration suite passes. The remaining `internal/application` failures (`TestPrivateIntegration_Switch_SelectsApplicationScopedBackend`, `TestSharedBackendAliasesCountOnePhysicalModule...`, `TestStandaloneSharedPostgresUsesPhysicalOwner...`) are pre-existing on develop head #1594 (card 0428-198, owner-field), confirmed via `git stash` on base HEAD; outside this write-set.

## PR, runs, and field-gate (measured, exact head)

PR #1724: head `408b18d2dc7b0abe299749bb3a506c8cbd089098`, base develop, draft=false, branch `perses-tmpfs-mountpoint-wt` == `refs/pull/1724/head` (witness: `git ls-remote origin refs/pull/1724/head` -> `408b18d2d`), 8 changed files (`git diff origin/develop...HEAD --name-only`), only my two commits above develop (`git log --oneline origin/develop..HEAD`):
```
408b18d2d fix(0428-177): gofmt perses_runtime_test.go (Source format gate)
03b66ceca fix(0428-177): perses tmpfs mount, advertised_address schema, and shared-namespace gateway routing
```
base attest: `git merge-base --is-ancestor 40cb28c758b0 HEAD` = JA (develop head `40cb28c758b0`).

CI run on the pre-gofmt head `03b66ceca53c` — run id `44791541129` (gh run 6804, `CI · PR #1724`, status completed, conclusion failure):
- `native/docker/perses-runtime-smoke` SUCCESS.
- `PR · Source format` FAILURE (my own defect, not a field gate): `internal/application/perses_runtime_test.go` was not gofmt-fest (`gofmt -l` names exactly this file).

Fix applied: `gofmt -w internal/application/perses_runtime_test.go`; `gofmt -l ./internal/... ./cmd/...` now empty; `go vet ./internal/serviceaccess/ ./internal/application/` clean; full Perses unit/integration suite passes. One commit `408b18d2d` on the same branch (no second PR, no merge with #1684), force-pushed.

CI run on the corrected head `408b18d2dc7b` — run id `44793908238` (gh run 6806, `CI · PR #1724`, status completed, conclusion failure):
- `native/docker/perses-runtime-smoke` SUCCESS. `PR · Source format` SUCCESS. `PR · go-build`/`go-vet`/`owner`/all validations SUCCESS.
- RED: `PR · Go unit · cli-0`, `cli-1`, `cli-2`, `cli-3`, `packages`. Verbatim (`run 44793908238`, job `PR · Go unit · cli-0`, step "Execute selected Go tests with isolated PostgreSQL"): `main_test.go:60: create failed: Managed-environment machine operations require an authenticated BaseHarbor operator.` and `app_repository_workflow_test.go:115: Managed-environment machine operations require an authenticated BaseHarbor operator.` These are the field-wide gate-defect 0428-198 (root 2af892e4e in `internal/serviceaccess/policy.go`, #1594), pre-existing on develop head `40cb28c758b0` (confirmed via `git stash` on base HEAD); outside this write-set. Not changed here; no `.github/**`, no test removed (§3.8, §5.4).
- Everything else skipped or success.

## PR / 0428-1684 (corrected; was misreported as a collision)

No collision and no Owner decision were ever required. `gh pr list --head perses-tmpfs-mountpoint-wt` was empty while the branch was un-PR'd; the earlier "GitHub auto-assigned the pushed branch the number 1684" line was a false reading of a message that referred to another branch. PR #1684 carries `refs/heads/lane-0428-083-datasources-r2` (head `43d3a8dc0c6c`), card 0428-083 "Connect Perses Prometheus datasource". `git merge-base --is-ancestor 03b66ceca 43d3a8dc0c6c` = NEIN: my work was never in #1684 and #1684 is never in mine. GitHub does not assign PR numbers per branch; the real PR for this card is the fresh PR #1724 above.

## cleanliness

before: docker ps -aq --filter name=perses = none; docker volume ls | grep perses = none.
after smoke gate PASS: docker ps -aq --filter name=perses = none; docker volume ls | grep perses = NO perses volumes.
host clean at END: no orphan Perses containers; no perses volumes; no compose project bh-perses-runtime-smoke-perses-runtime-prod.
