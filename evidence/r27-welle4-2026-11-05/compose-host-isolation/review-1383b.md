# CODEX-REVIEW — BaseHarbor PR #1383, round 2

Verdict: **REJECT** — exact head `789ae14655bfd52b0419f5eb35d32749b7253fe0`.

## Identity, base note, and changed files

PR #1383 is OPEN and ready (not draft), base `develop`. The PR API head and remote `work/r27-compose-isolation` both equal `789ae14655bfd52b0419f5eb35d32749b7253fe0`. The candidate's parent chain has `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7` as ancestor. Current remote develop is `42bfcb1cb481c9e37ecd6ce30580e27829284113`, so the requested 24c7 note is recorded as base drift for the merge branch, not as the technical blocker.

The name-only diff from the recorded 24c base has four files, all Go test/harness files:

- `cmd/baha/app_repository_integration_test.go`
- `cmd/baha/app_workload_integration_test.go`
- `cmd/baha/repository_runtime_fixture_test.go`
- `cmd/baha/runtime_integration_test_support_test.go`

The four literal per-test target names are `w169-repository-workflow-iso`, `w169-compose-workload-backends-iso`, `w169-compose-workload-only-iso`, and `w169-build-workload-iso`; their common prefix is joined with the `-iso` suffix by `isolateRuntimeForTest` (`runtime_integration_test_support_test.go:127-136`). They use the same rootless Docker daemon; the candidate does not allocate four separate sockets. The test target names/networks are the claimed isolation boundary.

There is no tracked `cmd/baha/testenv.go` at this head. The historical neutralized selector is actually `cmd/baha/runtime_integration_test_support_test.go:40` in commit `523ba9dfc4fbe9c34b9c5efe7bfe78ffe0cea57f` (`feat(v0.4.15): add target foundation (#410)`), where it used `os.Unsetenv("BASEHARBOR_TARGET")`. The candidate changes that shared support file (base blob `ef3ba430c96f0d0dd69165b0128fa19f8ce54af5`, head blob `f2eba784ddb058189df08b0b3f63337afe556cbc`) to set `BASEHARBOR_TARGET=w169-ci-bootstrap` globally and create that target as `--default`. The literal `testenv.go` path is untouched, but the historical shared selector is not unchanged; the implementation now leaves a shared bootstrap target selected for later calls.

## Isolation code and own counter-probe

Each of the four tests calls `ensureRuntimeIntegrationTrustPlane` and then `isolateRuntimeForTest` with a different name. That creates four unique target names. However, `ensureRuntimeIntegrationTrustPlane` first leaves `BASEHARBOR_TARGET` set to `w169-ci-bootstrap` (`:50-52`) and creates it as the configured default (`:72`). There is no restoration of that selection. `targetSelectionOrigin` recognizes a non-empty `BASEHARBOR_TARGET` as the selected environment override (`cmd/baha/target_selection.go:89-95`), and otherwise recognizes the persisted/configured default (`:96-108`).

I followed the required missing-override counter-probe against the exact source: if one call to `isolateRuntimeForTest` is removed, the variable remains `w169-ci-bootstrap`; it does **not** fall back to the polluted ambient `local` target as the helper comment claims (`runtime_integration_test_support_test.go:123-125`). The removed override therefore targets the shared bootstrap Core, not the foreign `local` Core, and does not prove that the omitted per-test override fails at the stated contamination gate. This is not a discriminating A1 mutation.

I did not launch the actual four-test ensemble or the destructive mutation run against the current shared daemon. Read-only inspection showed the exact fixed names from this test harness already active: `bh-w169-ci-bootstrap-*` containers on `baseharbor-w169-ci-bootstrap-default`, and `bh-w169-compose-workload-only-iso-workload-only-ci-dev-app-1` on the per-test workload network. The foreign `local` Core is also active on `baseharbor-local-default` (network ID `47a6da1c631ac125fc114369feee009ffd2fc28897c784b3a8da5bfe97283e4d`). Reusing or mutating these fixed-name resources would risk changing another live lane's Core/workload; no reset or cleanup was attempted. Thus the requested self-run contaminated pass / red mutation is **not established** in this session.

## Hosted gate

Run `42002171842` is terminal `completed/success` on exact head `789ae14655bfd52b0419f5eb35d32749b7253fe0`; `PR Selected Checks` passed. The hosted run skipped `PR · Selected Runtime`, `Targeted HA · docker`, `Targeted HA · podman`, and `validate`; it does not supply the required own contaminated four-test run or mutation result.

## Recipe

- **Files:** `cmd/baha/runtime_integration_test_support_test.go`, `cmd/baha/app_repository_integration_test.go`, and `cmd/baha/app_workload_integration_test.go`.
- **Change:** keep bootstrap selection scoped to bootstrap setup so it cannot remain the fallback for lifecycle tests; scope each per-test `BASEHARBOR_TARGET` change to that test and preserve the historical neutralized selector. Ensure a missing per-test override resolves to the deliberately polluted `local` target rather than `w169-ci-bootstrap`, and record the actual selected target/network in each test's evidence.
- **Test requirement:** on a safe isolated host, run the four named tests twice from clean state and twice with a foreign live Core present; record all four literal target names and resolved networks, and verify the foreign Core/network identities are unchanged afterward. Remove one test's override in a disposable mutant and require that test to fail at the foreign-Core gate, not to pass by reusing the shared bootstrap. Do not reset or delete shared daemon state.
- **Stop criterion:** the omitted-override mutant can use the shared bootstrap, the contaminated ensemble has not been run and verified safely, a foreign Core changes, or the test environment depends on a shared reset.

No PR, merge, comment, or task-card action was taken.
