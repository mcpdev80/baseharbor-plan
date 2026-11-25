---
id: t-20261125-hunt37-cross-perm-dup
card_number: "0428-308"
card_short_title: "cross-capability service grants"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: "Distinct capability grants may name the same service; service identity is deduplicated per workload component."
kanban_title: 0428-308 · cross-capability service grants
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/application/manifest_validation.go","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/application/runtime_identity_workload.go"]
---

- [x] t-20261125-hunt37-cross-perm-dup · 0428 hunt H-V37: cross-permission service duplication is not a defect #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/application/manifest_validation.go) · [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/application/runtime_identity_workload.go)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

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

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Task

Cast from hunt H-V37: H-V37-A (LOW) - duplicate service entries across permissions are not rejected; add validation + test.

## Audit disposition — DROP

Rechecked BaseHarbor `develop` at `3a2ae6b1139570c98b8924e3b19975c56a289400`. Runtime permissions are separate capability grants; the current validator rejects a duplicate capability and a repeated service within one grant, while allowing the same workload service to receive different capabilities. `RuntimeAuthorizedServices` then intentionally deduplicates service names into one stable per-service runtime identity. Treating a cross-capability repeat as a duplicate would prevent a service from combining distinct grants, and the hunt provides no evidence that this is an authorization leak or invalid state. Drop this low-severity optional proposal; preserve the original H-V37 record above and make no product change.

Current evidence: [capability-scoped manifest validation](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/application/manifest_validation.go), [per-service identity projection](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/application/runtime_identity_workload.go), [manifest permission tests](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/application/manifest_test.go).
