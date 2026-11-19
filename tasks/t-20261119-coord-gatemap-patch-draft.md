---
id: t-20261119-coord-gatemap-patch-draft
card_number: "0428-134"
card_short_title: "die vier audit-loecher als"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: gate-map-patch (codeman 1a8f8b70)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-134 · die vier audit-loecher als
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/7bc1ad15/evidence/r28-welle4-2026-11-19/gate-map/patch-2.md"]
---

- [x] t-20261119-coord-gatemap-patch-draft · Gate-map-patchvorschlag: die vier audit-loecher als EINer owner- patch datei (kein .github-eingriff durch die lane) #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** gate-map-patch (codeman 1a8f8b70)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/7bc1ad15/evidence/r28-welle4-2026-11-19/gate-map/patch-2.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.28  
**Depends on:** none  
**Owner:** gate-map-patch (codeman 1a8f8b70)  
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
Der audit 0428-133 hat vier loecher derselben klasse mit datei:zeile geliefert. Diese karte giesst sie in EINEN patchvorschlag, den der owner in einem stuck anwenden kann (0428-114 ist der traeger). Die lane schreibt KEIN .github und KEIN scripts/ — sie liefert den patch nur als datei im evidence-verzeichnis, anwendbar mit git apply.

## Acceptance
evidence/r28-welle4-2026-11-19/gate-map/patch-1.md + gate-map.patch: je fund eine aenderung (go-unit-routine auf PR-pfade des fensters; perses-smoke-zelle mit BASEHARBOR_PERSES_RUNTIME_SMOKE auf den bestehenden runtime-docker-pfad; demo pr-guided-consent.yml branches: [main, develop]; documentation-audit-pfad fuer docs/internal/*.json in scripts/pr-gate-plan.py), jeweils mit datei:zeile des audits als begruendung, KEIN neuer gate, keine produkt-aenderung. dry-run-zeug: 'git apply --check' gegen den jeweiligen head (patch-entwurf-AST unter /var/tmp, nicht die gemeinsame kopie) + 'git apply --check' fehlgeschlagen = befund statt behauptung. revision-labels, END.

lane arbeitet den gebuendelten patchvorschlag (akte gate-map/patch-1.md + gate-map.patch) — die vier funde aus 133 als EINER owner-aenderung, dry-run-zeug je aenderung, KEIN .github-eingriff in der lane

v2 abgegeben und VON MIR nachgeprueft (nicht nur die lane-Angabe): 'git apply --check' rc=0 gegen die AKTUELLEN heads — core develop da76c5cf9 (mit --exclude '*pr-guided-consent.yml') und demo main adda7599 (mit --include '*pr-guided-consent.yml'); die lane nannte in ihrer END wieder ein aelteres develop 907f1671 (ancestor von da76c5cf9), ihr dry-run gilt also erst durch meinen Nachlauf. FUNKTIONAL: CHANGE 1 wechselt jetzt die if-zeile tatstaechlich ('if: github.event_name != pull_request && ...' -> 'if: github.event_name == pull_request || (...)'), damit laeuft 'go test ./...' wieder auf PRs; CHANGE 2 ist ein echter job 'perses_runtime_smoke' in .github/workflows/targeted-integration.yml (yaml-geparst: env BASEHARBOR_PERSES_RUNTIME_SMOKE=1, steps inkl. 'Install verified ORAS for Core bootstrap' und 'Prepare isolated rootless Docker', timeout 20) — ABER an 'workflow_dispatch' mit inputs.gate == 'perses-runtime-smoke' gebunden: der job laeuft also NICHT automatisch im PR, sondern ist der freigegebene hosted-route, mit dem ich 088/#1592 und 119/#1690 die exaktkopfige Zelle auf demande bringe; CHANGE 3 (demo branches [main, develop]) und 4 (docs/internal/ in der documentation-audit-auswahl) bleiben wie in v1 richtig. kosten-hinweis fuer dich: CHANGE 1 macht die volle suite auf JEDEM PR scharf (laufzeit-kosten), wenn dir das zu grob ist, ist die alternative route die bestehende pr_plan-routine auf die fenster-pfade zu erweitern — sag mir welches, dann bestelle ich die entsprechende fassung
