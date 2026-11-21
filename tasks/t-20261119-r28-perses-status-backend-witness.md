---
id: t-20261119-r28-perses-status-backend-witness
card_number: "0428-142"
card_short_title: "echte backend-witness fuer"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w230-0428-142-hop
kanban_status: active
kanban_lane: active
kanban_summary: "'baha perses status' nennt pro observability-signal eine ECHTE backend-witness (erreicht / gematcht / nicht erreichbar) statt…"
kanban_title: 0428-142 · echte backend-witness fuer
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1702]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

## Current handoff

The former owner-decision blocker is resolved by 0428-143: `Verification=none`
means no verification assertion for every source class, and metrics exporters
omit those sources from scrape targets. This assigned, started lane is parked
pending worker capacity. #1702 still needs the concrete review corrections and
a fresh exact-head run; it is not ready to merge.

- [ ] t-20261119-r28-perses-status-backend-witness · CLI-Gesicht: echte backend-witness fuer perses host-status (app_status_result.go), damit Loki/Tempo nicht dauerhaft 'unavailable' gemeldet bleiben #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** w230-0428-142-hop  
    **PR:** [baseharbor#1702](https://github.com/mcpdev80/baseharbor/pull/1702)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261119-r28-perses-alert-verifier-caller-wiring](t-20261119-r28-perses-alert-verifier-caller-wiring.md)  
**Owner:** w230-0428-142-hop  
**Priority:** not set  
**PRs:** [baseharbor#1702](https://github.com/mcpdev80/baseharbor/pull/1702)  
**Source:** 
<!-- /generated:links -->

## Goal

'baha perses status' nennt pro observability-signal eine ECHTE backend-witness (erreicht / gematcht / nicht erreichbar) statt pauschal 'nicht verifiziert', sodass Loki und Tempo nicht dauerhaft als unbestaetigt erscheinen, obwohl der datasource-gesund-pfad (#1616, #1592 gemergt) die info laengst hat. Sichtbares ergebnis: ein operator sieht im status, WELCHE quelle warum gruen oder rot ist.

## Scope

- In scope: das status-ergebnis-feld und seine ausgabe in cmd/baha/app_status_result.go plus sein test cmd/baha/app_status_result_test.go; die drei faelle (backend erreicht UND stream gematcht) / (erreicht, aber KEIN match) / (nicht erreichbar) pro signal, inklusive source-id im text.
- Out of scope: aenderungen an den query-/health-pfaden selbst (internal/logs/loki_datasource.go, internal/capability/perses.go, internal/metrics/prometheus_verify.go). Diese karte KONSUMIERT nur, was dort gemergt ist.
- HARTE GRENZE: beruehrt die arbeit internal/capability/perses.go oder cmd/baha/machine_coverage.go, STOP + frage an den coordinator — die dateien haelt die laufende lane zu PR #1599 (0428-089).

## Acceptance

- 'perses status' liefert pro signal eine zeile mit source-id und einem der drei zustaende; kein zustand 'unverified' mehr, wenn der health-pfad eine entscheidung getroffen hat.
- Ein unit-test pro fall (gematcht / kein match / fehler) in cmd/baha/app_status_result_test.go, ausgefuehrt im 'PR · Go unit'-shard (CI-aufnahmepflicht neuer tests, owner-direktive 2026-11-07): die auswahlregel muss die datei treffen, sonst befuend mit datei:zeile melden.
- Die menschen-ausgabe und die machine-ausgabe (cli-machine-coverage) zeigen denselben zustand — kein drift zwischen den beiden gesichtern.

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

## Purpose (aus der korrektur 0428-077 hervorgegangen)
Die 077-korrektur hat die Perses-katalog-verfuegbarkeit backend-spezifisch gemacht (baseharbor_provider / baseharbor.provider statt health-uebertragung) und fail-closed defaultiert. Die lane meldet als grenze: das CLI-gesicht (cmd/baha/app_status_result.go) kann die echte backend-witness nicht ziehen, ohne die eine-argument-API zu aendern; deshalb zeigt 'baha app status' Loki/Tempo dauerhaft als unavailable, obwohl der perses-katalog langst richtig entscheidet. Das ist ein echtes produkt-loch, kein rund-fehler.

## Acceptance
ein test, der den CLI-pfad gegen eine backend-witness prueft ( Loki mit eigenem signal -> verfuegbar; Loki ohne eigenes signal -> unavailable), ohne die eine-argument-API von app_status_result zu aendern; die drei stellen internal/logs/render.go:145/163/296, internal/telemetry/otlp_payload.go:28 und internal/metrics/perses_dashboards_hosts.go:243-245 sind die label-zeugen. akte evidence/r28-welle4-2026-11-19/perses-status-witness/befund-1.md + pr. KEIN merge durch die lane, keine .github/scripts-anderungen (befund statt dessen), kein subagent (§4.8), host besenrein.

kopf e22f6795c (ls-remote), base develop 223cb97a9, draft=false, lauf 44600570152 completed/success, 15 checks ausgefuehrt, 6 SKIPPED (nicht erbracht; runtime/HA = owner-draht 114(a)). GESCHICHTS-BEFUND von mir gemessen: der zweite 'hopf' war KEIN merge-hopf — vorgaenger 317b730a9 ist kein ancestor, head hat einen eltern; drei blobs byte-identisch (a79ed5d365/be8d5fd7e7/2b9a088474), kein inhalt verloren. lane geruegt, akten-klarstellung verlangt.

CODEX-r1 REQUEST CHANGES auf e22f6795c (akte 1702-0428-142.md): (1) 'configured' ist manifest-erklaerung statt backend-witness, 'unreachable' deklariert aber ohne emission-pfad (app_status_result.go:64-65/:92-98/:108-114/:124-130); (2) oeffentliche ausgabe behaelt verbotene wortliste configured_unverified/verified (:38-45/:234-250/:351-353 + perses_lifecycle.go:75-79/:217-233); dazu ein test, der unreachable nur behauptet. rotation auf frische bahn.

ALLES VON MIR GEMESSEN, zum ersten mal in dieser karte ohne abweicherung: head 6740299f9, base 28fb427f = AKTUELLE develop-spitze, ZWEI eltern (56d85ddb63aff + develop, an der platte gezaehlt), merge-base --is-ancestor = 0, merge-tree konfliktfrei, draft=false, PR-lauf 44621032956 event=pull_request completed success am exakten kopf (21:44:55Z), akte fix-2.md auf main. Finding 1 ('unreachable' produzierbar) ist mit stop-kriterium ESCALIERT auf 0428-143 — review muss sagen, ob das eine akzeptanz-luecke ist oder eine follow-up-karte

CODEX r4 REQUEST CHANGES (zwei blocker): P2 'manifest flag duerfen keinen backend-nachweis vortaeuschen' (app_status_result.go:76-139) und P4 bleibt OWNER-punkt (0428-143, unreachable auf echtem evidence-pfad); P5 ist eine scope-frage an dich, nicht an die lane. Mechanischer teil (P1/P2-trennung/P3/P7-akte) geht auf laptop:2, mit hopf-zwang (mergeable_state=behind, develop 4b3a3559). 0428-152 haengt laut CODEX-urteil ausdbruecklich hinter diesem PR

review HOLD (owner-verdict 2026-11-20): PR #1702 ist am exakten head green, aber karte 0428-142 verlangt echte erreichbare UND unreachable backend-witnesses; der stand ist manifest-only, der branch BEHIND develop, und der diff editiert internal/capability/perses.go ohne dokumentierte freigabe. nicht als freigebbare review-arbeit zaehlen. naechster schritt: rebasen + die perses.go-aenderung zurueckziehen oder per karte freigeben lassen.

handoff abgeschlossen und required-aggregat GRUEN am exakten head: PR #1702 head 6740299f91c0, base develop, draft=false, 13 dateien, 'PR Selected Checks' = SUCCESS (check-runs am head: 15 success / 20 skipped, KEINE failure). das ist der EINE kandidat im fenster, der nicht an einer owner-buchung haengt (#1704 = karte 0428-073 mit ihrer entscheidung, #1650 = 0428-078 Codex). DARUM review statt wait. ZWEI RANDNOTIZEN FÜR DIE ABNAHME, beide gemessen: (i) die datei internal/metrics/verify_none_red_test.go existiert auf develop BEREITS (befund w219) - pruefen sie, ob der PR damit teils ueberfluessig ist oder ob die datei in ihrem PR weitergeht; (ii) ihr head ist aelter als #1594 (ancestry auf den aktuellen develop-tip NEIN), das required-aggregat ist aber trotzdem success, weil die required-zellen gegen den merge-ref laufen. ein merge ist also moeglich, OHNE dass 0428-204 fertig ist - und er wuerde inhalt auf develop bringen. TRIGGER FUER DIE NAechSTE KANTE: CODEX-verdict an diesem SHA, dann merge oder korrekturrunde.

CODEX-REVIEW VERDICT REQUEST CHANGES am unveraenderten head 6740299f91c0 (required-aggregat war SUCCESS; der verdict haelt drei andere punkte fest). Korrekturarbeit aufgesetzt: sitz w222-0428-142-witness (ornith) mit dem dreiteiligen Rezept - (1) 'unreachable' als echter zustand im witness-Pfad statt allein aus manifest-flags, (2) die von der lane falsch belegte 'validate ...'-Zeile in der Akte berichtigen, (3) Wissensstand: der reviewer bestaetigt, dass nach einem merge auf develop 40cb28c die vier cli-shards rot bleiben, deshalb finger weg von cmd/baha/main.go und internal/operatorauth/** (das ist 0428-204). RANDBEFUND GEGEN DAS PROTOKOLL: die review-Akte lag nur lokal in der reviewer-sandbox; nachlieferung in baseharbor-plan main angefordert (§5.3: ein verdict ohne erreichbare datei ist wertlos).


HANDOFF RECORDED (AGENTS 3.6): the previous lane (w222) delivered candidate 3f7600ded0d9 on #1702 with the P1 fix and an honest akte, then refused twice to hop onto current develop (ruleset 25223521 strict, merge-base --is-ancestor develop <head> = 1). The hop goes to a fresh lane with their candidate and evidence untouched; their END sentence (PR Selected Checks = SUCCESS) was disproved by the run job list and corrected here, not in their akte. Their work stands as delivered.
