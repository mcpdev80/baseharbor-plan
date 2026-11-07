# Compose host isolation — native CI acceptance, round 1

- Task: `t-20261105-r27-compose-host-isolation` (card 0427-110)
- Mission: `coordinator/missions/0427-110-compose-native-acceptance.txt`, lane `3a4d5d33`
- Date: 2026-11-07 (shift, UTC)
- Model: worker-ornith1.5 (ornith), session `ses_e49babc3dffebi1oqvACeMj7vx`

## Goal

Run the four compose/lifecycle integration tests ECHT in the existing develop-acceptance on Docker AND
Podman — no skip, no fake green — across (a) clean host state and (b) deliberately polluted host state
(foreign live Core/daemon running), plus an isolation-omission mutant that must be RED and revert to GREEN,
plus fail-closed without container capability.

## Base attestation (provenance)

- Product repo: `https://github.com/mcpdev80/baseharbor.git`
- `git ls-remote origin develop` => `812c99c8873df400348fbc8cc9be5e650b8966c4  refs/heads/develop`
- Working branch cut from: `812c99c8873df400348fbc8cc9be5e650b8966c4` (develop) — branch
  `runtime-validation/compose-isolation/0427-110-develop`
- `origin/develop` is an ancestor of the working branch (base confirmed before first commit).
- Planning repo: `https://github.com/mcpdev80/baseharbor-plan.git`, `origin/main` => `2b19a1329b8f52abcd28a809613f59d647cfb03e`

## ## PLAN (numbered steps)

- Read mission + task contract + AGENTS / DEVELOPMENT_GUIDELINES; verify base via `git ls-remote`.
- Create working branch from base 812c99c88.
- Audit both SSH test hosts (baha-docker, baha-podman): live Core/state, runtimes, images; claim via vm-lock.sh.
- Confirm skip gate locally; build host test binary (`go test -c`) on docker host.
- Diagnose why clean-develop build fails trust-plane gate on contaminated docker host (isolation vs default-target) with instrumented run.
- Run 4 tests x Docker x clean cell (transcript).
- Run 4 tests x Docker x polluted cell (transcript).
- Run 4 tests x Podman x clean cell (transcript).
- Run 4 tests x Podman x polluted cell (transcript).
- Build isolation-omission mutant (RED) + revert (GREEN) on Docker and Podman.
- Fail-closed without container capability verified.
- If real defect found: fix in product (test/fixture files only), rebuild, rerun to terminal, record exact SHA.
- Run hosted develop-acceptance (targeted-integration.yml compose-isolation) at exact SHA; observe to terminal.
- Publish evidence round-1.md; release VM locks; bring down lane containers; END.

## Environment witnesses

### Docker host `baha-docker` (192.168.6.166)

- SSH reachable, rootless docker 29.8.1, overlayfs, cgroupns v2.
- Live foreign stack present: `bh-local-core-shared-keycloak-1-1` (Up, healthy), `bh-local-shared-openbao-*`
  (Up), `bh-local-shared-postgres-*` (Up) — a real live Core/daemon on the shared daemon (native contamination).
- Images: `ghcr.io/mcpdev80/baseharbor-runtime:latest|edge`, plus gfield0427 dev images.
- Orphan volumes from prior lanes: `bh-w169-ci-bootstrap-*`, `bh-w242-smoke-*`.
- No baseharbor binary preinstalled; Go 1.26.8 on host.

### Podman host `baha-podman` (192.168.6.148)

- SSH reachable, rootless podman 5.7.0.
- Live contamination: TWO w169 ci-bootstrap stacks running (postgres + openbao + keycloak) — `bh-w169-ci-bootstrap-*-*`.
- No baseharbor binary, no `baseharbor-runtime` image; Go present.

## Run 1 — skip gate (local, no env) — PASS witness

- Command (host-local, no `BASEHARBOR_CI_RUNTIME_INTEGRATION`):
  `go test ./cmd/baha -run 'TestRepositoryWorkflowRealLifecycle' -count=1 -v`
- Output: `--- SKIP: TestRepositoryWorkflowRealLifecycle (0.00s)` then `PASS`.
- Confirms the fail-closed skip gate fires when the integration env var is absent (before container capability).

## Run 2 — Docker, develop HEAD, contaminated host

- Built host test binary: `go test -c -o /tmp/iso-tests-docker ./cmd/baha` on baha-docker (GOTOOLCHAIN=local), COMPILE_EXIT=0.
- Command: `/tmp/iso-tests-docker -test.count=1 -test.v -test.run '^TestRepositoryWorkflowRealLifecycle$' cmd/baha`
  with `BASEHARBOR_CI_RUNTIME_INTEGRATION=1 BASEHARBOR_TEST_RUNTIME=docker`.
- Result: `--- FAIL: TestRepositoryWorkflowRealLifecycle (0.50s)`
  `app_repository_integration_test.go:29: prepare BaseHarbor integration trust plane: Core sql failed: existing native network lacks a protected Core or shared backend owner`
- `DONE_EXIT=1` (terminal, reproducible).
- Interpretation: honest contamination detection — the ambient `local` Core's native network on the shared
  daemon trips the `inspectCoreDefaultNetworkBinding` gate in `cmd/baha/core_network_binding.go:56`.
  Under investigation whether this is a genuine isolation defect in the bootstrap selector or an
  environmental artifact (the `local` target is configured as default on this host).

## Status

- IN PROGRESS. Not yet DONE. The failure is being diagnosed (instrumented run to capture the exact evaluated
  target name) before deciding fix-vs-environmental.
- VM locks held: `baha-docker` (lane 0427-110-compose-native-acceptance).

## END

- (not posted yet)
