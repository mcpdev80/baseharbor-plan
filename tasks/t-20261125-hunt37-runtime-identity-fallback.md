---
id: t-20261125-hunt37-runtime-identity-fallback
card_number: "0428-307"
card_short_title: "runtime-identity fallback"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-307 · runtime-identity fallback
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261125-hunt37-runtime-identity-fallback · 0428 hunt H-V37: runtime-identity fallback silently downgrades to shared legacy app token (medium) #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Remove the shared legacy app-token fallback for broker-consuming services that lack an explicit runtime permission. Each service must use an explicit, authorized runtime identity scoped to its own application/service.

## Scope

- In scope: the broker identity selection/fallback path and focused identity authorization tests.
- Out of scope: changing candidate consent rules, adding a new identity store, or broad authorization redesign.

## Acceptance

- A missing per-service runtime identity fails closed; it never falls back to a shared legacy app token.
- A valid explicit identity remains scoped to its authorized service/application and cannot access a sibling service.
- Errors explain the missing authorization without exposing token values or secret material.
- Add focused positive and negative regressions, including the prior fallback case; bind them to the existing package/gate that actually runs them.
- Preserve all existing consent and operator-authorization checks.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.


## Owner decision — 2026-11-25

Remove the shared legacy app-token fallback. Require an explicit, narrowly scoped runtime identity; do not retain an implicit compatibility fallback.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Task

Cast from hunt H-V37 (akte plan main 687af1678, evidence/r28-welle6-2026-11-26/bughunt-hv37-compose-identity/): H-V37-D (MEDIUM) - broker-consuming services WITHOUT explicit runtime permission silently fall back to the SHARED legacy app token instead of a per-service runtime identity. Fail-closed or explicit consented fallback per secure-by-design; product-adjacent to consent surfaces - implementation must NOT weaken consent checks; add regression proving per-service scoping.
