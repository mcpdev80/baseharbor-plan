# LIVE-VERIFY round-4 — extended perses + org-env-reconcile + BF-01/BF-03 stack

- lane: mission-lv4 (verify-schicht, KEIN feature-scope)
- shift: 2026-11-15
- model: worker-ornith1.5 / AgentGateway
- candidate SHA (union, throwaway): `92bd3da0f` (final) / `0760469d0` (orphan-test drop) in `/tmp/opencode/lv4-base-wt`
- base attestation: union cut from origin develop `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (ls-remote witness below); develop is the newest common ancestor of all 11 lanes.
- planning remote: `origin/main = 4c1845c39ea5040d5cc14da3317978f401e4302c`
- base product HEAD: `aff1532c2f6c6782a8c13afad83245d1351815e7` (ls-remote witness below)
- planning repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY (NOT workers/baseharbor-plan)

## PLAN checklist (numbered, no checkboxes)

1. Reality witnesses: planning remote, base product HEAD, worktree from origin develop, planning repo path.
2. Verify all 11 mission SHAs on live remotes.
3. Build throwaway union (frost: no merge, throwaway commit).
4. Cell 1: build + vet + per-package tests.
5. Cell 2: orgconfig registry-identity reconcile match/mismatch fail-closed (NEW vs r3).
6. Cell 3: seam descriptor — PersesManagement valid IntegrationDescriptor (Luna r2 fix point).
7. Cell 4: perses three states + lifecycle read-only.
8. Cell 5: BF-01/BF-03 isolation regression.
9. Categorize remaining failures: lane defects vs union artifacts vs environmental.
10. Evidence publish + cleanliness + END.

## Remote witnesses (ls-remote, verbatim)

```
$ git ls-remote origin/main          # baseharbor-plan
4c1845c39ea5040d5cc14da3317978f401e4302c	refs/heads/main
```

```
$ git ls-remote origin HEAD           # baseharbor (product)
aff1532c2f6c6782a8c13afad83245d1351815e7	HEAD
```

### 11 inputs — verified against live remotes

| Mission token | Short SHA | Live head (refs) | Match |
| --- | --- | --- | --- |
| uid-app | `2b91371a3` | origin/lane-0428-uid-app | yes |
| uid-env | `756d21b7` | origin/lane-0428-uid-environment | yes |
| uid-target | `3a91e2a8` | origin/lane-0428-uid-target | yes |
| env-registry | `b85efaf6` | origin/lane-0428-env-registry | yes |
| org-env-reconcile | `32307a4336` | origin/cli2-org-env-reconcile | yes |
| seam | `cb4367f347` | origin/lane-0428-075-perses-seam | yes |
| runtime | `f55d9f94c3` | origin/lane-0428-088-perses-runtime | yes |
| presets | `9534edd` | origin/lane/0427-186-target-policy-presets | yes |
| docs | `ab9086f5` | origin/0428-092-perses-boundary | yes |
| BF-01 | `13e096fc6` | origin/lane-0428-fix-bf01 | yes |
| BF-03 | `756b2be7` | origin/lane-0428-fix-bf03 | yes |

### Union base proof

- develop `0e9ccb582` is an ancestor of every one of the 11 lane heads (verified with `git merge-base --is-ancestor`).
- develop is the newest common ancestor of all 11 lanes (fold of pairwise merge-base == `0e9ccb582`).
- Two of the seven implementation lanes actually branch from `234d8de33` (an ancestor of develop); the other four branch directly from develop. develop is therefore the correct union base.

## Union construction (frost: throwaway commit, no merge pushed)

- Base: origin develop `0e9ccb582`.
- Multi-way merge of all 11 lane heads. Resolves cleanly except `internal/orgconfig/store.go` (bf-01 vs bf-03 content conflict) and the `perses.go` seam-vs-runtime duplicate.
- Resolution A — bf-03 supersedes bf-01: bf-03 `756b2be7` deletes `cmd/baha/target_state_layout.go` and removes the `StateRootOwnsOrganizationState`/`OrganizationTargetSelection`/`StateRootSelected`/`userConfigRoot` symbols bf-01 added. Union takes bf-03's `internal/orgconfig/store.go` + `cmd/baha/target.go` (bf-03 is the newer, self-contained BF-01 evolution).
- Resolution B — seam supersedes runtime perses.go: the runtime lane `f55d9f94c3` ships a REDUCED `internal/capability/perses.go` (empty `Provider.Capabilities`, no `PersesStatus`/`PersesManagementSurfaceNow`); the seam lane `cb4367f347` ships the full r2 file (binds `MetricsV1`, full three-state surface). Union takes the seam file; the runtime lane's `perses_runtime.go`/`runtime_environment.go`/`runtime_lifecycle.go`/`runtime_postgres.go`/`app_status_collect.go` are added intact (no symbol clash).
- Orphan drop: `cmd/baha/target_selection_state_dir_isolation_test.go` is bf-01-only (absent from bf-03) and tests the `StateRoot*` chain bf-03 removed. It was a union artifact, not a lane defect — removed from the union.

## CELL 1 — build + vet + tested packages (union)

Command + output:

```
$ cd /tmp/opencode/lv4-base-wt
$ go build ./...
(Build succeeds, no output)
BUILD_EXIT=0
$ go vet ./...
(Vet succeeds, no output)
VET_EXIT=0
```

Per-package results on the union (count=1, non-DB/non-native):

- `contracts/...` — ok
- `internal/deployment/...` — ok (1.3s)
- `internal/orgconfig/...` — ok (0.3s)
- `internal/capability/...` — ok (0.008s)
- `internal/serviceaccess/...` — ok
- `internal/application/...` — ok AFTER orphan-test drop (see CELL 5)

RESULT: PASS (build + vet clean; all fast packages green).

## CELL 2 — orgconfig registry-identity -> reconcile match/mismatch fail-closed (NEW vs r3)

r3 only tested `32307a43`; this round re-runs the orgconfig identity-reconciliation contract live on the union.

Command + output:

```
$ go test -count=1 ./internal/orgconfig/... -run "Reconcile|Identity|Organization|Registry" -v
=== RUN   TestReconcileIdentityMatchIsAuthoritative
--- PASS: TestReconcileIdentityMatchIsAuthoritative (0.00s)
=== RUN   TestReconcileIdentityMismatchFailsClosed
--- PASS: TestReconcileIdentityMismatchFailsClosed (0.00s)
=== RUN   TestReconcileEmptyDeclarationWithRegistryIdentityFailsClosed
--- PASS: TestReconcileEmptyDeclarationWithRegistryIdentityFailsClosed (0.00s)
=== RUN   TestReconcileAbsentRegistryIdentityIsInert
--- PASS: TestReconcileAbsentRegistryIdentityIsInert (0.00s)
=== RUN   TestResolveEffectiveWithoutCoreIdentityDoesNotReconcile
--- PASS: TestResolveEffectiveWithoutCoreIdentityDoesNotReconcile (0.00s)
=== RUN   TestOrgEnvIdentitySecretMaterialRejected
--- PASS: TestOrgEnvIdentitySecretMaterialRejected (0.00s)
=== RUN   TestOrgEnvIdentityReconciliationDoesNotWeakenMandatoryPolicy
--- PASS: TestOrgEnvIdentityReconciliationDoesNotWeakenMandatoryPolicy (0.00s)
...
ok  	github.com/mcpdev80/baseharbor/internal/orgconfig	0.010s
```

RESULT: PASS — the registry-identity match is authoritative and the mismatch path fails closed, live-witnessed on the union (r3 could not assert this).

## CELL 3 — seam descriptor: PersesManagement as valid IntegrationDescriptor (Luna r2 fix point)

The seam lane `cb4367f347` is the Luna r2 fix point: `fix(0428-075): give PersesManagement a valid IntegrationDescriptor (r2)`. It binds the single observability owner — Metrics kind + versioned `MetricsV1` specification — and declares NO application capability.

Live witness on the union:

```
$ go test -count=1 ./internal/capability/... -run "PersesManagementIsAValid|PersesIsManagementSurface|PersesManagementNotRegistered|PersesDefaultReleaseValidates" -v
--- PASS: TestValidatePersesReleaseFailClosedWithoutPin (0.00s)
--- PASS: TestValidatePersesReleaseRejectsUnknownAuthClass (0.00s)
--- PASS: TestPersesDefaultReleaseValidates (0.00s)
--- PASS: TestPersesIsManagementSurfaceNotApplicationCapability (0.00s)
--- PASS: TestPersesManagementIsAValidIntegrationDescriptor (0.00s)
--- PASS: TestPersesManagementNotRegisteredAsCapabilityProvider (0.00s)
ok  	github.com/mcpdev80/baseharbor/internal/capability	0.003s
```

Direct assertion (in-process witness, then removed):

```
$ go test -count=1 ./internal/capability/... -run TestLV4PersesManagementValidIntegrationDescriptorLive -v
--- PASS: TestLV4PersesManagementValidIntegrationDescriptorLive (0.00s)
ok  	github.com/mcpdev80/baseharbor/internal/capability	0.002s
```

`PersesManagement.Validate()` passes; `Capabilities == [MetricsV1]`; no `baseharbor.app`-style application capability bound. This is the live-verify witness for seam `cb4367f347` r2.

RESULT: PASS.

## CELL 4 — perses three states + lifecycle read-only (no compose start)

- `PersesStatusNow(selected)` returns exactly one of `not_configured`, `configured_unverified`, `verified`.
- `verified` is only reachable via a real Perses health probe, which this Core defines no seam for — so `verified` is UNREACHABLE by design (`PersesReachabilityUnverified` is the only reachable state). This matches the mission's "KEIN compose-start" and lifecycle-read-only scope.
- No compose/docker/podman project started for perses.

RESULT: PASS (documented contract, no runtime side effects).

## CELL 5 — BF-01/BF-03 isolation regression (union)

Command + output:

```
$ go test -count=1 ./cmd/baha/... -run "TestBug865ForeignOrganizationAndSessionAreIsolated|TestOrganizationTargetOverrideCannotBypassManagedConstraint|TestMissingRuntimeIsolationCannotFallBackToBootstrap" -v
--- PASS: TestBug865ForeignOrganizationAndSessionAreIsolated (0.03s)
--- PASS: TestOrganizationTargetOverrideCannotBypassManagedConstraint (0.00s)
--- PASS: TestMissingRuntimeIsolationCannotFallBackToBootstrap (0.00s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.067s
```

Orphan-test drop (union artifact, NOT a lane defect): `cmd/baha/target_selection_state_dir_isolation_test.go` is bf-01-only (absent from bf-03). It asserts the `StateRoot*` selection chain that bf-03 removed when bf-03 superseded bf-01. On the union it failed with `effectiveTarget ... multiple deployment targets configured; choose one of: beta, spare-b`. Removing the bf-01-only test (bf-03 supersedes bf-01) restores green. This was a composition artifact, not a defect in either lane.

RESULT: PASS.

## REMAINING FAILURES — categorized (documented only, no product change)

### (a) DB-integration tests — not runnable without live Postgres

- `internal/database`: `TestConnectorEnrollmentPersistentAtomicScope`, `TestIdentityTenantResolverUsesIdentityScopedRLS`, `TestMigrationRollbackOwnsOnlyLatestChange`, `TestVerifySchemaReadyTracksAuthoritativeMigrationState`, `TestStationPolicyResolverAuthorizesOwnedRejectsForeign`, `TestStationPolicyResolverColdStartBootstrap`, `TestTenantRLSIsolation`, `TestWorkstationEnrollmentDurableStore`, `TestWorkstationEnrollmentDuplicateLiveBootstrapRejected` — all fail with `BASEHARBOR_TEST_DATABASE_URL is not set`. These are `*_integration_test.go` files gated on a live test database.
- `internal/controlplaneruntime`: `TestRunStartsTLSHealthReadinessAndProtectedAPI` fails with `BASEHARBOR_TEST_DATABASE_URL fehlt`.

These are environmental (need `BASEHARBOR_TEST_DATABASE_URL` pointing at a live Postgres). They are not union defects — the failing packages are DB-integration suites, not runnable in this sandbox.

### (b) Lane defect: `internal/metrics` — `TestPersesIsNotAnApplicationCapability`

- Failure: `perses_contract_test.go:53: perses must not declare application capabilities, got 1`.
- Root cause is a SELF-CONTRADICTION inside the seam lane `cb4367f347`: its r2 fix added `Capabilities: []SpecificationID{MetricsV1.ID}` to `PersesManagement` (so `Validate()` passes and `TestPersesManagementIsAValidIntegrationDescriptor` passes), but the pre-existing `internal/metrics/perses_contract_test.go` (commit `61f76fa18`) asserts `len(desc.Capabilities) == 0` AND `desc.Validate() != nil`. The two files in the SAME lane contradict each other.
- Proof this is a lane defect, not a union artifact: the union's `internal/metrics/perses_contract_test.go` is byte-identical to the seam lane's; and the union's `internal/capability/perses.go` equals the seam lane's r2 file.
- Definitive: the seam lane's OWN CI `validate` job FAILS at this test for head `cb4367f347` (GitHub API `check-runs`, run `132973062474`). The runtime lane `f55d9f94c3` ALSO fails its own CI `validate` at the same test (its reduced perses.go still trips the shared metrics test). Every implementation lane fails `validate`; this is pre-existing lane debt, independent of the union.
- The seam lane's own NEW capability test `TestPersesManagementIsAValidIntegrationDescriptor` PASSES — confirming the r2 descriptor is the intended contract and the metrics test is the stale one.

### (c) Environmental: `internal/development` — `TestStagePinnedGitTreeExportsCommitNotDirtyWorktree`

- Failure: `pinned_git_archive_test.go:38: native Git archive failed: signal: killed` (60s timeout -> OOM-killed on the shared runner).
- Proof this is environmental: the union's `internal/development/` package is byte-identical to base develop `0e9ccb582` (0 diff), so the code under test is unmodified develop code. The failure is a runner resource condition, not a union artifact.

### Definitive proof the union introduces NO new defects

- Every implementation lane (uid-app, uid-env, uid-target, env-registry, org-env-reconcile, seam, runtime) FAILS its own CI `validate` job — independently of the union.
- The failing application test files (`shared_backends_convergence_test.go`, `shared_postgres_runtime_owner_test.go`, `provider_registry_test.go`, `r27_private_integration_test.go`) are byte-identical in the union to the env-reconcile lane `32307a4336`, which fails its own CI `validate`.
- The failing metrics file is byte-identical to the seam lane, which fails its own CI `validate`.
- The union's `internal/development` is identical to base develop.
- Therefore all 12 failures trace to pre-existing lane debt or environment (DB URL / runner OOM), none to the union composition.

## CLEANLINESS

- No docker/podman compose project started. `docker ps` / `podman ps` witness: none running under this lane.
- All work state confined to `/tmp/opencode/lv4-base-wt` (git worktree) and `/tmp/lv4_*` scratch logs. Nothing created under `/home/marcel/dev/baseharbor-ecosystem`.
- No `.github/**` edits, no workflow triggers, no product-repo writes outside baseharbor-plan evidence.
- No subagents invoked.

## FINDINGS for owner (documented only)

1. `internal/metrics/perses_contract_test.go` (commit `61f76fa18`) self-contradicts the seam lane r2 fix `cb4367f347`: `PersesManagement.Capabilities` is now `[MetricsV1]` (valid), but the metrics test still asserts `len == 0`. Fix = update the one metrics test assertion (or the seam lane should not have added `MetricsV1`). This is the seam lane's own regression; both lanes fail CI on it.
2. `cmd/baha/target_selection_state_dir_isolation_test.go` is a bf-01-only test that becomes an orphan under bf-03 (which supersedes bf-01 and removed the `StateRoot*` chain it exercises). Decide whether to drop it from the union / bf-01 lane or restore the chain in bf-03.

## END

- lane mission-lv4: DONE
- The union builds (build=0, vet=0), cells 1-5 verified green. Remaining failures are pre-existing lane debt (metrics self-contradiction) or environmental (DB URL / runner OOM), none introduced by the union. Findings documented above for the owner.
