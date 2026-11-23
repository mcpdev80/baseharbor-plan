---
id: t-20261123-edit-toggle-ack
card_number: "0428-257"
card_short_title: "app-edit: space-toggle lacks"
type: task
areas: ["cli"]
release: v0.4.28
version: ""
parent: ""
owner: Coordinator (owner-merge + fecb delta-APPROVE) / f0f6c8b4
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: "0428-257 · app-edit: space-toggle lacks"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1801]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1801", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-23/sweep-1801/review-merge-delta.md"]
---

- [x] t-20261123-edit-toggle-ack · Bug (hunt H-P1): app-edit: space-toggle lacks on-screen acknowledgement #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** Coordinator (owner-merge + fecb delta-APPROVE) / f0f6c8b4  
    **PR:** [baseharbor#1801](https://github.com/mcpdev80/baseharbor/pull/1801)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1801), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-23/sweep-1801/review-merge-delta.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Coordinator (owner-merge + fecb delta-APPROVE) / f0f6c8b4  
**Priority:** not set  
**PRs:** [baseharbor#1801](https://github.com/mcpdev80/baseharbor/pull/1801)  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope: `cmd/baha/app_edit.go` — acknowledge the selected/deselected state after a Space toggle.
- In scope, documented post-merge extension: `cmd/baha/app_wizard_controller.go` — the two read-only selection-state accessors used by the acknowledgement path; `cmd/baha/app_edit_apply_test.go` — `TestReview918SpaceToggleAcknowledgesOnScreen` regression.
- Out of scope: changes to consent, fail-closed/provider behavior, unrelated wizard behavior, and `.github/**`.

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
%s

## Acceptance criteria
- Befund aus der H-P1-Akte reproduziert (hosted CI-Test oder dokumentierter manual-smoke als zusatz, NICHT als ersatz fuer CI-test).
- Minimaler, sicherer fix im genannten file:line-umfeld; keine nebenaenderungen.
- Neue/geaenderte tests laufen in der GitHub-CI (CI-aufnahmepflicht 5.3); keine konsent-/fail-closed-aufweichung.

## Evidence
- hunt-akte: evidence/r28-welle5-2026-11-23/hunt-hp1-f0f.md


## Post-merge scope and receipt review

The review of merged commit `b41103867e370f6588a396cb08ab0b3013e209ac` accepts the two additional paths as a documented scope extension. The controller methods only read the visible need at the cursor and its selected bit; the test file adds one regression without changing existing tests. The selection, provider, consent, and fail-closed semantics remain unchanged. No revert is required.

The regression's package receipt is run `45152943243`, job `137618621308` (`PR · Draft Go · cli-3`, pull_request trigger, source head `c3677dfa19f4aa0d0bc7ceccb51a6929b84f400c`). The `cmd/baha` package path selects the CLI unit-shard path; `TestReview918SpaceToggleAcknowledgesOnScreen` hashes to `cli-3` under the shard selector, and that job completed with `PASS cli-3: 438 passed / 16 intentionally skipped / 454 discovered; CLI inventory total=1872`. The test and implementation file blobs are unchanged through current head `ff81c5a17ba0ba6c1f784773302497771ab089d8` and merge `b41103867e370f6588a396cb08ab0b3013e209ac`. Exact-head ready run `45157306258` also passed Trusted Plan and terminal PR Selected Checks; its unit shards were skipped after the base hop, so the mapped package receipt above is the test-execution witness. See the linked review evidence for the complete mapping and remote witnesses.

CLOSED: b41103867 merged; post-merge delta APPROVE aac6fc60b. Deviation dokumentiert: +77 rein additiv, zwei dateien ueber write-set (controller +17 ack-durchreichpfad, apply_test +54) — funktional neutral befunden.
