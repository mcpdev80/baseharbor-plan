---
id: t-20261119-coord-r28-pr-inventory
card_number: "0428-135"
card_short_title: "38 offene PRs gegen board —"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: pr-inventory (codeman bf3d2fb7-61e8-4e01-98a2-479edace99b9)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-135 · 38 offene PRs gegen board —
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/d4a4efa4/evidence/r28-welle4-2026-11-19/pr-inventory/befund-1.md"]
---

- [x] t-20261119-coord-r28-pr-inventory · PR-inventar 0.4.28: 38 offene PRs gegen board — dublette/superseded/kandidatenlos, liste zum schliessen #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** pr-inventory (codeman bf3d2fb7-61e8-4e01-98a2-479edace99b9)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/d4a4efa4/evidence/r28-welle4-2026-11-19/pr-inventory/befund-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** pr-inventory (codeman bf3d2fb7-61e8-4e01-98a2-479edace99b9)  
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
Der basics-check meldet dauerhaft OPEN-PRS > 12. Diese karte stellt je offenem PR im core- und demo-repo fest, ob er (a) ein lebender kandidat mit karte ist, (b) inhaltlich schon in develop steckt (ancestor/diff leer = superseded), oder (c) eine dublette zu einer hoeheren runde derselben karte ist. grundlage fuer das schliessen veralteter PRs (§3.8 ancestry-nachweis) und fuer deinen 35-PR-punkt.

## Acceptance
evidence/r28-welle4-2026-11-19/pr-inventory/befund-1.md: tabelle je PR | head-sha | basis | mergeable_state | karte (task-id oder 'keine') | einordnung (LEBEND / SUPERSEDED-ancestry / DUPLIKAT-von-pr / FREMDKOERPER-andere-welt) | begruendung mit nachweis (merge-base --is-ancestor ausgabe oder 'git diff --stat basis...head' leer). KEIN schliessen, KEIN comment, KEIN merge durch die lane — nur die liste; das schliessen mache ich. kein subagent (§4.8), tmp /var/tmp, read-only, host besenrein.

lane lauft read-only durch die offenen PRs (akte pr-inventory/befund-1.md); klassen LEBEND/SUPERSEDED-ancestry/DUPLIKAT/FREMDE-welt, nachweis je zeile; schliessen mache ich

inventar abgegeben (akte d4a4efa4): 38 offene core-PRs = 25 LEBEND, 11 STACK-PR (kettenposition), 1 DUPLIKAT (#1606 zu #1650, karte 078), 1 SUPERSEDED-by-content (#1649); 0 demo-PRs offen, 0 ancestry-superseded, 0 fremdkoerper. MEINE NACHPRUEfung VOR DEM SCHLIESSEN: beide schliess-kandidaten FAILN meinen test, daher bleibt BEIDES offen — (a) #1649: 'git cherry -v origin/develop <head>' zeigt 7 von 8 commits als '-' (bereits in develop), aber EINEN '+' commit c8db6333c 'test: use empty fixtures across coreless runtime gates'; sein inhalt liegt NICHT in develop (datei-hash-vergleich scripts/pr-gate-coverage.json, scripts/pre-release-runtime-impact.json, scripts/test_pr_gate_coverage.py = UNTERSCHIEDLICH, nur scripts/test_pre_release_runtime_reuse.py = gleich). der riese zwei-dot diff (177 dateien, -8074) ist nur die basis-entfernung, kein supersessions-zeug. (b) #1606 vs #1650: 'git cherry -v <1650-head> <1606-head>' zeigt drei '+' commits (1c124c47d, 6e9b12243, 4e81c16dd) — 1606s inhalt ist also NICHT in 1650 enthalten, ein close waere ein verlust. beide PRs gehoeren zur owner-blockierten karte 078/101 (.github-scope) und bleiben offen, bis die 078-entscheidung faellt

Nachpruefung durch Codex-Team 2026-11-19 21:35 UTC: #1649 head `c3840695f4a5551a6474a59781bc130a1c400cf8` bleibt offen, nicht Draft, 10 Commits / 11 Dateien; sein attestierter PR-Base-SHA `34c2ede594afc215b1e46eea251a587162224aa0` ist durch aktuelle `develop` `28fb427f057499efca705c1b7459e7653bd532a8` abgeloest. Der Unique-Commit `c8db6333c` fehlt zwar als Commit-Ancestor, sein angekuendigtes Baseline-Verhalten ist in `develop` inzwischen staerker umgesetzt: `cmd/baha/app_backend_selective_runtime_test.go` verwendet `runtimeContainerSnapshotSet`/`runtimeContainerBaselineDiff` (Container-ID plus Zustand), und prueft unveraenderte Baseline waehrend der Lifecycle-Phasen; dieselbe Snapshot-Pruefung liegt in Application-, HTTPS- und Secrets-Lifecycle. `scripts/pr-gate-coverage.json` und `scripts/pre-release-runtime-impact.json` mappen die relevanten Fixture-Dateien und native Gates bereits auf `develop`. `TestSelectiveBackendCleanupPreservesRuntimeBaseline` prueft nun auch geaenderte/exited Container, staerker als der PR-Test.

Der alte PR-Zweig ist kein guter Merge-Kandidat: sein diff gegen aktuelle `develop` loescht staerkere Snapshot-Assertions und Coverage-Eintraege; sein Secrets-Lifecycle-Zweig erwartet nach explizitem `seedProviderRuntimeOwner` faelschlich, dass derselbe Owner nicht existiert. Das letzte PR-Run #43942855437 schlug auf Docker und Podman fehl (das Run-Artefakt benennt keinen genauen Assertion-Fehler). Auf aktueller `develop` lokal gruen: gezielter `go test ./cmd/baha -run 'TestSelectiveBackendCleanupPreservesRuntimeBaseline|TestSelectiveApplicationBackendRuntimeAddRemoveReAdd|TestApplicationCapabilityLifecycleExistingCore|TestSelectiveHTTPSRuntimeAddRemoveReAdd|TestSelectiveSecretsRuntimeAddRemoveReAdd|TestManagedRegisteredOTLPNativeConsumerHandoff' -count=1` und `python3 -m unittest scripts.test_pr_gate_coverage scripts.test_pre_release_runtime_reuse` (58 Python-Tests). Native Docker/Podman Acceptance wurde in diesem lokalen Lauf nicht ausgefuehrt.

Disposition: #1649 ist inhaltlich durch staerkere aktuelle `develop`-Implementierung ersetzt und wurde am 2026-11-19 21:40 UTC als superseded-by-content geschlossen, ohne Merge: https://github.com/mcpdev80/baseharbor/pull/1649. Detaillierter Nachweis: `evidence/r28-welle4-2026-11-19/pr-inventory/follow-up-1649.md`. `#1606` bleibt hiervon unberuehrt und ist weiterhin kein sicherer Duplikat-Schliesskandidat.
