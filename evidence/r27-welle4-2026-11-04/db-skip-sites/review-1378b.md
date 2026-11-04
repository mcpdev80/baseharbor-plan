# ROLLE: CODEX-REVIEW — PR #1378 Runde B

**Verdikt: BLOCKED (keine Abnahme).**

## Kandidat und Identität

- PR #1378, `mcpdev80/baseharbor`, Branch `work/r27-db-skip-sites`.
- Erwarteter und lokal geprüfter Kopf: `760c104a6c499dc2baf6c30ad002bb6141bb7d83`.
- PR-Basis und zweiter Eltern-Commit des Basis-Merges: `develop` `ea3fb38e8f372ab2da38c10d964f3ea452fb8561`.
- `git ls-remote origin refs/heads/work/r27-db-skip-sites refs/heads/develop` ergab exakt diese beiden SHAs.
- PR ist offen, nicht Draft, mergeable. Die Workflow-Run-Abfrage lieferte `[]`; der kombinierte Commit-Status lieferte ebenfalls `statuses: []`.

## Diff und Basis-Merge

GitHub listet genau diese vier geänderten Dateien:

- `internal/controlplaneruntime/server_integration_test.go`
- `internal/database/connector_enrollment_integration_test.go`
- `internal/database/migration_rollback_integration_test.go`
- `internal/database/schema_readiness_integration_test.go`

Der Diff gegen `develop` enthält nur diese vier Pfade. Es gibt keine Workflow-, Produkt- oder `AGENTS.md`-Änderung. Der Kandidat ist ein Merge-Commit mit Eltern `aca8ff97df821305880ed569bafc8dbadfab7857` und `ea3fb38e8f372ab2da38c10d964f3ea452fb8561`. Der Merge fügt Änderungen aus develop hinzu; die vier PR-eigenen Testdateien sind gegenüber dem ersten Eltern-Commit blob-identisch (`git diff --quiet aca8ff97..760c104 -- <vier Pfade>`: Exit 0). Damit hat der Basis-Merge die PR-eigenen Dateien nicht verändert.

Die vier SHA-genauen PR-Patches ändern jeweils ausschließlich den fehlenden-URL-Zweig von `t.Skip("BASEHARBOR_TEST_DATABASE_URL is not set")` zu `t.Fatal("testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt")`.

## Eigene Messungen

**Ohne `BASEHARBOR_TEST_DATABASE_URL` — fail-closed bestätigt:** Auf dem geprüften Kandidaten liefen die vier betroffenen Tests gezielt, einmalig, jeweils ohne gesetzte Variable:

- `go test ./internal/database -run '^(TestConnectorEnrollmentPersistentAtomicScope|TestMigrationRollbackOwnsOnlyLatestChange|TestVerifySchemaReadyTracksAuthoritativeMigrationState)$' -count=1` — Exit 1; alle drei Tests meldeten wörtlich `testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt`.
- `go test ./internal/controlplaneruntime -run '^TestRunStartsTLSHealthReadinessAndProtectedAPI$' -count=1` — Exit 1; derselbe wörtliche Fehler.

Keiner dieser Tests wurde als Skip oder Erfolg gewertet.

**Mit `scripts/pr-unit-database.sh` — nicht verifizierbar:** Der geforderte eigene Lauf `env -u BASEHARBOR_TEST_DATABASE_URL bash scripts/pr-unit-database.sh` endete mit Exit 125, bevor Tests starteten: `Bind for 127.0.0.1:5433 failed: port is already allocated`. Der bereits vorhandene Container `sleepy_ganguly` (Image `postgres:18-alpine`) belegt Port 5433. Ich habe ihn nicht verändert. Es gibt daher keinen grünen Positivlauf.

## Abnahmeentscheidung

Die negative Zelle und der enge Write-Set sind bestätigt. Die Pflicht-Positivzelle ist wegen des belegten Testports nicht gelaufen; außerdem sind für den Kandidaten keine Workflow-Runs oder Commit-Statuschecks sichtbar, also kein terminal grüner Gate-Nachweis. **BLOCKED**, nicht ACCEPT: Für eine Abnahme muss die Datenbank-Skriptzelle in einer isolierten Umgebung mit freiem gebundenem Port erfolgreich laufen und müssen die vorgesehenen gehosteten Checks am exakten Kopf terminal vorliegen. Keine Produktkorrektur wird aus diesem Umgebungsblocker abgeleitet.
