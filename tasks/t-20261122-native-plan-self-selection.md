---
id: t-20261122-native-plan-self-selection
card_number: "0428-235"
card_short_title: "catalog and planner"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
tags: [#task, #release/v0.4-28]
kanban_status: planned
kanban_lane: ready
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-235 · catalog and planner
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

- [ ] t-20261122-native-plan-self-selection · CI: catalog and planner self-change selects zero gates #task #release/v0-4-28 #status/planned #view/ready #kind/task
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


- **Test binding (select exactly one):**  normal (auto-discovered)   contract  add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR   new check  update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
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

## Finding (2026-11-22, from the PR #1756 hop)

Head `ebb6c9434a6` (run `44992226702`, 0 failed) emitted `PR  Native gate plan` job `137115562373` with
matrix `{"include":[]}`. The candidate changes exactly four catalog/planner files
(`scripts/ci-native-pr-gate.sh`, `scripts/pr-gate-coverage.json`, `scripts/test_pre_release_runtime_reuse.py`,
  `scripts/validate-pr-gate-coverage.py`) and none of those paths has a `components` row - neither in base
`c463edf87ee` nor in the head - so path->gate selection picks nothing and `PR  Selected Runtime`
(`137115617859`) plus `PR  Native  matrix` (`137115597380`) stay skipped. Consequence: edits to the admission
machinery itself carry no native gate evidence.

Missing: catalog rows whose `affected_sources` cover those four paths plus `scripts/pr-gate-plan.py` and
`scripts/pr-native-gate-plan.py`, mapped to the validation/coverage gates.

Scope note: `scripts/**` is Owner scope (card 0428-209); a worker may only implement this after the Owner
unblocks the path. Analysis witness:
`evidence/r28-welle5-2026-11-22/gate-admission-census/hop-develop-c463edf8-w223.md`.
