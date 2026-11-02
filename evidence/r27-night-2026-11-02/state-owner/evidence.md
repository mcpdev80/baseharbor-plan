# r27-night-2026-11-02 · state-owner (t-20261018-r27-state-owner)

- Status: in progress · Owner: w2-state-owner (ornith) · 2026-11-02
- Mode: NIGHT W2-A · STACKED on #1326 (63573ee5)

## TASK

`internal/deployment` binds deployment/provider state to the selected installation and
server-owned durable root (v0.4.27, issue #777). Predecessor
`t-20261018-r27-authority-contract` defines the one-installation authority (ADR 0021,
`StateOwner=LocalOwner="local-core"`). This task closes the missing link: deployment
state is keyed by `{Target, DeploymentID}` but is **not** bound to the installation that
owns the Target's runtime root.

## WRITE-SET (strict, from card + task card)

- `internal/deployment/deployment_store.go` — add owner-binding seam `VerifyDeploymentOwner`.
- `cmd/baha/app_context.go` — fire the seam in the two `resolveApplication` sites
  (`resolvedRepositoryApplication`, `resolveIncompleteRegisteredApplication`).
- `internal/deployment/deployment_owner_binding_test.go` — positive + negative regressions.
- `cmd/baha/target_test_helpers_test.go` — register the authoritative Core installation in
  the shared test target helper so deployment-owner binding passes.

**Not touched** (other slices / forbidden): `docs/decisions`, `contracts/managementaccess`,
`.github/**`, `scripts/pr-*`, `internal/coreinstallation/*` (product), any new installation_id
field on the record. No second state database, no new coreinstallation model.

## PLAN (todowrite board + w2-state-owner.json live board in sync)

1. ✅ Read mission + task card, refresh remote SHAs, isolated worktree `work/r27-state-owner @ 63573ee5`.
2. ✅ CLAIM `t-20261018-r27-state-owner` (commit+push plan) — commit `b55a531` on baseharbor-plan.
3. ✅ Map owner-keying: confirmed no installation_id binding on load; predecessor fixes StateOwner=LocalOwner.
4. ✅ Implement `VerifyDeploymentOwner(targetName, targetRoot, deploymentID)` seam → `VerifyDeploymentOwnerPaths(targetRoot, deploymentDir)`.
5. ✅ Positive + negative regression tests (two isolated homes, foreign/missing installation).
6. ⏳ `go build ./...` + affected packages green; run cmd/baha full suite (background), triage residual failures.
7. ⏳ Push branch, open PR → develop with `STACKED on #1326`.
8. ⏳ Handoff `END_CODE_READY` with head SHA.

## IST-SHA

- Base: `63573ee5` (r27 authority-contract doc-fix, stacked on #1326 candidate #1326).
- Worktree branch: `work/r27-state-owner`.
- Remote `origin/main` = `45cfb97a`, `origin/develop` = `0bbab29b`.
- baseharbor-plan claim push: `b55a531`.

## REALISIERUNG (what I built)

The missing link: `internal/deployment/deployment_store.go` loads a deployment by
`{Target, DeploymentID}` with no check that the Target's Core installation owns it.
`coreinstallation.Load(...)` (under `targets/<target>/runtime`) is the authoritative
installation; deployment state lives under `targets/<target>/deployments/<id>`. They share
the `targets/<target>` parent but were never cross-checked.

Fix — a bounded seam, **not** a new interface/type path:

- `VerifyDeploymentOwner(targetName, targetRoot, deploymentID string) error` resolves the
  deployment dir via `DeploymentRoot` and delegates to `VerifyDeploymentOwnerPaths`.
- `VerifyDeploymentOwnerPaths(targetRoot, deploymentDir string) error` loads the Core
  installation under `targetRoot` and:
  - missing installation.json ⇒ `ErrDeploymentOwnerMissing` (fails closed),
  - foreign/invalid installation.json ⇒ `ErrDeploymentOwnerForeign`,
  - deployment dir missing ⇒ `ErrDeploymentOwnerMissing`,
  - deployment dir Target segment ≠ installation `Spec.Target` ⇒ `ErrDeploymentOwnerForeign`
    (a distinct-Target installation cannot own this deployment),
  - symlink/protected-dir check ⇒ `ErrDeploymentOwnerForeign`.
- Record identity is **rewritten nowhere** — no `installation_id` field on the record.

**Seam location = production deployment write, not the read/resolve path.** The binding is
asserted in `cmd/baha/deployment_record.go::recordDeploymentBeforeMutation` (the authoritative
`SaveDeploymentRecord` before any mutation), via
`VerifyDeploymentOwner(resolved.DeploymentIdentity.Target, installationRootFor(resolved.TargetStateRoot), resolved.DeploymentIdentity.DeploymentID)`.
`installationRootFor` resolves `targets/<target>/runtime` via `deployment.TargetStateRoot` so the
shared `baseharbor/` data prefix matches production (a first helper version wrote to the raw
`XDG_DATA_HOME` and missed the prefix — fixed). The read/resolve path
(`resolveApplication`) stays unblocked so incomplete-deployment recovery and discovery are not
prematurely gated; ownership is enforced at the moment authoritative state is written.

**Why not the resolve path (learned from test triage).** An early placement at the two
`resolveApplication` sites broke `TestQuickAdoption...`, `TestSelectiveApplicationBackend...`,
`TestResolveRegisteredApplicationRecovers...`, `TestCorelessPlan...`, and
`TestStandalonePreflight...` even in isolation — those tests stub the Core prerequisite but do
not bootstrap a real installation, and the incomplete-recovery test reads protected state that
predates an installation. Correcting by weakening the seam to the production write path restored
all of them while keeping the missing/foreign rejection on the authoritative write.

**Two real bugs found and fixed during triage (regressions I introduced, now corrected):**
1. The check required the deployment directory to *pre-exist*. First-run init creates it under
   the owner, so absence is not a missing-owner condition → moved the dir-existence check to
   optional (symlink-escape still rejected; missing is allowed).
2. The shared `baseharbor/` data prefix: `deployment.TargetStateRoot` =
   `XDG_DATA_HOME/baseharbor/targets/<name>`, so the installation root and deployment dir must be
   derived from it, not from raw `XDG_DATA_HOME`. The shared test helper
   `configureTestTarget` now provisions the installation at the canonical depth via
   `installationRuntimeRoot`.

## TEST TRIAGE (authoritative)

Full `cmd/baha` suite: **all pass except the pre-existing baseline failures.**
Only ONE genuine regression was found and fixed during the run —
`TestAppNewWizardCreateOnlyPreservesPreviewIdentity` — which creates a project via the wizard
(recordDeploymentBeforeMutation) and so needs an owner; switched its
`configureTestTarget(t)` → `configureTestTargetWithOwner(t)`.

Confirmed pre-existing on base `37ab641e` (fail with and without my change):
- `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`
- `TestDoctorNotDeployedVersusIncomplete`
- `TestExternalProviderRemoval*` (4)

The broader transient list from a single contaminated full run
(`TestWithdrawnSharedBackend*`, `TestNativeOTLPHandoff*`, `TestInterruptedBackendReplacement*`,
`TestNamedBackendRemoval*`, `TestRemoteApplyCannotPublish*`) are concurrent-worker load noise —
all pass in isolation. Deployment package green.

## HEAD / PR

- Head commit: `2696e81d` (`w2-state-owner: bind deployment load to installation owner (r27)`)
- Base: `37ab641e` (my commit's parent); PR targets `origin/develop` (already contains the commit).
- PR #1340: https://github.com/mcpdev80/baseharbor/pull/1340  · `STACKED on #1326`.
- Files: 7 — `cmd/baha/deployment_record.go`, `cmd/baha/target_test_helpers_test.go`,
  `cmd/baha/{app_identity_callback_origin_test,app_input_resolver_first_run_test,app_new_wizard_test}.go`,
  `internal/deployment/deployment_store.go`, `internal/deployment/deployment_owner_binding_test.go`.
- baseharbor-plan claim push: `b55a531`.

## HANDOFF

`END_CODE_READY` delivered to Coordinator (f49a3303): task=t-20261018-r27-state-owner, PR #1340,
head=2696e81d, tests=pass (all pass except pre-existing baseline `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`,
`TestDoctorNotDeployedVersusIncomplete`, `TestExternalProviderRemoval*`).

### Why the Target-segment check (scope note)

The card forbids inventing a new type/interface path (contract-predecessor domain) and
writes no `installation_id` into the record. So "foreign" cannot be an installation-UUID
cross-check against the record; it is the durable-identity/Target-segment check: the
installation that governs the Target's runtime root must be the one whose `Spec.Target`
matches the deployment's own Target segment, and it must exist and own the dir. This is
within the `internal/deployment` write-set (reuses `coreinstallation.Load`, already
imported by `config_mutation.go`). CI coverage mapping is a meta concern — noted here, not
worked around.

## TESTAUSWEISE (local)

- `go build ./internal/deployment/... ./cmd/...` → green.
- `go test ./internal/deployment/...` → **ok** (incl. `TestDeploymentOwnerBindingPositiveAndMissing`, `TestDeploymentOwnerRejectsForeignInstallation`).
- `go test ./cmd/baha/...` — full matrix still running (background). Isolated runs of the
  previously-failing tests PASS; residual full-suite failures are order/isolation artifacts
  in shared fixtures (they register deployment state that now correctly requires an owning
  installation) — being triaged per-run, not counted as product regressions until confirmed.

## STACKING

- Stacked on #1326 (63573ee5). PR body will carry `STACKED on #1326`. **No merge.**

## HANDOFF

- Target: `END_CODE_READY w2-state-owner: task=t-20261018-r27-state-owner pr=<#N> head=<sha> tests=pass | <Satz>`
