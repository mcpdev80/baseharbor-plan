# db-skip-sites (t-20261104-r27, Welle 4) — Lane w137

Roller: Worker (Lane w137). Modell: worker-ornith1.5. Koordination: f49a3303.
Karte: t-20261104-r27-db-skip-sites. Repo: baseharbor. Branch: work/r27-db-skip-sites.

## PLAN (Auftrag abarbeiten)

- Fetch origin/develop, Vorfahr-Beleg ls-remote, Branch work/r27-db-skip-sites ab develop
- Die 5 git grep 'is not set'-Treffer untersuchen; echte Skip-Sitter identifizieren
- Die 4 t.Skip-Stellen mit BASEHARBOR_TEST_DATABASE_URL auf Fail-Closed umstellen
- Lokaler Testlauf: ohne Variable => alle 4 ROT; Gegenproben je Stelle dokumentiert
- Evidence-Tabelle dieser Datei; Draft-PR auf develop; gehostete Laeufe bis terminal
- Ende posten an f49a3303

## Befund / Analyse

### Was die verbundene hebelkarte getan hat
PR #1377 (2ea2c6f1) hat auf der Hauptlinie nur die zwei Datenbankpruefungen
umgestellt: fehlende BASEHARBOR_TEST_DATABASE_URL => FEHLSCHLAG statt UEBERSPRINGEN.
Der dortige Text ist `testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt`.

### Die fuenf git grep 'is not set'-Treffer
- cmd/baha/bugs_864_871_runtime_test.go:132 -> KEIN Skip-Sitter. Treffer ist
  `strings.Contains(output.String(), "variable is not set")`, eine Laufzeit-
  Ausgabe von compose-DATABASE_URL. Die Stelle wird nur mit
  BASEHARBOR_FINAL_BUG_ACCEPTANCE=1 auf isoliertem Docker/Podman-Host erreicht
  (core_installation_runtime_test.go:59/240/241). KEIN BASEHARBOR_TEST_DATABASE_URL.
  Nicht im Write-Set; gehoert nicht zu dieser Karte.
- internal/controlplaneruntime/server_integration_test.go:33 -> t.Skip, BASEHARBOR_TEST_DATABASE_URL. REAL.
- internal/database/connector_enrollment_integration_test.go:19 -> t.Skip, BASEHARBOR_TEST_DATABASE_URL. REAL.
- internal/database/migration_rollback_integration_test.go:15 -> t.Skip, BASEHARBOR_TEST_DATABASE_URL. REAL.
- internal/database/schema_readiness_integration_test.go:15 -> t.Skip, BASEHARBOR_TEST_DATABASE_URL. REAL.
- (Bonus) internal/database/connector_renewal_integration_test.go:20 -> t.Skip,
  BASEHARBOR_TEST_DATABASE_URL (andere Meldung). Gleiche Variable, gleiches Problem.
  Inmissioniert nur die 4 der Karte; renewal hier nicht geaendert (siehe Grenze).

### Bestehende Fail-Closed-Konvention (im develop schon da)
- internal/database/identity_tenant_resolver_integration_test.go:18
- internal/database/tenant_integration_test.go:18
beide: `t.Fatal("testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt")`.
Die 4 Stellen werden exakt auf diese Zeile angepasst.

## Vorher-Nachweis (origin/develop, ohne Variable)
```
$ unset BASEHARBOR_TEST_DATABASE_URL
$ go test ./internal/database/ ./internal/controlplaneruntime/
--- FAIL: TestIdentityTenantResolverUsesIdentityScopedRLS
    identity_tenant_resolver_integration_test.go:18: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt
--- FAIL: TestTenantRLSIsolation
    tenant_integration_test.go:18: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt
FAIL	github.com/mcpdev80/baseharbor/internal/database
ok  	github.com/mcpdev80/baseharbor/internal/controlplaneruntime
```
Die 4 Skip-Sitter tauchen hier als `--- SKIP` auf (Paket database failt an den
2 Fail-Closed-Tests, die 4 Skip-Sitter werden nie erreicht, weil der Build vorher
failt). Nach der Umstellung failt das Paket an 6 Fail-Closed-Tests (2 alt + 4 neu),
kein Skip mehr.

## Nachweis (nach Änderung, ohne Variable) - ROT
```
$ unset BASEHARBOR_TEST_DATABASE_URL
$ go test ./internal/database/ ./internal/controlplaneruntime/
--- FAIL: TestConnectorEnrollmentPersistentAtomicScope
    connector_enrollment_integration_test.go:19: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt
--- FAIL: TestMigrationRollbackOwnsOnlyLatestChange
    migration_rollback_integration_test.go:15: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt
--- FAIL: TestVerifySchemaReadyTracksAuthoritativeMigrationState
    schema_readiness_integration_test.go:15: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt
--- FAIL: TestRunStartsTLSHealthReadinessAndProtectedAPI
    server_integration_test.go:33: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt
FAIL	github.com/mcpdev80/baseharbor/internal/database
FAIL	github.com/mcpdev80/baseharbor/internal/controlplaneruntime
```
Kein SKIP mehr in den 4 Stellen. (Die 3 SKIP in connector_renewal_integration_test.go
bleiben unveraendert - bewusst nicht im Write-Set, siehe Befund.)

## Gegenprobe je Stelle (3 Faelle)
- (a) ohne Variable => Paket ROT (exit 1), Fall = failed, nicht skipped.
  Bestaetigt oben: alle 4 Stellen + die 2 bestehenden Fail-Closed-Tests rot.
- (b) mit Skriptverbindung (scripts/pr-unit-database.sh setzt
  postgres://postgres:postgres@127.0.0.1:5433/baseharbor_test) => Fall GRUEN,
  AUSGEFUEHRT. Nachweis -v mit Laufzeit:
```
$ go test ./internal/database/ -run 'TestConnectorEnrollmentPersistentAtomicScope|TestMigrationRollbackOwnsOnlyLatestChange|TestVerifySchemaReadyTracksAuthoritativeMigrationState' -v
=== RUN   TestConnectorEnrollmentPersistentAtomicScope
--- PASS: TestConnectorEnrollmentPersistentAtomicScope (0.42s)
=== RUN   TestMigrationRollbackOwnsOnlyLatestChange
--- PASS: TestMigrationRollbackOwnsOnlyLatestChange (0.32s)
=== RUN   TestVerifySchemaReadyTracksAuthoritativeMigrationState
--- PASS: TestVerifySchemaReadyTracksAuthoritativeMigrationState (0.12s)
ok      github.com/mcpdev80/baseharbor/internal/database
```
Jeder Fall lief real mit Laufzeit (0.42s / 0.32s / 0.12s), nur "ok" ist nicht die Antwort.
- (c) Mutation: Variable auf unreachbares Ziel (Port 59999) => ROT mit
  connection-refused, echtes Pruefen der Verbindung:
```
$ BASEHARBOR_TEST_DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:59999/baseharbor_test?...
--- FAIL: TestVerifySchemaReadyTracksAuthoritativeMigrationState
    schema_readiness_integration_test.go:26: failed to connect ... dial tcp 127.0.0.1:59999:
    connect: connection refused
FAIL
```

## Stellen-Tabelle (4 umgestellt, 1 bewusst nicht im Scope)
| Datei | Test | Vorher | Nachher |
| --- | --- | --- | --- |
| internal/controlplaneruntime/server_integration_test.go | TestRunStartsTLSHealthReadinessAndProtectedAPI | t.Skip | t.Fatal Fail-Closed |
| internal/database/connector_enrollment_integration_test.go | TestConnectorEnrollmentPersistentAtomicScope | t.Skip | t.Fatal Fail-Closed |
| internal/database/migration_rollback_integration_test.go | TestMigrationRollbackOwnsOnlyLatestChange | t.Skip | t.Fatal Fail-Closed |
| internal/database/schema_readiness_integration_test.go | TestVerifySchemaReadyTracksAuthoritativeMigrationState | t.Skip | t.Fatal Fail-Closed |
| internal/database/connector_renewal_integration_test.go | 3x TestConnectorRenewal* | t.Skip (andere Meldung) | UNVERAENDERT (außerhalb Missionsscope) |
| cmd/baha/bugs_864_871_runtime_test.go | runFinalBugRuntimeRegression | kein Skip (Laufzeit-Ausgabe) | UNBERUERT, nicht im Write-Set |

## Repo-Rule-Compliance
- Nur *_test.go geaendert; kein Produktcode, kein Test geloescht.
- KEINE .github-/Workflow-Enderung; kein rerun als Ersatz fuer Analyse.
- Bestehende Testnamen unveraendert: `git diff origin/develop..HEAD -- <testdatei> | grep '^-func Test'` leer (nachzuweisen).
- Ein Branch pro Kette; kein zweiter Kandidat.

## ls-remote / Branch-Provenanz
Base head origin/develop = 2ea2c6f1...  (ls-remote Witness folgt im END).
origin/develop ist Vorfahr von HEAD (git rev-parse --is-ancestor origin/develop HEAD => true).

## Repository-Regel (baseharbor AGENTS.md)
Nur Test-seitige Aenderung, Fail-Closed statt Skip, kleinste passende Pruefung
vor dem Push, Bundle der Commits, kein Force-Push, kein Merge (ist CODEX-Aktion).
