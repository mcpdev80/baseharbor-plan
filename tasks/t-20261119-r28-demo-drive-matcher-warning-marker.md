---
id: t-20261119-r28-demo-drive-matcher-warning-marker
card_number: "0428-129"
card_short_title: "drive.py matcher auf das"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-129 · drive.py matcher auf das
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261119-r28-demo-drive-matcher-warning-marker · Demo: drive.py matcher auf das Warning-marker-verhalten der annerkennenden stadien ziehen #task #release/v0-4-28 #status/planned #view/ready #kind/task
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

## Purpose
Folgekarte zu 0428-126 (core, PR #1696, gemeldet in evidence/r28-welle4-2026-11-19/dualmatch-docs/fix-1.md): das Warning-marker wird jetzt in JEDEM annerkennenden CLI-stadium gedruckt (gate-semantik unveraendert). Die Demo-Bahn `drive.py` erkennt stadien ueber ein eigenes matcher-pattern; bleibt das Muster unveraendert, sieht die demo einen zustand als nicht-annerkannt, waehrend der core das marker setzt — also eine demo-seitige Scheibenfalse-negativ-erkennungs-luecke.

## Acceptance
- `drive.py`-matcher akzeptiert die annerkennenden stadien MIT Warning-marker konsistent (identische regel wie core, keine doppelte auslegung).
- eine demo-seitige pruefung/regression deckt den fall "stadium annerkannt + marker gesetzt" ab, damit die kopplung nicht erneut driftet.
- exakte-head CI des demo-repos auf dem kandidaten terminal gruen; akte unter baseharbor-plan evidence/r28-welle4-2026-11-19/demo-drive-matcher/.

## Abhaengigkeiten
Content-abhaengig von 0428-126 (merged oder abgenommen); basis ist develop des demo-repos.
