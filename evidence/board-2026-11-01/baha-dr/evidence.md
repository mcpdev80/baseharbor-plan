# baha-dr Evidence — GH-Docker-TestTestAppBackupRestoreCLIRealDisasterRecovery FAIL ohne Text

## Mission
Befund: Auf GH-hosted Docker-Leg (Targeted-Lauf 41344498679, Job app-backup-restore) fällt
`TestAppBackupRestoreCLIRealDisasterRecovery` (163.9s) mit `--- FAIL` OHNE jegliche Fehler-/Panic-/Error-Trace.
Ziel: Ursachenklasse festmachen und echten Fix oder klaren Befund liefern.

## PLAN
1. [x] Test lokal im Worktree baha-dr reproduzieren (Docker rootless)
2. [x] cmd/baha/*backup*restore* Tests und Helpers lesen, TestMain/Cleanup/Parallel-Subtest analysieren
3. [x] 'FAIL ohne Text'-Phänomen erklären
4. [ ] Echte Mindestkorrektur NUR in cmd/baha/*-Test-/CLI-Dateien implementieren
5. [ ] Regression lokal laufen lassen, PR gegen develop erstellen
6. [x] Bei irreproduzierbar/timeoutlastig: END_BLOCKED mit Log-Zeilen + Flowchart

## END
END_BLOCKED — Ursachenklasse ist ein Runtime-Image-/Timing-Problem, kein Bug in cmd/baha/*-Test-/CLI-Dateien.

## Befund (reproduziert, lokaler rootless-Docker)
Der `--- FAIL` ist NICHT in einem Cleanup, NICHT parallel, NICHT in einem Helper einer anderen Datei.
Er landet in der Test-Routine selbst bei der ersten `t.Fatalf`, die über `runBackupFixtureWithConsent`
aus `app apply` nach 2 min Broker-Readiness-Timeout wirft. Der "ohne Text" stammt von der
abgebrochenen `-v`-Ausgabe: die `t.Fatalf`-Nachricht wird im Getriebe nicht in den getrackten Log-Ende
geschrieben, nur die FAIL-Zeile landet dort.

### Exakter Fehler
```
--- FAIL: TestAppBackupRestoreCLIRealDisasterRecovery (273.95s)
    app_backup_restore_integration_test.go:89: app apply: Starting secure runtime broker:
        application runtime broker readiness failed: application runtime broker container health is unhealthy;
        runtime diagnostics:
            bh-backup-recovery-ci-backup-cli-dev-broker-1  ghcr.io/mcpdev80/baseharbor-runtime:edge
            "/usr/local/bin/baha…"  broker  2 minutes ago  Up 2 minutes (unhealthy)  127.0.0.1:43013->8081/tcp
```

### Ursache
Der runtime-broker (verwaltete App-Runtime im `baseharbor-runtime`-Image) erreicht den internen
mTLS-Endpunkt `/readyz` (Port 8443) nicht innerhalb der 120s `runtimeReadinessTimeout`.
Die Container-Healthcheck-Config (compose_render.go:261) curlt
`https://baseharbor-runtime:8443/readyz` mit 5s Intervall, 12 retries, start_period 2s.
Nach 2 min → `unhealthy` → `app apply` schlägt fehl. `/version` antwortet, `/readyz` nicht.

### Warum edge-Bild der Auslöser ist
- Lauf 41344498679 nutzte den `app-backup-restore`-Gate mit der `edge`-Image-Tags (Build 2026-09-20).
- Reproduziert lokal identisch mit `ghcr.io/mcpdev80/baseharbor-runtime:edge` (273s) UND mit einem lokal
  aus develop gebautten Bild (`localhost/baseharbor-runtime:baha-repro`, ~194s).
- `/readyz` ist im Runtime-Bild implementiert (internal/runtimeexecutor/server.go:104), NICHT in
  cmd/baha. Eine Mindestkorrektur darf laut Mission nur in cmd/baha/*-Test-/CLI-Dateien liegen.

## Flowchart
```
TestAppBackupRestoreCLIRealDisasterRecovery
  └─ app apply (runBackupFixtureWithConsent)
       └─ ensureAndStartRuntimeBrokerWithCore
            ├─ waitForOpenBaoManagerReady (Core)   [OK]
            ├─ EnsureRuntimeMTLSIdentity            [OK mTLS identity verified]
            ├─ compose.UpProjectProgress broker     [container started]
            └─ verifyRuntimeBrokerRunning (120s)
                 ├─ container running              [OK]
                 └─ curl /readyz (8443, mTLS)        [FAIL nach 2 min → unhealthy]
                      └─ app apply FAIL → t.Fatalf
```

## Repo-rule compliance
- STOP-Bedingungen eingehalten: keine .github/*-Änderung, kein subagent/task-Spawn,
  kein codeman agent spawn/rm/send.
- Änderungen nur im baha-dr-Worktree; kein Push, kein PR (keine Mindestkorrektur im erlaubten Write-Set).
- Evidence nur im vorgesehenen evidence/.../baha-dr/-Pfad.
