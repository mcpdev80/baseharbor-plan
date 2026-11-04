# Gate Watch Round 2 — Terminal CI state for 4 candidate heads

Worker lane w126 (TORE-BOBACHTUNG — read-only, kein Code, kein Rerun). Coordinator f49a3303.
Repo: `mcpdev80/baseharbor`. Alle Fakten aus `gh pr view` / `gh run view` / `gh api` (nur lesend).
Datum der Lektuehren: 2026-11-04, UTC. Keine markdown-Checkboxen in dieser Datei.

## 1. Terminal-state table (alle 4 laeufe TERMINAL / completed)

| PR | head10 | branch | run-id | status | conclusion | fail(ures) | pass | pending | skip |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #1363 | 4c1480678f | work/r27-profile-codec | 41861683041 | completed | failure | 1 | viele | 0 | viele |
| #1373 | 11ed442eed | work/r27-execution-journal | 41859360020 | completed | failure | 1 | viele | 0 | viele |
| #1347 | 95533a788d | work/r27-state-owner | 41864610432 | completed | failure | 3 | viele | 0 | viele |
| #1371 | 9ac4e2c4af | work/w96-production-wiring-f8ef4255 | 41847022451 | completed | failure | 1 | viele | 0 | viele |

Rote Stellen je PR (Check-Name):

- #1363: `PR · Validation · documentation-audit` (FAILURE) → zieht `PR Selected Checks` (FAILURE) nach.
- #1373: `PR · Validation · go-unit-tests` (FAILURE) → zieht `PR Selected Checks` (FAILURE) nach.
- #1347: `PR · Validation · cli-package-tests` (FAILURE), `PR · Validation · go-unit-tests` (FAILURE), `PR · Validation · wizard-app-edit-tests` (FAILURE). Andere Validation-Jobs gruen (`cli-build`, `cli-vet`, `cli-gofmt`, `cli-guided-tests`, `deployment-package-tests`, `go-build`, `go-vet`, `openbao-package-tests`, `runtime-provider-package-tests`, `wizard-app-new-tests`, `wizard-machine-adapter-tests`, `source-contracts`).
- #1371: `PR · Validation · go-unit-tests` (FAILURE) → zieht `PR Selected Checks` (FAILURE) nach.

## 2. Exakte fehlzeilen (aus dem Job-Log, gh api …/logs / gh run view --log-failed)

### #1363 — PR · Validation · documentation-audit (run 41861683041)
```
spec/credential-access-v1.md: fenced code/example contents differ (8 EN vs 8 DE)
DE technical integrity: FAIL (1 findings across 163 paired pages)
##[error]Process completed with exit code 1.
```

### #1373 — PR · Validation · go-unit-tests (run 41859360020)
```
--- FAIL: TestIdentityTenantResolverUsesIdentityScopedRLS (0.23s)
    identity_tenant_resolver_integration_test.go:101: failed to connect to `user=baseharbor_resolver_ci database=baseharbor_test`: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused
--- FAIL: TestTenantRLSIsolation (0.23s)
    tenant_integration_test.go:87: failed to connect to `user=baseharbor_runtime_ci database=baseharbor_test`: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused
FAIL	github.com/mcpdev80/baseharbor/internal/database	1.855s
##[error]Process completed with exit code 1.
```

### #1371 — PR · Validation · go-unit-tests (run 41847022451)
```
--- FAIL: TestIdentityTenantResolverUsesIdentityScopedRLS (0.18s)
    identity_tenant_resolver_integration_test.go:101: failed to connect to `user=baseharbor_resolver_ci database=baseharbor_test`: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused
--- FAIL: TestMigrationRollbackOwnsOnlyLatestChange (0.17s)
--- FAIL: TestTenantRLSIsolation (0.13s)
    tenant_integration_test.go:87: failed to connect to `user=baseharbor_runtime_ci database=baseharbor_test`: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused
FAIL	github.com/mcpdev80/baseharbor/internal/database	1.716s
##[error]Process completed with exit code 1.
```

### #1347 — drei rote Jobs (run 41864610432)
`go-unit-tests` (Job-Id 126695587191):
```
--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (47.47s)
FAIL	github.com/mcpdev80/baseharbor/cmd/baha	344.784s
--- FAIL: TestIdentityTenantResolverUsesIdentityScopedRLS (0.15s)
    identity_tenant_resolver_integration_test.go:101: failed to connect to `user=baseharbor_resolver_ci database=baseharbor_test`: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused
--- FAIL: TestTenantRLSIsolation (0.19s)
    tenant_integration_test.go:87: failed to connect to `user=baseharbor_runtime_ci database=baseharbor_test`: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused
FAIL	github.com/mcpdev80/baseharbor/internal/database	1.590s
##[error]Process completed with exit code 1.
```
`wizard-app-edit-tests` (Job-Id 126695587393):
```
--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (28.80s)
FAIL	github.com/mcpdev80/baseharbor/cmd/baha	38.537s
##[error]Process completed with exit code 1.
```
`cli-package-tests` (Job-Id 126695587228): FAILURE (conclusion=failure); die begleitenden Go-Tests laufen sauber durch, der Job schlägt an der abschließenden grep-Prüfung des Owner-Vertrags fehl (kein Postgres-Dial in dieser Ausgabe).

## 3. Klassifikation je rotem Check (mit Begründung in einem Satz)

### #1363 — `PR · Validation · documentation-audit`
Klasse (1) produktfehler im kandidaten. Die einzige rote Zeile ist eininhaltlicher Audit-Fund: `spec/credential-access-v1.md: fenced code/example contents differ (8 EN vs 8 DE)` → DE- und EN-Seite einer dokumentations-seitengleichen paarens stimmen im fenced-code/example-inhalt nicht überein. Kein CI-/infra-befund; der kandidaten-inhalt ist zu korrigieren.

### #1373 — `PR · Validation · go-unit-tests`
Klasse (2) CI-/testumgebung (postgres-familie, querverweis lane w122). Die fehlzeilen zeigen durchgehend `dial tcp 127.0.0.1:5432: connect: connection refused` für `internal/database`-integrationstests; das ist exakt das musteraus w122 (PostgreSQL-Instanz auf 127.0.0.1:5432 im CI nicht erreichbar / fixture nicht gestartet). Kein produktinhalt des execution-journal-pr ist betroffen.

### #1371 — `PR · Validation · go-unit-tests`
Klasse (2) CI-/testumgebung (postgres-familie, querverweis lane w122). Gleiches wortgetreues mustar: `connection refused` auf `127.0.0.1:5432` in `internal/database` (`TestIdentityTenantResolverUsesIdentityScopedRLS`, `TestTenantRLSIsolation`) sowie `TestMigrationRollbackOwnsOnlyLatestChange` (gleicher test-helfer, gleicher port). Lane w122 behandelte denselben pfad (work/w96-production-wiring-f8ef4255, basis develop ecbb8854) — dieser kopf teilt die ungepatchte test-orchestrierung.

### #1347 — drei rote jobs (run 41864610432, kopf 95533a788d)
- `go-unit-tests`: mischung. `internal/database` (`TestIdentityTenantResolverUsesIdentityScopedRLS`, `TestTenantRLSIsolation`, `connection refused` 127.0.0.1:5432) = klasse (2) CI/testumgebung, querverweis w122.
- `go-unit-tests` (`cmd/baha`): `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` (47.47s / 28.80s) = klasse (1) produktfehler im kandidaten (state-owner PR #1347; real-lifecycle-e2e schlägt fehl, nicht postgres-bedingt).
- `wizard-app-edit-tests`: derselbe `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` = klasse (1) produktfehler im kandidaten.
- `cli-package-tests`: FAILURE ohne postgres-dial in der ausgabe; an der abschließenden grep-prüfung des owner-vertrags gescheitert. Einordnung unsicher (1 vs. 2), als offen markiert — kein produktinhalt eindeutig zuordenbar, keine infra-ursache im log sichtbar.

## 4. Zusammenfassung für den Coordinator

- terminal = 4/4 (alle vier läuft sind `completed`, keine laufen mehr in progress).
- rot_mit_klasse:
  - #1363: documentation-audit → (1) produktinhalt (EN/DE code-inhalt mismatch in spec/credential-access-v1.md).
  - #1373: go-unit-tests → (2) CI/postgres (w122-familie, connection refused 127.0.0.1:5432).
  - #1371: go-unit-tests → (2) CI/postgres (w122-familie, connection refused 127.0.0.1:5432).
  - #1347: 3 rote jobs — go-unit-tests gemischt (2 = postgres/w122 + 1 = produkt, TestAppEditCommandCompleteProviderEditRunsRealLifecycle), wizard-app-edit-tests (1 = produkt, derselbe e2e-test), cli-package-tests = offen (kein postgres-dial, grep-prüfung).
- abnahmeempfehlung: keine abnahme vor terminalem, saubertor-bild. #1373 und #1371 blieben wegen postgres-orchestrierung (w122) rot — die gehört vor abnahme aufgeklärt (w122 / CI-feld). #1363 braucht den doc-inhalt-fix (#1363 selbst). #1347 hat einen echt-produkt-befund (TestAppEditCommandCompleteProviderEditRunsRealLifecycle), den der state-owner-kandidat selbst beheben muss, plus offene ci-package-tests-einordnung.

---
END w126-gate-watch DONE · terminal=4/4 · rot_mit_klasse: #1363 documentation-audit=(1 produktinhalt, EN/DE code-inhalt mismatch in spec/credential-access-v1.md); #1373 go-unit-tests=(2 CI/postgres w122, connection refused 127.0.0.1:5432); #1371 go-unit-tests=(2 CI/postgres w122, connection refused 127.0.0.1:5432); #1347 go-unit-tests=mischt (2 postgres/w122 + 1 produkt, TestAppEditCommandCompleteProviderEditRunsRealLifecycle), wizard-app-edit-tests=(1 produkt, e2e real-lifecycle), cli-package-tests=offen (kein postgres-dim im log). END an f49a3303 um 2026-11-04.

Lane w126 · read-only gate watch · keine schreibenden kommandos, kein rerun, keine .github-aenderung, keine subagenten.
Evidence-Zeugen: gh pr view 1363/1373/1347/1371 (--repo mcpdev80/baseharbor), gh api …/actions/runs/{id}, gh api …/actions/jobs/{id}/logs.
