---
id: t-20261119-r28-bughunt-lifecycle-consent-desk
kanban_title: "0428-146 · hunt lifecycle/consent desk"
card_number: "0428-146"
type: task
areas: [runtime, ownership, qa]
release: v0.4.28
version: ""
parent: ""
owner: w146-0428-146-huntlifecycle
kanban_status: active
kanban_lane: active
blocker: ""
wait_reason: ""
depends_on: []
repos: [mcpdev80/baseharbor]
evidence:
  - "https://github.com/mcpdev80/baseharbor/commit/1019190d8dc0ecac7693f3461153e76be0e2cb8a"
  - "https://github.com/mcpdev80/baseharbor/commit/8dccd4fe1"
resolution: ""
created: 2026-11-19
card_short_title: "hunt lifecycle/consent desk"
---

- [ ] t-20261119-r28-bughunt-lifecycle-consent-desk · hunt lifecycle/consent desk #task #release/v0-4-28 #status/active #view/active #area/ownership #area/qa #area/runtime #kind/task
    <!-- generated:card -->
    **Owner:** w146-0428-146-huntlifecycle  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/1019190d8dc0ecac7693f3461153e76be0e2cb8a), [proof 2](https://github.com/mcpdev80/baseharbor/commit/8dccd4fe1)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w146-0428-146-huntlifecycle  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Reine Befundung der gemergten runtime-/eigentuems-/consent-flaeche auf develop in einer echten rootless-podman-zelle. Karten-Gefaess fuer die Funde dieses schnitts (Fund→Karte-Pflicht), damit nichts kartenlos verdampft.

## Object of audit (nur CLOSED/merged = develop-Stand)

- `1019190d8dc0ecac7693f3461153e76be0e2cb8a` [0428-084] Perses lifecycle commands: enable/status/disable + ownership-safe remove (#1598).
- `8dccd4fe1` (PR #1683, 0428-106) CLI destructive-consent pfade: kein deutscher 'Achtung'-fallback mehr, konsistente EN-marker.
- `0234e9aa8` (PR #1600, 0428-095) batched Podman ownership + Quadlet inspection.
- `145f98b9c` (PR #1664, 0428-118) guided rootless bootstrap.

## Pruefschnitt (was die Bahn konkret durchspielt)

1. enable → status → disable → remove an einer echten rootless-podman-application: bleibt der eigentuems-nachweis korrekt, und verweigert 'remove' zurecht, wenn ein FREMDDES objekt denselben namen haelt (ownership-safe, nicht 'last writer wins')?
2. Nach einem abgebrochenen enable (hostmittel weg, network belegt): welcher zustand bleibt zurueck, und ist disable/remove damit noch moeglich? Der fall 'partial state' ist der eigentliche pruefstein.
3. Consent-pfade (zerstoerische befehle) in BEIDEN sprachen: jeder zerstoerische pfad muss den landessprachlichen marker korrekt fuehren (EN 'Warning', DE 'Warnung') und der abbruch muss denselben text zurueckgeben wie der bestaetigungs-pfad. Abweichungen = doku-/ux-befund mit datei:zeile.
4. Rootless bootstrap gefuehrt: fuert der guided weg wirklich zu einem lauffaehigen zustand, oder braucht er einen schritt, den die doku nicht nennt? Jeder undocumented-schritt ist ein befund.

## Rules of the lane

Keine produkt-aenderungen, keine PRs, keine aenderungen an `.github/**` oder `scripts/**` (befunde mit datei:zeile an den Coordinator). vm-lock claim/release-Pflicht, HA-szenarien ausgeschlossen. Akte: `evidence/r28-welle4-2026-11-19/vm-bughunt/<host>.md` mit `## PLAN` (nummeriert, OHNE markdown-checkboxen), Befunde nach schwere (blocker/ux/daemm/doku) mit befehlsgenauem repro, vorher/nachher-liste der container/netzwerke/volumes und 'cleanliness:'-zeile. Fremde container (auch perses-probe-/deny-perses-/proto-perses-artige) bleiben UNANGETASTET, nur melden.

## Stop criteria

podman-zelle nicht erreichbar, linger/netns-haenger (exit 126, 'Cannot assign requested address') nicht loesbar, oder vm-lock streitig → STOP + Meldung an den Coordinator. Funde werden in DIESER karte nicht behoben, sondern in eigene bug-karten gegossen.

fund-zu-karte-pflicht erfuellt: 0428-187 traegt den fund; die hunt-akten hunt-signals-103/-104 sind geschlossen.

ARBEITET JETZT, kante gegen session gemessen (8f3509c0, laptop): hunt-schnitt H-V18 'aenderungs-desk der heutigen merges' - (1) grant-bindung aus #1717/0428-188: haelt der grant genau EINE operation (apply nach check, destroy nach check, zweiter aufruf pro invocation), (2) consent-stufen: gibt es einen pfad, der eine antwort als beide wertet, oder text-abweichung gegen provider_change_consent.go:37, (3) upgrade/rollback: neuer code auf altem state-file (0428-168, #1711, #1713). reine befundung, keine produktaenderung, FUND-FUER-KARTE-zeile pro fund; die registry.go-funde von heute (189-194) sind als bereits-karten ausgeschlossen.
