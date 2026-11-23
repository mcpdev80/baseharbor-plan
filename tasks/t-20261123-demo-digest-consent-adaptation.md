---
id: t-20261123-demo-digest-consent-adaptation
card_number: "0428-251"
card_short_title: "pass explicit candidate digest"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: Coordinator (merge 1450) / 9b7683b5
kanban_status: closed
kanban_lane: closed
kanban_summary: The baseharbor-demo footprint consent test passes with the explicit candidate digest while the product-side fail-closed Consent…
kanban_title: 0428-251 · pass explicit candidate digest
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor-demo]
prs: [mcpdev80/baseharbor#1780]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1780"]
---

- [x] t-20261123-demo-digest-consent-adaptation · Demo: pass explicit candidate digest in footprint consent test (fail-closed kept) #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** Coordinator (merge 1450) / 9b7683b5  
    **PR:** [baseharbor#1780](https://github.com/mcpdev80/baseharbor/pull/1780)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1780)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Coordinator (merge 1450) / 9b7683b5  
**Priority:** not set  
**PRs:** [baseharbor#1780](https://github.com/mcpdev80/baseharbor/pull/1780)  
**Source:** 
<!-- /generated:links -->

## Goal

The baseharbor-demo footprint consent test passes with the explicit candidate digest while the product-side fail-closed Consent validation stays untouched. Owner approved this adaptation on 2026-11-23; #1780 (core digest-consent harness, head 87ba9bac, behind develop) does NOT carry it - its write set is core-repo only.

## Scope

- In scope: baseharbor-demo test/script that currently blocks on the consent digest; adapt it to pass the explicit candidate digest; keep every fail-closed consent assertion.
- In scope: one PR in mcpdev80/baseharbor-demo per card (one PR per card rule).
- Out of scope: any baseharbor core product change; any edit of #1746/#1780 owner branches; weakening Consent validation; go.mod changes.

## Acceptance

- Demo footprint consent journey runs green in the demo repo hosted CI at one exact PR head, digest passed explicitly, fail-closed negative case still fails as designed.
- Handoff states test -> check/gate -> trigger -> execution result with exact candidate SHA.
- After this lands, #1780 is re-hopped onto current develop and re-run before its own review.

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

CLOSED: #1780 gemergt als fcccf7a205 nach delta-re-review; PR-run 45117979213 terminal success am head 4825f89c, files == 0428-241 write-set.
