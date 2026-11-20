---
id: t-20261120-r28-bughunt-connector-handshake-timeouts
kanban_title: 0428-173 · hunt connector handshake
card_number: "0428-173"
card_short_title: "hunt connector handshake"
type: review
areas: [observability, capability]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: []
blocked_by: []
superseded_by: []
owner: w173-pr0428-173-handshake
kanban_status: closed
kanban_lane: closed
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/bughunt-connector-handshake/round-1.md"]
prs: []
created: 2026-11-20
wait_reason: ""

---

- [x] t-20261120-r28-bughunt-connector-handshake-timeouts · audit handshake timeout and retry paths #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/capability #area/observability #kind/review
    <!-- generated:card -->
    **Owner:** w173-pr0428-173-handshake  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/bughunt-connector-handshake/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w173-pr0428-173-handshake  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Ziel

Bug-Hunt H-V16. Prüfschnitt: Timeout- und Retry-Wege im Zusammenspiel mit
Identitätsprovider/Connector — wo wird gewartet, wo abgebrochen, und was bleibt danach?

## Anker (develop)

- `internal/identityprovider/keycloak_realization.go` (registration, readiness)
- `internal/observability/registry.go` (List/Remove, exakte ID)
- `internal/logs/realization.go` (Loki-Signale, placement.Project)

## Schnitte

1. Welche Wartezeit ist wirklich konfiguriert, und welche Zeile setzt sie?
2. Nach einem Timeout: ist der Zustand wieder betretbar (idempotent), oder bleibt ein
   halb registriertes Signal stehen?
3. Zwei schnelle Versuche parallel — verliert einer stille Information?
4. Ein Provider ohne Signale: fail-closed oder leer sichtbar?

## Regel

Reine Befundung: KEINE Produktänderung, KEIN commit, KEIN PR, KEIN merge. Akte mit
`file:line` je Aussage, `git ls-remote origin refs/heads/develop` in der Akte,
`cleanliness:`-Zeile mit Vorher/Nachher-Liste (container/networks/volumes/state dirs).
Nichts gefunden = 'VERHALTEN KORREKT' + Prüfweg. Kartenlose Funde sind verlorene Arbeit —
die Akte nennt für jeden Fund `DATEI:ZEILE`, `ERWARTET (Vertrag)`, `IST (gemessen)`;
Karten gieße ich.

