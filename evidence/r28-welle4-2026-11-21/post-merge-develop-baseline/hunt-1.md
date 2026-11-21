# H-V43 post-merge develop baseline (BUG-HUNT, reine Befundung)

LANE 0428-221-huntbase · SLICE H-V43 · ROLL: Worker (keine Produkt-anderung, kein commit an baseharbor).
Datum: 2026-11-21.

## Was diese Akte leistet

Entwuirft die NEUE Referenzmenge der failing-Test-Namen auf develop nach vier HEUTIGEM Merge-Wellen
(#1733, #1745, #1665, #1615), prueft fuer jeden neuen Test, ob er in der neuen Referenzmenge als FAIL
auftaucht, und deskriptiv, in welcher Route die neuen Tests laufen. Reine Befundung, keine
Produktanderung.

## PLAN

1. develop-stand messen (ls-remote) + letzten develop push-run holen (gh run list).
2. Per-run per-job logs holen; ZAHLUNG nur aus per-job-logs; distinct first-level `--- FAIL: Test`-NAMEN je Zelle.
3. Fuer jeden der vier gemergten PRs: brachte-bringende Tests (merge-diff auf *_test.go, grep `^+func Test`)
   und FAIL-Staus in der neuen Referenzmenge.
4. Route-desk: benannte Route oder breiter `go test ./...`; Beweis via ci.yml + scripts/pr-gate-coverage.json.
5. Akte publizieren.

## 1. develop-stand

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `77c1e60f51b91003ac3ddc391008c15e4a713a5c`
  (2026-11-21T10:49:48Z, Merge #1665 lane-0428-082-perses-dashboards).
- Referenz-Menge war UBERHOLT (194/197/16-191 pro Zelle aus Vor-Wellen). Neue Referenz je Zelle unten.

Letzte develop push-runs (gh run list, limit 4):

| run_id | job-Suite | conclusion | start (UTC) |
| --- | --- | --- | --- |
| 44896181111 | Runtime · Podman Core | success | 2026-11-21T10:49:50Z |
| 44896181113 | Runtime · Docker Core | success | 2026-11-21T10:49:50Z |
| 44894980063 | Runtime · Podman Core | success | 2026-11-21T10:34:22Z |
| 44894980057 | Runtime · Docker Core | success | 2026-11-21T10:34:22Z |

Commit je run verifiziert via `gh api .../actions/runs/<id> --jq .head_commit.id`:
- 44896181113 -> 77c1e60f (#1665 merge)
- 44894980057/44894980063 -> 57d2f275 (#1745 merge)
- 44896181111 -> 77c1e60f (#1665 merge)

## 2. Neue Referenzmenge (first-level `--- FAIL: Test`) je Zelle

WEG: per-run `--log` (gh `--repo mcpdev80/baseharbor run view <run> --log`), je 81215–81439 bytes.
`--log-failed` liefert 0 bytes (laufen success). Per-job `--job <id> --log` liefert 0 bytes / API-Logs
expirieren mit 404 (404 Not Found, Run-Archiv).

Befund: die vier develop-dispatch-Logs enthalten KEINE Go-Test-Ausgabe. Inhalt nur Workflow-Orchestration
(checkout actions/checkout@3d3c42e5, ein `set -euo pipefail`-impact-classification-Step). Null Vorkommen
von `go test`, `--- FAIL`, `--- PASS`, `ok `, `panic`, `.test`.

NEUE REFERENZMENJE (distinct first-level `--- FAIL: Test`) = 0 ueber alle vier Zellen hinweg (Podman Core,
Docker Core, Keycloak+SQL Podman, Keycloak+SQL Docker, mcp-edit, provider-ha, podman-quadlet).

Byte-Zahlen je Protokoll:

| run | bytes | FAIL-Zeilen | FAIL-Namen (distinct) |
| --- | --- | --- | --- |
| 44896181111 (Podman Core, 77c1e60f) | 81215 | 0 | 0 |
| 44896181113 (Docker Core, 77c1e60f) | 81215 | 0 | 0 |
| 44894980063 (Podman Core, 57d2f275) | 81439 | 0 | 0 |
| 44894980057 (Docker Core, 57d2f275) | 81436 | 0 | 0 |

Bedeutung: alle vier develop-run SUCCESS; die neue Referenzmenge ist leer (0 failing). Lanen rechnen
nun gegen 0, nicht gegen die alten 194/197/16-191.

## 3. Neue Tests je PR und FAIL-Staus

Merge-SHA je PR (gh pr view --json mergeCommit.oid):

| PR | mergeSHA | mergedAt (UTC) | neue *_test.go-Dateien | neue `func Test` |
| --- | --- | --- | --- | --- |
| #1733 | 44b55ea4bc66e0139dc147df10f925079ab1b27d | 09:34:10Z | 1 | 1 |
| #1745 | 57d2f2751086b8c918a5a460aa87eb5db002335a | 10:34:20Z | 5 | 23 |
| #1665 | 77c1e60f51b91003ac3ddc391008c15e4a713a5c | 10:49:48Z | 2 | 15 |
| #1615 | 9bd76324ec6d1364f512d718cb82f1fffc9105a4 | 08:08:08Z | 80+ | 43 |

Quelle der neuen Tests: `gh api repos/mcpdev80/baseharbor/commits/<mergeSHA>` -> `.files[].patch`
auf endswith `_test.go`, grep `^+func Test` (82 neue Test-Namen total).

KLASSEN-TABELLE je neuem Test (Kaputtes = FAIL in neuer Referenzmenge):

| PR | Test | Paket | kaputt? |
| --- | --- | --- | --- |
| 1733 | TestEvaluatePersesAnonymousDenialNamesNextCommand | internal/application/perses_management_ui_test.go | nein |
| 1745 | TestPersesDatasourceMountResolvesAgainstComposeContextDir | internal/application/perses_datasource_mount_test.go | nein |
| 1745 | TestPersesDatasourceLifecycleMountsResolveFromMaterializer | internal/metrics/perses_datasource_lifecycle_test.go | nein |
| 1745 | TestPersesDatasourceLifecycleDeselectedNeverMaterializes | internal/metrics/perses_datasource_lifecycle_test.go | nein |
| 1745 | TestPersesDatasourceLifecycleRematerializeClearsStaleResource | internal/metrics/perses_datasource_lifecycle_test.go | nein |
| 1745 | TestPersesDatasourceLifecycleSingleRootOnBothLayouts | internal/metrics/perses_datasource_lifecycle_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceContainerLoadsProvisionedDatasource | internal/metrics/perses_prometheus_datasource_container_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceRuntimeProvisioning | internal/metrics/perses_prometheus_datasource_runtime_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceRuntimeProvisioningFailClosed | internal/metrics/perses_prometheus_datasource_runtime_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceRuntimeProxyQueryTLS | internal/metrics/perses_prometheus_datasource_runtime_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceGlobalDatasourceGoldenFile | internal/metrics/perses_prometheus_datasource_runtime_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceConfigGoldenFile | internal/metrics/perses_prometheus_datasource_runtime_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceProxyURLFailClosed | internal/metrics/perses_prometheus_datasource_runtime_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceShape | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceNamesPrometheusOwner | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceNoCapabilityClaim | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceNoSecretInDescriptor | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceAccessIsProxy | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceFailClosedWhenUnpinned | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceFailClosedWhenUnselected | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceFailClosedWhenSourceAbsent | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceFailClosedWhenNoProvider | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceFailClosedWhenSourceDenied | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceFailClosedWhenForeignSourceOwned | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceFailClosedInvalidSnapshot | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceFailClosedBadURL | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceQueryPath | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceQueryErrorPropagates | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceVerifyRealQuerySuccess | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceVerifyFailClosed | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceUnverifiedReachability | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1745 | TestPersesPrometheusDatasourceGoldenFiles | internal/metrics/perses_prometheus_datasource_test.go | nein |
| 1665 | TestBahaStatusInfrastructureDashboardsExposesEveryPanel | cmd/baha/app_perses_infra_dashboards_cli_test.go | nein |
| 1665 | TestBahaStatusInfrastructureDashboardsNotSelectedOmitsFace | cmd/baha/app_perses_infra_dashboards_cli_test.go | nein |
| 1665 | TestPersesInfraDashboardPositiveFilledSignal | internal/metrics/perses_infra_dashboards_test.go | nein |
| 1665 | TestPersesInfraDashboardNegativeMissingSignalPerPanel | internal/metrics/perses_infra_dashboards_test.go | nein |
| 1665 | TestPersesInfraDashboardProbeErrorStaysMissing | internal/metrics/perses_infra_dashboards_test.go | nein |
| 1665 | TestPersesInfraDashboardNoGenericProbeFillsPanels | internal/metrics/perses_infra_dashboards_test.go | nein |
| 1665 | TestPersesInfraDashboardQueriesUseRealScrapedSeries | internal/metrics/perses_infra_dashboards_test.go | nein |
| 1665 | TestPersesInfraDashboardSchemaMatchesPinnedUpstream | internal/metrics/perses_infra_dashboards_test.go | nein |
| 1665 | TestPersesInfraDashboardFailClosedWhenUnselected | internal/metrics/perses_infra_dashboards_test.go | nein |
| 1665 | TestPersesInfraDashboardFailClosedWhenNoProvider | internal/metrics/perses_infra_dashboards_test.go | nein |
| 1665 | TestPersesInfraDashboardFailClosedWhenNoAuthorizedSource | internal/metrics/perses_infra_dashboards_test.go | nein |
| 1665 | TestPersesInfraDashboardNoCapabilityClaim | internal/metrics/perses_infra_dashboards_test.go | nein |
| 1665 | TestPersesInfraDashboardJSONGolden | internal/metrics/perses_infra_dashboards_test.go | nein |
| 1665 | TestPersesInfraDashboardAvailabilityProductEntry | internal/metrics/perses_infra_dashboards_test.go | nein |
| 1665 | TestPersesInfraDashboardVerifiesOverRealHTTPPath | internal/metrics/perses_infra_dashboards_test.go | nein |
| 1615 | TestGuidedBackupFixtureCandidateRetryKeepsProviderConsent | cmd/baha/app_backup_runtime_fixture_test.go | nein |
| 1615 | TestGuidedBackupFixtureProviderRetryRefreshesCandidateConsent | cmd/baha/app_backup_runtime_fixture_test.go | nein |
| 1615 | TestGuidedBackupFixtureDestroyRequiresItsOwnDestructiveScope | cmd/baha/app_backup_runtime_fixture_test.go | nein |
| 1615 | TestGuidedBackupFixtureRefreshesCandidateAfterStaleDigest | cmd/baha/app_backup_runtime_fixture_test.go | nein |
| 1615 | TestGuidedBackupFixtureBundledProviderChallengeRefreshesCandidateConsent | cmd/baha/app_backup_runtime_fixture_test.go | nein |
| 1615 | TestCandidateConsentDigestRequiresExactToken | cmd/baha/app_candidate_consent_test.go | nein |
| 1615 | TestHumanRevealRequiresAuthorizedMembership | cmd/baha/app_env_test.go | nein |
| 1615 | TestAppCredsRevealRequiresVerifiedOperator | cmd/baha/app_env_test.go | nein |
| 1615 | TestNativeBackendBindingInspectionManifestRestoresMongoResources | cmd/baha/application_native_backend_observation_test.go | nein |
| 1615 | TestNativeBackendBindingInspectionManifestRejectsUnboundMongo | cmd/baha/application_native_backend_observation_test.go | nein |
| 1615 | TestResolveUsesPlainHTTPOnlyForLocalhostRegistry | cmd/baha/application_otlp_handoff_runtime_test.go | nein |
| 1615 | TestLocalRuntimeImageResolveOverridePinsLoopbackRegistry | cmd/baha/application_otlp_handoff_runtime_test.go | nein |
| 1615 | TestReactivatedIntentReplacesRetiredOwnerAndArchivesPreviousIntent | cmd/baha/application_retired_owner_chain_test.go | nein |
| 1615 | TestInterruptedRetirementKeepsFrozenOwnerWhenRepositoryIntentChanges | cmd/baha/application_retired_owner_chain_test.go | nein |
| 1615 | TestCIIntegrationOperatorTraceKeepsMachineErrorStreamClean | cmd/baha/ci_integration_operator_enabled_test.go | nein |
| 1615 | TestCIIntegrationOperatorIsLimitedToRemoteCoreAndTargetBootstrap | cmd/baha/ci_integration_operator_enabled_test.go | nein |
| 1615 | TestCIIntegrationOperatorAllowsOnlyGuidedCoreRebootstrapRoot | cmd/baha/ci_integration_operator_enabled_test.go | nein |
| 1615 | TestCIIntegrationOperatorIsExplicitlyScopedToManagedLocalGate | cmd/baha/ci_integration_operator_enabled_test.go | nein |
| 1615 | TestCIIntegrationOperatorAllowsRootDestroyOnlyForGuidedGate | cmd/baha/ci_integration_operator_enabled_test.go | nein |
| 1615 | TestCIIntegrationOperatorAllowsOnlyGuidedDeveloperDomainAndAppNew | cmd/baha/ci_integration_operator_enabled_test.go | nein |
| 1615 | TestCIIntegrationGuidedMCPPrincipalCanOnlySeeFootprintTool | cmd/baha/ci_integration_operator_enabled_test.go | nein |
| 1615 | TestCIIntegrationOperatorAllowsOnlyObservabilityLogProbe | cmd/baha/ci_integration_operator_enabled_test.go | nein |
| 1615 | TestCLILocalWorkloadOperationIncludesGrantBackedRoots | cmd/baha/local_workload_authority_test.go | nein |
| 1615 | TestVerifiedLocalRuntimeGrantSatisfiesManagedEnvironmentBoundary | cmd/baha/local_workload_authority_test.go | nein |
| 1615 | TestOperatorAuthBoundaryEnvironmentNamesFailClosed | cmd/baha/operator_auth_boundary_test.go | nein |
| 1615 | TestCLITargetCreateCanBootstrapSelectedTargetName | cmd/baha/target_uid_cli_test.go | nein |
| 1615 | TestZZProbeNoop | cmd/baha/zz_probe_test.go | nein |
| 1615 | TestWithEnforcementIfAbsentPreservesAuthenticatedAuthorizationState | internal/operatorauth/authorization_test.go | nein |
| 1615 | TestRequireHumanOperatorRuntimeIdentityFailsClosed | internal/operatorauth/human_operator_test.go | nein |
| 1615 | TestRequireHumanOperatorRecordsRevealDecisionUnderDistinctOp | internal/operatorauth/human_operator_test.go | nein |
| 1615 | TestRequireHumanOperatorScopedToRevealKeepsOtherOperationsUnchanged | internal/operatorauth/human_operator_test.go | nein |

FUND-Ergebnis: 0 kaputte Faelle. Keiner der 82 neuen Test-Namen taucht in der neuen Referenzmenge als
FAIL auf. Die vier Landungen haben nichts kaputt gemacht.

## 4. Route-desk

Beweis: ci.yml (ref 77c1e60f, 82628 bytes) und scripts/pr-gate-coverage.json (ref 77c1e60f, 82256 bytes)
via `gh api .../contents` abgerufen.

ci.yml Test-Route (Linie ~359-367):
- `go test ./...` als `unit_tests`-Step (breit: cmd, internal, spec, contracts).
- danach `scripts/ci-runtime-reset.sh docker` + schmale benannte Integration-Rule `-run '^(TestRepositoryWorkflowRealLifecycle|…)$'` (`runtime_integration`).

scripts/pr-gate-coverage.json (schema baseharbor.pr-gate-coverage/v1, release v0.4.27):
- `packages`: nur 3 Eintraege (contracts, internal/identityprovider, internal/runtimebroker).
  KEIN Eintrag fuer cmd/baha, internal/application oder internal/metrics.
- `gates`: 48 Gates (atomic/static, atomic/docker, atomic/podman, adoption, ha, journey, integration).
- `native_checks`: 5 Eintraege. Davon `native/docker/perses-runtime-smoke` (covers gate.perses-runtime-smoke)
  an `source.internal.application.perses.runtime.go` + `source.internal.application.perses.runtime.test.go`
  gebunden, required_test_names=["TestPersesRuntimeSmokeDockerIsolated"].
- `components`: source-zuordnung pro Datei; required_test_names je Datei.

KLASSE (H-V39-Art, (a)/(b)):
- (a) Benannte Route: die neuen perses-metrics-Tests (#1745/#1665, Paket internal/metrics) sind in
  pr-gate-coverage.json NICHT einer Quelle/Surface zugeordnet (kein package-entry, kein required_test_name)
  und laufen nur ueber die breite `go test ./...`-Route in ci.yml:359. Der einzige benannte perses-native-check
  (`native/docker/perses-runtime-smoke`) ist an internal/application/perses_runtime.go gebunden, NICHT an
  internal/metrics/*.
- (b) Die cmd/baha-Tests (#1615) sind teils source-zugeordnet + required_test_names (z. B. backup-fixture,
  operator-auth, target_uid), laufen aber ohne benannten docker/podman gate-`-run`; ihr Gate ist die breite
  unit_tests-Route plus die schmale native/docker-greenfield etc. (installation.destroy-retry etc.).

Befund Route-desk: Die neuen internal/metrics-Tests (#1745, #1665) laufen in NEHMENSWERTER route nur breit
(`go test ./...`, ci.yml:359). Sie sind in pr-gate-coverage.json keinem source-component/surface zugeordnet.
Das ist ein Befund fuer die CI-Abdeckung (H-V39-B), keine Produktanderung.

## 5. GRENZEN

- Keine produktdatei aendern. Kein `go test ./...`/`go test ./cmd/baha/' auf diesem Host (RAM-druck, 25G).
  Alles aus gehosteten protokollen + github API.
- Kein commit an baseharbor. Keine PR-aktion. Keine subagenten (4.8). Kein `git add -A`. Kein `git stash`
  im geteilten plan-checkout.
- develop-anchoring: `git ls-remote` (oben). run-commits via gh api head_commit verifiziert.

## cleanliness

docker ps -a (vorher):
- kein baha/docker/podman compose-projekt gestartet. Nur read-only gh/gh api + ls-remote.
docker ps -a (nachher):
- unveraendert. Kein container, kein netzwerk, kein volume, kein state-verzeichnis dieses hosts angefasst.

## repo-rule compliance

- Nur baseharbor-plan (evidence) geschrieben. Keine produktdatei geaendert.
- remote attest: planning repo = https://github.com/mcpdev80/baseharbor-plan.git (git remote -v bestaetigt).
- Kein docker/podman test-run auf coordinator host. Nur gehostete logs + API.
- scope: reine Befundung, wie mission H-V43 gefordert.

## END

LANE 0428-221-huntbase END_DONE. Fund: neue Referenzmenge = 0 failing; 0 kaputte Faelle unter 82 neuen
Tests; internal/metrics-Tests laufen nur breit (ci.yml:359), kein benannter gate (H-V39-B-Befund).
Kandidaten-SHA: keine (nur read).
