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
owner: w171-pr0428-171-revealhunt
kanban_status: closed
kanban_lane: closed
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/bughunt-secret-reveal-paths/round-1.md"]
prs: []
created: 2026-11-20
wait_reason: ""

---

- [x] t-20261120-r28-bughunt-secret-reveal-paths · audit where secrets land in clear text #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/runtime #area/security #kind/review
    <!-- generated:card -->
    **Owner:** w171-pr0428-171-revealhunt  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/bughunt-secret-reveal-paths/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w171-pr0428-171-revealhunt  
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

jagd H-V14 BEFUNDLOS fuer die vier schnitte (human/runtime reveal, aufhebung, zugriffspruefung, invalid input) — alle vier 'VERHALTEN KORREKT' mit pruefweg, build/vet/293 tests clean. ihre erste END war zurueckgewiesen (gemeldeter stand 0000...0000, kein branch, keine akte auf main); die nachlieferung ist echt: akte 11492 bytes @ fbac5cff, checkboxen null, cleanliness-zeile vorhanden. SICHERHEITSBEFUND (§5.6), als metadatum, inhalt nie gelesen: /home/marcel/.codex/auth.json, eigentümer marcel:marcel, modus 600, mtime 2026-11-18 09:14:31 — das ist die anmeldedatei des localen Codex-CLI (nicht aus unserem oekosystem), und sie erklaert die Codeman-installation auf diesem rechner. rotation/entwertung entscheidet der owner; ich habe die lane angewiesen, datei unangetastet zu lassen (kein lesen/kopieren/verschieben/loeschen). weiterfuehrende karte: keine aus diesem schnitt
