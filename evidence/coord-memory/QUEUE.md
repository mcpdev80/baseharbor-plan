# Vorgemerkte Missionen (Warteschlange, durch Tick zu prüfen)

<!-- STAND 2026-11-05 19:1xZ: welle-4-einträge alle geliefert/gemergt; entries 0,00,1,2,3,4,9 geloescht (erledigt ausser plan-bereinigung). -->

Frei wird ein Platz, sobald eine Lane plattenfest abgeliefert und released ist. Eintrag löschen, sobald die
Lane dispatcht wurde. Der Audit-Punkt "POOL" zeigt beim Tick, ob ein Platz frei ist.

| # | Mission | Warum noch nicht dispatcht | Nächster Auslöser |
| --- | --- | --- | --- |

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

## Einstweilen (2026-11-04, ~02:20)
  rc=0 und echte Folgeanwendung bis READY, vorher rot. Nächster Auslöser: erster freier Worker-Sitz.
- cx05-ci-skip-fix.txt — läuft (Codex-Arbeitersitz): Scheingrün-Überspringung wird echtes Fail.
  than the last change). Next trigger: first free worker seat. Prerequisite noted: do NOT touch the DSN fix
  (belongs to PR #1377).
  Abschluss muss weg, Kurzschreib-Beweis mit n<len-Wert, Vertrauen ohne Schalter, Rundlauf mit vollständigem
  Datensatz plus goldenen Bytes, Canary je Kategorie, Aufräumfehler typisiert, EN/DE parallel.
  Nächster Auslöser: erster freier Worker-Sitz (der_codec-Kopf 064ba01820b bleibt bis dahin in review).

## Einstweilen (2026-11-04, ~04:40) — nach der Hebelkarten-Verbindung (develop 2ea2c6f1)
  der restliche Fehl (Anwendungsänderung / Tresordienst) als Befund von t-20261018-r27-state-owner BENENNEN.
  Auslöser: erster freier Sitz. Danach analog für #1369 (team-auth, falls dasselbe Bild) und #1347.
- codex-r1363e.txt — Abnahme profil-codec Runde 6 (Kopf ac6a048e290). Auslöser: Luna ist nach der
  Zustimmungsrunde (#1375) frei. Der Codex-Arbeitersitz darf sie NICHT prüfen (eigene Lieferung).
- codex-r1371b.txt — Abnahme Geräteregelung (Kopf 8d3531f03ec, zwölf grün). Auslöser: Luna nach #1375 frei.
  Prüfschwerpunkt: Rückbau folgt der Stufenliste, Überspringen ohne Verbindung ist kein Scheingrün mehr.

## Einstweilen (2026-11-04, ~07:25)
- codex-r1373c.txt — Abnahme Ausführungsprotokoll (Kopf 0d89a13e63a, acht grün). Auslöser: freier Prüfkanal.
  Schwerpunkt: eigene Rückbau-Gegenprobe (Hintergrund writers zurück => Prüfung muss rot werden).
- codex-r1378a.txt — Abnahme Umgebungsfehlstellen (Kopf aca8ff97df8, acht grün). Auslöser: freier Prüfkanal.
  Enthält meine Bitte an die Prüferseite, die vollständige Überspringliste selbst zu klassifizieren.
  Regelableitung + Stufenmutation rein, drei Datenbankprüfungen ohne Überspringen; Dateizuschnitt gegen #1378
  im Auftrag. Auslöser: erster freier Sitz (alle fünf belegt).
  (CI, Review, Merge, Planning-Abschluss). Kein Prüfkanal-Auftrag r19d mehr, keine Zeugnahme, keine
  Kartenschließung durch uns. Missionen codex-r19*.txt und w*-connector*.txt sind Makulatur.
- cx10-base-refresh.txt — läuft auf dem Arbeitersitz (drei Äste auf develop e444ae11).
  Ruecknamedatei, AGENTS.md aus dem Antrag. Ausloeser: erster freier Sitz (ornith/laptop voll).
  sleep-freie Tests (Luna review-1373c REJECT, drei Rezepte). Auslöser: erster freier Sitz.
  develop e444ae11 heben, Exakt-SHA-Reviews danach neu. Auslöser: zweiter freier Sitz.
- SPERRVERMERK (Direktive): alle connector-seitigen Aufgaben (node-trust-Scope: Zertifikatsrotation,
  Widerruf, mTLS-Vertrauen, Session-Wiederherstellung, Reconnect) liegen bei ChatGPT. Keine Reservierung,
  kein Dispatch, keine Abnahme. Abhängige Karten erst nach deren bestätigtem Merge + Plan-Abschluss.
  ea3fb38e neu + echter Integrationslauf inkl. Zerstörungsfall. Lücke war ein Dispatch-Versäumnis von mir.
  BLOCKED durch sandbox-Port, nicht durch Produktbefund; gehosteter Lauf inzwischen terminal success).
- t-20261018-r27-ci-lanes — NICHT dispatchen: Arbeitsanweisung liegt bei CODEMAN-START.md (Owner-Feld).
  ist closed/accepted, Plan-CI #41926483152 success — von mir gemessen). Connector-Dateien: enger
  Schreibsatz der Karte (targetaccess/session*, outbound*), niemals die von ChatGPT hinterlassenen Pfade
  parallel; basis main 816720c+ frisch fetchen.
  abgebrochenem provider-wechsel). #1378c ACCEPT → merge befohlen; candidate-pack #1381 in pruefung.
  tests + Panic-Wortlaut; Entscheidung Grundlage fuer #1373-runde-5 oder Vor-Bestand-Karte.
- t-20261105-r27-compose-host-isolation — Hebelkarte (gemessen, cross-branch). Erste freie Bahn:
  Gegenprobe mit absichtlich verseuchtem shared state + isolierte pro-test daemon-leitung.
  CLI-Pfad-Verbindung zu ConnectionSelection.Resolve.
  #1380 wieder an (warnung "connection-client active mit offener abhaengigkeit" ist gewollt und ehrlich).
  punkte vor der prüfung (zustimmung fix = nachgewiesen, isolierung = evtl. nicht reproduzierbar).
- t-20261105-r27-snapshot-change-guard-deterministic — NEU (p1 nach laufenden ends): same-head flake
  belegt (41981861515 gruen vs 41983173186 rot, 0.01s), determinischer hook noetig; entpoisoned die gates.
- SPERRVERMERK: #1347 state-owner komplett an Owner+ChatGPT (Direktive 08:0x). Keine Lane dieser Seite in
  internal/application state-owner-Pfade; Abhaengige (u.a. podman-recovery-bootstrap-cleanup,
  mutation-lock-Kette) erst nach deren bestaetigtem Abschluss.
- ENTRIEGELT 2026-11-05: #1347 gemerged (develop 42bfcb1cb4). Fuenf abhaengige Welle-4-Karten geplant frei:
  app-binding, management-host, mutation-lock, stage-versions, state-recovery — Besetzung nach Kapazitaet,
  basis ist jetzt 42bfcb1cb4 fuer ALLE neuen schnitte (missionstexte beim naechsten dispatch anpassen).
- Welle-5 eroeffnet: app-binding LAEUFT (laptop), mutation-lock = p1 naechste (dependencies all closed),
  stage-versions/state-recovery/management-host weiter gesperrt (planned vorginger: device-lifecycle,
  journal-wiring, candidate-ingress, app-binding).
  journal r7/streams r4 laufen. credentials-r4 p2.
- COMPOSE-GATE: OWNER-BLOCKER (daemon.json default-address-pools, VM baha-runner-docker-2; nachweis gate-vm-1.md).
  (session-getrennt von der abnahme; mission traegt ROLLE: CODEX-WORKER). TICK-DUTIES punkt 7 angepasst.
- SPERRVERMERK: #1373 journal an Owner+ChatGPT (Direktive 15:5x). Keine Lane in machinehttp-journal-pfade;
  1373g-abnahme abbestellt; journal-wiring-abhaengige bleiben warten.
- JOURNAL GEMERGT (owner 16:1x, develop 77511c8a667, karte accepted). journal-wiring wartet nur noch auf
| 18 | coordinator/missions/w217-managed-users-r3-rebase.txt | ABHÄNGIG: kur-r8 muss zuerst in develop (r7 wurde in 1400a abgelehnt, r8 laeuft) | dann naechster freier sitz |
| 21 | coordinator/missions/w220-secure-export-r4-greenrun.txt | ABHÄNGIG: kur-r8 in develop (r7 abgelehnt, r8 laeuft) | dann naechster flash/laptop sitz |
