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
depends_on: []
blocked_by: []
superseded_by: []
owner: ""
kanban_status: planned
kanban_lane: ready
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md"]
prs: []
created: 2026-11-20
---

- [ ] t-20261120-r28-provider-signal-id-scope-inconsistency · scope signal ids uniformly per project #bug #release/v0-4-28 #status/planned #view/ready #area/capability #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md)  
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
