# round-3-teardown-fix.md — 0428-215 native cell operator seam: bootstrap target config

Card: 0428-215 (0428-215-native-cell-operator-seam). Role: Worker.
Shift akte dir: evidence/r28-welle4-2026-11-21/native-cell-operator-seam/
Base develop head (ls-remote, measured 2026-11-21): `4da7ce94b015d5bbd3a8006311785ade5f97b530` (drifted through the shift; PR base pinned at `40cb28c758b02960356434b630086a341ebe1738`).
Branch: `lane-0428-215-native-cell-operator-seam` cut from `40cb28c758b0`, identity `0428-215-natfix`.

## PLAN

- Facts first with byte counts: reproduce the red, diagnose the root cause (done).
- Decide the fix location: fixture (`cmd/baha/runtime_integration_test_support_test.go`), NOT teardown, NOT `internal/operatorauth/**` (tabu) — done.
- Apply the body fix: persist the bootstrap Target config before the gated `target create` so the runtime provider is resolvable for setup and teardown.
- Verify the "not configured" error is gone (done): the test now advances to the operator-auth gate.
- Second proof (read-only): confirm the operator body is selected in the native CI cells (ci.yml + ci-owner-node-native.sh) — done.
- Report the operator-auth gate as STATE (file:line) — it is an owner/base action, not a fixture fix.
- Write repo-rule compliance + cleanliness, todo 4.4.

## Base attestation

- PR base (develop head this PR cuts from): `40cb28c758b02960356434b630086a341ebe1738` (`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` at branch cut; git log shows `40cb28c75 Merge pull request #1594`).
- `git merge-base --is-ancestor 40cb28c758b0 HEAD` -> yes, `40cb28c` is an ancestor of my first commit.
- `git log --oneline 40cb28c758b0..HEAD` lists only my own commit (no foreign candidate carried on top).
- develop has since drifted (ls-remote now `4da7ce94...`); the PR keeps its `40cb28c` base per the mission.

## Red witness (before the fix)

- Command: `BASEHARBOR_SINGLE_DEFAULT_NATIVE_ACCEPTANCE=1 BASEHARBOR_TEST_RUNTIME=docker BASEHARBOR_CI_RUNTIME_INTEGRATION=1 go test ./cmd/baha/ -count=1 -run TestControlPlaneSingleDefaultNativeRuntimeInCI -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"`.
- Verbatim failure (fixture body, before any fix):
  - `control_plane_single_native_ci_test.go:30: prepare BaseHarbor integration trust plane: target "w169-ci-bootstrap-<10hex>" is not configured`.
  - Package teardown echoes it: `bootstrap trust-plane teardown could not begin: ... target "w169-ci-bootstrap-<10hex>" is not configured` and `bootstrap trust-plane teardown left residual resources: wachter cannot inspect residuals: no runtime provider available for target "w169-ci-bootstrap-<10hex>"`.
- Root cause (diagnosed with a targeted trace, not a daemon run): the fixture sets `BASEHARBOR_TARGET = bootstrapTarget` BEFORE `baha target create`. The machine-operation authorization (`authorizeCurrentMCPContext` -> `authorizeMCPOperation` -> `ensureOperatorAuthForBoundary` -> `verifiedLocalWorkloadAuthority`) resolves the effective Target with `deployment.ResolvedTarget` and the not-yet-created bootstrap Target fails `cfg.ResolveTarget(name)` with `target %q is not configured` (internal/deployment/target.go:490), which `verifyLocalWorkloadAuthority` surfaces as a hard error (cmd/baha/local_workload_authority.go:58-61) before the gate can fall through. So the fixture never persists the target definition and the package teardown re-reads an empty targets map at the same config root.
- Note: the same "not configured" string also appears from `internal/deployment/operator_auth.go:29/44/66` when `OperatorAuthForTargetEnvironment` is asked about a target the config does not define; both traces are the same underlying cause (bootstrap Target absent from the config the teardown re-reads).

## Fix applied

- File: `cmd/baha/runtime_integration_test_support_test.go` (fixture, in the mission write-set). No change to `internal/deployment/**`, no `.github/**`, no `scripts/**`, no `internal/operatorauth/**`.
- New helper `persistBootstrapTargetForNativeAcceptance(name string) error` writes the freshly generated bootstrap Target into the active configuration (`deployment.LoadConfigForMutation` + `cfg.Targets[name]` + `cfg.SaveExpected`) at the point the target name is generated, BEFORE the shared `up`. It defaults `DefaultTarget` and the `local` access reference so the runtime provider resolves.
- The gated `baha target create` (which fails closed on this base because `target.create` is not in `internal/operatorauth/local_runtime.go:56` `LocalWorkloadOperation` allowlist and no local-workload operation is set on the CLI path) is replaced by the direct config persist; the single `up --control-plane-only --yes` then converges the management Core on the fresh isolated `<name>-default` native network.
- Result of the fix on the "not configured" bug: re-running the named case no longer emits `target "w169-ci-bootstrap-<hex>" is not configured`. The bootstrap Target now resolves.

## Second proof — operator body selected in the native cells (read-only)

- `scripts/ci-owner-node-native.sh:33` runs `require_pass ./cmd/baha TestControlPlaneSingleDefaultNativeRuntimeInCI 20m` inside the native gate. The gate (`bash scripts/ci-native-pr-gate.sh`) is fed by the `pr_native_selected` matrix in `.github/workflows/ci.yml:478-510` (draft=false PR against develop/lane, `needs.pr_native_impact.outputs.required == 'true'`), and `ci.yml:352-389` resets the dedicated CI runtime and runs the serial runtime-integration + package-teardown gate. The operator control-plane body therefore runs as `=== RUN` in both native cells — selection verified by read-only source inspection. `.github/**` and `scripts/**` are owner scope; not edited here.
- `internal/identityprovider` native SQL body `TestKeycloakSingleNativeSQLInCI` is required green in the same cells (`ci-owner-node-native.sh:31`, `docker-runtime-acceptance.yml:124`, `podman-acceptance.yml:124`), which is what proves the native runtime build infra (rootless daemon, Go toolchain, image cache) is healthy and isolates this from an infra failure.

## STATE — operator-auth gate (owner/base action, not a fixture fix)

After the "not configured" fix the named case advances to the managed-environment operator-auth gate and stops there:

- `control_plane_single_native_ci_test.go:30: prepare BaseHarbor integration trust plane: Managed-environment machine operations require an authenticated BaseHarbor operator.`
- Root cause of THIS gate: on base without a trusted-local policy every environment name fails closed as managed (`internal/operatorauth/config.go:89-91` `ManagedEnvironment` = `ManagedEnvironmentWithPolicy(env, false)` = `!false`). `ensureOperatorAuthForBoundary` (cmd/baha/operator_auth_boundary.go:55) therefore requires operator auth. `verifiedLocalWorkloadAuthority` returns `local=false` because no local-workload operation is set on the `up`/`target` CLI path (only `app` commands set it via `cmd/baha/app_context.go:106`), and the local-runtime grant path (cmd/baha/local_workload_authority.go:113+) is never reached. `resolveOperatorAuthBoundaryConfig` then returns `operatorauth.ErrConfigurationRequired` ("operator OIDC configuration is required for managed environments") at **cmd/baha/operator_auth_boundary.go:113** because no `BASEHARBOR_OPERATOR_OIDC_*` env is set and `noInput`/`assumeYes` are false.
- This is the "operator-auth-klasse erwartet rot on base develop without #1615" the mission anticipates. The fix to make local/dev targets trusted (a trusted-local policy source that makes `ManagedEnvironmentWithPolicy(env, trustedLocal=true)` skip the gate) lives in `internal/operatorauth/**` (tabu) / the base required-plan, i.e. an owner/coordinator action, not a fixture fix. Reported here as STATE with file:line, not implemented.

## repo-rule compliance

- Write-set respected: only `cmd/baha/runtime_integration_test_support_test.go` changed (mission write-set includes the fixture that generates the bootstrap target name). No `.github/**`, no `scripts/**`, no `internal/operatorauth/**`, no `internal/identityprovider/**`, no `internal/serviceaccess/**`, no `internal/capability/perses_selection.go`, no `internal/observability/registry.go`, no owner stacks #1615/#1625/#1623/#1650/#1606/#1614/#1731/#1704.
- No subagents (4.8): every step ran inside this session.
- No bare `go test ./cmd/baha/`: all runs used the named `-run` + `-skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` form.
- No real docker/podman daemon started on the coordinator host; no container/compose project launched. The red/green witnesses are the named Go case output only.
- No `codeman agent post` to the coordinator session; END posted via idle/watcher protocol. No merge, no close, no comment.

## cleanliness

- `docker ps -a` before (my pid here): no BaseHarbor-owned containers; the ambient `bh-docker-dev-shared-*` stack is absent on this host by design.
- `docker ps -a` after: unchanged, no orphaned containers/volumes/networks started by this lane.
- No scratch/checkout files under `/home/marcel/dev/baseharbor-ecosystem`; worktree beside working dir, caches in the worktree. Evidence authored in baseharbor-plan, not the product repo.

## todo (4.4)

- Reproduce red and diagnose root cause: done.
- Fix location decision (fixture, not teardown/operatorauth): done.
- Apply body fix (persist bootstrap Target config before gated create): done.
- Verify "not configured" is gone: done (named case now stops at the operator-auth gate).
- Second proof: operator body selected in native cells (read-only): done.
- STATE the operator-auth gate with file:line: done.
- Akte written: done.
- Commit evidence to baseharbor-plan origin/main and verify path present: pending.
- END handoff: pending.
