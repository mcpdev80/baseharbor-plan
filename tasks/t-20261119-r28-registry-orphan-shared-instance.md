---
id: t-20261119-r28-registry-orphan-shared-instance
kanban_title: "0428-151 · registry: orphan shared"
card_number: "0428-151"
card_short_title: "registry: orphan shared"
type: task
areas: [capability, lifecycle]
release: v0.4.28
version: ""
parent: ""
owner: codex-open-pr-sweep-0428-151
kanban_status: active
kanban_lane: active
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

- [ ] t-20261119-r28-registry-orphan-shared-instance · orphan shared instanz nach remove #task #release/v0-4-28 #status/active #view/active #area/capability #area/lifecycle #kind/task
    <!-- generated:card -->
    **Owner:** codex-open-pr-sweep-0428-151  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/vm-bughunt/baha-podman-146.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** codex-open-pr-sweep-0428-151  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Nach dem entfernen des letzten verbrauchers bleibt eine ScopeShared-instanz als registry-eintrag (und damit auf jeder oberflaeche, die daraus liest) bestehen. Auf einer echten Podman-zelle beobachtet. Ziel: die retention auf dem destroy-/retirement-pfad so zu entscheiden, dass eine shared instanz nur dann zurueckkehrt, wenn nach dem release NOCH ein binding auf sie zeigt — ohne dass eine instanz mit lebendem sibling-binding angefasst wird.

PREMISE-CORREKTUR (von der lane gemeldet, von MIR UND DEM OWNER am stand entwickelt nachgemessen): die urspruengliche vermutung (und der wortlaut der hunt-akte) zeigte auf internal/capability/registry.go:381-384 removeUnboundOwnedInstances. DIE STELLE IST RICHTIG: 'case ScopeShared: continue' springt vor dem append weg — die instanz wird ALSO ENTFERNT, wenn kein binding mehr auf ihr steht (referenced-set wird :367-370 global ueber alle bindings aufgebaut). Das wort 'continue' war der les-fehler. DIE WIRKLICH UNDICHTE STELLE ist der wieder-eintragungs-loop auf dem destroy-pfad.

## Scope

- In scope: internal/application/provider_registry.go, ReleaseApplicationProviderRegistryAt (gemessen develop 28fb427f, :270-290): die funktion sammelt ZUERST JEDE ScopeShared-instanz in 'retained', ruft 'registry.ReleaseApplicationDeployment(m.ApplicationID, m.Environment)' und registriert dan ALLE gespeicherten instanzen per 'registry.Register(instance)' WIEDER — ohne blick auf die bindings. Eine orphan-shared-instanz (bindings = 0) aufersteht auf diesem pfad. Produktions-aufrufer gemessen: cmd/baha/app_destroy_lifecycle.go:714, cmd/baha/app_runtime_retirement.go:78, cmd/baha/runtime_destroy_all.go:388 (tests: cmd/baha/app_core_requirement_test.go:202, cmd/baha/runtime_openbao_registry_test.go:39, cmd/baha/shared_core_dedup_runtime_test.go:38).
- Out of scope: internal/capability/registry.go — dort ist das verhalten nachweislich richtig; ein 'defense in depth' dort ist ein scope-verstoß ohne befund (§4.2, owner-entscheidung 2026-11-19: 'Do not add the unrelated registry.go defense-in-depth change; the original hunt premise at that file was disproven'). Ebenso ausserhalb: jede neue zustands-ablage, jedes neue manifest-feld (kein state ohne vertrag).
- Kollisions-pruefung gemessen: karte 0428-119 aendert internal/application/provider_consent_authority.go (andere datei, disjunkt), karten 0428-123/073/083 internal/metrics/**, 0428-142 cmd/baha/app_status_*.go — die write-sets dieser karte sind disjunkt.arbor' und (b) im 'case ScopeShared:' wird per 'continue' verworfen, im 'case ScopeApplication:' nur bei owner-gleichheit; der rest der zweige faellt durch und wird mit 'instances = append(instances, instance)' BEHALTEN. Der jagd-befund nennt :381-384 als die stelle, an der 'Shared-Instanzen IMMER' bleiben — pruefe das an deinem kopf, bevor du aenderst (§4.7).

## Acceptance

- Nach dem entfernen des letztenverbrauchers ist die Shared-Instanz NICHT mehr in der registry, und ein 'baha app status'/'doctor'-pfad zeigt sie nicht mehr.
- Der fall 'Shared-Instanz mit weiter bestehendem sibling-binding' bleibt UNANGETASTET (regression fuer beide richtungen, positiv + blockend).
- Kein neuer zustands-behaälter: die entscheidung muss aus den bestehenden bindings + ownership feldernableitbar sein (bhrule: kein state ohne vertrag).

## Required checks

- **Modified features:** go test ./internal/capability -run '^Test(Registry|RemoveUnbound|Provider|External)' und die lifecycle-regression am gleichen pfad; neue tests muessen vom 'PR · Go unit'-shard ausgefuehrt werden (CI-aufnahmepflicht).
- **CI integration:** exact-head-lauf bis terminal; runtime-zellen koennen SKIPPED bleiben (owner-draht 114(a)) und sind dann als nicht erbracht zu nennen (§5.4).

fund->karte erfuellt; lane dispatched auf laptop:2 mit meiner eigenen messung der stelle (removeUnboundOwnedInstances behaelt ScopeShared unbedingt, registry.go:366-390 am develop 6e87ddcb4)
