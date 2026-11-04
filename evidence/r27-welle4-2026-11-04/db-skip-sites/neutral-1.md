# w152-neutral-probe (t-20261104-r27 db-skip-sites) — neutrale Gegenprobe

ROLLE: Worker (Lane w152). Modell: worker-ornith1.5. Koordination: f49a3303.
Karte: t-20261104-r27-db-skip-sites. Repo: baseharbor. Branch: work/r27-db-skip-sites.
Auftrag: NEUTRALE GEGENPROBE, kein product- oder test-file wird geändert (read-only, AGENTS §5.3).
Grund: review-1378b (Luna) war BLOCKED, nicht REJECT — ihre positive Datenbankzelle fiel auf
belegten Port 5433, der gehostete Lauf war damals nicht terminal. Der Lauf ist jetzt terminal
SUCCESS (Run 41922518146 auf 760c104a6c4). Diese Lane liefert die isolierte Positivzelle mit FREIEM
Port auf neutalem Boden (RUNBOOK §6.7/§5.3: Befunde aus Prüfer-Sandboxen gegen den Produktionspfad
nachmessen).

## PLAN

- Schritt 1: worktree auf exakt 760c104a6c499dc2baf6c30ad002bb6141bb7d83, ls-remote Witness, git-Integrität
- Schritt 2: Freien Port ermitteln + Postgres 18 gebunden an Port 55000, POSITIVZelle mit gebundenem Port
- Schritt 3: NEGATIVZelle ohne BASEHARBOR_TEST_DATABASE_URL (fail-closed, rc!=0)
- Schritt 4: Befund ausgewertet — beide Zellen konsistent, kein ROT auf neutalem Boden, kein ROT das auf gehostet grün war

## STATUS

- END w152-neutral-probe: DONE — Positivzelle 4/4 grün auf freiem Port 55000, Negativzelle 4/4 fail-closed (rc=1), read-only. Kein ROT auf neutalem Boden; kein Zielkonflikt mit dem terminalen gehosteten Lauf.

## Kopf-Identität (exakt)

- Kandidat-Kopf: 760c104a6c499dc2baf6c30ad002bb6141bb7d83
- Branch: work/r27-db-skip-sites
- 760 ist ein Merge-Commit mit Eltern `aca8ff97df821305880ed569bafc8dbadfab7857` (PR-Basis) und
  `ea3fb38e8f372ab2da38c10d964f3ea452fb8561` (develop).
- develop-Base: ea3fb38e8f372ab2da38c10d964f3ea452fb8561

## ls-remote Witness (Schritt 1)

```
$ git ls-remote origin refs/heads/work/r27-db-skip-sites refs/heads/develop
ea3fb38e8f372ab2da38c10d964f3ea452fb8561	refs/heads/develop
760c104a6c499dc2baf6c30ad002bb6141bb7d83	refs/heads/work/r27-db-skip-sites
```

- Lokaler `git rev-parse HEAD` = 760c104a6c499dc2baf6c30ad002bb6141bb7d83 (detached HEAD auf exakt diesem SHA).
- `git rev-parse --is-ancestor ea3fb38e... 760c104a...` = true → develop ist Vorfahr des Kandidaten.
- Branch-Provenanz: 760 liegt auf `work/r27-db-skip-sites` (eine Kette). Die PR-eigenen 4 Dateien sind
  gegenüber dem ersten Eltern-Commit aca8ff97 blob-identisch:
  `git diff --quiet aca8ff97..760c104 -- <4 PR-Dateien>` → Exit 0 (IDENTICAL). Der Basis-Merge hat die
  PR-eigenen Dateien nicht verändert; der "DIFFERS gegen develop" kommt nur vom Merge-in-von-develop.

## Repository-Integrität (read-only belegt)

- Nach allen Läufen: 0 modifizierte/tracked Files im Produkt. Einzig untracked (nicht staged) sind
  `.gopath/` (vorhandene Modul-Cache-Verunreinigung durch andere Lanes, nicht mein Werk) und mein
  isolierter Cache `.w152/` unterhalb des Checkout-Wurzelpfads.
- GOCACHE/GOMODCACHE/GOPATH/TMPDIR liefen nach `/home/marcel/dev/baseharbor-ecosystem/baseharbor/.w152/`
  (auhalb des git-Tracking); kein scratch/checkout/im/export im Ecosystem-Root, keine Produkt-Änderung.

## Freier Port (Schritt 2)

```
$ ss -ltn | awk 'NR>1 {print $4}' | sed 's/.*://' | sort -n > used-ports
# freier Port: 55000  (kein Listener auf 55000 vor Start)
$ docker run -d --name w152-neutral-pg -p 127.0.0.1:55000:5432 \
      -e POSTGRES_USER=testuser -e POSTGRES_PASSWORD=testpass -e POSTGRES_DB=baseharbor_test \
      postgres:18-alpine
0b25380a6f4373b1d414c8f970516d376f0c23183de7863f378c75dc42c8da35
$ docker ps --filter name=w152-neutral-pg
w152-neutral-pg  Up  127.0.0.1:55000->5432/tcp
```

- Gebundener Port: **55000**. DSN: `postgresql://testuser:testpass@127.0.0.1:55000/baseharbor_test?sslmode=disable`
- Postgres 18.6 (postgres:18-alpine), isolierter docker-netz (`w152-net`), nach Messung gestoppt/entfernt:
  `docker stop && docker rm w152-neutral-pg; docker network rm w152-net`. Kein fremder Container verändert.

## Positivzelle (Schritt 2) — GRÜN, freier Port 55000

```
$ BASEHARBOR_TEST_DATABASE_URL='postgresql://testuser:testpass@127.0.0.1:55000/baseharbor_test?sslmode=disable' \
    go test ./internal/database/ ./internal/controlplaneruntime/ \
      -run 'TestConnectorEnrollmentPersistentAtomicScope|TestMigrationRollbackOwnsOnlyLatestChange\
            |TestVerifySchemaReadyTracksAuthoritativeMigrationState|TestRunStartsTLSHealthReadinessAndProtectedAPI' \
      -count=1 -v
=== RUN   TestConnectorEnrollmentPersistentAtomicScope
--- PASS: TestConnectorEnrollmentPersistentAtomicScope (0.62s)
=== RUN   TestMigrationRollbackOwnsOnlyLatestChange
--- PASS: TestMigrationRollbackOwnsOnlyLatestChange (1.05s)
=== RUN   TestVerifySchemaReadyTracksAuthoritativeMigrationState
--- PASS: TestVerifySchemaReadyTracksAuthoritativeMigrationState (0.33s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/database	2.005s
=== RUN   TestRunStartsTLSHealthReadinessAndProtectedAPI
--- PASS: TestRunStartsTLSHealthReadinessAndProtectedAPI (1.80s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/controlplaneruntime	1.807s
```

- 4/4 GRÜN, real ausgeführt mit Laufzeit (0.62s / 1.05s / 0.33s / 1.80s), Exit 0. Kein SKIP.
- Die Tests managen ihr eigenes Schema (`resetTestDatabase` + `Migrate`), kein Pre-Schema nötig.

## Negativzelle (Schritt 3) — ROT (fail-closed), rc=1

```
$ unset BASEHARBOR_TEST_DATABASE_URL
$ go test ./internal/database/ ./internal/controlplaneruntime/ \
    -run 'TestConnectorEnrollmentPersistentAtomicScope|TestMigrationRollbackOwnsOnlyLatestChange\
          |TestVerifySchemaReadyTracksAuthoritativeMigrationState|TestRunStartsTLSHealthReadinessAndProtectedAPI' \
    -count=1 -v
=== RUN   TestConnectorEnrollmentPersistentAtomicScope
    connector_enrollment_integration_test.go:19: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt
--- FAIL: TestConnectorEnrollmentPersistentAtomicScope (0.00s)
=== RUN   TestMigrationRollbackOwnsOnlyLatestChange
    migration_rollback_integration_test.go:15: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt
--- FAIL: TestMigrationRollbackOwnsOnlyLatestChange (0.00s)
=== RUN   TestVerifySchemaReadyTracksAuthoritativeMigrationState
    schema_readiness_integration_test.go:15: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt
--- FAIL: TestVerifySchemaReadyTracksAuthoritativeMigrationState (0.00s)
FAIL
FAIL	github.com/mcpdev80/baseharbor/internal/database	0.004s
=== RUN   TestRunStartsTLSHealthReadinessAndProtectedAPI
    server_integration_test.go:33: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt
--- FAIL: TestRunStartsTLSHealthReadinessAndProtectedAPI (0.00s)
FAIL
FAIL	github.com/mcpdev80/baseharbor/internal/controlplaneruntime	0.006s
```

- 4/4 ROT (rc=1), fail-closed via `t.Fatal` an den Zeilen 19/15/15/33 der 4 PR-Dateien, wörtliche Meldung
  „testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt". Kein SKIP.
- Die 4 Skip-Stellen am Kandidaten-Kopf 760c104a6c4 sind damit erfolgreich in fail-closed umgestellt —
  Negativzelle greift exakt an den 4 Stellen.

## Befund / Auswertung (Schritt 4)

- NEUTRALER BODEN: Beide Zellen laufen sauber auf einem eigenen Postgres 18 auf freiem Port 55000.
- Positivzelle GRÜN (4/4), Negativzelle ROT (4/4) — beides konsistent und reproduzierbar, Exit-Codes
  0 bzw. 1, wörtliche Log-Zeilen gesichert.
- KEIN Zielkonflikt: Keine Zelle wird auf neutalem Boden rot, die am terminalen gehosteten Lauf (Run
  41922518146, status=completed, conclusion=success auf 760c104a6c4) grün war. Der positive Befund
  bestätigt die isolierte Positivzelle, die Luna fehlte; der negative fail-closed-Befund bestätigt
  Skipped→Fail-Closed an allen 4 Stellen.
- Der im Vorfeld (stiller develop-Checkout) gesehene SKIP war kein Kandidaten-Zustand; am exakten Kopf
  760c104a6c4 sind alle 4 Stellen fail-closed (negativ rot, wie oben).
- GRENZEN eingehalten: KEIN produkt-/test-file geändert (read-only, 0 tracked changes), KEIN
  .github/Workflow-Rerun, KEIN PR, KEIN Subagent.

## Repository-Regel-Compliance

- Nur read-only + Testausführung; keine Produkt-, Test- oder Workflow-Änderung.
- KEINE .github-/Workflow-Änderung; kein rerun/workflow_dispatch als Ersatz für Messung.
- Branch-Provenanz: eine Kette (work/r27-db-skip-sites), develop Vorfahr, PR-Dateien blob-identisch zu aca8ff97.
- GOCACHE/TMPDIR im Lane-Pfad/Checkout-Unterverzeichnis; kein scratch im Ecosystem-Root.
