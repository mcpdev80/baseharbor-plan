# Vorgemerkte Missionen (Warteschlange, durch Tick zu prüfen)

Frei wird ein Platz, sobald eine Lane plattenfest abgeliefert und released ist. Eintrag löschen, sobald die
Lane dispatcht wurde. Der Audit-Punkt "POOL" zeigt beim Tick, ob ein Platz frei ist.

| 0 | coordinator/missions/w127-team-auth-r2.txt | Pool 5/5 | Team-Anmeldung Runde 2 (review-1369a REJECT: kein Fail-closed ohne Anbieter, Produktionsanbieter fehlt,schreibfeld-fremde dateien) |
| 00 | coordinator/missions/cx04-ci-delivery.txt | Codex-Worker-Sitz belegt (cx02) | Owner-Massnahme: Go/Docker/DB-Testursache eingrenzen (Hebel fuer 12 nachfolgende aufgaben) |
| # | Mission | Warum noch nicht dispatcht | Nächster Auslöser |
| --- | --- | --- | --- |
| 1 | coordinator/missions/w125-native-auth-r4.txt | Pool 5/5 | native-auth runde 4 (review-1362b REJECT: broker nicht im pfad, leer-treffer == erfolg) |
| 2 | coordinator/missions/w123-codec-r3.txt | Pool 5/5 belegt | Profil-Kodierung Runde 3 (review-1363b REJECT: secret-felder, atomarer commit, vertrauenspflicht, vollständiger rundlauf, gates) |
| 2 | ~~w121-podman-rebuild~~ | ERLEDIGT-DURCH-ANDEREN | Podman-Host läuft jetzt in codex-ops-podman (zweite Codex-Instanz, Owner-Direktive 17:5x). w121 bleibt als Fallback-Mission, wird NICHT doppelt dispatcht (ein Host, ein Bearbeiter). |
| 3 | VM-Folgeauftrag Docker-Host: keycloak-stapel crasht in schleife (datenbankzertifikat wird stapeluebergreifend falsch aufgeloest) — down/up mit berichtigter zertifikatsangabe, definition liegt vor | Pool 5/5 belegt | naechster freier ornith-sitz |
| 4 | ~~w119-journal-r2~~ | ERLEDIGT | wurde von cx01 (Codex-Worker) geliefert: head 11ed442e, Karte auf review, Luna prueft | Pool 4/4 | Ausführungstagebuch-Runde 2 (Codex review-1373a REJECT, fünf Rezepte) |
| 4 | coordinator/missions/w118-connector-fmt.txt | Pool 4/4 | Connectort-Antrag #19 hat nur den roten Source-Format-Job |

## Tor vor der Integrationsphase

Die eigentlichen Docker-/Podman-Integrationstests (Karte t-20261104-r27-vm-integration-runs) starten erst, wenn
beide Rechner ein `baha` aus der geprüften Quellrevision melden. Befund 2026-11-04: auf beiden Hosts lag
BaseHarbor 0.4.23, auf dem Podman-Rechner wurde diese alte Version heute sogar vom Setup-Skript neu
installiert. Läufe gegen 0.4.23 zählen nicht als Test.

## Kanalbesetzung

- `codex-luna-ch` (d9eca6e7): Abnahme-Kanal, gerade leer, weil kein Kandidat eine grüne Pflichtprüfung hat.
- `codex-pod-ops` (a0ce49b3, zweite Instanz, Owner-Direktive 2026-11-04): OPS-Auftrag Podman-Host.
  Rollenhygiene: dieser Kanal führt einen ausdrucklich als OPS gekennzeichneten Auftrag aus — er schreibt kein
  Review-Urteil und merged nichts; die Revisions- und Versionsnachweise legt er als Evidence ab.
| 9 | coordinator/missions/w126-gate-watch.txt | Pool 5/5 | vier kandidaten haben nicht-terminale gehostete laeufe; abnahme braucht das terminal-bild + klassifikation |

## Einstweilen (2026-11-04, ~02:20)
- w131-consent-abort-r2.txt — Runde 2 für PR #1375 (Abnahme review-1375a REJECT): echter destroy-Durchlauf mit
  rc=0 und echte Folgeanwendung bis READY, vorher rot. Nächster Auslöser: erster freier Worker-Sitz.
- cx05-ci-skip-fix.txt — läuft (Codex-Arbeitersitz): Scheingrün-Überspringung wird echtes Fail.
- w132-enroll-rollback.txt — product regression behind the enrollment candidate (migration rollback drops more
  than the last change). Next trigger: first free worker seat. Prerequisite noted: do NOT touch the DSN fix
  (belongs to PR #1377).
- w133-codec-r6.txt — Runde 6 für PR #1363 (review-1363d REJECT): doppelter Schreibvorgang im atomaren
  Abschluss muss weg, Kurzschreib-Beweis mit n<len-Wert, Vertrauen ohne Schalter, Rundlauf mit vollständigem
  Datensatz plus goldenen Bytes, Canary je Kategorie, Aufräumfehler typisiert, EN/DE parallel.
  Nächster Auslöser: erster freier Worker-Sitz (der_codec-Kopf 064ba01820b bleibt bis dahin in review).

## Einstweilen (2026-11-04, ~04:40) — nach der Hebelkarten-Verbindung (develop 2ea2c6f1)
- w135-native-auth-base.txt — PR #1362 auf neue Hauptlinie mergen (nur basis, DB-Paarung muss grün werden),
  der restliche Fehl (Anwendungsänderung / Tresordienst) als Befund von t-20261018-r27-state-owner BENENNEN.
  Auslöser: erster freier Sitz. Danach analog für #1369 (team-auth, falls dasselbe Bild) und #1347.
- Bereits angesetzt: w134 (Journal #1373) läuft.
- codex-r1363e.txt — Abnahme profil-codec Runde 6 (Kopf ac6a048e290). Auslöser: Luna ist nach der
  Zustimmungsrunde (#1375) frei. Der Codex-Arbeitersitz darf sie NICHT prüfen (eigene Lieferung).
- codex-r1371b.txt — Abnahme Geräteregelung (Kopf 8d3531f03ec, zwölf grün). Auslöser: Luna nach #1375 frei.
  Prüfschwerpunkt: Rückbau folgt der Stufenliste, Überspringen ohne Verbindung ist kein Scheingrün mehr.

## Einstweilen (2026-11-04, ~07:25)
- w138-consent-abort-r3.txt — läuft seit ~07:40 auf Lane w138 (PR #1375, Runde 3).
- codex-r1373c.txt — Abnahme Ausführungsprotokoll (Kopf 0d89a13e63a, acht grün). Auslöser: freier Prüfkanal.
  Schwerpunkt: eigene Rückbau-Gegenprobe (Hintergrund writers zurück => Prüfung muss rot werden).
- codex-r1378a.txt — Abnahme Umgebungsfehlstellen (Kopf aca8ff97df8, acht grün). Auslöser: freier Prüfkanal.
  Enthält meine Bitte an die Prüferseite, die vollständige Überspringliste selbst zu klassifizieren.
- ~~w143-enroll-r4.txt~~ — Makulatur (w146-runde5 uebernimmt, review-1371c-rezepte eingearbeitet).
  Regelableitung + Stufenmutation rein, drei Datenbankprüfungen ohne Überspringen; Dateizuschnitt gegen #1378
  im Auftrag. Auslöser: erster freier Sitz (alle fünf belegt).
- ~~w145-native-witness.txt~~ — STORNIERT (Owner-Direktive): #19 komplett an ChatGPT übergeben
  (CI, Review, Merge, Planning-Abschluss). Kein Prüfkanal-Auftrag r19d mehr, keine Zeugnahme, keine
  Kartenschließung durch uns. Missionen codex-r19*.txt und w*-connector*.txt sind Makulatur.
- cx10-base-refresh.txt — läuft auf dem Arbeitersitz (drei Äste auf develop e444ae11).
- ~~w146-enroll-r5.txt~~ — erledigt (lieferung gemessen, karte im fluss).
  Ruecknamedatei, AGENTS.md aus dem Antrag. Ausloeser: erster freier Sitz (ornith/laptop voll).
- ~~w147-journal-r4.txt~~ — erledigt (lieferung gemessen, karte im fluss).
  sleep-freie Tests (Luna review-1373c REJECT, drei Rezepte). Auslöser: erster freier Sitz.
- Basis-Refresh LAEUFT als w148 (alle drei Äste auf develop ea3fb38e).
  develop e444ae11 heben, Exakt-SHA-Reviews danach neu. Auslöser: zweiter freier Sitz.
- w149-base-refresh2.txt — ERLEDIGT-TEIL: #1378=760c104a6c4 (lauf 41922518146 in arbeit, Beobachtung ist
  jetzt BEI MIR, Uebergabe dokumentiert); #1373-Basis macht w147 mit seiner eigener lieferung.
- SPERRVERMERK (Direktive): alle connector-seitigen Aufgaben (node-trust-Scope: Zertifikatsrotation,
  Widerruf, mTLS-Vertrauen, Session-Wiederherstellung, Reconnect) liegen bei ChatGPT. Keine Reservierung,
  kein Dispatch, keine Abnahme. Abhängige Karten erst nach deren bestätigtem Merge + Plan-Abschluss.
- w150-vm-integration.txt — LAEUFT (laptop-Sitz 2/2): beide Test-VMs aus setup-Skripten auf develop
  ea3fb38e neu + echter Integrationslauf inkl. Zerstörungsfall. Lücke war ein Dispatch-Versäumnis von mir.
- w151-candidate-pack.txt — LAEUFT (ornith): bounded source-snapshot packer, fünf Pflichtfallgruppen.
- w152-neutral-probe.txt — LAEUFT (ornith): neutrale Positivzelle mit freiem Port für #1378 (review war
  BLOCKED durch sandbox-Port, nicht durch Produktbefund; gehosteter Lauf inzwischen terminal success).
- t-20261018-r27-ci-lanes — NICHT dispatchen: Arbeitsanweisung liegt bei CODEMAN-START.md (Owner-Feld).
- w153-node-streams.txt — LAEUFT (ornith): stream-nachweise a-d auf connector main 346e5ae77ff.
  ist closed/accepted, Plan-CI #41926483152 success — von mir gemessen). Connector-Dateien: enger
  Schreibsatz der Karte (targetaccess/session*, outbound*), niemals die von ChatGPT hinterlassenen Pfade
  parallel; basis main 816720c+ frisch fetchen.
- w154-destroy-aborted-apply.txt — LAEUFT (ornith): neue bug-karte aus VM-reproduktion (zerstoerung nach
  abgebrochenem provider-wechsel). #1378c ACCEPT → merge befohlen; candidate-pack #1381 in pruefung.
- w157-compose-baseline.txt — LAEUFT (laptop): Matrix develop-512 vs journal-52e fuer die vier Compose-
  tests + Panic-Wortlaut; Entscheidung Grundlage fuer #1373-runde-5 oder Vor-Bestand-Karte.
- t-20261105-r27-compose-host-isolation — Hebelkarte (gemessen, cross-branch). Erste freie Bahn:
  Gegenprobe mit absichtlich verseuchtem shared state + isolierte pro-test daemon-leitung.
- w156-destroy-r2.txt — ERLEDIGT: runde 2 head 3691173821 in pruefung (r1382b).
- w158-destroy-r3.txt — ERLEDIGT: runde 3 head d1f4eada327, r1382c beauftragt (ACCEPT => merge).
- w159-compose-isolation.txt — LAEUFT (desktop): Hebelkarte gegen Compose-Verseuchung, Gegenproben-pflicht.
- w161-device-lifecycle.txt — wartet auf ersten freien sitz (ornith voll, w160/w159 arbeiten).
- w162/w163 LAEUFT (laptop x2). ruhe: #1373/#1379/#1380 urteile (read-only) an luna uebergeben.
- w164-connection-r2.txt — Warteschlange (prioritaet 1 beim naechsten freien sitz): rezept 1380a = echte
  CLI-Pfad-Verbindung zu ConnectionSelection.Resolve.
- w165-journal-r5.txt — Warteschlange (p2): sleep-Polling raus, kanal-ordnung, race-20, mutante.
- w166-private-gate.txt — Warteschlange (p3, klein): PR #1379 ready machen + Selected Checks beobachten.
- w167-profiles-r2.txt — Warteschlange (p1): access-profiles korrektur nach 1384a (zweite wahrheit -> eine).
- w165-journal-r5.txt — Warteschlange (p2). w166-private-gate.txt — Warteschlange (p3).
