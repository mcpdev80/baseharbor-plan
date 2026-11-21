# Hunt 1 — CI-Aufnahmepflicht-desk (fenster seit 2026-11-19)

ROLLE: Worker (BUG-HUNT, reine Befundung, KEINE Produkt-aenderung, KEIN commit an baseharbor).
LANE: 0428-221-huntci. SLICE: H-V37.
Datum: 2026-11-21.

## Basis-Kontrolle (remote attestation)
- Planning-Repo remote (BEVOR erster evidence-commit):
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` ->
  origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push)
- baseharbor develop head (ls-remote): 4fa5293a49b7a6cd74c6513cf329dec15d08cfa9
- baseharbor main head (ls-remote): c000c5db2560c471fe84842136e03d6e54d96779
- ARBEITSREINE: Nur Lesezugriff auf Klon unter /tmp/opencode/221-wt/repo; kein Commit, kein Push an baseharbor.
- Remote-Guard: der Checkout /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor zeigt `origin git@github.com` (kein github.com-URL) und ist Quarantäne; NICIT zitiert. Realer GitHub-Remote = https://github.com/mcpdev80/baseharbor.git.

## 1. Menge neuer/geraendertter Test-Funktionen seit 2026-11-19 (develop)
Methode: `git log --no-merges --format=%h origin/develop --since=2026-11-19T00:00:00 -- '*.go'` -> 157 Commits.
Je Commit `git show --unified=0 <c>` gefiltert nach `^+func Test` -> 338 eindeutige neue Test-Funktionen.
Gegenprobe: `git grep -l "func TestXxx(" origin/develop` mapt 327 auf ihre Datei; 11 Namen existierten
nur transient innerhalb des Fensters (in 9d905cbd eingeführt, in 4d3494ea/Spätere Commits durch
Refactor ersetzt) und stehen am develop-HEAD nicht mehr -> gehören NICHT zum Endbestand, sondern an
die Change-Historie (0428-168 re-book legacy keycloak source). Kein fachliches Vakuum: die
entsprechenden Fälle leben in `internal/identityprovider/keycloak_legacy_migration_integration_test.go`
(8 Tests) und `internal/observability/migration.go`.

SAMMENUNG: 338 neue Test-Funktionen im develop-Endbestand seit 2026-11-19.
Vollständige test-name/datei/shard-Tabelle: fulltable.txt (dieser Akte beigefügt).

## 2. Welche Zelle waehlt jeden Namen? (nur lesen)
Entscheidende Laufwege (alle NUR gelesen, kein Edit):
- .github/workflows/ci.yml -> pr_unit_shards (line 1196) mit unit_scope != none ->
  bash scripts/pr-unit-database.sh <shard>.
- scripts/pr-unit-database.sh:
    * mode=packages -> python3 scripts/pr-go-unit-shard.py --mode packages ->
      `go test ./...` fuer ALLE nicht-CLI-Pakete, OHNE -run (jeder Test im Paket laeuft).
    * mode=cli-0..3 -> pr-go-unit-shard.py -> discover_cli_tests() (-list) ->
      sha256(name) % 4 teilt NAMED TESTS exakt auf 4 Shards; jeder Test laeuft in genau einer Zelle
      via `-run '^(<hash-selected>)$'`. owner-Mode laeuft 4 fixierte Tests.
- scripts/pr-gate-plan.py + pr-gate-coverage.json:
    * CLI-/internal/application-/internal/*-Routing waehelt package-checks; interne Pakete landen
      ueber CLI_PACKAGE_CHECKS/CODE_CHECKS auf `go test ./cmd/baha`/`go test ./internal/...`.
    * runtime_specific required_test_names binden Tests an native Gates (atomic/docker|podman/...).
      Im aktuellen Fenster TRAGT KEIN neuer Test einen required_test_names-Eintrag ->
      alle neuen Tests laufen ueber die Go-Shards, nicht ueber ein natives Runtime-Gate.
- .github/workflows/pre-release-runtime-suite.yml line 288:
    * GOFLAGS: -tags=baseharbor_ci_operator_testonly -> die build-tag-gaten
      `*_test.go` (z.B. cmd/baha/ci_integration_operator_enabled_test.go,
      //go:build baseharbor_ci_operator_testonly) laeuft nur in pr_runtime_selected (runtime_required==true).
      Die 8 `CIIntegrationOperatorAllowsOnlyGuided*`-Tests dieses Fensters sind CLI-hash-teilt
      (cli-0..3) UND zusätzlich build-tag-sichtbar; beide Wege decken.

## 3. Klassifikation JEDEN Namens
Klasse (a) von einer Zelle ausgewaehlt: JA fuer alle 338.
Klasse (b) go test ./... ohne -run: 234 interne Pakete (packages shard).
Klasse (c) nirgends: 0.

SUMME:
- Klasse (a) gesamt: 338 (100%)
- davon Klasse (b) broad packages shard: 234
- davon Klasse (a) CLI shard (hash): 93
- davon Klasse (a) build-tag operator: enthalten in den 93 CLI (plus native Sicht)
- Klasse (c) ohne Route: 0
- Fund-N ohne Route (datei:zeile): 0

## 4. Gegenprobe an drei Gelaufenen (job-conclusion + mutation-akte, nicht grep-abwesenheit)
- perses_dashboards_hosts_test.go (14 neue Tests) nachweisbar:
  `go test ./internal/metrics/ -list ".*" | grep -i PersesHostDashboard` liefert
  TestPersesHostDashboardCatalogHasRealBackendsOnly, TestPersesHostDashboardGoldenFiles,
  TestPersesHostDashboardJSONIsDeterministic, TestPersesHostDashboardKeysMatchSelectionCatalogKeys
  etc. -> Paket inventory existiert, packages shard fuehrt sie aus.
- internal/application: `go test ./internal/application/ -list ".*"` ->
  TestPersesRuntimeSmokeDockerIsolated (build-tag/native Sicht + packages shard).
- cli shard deterministisch: pr-go-unit-shard.py hash(name)%4 ordnet jeden Namen exakt einem
  cli-Zuordnungs-Fach zu; kein Test faellt durch (empty shard => fail-closed, also kein stilles Skip).

BELEG: gruene shard-protokolle enthalten keine RUN-Zeilen (PR-Memo cli-2 success = 22242 bytes ohne
RUN-zeile); 'kein name im gruenen protokoll' ist KEIN Gegenbeweis. hier nicht noetig: positiver
-list-Nachweis + mutation-akte dass die Namen am develop-HEAD existieren.

## 5. Fund je Klasse (c): NICHT ANWENDBAR
0 Tests in Klasse (c). Es gibt KEINEN fehlenden Grund auf Datei:Zeile-Ebene fuer dieses Fenster.
Kein Owner-Change notwendig (kein .github/**-Fund). Das PR-Memo 'app_list_all_targets_test.go'
erschien in keiner der drei Zellen — dieser Fall TRIFFT DIESER FENSTER NICHT: alle 338 neuen Tests
laufen. Falls ein kommener Fund doch klasse-c ist, muss der Owner die path-match-Regel in
scripts/pr-gate-plan.py oder scripts/pr-go-unit-shard.py aendern; hier kein file:line.

## ## cleanliness
docker ps -a vorher: 0 container (leere Tabelle, nur header).
docker ps -a nachher: 0 container (leere Tabelle, nur header).
rechner-ben: kein container, kein netzwerk, kein volume, kein state-verzeichnis des koordinators
erzeugt; der Klon lebt unter /tmp/opencode/221-wt (außerhalb des ecosystem-wurzels).
ambient-core/ bilder unangetastet.
cleanliness: sauber.

## ## repo-rule compliance
- KEINE produktdatei aendern (baseharbor). Nur Leserefeenzen auf develop-Klon.
- KEIN commit an baseharbor, KEINE PR-aktion.
- KEINE subagenten (4.8): jeder schritt in dieser session.
- KEIN nacktes `go test ./...` auf dem coordinator-host: verwendet habe nur `go test <pkg> -list`
  (keine ausführbaren container-faelle) und die CI-schreibweise im klon; kein docker-podman-start.
- KEIN git add -A, KEIN git stash im geteilten plan-checkout.
- evidence lebt NUR in baseharbor-plan/evidence/... ; kein .evidence/ im produkt-repo.

## ## end
LANE 0428-221-huntci: DONE. SHA des Klon-heads (nur lesbar): 4fa5293a49b7a6cd74c6513cf329dec15d08cfa9.
CLI-shard tests: 93
| 0428207CoreActivationFailsBeforeComposeWhenOwnerInventoryMissing | cli-0 | cmd/baha/core_network_binding_actionability_test.go |
| 0428207CoreNetworkBindingGuardActivationPathReturnsGuardedError | cli-3 | cmd/baha/core_network_binding_actionability_test.go |
| 0428207CoreNetworkBindingGuardFailClosedNeverSilent | cli-0 | cmd/baha/core_network_binding_actionability_test.go |
| 0428207CoreNetworkBindingGuardNamesMissingPreconditions | cli-2 | cmd/baha/core_network_binding_actionability_test.go |
| 0428207CoreNetworkBindingGuardNoncanonicalShape | cli-2 | cmd/baha/core_network_binding_actionability_test.go |
| ActivationSnippetRender | cli-0 | cmd/baha/context_terminal_test.go |
| AppDestroyReportsVersionMismatchNotNotRegistered | cli-1 | cmd/baha/w200_deployment_version_mismatch_test.go |
| AppEditApplyPartialHasNoDiagnosticStdoutInAnyDiagExecMode | cli-3 | cmd/baha/app_edit_diag_exec_stdout_test.go |
| AppEditDiagExecStdoutChild | cli-3 | cmd/baha/app_edit_diag_exec_stdout_test.go |
| AppStatusReportsVersionMismatchNotNotRegistered | cli-1 | cmd/baha/w200_deployment_version_mismatch_test.go |
| BahaStatusHostContainersDashboardsExposesUnavailable | cli-3 | cmd/baha/app_perses_host_containers_cli_test.go |
| BahaStatusPersesAccessDeclaresUnsupportedRoleMappings | cli-2 | cmd/baha/app_perses_access_cli_test.go |
| BahaStatusPersesAccessOutputCarriesNoCredentialNames | cli-0 | cmd/baha/app_perses_access_cli_test.go |
| CIIntegrationGuidedMCPPrincipalCanOnlySeeFootprintTool | cli-1 | cmd/baha/ci_integration_operator_enabled_test.go |
| CIIntegrationOperatorAllowsOnlyGuidedCoreRebootstrapRoot | cli-0 | cmd/baha/ci_integration_operator_enabled_test.go |
| CIIntegrationOperatorAllowsOnlyGuidedDeveloperDomainAndAppNew | cli-0 | cmd/baha/ci_integration_operator_enabled_test.go |
| CIIntegrationOperatorAllowsOnlyObservabilityLogProbe | cli-1 | cmd/baha/ci_integration_operator_enabled_test.go |
| CIIntegrationOperatorAllowsRootDestroyOnlyForGuidedGate | cli-3 | cmd/baha/ci_integration_operator_enabled_test.go |
| CIIntegrationOperatorIsExplicitlyScopedToManagedLocalGate | cli-1 | cmd/baha/ci_integration_operator_enabled_test.go |
| CIIntegrationOperatorIsLimitedToRemoteCoreAndTargetBootstrap | cli-1 | cmd/baha/ci_integration_operator_enabled_test.go |
| CIIntegrationOperatorTraceKeepsMachineErrorStreamClean | cli-1 | cmd/baha/ci_integration_operator_enabled_test.go |
| CLILocalWorkloadOperationIncludesGrantBackedRoots | cli-1 | cmd/baha/local_workload_authority_test.go |
| CLITargetCreateCanBootstrapSelectedTargetName | cli-0 | cmd/baha/target_uid_cli_test.go |
| CandidateConsentDigestRequiresExactToken | cli-3 | cmd/baha/app_candidate_consent_test.go |
| CompletionHookEmitted | cli-1 | cmd/baha/context_terminal_test.go |
| CompletionWorksWithHookInstalled | cli-2 | cmd/baha/context_terminal_test.go |
| ContextClearUnsetsInProcess | cli-3 | cmd/baha/context_terminal_test.go |
| ContextGroupRegistered | cli-1 | cmd/baha/context_terminal_test.go |
| ContextPrecedenceDefaultFallback | cli-1 | cmd/baha/context_terminal_test.go |
| ContextPrecedenceExplicitFlagWins | cli-0 | cmd/baha/context_terminal_test.go |
| ContextPrecedenceTerminalEnvWinsOverDefault | cli-2 | cmd/baha/context_terminal_test.go |
| ContextSelectionFailsClosedForAmbiguousTargets | cli-1 | cmd/baha/context_terminal_test.go |
| ContextShowPersistedWinsOverConfiguredDefault | cli-0 | cmd/baha/context_terminal_test.go |
| ContextShowReportsWinningStage | cli-3 | cmd/baha/context_terminal_test.go |
| ContextUseEmitsExportSnippet | cli-2 | cmd/baha/context_terminal_test.go |
| ContextUseFishSnippet | cli-1 | cmd/baha/context_terminal_test.go |
| ContextUseRejectsUnknownShell | cli-2 | cmd/baha/context_terminal_test.go |
| ContextUseRequiresTarget | cli-3 | cmd/baha/context_terminal_test.go |
| ContextWrapperCallsRealCommandViaCommand | cli-3 | cmd/baha/context_terminal_test.go |
| CoreDefaultNetworkBindingRejectsUnownedNativeNetwork | cli-0 | cmd/baha/operator_core_network_binding_native_test.go |
| EndToEndBashInteractiveContextUseAndClear | cli-1 | cmd/baha/context_terminal_test.go |
| EndToEndInstalledZshAndFishWrappers | cli-2 | cmd/baha/context_terminal_test.go |
| GuidedBackupFixtureBundledProviderChallengeRefreshesCandidateConsent | cli-1 | cmd/baha/app_backup_runtime_fixture_test.go |
| GuidedBackupFixtureCandidateRetryKeepsProviderConsent | cli-0 | cmd/baha/app_backup_runtime_fixture_test.go |
| GuidedBackupFixtureDestroyRequiresItsOwnDestructiveScope | cli-3 | cmd/baha/app_backup_runtime_fixture_test.go |
| GuidedBackupFixtureProviderRetryRefreshesCandidateConsent | cli-1 | cmd/baha/app_backup_runtime_fixture_test.go |
| GuidedBackupFixtureRefreshesCandidateAfterStaleDigest | cli-0 | cmd/baha/app_backup_runtime_fixture_test.go |
| HumanRevealRequiresAuthorizedMembership | cli-2 | cmd/baha/app_env_test.go |
| InteractiveGuardPresent | cli-2 | cmd/baha/context_terminal_test.go |
| InterruptedRetirementKeepsFrozenOwnerWhenRepositoryIntentChanges | cli-0 | cmd/baha/application_retired_owner_chain_test.go |
| LocalRuntimeImageResolveOverridePinsLoopbackRegistry | cli-1 | cmd/baha/application_registry_source_test.go |
| NativeBackendBindingInspectionManifestRejectsUnboundMongo | cli-3 | cmd/baha/application_native_backend_observation_test.go |
| NativeBackendBindingInspectionManifestRestoresMongoResources | cli-3 | cmd/baha/application_native_backend_observation_test.go |
| OperatorAuthBoundaryEnvironmentNamesFailClosed | cli-0 | cmd/baha/operator_auth_boundary_test.go |
| PersesAccessContractIsFailClosedOnMissingPin | cli-1 | cmd/baha/app_perses_access_cli_test.go |
| PersesAccessRoleMappingsAreFullyClassified | cli-3 | cmd/baha/app_perses_access_cli_test.go |
| PersesLifecycleCommandIsWiredIntoAppRoot | cli-3 | cmd/baha/perses_lifecycle_test.go |
| PersesLifecycleGatePredicate | cli-1 | cmd/baha/perses_lifecycle_transport_test.go |
| PersesLifecycleHumanNoticeForEveryDeferredAction | cli-2 | cmd/baha/perses_lifecycle_transport_test.go |
| PersesLifecycleMCPSharedSeamRunsApplyLifecycle | cli-1 | cmd/baha/perses_lifecycle_transport_test.go |
| PersesLifecycleTransportActionMatrix | cli-1 | cmd/baha/perses_lifecycle_transport_test.go |
| PersesStatusFailsClosedWithoutRepositoryManifest | cli-3 | cmd/baha/perses_lifecycle_test.go |
| ProviderImpactAcknowledgementStagesAllCarryAttention | cli-1 | cmd/baha/provider_change_confirmation_test.go |
| ProviderImpactMarkerPrintedOnEveryAcknowledgingStage | cli-3 | cmd/baha/provider_change_confirmation_test.go |
| ReactivatedIntentReplacesRetiredOwnerAndArchivesPreviousIntent | cli-3 | cmd/baha/application_retired_owner_chain_test.go |
| RepositoryComposePinnedWorkloadLifecycleInCI | cli-3 | cmd/baha/app_workload_integration_test.go |
| RepositoryDesiredStateFingerprintTracksLocalSourceFiles | cli-3 | cmd/baha/app_up_noop_test.go |
| RepositoryTreeFingerprintDoesNotFollowSymlinks | cli-2 | cmd/baha/app_up_noop_test.go |
| RequestPathRejectsDuplicateCapabilityMaskingRegistryChange | cli-3 | cmd/baha/application_provider_authorization_test.go |
| RequestPathRejectsOwnerApplicationRegistryChange | cli-1 | cmd/baha/application_provider_authorization_test.go |
| RequestPathRejectsOwnerEnvironmentRegistryChange | cli-0 | cmd/baha/application_provider_authorization_test.go |
| RequestPathRejectsReferenceRegistryChange | cli-1 | cmd/baha/application_provider_authorization_test.go |
| ResolveUsesPlainHTTPOnlyForLocalhostRegistry | cli-0 | cmd/baha/application_registry_source_test.go |
| ShellAbsentFallbackHints | cli-2 | cmd/baha/context_terminal_test.go |
| VerifiedLocalRuntimeGrantSatisfiesManagedEnvironmentBoundary | cli-0 | cmd/baha/local_workload_authority_test.go |
| VerifyManagedMetricsCompositionErrorBranchIsReached | cli-0 | cmd/baha/app_metrics_composition_state_test.go |
| VerifyManagedMetricsDedupesProviderCompositionState | cli-2 | cmd/baha/app_metrics_composition_state_test.go |
| VerifyManagedMetricsProviderCompositionStateReasonIsUniqueLine | cli-1 | cmd/baha/app_metrics_composition_state_test.go |
| VerifyManagedMetricsSurfacesNullTargetState | cli-1 | cmd/baha/app_metrics_composition_state_test.go |
| WorkspaceComponentAddListRemove | cli-2 | cmd/baha/app_workspace_source_model_test.go |
| WorkspaceGitStatusIncludesLocalGitSources | cli-1 | cmd/baha/app_workspace_source_model_test.go |
| WorkspaceInitAcceptsLocalDirectorySource | cli-0 | cmd/baha/app_workspace_source_model_test.go |
| WorkspaceInitRejectsArtificialComponents | cli-0 | cmd/baha/app_workspace_source_model_test.go |
| WorkspaceLocalSourceMappingOverridesPortablePath | cli-3 | cmd/baha/app_workspace_source_model_test.go |
| WorkspacePathRejectsForeignCheckoutOwnership | cli-1 | cmd/baha/app_workspace_source_model_test.go |
| WorkspacePathSetsAndShowsSourcePaths | cli-2 | cmd/baha/app_workspace_source_model_test.go |
| WorkspaceRootNamespaceMirrorsSourceModelCommands | cli-2 | cmd/baha/app_workspace_source_model_test.go |
| WorkspaceSourceAddAndRemoveDetachSafely | cli-2 | cmd/baha/app_workspace_source_model_test.go |
| WorkspaceSourceAddMissingIdentityValueReturnsUsageError | cli-0 | cmd/baha/app_workspace_source_model_test.go |
| WorkspaceSourceModelMachineParity | cli-1 | cmd/baha/app_workspace_source_model_test.go |
| WorkspaceSourceModelPreservesExistingMachineSemantics | cli-0 | cmd/baha/app_workspace_source_model_test.go |
| WorkspaceSourceModelWritesRequireUpdatePermission | cli-3 | cmd/baha/app_workspace_source_model_test.go |
| ZZProbeNoop | cli-0 | cmd/baha/zz_probe_test.go |
---
packages-shard tests: 234
| ApplicationClassLogSourceBindKeepsSiblings | internal/logs/appclass_log_writer_identity_test.go |
| ApplicationClassLogSourceDisabledPolicyReclaims | internal/logs/appclass_log_writer_test.go |
| ApplicationClassLogSourceDisabledPolicyReclaimsEveryService | internal/logs/appclass_log_writer_identity_test.go |
| ApplicationClassLogSourceHasProductionWriter | internal/logs/appclass_log_writer_test.go |
| ApplicationClassLogSourcePolicyDisableReclaims | internal/logs/appclass_log_writer_test.go |
| ApplicationClassLogSourceReconcileRegistersActiveServiceSet | internal/logs/appclass_log_writer_identity_test.go |
| ApplicationClassLogSourceReferenceClassCounterCheck | internal/logs/appclass_log_writer_test.go |
| ApplicationClassLogSourceSurvivesManagedReconcile | internal/logs/appclass_log_writer_test.go |
| ApplicationClassLogSourcesStayDistinguishablePerService | internal/logs/appclass_log_writer_identity_test.go |
| AuthorizeMachineOperationNameOnlyPolicyFailsClosed | internal/operatorauth/authorization_test.go |
| BuildPersesGatewayDeniesDatasourceProxy | internal/serviceaccess/perses_gateway_test.go |
| BuildPersesGatewayRefusesAnonymousSurface | internal/serviceaccess/perses_gateway_test.go |
| BuildPersesGatewayRendersProxyRefusalWithoutLeakingSecrets | internal/serviceaccess/perses_gateway_test.go |
| BuildPersesGatewayRequiresGatewayAuthentication | internal/serviceaccess/perses_gateway_test.go |
| CheckLocalRuntimeGrantFailsClosedAndUsesMonotonicNonce | internal/operatorauth/local_runtime_test.go |
| CompositionStateBackendSourceReportsOneEffectiveTarget | internal/metrics/composition_state_r4_test.go |
| CompositionStateEmptyRegistryReportsNoSource | internal/metrics/composition_state_r4_test.go |
| CompositionStateMatchesWriterSourceSet | internal/metrics/composition_state_r4_test.go |
| CompositionStateTwoEnvironmentsSameVerificationNoneID | internal/metrics/composition_state_r4_test.go |
| CompositionStateUsesManifestEnvironment | internal/metrics/composition_state_r4_test.go |
| ConsentDoesNotFoldUnwitnessedRuntimeState | internal/application/provider_consent_oscillation_test.go |
| ConsentSurvivesObservationClockChurn | internal/application/provider_consent_oscillation_test.go |
| ConsentSurvivesUnverifiableStateOscillation | internal/application/provider_consent_oscillation_test.go |
| DeregisterEnvironmentAssociationRejectsEnvironmentPathTraversal | internal/deployment/environment_association_test.go |
| EnsurePersesGatewayMaterialRequiresIssuerAndTLS | internal/serviceaccess/perses_gateway_test.go |
| EnsureProviderFilesCompositionStateCarriesState | internal/metrics/verify_none_red_test.go |
| EnvironmentPathNamesRejectTraversalBeforeAccess | internal/deployment/environment_identity_test.go |
| EqualProviderCapabilitiesRejectsDuplicateMasking | internal/application/provider_consent_oscillation_test.go |
| EqualRegistryBlockendBindingRetarget | internal/application/provider_consent_oscillation_test.go |
| EqualRegistryBlockendOwnerApplicationOnly | internal/application/provider_consent_oscillation_test.go |
| EqualRegistryBlockendOwnerEnvironmentOnly | internal/application/provider_consent_oscillation_test.go |
| EqualRegistryBlockendReferenceOnly | internal/application/provider_consent_oscillation_test.go |
| EqualRegistryBlockendSameCountDifferentContent | internal/application/provider_consent_oscillation_test.go |
| EqualRegistryBoundaryEmpty | internal/application/provider_consent_oscillation_test.go |
| EqualRegistryFailClosedReferenceAndEnvironment | internal/application/provider_consent_oscillation_test.go |
| EqualRegistryFailClosedRevalidation | internal/application/provider_consent_oscillation_test.go |
| EqualRegistryPositiveSameContentDifferentOrder | internal/application/provider_consent_oscillation_test.go |
| EvaluatePersesAnonymousDenialNamesNextCommand | internal/application/perses_management_ui_test.go |
| EvaluatePersesOperatorAccessAllowsScopedDatasource | internal/application/perses_management_ui_test.go |
| EvaluatePersesOperatorAccessAllowsVerifiedRoles | internal/application/perses_management_ui_test.go |
| EvaluatePersesOperatorAccessFailsClosedWithoutIdentity | internal/application/perses_management_ui_test.go |
| EvaluatePersesOperatorAccessReadOnlyDeniesMutatingRoles | internal/application/perses_management_ui_test.go |
| EvaluatePersesOperatorAccessRefusesAnonymousSurfaceEvenForAdmin | internal/application/perses_management_ui_test.go |
| EvaluatePersesOperatorAccessRefusesSSRFDatasourceEndpoint | internal/application/perses_management_ui_test.go |
| EvaluatePersesOperatorAccessRefusesVulnerablePin | internal/application/perses_management_ui_test.go |
| ImplicitComposeWorkloadRecordsSelectedServiceSet | internal/logs/appclass_writer_implicit_selection_test.go |
| ImplicitComposeWorkloadShrinkReclaimsStaleService | internal/logs/appclass_writer_implicit_selection_test.go |
| InstallRenameRefusesMismatchedDestination | internal/deployment/environment_identity_test.go |
| KeycloakSignalIDCollisionOnNormalizationBoundary | internal/identityprovider/keycloak_signal_collision_test.go |
| KeycloakSignalIDGoldenSingleTokenStable | internal/identityprovider/keycloak_signal_golden_test.go |
| KeycloakSignalRegistrationKeepsProjectsDistinct | internal/identityprovider/keycloak_signal_registration_test.go |
| LegacyKeycloakMetricsSourceCorpseProvesTheBug | internal/observability/keycloak_legacy_migration_test.go |
| LegacyTargetUIDMigrationRespectsConfigurationLock | internal/deployment/target_migration_test.go |
| ListApplicationMetricsRequiresExplicitClassAndApplicationScope | internal/observability/registry_test.go |
| ListDeploymentsForDisplaySurfacesVersionMismatch | internal/deployment/w200_deployment_version_mismatch_deploy_test.go |
| ListKeycloakOwnerProjectsReportsPartialScan | internal/identityprovider/keycloak_legacy_migration_integration_test.go |
| LocalRuntimeGrantIsOperationTargetEnvironmentBoundAndSingleUse | internal/operatorauth/local_runtime_test.go |
| ManagedEnvironmentCompatibilityWrapperFailsClosedForEveryName | internal/operatorauth/config_explicit_policy_test.go |
| ManagedEnvironmentFailsClosedForEveryName | internal/operatorauth/operatorauth_test.go |
| ManifestPersesSelectionRequiresManagementUI | internal/application/manifest_test.go |
| ManifestPersesSelectionRoundTripWithManagementUI | internal/application/manifest_test.go |
| MigrateScopedIsIdempotentAndWritesNoByte | internal/observability/keycloak_legacy_migration_test.go |
| MigrateScopedNeverCollidesWithCallersRegistration | internal/observability/keycloak_legacy_migration_test.go |
| MigrateScopedReBooksObservablyForOwner | internal/observability/keycloak_legacy_migration_test.go |
| NormalizedPersesUpstreamRejectsCredentialBearingAndRoutableAddresses | internal/serviceaccess/perses_gateway_test.go |
| PersesAccessDecisionCarriesNoSecretMaterial | internal/application/perses_management_ui_test.go |
| PersesComposeAliasLivesOnGatewayNotPerses | internal/application/perses_fix7_regression_test.go |
| PersesComposeRenderedWhenSelected | internal/application/perses_runtime_test.go |
| PersesComposeServicesNeverPublishesPersesDirectly | internal/serviceaccess/perses_gateway_test.go |
| PersesComposeServicesProvenanceFailClosed | internal/serviceaccess/perses_config_render_test.go |
| PersesComposeValidatesUnderRealToolchain | internal/application/perses_fix7_regression_test.go |
| PersesConfiguredUnverifiedWhenSelectedPinned | internal/application/perses_runtime_test.go |
| PersesDatabaseVolumeReplacementRegression | internal/application/perses_runtime_test.go |
| PersesGatewayMaterialProjectionKeepsPrivateKeyOwnerOnly | internal/serviceaccess/perses_gateway_test.go |
| PersesGatewayPlanForRequiresSelectionAndPolicy | internal/application/perses_management_ui_test.go |
| PersesGatewayReachabilityAuthAndHostInvisibility | internal/serviceaccess/perses_gateway_integration_test.go |
| PersesGatewayTokenAuthenticationRequiresTokenFileReference | internal/serviceaccess/perses_gateway_test.go |
| PersesHostDashboardAvailabilityConsumesAuthoritativeSignal | internal/metrics/perses_dashboards_hosts_test.go |
| PersesHostDashboardAvailabilityPerBackendNoInference | internal/metrics/perses_dashboards_hosts_test.go |
| PersesHostDashboardAvailableAvailabilityWitness | internal/metrics/perses_dashboards_hosts_test.go |
| PersesHostDashboardCatalogHasRealBackendsOnly | internal/metrics/perses_dashboards_hosts_test.go |
| PersesHostDashboardGoldenFiles | internal/metrics/perses_dashboards_hosts_test.go |
| PersesHostDashboardJSONIsDeterministic | internal/metrics/perses_dashboards_hosts_test.go |
| PersesHostDashboardKeysDistinctFromDatabaseDashboards | internal/metrics/perses_dashboards_hosts_test.go |
| PersesHostDashboardKeysMatchSelectionCatalogKeys | internal/metrics/perses_dashboards_hosts_test.go |
| PersesHostDashboardPersesNativeJSON | internal/metrics/perses_dashboards_hosts_test.go |
| PersesHostDashboardPersesNativeSchema | internal/metrics/perses_dashboards_hosts_test.go |
| PersesHostDashboardQueriesAreRealSignals | internal/metrics/perses_dashboards_hosts_test.go |
| PersesHostDashboardUnavailableAvailabilityWitness | internal/metrics/perses_dashboards_hosts_test.go |
| PersesHostDashboardUnavailableWithoutVerifiedSignal | internal/metrics/perses_dashboards_hosts_test.go |
| PersesHostUnavailableEntryMarshalsReason | internal/metrics/perses_dashboards_hosts_test.go |
| PersesLifecycleBackendPreservedInvariant | internal/application/perses_lifecycle_test.go |
| PersesLifecycleEnableIdempotentWhenAlreadySelected | internal/application/perses_lifecycle_test.go |
| PersesLifecycleEnableSetsPersesFlag | internal/application/perses_lifecycle_test.go |
| PersesLifecycleRejectsPersesWithoutObservabilitySurface | internal/application/perses_lifecycle_test.go |
| PersesLifecycleRemovePreservesBackendDataOwners | internal/application/perses_lifecycle_test.go |
| PersesLifecycleResourcesIncludeManagedService | internal/application/perses_runtime_test.go |
| PersesLifecycleStatusThreeStates | internal/application/perses_lifecycle_test.go |
| PersesLifecycleUnauthorizedIsFailClosed | internal/application/perses_lifecycle_test.go |
| PersesLifecycleUnresolvedOwnershipFailClosed | internal/application/perses_lifecycle_test.go |
| PersesLokiDatasourceEmitsNativeResource | internal/logs/loki_test.go |
| PersesLokiDatasourceFailClosedWhenEndpointAbsent | internal/logs/loki_test.go |
| PersesLokiDatasourceFailClosedWhenForeignOwned | internal/logs/loki_test.go |
| PersesLokiDatasourceFailClosedWhenProviderAbsent | internal/logs/loki_test.go |
| PersesLokiDatasourceFailClosedWhenSourceAbsent | internal/logs/loki_test.go |
| PersesLokiDatasourceFailClosedWhenUnselected | internal/logs/loki_test.go |
| PersesLokiDatasourceGoldenFiles | internal/logs/loki_test.go |
| PersesLokiDatasourceMultiSourceNoneMatchFailsClosed | internal/logs/loki_test.go |
| PersesLokiDatasourceMultiSourcePartialMatchability | internal/logs/loki_test.go |
| PersesLokiDatasourceMultiSourceQueryOneSelectorPerSource | internal/logs/loki_test.go |
| PersesLokiDatasourceNamesLokiOwner | internal/logs/loki_test.go |
| PersesLokiDatasourceNoCapabilityClaim | internal/logs/loki_test.go |
| PersesLokiDatasourceNoSecretInDescriptor | internal/logs/loki_test.go |
| PersesLokiDatasourceReachabilityUnverified | internal/logs/loki_test.go |
| PersesLokiDatasourceVerifyBindsServiceAccessClient | internal/logs/loki_test.go |
| PersesLokiDatasourceVerifyFailsClosedWithoutProbe | internal/logs/loki_test.go |
| PersesLokiDatasourceVerifyNeverReportsHealthy | internal/logs/loki_test.go |
| PersesMessagingAvailabilityMapIsExplicit | internal/metrics/perses_dashboards_messaging_test.go |
| PersesMessagingCatalogIsUnavailableWithoutNativeSignal | internal/metrics/perses_dashboards_messaging_test.go |
| PersesMessagingEligibilityFailsClosedForSelectionAndInventories | internal/metrics/perses_dashboards_messaging_test.go |
| PersesMessagingEligibilityFailsClosedWithoutPinnedRelease | internal/metrics/perses_dashboards_messaging_test.go |
| PersesMessagingNativeSignalRequiresBackendVerification | internal/metrics/perses_dashboards_messaging_test.go |
| PersesMessagingUnavailableJSONMatchesGolden | internal/metrics/perses_dashboards_messaging_test.go |
| PersesMountedConfigProvenanceAndEffectivePolicy | internal/application/perses_config_provenance_test.go |
| PersesNotConfiguredWithoutSelection | internal/application/perses_runtime_test.go |
| PersesOwnershipErrorIsTheSentinelForUnattributableRequests | internal/application/perses_management_ui_test.go |
| PersesProductionComposeFailsClosedWithoutKeyMaterial | internal/application/perses_fix6_regression_test.go |
| PersesProductionComposeIsGatewayOnlyExposure | internal/application/perses_fix6_regression_test.go |
| PersesProductionComposeMountsKeyAndConfig | internal/application/perses_fix6_regression_test.go |
| PersesProxyDestinationAllowedHostsListIsAuthoritative | internal/capability/perses_security_test.go |
| PersesProxyDestinationDeniesPrivateNetworksWhenConfigured | internal/capability/perses_security_test.go |
| PersesProxyDestinationDeniesUpstreamDefaultSet | internal/capability/perses_security_test.go |
| PersesProxyDestinationFailsClosedOnUnparseableEndpoints | internal/capability/perses_security_test.go |
| PersesProxyDestinationMostSpecificWinsAgainstDefaultDeny | internal/capability/perses_security_test.go |
| PersesProxyDestinationRejectsCredentialsAndSchemes | internal/capability/perses_security_test.go |
| PersesProxySSRFDenyNetworksAddsTargetKnowledge | internal/serviceaccess/perses_gateway_test.go |
| PersesProxySafeDefaultsAreStatedAndSorted | internal/capability/perses_security_test.go |
| PersesRenderedConfigAuthenticationProviderIsValid | internal/application/perses_fix7_regression_test.go |
| PersesRoleMappingsNeverClaimUnsupportedAuthorization | internal/application/perses_management_ui_test.go |
| PersesRuntimeFilesProjectProviderFiles | internal/application/perses_runtime_test.go |
| PersesRuntimeFilesRequireConfigProducerFailClosed | internal/application/perses_config_provenance_test.go |
| PersesRuntimeSmokeDockerIsolated | internal/application/perses_runtime_test.go |
| PersesRuntimeVolumeNameIsStableAndIsolated | internal/application/perses_runtime_test.go |
| PersesSecurityPolicyAcceptsAbsoluteSecretDirectories | internal/capability/perses_security_test.go |
| PersesSecurityPolicyDefaultValidates | internal/capability/perses_security_test.go |
| PersesSecurityPolicyRejectsAnonymousExposure | internal/capability/perses_security_test.go |
| PersesSecurityPolicyRejectsCredentialForwarding | internal/capability/perses_security_test.go |
| PersesSecurityPolicyRejectsVulnerablePins | internal/capability/perses_security_test.go |
| PersesSecurityPolicyRequiresEncryptionKeyWhenAuthEnabled | internal/capability/perses_security_test.go |
| PersesSecurityPolicyRequiresProxyRestriction | internal/capability/perses_security_test.go |
| PersesSecurityPolicyValidatesNetworkAndSchemeSyntax | internal/capability/perses_security_test.go |
| PersesStatusCannotReportConfiguredForAnonymousSurface | internal/capability/perses_security_test.go |
| PersesTLSFilesProjectedAndConsumed | internal/application/perses_runtime_test.go |
| PersesUITLSRequiredIsFailClosed | internal/application/perses_runtime_test.go |
| PostgreSQLAndValkeyMetricsAreNotRequiresAdapter | internal/capability/integration_contract_test.go |
| PostgreSQLAndValkeyMetricsWithoutProducerFailCatalog | internal/capability/integration_contract_test.go |
| ProviderCompositionStateEmptySourceListIsNoSource | internal/metrics/verify_none_red_test.go |
| ProviderCompositionStateNonEmptyAllNoneReportsNullTarget | internal/metrics/verify_none_red_test.go |
| ProviderImpactPlansConsentEquivalentStabilizesClassification | internal/application/provider_consent_oscillation_test.go |
| ProviderResultNonContinuationBehaviourPin | internal/application/provider_change_dependency_result_test.go |
| ReadSignalsForTestSortsStably | internal/observability/read_signals_test.go |
| RebookLegacySignalsConvergesCallerOwnRecordToRegistrationID | internal/observability/keycloak_legacy_migration_test.go |
| RebookLegacySignalsPreservesEverySourceField | internal/observability/keycloak_legacy_migration_test.go |
| ReconcileMatchingFailsClosedOnForeignProviderSource | internal/logs/appclass_log_writer_test.go |
| RedAllVerificationNoneHasNoCompositionCounter | internal/metrics/verify_none_red_test.go |
| RegVisibilityApplicationNamedProviderIsDisjoint | internal/metrics/regvisibility_regression_test.go |
| RegVisibilityDeselectedProviderFileRemovedByApplicationSync | internal/metrics/regvisibility_regression_test.go |
| RegVisibilityDeselectedProviderFileRemovedByProviderSync | internal/metrics/regvisibility_regression_test.go |
| RegVisibilityForeignProviderFileSurvivesApplicationReconciliation | internal/metrics/regvisibility_regression_test.go |
| RegVisibilityLiveSecondOwnerSurvivesProviderSync | internal/metrics/regvisibility_regression_test.go |
| RegVisibilityProviderFileGlobClassification | internal/metrics/regvisibility_regression_test.go |
| RegVisibilityProviderFileGlobCorruption | internal/metrics/regvisibility_regression_test.go |
| RegVisibilityStaleApplicationTargetReconciledOnSync | internal/metrics/regvisibility_regression_test.go |
| RegisterKeycloakSignalsAbortsOnPartialOwnerStateScan | internal/identityprovider/keycloak_legacy_migration_integration_test.go |
| RegisterKeycloakSignalsAbortsOnUnreadableLegacyRegistry | internal/identityprovider/keycloak_legacy_migration_integration_test.go |
| RegisterKeycloakSignalsCommitsLegacyRebookBeforeRejectingCollision | internal/identityprovider/keycloak_legacy_migration_integration_test.go |
| RegisterKeycloakSignalsPreservesCanonicalLegacyOwnerOnCollision | internal/identityprovider/keycloak_legacy_migration_integration_test.go |
| RegisterKeycloakSignalsPreservesLegacySourceForOwner | internal/identityprovider/keycloak_legacy_migration_integration_test.go |
| RegisterKeycloakSignalsRebooksLegacyOwnerWithoutStateDir | internal/identityprovider/keycloak_legacy_migration_integration_test.go |
| RegisterKeycloakSignalsSecondRegistrationIsNoMutationOnFirst | internal/identityprovider/keycloak_legacy_migration_integration_test.go |
| RegisterProviderSignalsRebooksLegacyBeforeReplacement | internal/observability/keycloak_legacy_migration_test.go |
| RemoveSourceRejectsLastSourceAndReportsReferences | internal/development/source_model_test.go |
| RenamePreservesEnvironmentAssociations | internal/deployment/environment_identity_test.go |
| RenameRetryCleansSourceAfterInterruptedInstall | internal/deployment/environment_identity_test.go |
| RenderPersesConfigFailsClosedForInvalidPosture | internal/serviceaccess/perses_config_render_test.go |
| RenderPersesConfigIsDeterministicAndCredentialFree | internal/serviceaccess/perses_config_render_test.go |
| ResolveCompatibilityWrapperFailsClosedForEveryName | internal/serviceaccess/policy_explicit_test.go |
| ResolveDefaultsToManagedLocalTLSAndAuthentication | internal/serviceaccess/policy_test.go |
| ResolveHostDashboardSignalStatusFailClosed | internal/capability/perses_test.go |
| ResolveHostDashboardSignalStatusRequiresNativeSignalWitness | internal/capability/perses_test.go |
| ResolveWorkloadSecurityPolicyCompatibilityWrapperFailsClosed | internal/application/workload_security_explicit_policy_test.go |
| ResolveWorkspaceLocalDirectoryWithSubPaths | internal/development/source_model_test.go |
| ResolveWorkspaceRejectsSubpathSymlinkEscapes | internal/development/source_model_test.go |
| Route2AnchorRuleTable | internal/observability/envfilter_route2_test.go |
| Route2EmptyRequestedEnvironmentFailsClosed | internal/observability/envfilter_route2_test.go |
| Route2HyphenatedApplicationProvider | internal/observability/envfilter_route2_test.go |
| Route2MutationEnvDropExcludes | internal/observability/envfilter_route2_test.go |
| Route2ProviderEnvMatch | internal/observability/envfilter_route2_test.go |
| Route2SameAppProdStageProdCaller | internal/observability/envfilter_route2_test.go |
| Route2SharedSourceStaysVisibleForSharedCaller | internal/observability/envfilter_route2_test.go |
| Route2UnresolvableAppSourceFailsClosed | internal/observability/envfilter_route2_test.go |
| Route5ContradictingCanonicalSidesFailClosed | internal/observability/envfilter_route5_listseam_test.go |
| Route5ListSeamCaseC_MyAppDevIncludesProdExcludes | internal/observability/envfilter_route5_listseam_test.go |
| Route5LogsCaseA_DemoWestCallerExcludes | internal/observability/envfilter_route5_listseam_test.go |
| Route5LogsCaseB_DemoProdWestCallerIncludes | internal/observability/envfilter_route5_listseam_test.go |
| Route5MetricsCaseA_DemoWestCallerExcludes | internal/observability/envfilter_route5_listseam_test.go |
| Route5MetricsCaseB_DemoProdWestCallerIncludes | internal/observability/envfilter_route5_listseam_test.go |
| Route5MutationAnchorDestruction | internal/observability/envfilter_route5_listseam_test.go |
| Route5ServiceDimensionInert | internal/observability/envfilter_route5_listseam_test.go |
| RuntimeSourceSeparatesTargetFilesPerEnvironment | internal/metrics/runtime_source_envkey_0428_125_test.go |
| SaveRemovableSourceDetachesMappingOnly | internal/development/source_model_test.go |
| SaveRemovableSourceDoesNotChangeModelWhenMappingCannotBeLoaded | internal/development/source_model_test.go |
| SaveRemovableSourceRollsBackWhenMappingSaveFails | internal/development/source_model_test.go |
| SaveRouteXDGGhostStillRejected | internal/deployment/config_mutation_test.go |
| SaveStateRouteFirstWriteNotRejectedAsGhost | internal/deployment/config_mutation_test.go |
| SharedDestroyKeepsEnvironmentForRegistryPruneRetry | internal/application/shared_backends_resources_runtime_test.go |
| SharedDestroyPreservesForeignPlatformSources | internal/application/shared_backends_resources_runtime_test.go |
| SharedDestroyRemovesOwnedPlatformSources | internal/application/shared_backends_resources_runtime_test.go |
| SourceAndComponentUpsertReplaceWithoutDuplicates | internal/development/source_model_test.go |
| SourceModelAllowsOptionalUniqueComponents | internal/development/source_model_test.go |
| SourceModelLocalDirectorySource | internal/development/source_model_test.go |
| UntrustedEnvironmentNameCannotEnableDevelopmentMode | internal/application/workload_security_explicit_policy_test.go |
| ValidateNameAcceptsSlugsAndRejectsPathNames | internal/environment/environment_test.go |
| ValidatePersesEndpointTrustRejectsPlainOrRoutableEndpoints | internal/application/perses_management_ui_test.go |
| VerificationNoneCompositionReportsNullTargetState | internal/metrics/verify_none_red_test.go |
| VerifyApplicationSourceVerificationNoneIsSkipped | internal/metrics/prometheus_verify_workload_only_test.go |
| VerifyApplicationSourceVerificationNoneRetiresPreviouslyEmitted | internal/metrics/prometheus_verify_workload_only_test.go |
| VerifyNoneCompositionSurfacesNullTargetState | internal/metrics/composition_state_verify_test.go |
| VerifyPositiveTargetCompositionReportsOneTarget | internal/metrics/composition_state_verify_test.go |
| VerifyProviderAndApplicationSourcesSkipsOnlySnapshotMetadata | internal/metrics/prometheus_verify_workload_only_test.go |
| VerifyUnchangedNoCompositionDoesNotSurfaceState | internal/metrics/composition_state_verify_test.go |
| WithEnforcementIfAbsentPreservesAuthenticatedAuthorizationState | internal/operatorauth/authorization_test.go |
| WorldWritableMigrationRejectsForeignOwnedRegularFile | internal/orgconfig/orgconfig_test.go |
| WorldWritableMigrationRejectsUntrustedDirectoryAncestor | internal/orgconfig/orgconfig_test.go |
