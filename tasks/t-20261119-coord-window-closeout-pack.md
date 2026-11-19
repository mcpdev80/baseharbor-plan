---
id: t-20261119-coord-window-closeout-pack
card_number: "0428-132"
card_short_title: "karten-/PR-/run-inventar mit"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: closeout-pack (codeman 59c94cab)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-132 · karten-/PR-/run-inventar mit
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/24a32c43/evidence/r28-welle4-2026-11-19/window-closeout/pack-1.md"]
---

- [x] t-20261119-coord-window-closeout-pack · Merge-window closeout-pack v0.4.28: karten-/PR-/run-inventar mit fernzeugen #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** closeout-pack (codeman 59c94cab)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/24a32c43/evidence/r28-welle4-2026-11-19/window-closeout/pack-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.28  
**Depends on:** none  
**Owner:** closeout-pack (codeman 59c94cab)  
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
Dachkarte fuer das closeout-heft des merge-windows: je karte status + PR + exakter head + terminal-run + abnahme-verdict + merge-commit, develop-linie als kette, und die offenen linien mit grund (owner-scope gate-map/ORAS, serielle reihenfolge, abhaengigkeiten). read-only gegen fernzeuge; keine statuswechsel durch die lane.

lane arbeitet das heft plan-only (evidence/r28-welle4-2026-11-19/window-closeout/pack-1.md); keine statuswechsel durch die lane

pack-1 geliefert und verifiziert (akte commit 24a32c43, ls-remote-zeug; 6c3add19 war der zwischenstand): 21 karten mit exakten head-shas, terminal-laufen, urteils-ids und merge-shas, develop-kette 907f16713..da76c5cf9 (11 merges), offene linien 088/114/119/121/122/123/124/131 + gate-map-patch 134. BEFUNDE AUS DEM HEFT, von mir dispositioniert: F-1 window-begin-marker fehlt (release-ops, owner-punkt), F-2 #1686 wurde vor dem letzten REQUEST_CHANGES-protokoll gemergt (protokoll-befund, in queue), F-4 demo#165 base=main -> VON MIR BEHOBEN: PR ist jetzt auf base=develop retargetet (head bc4c6113b unveraendert, exact-head run 44477622615 bleibt der zeuge), F-7 dispatch-FAIL 44466684726 -> eigene probe-karte (queue450), weil der grund ein neuer ist
