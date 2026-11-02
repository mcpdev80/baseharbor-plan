# dr-doctor Evidence

## PLAN
1. [ ] 1) Log-Slice ziehen: gh api jobs/<id>/logs — app_backup_restore-Familie grep, subtest-Frage klären
2. [ ] 2) Kontextdifferenz validate vs Selected Runtime: Services-Postgres, XDG/rootless, -count, Timeout-Default 240s
3. [ ] 3) Minimaler Fix/Verhartung in cmd/baha (Test-Setup oder Toleranz) oder belegter Befund
4. [ ] 4) Beweis: go test ./cmd/baha -run 'AppBackupRestore' lokal zweimal (Vorher/Nachher)
5. [ ] 5) PR 'test(cmd/baha): make disaster-recovery probe deterministic on hosted validation', PRSC terminal

## END:
END_BLOCKED dr-doctor: awaiting results
