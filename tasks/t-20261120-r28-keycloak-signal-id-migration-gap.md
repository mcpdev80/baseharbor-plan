---
id: t-20261120-r28-keycloak-signal-id-migration-gap
kanban_title: 0428-168 · signal id migration gap
card_number: "0428-168"
card_short_title: "signal id migration gap"
type: bug
areas: [observability, capability]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: []
blocked_by: []
superseded_by: []
owner: w168-pr0428-168-signal-mig-r2
kanban_status: active
kanban_lane: active
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md"]
prs: [mcpdev80/baseharbor#1709]
created: 2026-11-20
wait_reason: ""

---

- [ ] t-20261120-r28-keycloak-signal-id-migration-gap · migrate un-prefixed keycloak registrations #task #release/v0-4-28 #status/active #view/active #area/capability #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** w168-pr0428-168-signal-mig-r2  
    **PR:** [baseharbor#1709](https://github.com/mcpdev80/baseharbor/pull/1709)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261120-r28-provider-signal-id-scope-inconsistency](t-20261120-r28-provider-signal-id-scope-inconsistency.md), [t-20261120-r28-signal-id-normalization-collision](t-20261120-r28-signal-id-normalization-collision.md)  
**Owner:** w168-pr0428-168-signal-mig-r2  
**Priority:** not set  
**PRs:** [baseharbor#1709](https://github.com/mcpdev80/baseharbor/pull/1709)  
**Source:** 
<!-- /generated:links -->

## Ziel

Bug-Karte aus Bug-Hunt H-V12 (FUND 3, K3). PR #1707 hat die Keycloak-Signal-ID von
`"keycloak-metrics"` auf `"keycloak:<project>"` umgestellt, ohne Bestandsumschreibung.

## Befund (Quelle: Akte)

- Vor #1707: `ID: "keycloak-metrics"` (wörtlich, aus dem Merge-Diff gestrichen).
- Nach #1707: `ID: "keycloak:" + r.files.Project` = z. B. `keycloak:bh-<target>-<app>-identity-<env>`.
- `List` (`internal/observability/registry.go:383`) und `Remove` (`:367`) arbeiten auf exakter ID.
- Eine bestehende Registration ohne Präfix wird damit nach dem Deploy **nicht mehr gefunden** —
  sie ist weder sichtbar noch löschbar.

## Erwartung vs. Ist

Erwartet: Ein Deploy der ID-Regel behält bestehende Registrationen beobachtbar oder stellt sie um.
Ist: bestehende Registrationen werden zu unreachbaren Leichen.

## Reihenfolge

Diese Karte blockiert 0428-166 und 0428-167 (jede weitere ID-Änderung vertieft das Loch).

## Akte

https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md

loop-abbruch angeordnet (§3.6): gemessen 861 FAIL-zeilen, 234 paketlaeufe, ein test 177x rot. der wichtige unterschied: ihr NEUER test und ReconcileLegacySignals existieren NICHT auf develop (git grep leer), aber TestStandaloneSharedPostgresUsesPhysicalOwnerAcrossAppAndRecoveryLifecycle EXISTIERT dort (internal/application/shared_postgres_runtime_owner_test.go) und laeuft dort gruen (develop-push 44669117744/44669117784 success, packages-shard ohne namenfilter) — bei ihnen rot. das ist inhalt, nicht umfeld. befehl: zuerst WIP-stand ausliefern (vier stunden arbeit existieren nur auf diesemrechner = derselbe risikotyp wie bei karte 078), dann nur noch isolierte -run-laeufe mit den beiden FAIL-Blocken woertlich in die akte. DECKEL: scheitert ein weiterer anlauf an demselben existierenden test, rotation auf frische Lane
