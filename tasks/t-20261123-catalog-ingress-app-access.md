---
id: t-20261123-catalog-ingress-app-access
card_number: "0428-254"
card_short_title: "register cmd/baha/app_access"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "One develop-only catalog PR registers cmd/baha/appaccess.go and cmd/baha/appaccesstest.go in the trusted BASE so #1620…"
kanban_title: 0428-254 · register cmd/baha/app_access
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

- [ ] t-20261123-catalog-ingress-app-access · Catalog ingress 2: register cmd/baha/app_access source rows in base #task #release/v0-4-28 #status/planned #view/ready #kind/task
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

One develop-only catalog PR registers cmd/baha/app_access.go and cmd/baha/app_access_test.go in the trusted BASE so #1620 (per-reveal audit, 0428-067) can pass Trusted Plan; same mechanism and shape as the merged ingress #1790 (card t-20261123-catalog-ingress-develop-prereqs).

## Scope (owner-coordinated 2026-11-23)
- In scope: scripts/pr-gate-coverage.json only; two component rows for paths that already exist at the base: cmd/baha/app_access.go and cmd/baha/app_access_test.go; surfaces = the same two atomic docker+podman data-capabilities surfaces used by the analogues cmd/baha/app_env_test.go and cmd/baha/target_runtime_access_provider_test.go (both listed by Owner as consistency anchors; 0428-067 acceptance covers per-reveal consent/permission paths exercised inside those data-capability gates).
- In scope: runtime_specific=true mirrors the provider-test analogue; the executing lane records the flag decision per line against the analogues in its evidence.
- Out of scope: any product code; .github; any other catalog rows; re-running #1620 before this PR merges.

## Acceptance

- Trusted Plan on this PR is green (catalog-only diff, no product source changed); validator reports no duplicate id/path; release field stays v0.4.27.
- After merge, #1620 re-hops onto the new tip and its exact run passes Trusted Plan and PR Selected Checks with no branch-side catalog edit.

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
