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

## PR collision (blocking, awaiting Owner decision)

GitHub auto-assigned the pushed branch `perses-tmpfs-mountpoint-wt` the number 1684. PR #1684 already belongs to card 0428-083 (head 43d3a8dc0c6c, "Connect Perses Prometheus datasource"), and my commit 03b66ceca53c is NOT in it (clean separation; merge base dbe7fbc3905b). My commit has zero PRs pointing to it. Merging my work into another card's PR would violate one-candidate-per-chain (§4.2) and the one-PR-per-card rule. My branch stays pushed at 03b66ceca; awaiting Owner/Coordinator decision on opening a fresh PR for this branch.

## cleanliness

before: docker ps -aq --filter name=perses = none; docker volume ls | grep perses = none.
after smoke gate PASS: docker ps -aq --filter name=perses = none; docker volume ls | grep perses = NO perses volumes.
host clean at END: no orphan Perses containers; no perses volumes; no compose project bh-perses-runtime-smoke-perses-runtime-prod.
