---
id: t-20261125-hunt47-keycloak-migration-docs
card_number: "0428-357"
card_short_title: "keycloak migration docs"
type: bug
areas: [docs, cli]
release: v0.4.28
version: ""
parent: ""
owner: w193-0428-224-hunt-v47-intake
kanban_status: planned
kanban_lane: ready
kanban_summary: "The upgrade surface states plainly which provider transitions are supported, so a release that bumps the Keycloak pin does not…"
kanban_title: 0428-357 · keycloak migration docs
priority: low
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/blob/develop/internal/providerupgrade/keycloak/native_ops.go
---

- [ ] t-20261125-hunt47-keycloak-migration-docs · 0428 hunt H-V47: managed Keycloak pin upgrades beyond the single reviewed 26.7.5→26.8.0 path are unsupported but undocumented (docs-accuracy bug) #task #release/v0-4-28 #status/planned #view/ready #area/cli #area/docs #kind/bug
    <!-- generated:card -->
    **Owner:** w193-0428-224-hunt-v47-intake · **Priority:** low  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/develop/internal/providerupgrade/keycloak/native_ops.go)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w193-0428-224-hunt-v47-intake  
**Priority:** low  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Summary

The upgrade surface states plainly which provider transitions are supported, so a release that bumps the Keycloak pin does not surprise operators with a fail-closed `baha update`.

## Scope

- In scope:
  - Documentation accuracy for `docs/spec/core-provider-update-v1.md` ("migration_required" is presented as a supported classification), `docs/explanation/providers.md` (line ~145 already tracks the Shared-Keycloak DB variant) and the CHANGELOG promise at line ~155 ("unsupported provider upgrade paths remain blocked" never names Identity).
  - Intake correction to BF-47-5: the Compatibility hook IS production-wired — `coreNativeRuntimeOps.keycloakUpgradePath` (cmd/baha/update_provider_binding_runtime.go:76-81, passed at update_core_native.go:176 and update_provider_binding_runtime.go:280) admits exactly `from=="26.7.5" && to=="26.8.0" && !HA` and otherwise routes to `patchProviderUpgradePath` (update_provider_binding_runtime.go:59-72), which requires a strictly-newer PATCH within the same major/minor. So "always errors without injected evidence" is false for the pinned transition; the residual, real gap is that all other reviewed evidence for Identity transitions is a hardcoded single pair. The `NativeOps.CheckUpgradePath` nil-hook refusal (internal/providerupgrade/keycloak/native_ops.go:49-53) remains as defense-in-depth.
  - Add/update a test pinning the named refusal text for an unreviewed Identity transition through `coreupdate.Build`/preflight classification (plan.go:166-167 MigrationRequired → hooks path) so the documented contract cannot silently drift.
- Out of scope:
  - Implementing a real compatibility-evidence catalog for Keycloak upgrades (separate feature card if the owner wants it); provider version message precision (0428-347).

## Acceptance

- EN+DE docs name the supported Identity transitions (today: 26.7.5→26.8.0 single; same-minor patches via the generic path) and state that `baha update` fails closed for anything else.
- A test asserts the refusal text for an unreviewed Identity transition (e.g. 26.9.0 → 26.10.0 minor, and 26.8.0 → HA) — extending the existing `TestNativeKeycloakMinorRequiresSingleOwnedMigration` family (cmd/baha/update_image_reference_test.go:36).
- `bash scripts/documentation-audit.sh` passes (EN/DE parity).

## Required checks

- **Modified features:** existing keycloak upgrade-path tests stay green.
- **New tests:** the named-refusal assertion above (package cmd/baha or internal/providerupgrade/keycloak); auto-discovered unit lane.
- **CI integration and mapping:** no `.github/**` change; docs + Go changes select the standard unit/docs lanes per pr-gate-plan mapping.
- **Mapping selection proof:** plan artifact.
- **Hard acceptance gate:** SHA -> test ID -> gate -> run URL.

## Dependencies and file ownership

- Owned files or areas: `docs/spec/core-provider-update-v1.md`, `docs/de/spec/...`, `docs/explanation/providers.md`, CHANGELOG wording, one test file in cmd/baha or internal/providerupgrade/keycloak.
- Shared files: none.

## Handoff

- Cast from hunt H-V47 (akte `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/`, origin/main 59a288736, anchor develop 99d9ddebc). BF-47-5 PARTIALLY LIVE — disposition: cast as docs-accuracy card; the akte's "structurally dead in the native build" claim is REFUTED at intake: the hook is wired with one reviewed pair (update_provider_binding_runtime.go:76-81); everything else fail-closes with an accurate-by-design refusal. The nil-hook test fixture (internal/providerupgrade/keycloak/native_ops_test.go:63) is a unit fixture, not the production site.
- Current state, branch, PR and evidence links. Newest first.
