---
id: t-20261116-i18n-demo-consumer-rename
card_number: "0428-099"
card_short_title: "match renamed Warning marker"
type: task
areas: []
release: v0.4.28
version: ""
parent: v0.4.28
owner: coord
kanban_status: review
kanban_lane: review
kanban_summary: "baseharbor-demo/tests/guided/drive.py:431-432 (and 507-508, 203, newedithelperstest.py:190 per lane finding) still match the…"
kanban_title: 0428-099 · match renamed Warning marker
priority: ""
depends_on: [t-20261115-bughunt-d28-i18n-achtung]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor-demo#164]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261116-i18n-demo-consumer-rename · Demo: match renamed Warning marker after core 0428-093 lands #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** coord  
    **PR:** [baseharbor-demo#164](https://github.com/mcpdev80/baseharbor-demo/pull/164)  
    **Needs:** [t-20261115-bughunt-d28-i18n-achtung](t-20261115-bughunt-d28-i18n-achtung.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** v0.4.28  
**Depends on:** [t-20261115-bughunt-d28-i18n-achtung](t-20261115-bughunt-d28-i18n-achtung.md)  
**Owner:** coord  
**Priority:** not set  
**PRs:** [baseharbor-demo#164](https://github.com/mcpdev80/baseharbor-demo/pull/164)  
**Source:** 
<!-- /generated:links -->

## Goal

baseharbor-demo/tests/guided/drive.py:431-432 (and 507-508, 203, new_edit_helpers_test.py:190 per lane finding) still match the literal "Achtung:" prompt. core #1663 renames it to "Warning:" — after #1663 MERGES, the demo consumer matchers must be renamed in the same window; before the merge the demo must keep matching "Achtung:" against current core, Delivery mode: DUAL-MATCH (alternation Achtung|Warning) so the demo stays green against both pre-merge and post-merge core; no merge-window dependency remains. 0428-093 stays listed as content dep for the eventual hard switch.

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
