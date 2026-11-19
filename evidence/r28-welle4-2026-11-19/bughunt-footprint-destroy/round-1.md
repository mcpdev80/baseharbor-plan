# Bug Hunt H-V8 — destroy/retirement vs `footprint.Unused` view

- Shift: r28-welle4-2026-11-19
- Lane: x-157h
- Role: hunt-worker (pure finding, no product change, no PR, no commit on baseharbor, no container/VM)
- Base measured: `4b3a3559070e9b81b1886a357f6a46bc6dfce790` (origin/develop)
- Worktree: /var/tmp/baseharbor-x157h (fresh git clone against https://github.com/mcpdev80/baseharbor.git)

## Scope

The view `footprint.Unused` (internal/application/footprint.go:345-347) lists an
instance when `!selected[instance.ID] && len(bindingsForProviderInstance)==0`.
This hunt inspects the destroy/retirement paths against that view for two defect
classes: (a) an orphan that stays in the registry though no binding/selection
carries it (the "double-view" case — remains in `Unused` though it should have
gone), and (b) an instance already gone from the registry that `Unused` would
still show (the "invisible" case). The removen itself is out of scope; only the
sicht is under review.

## PLAN (numbered)

- Measure base: `git ls-remote origin refs/heads/develop` => `4b3a3559070e9b81b1886a357f6a46bc6dfce790`; clone to /var/tmp; `git log -1 --format=%H` confirmed same SHA. go.mod pins `go 1.25.0` / toolchain go1.26.9; host go 1.26.8.
- Enumerate all write-modifying paths that change provider instances/bindings:
  - `func (Registry|Instances|Bindings)` on Registry: none in non-test code (the Registry accessors live in internal/capability/registry.go; the grep for that exact signature in registry.go+internal/application/*.go returned no match — the mutating methods are `Register`/`UnregisterExternal`/`Release*`/`removeUnboundOwnedInstances`).
  - Register/Unregister/Release/removeUnbound/Reconcile in internal/application + internal/capability:
    - internal/capability/registry.go:63 Register, :174 UnregisterExternal, :296 ReleaseManagedApplication, :313 removeUnboundOwnedInstances (via ReleaseManagedApplication), :316 ReleaseManagedDeployment, :320 ReleaseApplication, :332 removeUnboundOwnedInstances (via ReleaseApplication), :335 ReleaseApplicationDeployment, :366 removeUnboundOwnedInstances, :262 ApplicationLifecycle (builds destroy actions).
    - internal/application/provider_registry.go:73 ReleaseApplicationDeployment (reconcile), :247 ReleaseApplicationProviderRegistry (wrapper), :255 ReleaseApplicationProviderReferencesAt (wrapper), :270 ReleaseApplicationProviderRegistryAt (destroy core), :154 Register (reference providers).
    - internal/application/external_provider_scope.go:254 UnregisterExternal (external destroy).
  - The three destroy entry points and their registry effect:
    - cmd/baha/app_destroy_lifecycle.go:714 -> ReleaseApplicationProviderRegistryAt (full destroy).
    - cmd/baha/app_runtime_retirement.go:78 (never-delivered path) AND :164 (retired path) -> ReleaseApplicationProviderReferencesAt (releases deployment binding, keeps instances).
    - cmd/baha/runtime_destroy_all.go:388 -> ReleaseApplicationProviderRegistryAt (full destroy).
- Per path ask (a) orphan-remain and (b) invisible-gone (detailed below).
- Check Existing/Additional and sort stability for cross-list dupes (footprint.go:349-352).
- Check the three destroy inputs for divergent shared-state effect.
- Two go test commands (results below).
- Card: not written — owner responsibility (§3.3 point 5).

## Findings

### FUND 1 — Shared instances cannot orphan into `Unused`; shared scope is explicitly protected in every destroy path. NOT A DEFECT.

Szenario: after destroying one application, could a BaseHarbor-owned shared provider stay in the registry unbound yet still be counted by `Unused` (orphan-remain)?
ERWARTET (vertrag): shared instances are shared across applications; an app destroy must not delete a shared instance that other apps may still bind.
IST (gemessen): `removeUnboundOwnedInstances` (internal/capability/registry.go:366) keeps `instance.Ownership != OwnershipBaseHarbor` and drops only `ScopeShared` when unbound — but the production destroy core `ReleaseApplicationProviderRegistryAt` (internal/application/provider_registry.go:276) first collects all `ScopeShared` instances into `retained`, releases the deployment binding, then re-registers every shared instance. So shared instances survive a destroy and remain registered. They show in `Unused` only if they truly have no binding AND are not `selected`. That is the correct contract: a genuinely unused shared instance is reported; a shared instance still owned by the fleet is not dropped.
DATEI:ZEILE: internal/application/footprint.go:345-347 (Unused rule), internal/application/footprint.go:348 (sort.Strings(result.Unused)), internal/capability/registry.go:366-391 (removeUnboundOwnedInstances), internal/application/provider_registry.go:276-290 (ReleaseApplicationProviderRegistryAt shared guard).
WIRKUNG auf user-sicht: none. `Unused` reflects reality; no false orphan, no leaked instance.
STUFE: nicht-block.
VERHALTEN KORREKT — witness tests: TestFootprintUnusedRespectsTargetWideConsumers (internal/application/v0425_contract_test.go:379) asserts another app's shared provider is neither unused nor selected; TestRegistryReusesOneSharedProviderAcrossApplications, TestRegistryAllowsSameSharedProviderAcrossDifferentSharingBoundaries (internal/capability/registry_test.go).
Reproduce: `go test ./internal/application -count=1 -run "^TestFootprint$"; go test ./internal/capability -count=1 -run "^TestRegistry$"`.

### FUND 2 — `Unused` and `Existing` are disjoint by construction; the sort does not create a cross-list double. NOT A DEFECT.

Szenario: could a single instance appear simultaneously in `result.Unused` and `result.Existing` (or `Additional`) because both use sorted slices?
ERWARTET (vertrag): `Unused` = instances not selected and unbound; `Existing`/`Additional` = instances included in resolution (selected or a dependency root). A selected/selected-as-required instance is `selected[id]==true`, so it is excluded from `Unused` by the same guard.
IST (gemessen): footprint.go:345 guards `!selected[instance.ID]`; `selected[id]` is set in `include()` (footprint.go:243) for every instance pulled into the resolution closure, including dependency roots (footprint.go:323-326) and the extra permission/consumes intent (footprint.go:332-337). Any instance that lands in `Existing`/`Additional` was `include`d and therefore marked `selected`; it is excluded from `Unused`. The two slices are keyed on mutually exclusive predicates; sorting (footprint.go:349-352) only orders each slice alphabetically by InstanceID and cannot move an entry between slices.
DATEI:ZEILE: internal/application/footprint.go:243, 323-326, 345, 349-352.
WIRKUNG auf user-sicht: none. The report never shows the same instance twice.
STUFE: nicht-block.
VERHALTEN KORREKT — witness tests: TestFootprintUnusedRespectsTargetWideConsumers (v0425_contract_test.go:379) checks neither-unused-nor-existing for a cross-app instance; TestFootprintCorelessAndUnboundAreDifferent, TestFootprintReusesBindingAndDependencyUnion (internal/application/v0425_contract_test.go).
Reproduce: `go test ./internal/application -count=1 -run "^TestFootprint$"`.

### FUND 3 — The three destroy inputs do NOT diverge in their registry effect on owned instances. NOT A DEFECT (observation).

Szenario: do the three destroy entry points change the shared/owned instance pool differently?
ERWARTET (vertrag): all three destroy inputs for an application must converge on the same registry end-state (owned application instance removed; shared instances retained; external instances retained) so the `Unused` view is identical regardless of which entry point was taken.
IST (gemessen):
- app_destroy_lifecycle.go:714 and runtime_destroy_all.go:388 both call `ReleaseApplicationProviderRegistryAt` (provider_registry.go:270) — shared retained, owned removed, external retained (removeUnboundOwnedInstances keeps non-owner instances).
- app_runtime_retirement.go:78 (never-delivered) and :164 (retired) call `ReleaseApplicationProviderReferencesAt` (provider_registry.go:255), which releases the deployment binding but KEEPS every instance (`instances := append(...instances...); registry.Instances = instances`). This is the correct semantic difference: retirement keeps the physical instance alive (data/recovery owner retained) and only drops the reference, so the instance is NOT `Unused`. Full destroy removes the owned application instance. Two different contracts, two correct views — retirement correctly keeps an instance out of `Unused` because it still exists; full destroy removes it so `Unused` is empty. No path leaves an owned instance bound-less-but-present when it should be gone.
DATEI:ZEILE: cmd/baha/app_destroy_lifecycle.go:714, cmd/baha/app_runtime_retirement.go:78, cmd/baha/app_runtime_retirement.go:164, cmd/baha/runtime_destroy_all.go:388, internal/application/provider_registry.go:255, 270.
WIRKUNG auf user-sicht: none. `Unused` correctly reflects retired (present) vs destroyed (gone).
STUFE: nicht-block.
VERHALTEN KORREKT — witness tests: TestRuntimeRetirementReleasesOnlySelectedReferencesPreservingEveryOwner (internal/application/provider_registry_retirement_test.go:11), TestReleaseManagedApplicationPreservesExternalBinding (internal/capability/registry_test.go:224).

### FUND 4 — The production destroy core preserves external instances; the unused-external check is scoped correctly. NOT A DEFECT (observation).

Szenario: could an external instance show as `Unused` after destroy though its owner still "exists" in some sense, or be wrongly dropped?
ERWARTET (vertrag): external instances are owned by the customer, not BaseHarbor; destroy of a BaseHarbor app must not delete them, and they must not be reported as BaseHarbor-`Unused`.
IST (gemessen): removeUnboundOwnedInstances (registry.go:369-370) keeps any `instance.Ownership != OwnershipBaseHarbor` first — external instances are retained through the destroy. `ReleaseApplicationProviderRegistryAt` re-registers shared + retained external instances. `Unused` only ever iterates the registry instances and applies `!selected && unbound`; external instances are excluded from BaseHarbor ownership accounting by scope/ownership semantics elsewhere (eligibleInstance requires matching owner scope). No divergence.
DATEI:ZEILE: internal/capability/registry.go:366-391, internal/application/footprint.go:361-364 (eligibleInstance), internal/application/external_provider_scope.go:254 (external destroy path).
WIRKUNG auf user-sicht: none.
STUFE: nicht-block.
VERHALTEN KORREKT — witness tests: TestRegistryExternalProviderIsBindableButNeverLifecycleOwned (internal/capability/registry_test.go:103), TestApplicationDestroyRequiresConnectivityRelease (internal/application/connectivity_test.go:86).

## Test coverage (mission step 6)

Command 1: `go test ./internal/application -count=1 -run "^(TestFootprint|TestCapabilityRemoval|TestProviderRegistry|TestRelease)"`
Result: `ok github.com/mcpdev80/baseharbor/internal/application 0.034s` — EXIT 0.
Covers: TestFootprintBindingFixtures, TestFootprintCorelessAndUnboundAreDifferent, TestFootprintReusesBindingAndDependencyUnion, TestFootprintEvidenceValidation, TestFootprintUnusedRespectsTargetWideConsumers, TestFootprintUnprojectedDependenciesNeverClaimCoreless, TestProviderRegistryKeepsSameApplicationEnvironmentsIsolated, TestProviderRegistryMigratesLegacyEnvironmentlessBindingOnReconcile, TestReleaseSharedBackendApplicationKeepsDataWhenProtectedConsumerRecordIsMissing.

Command 2: `go test ./internal/capability -count=1 -run "^(TestRegistry|TestRemoveUnbound|TestProvider|TestExternal|TestShared)"`
Result: `ok github.com/mcpdev80/baseharbor/internal/capability 0.003s` — EXIT 0.
Covers: TestRegistryReusesOneSharedProviderAcrossApplications, TestRegistryRejectsDuplicateSharedProvider, TestRegistryApplicationProviderCannotCrossApplicationBoundary, TestRegistryExternalProviderIsBindableButNeverLifecycleOwned, TestRegistryLifecycleOwnsOnlyDedicatedManagedProvider, TestRegistryAllowsSameSharedProviderAcrossDifferentSharingBoundaries, TestRegistryRejectsDuplicateSharedProviderWithinSameSharingBoundary (and lifecycle-observer / distribution-metadata registry tests matched by `TestRegistry`).

go vet ./internal/application/ ./internal/capability/ — VET_EXIT 0.

No PANIC, no dead-lock observed in either command.

## Un-covered surface (observation, not a new defect)

The registry-level `ReleaseManagedApplication` (internal/capability/registry.go:296) and `ReleaseApplication` (internal/capability/registry.go:320) are exercised only in tests (registry_test.go:242, :254) and are NOT called from any production destroy path — the production destroy core is `ReleaseApplicationProviderRegistryAt`. This is a coverage observation for the reviewer, not a footprint.Unused defect: the paths they call (`removeUnboundOwnedInstances`) are covered by TestReleaseManagedApplicationPreservesExternalBinding and TestRegistryStorePersistsOwnerOnlyValidatedState. No product change in scope.

## Conclusion

H-V8 found no footprint.Unused defect. Every write-modifying path that changes a
provider instance or binding during destroy/retirement preserves the intended
view: shared instances are retained and correctly kept out of a false
`Unused`; `Unused` and `Existing`/`Additional` are disjoint by construction; the
three destroy entry points converge on the correct owned-instance outcome; and
external instances are retained, never reported as BaseHarbor-`Unused`. The
destroy paths are well-covered by the existing footprint, registry, and
retirement unit tests.

## KARTE: offen (an coordinator) — no findings to cast

All four inspected scenarios returned VERHALTEN KORREKT. No defect found, so no
bug card is warranted. The coverage observation (FUND 4 / un-covered surface)
is a reviewer note, not a contract violation; it stays off unless the owner
wishes to raise it.

## Cleanliness

- Worktree: /var/tmp/baseharbor-x157h (git status clean, 0 modified/untracked).
- Containers: none started.
- Networks: none created.
- Volumes: none created.
- State directories: none created (no docker/podman; unit tests use temp dirs under /tmp via t.TempDir(), auto-removed).
- Before/after list: empty on both sides (this is a pure source/unit-test lane).

## Base attestation

- Base SHA cut from: `4b3a3559070e9b81b1886a357f6a46bc6dfce790` (origin/develop).
- This lane wrote only into baseharbor-plan evidence (this file). No commit, branch, or PR on baseharbor.
