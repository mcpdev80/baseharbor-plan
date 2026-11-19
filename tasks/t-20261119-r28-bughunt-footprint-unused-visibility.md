---
id: t-20261119-r28-bughunt-footprint-unused-visibility
kanban_title: 0428-157 · hunt footprint unused sight
card_number: "0428-157"
card_short_title: "hunt footprint unused sight"
type: bughunt
areas: [capability, lifecycle, cli]
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
source_note: "fuell-hunt nach AGENTS 3.3 punkt 5 (kein abhaengigkeitsfreie karte fuer den freien sitz ornith:2); anlass ist der 0428-151-befund, der als vertragsstreu endete: cmd/baha/app_core_requirement_test.go:192 verlangt eine shared instanz mit null bindungen, internal/application/footprint.go:345-347 rechnet Unused aus '!selected && keine bindings'. Reine befundung, keine produkt-aenderung."
evidence: []
resolution: ""
created: 2026-11-19
---

- [ ] t-20261119-r28-bughunt-footprint-unused-visibility · destroy-pfade und unused-sicht pruefen #task #release/v0-4-28 #status/planned #view/ready #area/capability #area/cli #area/lifecycle #kind/bughunt
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
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

Hunt (nur befundung): die destroy-/retirement-pfade des provider-bestands gegen die footprint-sicht pruefen. Die frage ist nicht, ob eine orphan-instanz entfernt wird (0428-151 hat gezeigt, dass das entfernt-wollen den vertrag bricht), sondern ob die SICHT luegt: kann eine instanz doppelt erscheinen (Unused + Existing/Additional), kann sie unsichtbar werden, obwohl ein besitzer sie noch erwartet, und verhalten sich die drei destroy-eingaenge unterschiedlich?

## Scope

- In scope: lesen und lokale unit-laeufe in internal/capability/registry.go, internal/application/provider_registry.go, internal/application/footprint.go, internal/application/app_runtime_retirement.go, cmd/baha/app_destroy_lifecycle.go, cmd/baha/app_runtime_retirement.go, cmd/baha/runtime_destroy_all.go.
- Out of scope: JEDE produkt-aenderung (diese karte hat keinen PR), jede container-/VM-arbeit (diese bahn nutzt keine zelle, damit der vm-lock frei bleibt), jede aenderung an den dateien, in denen andere bahnen gerade schreiben (0428-119 provider_consent_authority.go).

## Acceptance

- Akte mit je fund: szenario, erwartet (vertrag), ist (gemessen), datei:zeile, wirkung auf die user-sicht, stufe, repro-befehl — und je ungeflaggtem verhalten eine zeile 'VERHALTEN KORREKT' mit dem testnamen als zeugen.
- Die schreibenden pfade des provider-bestands sind vollstaendig aufgelistet (zaehlung + datei:zeile), damit ein reviewer sieht, was der schnitt abdeckt und was nicht.
- Alle funde sind innerhalb eines tages in karten gegossen (Fund→Karte-Pflicht des coordinators, §3.3 punkt 5); die akte verweist auf die Kartennummern, die ich setze.

## Required checks

- **Modified features:** keine — therefore 'go test' dient nur als beweis-mittel der befundung, nicht alsnderung: 'go test ./internal/application -count=1 -run "^(TestFootprint|TestCapabilityRemoval|TestProviderRegistry|TestRelease)"' und 'go test ./internal/capability -count=1 -run "^(TestRegistry|TestRemoveUnbound|TestProvider|TestExternal|TestShared)"', exit-codes und abgedeckte testnamen in der akte.
- **CI integration:** kein gehosteter lauf erforderlich und keiner erwartet (grund in der akte: nur befundung, kein diff). Ein etwaiger skipped-hinweis ist damit kein mangelpunkt dieser karte.
