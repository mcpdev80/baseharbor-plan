# CODEX-REVIEW 0427-127 — PR #1454 test bootstrap cleanup

Date: 2026-11-08

## PLAN

1. Refresh PR #1454, develop, and the exact candidate diff from GitHub.
2. Trace setup, teardown registration, Go test cleanup lifetime, and the watcher’s resource identity filter.
3. Verify which hosted CI tests ran on the exact candidate and which relevant jobs were skipped.
4. Record the verdict and actionable correction, regression-test requirements, CI-owner finding, and stop criteria.
5. Validate and publish this review act to baseharbor-plan origin/main.

## Candidate and evidence

- Repository: `mcpdev80/baseharbor`; PR #1454 is open and mergeable.
- Head: `f03b12bdd0b9549b9dd36dae2d947db322caac6e`, confirmed by PR API and `git ls-remote refs/pull/1454/head`.
- Base: `develop` at `e39b0004346cdfd082e34ba55d94d24757bbbd27`; `git merge-base --is-ancestor` exited 0.
- Exact diff: `cmd/baha/runtime_integration_test_support_test.go` only, 137 insertions and one deletion. No production destroy path and no `.github/**` file changed.
- Submitted VM evidence in `round-1.md` reports a baseline of 9 residual containers and a post-fix count of 0 on `baha-docker-2`, including an injected residual that made its temporary witness fail. These are smoke/validation results; I did not rerun the VM test.
- Hosted run `42443497463` is terminal success on this exact PR head. `PR · Validation · cli-package-tests` and `PR Selected Checks` passed; `Targeted HA · docker`, `Targeted HA · podman`, and `PR · Native Keycloak/Core` were skipped.

## Verdict

**REQUEST-CHANGES.** The product destroy path is untouched, but the proposed suite cleanup is registered on one `testing.T` despite being package-wide state, can miss setup failures, and its watcher uses a broad cross-lane prefix. The exact-candidate PR run also did not execute the runtime integration tests that use this helper.

## Findings

### 1. Cleanup lifetime and failure coverage are incomplete

`ensureRuntimeIntegrationTrustPlane` provisions the shared Core at `cmd/baha/runtime_integration_test_support_test.go:122`, but registers `t.Cleanup` only at lines 184-190, after setup and validation have succeeded. Failures after provisioning but before line 190 (for example `openBaoRuntime`, inspection, or bootstrap errors at lines 138-164) call `t.Fatalf` at lines 166-167 before any cleanup is registered. The best-effort provider capture at lines 131-135 also leaves the provider nil on error, while teardown silently returns at lines 221-224.

Further, `runtimeIntegrationTrustPlaneCleanupOnce` registers a cleanup on the first `*testing.T` that reaches the helper (lines 193-208). Go runs that cleanup when that individual test ends, not after the package. The helper has multiple call sites, including four tests selected by the `runtime_integration` selector. Thus the first test can destroy the singleton trust plane while later tests still expect it, and the sync.Once prevents recreation. A test failure or panic after cleanup registration is covered by `t.Cleanup`; a setup failure before registration is not. The implementation does not establish package-wide cleanup on both success and failure paths.

### 2. Watcher identity is broad and the stored lane name is wrong/unused

The actual bootstrap target is generated at line 82. At line 189, `runtimeIntegrationTrustPlaneBootstrap` is assigned a second call to `bootstrapTargetSuffix()`, so it does not identify the target created by setup; `rg` confirms the field is never read. The watcher at lines 263-265 counts every project beginning `bh-w169-ci-bootstrap`, which can include another concurrent lane’s randomly suffixed project. The additional `bh-` plus captured target prefix is the lane-specific scope; the wider prefix violates the requirement to count only this run’s residual class.

The inventory errors in `assertBootstrapTrustPlaneLeavesNoLeftover` return errors and become `t.Errorf` through teardown, which is fail-closed when the cleanup is reached. However, the nil-provider early return and the late cleanup registration bypass that watcher. The temporary injected-leak witness in the submitted evidence is not a durable regression test in the PR diff.

### 3. No production destroy-path ripple

The sole changed file is test support. The teardown calls existing runtime/application/identity-provider APIs only from test code; no production destruction implementation or workflow changed. This scope point passes.

### 4. The exact PR CI run does not execute this change’s runtime tests

The hosted `cli-package-tests` log for run `42443497463` selects the client-command tests (`TestClientCommands...`) and does not select the runtime integration tests calling `ensureRuntimeIntegrationTrustPlane`. The test support’s CI consumers are in `runtime_integration_test_support_test.go` call sites; `.github/workflows/ci.yml:342-349` defines the serial runtime integration command, but the enclosing `validate` job is excluded from pull requests by `.github/workflows/ci.yml:255`. Consequently that job did not run for this PR event. The green selected CLI package result is not execution evidence for the cleanup or watcher.

The necessary routing change is owner-owned: `.github/workflows/ci.yml:255` and `:342-349` need a selected PR/native CI path that executes the affected runtime integration suite on the exact candidate, with skip/fail rejected. I did not edit or dispatch any workflow.

## Correction recipe

- File: `cmd/baha/runtime_integration_test_support_test.go`. Make the lifecycle owner match the singleton lifetime: register one package-level teardown (for example via `TestMain`/an equivalent suite owner), and ensure it runs after all tests. Capture the actual generated bootstrap target and resolved provider before materializing resources. Arrange cleanup before the first operation that can leave runtime resources, and make missing target/provider capture an explicit failure rather than a silent no-op. Preserve a fresh bounded cleanup context so test cancellation does not prevent teardown.
- Watcher: filter by the exact generated target/project namespace owned by this run, including only explicitly derived shared subprojects. Remove the broad `bh-w169-ci-bootstrap` prefix, assign the real target name instead of generating another suffix, and fail the suite if target/provider resolution or inventory inspection is unavailable.
- Tests: add durable package-level coverage proving cleanup runs after multiple helper callers, after an ordinary test failure/panic following setup, and after a setup failure occurring after resource creation. Add a watcher test where this run’s leftover fails, another random `bh-w169-ci-bootstrap-*` project does not fail, and inventory failure fails closed. Confirm later tests still see the trust plane until the suite ends. Keep the tests isolated and avoid any production-destroy path changes.
- CI: have the workflow owner route the changed integration test support through an exact-candidate GitHub job that executes it and rejects skips. The current PR run `42443497463` has no such witness. The required workflow change is `.github/workflows/ci.yml:255,342-349`; no workflow file was changed in this review.
- Stop criterion: do not approve until cleanup runs once after the entire package, setup failures cannot leak resources, the watcher is scoped to this run and fails closed, and the relevant runtime suite is observed passing in hosted CI on the reviewed candidate SHA.

## Repo-rule compliance

- Review-only: product source was not changed; the PR head remained `f03b12bdd0b9549b9dd36dae2d947db322caac6e` at final verification.
- No `.github/**` edits, workflow dispatches, reruns, or container tests on the coordinator host.
- Evidence is stored only in the `baseharbor-plan` vault and contains no Markdown checkbox task lines.

END_DONE 0427-127: REQUEST-CHANGES for PR #1454; candidate `f03b12bdd0b9549b9dd36dae2d947db322caac6e`.
