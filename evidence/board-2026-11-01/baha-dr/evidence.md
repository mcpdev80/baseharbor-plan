# baha-dr Evidence — GH-Docker-TestAppBackupRestoreCLIRealDisasterRecovery FAIL ohne Text

## Mission
Befund: Auf GH-hosted Docker-Leg (Targeted-Lauf 41344498679, Job app-backup-restore) fällt
`TestAppBackupRestoreCLIRealDisasterRecovery` (163.9s) mit `--- FAIL` OHNE jegliche Fehler-/Panic-/Error-Trace.
Die letzten Test-Logs sind POSITIV (cleanup ok, foreign volume retained).
Ziel: Ursachenklasse festmachen und echten Fix oder klaren Befund liefern.

## PLAN
1. [ ] Test lokal im Worktree baha-dr reproduzieren (Docker rootless)
2. [ ] cmd/baha/*backup*restore* Tests und Helpers lesen, TestMain/Cleanup/Parallel-Subtest analysieren
3. [ ] 'FAIL ohne Text'-Phänomen erklären: Parallel-Subtest? t.Cleanup-Fehler? helper-Fehler in anderem File?
4. [ ] Echte Mindestkorrektur NUR in cmd/baha/*-Test-/CLI-Dateien implementieren
5. [ ] Regression lokal laufen lassen, PR gegen develop erstellen
6. [ ] PRSC bis terminal beobachten; bei irreproduzierbar: END_BLOCKED mit Log-Zeilen + Flowchart

## END
Bereit — Schritt 1 startet jetzt.
