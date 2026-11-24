# Post-Merge Verification Desk — r28 Welle 6 (Bug-Hunt fill, Befund only)

Card: w74-0428-216-postmerge. Read-only adversarial verification of the three cards
merged into develop this window; no edits, no PRs, no merges, no subagents (§4.8).
Object: verify the three cards merged into develop THIS window and find any
silent-skip / coverage gap they introduced. develop = current origin/develop.

## PLAN

- Fetch origin/develop, record SHA, confirm >= 2b9a2c6d
- Item 1 (#1821 / 0428-270): dead trusted-local fail-open seam gone, fail-closed path
- Item 2 (#1822 / 0428-273/274/275): 6 pr-gate-coverage.json rows each resolve to an executed gate
- Item 3 (#1824 / 0428-276): per-deployment VerifyDeploymentOwner re-check gates applyEnvironmentDestroyScope
- List any cmd/baha/*.go or internal/*.go changed by the three with NO required-gate admission row
- Write Befundakte table with per-item PASS/FINDING, FINDING gets proposed card number + file:line repro
- Commit + push atomically (single evidence file only; pull --rebase origin main first)
- Bring down any containers; post END_DONE

## Repo / provenance attestation

Planning repo (verified): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`
```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```
Real product remote: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
```
2b9a2c6d1611ea85e11bf81e9650c28165c8293a	refs/heads/develop
```
develop SHA = `2b9a2c6d` >= 2b9a2c6d expected. Verified via clone in /tmp (persistent /tmp zone),
NOT via the quarantined workers/baseharbor checkout.

Three merged commits at develop head:
- `05ef4853` fix(0428-270): remove dead trusted-local fail-open arm (#1821)
- `90086a1f` feat(0428-269): batch baseline — pr-gate-coverage six rows + pre-release baha-ci-operator-testonly (#1822)
- `2b9a2c6d` fix(0428-276): env-destroy OwnerVerified per-deployment owner re-check (#1824)

## Evidence commit

origin/main witness: `git ls-tree -r --name-only origin/main | grep postmerge-verify-2b9a2c6d`
```
evidence/r28-welle6-2026-11-24/postmerge-verify-2b9a2c6d.md
```
Commit SHA: `fd9e6390b4520ec48325cdce40cee676013d56f7` (reachable on origin/main via `git ls-remote main`).
Committed with `git add` of the single evidence file only; pre-existing unstaged edits from other
lanes (releases/v0.4.28.md, two task notes) left untouched.

## 1. #1821 / 0428-270 — operatorauth trusted-local fail-open seam — PASS

Files: `internal/operatorauth/authorization.go` (dead arm removed, commit `05ef4853`),
`internal/operatorauth/config.go` (contract comment corrected).

Read-only reproduction (read from develop):
```
git show origin/develop:internal/operatorauth/authorization.go | sed -n '273,290p'
```
The `if !ManagedEnvironment(...) && !ok { Allowed=true; Mode:"trusted-local" }` arm is gone.
The decision context now has exactly three live outcomes (comment in place): authenticated operator
(tenant scope or claim-resolved membership), the opaque single-use local-runtime grant, or a
fail-closed denial. An unauthenticated request without a valid grant is denied regardless of
environment name.

fail-closed path (read from develop):
```
git show origin/develop:internal/operatorauth/authorization.go | sed -n '285,300p'
```
```go
if !ok {
    decision.ReasonCode = "operator_authentication_required"
    ...
    return decision, machine.NewError(machine.ErrorAuthenticationFailed, ...)
}
```

Other authorizer paths unchanged: the local-runtime grant (`if !ok && grantValid`) and the
authenticated-operator path are both intact; no default trust widened. Confirmed no other caller
rewires trust from the environment name.

Test pins the seam (live, not dead): `internal/operatorauth/authorization_test.go`
`TestAuthorizeMachineOperationNameOnlyPolicyFailsClosed` — failure text "environment name alone
unexpectedly enabled trusted-local authorization" now guards a live boundary. Both `dev` and
`prod` names fail closed with `operator_authentication_required`.

Result: PASS. No silent-skip.

## 2. #1822 / 0428-273/274/275 — pr-gate-coverage six rows — 1 PASS + 1 FINDING

File: `scripts/pr-gate-coverage.json` (6 new component rows), `pre-release.yml`
(`baha-ci-operator-testonly` candidate binary produced so runtime gates' mandatory `test -s` passes;
.ci.yml left byte-identical).

Six rows added by `90086a1f`:
| id | path | resolves to |
| --- | --- | --- |
| source.internal_application_runtime_postgres_go | internal/application/runtime_postgres.go | EXISTS on develop → gates |
| source.internal_metrics_perses_dashboard_provision_go | internal/metrics/perses_dashboard_provision.go | **MISSING on develop** → ghost |
| source.internal_metrics_perses_dashboard_provision_test_go | internal/metrics/perses_dashboard_provision_test.go | **MISSING on develop** → ghost |
| source.cmd_baha_app_broker_compat_test_go | cmd/baha/app_broker_compat_test.go | EXISTS → gates |
| source.internal_operatorauth_authorization_go | internal/operatorauth/authorization.go | EXISTS → gates |
| source.internal_operatorauth_config_go | internal/operatorauth/config.go | EXISTS → gates |

### 2a. Resolution behavior (read-only probe)

`resolve_covered_gates` in `scripts/validate-pr-gate-coverage.py` matches changed paths to the
longest matching `components[].path`; a path that does not exist is absorbed by its parent package
component via `changed.startswith(row["path"])`. The two ghost paths are absorbed by whichever
`internal/metrics` component is longest — effectively zero owner for the specific ghost path.

Run against the 6 declared-but-ghost paths with the real develop-tree:
```
python3 -c "...resolve_covered_gates([...6 paths...], dev_cov)..."
=> COVERED: ['atomic/docker/data-capabilities']   UNOWNED: []   (absorbed, not surfaced)
```
The tool does NOT flag the missing files — it reports the parent `data-capabilities` gate as the
covered owner. So a SELECTED gate does run, but it runs for a file that is not on develop.

### 2b. Ghost-file provenance (read-only)

```
git ls-tree -r --name-only origin/develop | grep perses_dashboard   -> only perses_dashboards.go / *_test.go / _helpers / _hosts / _messaging / _valkey ... NO _provision
git log --all --oneline -- internal/metrics/perses_dashboard_provision.go
   17381017 fix(0428-181): ...   (on branch origin/w54-0428-181-export, NOT develop)
   9f84f47a 0428-181 wire Perses identity dashboard into export path
git merge-base --is-ancestor 9f84f47a origin/develop  -> NO
```
The two `_provision` files never existed on develop; they live only on the separate
`w54-0428-181-export` branch. The 6-row catalog entry claims coverage for source files that are
absent from the merged tree — the row resolves to a gate only by being absorbed into a parent
`internal/metrics` component, not because the named file is real.

Result for item 2: **PASS for the 4 real rows** (runtime_postgres, app_broker_compat_test,
operatorauth/authorization.go, operatorauth/config.go all exist on develop and map to real gates:
`atomic/docker|podman/data-capabilities` + `native/docker|podman/data-capabilities`).
**FINDING for the 2 perses_dashboard rows** — see below.

Proposed card: **t-20261124-0428-277-perses-dashboard-coverage-ghost**
Repro (read-only, file:line in `scripts/pr-gate-coverage.json`):
- line of `"id": "source.internal_metrics_perses_dashboard_provision_go", "path": "internal/metrics/perses_dashboard_provision.go"`
- line of `"id": "source.internal_metrics_perses_dashboard_provision_test_go", "path": "internal/metrics/perses_dashboard_provision_test.go"`
Neither path exists on develop; the rows are unprovable against the merged tree. Note: this is a
catalog-data correctness finding, not a CI-red. Whether the gate actually executes for a real file
depends on the CI-selected changed-path set; the desk only proves the declared rows do not map to
real develop files.

## 3. #1824 / 0428-276 — environment destroy owner re-check — PASS

Files: `internal/deployment/environment_destroy_scope.go`, `cmd/baha/env_destroy.go`,
`internal/deployment/environment_destroy_scope_test.go`, `cmd/baha/env_destroy_integration_test.go`.

Read-only trace of the genuine re-check (`internal/deployment/environment_destroy_scope.go`, develop):
```go
OwnerVerified: verifyEnvironmentDestroyDeploymentOwner(target, record.Identity.DeploymentID, &scope),
...
func verifyEnvironmentDestroyDeploymentOwner(target, deploymentID string, scope *EnvironmentDestroyScope) bool {
    if TestOnlyDeploymentOwnerSeamHook != nil { TestOnlyDeploymentOwnerSeamHook(target, deploymentID) }
    if err := verifyDeploymentOwnerAtSeam(target, deploymentID); err != nil {
        scope.FailClosed = append(scope.FailClosed, fmt.Sprintf("deployment %s owner re-check failed: %v", deploymentID, err))
        return false
    }
    return true
}
func verifyDeploymentOwnerAtSeam(targetName, deploymentID string) error {   // internal/deployment/deployment_store.go:38
    ValidateTargetName(targetName)
    targetRoot, err := TargetStateRoot(targetName)
    ...
    return VerifyDeploymentOwner(targetName, filepath.Join(targetRoot, "runtime"), deploymentID)
}
```
The marker is no longer `OwnerVerified: true` (hardcoded). A failed re-check records a precise
`FailClosed` reason and returns false. The preserved-deployment branch does the same (not a nominal
true).

CLI gate (`cmd/baha/env_destroy.go`, develop):
- Line ~104: `if scope.IsFailClosed() { ... return machine.NewError(machine.ErrorOwnershipAmbiguous, ...) }` — scope build aborts fail-closed on any failed re-check.
- Line ~260: `applyEnvironmentDestroyScope`: `if scope.IsFailClosed() { return fmt.Errorf("environment destroy scope is fail-closed: ...") }`
- Line ~264: per-deployment guard: `if !dep.OwnerVerified || dep.DeploymentID == "" || dep.Environment != scope.Environment || dep.Scope != "scoped" { return fmt.Errorf("deployment ownership is not verified for %s; refusing environment destroy", dep.Application) }`

So `applyEnvironmentDestroyScope` genuinely gates on a real per-deployment `VerifyDeploymentOwner`
re-check, not a nominal true. A scoped deployment that never passed the re-check carries the zero
value `false` and is refused.

Regression tests (`internal/deployment/environment_destroy_scope_test.go`):
- `TestCollectEnvironmentDestroyScopeMarksVerifiedDeployments` (genuine owner => marker true)
- `TestCollectEnvironmentDestroyScopeOwnerReCheckIsGenuine` (seam hook observes the seam ran; marker follows genuine owner state; "marker is nominal, not genuine" failure)
- `TestCollectEnvironmentDestroyScopeUnverifiedUntilReCheckPasses` (zero value IS not-verified; constructed scope without re-check => not marked)
- `TestVerifyEnvironmentDestroyDeploymentOwnerMarkerDirect`
- `cmd/baha/env_destroy_integration_test.go`: `TestApplyEnvironmentDestroyScopeRejectsUnverifiedDeployment`, `TestCLIEnvDestroyFailClosedWhenOwnershipUnknown`

Gate admission (item 4): reachable via `native/docker/environment-destroy` +
`native/podman/environment-destroy` (run `TestEnvironmentDestroyNativeLifecycle` in `./cmd/baha`;
`ci-native-pr-gate.sh`). Result: PASS.

## 4. Silent-sweep — changed product files and their gate admission

All 7 files changed by the three cards vs base:
- `internal/operatorauth/authorization.go` — DECLARED row, gates: atomic/docker|podman/data-capabilities, native/docker|podman/data-capabilities
- `internal/operatorauth/config.go` — DECLARED row (parent), gates same as above
- `internal/application/runtime_postgres.go` — DECLARED, gates data-capabilities
- `cmd/baha/app_broker_compat_test.go` — DECLARED, gates data-capabilities
- `internal/deployment/environment_destroy_scope.go` — DECLARED, gates native/docker|podman/environment-destroy + coreless-lifecycle
- `internal/deployment/environment_destroy_scope_test.go` — DECLARED, gates native/docker|podman/environment-destroy
- `cmd/baha/env_destroy_integration_test.go` — DECLARED, gates native/docker|podman/environment-destroy
- `scripts/pr-gate-coverage.json` — catalog data (not product source; excluded from silent-sweep)
- `.github/workflows/pre-release.yml` — Owner-scope workflow; not product source

Every changed product source file carries a declared admission row and maps to at least one real,
executed CI/native gate. No new-file silent-skip risk among the real files.

## Summary table

| Item | Card | Result | FINDING file:line / proposed card |
| --- | --- | --- | --- |
| 1 | #1821 / 0428-270 | PASS | dead fail-open arm gone; fail-closed live; test pins it |
| 2 | #1822 / 0428-273-275 | PASS (4 rows) + FINDING (2 rows) | `scripts/pr-gate-coverage.json`: `internal/metrics/perses_dashboard_provision.go` + `_test.go` MISSING on develop (ghost); proposed card `t-20261124-0428-277-perses-dashboard-coverage-ghost` |
| 3 | #1824 / 0428-276 | PASS | `applyEnvironmentDestroyScope` line ~264 gates on genuine per-deployment `VerifyDeploymentOwner` re-check; regression tests pin fail-closed |
| 4 | silent-sweep | PASS | all 7 changed files admitted + gate-reachable |

## END
END_DONE w74-0428-216-postmerge: post-merge verification desk complete — 2 PASS (items 1,3), 1 PASS +
1 FINDING (item 2: 2 ghost perses_dashboard coverage rows on develop); no new-file silent-skip.
candidate develop SHA: 2b9a2c6d; evidence commit: fd9e6390b4520ec48325cdce40cee676013d56f7.
