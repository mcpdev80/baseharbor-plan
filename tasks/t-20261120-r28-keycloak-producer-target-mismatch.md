---
id: t-20261120-r28-keycloak-producer-target-mismatch
card_number: "0428-185"
card_short_title: "producer target mismatch"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: 0847d100 (lane, messung) / coord (abgleich)
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-185 · producer target mismatch
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/keycloak-producer-0428-185/round-1.md"]
---

- [x] t-20261120-r28-keycloak-producer-target-mismatch · Keycloak producer registers ID/target the identity witness can never match #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/bug
    <!-- generated:card -->
    **Owner:** 0847d100 (lane, messung) / coord (abgleich)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/keycloak-producer-0428-185/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** 0847d100 (lane, messung) / coord (abgleich)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Found by the owner's Codex takeover of 0428-078 (2026-11-20, finding-to-card duty AGENTS 3.3.5)

Measured while the owner completed 0428-078: internal/identityprovider/keycloak_realization.go registers the signal with id 'keycloak:<files.Project>' and target 'keycloak:9000', while internal/metrics/perses_identity_witness.go looks for the name 'keycloak-metrics' with target = m.Name. The two spellings never coincide, so the witness rejects a genuine production record. This is the root cause behind the P3 blocker of review 1650-0428-078-r8.md: target isolation cannot be proven while the producer and the witness disagree about what a target is.

## Acceptance

1. One canonical identity for the produced signal (name and target) chosen in the producer or in the witness, not both patched independently; write the chosen form into a comment where it is read.
2. A regression that registers the REAL producer record and asserts the witness accepts it (positive direction) and that a foreign target still fails (negative direction).
3. If target-uid/state-root scoping needs a schema change in internal/observability/registry.go or provider_registration.go (today the registryPath is global, without target uid/root): that change belongs to the card that owns those files for this release - coordinate before editing, see AGENTS 4.3.

## Boundaries

internal/identityprovider/keycloak_realization.go plus internal/metrics/perses_identity_witness.go. internal/observability/registry.go and provider_registration.go are released to the 0428-078 takeover work for the target-root change; 0428-184 is confined to its destroy-side cleanup. No .github/**.

BEAUFTRAGT AUF EINER FREI GEWORDENEN ausfuehrenden lane (0847d100, nach abgabe von 0428-091):arbeit beginnt bei der card-messe, dann branch lane-0428-185-producer-target auf develop acc34323968, write-set ist ausschliesslich internal/identityprovider/keycloak_realization.go plus internal/metrics/perses_identity_witness.go. STOP ist vorgespannt, wenn ziel-uid-/state-root-scoping ein schema-wechsel in internal/observability/registry.go oder in provider_registrations verlangt (acceptance 3, owner-scope). Kein dependency zu anderen karten, kein konflikt mit den laufenden kandidaten: die tempo-datei in internal/metrics wird von PR 1645 angefasst, diese karte nicht.

KARTE WIRD AUFGEGEBEN, weil ihre PRAMISSE NICHT EXISTIERT - gemessen von zwei seiten. (1) meine messung: internal/identityprovider/keycloak_realization.go ist auf develop 8629450ef3c DA, internal/metrics/perses_identity_witness.go FEHLT dort; der witness steht nur auf dem branch von 0428-078 (PR 1650, head 28c18f02039). (2) die lane misst zusaetzlich: producer und witness SAGEN BEIDE keycloak:<project> mit target keycloak:9000 (registerKeycloakSignals, KeycloakMetricsRegistrationIDAt ueber dieselbe keycloakStateIdentity; witness filtert genau diese id und dieses target) - die auf der karte behauptete ziel-verwerfung (target=m.Name) passt nicht zum witness-code. Damit ist kein fehler zu beheben: auf develop gibt es den witness nicht, auf dem 0428-078-branch sind sich beide einig. WAS BLEIBT: 0428-078/#1650 braucht bei der abnahme den hinweis, dass ihr target-isolation-test synthetische datensaetze setzt statt des echten producer-datensatzes (acceptance-punkt 2 dieser karte) - ich haenge den hinweis an die 078-karte, sobald sie in die pruefung geht. Kein produkt-aenderung, kein PR aus dieser karte.

KARTE WIRD AUFGEGEBEN, weil ihre PRAMISSE NICHT EXISTIERT - gemessen von zwei seiten. (1) meine messung: internal/identityprovider/keycloak_realization.go ist auf develop 8629450ef3c DA, internal/metrics/perses_identity_witness.go FEHLT dort; der witness steht nur auf dem branch von 0428-078 (PR 1650, head 28c18f02039). (2) die lane misst zusaetzlich: producer und witness SAGEN BEIDE keycloak:<project> mit target keycloak:9000 (registerKeycloakSignals, KeycloakMetricsRegistrationIDAt ueber dieselbe keycloakStateIdentity; witness filtert genau diese id und dieses target) - die auf der karte behauptete ziel-verwerfung (target=m.Name) passt nicht zum witness-code. Damit ist kein fehler zu beheben: auf develop gibt es den witness nicht, auf dem 0428-078-branch sind sich beide einig. WAS BLEIBT: 0428-078/#1650 braucht bei der abnahme den hinweis, dass ihr target-isolation-test synthetische datensaetze setzt statt des echten producer-datensatzes (acceptance-punkt 2 dieser karte). Kein produkt-aenderung, kein PR aus dieser karte. Plan-hygiene: checkbox-zeilen in der akte round-1.md wurden von mir bereinigt (sonst falsch-karten im board).

KARTE WIRD AUFGEGEBEN, weil ihre PRAMISSE NICHT EXISTIERT - gemessen von zwei seiten. (1) meine messung: internal/identityprovider/keycloak_realization.go ist auf develop 8629450ef3c DA, internal/metrics/perses_identity_witness.go FEHLT dort; der witness steht nur auf dem branch von 0428-078 (PR 1650, head 28c18f02039). (2) die lane misst zusaetzlich: producer und witness SAGEN BEIDE keycloak:<project> mit target keycloak:9000 (registerKeycloakSignals, KeycloakMetricsRegistrationIDAt ueber dieselbe keycloakStateIdentity; witness filtert genau diese id und dieses target) - die auf der karte behauptete ziel-verwerfung (target=m.Name) passt nicht zum witness-code. Damit ist kein fehler zu beheben: auf develop gibt es den witness nicht, auf dem 0428-078-branch sind sich beide einig. WAS BLEIBT: 0428-078/#1650 braucht bei der abnahme den hinweis, dass ihr target-isolation-test synthetische datensaetze setzt statt des echten producer-datensatzes (acceptance-punkt 2 dieser karte). Kein produkt-aenderung, kein PR aus dieser karte. Plan-hygiene: checkbox-zeilen in der akte round-1.md sind bereinigt (plan main siehe remote-zeile).
