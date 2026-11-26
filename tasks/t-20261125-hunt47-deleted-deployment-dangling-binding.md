---
id: t-20261125-hunt47-deleted-deployment-dangling-binding
card_number: "0428-350"
card_short_title: "clean bindings of deleted apps"
type: bug
areas: [cli, deployment]
release: v0.4.28
version: ""
parent: ""
owner: w193-0428-224-hunt-v47-intake
kanban_status: planned
kanban_lane: ready
kanban_summary: "Removing a deployment removes its provider bindings and unreferenced managed instances, so provider-registry.json cannot…"
kanban_title: 0428-350 · clean bindings of deleted apps
priority: low
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/blob/develop/internal/capability/registry.go
---

- [ ] t-20261125-hunt47-deleted-deployment-dangling-binding · 0428 hunt H-V47: provider-registry bindings of deleted deployments are never collected (Validate-perpetuating garbage) #task #release/v0-4-28 #status/planned #view/ready #area/cli #area/deployment #kind/bug
    <!-- generated:card -->
    **Owner:** w193-0428-224-hunt-v47-intake · **Priority:** low  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/develop/internal/capability/registry.go)  
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

Removing a deployment removes its provider bindings and unreferenced managed instances, so `provider-registry.json` cannot accumulate state that only a hand edit can clean.

## Scope

- In scope:
  - `internal/capability/registry.go:365-392` release/prune logic: managed SHARED instances are pruned only when zero bindings reference them — but the prune runs inside `releaseDeployment`, which first filters `r.Bindings` for the target `applicationID`; for a DELETED application whose bindings still name it, `ReleaseApplicationDeployment(deletedID, env)` + reconcile (`releaseManagedBindingsPreservingInstances`, internal/application/provider_registry.go:68-75, called with the deleted identity) leaves the bindings only if no code path projects them away. Intake probe result: the develop code DOES drop stale bindings for the released identity and prunes the unreferenced shared instance, i.e. the normal destroy path is clean — the residue case is when reconcile NEVER RUNS again for that identity (destroy interrupted before provider release): the bindings keep the old application_id, `Validate` (registry.go:419 requires UUID, satisfied) keeps passing, and every later listing/plan path loads a registry describing deployments that do not exist.
  - Add binding garbage collection to the reconciliation seam itself (drop bindings whose `ProviderInstanceID` references no instance, and bindings whose deployment identity has no record on the Target, verified against `ListDeployments`), instead of only during app-scoped release.
- Out of scope:
  - v1 file migration (0428-341); destroy-all disclosure (0428-343).

## Acceptance

- A registry fixture holding a binding for a deployment that no longer exists (plus one referencing a missing instance) reconciles clean in one pass without any lifecycle event; a binding whose instance still exists but is referenced by no deployment is retained only while its deployment exists (no behavior change for live apps).
- `baha app list`/plan paths never surface provider capacity owned by removed deployments; regression asserts the GC in `internal/application`.

## Required checks

- **Modified features:** `internal/application/provider_registry_test.go` suites (binding isolation, legacy migration) stay green.
- **New tests:** `TestReconcileGarbageCollectsDanglingBindings` (package internal/application); auto-discovered unit lane.
- **CI integration and mapping:** no `.github/**` change.
- **Mapping selection proof:** plan artifact.
- **Hard acceptance gate:** SHA -> test ID -> gate -> run URL.

## Dependencies and file ownership

- Owned files or areas: `internal/capability/registry.go` (prune semantics), `internal/application/provider_registry.go` (reconcile seam).
- Shared files: reconcile seam also touched by 0428-341 — order via depends edges when both open.

## Handoff

- Cast from hunt H-V47 intake (akte `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/`, origin/main 59a288736, anchor develop 99d9ddebc) as a NEW row BF-47-11 discovered during the BF-47-1 fixture probe at intake: `Register()` on a registry whose bindings already reference the instance does not dedupe, and `releaseDeployment` prunes instances only for the released application — the dangling-binding case above was reproduced live while probing the v1 revive path (the post-reconcile registry retained a binding whose instance was pruned in the interrupted-release variant). Severity low: garbage grows only after interrupted destroys, no data loss.
- Current state, branch, PR and evidence links. Newest first.
