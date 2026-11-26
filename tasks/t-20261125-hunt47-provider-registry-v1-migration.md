---
id: t-20261125-hunt47-provider-registry-v1-migration
card_number: "0428-354"
card_short_title: "migrate v1 provider registry"
type: bug
areas: [cli, deployment]
release: v0.4.28
version: ""
parent: ""
owner: w193-0428-224-hunt-v47-intake
kanban_status: planned
kanban_lane: ready
kanban_summary: "An upgrade from a pre-v0.4.19 installation can reconcile its provider registry instead of dead-ending, or the release documents…"
kanban_title: 0428-354 · migrate v1 provider registry
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/blob/main/CHANGELOG.md
---

- [ ] t-20261125-hunt47-provider-registry-v1-migration · 0428 hunt H-V47: provider-registry v1 files hit a hard load wall; the documented v1→v2 migration does not exist #task #release/v0-4-28 #status/planned #view/ready #area/cli #area/deployment #kind/bug
    <!-- generated:card -->
    **Owner:** w193-0428-224-hunt-v47-intake · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/main/CHANGELOG.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w193-0428-224-hunt-v47-intake  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Summary

An upgrade from a pre-v0.4.19 installation can reconcile its provider registry instead of dead-ending, or the release documents exactly why it cannot and how the operator recovers.

## Scope

- In scope:
  - `internal/capability/registry.go`: the exact-equality version gate in `Validate` (registry.go:395-396, "unsupported provider registry version %d") plus `RegistryStore.Load` (registry.go:448-463) and `store.Update` → `s.Load()` (registry.go:473-484), which reconciliation reaches through `ReconcileReferenceProviderRegistryAt` (internal/application/provider_registry.go:85-97).
  - Either implement a v1→v2 loader migration (name-owned instances → UUID-scoped bindings; the v1 shape is verified: no `application_id` on bindings, `OwnerApplication`/`Provider`-only instances at CHANGELOG-era code `642bc6abd^`), or correct CHANGELOG.md:370 (v0.4.19 "Changed") and the upgrade docs to state that pre-v0.4.19 provider-registry files are NOT readable and name the operator recovery.
- Out of scope:
  - The deployment-record v1 wall (0428-342), the config.yaml version wall (0428-344), and the generic version-gate error-surface cleanup (0428-345) — different seams, sibling cards from the same hunt.

## Acceptance

- A regression test loads an authentic `version: 1` provider-registry.json fixture through `RegistryStore.Load` and `ReconcileReferenceProviderRegistryAt` and asserts the chosen contract (migrated successfully, or the named documented refusal with recovery text). The existing `TestProviderRegistryMigratesLegacyEnvironmentlessBindingOnReconcile` (internal/application/provider_registry_test.go:378) stays green; it only covers a within-v2 shape migration built via `capability.NewRegistry()`.
- If migration is implemented: v1 instances/bindings survive reconciliation with no silent drop — note the intake probe found that a version-number-only edit is NOT sufficient (the v1 name-owned binding fails `stableid.ValidateUUIDv4` at registry.go:419), so a real projection is required.
- CHANGELOG/upgrade documentation and the error text agree with the implemented behavior.

## Required checks

- **Modified features:** the provider-registry load/reconcile suites in `internal/capability` and `internal/application`; add the missing file-version fixture case.
- **New tests:** named fixture test (package `internal/application`, e.g. `TestProviderRegistryUpgradesV1FileOnReconcile`), normal auto-discovered Go tests in the existing packages.
- **CI integration:** no new gate needed — the affected packages run in the standard Go unit suite that every PR selects (scripts/pr-gate-plan.py path mapping for internal/** and cmd/**).
- **Mapping selection proof:** changes under internal/capability and internal/application select the Go unit lane; record the run.
- **Hard acceptance gate:** exact SHA -> test ID -> mapped check -> trigger -> run URL in handoff.

## Dependencies and file ownership

- Owned files or areas: `internal/capability/registry.go`, `internal/application/provider_registry*.go`, `docs/reference/platform-support.md` / CHANGELOG wording if the docs path is chosen.
- Shared files: none.

## Handoff

- Cast from hunt H-V47 (akte `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/` on origin/main 59a288736, anchor develop 99d9ddebc). BF-47-1 LIVE at intake, reproduced three ways at 99d9ddebc:
  - CLI: v0.4.18 binary (`app init` on a real v1 store) then develop-tip `baha app init --yes` → `Error: validate provider registry: unsupported provider registry version 1`; the file stays v1 (no reconcile-write).
  - Unit probe: writing the v1 fixture and calling `ReconcileReferenceProviderRegistryAt` → same wall; version-bumping only the number → `provider binding: application id "" must be a UUIDv4` (registry.go:419), i.e. the CHANGELOG's "migrate during reconciliation" cannot happen even with the gate relaxed naively.
  - The CHANGELOG sentence exists verbatim in BOTH v0.4.18 (line 52) and v0.4.19 (line 89) — it promised a migration that `642bc6abd` never shipped (grep: no migrate path in internal/capability at v0.4.19 or develop tip).
- Current state, branch, PR and evidence links. Newest first.
