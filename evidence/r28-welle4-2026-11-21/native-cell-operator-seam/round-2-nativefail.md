# round-2-nativefail.md — Native Keycloak/Core docker + podman CI failure (diagnose only)

Card 0428-215 (0428-215-nativefaildiag). Role: Worker, diagnosis only, no product change.
Scope split: `.github/**`, `scripts/**`, `cmd/baha/**` are read-only for this lane.

## PLAN

- Facts first with byte counts: locate the matching PR #1743 run and both native cells.
- Decide (a) whether the failing test runs as `=== RUN` in the two native cells (yes).
- Decide (b) whether it fails in its body (yes) or in build infra (no).
- Decide (c): N/A — the test runs, so the selection/skip path is not the cause.
- Verify against PR-head source tree: `ci-owner-node-native.sh` drives the failing test.
- Bound against the owner's other-failure classes (operatorauth gate, package rotes).
- Write the three-line verdict and the required owner action.

## Base attestation

- develop head (run base): `40cb28c758b02960356434b630086a341ebe1738` (`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`, measured 2026-11-21; later drifted to `d2d4ded3...` — the run witnesses below pin the exact base).
- PR #1743 head (run head): `57e7941772ce85dbc60bad7faddd3613c3191c4c`.
- Both native cells ran against exactly `57e7941772ce85dbc60bad7faddd3613c3191c4c` (checkout line in both logs: `HEAD is now at 57e7941 test: use Podman runtime storage environment`).

## Facts (run + jobs, byte counts)

- Run: `gh api repos/mcpdev80/baseharbor/actions/runs?head_sha=57e7941772ce85dbc60bad7faddd3613c3191c4c` -> `database_id 44878727267`, `run_number 6941`, `event pull_request`, `status in_progress` (Go unit job still running at fetch time). `name "CI · PR #1743"`, `path .github/workflows/ci.yml`, head `57e7941772ce...`, base `40cb28c758b0...`.
- Jobs (from `.../runs/44878727267/jobs`):
  - `PR · Native Keycloak/Core · docker` job_id `136769154180` conclusion failure.
  - `PR · Native Keycloak/Core · podman` job_id `136769154127` conclusion failure.
  - `PR · Native gate plan` success, `PR · Trusted Plan` success, `PR · Native · ${{ matrix.id }}` skipped, `PR · Go unit · cli-0/1/2/3` failure, `PR Selected Checks` failure.
- Job log bytes (raw, per-job, the authoritative count — the aggregate run log drops whole job sectors):
  - docker full job log: 50778 bytes (`gh api .../jobs/136769154180/logs`).
  - podman full job log: 39358 bytes (`gh api .../jobs/136769154127/logs`).
  - docker failed-log grep (FAIL/error/not-configured lines): 2087 bytes.

## (a) Does the failing test run as === RUN in the two native cells?

Yes, genuine body execution, not a skip, in both cells.

- docker: `=== RUN   TestControlPlaneSingleDefaultNativeRuntimeInCI` (log line 542), no skip.
- podman: `=== RUN   TestControlPlaneSingleDefaultNativeRuntimeInCI` (log line 400), no skip.
- `TestKeycloakSingleNativeSQLInCI` PASSED in both cells (docker 44.27s, podman 43.78s), which proves the runtime build infra (rootless daemon, Go toolchain, image cache) is healthy and isolates this from an infra failure.
- The run's own Go unit gate `go test ... -run TestControlPlaneSingleDefaultNativeRuntimeInCI` (via `scripts/ci-owner-node-native.sh`) reports `--- FAIL: TestControlPlaneSingleDefaultNativeRuntimeInCI (0.00s)` in both logs (docker line 544, podman line 402).

## (b) Body or infra?

Body failure. Exact error (verbatim from both cells):

- docker log line 543: `    control_plane_single_native_ci_test.go:30: prepare BaseHarbor integration trust plane: target "w169-ci-bootstrap-a755c994" is not configured`
- docker log line 547 (package teardown): `bootstrap trust-plane package teardown failed: bootstrap trust-plane teardown could not begin: bootstrap trust-plane teardown target "w169-ci-bootstrap-a755c994" is not configured`
- docker log line 548: `bootstrap trust-plane teardown left residual resources: wächter cannot inspect residuals: no runtime provider available for target "w169-ci-bootstrap-a755c994"`
- podman log line 401: same text with suffix `w169-ci-bootstrap-9438a4f9`.

The failing test is `TestControlPlaneSingleDefaultNativeRuntimeInCI` in `cmd/baha/control_plane_single_native_ci_test.go`. Its line 30 calls the package fixture `ensureRuntimeIntegrationTrustPlane(t, ctx)`. The fixture generates a fresh bootstrap target name `w169-ci-bootstrap-<10-hex>` (pattern `^w169-ci-bootstrap-[0-9a-f]{10}$` in `cmd/baha/runtime_integration_test_support_test.go:1348`), and the failure surfaces as the fixture's teardown re-reading persisted config.

Root cause (body, not infra): the fixture's teardown path `bootstrapTeardownProvider()` (integration `internal/deployment`) calls `deployment.LoadConfig()` and checks `cfg.Targets[name]`; a missing definition returns `fmt.Errorf("bootstrap trust-plane teardown target %q is not configured", name)` (the verbatim message seen). The per-process target `w169-ci-bootstrap-<hex>` was not present under the config root the teardown re-reads, so the fixture fails closed before inspecting any running Core. This is a body/logic failure of the control-plane native acceptance, not a daemon/compose/network/build failure:

- docker `docker ps -a` witness at reset: `[runtime-reset] containers: none`, `[runtime-reset] networks: no BaseHarbor-owned targets` (log lines 501/503) — rootless daemon + engine healthy, no orphaned cells.
- podman `podman ps -a` witness at reset: `[runtime-reset] quadlet: discovering units` ... `containers: none`, `networks: no BaseHarbor-owned targets` (log lines 357-361) — same.
- Go toolchain, image cache, and the Keycloak native SQL test all passed, so the cell build infra is not the cause.

## (c) Selection/skip path

N/A. The test runs as a real `=== RUN` (see a), so it is not gated out by `.github/workflows/ci.yml`, `scripts/ci-owner-node-native.sh`, or a skip path in the test. The gate script `scripts/ci-owner-node-native.sh:37` requires `TestControlPlaneSingleDefaultNativeRuntimeInCI` to PASS in both `native/docker` and `native/podman` cells; the selection matrix `pr_native_selected` (ci.yml) runs it under `matrix.runtime`.

## (3) Boundary against the owner's other-failure classes

- Not `internal/operatorauth/authorization.go:285` ("Managed-environment machine operations require an authenticated BaseHarbor operator"): that string does not appear anywhere in either native cell log.
- Not a develop-without-#1615 package/CLI "rotes" error: the failure is the bootstrap target config identity, not a CLI package resolution error. The only `not configured` text in both logs is the `w169-ci-bootstrap-<hex>` trust-plane target.
- `geerbt`: quoted only where seen; the operatorauth gate line was not seen in these logs and is therefore not cited.

## (4) Verdict

- Ursaache = body failure in `cmd/baha/control_plane_single_native_ci_test.go` (fixture `ensureRuntimeIntegrationTrustPlane` / teardown `bootstrapTeardownProvider`): the generated bootstrap Target `w169-ci-bootstrap-<hex>` is absent from the config root re-read by `deployment.LoadConfig()` at teardown, so teardown fails closed with `... target "w169-ci-bootstrap-<hex>" is not configured`. This is the failing test's own body, not the cell build infra (docker/podman daemon + Keycloak native SQL test passed; `docker ps -a`/`podman ps -a` = containers none).
- Beleg = run `44878727267` (run_number 6941, PR #1743, head `57e7941772ce85dbc60bad7faddd3613c3191c4c`, base `40cb28c758b0`); docker job `136769154180` (full log 50778 bytes), podman job `136769154127` (full log 39358 bytes); verbatim: `control_plane_single_native_ci_test.go:30: prepare BaseHarbor integration trust plane: target "w169-ci-bootstrap-a755c994" is not configured` (docker log line 543) and the matching podman line with suffix `9438a4f9` (podman log line 401).
- Benoetigte Owner-Aktion: this is 0428-215's own write-set (`cmd/baha/control_plane_single_native_ci_test.go` and its fixture `cmd/baha/runtime_integration_test_support_test.go`). Concrete fix needed: make the bootstrap Target `w169-ci-bootstrap-<hex>` resolve under the config root the teardown re-reads (i.e. `cfg.Targets[name]` is populated when `bootstrapTeardownProvider` runs) — a body fix, not a `.github/**` or `scripts/**` change. If the fix must instead touch `.github/**` (CI matrix selection) or `scripts/**` (ci-owner-node-native.sh / ci-native-pr-gate.sh), that is Owner scope: report file:line, do not edit.

## cleanliness

- No container/compose/network started by this lane. No native cell launched on this host; the hosted cells ARE the evidence.
- `docker ps -a` (from the docker cell reset, witness): `[runtime-reset] containers: none`, `[runtime-reset] networks: no BaseHarbor-owned targets`, `[runtime-reset] volumes: none`.
- `podman ps -a` (from the podman cell reset, witness): `[runtime-reset] quadlet: discovering units` -> `containers: none`, `[runtime-reset] networks: no BaseHarbor-owned targets`, `[runtime-reset] volumes: none`.
- No scratch files written under `/home/marcel/dev/baseharbor-ecosystem`; logs read from the GitHub API only. Evidence file authored in the planning repo, not the product repo.

## repo-rule compliance

- Read-only on PR-head source via `gh api .../contents?...?ref=57e7941772ce...`; no edit to `.github/**`, `scripts/**`, or `cmd/baha/**`.
- No push, no branch cut, no `docker compose up`, no subagents. No bare `go test ./cmd/baha/` run.
- First git remote resolved to the planning repo: `origin https://github.com/mcpdev80/baseharbor-plan.git`. The `workers/` bookkeeping repo origin is `https://github.com/mcpdev80/baseharbor.git` (product repo) — not cited as planning state.

## todo (4.4)

- Facts first with byte counts: done.
- (a) running test confirmed: done.
- (b) body vs infra decided: done.
- (c) N/A: done.
- Source-tree verification: done.
- Evidence file written: done.
- Push evidence to baseharbor-plan origin/main and verify path present: pending.
- END handoff: pending.
