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
2. ✅ CLAIM `t-20261018-r27-state-owner` (commit+push plan) — see commit below.
3. ✅ Map owner-keying: confirmed no installation_id binding on load; predecessor fixes StateOwner=LocalOwner.
4. ✅ Implement `VerifyDeploymentOwner(targetName, targetRoot, deploymentID)` seam → `VerifyDeploymentOwnerPaths(targetRoot, deploymentDir)`.
5. ✅ Positive + negative regression tests (two isolated homes, foreign/missing installation).
6. ⏳ `go build ./...` + affected packages green; run cmd/baha suite, fix order-isolation breakage.
7. ⏳ Push branch, open PR → develop with `STACKED on #1326`.
8. ⏳ Handoff `END_CODE_READY` with head SHA.

## IST-SHA

- Base: `63573ee5` (r27 authority-contract doc-fix, stacked on #1326 candidate #1326).
- Worktree branch: `work/r27-state-owner`.
- Remote `origin/main` = `45cfb97a`, `origin/develop` = `0bbab29b`.

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
- Fired at the two `resolveApplication` sites in `cmd/baha/app_context.go` where
  `targetRuntimeStateRoot` (the installation root) is available.

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
