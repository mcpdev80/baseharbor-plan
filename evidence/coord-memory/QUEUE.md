# Vorgemerkte Missionen (Warteschlange, durch Tick zu prüfen)

<!-- STAND 2026-11-05 19:1xZ: welle-4-einträge alle geliefert/gemergt; entries 0,00,1,2,3,4,9 geloescht (erledigt ausser plan-bereinigung). -->

Frei wird ein Platz, sobald eine Lane plattenfest abgeliefert und released ist. Eintrag löschen, sobald die
Lane dispatcht wurde. Der Audit-Punkt "POOL" zeigt beim Tick, ob ein Platz frei ist.

| # | Mission | Warum noch nicht dispatcht | Nächster Auslöser |
| --- | --- | --- | --- |
| 2 | ~~w121-podman-rebuild~~ | ERLEDIGT-DURCH-ANDEREN | Podman-Host läuft jetzt in codex-ops-podman (zweite Codex-Instanz, Owner-Direktive 17:5x). w121 bleibt als Fallback-Mission, wird NICHT doppelt dispatcht (ein Host, ein Bearbeiter). |
| 4 | ~~w119-journal-r2~~ | ERLEDIGT | wurde von cx01 (Codex-Worker) geliefert: head 11ed442e, Karte auf review, Luna prueft | Pool 4/4 | Ausführungstagebuch-Runde 2 (Codex review-1373a REJECT, fünf Rezepte) |

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
- w168-authority-boundary.txt — LAEUFT: ziel-stufige live-verbindung in der bestehenden grenze; naehert
  #1380 wieder an (warnung "connection-client active mit offener abhaengigkeit" ist gewollt und ehrlich).
- w159-compose-iso.txt — GRUND-ERHALTEN: basis-drift + isolierungszelle unentschieden, lane klaert beide
  punkte vor der prüfung (zustimmung fix = nachgewiesen, isolierung = evtl. nicht reproduzierbar).
- w169-compose-r2.txt — Warteschlange p1 (isolierung offen), w170-credentials-r2.txt — p2 (doppel-write).
- w171-streams-r3.txt — Warteschlange p1 (zwei mutantenluecken C/D). w169-compose-r2 p2, w170-credentials-r2 p3.
- w171-streams-r3.txt — LAEUFT (ornith). w170-credentials-r2 — p1 Warteschlange. w169-compose-r2 laeuft.
- w170-credentials-r2.txt — LAEUFT (ornith). w171 streams-r3 laeuft (laptop). Compose w169, Profile w167 laufen.
- w172-boundary-r2.txt — p1 Warteschlange; w173-journal-r6.txt — p2. (beide missions-dateien fertig).
- t-20261105-r27-snapshot-change-guard-deterministic — NEU (p1 nach laufenden ends): same-head flake
  belegt (41981861515 gruen vs 41983173186 rot, 0.01s), determinischer hook noetig; entpoisoned die gates.
- w172-boundary-r2.txt — LAEUFT (laptop). w173-journal-r6 — p1 Warteschlange.
- SPERRVERMERK: #1347 state-owner komplett an Owner+ChatGPT (Direktive 08:0x). Keine Lane dieser Seite in
  internal/application state-owner-Pfade; Abhaengige (u.a. podman-recovery-bootstrap-cleanup,
  mutation-lock-Kette) erst nach deren bestaetigtem Abschluss.
- w174-profiles-r3.txt — p1 Warteschlange (produktion-plus-zukunftsrevision); w173-journal-r6 p2.
- w175-credentials-r3.txt — p1 Warteschlange (CAS-Seed + heilender Race-Test); w174 läuft, w173 p2.
- w175-credentials-r3.txt — LAEUFT. w173-journal-r6 — p1 Warteschlange. Boundary r2 im pruefkanal (1386b).
- w173-journal-r6.txt — LAEUFT (laptop, von w171). Streams im pruefkanal (22c). p-Warteschlange: snapshot-flake.
- w176-streams-r4.txt — p1 (A/B echter Pfad, D-Abbruch, execx-CLAERUNG, echter Smoke). snapshot-flake p2.
- ENTRIEGELT 2026-11-05: #1347 gemerged (develop 42bfcb1cb4). Fuenf abhaengige Welle-4-Karten geplant frei:
  app-binding, management-host, mutation-lock, stage-versions, state-recovery — Besetzung nach Kapazitaet,
  basis ist jetzt 42bfcb1cb4 fuer ALLE neuen schnitte (missionstexte beim naechsten dispatch anpassen).
- w176-streams-r4.txt — LAEUFT (laptop). Journal r6 im pruefkanal (1373f). p: snapshot-flake, neue 5er-Welle.
- w177-journal-r7.txt — p1 (einzellauf-mutante + basis-42bfcb1cb4). snapshot-flake + 5er-welle dahinter.
- w177-journal-r7.txt — LAEUFT (ornith). Profiles r3 im pruefkanal (1384c).
- Compose r2 + Credentials r3 im pruefkanal (1383b verteilt, 1385c folgt). w178 snapshot-flake LAEUFT.
- Welle-5 eroeffnet: app-binding LAEUFT (laptop), mutation-lock = p1 naechste (dependencies all closed),
  stage-versions/state-recovery/management-host weiter gesperrt (planned vorginger: device-lifecycle,
  journal-wiring, candidate-ingress, app-binding).
- w180-compose-r3.txt — p1 Warteschlange (bootstrap-scope + kontaminiertes ensemble). mutation-lock p2.
- w181-credentials-r4.txt — p1 (produktiver CAS-pfad + option-mutante). mutation-lock p2.
- w182-snapshot-flake-r2.txt — p1 (fail-fast statt timeout-deadlock). w181-credentials-r4 p2, mutation-lock p3.
- w182 LAEUFT (laptop). app-binding r1 im pruefkanal (1388a). naechste: w181-credentials-r4, mutation-lock.
- w183-compose-gate.txt — p1 (VM-raeumen + vier-zellen + mutante; inhalt des PRs unveraendert). flake-r2/
  journal r7/streams r4 laufen. credentials-r4 p2.
- COMPOSE-GATE: OWNER-BLOCKER (daemon.json default-address-pools, VM baha-runner-docker-2; nachweis gate-vm-1.md).
  w181 credentials-r4 LAEUFT. mutation-lock p1 Warteschlange.
- AGENTS-ÄNDERUNG 2026-11-05: pool=5 (2+2+1 CODEX-WORKER). w184-mutation-lock als erster codex-worker LAEUFT
  (session-getrennt von der abnahme; mission traegt ROLLE: CODEX-WORKER). TICK-DUTIES punkt 7 angepasst.
- SPERRVERMERK: #1373 journal an Owner+ChatGPT (Direktive 15:5x). Keine Lane in machinehttp-journal-pfade;
  1373g-abnahme abbestellt; journal-wiring-abhaengige bleiben warten.
- JOURNAL GEMERGT (owner 16:1x, develop 77511c8a667, karte accepted). journal-wiring wartet nur noch auf
  mutation-lock (w184 laeuft). streams r5 besetzt (w185). credentials-nachlieferung laeuft (w181).
| 18 | coordinator/missions/w217-managed-users-r3-rebase.txt | ABHÄNGIG: kur-r7 muss zuerst in develop | dann naechster freier sitz |
| 21 | coordinator/missions/w220-secure-export-r4-greenrun.txt | ABHÄNGIG: kur-r7 in develop | dann naechster flash/laptop sitz |
