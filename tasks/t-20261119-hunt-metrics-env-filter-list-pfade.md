---
id: t-20261119-hunt-metrics-env-filter-list-pfade
card_number: "0428-121"
card_short_title: "Env-Filter wirkt nicht auf"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: mission-efilter
kanban_status: review
kanban_lane: review
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-121 · Env-Filter wirkt nicht auf
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1691]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/env-filter-fix/fix-1.md", "https://github.com/mcpdev80/baseharbor/pull/1691"]
---

- [ ] t-20261119-hunt-metrics-env-filter-list-pfade · Environment-Filter wirkt nicht auf alle list-Pfade (caller-side prefix workaround only) #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** mission-efilter  
    **PR:** [baseharbor#1691](https://github.com/mcpdev80/baseharbor/pull/1691)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/env-filter-fix/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1691)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** mission-efilter  
**Priority:** not set  
**PRs:** [baseharbor#1691](https://github.com/mcpdev80/baseharbor/pull/1691)  
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
## Befund (intake aus hunt-918)
Befund 2 (HIGH): Der Environment-Filter ist kein echter Filter: er wird caller-seitig als Prefix-Workaround implementiert und wirkt daher NICHT auf alle list-Pfade. Akzeptanz: ein zentraler filterpfad fuer ALLE list-EOFs (datei:zeile je EOF in der akte), regression je EO-Pfad mit zwei environments. Bezug: residual of closed 0428-102.
Erlaubtes write-set (vorschlag, lane prueft): internal/observability (list-pfade). Evidence-Quelle: https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/hunt-metrics/befund-1.md (17 probes, base 97a840e54).
