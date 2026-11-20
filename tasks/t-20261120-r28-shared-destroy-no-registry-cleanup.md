---
id: t-20261120-r28-shared-destroy-no-registry-cleanup
card_number: "0428-184"
card_short_title: "shared destroy skips registry"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w184-0428-184-shareddestroy
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-184 · shared destroy skips registry
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["1715"]
sources: []
blocker: "wartet auf karte 0428-187 (podman data-capabilities consent-gate stall, run 44743111417 job 136312259900) - ohne die_loesung ist der selected-aggregate am exakten head rot, gleich gueltig ihr diff ist"
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md"]
---

- [ ] t-20261120-r28-shared-destroy-no-registry-cleanup · Shared destroy does not clean the signal registry (stale owners survive) #task #release/v0-4-28 #status/active #view/active #kind/bug
    <!-- generated:card -->
    **Owner:** w184-0428-184-shareddestroy  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w184-0428-184-shareddestroy  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Found by bug hunt H-103 (funded from card t-20261117-hunt-signals-103, AGENTS 3.3.5 finding-to-card duty)

F3 of hunt round-1: the destroy path for shared resources removes containers/volumes but does not drop the registry rows that named those signals, so a later RegisterProviderSignals sees an owner that no longer exists. This is the same registry that 0428-166 just hardened with a collision guard, so the interaction is not hypothetical.

## Acceptance

1. Destroy of a shared resource removes (or marks reusable) exactly the registry entries it owns, and a re-registration afterwards succeeds with a fresh owner.
2. A regression that is red if the cleanup line is deleted, and a second case proving a FOREIGN owner entry is NOT deleted (no cross-tenant wipe).
3. CI job name recorded; the test runs in the packages shard.

## Boundaries

internal/observability/** plus the destroy path in internal/runtime/**. Read 0428-166 merged behaviour first (provider_registration.go, migration.go) and stop with a report if the cleanup would change collision semantics.

lane auf dem zweiten freien sitz, gegruendet aus zwei hunt-befunden dieses tages (hunt-signals-103 F3 und die
wiederholung in hunt-signals-104: loki/tempo/otel sauber, keycloak/broker/executor/shared-backends OHNE Remove).
auftrag: shared destroy raumt genau die registry-eintraege des eigenen owners, eine re-registration mit demselben token
gelingt danach; regression in beide richtungen PLUS der fall 'fremder owner-eintrag bleibt ERHALTEN' (kein cross-tenant
wipe). vorgeschaltet ist lesend die pruefung der HEUTE gemergten 0428-166-stellen (internal/observability/provider_registration.go
und migration.go) mit der zeile 'welche zeile ich NICHT antaste' in der akte. grenzen: KEIN .github/**, KEINE aenderung an
internal/application/perses_runtime.go (dort arbeitet 0428-083), stopp + meldung bei drohender §4.3-kollision.

PR #1715 head c1485721f130, run 44743111417 TERMINAL FAILURE: 'PR · Selected Runtime (atomic/podman/data-capabilities' + 'PR Selected Checks' rot, 16 success/16 skipped. die rote zelle ist NICHT ihr defect: sie hat weder wizard noch consent geaendert, die ursache liegt auf karte 0428-187 (consent-gate-stall, log-beleg dort). unabhaengig davon die abnahme: mutationstest umgeht die owner-guard in RegisterProviderSignals, valkey-regression fehlt, akte fehlte auf main. korrektur ist zugestellt; ihr PR bleibt BIS 187 geloest in 'blocked' gefuehrt, nicht als review-wait.
