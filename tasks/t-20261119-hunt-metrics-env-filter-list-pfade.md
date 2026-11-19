---
id: t-20261119-hunt-metrics-env-filter-list-pfade
card_number: "0428-121"
card_short_title: "Env-Filter wirkt nicht auf"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: 0428-121 r3 (codeman 045d7e8a, entlassen)
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
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/env-filter-fix/fix-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1691-route2-review.md", "https://github.com/mcpdev80/baseharbor/pull/1691"]
---

- [ ] t-20261119-hunt-metrics-env-filter-list-pfade · Environment-Filter wirkt nicht auf alle list-Pfade (caller-side prefix workaround only) #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** 0428-121 r3 (codeman 045d7e8a, entlassen)  
    **PR:** [baseharbor#1691](https://github.com/mcpdev80/baseharbor/pull/1691)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/env-filter-fix/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1691-route2-review.md), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1691)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** 0428-121 r3 (codeman 045d7e8a, entlassen)  
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

END akzeptiert: zentraler env-filter auf allen list-Pfaden, head d9d70a98 base-exakt ec592fd38 MERGEABLE, exact-run 44450253933 SUCCESS, red->green regression envfilter_regression_test.go, akte am band (head+run refs). Overlap mit #1692 (122, beide review): functionsdisjunkt, erst-gruenes-review-zuerst-Regel gilt — Integrationsreihenfolge wird beim ersten merge veraendert

korrektur-runde laeuft: environment-resolver faehrt application-scoped quellen mit fehlender/mehrdeutiger environment-zuordnung nicht sauber raus (cross-environment visibility leak, REQUEST_CHANGES-kommentar auf d9d70a984). rezept: explizite oder eindeutig ableitbare zuordnung verlangen, sonst fail-closed im filter. head afc0dde86 ist base-exakt deeeb6477

routen-entscheid gefallen (route 2, caller-agnostic source-herleitung + fail-closed), weil der eigene placement.Environment-head auf der 125-basis nicht baut (develop traegt environment jetzt in internal/application/connectivity.go, nicht in capability/provider_placement.go). bedingung: go build/vet lokal gruen vor jedem push; realer caller-placement-only-fall im code = STOP + QUESTION (dann route 1 additiv). run 44467889900 (PR · Go unit · packages) war rot auf 295b908edc

uebergabe-punkt: commit 9a4325028 liegt fertig im worktree auf develop da76c5cf9 (route 2: herleitung aus source-id, fail-closed bei mehrdeutig/fehlend). ausstehend: gofmt/build lokal gruen, push auf lane-0428-efilter (monoton, ancestor-zeug), exact-head-CI bis terminal, akte fix-2.md mit W-belegen, verlustfreie rueckgabe der gemeinsamen kopie (11 dirty eintraege, stash statt reset). 122r3 laeuft erst NACH deinem merge — beide schreiben runtime_observability.go

STOP vor push/merge nach unabhaengigem review: SourceMatchesEnvironment prueft nur aufloesbarkeit, keinen vergleich mit dem gewuenschten environment -> fail-open fuer cross-environment listing (prod+stage derselben application passieren die zentrale List-pruefung). carrier-umfeld ist an allen aufruferstellen schon da (cmd/baha/app_logs.go:140 und app_traces.go:249 ueber prepared.manifest.Environment; internal/metrics/prometheus_files.go:233/240/451 und prometheus_verify.go:141/152 ueber m.Environment; internal/logs/overrides.go:105, registration.go:27 im manifest-/registration-kontext). befehl: parameter requestedEnvironment in List + wrapper, vergleich case-normalisiert, nicht aufloesbar/mehrdeutig = unsichtbar, '' = explicit fail-closed; regression prod/stage/leer + mutations-kontrolle; dann gofmt/build/vet, hopf auf da76c5cf9, push, exact-head-CI terminal, akte fix-2.md mit aufrufer-tabelle. KEIN ProviderPlacement.Environment, KEIN security.go

INHALTLICH GELUOST auf head 4f4b3d7a60b057fd8f29cbba3c2685fc9346b66d (monoton, develop da76c5cf9 ancestor): SourceMatchesEnvironment(source, requestedEnvironment) vergleicht case-normalisiert, false bei unloesbarem environment; List + wrapper reichen requestedEnvironment durch; sechs tests (prod/stage-caller, leer fail-closed, unloesbar fail-closed, mutation-drop, shared-sichtbarkeit). Go-unit shards + Selected Runtime SUCCESS. EIN FEHLJOB: 'PR · Source format' — job-log: 'source readability: internal/observability/registry.go has 877 lines (limit: 800)'. befehl r3: die neue filter-logik in eigene datei internal/observability/envfilter.go auslagern (verhalten/API unveraendert, datei unter 800 zeilen), gofmt -l leer, hopf (kein rebase), push mit ancestor-zeug, exact-head CI terminal SUCCESS, akte env-filter-fix/fix-3.md. KEIN ProviderPlacement.Environment, KEIN security.go, KEIN .github

abgegeben und von mir verifiziert: head d1fcfdf6b8376a30f5100c8c30f5f3491427cf9e, monoton (develop da76c5cf9 ancestor), PR #1691 clean, exact-head run 44487090323 TERMINAL SUCCESS und KEIN nicht-gruener job (der Source-format-fehljob ist weg: registry.go 730 zeilen < 800, die neue datei internal/observability/environment.go nimmt die filter-logik). inhalts-zeug der route: SourceMatchesEnvironment(source, requestedEnvironment) vergleicht case-normalisiert, false bei unloesbar/mehrdeutig/leer; List + wrapper geben requestedEnvironment durch; sechs tests inkl. prod/stage-caller, leer fail-closed, mutation-drop. akte env-filter-fix/fix-3.md. abnahme vorgelegt — damit.loest sich die serie 122r3 und 124r3 sowie 123 auf
