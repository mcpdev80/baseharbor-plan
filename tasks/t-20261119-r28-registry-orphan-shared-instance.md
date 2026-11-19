---
id: t-20261119-r28-registry-orphan-shared-instance
kanban_title: "0428-151 · registry: orphan shared instanz"
card_number: "0428-151"
card_short_title: "registry: orphan shared instanz"
type: task
areas: [capability, lifecycle]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
blocker: ""
wait_reason: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
source_note: "hunt 0428-146 (akte evidence/r28-welle4-2026-11-19/vm-bughunt/baha-podman-146.md, haupt b2adabe7); fund-stelle von MIR am develop 6e87ddcb4 nachgemessen"
evidence:
  - "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/vm-bughunt/baha-podman-146.md"
resolution: ""
created: 2026-11-19
---

- [ ] t-20261119-r28-registry-orphan-shared-instance · orphan shared instanz nach remove #task #release/v0-4-28 #status/planned #view/ready #area/capability #area/lifecycle #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/vm-bughunt/baha-podman-146.md)  
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

## Goal

Nach dem entfernen des letzten verbleibendenverbrauchers bleibt eine ScopeShared-Instanz als Registry-Eintrag (und damit als Doku-/status-oberflaeche) stehen. Auf einer echten Podman-Zelle beobachtet: eine 'sql/shared'-Instanz, deren einziger consumer entfernt wurde, hängt weiter in der registry. Ziel ist ein aufräum-pfad, der Shared-Instanzen entfernt, wenn IHR letzter besitz/rest-binding wegfaellt — ohne dass eine Instanz mit noch lebendem sibling-binding angefasst wird (das ist der bestehende, richtige fall A).

## Scope

- In scope: internal/capability/registry.go, removeUnboundOwnedInstances (:366-390). VON MIR NACHGELESEN am develop 6e87ddcb4: die funktion behaelt (a) alle instanzen mit 'instance.Ownership != OwnershipBaseHarbor' und (b) im 'case ScopeShared:' wird per 'continue' verworfen, im 'case ScopeApplication:' nur bei owner-gleichheit; der rest der zweige faellt durch und wird mit 'instances = append(instances, instance)' BEHALTEN. Der jagd-befund nennt :381-384 als die stelle, an der 'Shared-Instanzen IMMER' bleiben — pruefe das an deinem kopf, bevor du aenderst (§4.7).
- Out of scope: die consent-aequivalenz-frage (karte 0428-119, laufende korrektur) und jede aenderung an internal/application/**.

## Acceptance

- Nach dem entfernen des letztenverbrauchers ist die Shared-Instanz NICHT mehr in der registry, und ein 'baha app status'/'doctor'-pfad zeigt sie nicht mehr.
- Der fall 'Shared-Instanz mit weiter bestehendem sibling-binding' bleibt UNANGETASTET (regression fuer beide richtungen, positiv + blockend).
- Kein neuer zustands-behaälter: die entscheidung muss aus den bestehenden bindings + ownership feldernableitbar sein (bhrule: kein state ohne vertrag).

## Required checks

- **Modified features:** go test ./internal/capability -run '^Test(Registry|RemoveUnbound|Provider|External)' und die lifecycle-regression am gleichen pfad; neue tests muessen vom 'PR · Go unit'-shard ausgefuehrt werden (CI-aufnahmepflicht).
- **CI integration:** exact-head-lauf bis terminal; runtime-zellen koennen SKIPPED bleiben (owner-draht 114(a)) und sind dann als nicht erbracht zu nennen (§5.4).
