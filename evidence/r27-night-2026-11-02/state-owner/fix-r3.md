# Fix round r3 — grant-only TenantOwnerResolver + real seams

Lane: w14-stateowner-resolver · Role: Worker · Coord: f49a3303
Basis: PR #1347 head 47c1993d (branch work/r27-state-owner, base develop).
Kanditat: **dea01b83b53b3942fba74dd8b0e64a0daaf8bea0** (Merge remote-tracking branch 'origin/develop' into
work/r27-state-owner; FF von e9c30f52, ANCESTOR_RC=0 auf develop 9a57107f). ls-remote==head.
Befundquelle: review-1347b Befunde 1-3. Kernfehler: deployment.TenantOwnerResolver war VETO-hook
(authorized=false => ErrDeploymentOwnerForeign), coreinstallation.Load lief NUR wenn hook==nil. CLI-hook
gab bei nicht-aufloesbarem/nicht-tenant target (true,nil) => Core-pruefung umgangen (fail-open).

## PLAN

1. HOOK SEMANTIKN (internal/deployment/deployment_store.go VerifyDeploymentOwner): TenantOwnerResolver
   GRANT-only — (true,nil) => tenant-pfad autorisiert, return nil. Alle andere rueckgaben
   ((false,nil)/(false,err)/(true,err)) => durchfallen auf unveraenderten coreinstallation.Load
   single-installation-owner-check. Kein Frueh-Return, kein Foreign-Shortcut im !authorized-zweig.
2. CLI HOOK (cmd/baha/deployment_record.go init): !ok/!isTenant => (false,nil) durch zur Core-pruefung
   (frueher (true,nil), fail-open). tenant+connectorScopeForTarget err => (false,err) propagiert.
   scope.Validate() err => (false,nil); nur gueltiger scope => (true,nil).
3. TESTS (echte seams):
   a) internal/deployment: unit-test fuer alle drei hook-ergbnisse (grant=>nil,
      (false,nil)=>faellt durch auf coreinstallation-pruefung, err=>propagiert).
      TestTenantOwnerResolverGrantOnly + TestDeploymentOwnerTenantBypassGrantOnlyThroughSeam.
   b) cmd/baha: integration-test des echten SaveDeploymentRecord-pfades — negativer tenant scope =>
      abgewiesen (beweis: kein persisted state); nicht-tenant ohne Core installation => abgewiesen;
      gueltiger tenant => durchgelassen. TestTenantOwnerResolverCLIFallsThroughProvesNoBypass +
      TestDeploymentRecordHookPropagatesError.
   c) fixture-helfer configureTestTargetEmpty (cmd/baha/target_test_helpers_test.go): RemoveAll/
      TargetStateRoot-fehler => t.Fatal statt still skip.

## repo-rule compliance

- Write-set streng auf Task-Vortrag begrenzt: internal/deployment/deployment_store.go (resolver/store),
  cmd/baha/deployment_record.go (resolver/store), cmd/baha/target_test_helpers_test.go + 9 cmd/baha
  test-dateien (NUR registerInstallationForTarget/tenant-config an 12 sites, test-semantik/unveraendert),
  neue state-owner tests (deployment_owner_binding_test.go, deployment_tenant_owner_hook_test.go).
- KEINE CI/authority-dateien im commit (grep .github/scripts/contracts etc. leer).
- resolver/store NICHT angefasst um tests gruen zu machen — nur die seam-anderung der karte.
- STOP-Regel eingehalten: 1 iteration je punkt. Kein force-push, kein merge-force.

## 12 fix-sites (registerInstallationForTarget an den echten write-sites, test-semantik unveraendert)

- cmd/baha/app_backup_restore_integration_test.go:345 — configureAppBackupRuntimeTarget (TestGuidedBackupFixture*)
- cmd/baha/app_backup_non_tty_test.go:26 — TestNonTTYBackupDefaultUsesProtectedExternalArchive (install nach XDG_DATA_HOME-switch)
- cmd/baha/app_context_incomplete_test.go:17 — TestResolveRegisteredApplicationRecoversIncompleteDeploymentFromProtectedState
- cmd/baha/app_context_incomplete_test.go:56 — TestResolveRegisteredApplicationFailsClosedWhenIncompleteStateCannotBeReconstructed
- cmd/baha/update_core_isolated_test.go:43 — TestIsolatedCoreInventoryOnlyRegisteredOwnedProject (SaveDeploymentRecord)
- cmd/baha/update_core_isolated_test.go:104 — TestIsolatedCoreInventoryRejectsRuntimeMismatch (SaveDeploymentRecord)
- cmd/baha/application_runtime_retirement_preferences_test.go:39 — TestGuidedWithdrawalPreferencesPreserveCanonicalOwners (install fuer other-dev)
- cmd/baha/application_provider_pending_consumer_test.go:75 — TestOtherInterruptedApplyRetainsOneConsumerAndPreviousBindings (Coreless-tenant: install entfernt + node-connector binding => grant-only hook)
- cmd/baha/application_backend_binding_change_test.go:58 — backendBindingFixtureEmpty: Coreless-tenant (install entfernt + connector binding), TestBackendBindingReplacementPlan + TestInterruptedBackendReplacement
- cmd/baha/app_backup_non_tty_test.go + app_backup_restore_integration_test.go + update_core_isolated_test.go — je 1 zeilen-verweis oben

Exception (regel 3): TestOtherInterruptedApply + backendBindingFixtureEmpty sind gezielt CORELESS —
statt ergaenzende installation => Coreless-tenant mit gueltiger node-connector access binding (grant-only
hook laesst durch). Semantik bleibt "kein Core installation owner".

## verifizerer

- go build ./... rc=0
- go test ./internal/deployment/... => ok (0.017s)
- go test ./cmd/baha/... => 864 pass/fail; remaining 5 failures EXACTLY equal clean-base 5
  (TestAppEditCommandCompleteProviderEditRunsRealLifecycle, TestDoctorNotDeployedVersusIncomplete,
  TestExternalProviderRemoval{CannotInferGlobalOwnershipFromTenantRole,ChecksEveryManagedConsumerBeforeMutation,
  TransportsShareScopeAndExplicitStages}) — environment/Docker-abhaengig, rc auf clean-base identisch,
  KEINE regression.
- gofmt -l ueber alle aenderten files => leer (clean)
- ANSANDE: merge origin/develop is-ancestor rc=0; write-set grep .github/scripts/contracts leer
- push FF origin work/r27-state-owner: 47c1993d..e9c30f52; ls-remote origin work/r27-state-owner == e9c30f52 == local HEAD
## merge-block (w14-mergeblock.sh)
- skript cd'd selbst, fail-fast; fetch origin develop(9a57107f)+work/r27-state-owner; merge --no-edit
  origin/develop => clean merge (9 files contracts/managementaccess/v1新增, KEIN konflikt); build ./... rc=0;
  go test ./internal/deployment ok; push FF e9c30f52..dea01b83; ls-remote==dea01b83==local HEAD;
  ANCESTOR_RC=0 (9a57107f ancestor). kein force-push.

## END line

END_DONE w14-stateowner-resolver: head=dea01b83 grant-only=3tests | deploy.store+cli.hook grant-only (bypass gone); 12 cmd/baha deployment-owner tests an write-sites provisioned/coresless-tenant; internal/deployment green + cmd/baha only 5 env-fails (=clean-base, no regression); FF push e9c30f52..dea01b83; ANCESTOR_RC=0 (develop 9a57107f ancestor); ls-remote==head.
