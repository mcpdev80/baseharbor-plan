# Coordinator-Session-Handoff 2026-11-02 (Option B — neue Session)

## PFO 0 — Automatisierungs-Umschreiben auf NEUE Session-ID (ZUERST, vor allem anderen)
Die komplette Watcher-/Tick-Maschine zeigt noch auf die alte Session `35cdb02e-…`. Pflichtroutine
nach dem Start (neue ID hier überall einsetzen):

1. **Watcher-Registratur:** `coordinator/scripts/watcher-state.json` → Feld
   `.watcher.coordinator` auf NEUE ID setzen; anschließend Watcher neu starten:
   `bash coordinator/scripts/watch-keepalive.sh` (läuft via crontab jede Minute, stellt den
   `watch.py`-Prozess wieder her — aktuell PID läuft noch mit alter Registratur; sicherheitshalber
   erst `python3 coordinator/scripts/watch.py stop`, dann keepalive greift).
2. **basics-check.py:** Zeile 49 `COORD_IDS = {…}` um NEUE ID erweitern (alte Einträge dürfen bleiben,
   sie verursachen nur Alt-Toleranz).
3. **Crontab prüfen (unverändert nutzbar, da Skript-Pfade absolut):**
   `*/10 … coord-tick-once.sh` + `* … watch-keepalive.sh` — der Tick weckt über
   `coord-env.sh → BH_COORD_SESSION` (liest .watcher.coordinator aus Schritt 1), keine Extra-Arbeit.
4. **Lane-Missionstexte:** alle aktiven Missionen unter `coordinator/missions/` enthalten
   `post 35cdb02e-…` als HANDOFF-Adresse. Für jede LAUFENDE Lane (obslok2, rcptfix2, boardup):
   `codeman agent send <lane> "END-Handoff ab sofort an <NEUE-ID> posten."` und Missionsdatei
   sed-mäßig auf neue ID ziehen (für Nachfolge-Lanes stimmt der Text dann automatisch).
5. **Gegentest der Umschreibung:** eine Test-Lane idle-Wachen erzwingen (watch.py check) und prüfen,
   dass der Wake an der NEUEN Session ankommt; `codeman agent inbox` zeigt die alten Postfächer leer.

## Sofort nach Start der neuen Session (Post-Start-Pflichten)
0. PFO 0 oben erledigen.
1. `python3 coordinator/scripts/basics-check.py` + `python3 coordinator/scripts/events-check.py --reminders --ack` (Turn-Start-Pflicht).
2. Remote Reality-Check (Board + gh, Abschnitte Betriebsstand/Dateien unten als Soll-Zustand).

## Betriebsstand (verifiziert, 2026-11-02 ~11:30)
- develop-Tipp: `7c6de98b`+#1272-Merge (`9a93865a`-Kette, PRSHA siehe `git log origin/develop`).
  Heute gemergelt: #1267 #1268 #1269 #1270 #1271 #1272 #1274 #1275 #1276 #1282 (jeweils PRSC-green,
  Details + Merge-SHAs in release-0427-chain.md, gleiches Verzeichnis).
- Offene PRs: #1283 (Loki render.go Fix; CI·S&Q Run in Queue), #1273 (Broker/OpenBao-Registrierung;
  native qualification Runs auf `765033d4` in Queue: runtime-broker.yml x2, runtime-s3, docker/podman-Refs),
  #1258 (GH-Hosted-Sweep, head `735acd95`), #1257 (Paritaet, head-Refs ready nach #1258),
  Parkdeck #1243 #1244 #1247 #1248 #1249 #1238 #1239: Inhalte in #1258 enthalten
  (Tabelle + Close-Routine: ../board-2026-11-02/supersede/evidence.md).
- Receipt · Post-Run Writer rot: ROOT CAUSE dokumentiert — scripts/receipt_verifier.py:408-415
  verlangt Job 'PR · Public Contracts' HARDCODED success; bei PRs ohne contracts-Pfade ist der Job
  SKIPPED -> Block fuer jede Receipt. rcptfix2-Lane arbeitet Fix (fail-closed-Eigenschaft behalten:
  required nur wenn im Trusted-Plan required).
- Autorisierungs-Ledger-Muster (PR #1272, Erst-Eltern-Kette) laeuft; Paritaet #1257 nach #1258.
- Host-Queue: gelegentlich 5-10 Runs backlog (kein Fake-Rerun; warten).
- Pool: Ziel 2 Ornith + 2 Qwen (flash LIMITS=0, parked); aktuell 3 Lanes busy, 1 qwen-Slot frei.
- GUI-Note: P0-Direktive-Block steht nur in Session-Transkripten (DB), nicht in Logs; Content der
  Direktive ist laengst Arbeitsprogramm (siehe chain-Log Abschnitte 'Direktive').

## Naechste Schritte (Reihenfolge)
1. #1283 + #1273 native Runs ernten -> Merges.
2. #1258 auf geheilten develop rebase + Re-Qualifikation (Refs + Dispatches auf neuen head), Merge.
3. Parkdeck-Closes mit Null-Diff-Nachweis (#1243 zuerst, Inhalt == #1258).
4. rcptfix2-Ergebnis -> Receipt-Runs gruen pruefen.
5. #1257 Probe auf neuem develop (Targeted/runtime-validation Refs), Merge.
6. Targeted-HA-Run (GitHub-hosted) als letzter Nachweis; dann release-prepare Karte — Owner-Freigabe
   fuer Release/Tag bleibt PFLICHT (kein Auto-Release).

## Dateien
- Running log: release-0427-chain.md (hier, lueckenlos)
- Acceptance-Board: coordinator/board/acceptance.json
- Missionen + Archive: coordinator/missions/ , coordinator/missions/archive/
- Parkdeck-Tabelle: ../board-2026-11-02/supersede/evidence.md
