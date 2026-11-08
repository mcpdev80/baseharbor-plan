# 0427-132 r3 — native acceptance of TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry

Native acceptance attempt on PR #1453 head `7557a0b1d088ee8bcb0df2a82a230b5c17f51530`. The mission asked for a live Docker/Podman native PASS of the exact candidate under `BASEHARBOR_INSTALLATION_DESTROY_ACCEPTANCE=1` with an explicit runtime. The acceptance run did not reach PASS; the named test fails with a real, well-characterized regression at the owner seam, which this mission forbids a product code fix for.

## PLAN

- Read mission-132-r3.md + act-1453-review-r2.md; verify PR head + develop ancestry via ls-remote.
- Check runtime prerequisites on host (docker preferred, podman optional).
- Checkout exact PR head in own worktree under /tmp/opencode/.
- Run the acceptance test with explicit Docker runtime under ACCEPTANCE=1; observe terminal state.
- Reproduce against develop HEAD and against the v0.4.25 release to locate the regression.
- Trace the exact failing seam end-to-end (CLI command -> resolveApplication -> SaveDeploymentRecord -> VerifyDeploymentOwner).
- Capture the failure output persistently in evidence/scripts/.
- Write round-3.md; commit evidence to baseharbor-plan origin/main; ls-remote witness; post END.

## Candidate and remote witnesses

- Repository: `mcpdev80/baseharbor`, PR #1453.
- Candidate head: `7557a0b1d088ee8bcb0df2a82a230b5c17f51530` verified with `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1453/head`.
  ```
  $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1453/head
  7557a0b1d088ee8bcb0df2a82a230b5c17f51530  refs/pull/1453/head
  ```
- Develop head: `07ae6c3e91b081a189266ca4b162ba705d4aa78f` (`git ls-remote ... refs/heads/develop`).
- PR merge-base with develop: `e39b0004346cdfd082e34ba55d94d24757bbbd27`. `develop` moved forward to `07ae6c3e` (#1430) after the PR was cut; `git merge-base --is-ancestor 07ae6c3e 7557a0b` exits non-zero (expected, documented in round-2).
- Changed files vs merge base: exactly `cmd/baha/installation_destroy_local_orphan_scope_test.go`, `cmd/baha/runtime_destroy_all.go`, `cmd/baha/runtime_destroy_local_owner_stat.go`. No `.github/**` changes.
- Planning repo used: `/tmp/opencode/0427-132-r3-plan-wt`; `git remote -v` reports `origin https://github.com/mcpdev80/baseharbor-plan.git`. Base before this evidence commit: `e313ca67d021be94c70abc7579b710c7ac114726`.
- Host runtime: Docker `29.9.3` plus a working rootless daemon at `unix:///run/user/1000/docker.sock` (witnessed `docker compose up -d` returning `Started`). Compose plugin `v5.7.0`. Podman not installed on host; one Docker PASS is sufficient per the recipe.

## Acceptance run

- Command (exact PR head, explicit Docker runtime, ACCEPTANCE=1), output tee'd to `evidence/scripts/finalclean.log`:
  ```
  DOCKER_HOST=unix:///run/user/1000/docker.sock BASEHARBOR_INSTALLATION_DESTROY_ACCEPTANCE=1 BASEHARBOR_TEST_RUNTIME=docker \
    go test -p 1 ./cmd/baha/ -run '^TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry$' -count=1 -v -timeout 240s
  ```
- Branch provenance (own worktree `/tmp/opencode/0427-132-r3-accept-wt`):
  ```
  $ git -C /tmp/opencode/0427-132-r3-accept-wt rev-parse HEAD
  7557a0b1d088ee8bcb0df2a82a230b5c17f51530
  $ git -C /tmp/opencode/0427-132-r3-accept-wt status --short
  (clean)
  ```
- Build + vet on the exact head: `go build -o /tmp/baha-132-r3 ./cmd/baha` OK; `go vet ./cmd/baha/` clean.

### Terminal result (exact PR head)

```
=== RUN   TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry
    installation_destroy_native_test.go:43: missing deployment state for installation-retry-native/installation-retry/dev [882b57fe-8564-4116-b0a6-caff423fb058]: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable
--- FAIL: TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry (0.00s)
FAIL
```
The test failed (exit 1) at line 43, the `app init --quick` seam, with `ErrDeploymentOwnerMissing`. It never reached the destroy/retry phases.

## Root-cause: the owner seam at `app init --quick`, not the Core bootstrap

The failure is a genuine code regression, reproduced identically on three independent sources, each built from a clean checkout with an isolated state dir and the rootless Docker daemon:

1. Exact PR head `7557a0b1` — FAIL with `ErrDeploymentOwnerMissing` (above).
2. Develop HEAD `07ae6c3e91b081a189266ca4b162ba705d4aa78f` — FAIL identically (same helper, same target name, different UUID).
3. v0.4.25 release (`bad37ce6`) — PASSES: `target create --reference local` then `app init --quick` returns a valid application manifest (`{"application":"installation-retry", ... "created":false}`).

The distinguishing change is `#1347 fix: enforce state owner and complete app edit lifecycle` (`42bfcb1c`), which made `VerifyDeploymentOwner` mandatory inside `recordDeploymentBeforeMutation` (cmd/baha/app_candidate_consent.go) / cmd/baha/deployment_record.go. Before #1347 (v0.4.25) the seam was not enforced and a `--reference local` target without a Core passed. After #1347, `VerifyDeploymentOwner` fires for the local target's `TargetStateRoot` (which is non-empty for a local target), `coreinstallation.Load(runtime)` returns `os.ErrNotExist` (no Core was installed for a local target), the owner-loan seam requires a boot Target that owns a Core AND that boot Target differs from the requested one, and the tenant hook does not grant. The result is a hard fail-closed at `app init --quick` for a `--reference local` target that is the effective boot Target.

### Exact failing seam (traced)

The failing step is `app init --quick --json` at `cmd/baha/installation_destroy_native_test.go:43`:

```
app_init (app.go:125 / app_input_resolver.go:137)
  -> resolveApplication(ctx, store, nil, "init")   (cmd/baha/app_context.go:72)
  -> SaveDeploymentRecord(record)                  (internal/deployment/deployment_store.go:365)
  -> verifyDeploymentOwnerAtSeam(target, id)       (internal/deployment/deployment_store.go:389)
  -> VerifyDeploymentOwner(target, runtime, id)    (internal/deployment/deployment_store.go:115)
  -> coreinstallation.Load(runtime) == os.ErrNotExist  (no Core for a --reference local target)
  -> ErrDeploymentOwnerMissing                     (internal/deployment/deployment_store.go:139)
  -> wrapped as DeploymentRecordStateError{Kind:"missing", Err: ErrDeploymentOwnerMissing}  (deployment_store.go:390)
```

`VerifyDeploymentOwner` is reached through the `SaveDeploymentRecord` write seam (the `app init` path records a managed deployment record), and the owner verification there fails closed because the `--reference local` default target carries no installation under its `targets/<target>/runtime` root, and the equal-name loan guard (`cmd/baha/deployment_record.go:172`, `bootTargetName == targetName`) refuses to lend the boot Core.

### Core bootstrap is NOT the blocker here

A separate hypothesis — that the test's accepted path needs the shared Core bootstrap (`ensureRuntimeIntegrationTrustPlane`, `cmd/baha/runtime_integration_test_support_test.go:100` running `up --control-plane-only --yes`) to have run first — was tested and **disproved**:

- With `DOCKER_HOST=unix:///run/user/1000/docker.sock` exported, `up --control-plane-only --yes` on a fresh `w169-ci-bootstrap-99` target completes and reports `BaseHarbor Core READY: SQL + Secrets + Identity.` The daemon (Docker `29.9.3`, compose `v5.7.0`) works.
- The earlier `container runtime orchestration not found` seen on the first direct CLI attempts was a **session-state artifact**: those runs never exported `DOCKER_HOST` for the inner runtime, so the runtime fell back to the rootful socket. Once `DOCKER_HOST` was in the environment the bootstrap path works; the destroy test still fails identically at line 43.

This means the bootstrap path is reachable in this sandbox; the decisive, reproducible blocker is the owner seam at `app init --quick`.

### Corroborating external witness

GitHub CI run 42434076648 (`Native single-default · Docker`, develop commit `1fe57f250074`) failed at the "Validate real installation destroy and interrupted retry" step with the identical line:
```
installation_destroy_native_test.go:43: missing deployment state for installation-retry-native/installation-retry/dev [ebe18d9c-4024-4f71-a848-7ffd1ac49b26]: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable
```
This proves the test does not pass on develop either, so it is not a sandbox-specific condition that a different runner would resolve.

## Impact on the mission acceptance criterion

- The named native test cannot be made to PASS on this source without a product code change to the owner seam (for example: admit a `--reference local` target through `app init` without a Core, or have the test seed a Core/tenant scope). The mission scopes this lane to acceptance evidence only and forbids a product code fix. No workflow file was edited and no workflow was dispatched (both are Owner-owned).
- The exact-head `go-unit-tests` pass cited in round-2 (CI run `42448230775`) remains a valid unit-level witness for the changed files; it does not satisfy the native-PASS acceptance criterion, which the recipe reserves for a live Docker/Podman run.

## Repo-rule compliance

- Evidence only. No product file, test, or workflow was modified. No workflow was edited or dispatched.
- No runtime, test, or workflow artifact was pushed to `baseharbor` (evidence lives only in `baseharbor-plan`).
- No Markdown checkbox task lines are present in this evidence file.
- Containers from this lane were removed after each run (only a single short-lived `zzboot`/bootstrap target remained between runs; none left running at END).

## Scope decision requested from the Owner

The native PASS is currently unreachable on this source without a product code fix to the owner seam (#1347). Options the Owner may choose:

- Authorize a product code fix (outside this acceptance lane) to admit a `--reference local` target through `app init` without a Core, then re-run the native acceptance; or
- Accept that the native PASS is blocked by the #1347 regression and lift the exact-head native-PASS requirement for this card; or
- Redirect the lane to a different, currently-passing verification of the same contract.

No action was taken that requires the Owner; this is a blocker requiring an Owner scope decision.

END_BLOCKED 0427-132-r3: native PASS of TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry unreachable on PR #1453 head 7557a0b1 — real #1347 owner-seam regression (fails identically on develop HEAD 07ae6c3e and CI run 42434076648; v0.4.25 passes). Failing seam traced: `app init --quick --json` (installation_destroy_native_test.go:43) -> resolveApplication(ctx, store, nil, "init") -> SaveDeploymentRecord -> verifyDeploymentOwnerAtSeam -> VerifyDeploymentOwner -> ErrDeploymentOwnerMissing (os.ErrNotExist: no Core for --reference local default target; boot-target loan refused). Core bootstrap (up --control-plane-only) is NOT the blocker: it succeeds with DOCKER_HOST exported. Evidence-only; no product/workflow change.
