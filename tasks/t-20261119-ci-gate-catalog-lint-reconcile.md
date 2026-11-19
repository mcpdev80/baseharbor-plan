---
id: t-20261119-ci-gate-catalog-lint-reconcile
card_number: "0428-145"
card_short_title: "reconcile catalog lint guard"
type: task
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: Codex team (current thread)
kanban_status: active
kanban_lane: active
kanban_summary: "Make the CI gate-catalog policy detect validation registration changes in existing planner, runner, and workflow files, then…"
kanban_title: 0428-145 · reconcile catalog lint guard
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1581]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261119-ci-gate-catalog-lint-reconcile · CI: reconcile catalog lint guard on current develop #task #release/v0-4-28 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Codex team (current thread)  
    **PR:** [baseharbor#1581](https://github.com/mcpdev80/baseharbor/pull/1581)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** v0.4.28  
**Depends on:** none  
**Owner:** Codex team (current thread)  
**Priority:** not set  
**PRs:** [baseharbor#1581](https://github.com/mcpdev80/baseharbor/pull/1581)  
**Source:** 
<!-- /generated:links -->

## Goal

Make the CI gate-catalog policy detect validation registration changes in existing planner, runner, and workflow files, then rebase PR #1581 onto current develop and prove both violation and non-violation cases through the existing required CI route.

## Scope

- In scope: `scripts/ci-workflow-policy.sh`; regression cases in the existing `scripts/test_pr_gate_plan.py`; rebase and repair PR #1581. Detect meaningful added/removed validation IDs and inline validation dispatch registrations in the existing PR planner, check runner, and CI workflow, including inline pre-release surfaces.
- Out of scope: new workflow files, new validation IDs/checks, changes to `scripts/pr-gate-plan.py` gate definitions or `scripts/release-requirements.json` unless a concrete required registration is discovered, unrelated CI redesign, full release/runtime qualification.

## Acceptance

- Regression tests fail when an existing planner/runner/CI dispatch registration is added or removed without required planner/catalog updates, and pass for unrelated edits and correctly co-updated catalog/planner changes.
- `bash -n`, focused regression tests, workflow policy, and the current exact-head required `PR Selected Checks` pass after rebasing onto current `develop`.
- Handoff records test → check → trigger → exact candidate SHA → actual run result. No merge based on stale CI.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):** ☒ normal (auto-discovered within existing `scripts/test_pr_gate_plan.py` unittest run).
- Tests: new/updated `WorkflowPolicyCatalogTests` cases in `scripts/test_pr_gate_plan.py`; temporary git/event fixtures exercise additions/removals and benign changes. Target `pr-planner-tests` and `ci-policy` through the existing CI planner mapping.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas: `scripts/ci-workflow-policy.sh`, `scripts/test_pr_gate_plan.py`.
- Shared files: none expected. If new planner/catalog definitions or CI workflow ownership are needed, stop and coordinate with the owner before expanding scope.

## Handoff

- Current state: #1581 is open, non-draft, unassigned, based on stale develop; independent review found a false-negative in existing-file registrations. Work starts only after this claim is published.
- Test binding route: existing unittest + `pr-planner-tests`/`ci-policy` checks, selected by changes to the owned paths.
- Newest first: branch/PR, exact head, run and findings.
