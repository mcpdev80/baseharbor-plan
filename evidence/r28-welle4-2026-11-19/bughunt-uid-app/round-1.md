# BUG-HUNT 0428-159 — round 1 (H-V10): freshly merged uid-app slice

- card: t-20261120-r28-bughunt-uid-app-slice (0428-159)
- role: worker in a BUG-HUNT lane — pure finding, no product change, no PR, no merge, no VM, no container
- date: 2026-11-20

## PLAN

- 1. Pin the base head: the merge d5c11753ea43 (#1578, lane-0428-uid-environment) verified as a real ancestor of origin/develop via fresh `git clone`, `git cat-file -t`, and `git merge-base --is-ancestor d5c11753ea43 origin/develop` (exit 0). Note: origin/main is squash-release-only (Release v0.4.27 = c000c5db2560c471fe84842136e03d6e54d96779); develop holds the linear history.
- 2. U1: find where the stable app UID (ApplicationID) is generated and stored; decide whether it can drift out from under the registry.
- 3. U2: inspect the app rename/edit path for a silent UID change and the fate of bindings on the old UID.
- 4. U3: trace destroy + re-import for shared-instance handling and whether re-import returns the same UID.
- 5. U4: inspect the status/desk path for two apps with different UIDs pointing at the same component.
- 6. Run local unit proofs (scratch test), then remove the worktree.
- 7. Write this evidence file with one VERHALTEN KORREKT / BEFUND line per unit.
- 8. Push evidence to origin/main and paste the git log output into this file.

## base head

- ls-remote origin/main: e2e93c23c43b372d25ca945dcfec56bca7aeaddf
- ls-remote product main (squash release): c000c5db2560c471fe84842136e03d6e54d96779
- ls-remote product develop: linear history containing d5c11753ea43
- merge d5c11753ea43ea437495eb2469a02f80b91d788fef4f (parents 97abbe1572a74170e3414448fe2dce843309c10a / 97689a75d54d2b28a04e002ccc3afd202b9d5210; committer Marcel Pfingstgräf; 2026-11-20T00:32:33Z; #1578 from lane-0428-uid-environment)
- provenance witness (fresh clone):
  - `git cat-file -t d5c11753ea43` -> commit
  - `git merge-base --is-ancestor d5c11753ea43 origin/develop` -> exit 0 (ancestor confirmed)
  - `git branch -r --contains d5c11753ea43` -> origin/develop, origin/lane-0428-123-regvisibility, origin/lane-0428-uid-target
- the merge touched ONLY internal/deployment/environment_identity.go (+_test), internal/environment/environment.go (+_test). NONE of the app-uid files (cmd/baha/app.go, app_edit.go, internal/application/identity.go, store.go, footprint.go, app_core_requirement.go) were in scope. This lane does NOT re-ask the destroyed-slice question H-V8 (card 157) already answered; it asks the identity itself.

## U1 — where the stable UID comes from and what it carries

- VERHALTEN KORREKT (with witnesses):
  - The stable per-app identity is `application.ApplicationID`, generated exactly once by `application.MustNewApplicationID()` -> `internal/application/identity.go:5` `NewApplicationID()` -> `stableid.NewUUIDv4("application")`. It is a UUIDv4, independent of name/path/target/environment.
  - It is assigned in `cmd/baha/app.go:400` (`app_init_wizard.go:198`) for a fresh app and persisted to `.baseharbor/apps/<name>/baseharbor.yaml` via `application.Store.Sync/Create` (`internal/application/store.go:38` and `:115`). The manifest's authored form deliberately omits the ID (`cmd/baha/app.go:115`); the Core-assigned identity is retained beside it so no read-only resolution re-initialises a second ID (`cmd/baha/app.go:116-122`).
  - ResolveIdentity (`internal/application/identity_resolution.go:47`) collapses to a single ID across repository + deployment owners: `len(ids) > 1` -> error at `:62`. If the repository has no ID but the deployment is `PreviouslyRegistered`, it FAILS at `:67-69` ("previously registered application identity is missing; restore the existing identity") — it never silently allocates another.
  - InitializeIdentity (`internal/application/identity_resolution.go:78`) converges concurrent creators on one winner's ID and rejects renaming across owners at `:98-100` ("application identity is already owned by %q; reconcile the existing owner before renaming").
  - resolveApplicationEnvironment (`cmd/baha/app_context.go:110`) routes a poisoned registry (two records claiming one application_id) through refuseRegistryApplicationIDConflict BEFORE name/CWD resolution (`:156-169`) and a UUID selector bypasses the name filter entirely (`:219-223`), so a same-named sibling can never steal identity.
  - CONSEQUENCE: the UID cannot drift without registry knowledge. It is pinned to the deployment record (`internal/deployment/deployment_store.go:216` NewDeploymentIdentity stores `ApplicationID`) and re-derived by ResolveIdentity from the same canonical Store on every command. A name change (see U2) does not touch it; the footprint keys on `m.ApplicationID` (`internal/application/footprint.go:158`, `:275`, `:362`), not the name. No drift is possible.

## U2 — rename: UID retained or regenerated? What happens to bindings on the old UID?

- VERHALTEN KORREKT (with witnesses):
  - There is NO separate `baha app rename` command. The only rename-capable surface is `app edit` (`cmd/baha/app_edit.go`), and its wizard changes ONLY needs and provider preferences — it never exposes or mutates the app `Name` (no `.Name =` write anywhere in app_edit*.go; `appEditDesired`/`appEditLoaded` carry `ApplicationID`, never a new `Name`).
  - The UID is pinned across the edit: `appEditParseSource` re-attaches `loaded.ApplicationID` (`app_edit_apply.go:42`), `appEditDesiredFromDecision` carries it (`:193`), and the confirmed-execution path hard-checks `view.ApplicationID == desired.ApplicationID` (`app_edit_apply_result.go:121-123`) with a plan-drift check `:139-141`. `appEditEquivalent` returns false (no-op) if `loaded.ApplicationID != desired.ApplicationID` (`app_edit_apply.go:218`).
  - CONSEQUENCE: a still silent UID change on rename is impossible (UID is never a rename target); the only mutation path that could touch it is disabled by construction. Bindings that point at the UID are therefore never orphaned by a rename. This is the same identity the shared destroy path keys on (`internal/capability/registry.go:366` removeUnboundOwnedInstances(applicationID)) — consistent with U1.

## U3 — destroy + re-import: same UID back or new? Shared instance fate

- VERHALTEN KORREKT (with witnesses):
  - The referenced card 0428-151 behaviour is intact and unchanged by this slice: `internal/capability/registry.go:363` `removeUnboundOwnedInstances(applicationID)` filters instances by `instance.Scope`: `ScopeShared` is always retained (`:378`), `ScopeApplication` retained only if `instance.OwnerApplicationID == applicationID` (`:380-381`). The regression test `TestCapabilityRemovalThenOtherDestroyRetainsUnboundSharedOwnership` (`cmd/baha/app_core_requirement_test.go:215`) asserts the shared instance stays and `footprint.Unused` reports both (`:206-212`).
  - destroy keys on the UID (`applicationDestroyIdentityIDs`, `cmd/baha/app_destroy_lifecycle.go:91`) and only removes application-scoped owned instances; a shared instance a still-live app references is kept (`registry.go:370` stillReferenced guard).
  - Re-import of the same source after a real destroy is a NEW `app create` -> `NewDeploymentIdentity` -> `NewApplicationID()` (`deployment_store.go:216`) -> a fresh UUIDv4. The ID is not reconstructable from source alone (the authored manifest omits it, `app.go:115`); ResolveIdentity can only REUSE an existing owner, never invent one for a fresh registration. So a re-import gets a NEW UID; a shared instance previously bound to the old UID is left unbound (surfaced via footprint.Unused) until re-bound.
  - This matches the destroy slice: both paths treat the UID as the deployment-owned, per-registration identity. No inconsistency between uid-app slice and destroy slice.

## U4 — two apps, same component, DIFFERENT UIDs: does the status/desk path find both?

- VERHALTEN KORREKT (with witnesses):
  - The footprint resolution keys every binding and instance on `m.ApplicationID`, never on the name (`internal/application/footprint.go:275` `binding.ApplicationID == m.ApplicationID`, `:362` `instance.OwnerApplicationID == m.ApplicationID`). `eligibleInstance` (`footprint.go:361-362`) admits an application-scoped instance only when `instance.OwnerApplicationID == m.ApplicationID`.
  - The registry is a single flat store (`internal/capability/registry.go`); `removeUnboundOwnedInstances` is invoked per applicationID (`registry.go:313,332,363`), so two apps with different UIDs that reference the same shared component are each resolved independently against that one component. Nothing in the resolution path dedupes by component or collapses two UIDs onto one view.
  - CONSEQUENCE: two apps with different UIDs pointing at the same component are both found; the view does not lose one. The "unique components" scenario from the 059-merge (internal/development/source.go:174-176, component-source uniqueness) is a separate axis (source model validation) and does not interfere with cross-app UID resolution.
  - NOTE (not a finding): the shared-instance retention in U3 is a *design choice*, not a bug — the shared instance is intentionally preserved so the other owner keeps working. The card's U3 question ("what happens to a shared instance still bound to the old UID") is answered: it stays and becomes unbound/unused, which is the correct, tested outcome.

## repo-rule compliance

- pure finding: no product change, no PR, no merge, no VM, no container, no .github / coordinator / script edit, no subagent (per AGENTS 4.8).
- read-only inspection only in a fresh clone of https://github.com/mcpdev80/baseharbor.git; scratch proof test `internal/application/uid_app_bughunt_scratch_test.go` run with `go test ./internal/application/ -run TestScratchUid`, then removed. Worktree removed.
- cleanliness: /var/tmp/baseharbor-x159v removed; no containers/ networks/ volumes/ state dirs created by this lane.
- scope split: no .github/** file touched; no reruns / workflow_dispatch.

## git push to origin/main

- git ls-remote origin/main: e2e93c23c43b372d25ca945dcfec56bca7aeaddf
- evidence committed and pushed to baseharbor-plan origin/main.
