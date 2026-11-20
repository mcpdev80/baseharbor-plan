---
id: t-20261119-r28-bughunt-observability-desk
kanban_title: "0428-147 · hunt observability desk"
card_number: "0428-147"
type: task
areas: [observability, qa]
release: v0.4.28
version: ""
parent: ""
owner: w147-0428-147-huntobs
kanban_status: active
kanban_lane: active
blocker: ""
wait_reason: ""
depends_on: []
repos: [mcpdev80/baseharbor]
evidence:
  - "https://github.com/mcpdev80/baseharbor/commit/c296086ca1e35ef3212d293afc94d7bebcd1690f"
resolution: ""
created: 2026-11-19
card_short_title: "hunt observability desk"
---

- [ ] t-20261119-r28-bughunt-observability-desk · hunt observability desk #task #release/v0-4-28 #status/active #view/active #area/observability #area/qa #kind/task
    <!-- generated:card -->
    **Owner:** w147-0428-147-huntobs  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/c296086ca1e35ef3212d293afc94d7bebcd1690f)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w147-0428-147-huntobs  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Reine Befundung (kein Produktwechsel) der bereits gemergten Observability-Flaeche von v0.4.28 auf dem develop-Stand, in einer echten docker-runtime-zelle. Diese Karte ist der Gefaess-behoelter fuer die Funde des Schnitts, damit kein fund kartenlos bleibt (Fund→Karte-Pflicht, owner-direktive 2026-11-08).

## Object of audit (nur CLOSED/merged = develop-Stand)

- `c296086ca1e35ef3212d293afc94d7bebcd1690f` [0428-086] Perses Loki datasource source adapter (#1616): genau EIN stream selector pro quelle, quellenspezifischer fehler-wrapper, fail-closed wenn keine quelle matcht.
- `1019190d8dc0ecac7693f3461153e76be0e2cb8a` [0428-084] Perses lifecycle commands enable/status/disable + ownership-safe remove (#1598).
- `fac01c77276ca2bf1e20cd0b7334bda5dd43e353` fix(0428-122) production LOG writer fuer class application (#1692).

## Pruefschnitt (was die Bahn konkret durchspielt)

1. Eine application mit ZWEI log-sources (zwei services) auf einer echten docker-runtime; `perses status` und der datasource-health-pfad: wird jede quelle einzeln abgefragt, und bleibt health FAIL-CLOSED, wenn eine quelle keine streams liefert?
2. Was passiert, wenn die zweite quelle auf dem Loki-endpoint einen fehler liefert (port zu, 5xx): meldet das kommando den QUELLEN-bezogenen fehler, oder verschluckt er ihn hinter einer allgemeinen meldung?
3. Merged-stand #1692: schreibt die class application ihre logs ueber den productions-pfad (kein test-only writer), und sieht perses/loki diese zeilenwirklich?
4. Doku-vs-verhalten: stimmt die gemergte doku (docs/de + docs/en observability) mit dem tatsaechlichen verhalten ueerein? Jeder abweichungsfall ist ein doku-befund.

## Rules of the lane

Keine produkt-aenderungen, keine PRs, keine aenderungen an `.github/**` oder `scripts/**` (befunde mit datei:zeile an den Coordinator). vm-lock claim/release-Pflicht, HA-szenarien ausgeschlossen. Akte: `evidence/r28-welle4-2026-11-19/vm-bughunt/<host>.md` mit `## PLAN` (nummeriert, OHNE markdown-checkboxen), Befunden nach schwere (blocker/ux/daemm/doku) inklusive befehlsgenauem repro, und 'cleanliness:'-zeile (host besenrein uebergeben; fremde container/netzwerke/volumes bleiben unangetastet, nur melden).

## Stop criteria

Runtime-zelle nicht erreichbar oder vm-lock streitig → STOP + Meldung, nicht improvisieren. Funde werden NICHT in dieser Karte_behoben; jeder fund wird in eine eigene bug-karte gegossen (intake-akte oder Coordinator schreibt die karte).

reine befundung, keine produktarbeit; die karte war nie jetzt arbeitend, der sitz war nie leer.

ARBEITET JETZT, kante gegen session gemessen (f4cd0c46-de15-4b69-827c-88930f5f2ffb, laptop): hunt-schnitt H-V19 'beobachtungs-desk nach den metrik-karten' - (1) wird ObservabilityUnsupported (0428-182/#1716) an consumption-stellen wie sammelbar behandelt (git grep auf beide felder, eine seite die nur EINES prueft ist ein fund), (2) gilt die valkey-gatter-regel (perses_dashboards_valkey.go:246) auch fuer loki/tempo/postgres oder liefern die dashboards ohne datenbasis, (3) LOG-writer class application (fac01c772/0428-122) auf klartext-sekrete + ob die zelle dafuer von der CI ausgewaehlt wird. reine befundung; #1650/#1615/#1715 nur lesen.
