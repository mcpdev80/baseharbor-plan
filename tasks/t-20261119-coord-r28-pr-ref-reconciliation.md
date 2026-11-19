---
id: t-20261119-coord-r28-pr-ref-reconciliation
card_number: "0428-140"
card_short_title: "PR-verweise korrigieren und"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: pr-ref-reconciliation (codeman 3b553796, ornith)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-140 · PR-verweise korrigieren und
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/b2cc2ffbfa58ce20175a5d36d94a9f32af9f3c47/evidence/r28-welle4-2026-11-19/pr-ref-reconciliation/befund-1.md"]
---

- [x] t-20261119-coord-r28-pr-ref-reconciliation · Review-karten gegen fernzeuge nachziehen: PR-verweise korrigieren (nachfolger zu #1603/#1610/#1619, basis-ast von #1665) und grund je karte dokumentieren #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** pr-ref-reconciliation (codeman 3b553796, ornith)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/b2cc2ffbfa58ce20175a5d36d94a9f32af9f3c47/evidence/r28-welle4-2026-11-19/pr-ref-reconciliation/befund-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.28  
**Depends on:** none  
**Owner:** pr-ref-reconciliation (codeman 3b553796, ornith)  
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
Die zulassungs-pruefung 0428-139 (akte review-compliance/befund-1.md, findings 3 und 5) hat drei karten im zustand review, deren PR-VERWEIS ins leere fuehrt: #1603 (0428-079), #1610 (0428-091), #1619 (0428-085) sind CLOSED, ihre head-refs teils geloescht; und #1665 (0428-082) basischt auf dem zweig der CLOSED #1608 statt auf dem nachfolger #1684 (lane-0428-083-datasources-r2). Fuer den merge-window brauche ich an diesen stellen die wahrheit im board, nicht eine vermutung.

## Acceptance
akte evidence/r28-welle4-2026-11-19/pr-ref-reconciliation/befund-1.md: tabelle je betroffene karte (task-id | bisheriger PR-verweis | fernzeug: state/head-ref-existenz von PR + branch via ls-remote | nachfolger-PR oder 'kein nachfolger' | EMPTFEHLUNG: welchen verweis ich im board setzen soll + grund mit lauf-id/datei:zeile). zusaetzlich fuer #1665: 'git -C baseharbor merge-base --is-ancestor <head von #1684> <head von #1665>' als zeuge, ob der basis-ast ueberhaupt drin steckt, und was ein retarget bedeuten wuerde (zahl der konflikte ueber 'git merge-tree --write-tree'). KEIN karten-statuswechsel, KEIN PR-comment, KEIN retarget durch dich, KEIN merge, KEIN rerun/dispatch, isolierte clones unter /var/tmp, read-only, kein subagent (§4.8), host besenrein (vorher/nachher docker ps -a, 'cleanliness:'-zeile).

END akzeptiert, sitz entlassen: 4 karten nachgezogen, alle vier fernzeuge von mir gegengelesen (#1603 closed/merged=null, head-ref lane-0428-079-r28-perses-messaging; #1610 closed auf basis lane-0428-075-perses-seam; #1619 closed mit base w091-0428-091; #1665 base=w083-perses-datasources@ed55d8933, gegen develop UND gegen #1684-ast je 6 konflikte per merge-tree, #1684-head NICHT enthalten — meine eigene zaehlung bestaetigt die lane). EINE KORREKTUR ZU IHRER EMPFEHLUNG: sie nennt #1645 als nachfolger mit 'terminal SUCCESS' — das ist als zulassung NICHT brauchbar, denn #1645 ist weiter draft=true, und auf lauf 43876671426 ist 'PR Selected Checks' SKIPPED (30 zellen ausgefuehrt, aber der aggregate nicht), also draft-zellen-only. repoint ist richtig, qualifiziert ist der kopf erst nach promotion + frischem lauf
