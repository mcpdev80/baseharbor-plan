---
id: t-20261119-coord-r28-review-compliance
card_number: "0428-139"
card_short_title: "jeder karte im zustand review"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: review-compliance (codeman 5435da37-bf38-4790-9543-f33232f568ae)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-139 · jeder karte im zustand review
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/59358ba677993e7d62f5ed04a49a4ab823377a1b/evidence/r28-welle4-2026-11-19/review-compliance/befund-1.md"]
---

- [x] t-20261119-coord-r28-review-compliance · Review-zulassungs-pruefung: jeder karte im zustand review ihr PR + exakten head + terminalen run + nicht-draft zuordnen, ausnahmen liste #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** review-compliance (codeman 5435da37-bf38-4790-9543-f33232f568ae)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/59358ba677993e7d62f5ed04a49a4ab823377a1b/evidence/r28-welle4-2026-11-19/review-compliance/befund-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.28  
**Depends on:** none  
**Owner:** review-compliance (codeman 5435da37-bf38-4790-9543-f33232f568ae)  
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

## Purpose (coordination)
Im fenster sind karten in review, deren PRs drafts sind, deren letzter lauf ein draft-lauf war, oder deren head nicht mehr der gepushte ist. Diese karte prueft JEDE karte im zustand review gegen die fernzeuge und liefert die ausnahmen-liste, damit ich keine kandidaten zur abnahme stelle, die ihre required-CI nicht haben (praezedenz 073 draft-lauf, 082/#1665, 091/#1645, cli2-kette).

## Acceptance
akte evidence/r28-welle4-2026-11-19/review-compliance/befund-1.md: tabelle je review-karte (task-id | PR | gepushter head aus ls-remote/gh | PR draft-flag | letzter terminaler PR-lauf id + schluss + zahl der ausgefuehrten zellen | ZULASSUNG ja/nein + grund mit datei:zeile oder lauf-zeug). ausnahmen-oben, dann die erfuellten. KEIN draft-wechsel, KEIN comment, KEIN merge, KEIN rerun, keine karten-statuswechsel, isolierte clones unter /var/tmp, read-only, kein subagent (§4.8), host besenrein.

prueft den gesamten review-bestand gegen fernzeuge (draft-flag, gepushter head, terminaler lauf, 'PR Selected Checks' ausgefuehrt) und liefert die ausnahmen-liste (akte review-compliance/befund-1.md). read-only

END akzeptiert, 22 review-karten gepraemt (8 ZULASSUNG JA, 14 ausnahmen), von mir an vier stichproben gegen die fernzeuge bestaetigt: #1684 lauf 44505333646 mit 'PR Selected Checks' = success (nebenbei: 'PR · Selected Runtime' ist dort skipped, der Aggregate ist der entscheidende zeuge); #1602 und #1592 open/draft=false/behind; #1615 hat NULL laeufe auf dem head f93564a0d (befund 1, bestaetigt meine eigene status-context-pending-pruefung); #1598 letzter terminaler lauf 44499778660 = failure auf 831c2bea8. NEWE INFO, die die akte nicht haben konnte: 084 hat nach ihrem fehlgeschlagenen lauf einen FRISCHEN head 6e371c99b gepusht, lauf 44509535053 laeuft gerade — die zeile #1598 der akte ist damit ueberholt (kopf, nicht ergebnis). sitz entlassen
