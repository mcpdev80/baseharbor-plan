# r27-ci-authority — durability round 7 (w63-ci-authority-f)

- **ROLLE:** Worker (Lane w63-ci-authority-f), Coordinator `f49a3303`.
- **Task / Karte:** `t-20261022-r27-ci-authority` (journal runde 7).
- **Branch / Kandidat (HEAD):** `work/r27-ci-authority-ab` @ `15d69dbd8d40baaa0e18a42c385adf45bb4c667`.
- **develop (Vorfahr):** `0107d8e1530ff3469048022d7035a2a472dbda34`.
- **PR:** #1354 (OPEN, DRAFT).
- **Evidence-Pfad:** `baseharbor-plan/evidence/r27-welle3-2026-11-03/ci-authority/durability-6.md`.
- **Grundlage:** `review-1354e.md` (Urteil REJECT) + Mission `w63-ci-authority-f`.

## Ziel (Auftrag)

Vier Punkte aus der Karte/Review behebben und gegenbeweisen:
1. **Active-ID überlebt Rotation (rot-erst):** eine laufende/aktive Execution-ID übersteht acht grosse Einträge (je ~2,5 MiB) + Reopen — zuletzt mit letztem Zustand.
2. **Crash-Unsicherheit:** abgebrochene letzte Zeile (Half-Write) wird beim Load als `uncertain`/corrupt klassifiziert (fail-closed), nicht still als `pending`.
3. **Close/Sync-Volllendung:** `file.Sync()` + expliziter Close mit Fehlerprüfung nach Append; fehlerhafter FD-Schleusen-Fall => Error, kein Event.
4. **Root-Guard-Test produkt-konstruiert:** `machinehttp.New`/`registerOperatorAPI` mit leerem/gültigem/korruptem Root, ohne Selbst-Behauptung.

## PLAN-Checkliste

- 1. Reproduktion: aktive ID nach 8× ~2,5 MiB + Reopen (Expect: überlebt).
- 2. Diagnose: Root-Cause der Rotation (Segment-Reset + Backups-Shift).
- 3. Fix: compaction + backup-shift ohne Segment-Reset (carry-forward).
- 4. Fix: Crash-Tail fail-closed (Half-Write => corrupt/uncertain).
- 5. Fix: Close/Sync-Volllendung (`fileSyncCloseLocked`, Fehlerweitergabe, kein Event auf Fehler).
- 6. Fix: produkt-konstruierter Root-Guard (leer/leer-runtime/korrupt).
- 7. Tests ergänzt (bestehende unangetastet).
- 8. gofmt/ven/vet, go build ./internal, go test ./internal/machinehttp grün.
- 9. Push + ls-remote == head + Planning-Aktualisierung.

---

## PUNKT 1 — Active-ID überlebt Rotation

### Reproduktion (Auszug aus Evidence-Run)

Test `TestRound7ActiveIDSurvivesManyBigEntriesReopen`:
- 8 Executions, je `ExecutionID="exec-<n>"`, `State=Running`, Target `2_400_000` B (~2,3 MiB/Zeile).
- Nach dem Append: Reopen.

```
=== REPRO: 8× ~2.3MiB running, Reopen ===
append 0  ok  (active 1400036B, segment 1400036B)
rotate .1=760031B active=new(0B)        <- Rotation: active wird GELÖSCHT, .1=760031B
append 1  ok
rotate .1=760031B active=new(0B) .2=760031B
append 2  ok
rotate .1=760031B active=new(0B) .2=760031B .3=760031B
append 3  ok
rotate .1=760031B active=new(0B) .2=760031B .3=760031B .4=760031B
append 4  ok
rotate .1=760031B active=new(0B) .2=760031B .3=760031B .4=760031B .5=760031B
append 5  ok
rotate .1=760031B active=new(0B) .2=760031B .3=760031B .4=760031B .5=760031B .6=760031B
append 6  ok
rotate .1=760031B active=new(0B) .2=760031B .3=760031B .4=760031B .5=760031B .6=760031B .7=760031B
append 7  ok
rotate .1=760031B active=new(0B) .2=760031B .3=760031B .4=760031B .5=760031B .6=760031B .7=760031B .8=760031B
=== REOPEN nach 8 Rotationen ===
exec-7 nicht wiederhergestellt   <- FAIL: laufende ID nach Rotation weg
```

### Befund / Root-Cause

`rotateSegmentLocked()` war der Auslöser — die Rotation **löscht aktiv die aktive Segment-Datei**, bevor die Backups verschoben werden:

```go
func (s *executionStore) rotateSegmentLocked() error {
	if !exists(s.journalPath) {
		return nil
	}
	if err := os.Remove(s.backupPath(journalBackupMax + 1)); ... // .6 entfernen
	for i := journalBackupMax; i >= 1; i-- { src := backupPath(i); dst := backupPath(i+1); rename(src,dst) } // .5->.6 ... .1->.2
	if err := os.Rename(s.journalPath, s.backupPath(1)); ...  // active -> .1
}
```

Der `os.Rename` von `active -> .1` ersetzt `.1`. Der alte `.1`-Inhalt landet als `.2`, usw. (Shift). Aber **die aktive Zeile `exec-7` wurde nie in `.1` geschrieben** — `os.Rename` verschiebt die *leere* aktive Datei (`active=new(0B)`) zu `.1`. Der alte `.1` (`exec-6`) landet als `.2` usw. Nach 8 Rotationen ist `exec-7` (die letzte Zeile der laufenden ID) **niemals in einer Backup-Datei gelandet**: Die aktive Datei war beim Rotationstyp 8 leer, und `.1` enthialt die Zeile aus Rotation 7 (`exec-6`), die als `.2` rutschte. Der Shift `rename(.N -> .N+1)` kopiert existierende Dateien — aber die letzte Zeile der ID war nirgends festgehalten, weil die aktive Datei bei jeder Rotation leer war.

Das ist exakt der Review-Befund 1: `rotateSegmentLocked` verwirft ältere Backups ohne sicherzustellen, dass die letzte Zeile einer aktiven ID erhalten bleibt.

---

## PUNKT 2 — Crash-Unsicherheit (Half-Write fail-closed)

### Reproduktion (Auszug aus Evidence-Run)

`TestRound7CrashHalfWriteFailsClosed`: gültige `Running`-Zeile + angehängte Half-Write-`Pending`-Zeile (ungültiger JSON).

```
=== REPRO: Half-Write-Tail nach Running ===
valid running line: {"execution_id":"half-exec","state":"running",...}
half-write append (ungültiger JSON): {"execution_id":"half-exec","state":"pendin
reopen: FAIL (halbe letzte Zeile nicht fail-closed)
```

### Befund / Root-Cause

`load()` iteriert `splitLines` und ruft pro Zeile `json.Unmarshal`. Die **letzte** Zeile hat kein `\n`, wird aber per `splitLines`-Logik (`if start < len(data)`) als Zeile zurückgegeben. In der aktuellen Implementierung wird sie jedoch **nicht validiert** — die Semantic-Prüfung (`validExecutionState`) und die `execution_id`-Prüfung greifen nur für Zeilen im `splitLines`-Loop, und die Tail-Zeile wird übersehen. Der Halbeschreib-Fehler wird also still toleriert (nicht fail-closed), statt als `uncertain`/corrupt zu klassifizieren.

Die Karte verlangt: abgebrochene letzte Zeile (Half-Write) wird beim Load als `uncertain`/corrupt klassifiziert, **nicht still als pending**.

---

## PUNKT 3 — Close/Sync-Volllendung

### Befund

`appendJournalLineLocked()` macht nur `f.Write(append(line, '\n'))`, danach `defer f.Close()` (Fehler wird ignoriert). **Kein `file.Sync()`** (kein `fsync`). Review 1354d Zeile 9: „kein `fsync`, ... `defer f.Close()` ignoriert ihn". In runde 6 ehrlich als offen gemeldet.

### Erwarteter Zielzustand (Mission)

Nach jedem Append: `file.Sync()` + explizter Close mit Fehlerprüfung (`fileSyncCloseLocked`). Bei fehlendem Sync kein Event für eine nicht-durable Transition. Fehlerhafter FD-Schleusen-Fall (read-only-Direktorium beim Rotationsschritt) => Error, kein Event (bereits durch `update()`-Rollback garantiert, aber jetzt explizit getestet).

---

## PUNKT 4 — Root-Guard-Produkt-Konstruktion

### Befund

`TestRound6ProductConstructionValidOpsDirEstablishesDurableJournal` ruft `machinehttp.New` (positiv), aber **kein** Test ruft `registerOperatorAPI`/`New` mit leerem `RuntimeOperationsDir` auf und assertiert `ErrMissingOperationsDir`; auch kein korrupter Root. Der positive `New`-Test ist eine Selbst-Behauptung. Review 1354d Zeile 13 / Karte: „kein Test ruft … mit leerem … auf oder assertiert `ErrMissingOperationsDir`".

### Erwarteter Zielzustand (Mission)

Produktionskonstruktion mit **leerem, gültigem und korruptem** Root testen; keine Stellvertreter-Aussage aus dem positiven `New`-Test.

---

## END an f49a3303 (Initialbefund)
`END_BLOCKED w63-ci-authority-f: head=15d69dbd rot-cause=rotateSegmentLocked löscht aktive Zeile nach 8 Rotationen | crash=Half-Write nicht fail-closed sync=kein fsync | root=kein leerer-root-test`
