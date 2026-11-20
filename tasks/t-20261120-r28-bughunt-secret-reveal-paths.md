---
id: t-20261120-r28-bughunt-secret-reveal-paths
kanban_title: 0428-171 · hunt secret reveal paths
card_number: "0428-171"
card_short_title: "hunt secret reveal paths"
type: review
areas: [security, runtime]
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
evidence: []
prs: []
created: 2026-11-20
---

- [ ] t-20261120-r28-bughunt-secret-reveal-paths · audit where secrets land in clear text #task #release/v0-4-28 #status/planned #view/ready #area/runtime #area/security #kind/review
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

## Ziel

Bug-Hunt H-V14 (reine Befundung, KEINE Produktänderung). Prüfschnitt: wo liegt beim
reveal/access-Pfad ein Secret im Klartext, und wo wird es gelöscht oder eben nicht?

## Anker (develop, von mir gemessen)

- `cmd/baha/app_access.go`, `cmd/baha/app_access_urls.go` (aus den PR-Dateien von #1623/#1627)
- Karte 0428-057 'separate human/runtime secret reveal' (#1615) ist gemergt — der
  getrennte Pfad ist also Bestand und wird auf Löcher geprüft, nicht auf Existenz.
- Befund 0428-151 (invalid org environment key) wurde am 2026-11-20 als false positive
  geschlossen; diese Jagd prüft den Weg NEU, ohne die alte Annahme zu wiederholen.

## Schnitte

1. human vs. runtime reveal: zwei getrennte Pfade? Welcher Pfad schreibt wohin (stdout,
   datei, log, registry)?
2. aufhebung: wird ein einmal gerenderter/enthüllter wert wieder aus zustand/protokollen
   entfernt, oder bleibt er?
3. zugriffs-prüfung: jeder reveal-pfad mit berechtigung? fehlende prüfung = fund mit
   datei:zeile.
4. invalid-input: unvollständige/ungültige keys — fail-closed oder stiller leerwert?

## Regel

Keine Produktänderung, keine Kartenentscheidung. Akte mit datei:zeile je Aussage,
vorher/nachher-liste container/netzwerke/volumes + 'cleanliness:'-zeile. Gefundene
Secret-dateien nur als METADATUM festhalten (pfad, eigentümer, modus, alter) — inhalt
NICHT lesen, nicht kopieren (§5.6), sofort an den coordinator melden.
