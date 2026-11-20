---
id: t-20261120-r28-provider-signal-id-scope-inconsistency
kanban_title: 0428-167 · provider signal id scope split
card_number: "0428-167"
card_short_title: "provider signal id scope split"
type: bug
areas: [observability, capability]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: [t-20261120-r28-keycloak-signal-id-migration-gap]
blocked_by: []
superseded_by: []
owner: w167-pr0428-167-loki-scope
kanban_status: closed
kanban_lane: closed
blocker: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/loki-signal-scope/round-1.md"]
prs: []
created: 2026-11-20
wait_reason: ""

---

- [x] t-20261120-r28-provider-signal-id-scope-inconsistency · scope signal ids uniformly per project #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/capability #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** w167-pr0428-167-loki-scope  
    **Needs:** t-20261120-r28-keycloak-signal-id-migration-gap  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/loki-signal-scope/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** t-20261120-r28-keycloak-signal-id-migration-gap  
**Owner:** w167-pr0428-167-loki-scope  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Ziel

Bug-Karte aus Bug-Hunt H-V12 (FUND 2, K2). Vier Provider bauen ihre Perses-Identitaet nach
derselben Regel `"provider:" + project` — aber zwei von ihnen tragen das Projekt, zwei nicht.

## Befund (Quelle: Akte, von mir am Quelltext bestaetigt)

- Keycloak: `internal/identityprovider/keycloak_realization.go:164` -> `ID: "keycloak:" + r.files.Project`
- Tempo: `internal/traces/tempo.go:404` -> `ID: "tempo:" + p.Project`
- Loki: `internal/logs/realization.go:233` -> `signals["loki-metrics"]` (LITERAL, ohne Projekt)
- OpenTelemetry-Collector: `internal/telemetry/realization.go:197` -> `"opentelemetry-collector:" + files.Project`
- Lesepfad `internal/observability/registry.go:383-442` (`List`) filtert exakt nach `source.ID`.

Folge: zwei Applications, die Loki nutzen, schreiben in dieselbe Registration — die zweite
überschreibt die erste oder verschwindet aus der Ansicht, je nach Reihenfolge.

## Erwartung vs. Ist

Erwartet: gleiche Regel für alle Provider-Signale (pro Projekt/App eindeutig).
Ist: eine gemischte Regel, verifiziert an vier Stellen im Quelltext.

## Stop-Kriterium

Keinesilent-Change der Loki-/Registry-IDs ohne Migrationspfad (siehe 0428-168).

## Akte

https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md

KEIN DEFEKT, karte DROPPED — der fehler sass in MEINEM jagd-befund (H-V12, fund 2), die lane hat ihn widerlegt und ich habe es selbst nachgemessen. Befund behauptete, Loki trage eine projektlose registration-id, belegt mit 'internal/logs/realization.go:233 signals["loki-metrics"]'. GEMESSEN auf develop 2026-11-20: dieselbe datei uebergibt 'ID: "loki:" + placement.Project'; das literal ist der SCHLUESSEL innerhalb der Signals-map, sonst nur ein descriptor-name in internal/capability/reference.go:132 ('git grep -c loki-metrics origin/develop -- internal/**/*.go' = 2 treffer, keine davon eine registration-id). registry.go RegisterProviderSignals uebernimmt registration.ID unveraendert, also war Loki immer projekt-scopiert (laut lane seit v0.4.19) und eine ueberdeckung zweier apps ist nach dieser regel nicht moeglich. DAUERHAFTER WERT: die lane haelt die invariant mit regressionen in internal/observability und internal/logs, die der CI-shard ueber 'scripts/pr-go-unit-shard.py --mode packages' (go list ./...) ausfuehrt — der fall ist also getestet, nicht nur behauptet. FOLGE FUER MEINE JAGD-METHODE: signal-NAME und registration-ID sind zwei ebenen, die ich kunftig getrennt belege, bevor ich eine karte giess. Karte 0428-168 ist von diesem fehler NICHT beroehrt (dort aendert #1707 die id-formel selbst, nachgewiesen am merge-diff)
