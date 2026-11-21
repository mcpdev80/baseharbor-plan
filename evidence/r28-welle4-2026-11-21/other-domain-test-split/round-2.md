# 0428-206 other-domain test split — round 2 (recount over the neutral production path)

round-1: evidence/r28-welle4-2026-11-20/other-domain-test-split/round-1.md

- Lane: w206-0428-206-testsplit-recount (sitz flash, session ca3a71d0)
- Card: 0428-206 `t-20261120-other-domain-test-split`, state active
- Mission: rebuild the first-level failure inventory row-by-row after the CODEX-REVIEW verdict
  (`evidence/r28-welle4-2026-11-21/other-domain-test-split/codex-review-r2.md`, plan 8a086890:
  "REJECT the round-1 classification as incomplete"). Coordinator rulings: /var/tmp/a206.txt,
  /var/tmp/go206.txt, /var/tmp/go206b.txt, /var/tmp/a206c.txt.
- Result: DONE (read-only). The 117 first-level failures of the neutral production path are inventoried
  row-by-row with a hosted carrier per row; 97 are the operator-auth gate, 9 fail with another hosted
  message, 7 more are gate-backed only by a subtest, 1 by a subtest with another cause, and 3 have no
  hosted error line at all ("ohne nachweis") — summenprobe 97+7+9+1+3 = 117 (§3). The old "89"
  is shown to have never had a proof carrier (§3). No product change, no PR, no hosted rerun.

## PLAN

- 1. Mission and verdict read; `/tmp/w206-rerun.json` checked — absent on this host — done
- 2. Neutral production path established: hosted job logs of run 44850031032 (PR #1726, head
  `7db142852d22133b0d1cb7d33a9f8dc5eb11274d`), cells cli-0..3 — done
- 3. 117 distinct first-level failing names extracted (36+36+17+28 across cells); no local `go test` — done
- 4. Row-by-row class from the LOG FACT (gate message vs other message) + reachable-branch kind
  (runWithIO / direct .Run / domain fixture / shared-session MCP / direct call) — done
- 5. Heilungsprobe against #1615 head `7fae3a288f4a7639728a10b047bda9a36e35604a`: transitive
  stempel-pfad (call graph at that head) — 115/117 stamped, 2 not — done
- 6. "89 vs 117" evidence trio (ls-tree, ls /tmp, develop-push cell table) — done
- 7. "Zwei Methoden, zwei Cohorten" (cards 0428-213/214/210 named, one line each) — done
- 8. `git credential fill` hang located at file:line; no invented cause — done
- 9. "Wo round-1 sich verzehlt hat": the four verdict objections answered singly — done
- 10. repo-rule compliance + cleanliness + END — done (last actions)

## Basis attestation (remote truth, measured this session)

```
$ git remote -v | grep 'github.com/mcpdev80'
origin	https://github.com/mcpdev80/baseharbor.git (fetch)
origin	https://github.com/mcpdev80/baseharbor.git (push)
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v | grep '(fetch)'
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
```

Product reads live in the read-only partial clone `/tmp/opencode/w206-0428-206-split-wt`, detached at
exactly `40cb28c758b02960356434b630086a341ebe1738`. Ancestry witnesses (GitHub compare API):
`40cb28c758b0` is the merge-base of develop with both candidate heads (`7db142852d22` ahead 4,
`7fae3a288f4a` ahead 70). This card is read-only (AGENTS 4.4): no branch, no PR, therefore no
`git log origin/<base>..HEAD` — the clone carries zero commits over the base.

## 1) The neutral production path (cohort carrier)

Per coordinator ruling the ONLY counting source is the hosted cell logs; the local machine is excluded
(its ambient `bh-docker-dev-shared-*` stack was removed by a hop-lane around 03:0xZ following the
coordinator's own mission line "tear down orphaned containers" — coordinator-owned damage, not repaired
by lanes; local counts after that time are not comparable with the inherited CI and are not used here).

Cohort carrier: run `44850031032` (PR #1726, head `7db142852d22`, base develop `40cb28c758b0`), jobs:

| cell | job id | first-level fails |
| --- | --- | --- |
| PR · Go unit · cli-0 | 136678994688 | 36 |
| PR · Go unit · cli-1 | 136678994890 | 36 |
| PR · Go unit · cli-2 | 136678994909 | 17 |
| PR · Go unit · cli-3 | 136678994648 | 28 |
| summe | | 117 (distinct names, no overlap between cells) |

Logs were fetched via `curl -sL "https://api.github.com/repos/mcpdev80/baseharbor/actions/jobs/<id>/logs"`
(following the blob redirect; `gh run view --log` on this host returns "zip: not a valid zip file" — a
known read-path defect, not a permission failure). Scratch copies under `/tmp/opencode/w206r2/`.

Heal-counterproof (kept separate from the cohort): run `44854729670` (PR #1615, head `7fae3a288f4a`)
shows `PR · Go unit · cli-0..3` and `packages` = success at that head (re-measured completed at 03:4xZ).
#1615's current head has since moved (`5466a87bffe1`), so that green is on a superseded head — recorded
as the coordinator measured it, and it is the empirical counterproof against a purely static coverage map.

## 2) Row-by-row inventory (117 cases, each exactly once)

Columns: `fall | datei:zeile (Test-Definition am develop-Anker) | klasse (logsachverhalt) | wörtliche meldung (Auszug) | quelle des nachweises (job + Zeile im artefakt) | erreichbarer ast (Stempel-Kette zu #1615) | ast-typ | geheilt-durch-#1615 (transitiv, Zählung DIESER lane)`

`klasse` is only ever one of: `GATE` (the verbatim line carries an operator-auth message),
`ANDERER GRUND` (a hosted error line exists but its text is not the gate), `OHNE NACHWEIS`
(no hosted error carrier for this name in run 44850031032 — never estimated).

`geheilt-durch-#1615` was computed against the #1615 head blobs: a test is `ja` when any function on its
call path contains a `testOperatorContext(` / `runWithIOAsTestOperator(` / `operatorAuthFixtureContext(`
stamp added by #1615 (verified per file against diff-added line numbers; 0 line-gate violations).
The card's own class-A count is NOT implied here (coordinator ruling: "114/117 konvertierung ist THEIR
Zählung, nicht die der Karte"; this lane measures 115/117 transitively stamped).

### 2.1) The table (117 rows, each first-level case exactly once)

| fall | declaration | klasse (logsachverhalt) | abzug | woertliche meldung | nachweis-traeger | ast-typ | geheilt #1615 |
|---|---|---|---|---|---|---|---|
| TestActiveCoreConsumerIsConsequenceInsteadOfPermanentDestroyVeto | cmd/baha/control_plane_destroy_test.go:162 | GATE | B | active consumer blocked deliberate Core removal Managed-environment machine operations require an authenticated Bas… | run 44850031032 / job 136678994648 Z 273 / cmd/baha/control_plane_destroy_test.go:182 | domain fixture | ja |
| TestAppEnvMasksSecretsByDefaultAndRevealsExplicitly | cmd/baha/app_env_test.go:18 | GATE | A | environment query failed: &mcp.CallToolResult{Meta:mcp.Meta{"io.modelcontextprotocol/serverInfo":map[string]interfa… | run 44850031032 / job 136678994890 Z 273 / cmd/baha/app_env_test.go:60 | runWithIO | ja |
| TestAppListAllTargetsWorksAfterInstallationDestroy | cmd/baha/app_list_all_targets_test.go:12 | ANDERER GRUND | D | all-targets inventory depended on deleted Target config "docker-dev": BaseHarbor config root is configured but the … | run 44850031032 / job 136678994688 Z 273 / cmd/baha/app_list_all_targets_test.go:26 | direct .Run | ja |
| TestAppPruneMCPHappyPathRemovesUniquelyResolvedRecord | cmd/baha/app_prune_test.go:803 | GATE | C | MCP prune must remove the uniquely-resolved record: {"contract_version":"v1","error":{"code":"authentication_failed… | run 44850031032 / job 136678994909 Z 273 / cmd/baha/app_prune_test.go:863 | shared-session MCP | ja |
| TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation | cmd/baha/app_prune_test.go:678 | ANDERER GRUND | D | injected drift hook never fired: the registered handler's authorization→mutation seam was not exercised | run 44850031032 / job 136678994688 Z 278 / cmd/baha/app_prune_test.go:776 | shared-session MCP | ja |
| TestAppPruneMCPPreservesTargetOverride | cmd/baha/app_prune_test.go:537 | GATE | C | MCP prune with pinned second target must resolve the record on that target, got error: {"contract_version":"v1","er… | run 44850031032 / job 136678994890 Z 278 / cmd/baha/app_prune_test.go:640 | shared-session MCP | ja |
| TestApplicationDestroyCanProceedWithDamagedUnrelatedConsumerInventory | cmd/baha/application_destroy_authorization_test.go:18 | GATE | B | destroy must produce a partial plan for the selected app: Managed-environment machine operations require an authent… | run 44850031032 / job 136678994688 Z 283 / cmd/baha/application_destroy_authorization_test.go:33 | domain fixture | ja |
| TestApplicationDestroyUsesShortPlanAndSingleInteractiveApproval | cmd/baha/application_destroy_authorization_test.go:134 | GATE | B | interactive approval did not authorize the current plan: Managed-environment machine operations require an authenti… | run 44850031032 / job 136678994890 Z 283 / cmd/baha/application_destroy_authorization_test.go:139 | domain fixture | ja |
| TestApplicationDestroyWithoutInteractiveConsentGivesUsefulNextStep | cmd/baha/application_destroy_authorization_test.go:157 | GATE | B | expected a typed consent requirement, got Managed-environment machine operations require an authenticated BaseHarbo… | run 44850031032 / job 136678994909 Z 278 / cmd/baha/application_destroy_authorization_test.go:163 | domain fixture | ja |
| TestApplicationDestructionConsentInvalidatedByRetainedPublicationChange | cmd/baha/application_destroy_authorization_test.go:170 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994648 Z 278 / cmd/baha/application_destroy_authorization_test.go:174 | domain fixture | ja |
| TestApplicationDestructionRequiresCurrentOuterScopeAndSeparateDataConsent | cmd/baha/application_destroy_authorization_test.go:93 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994688 Z 288 / cmd/baha/application_destroy_authorization_test.go:103 | domain fixture | ja |
| TestApplicationStopCLIJSONMCPExposeSameRequiredAcknowledgement | cmd/baha/application_stop_impact_test.go:150 | GATE | A | CLI/MCP error semantic drift: {"contract_version":"v1","error":{"code":"authentication_failed","message":"Managed-e… | run 44850031032 / job 136678994909 Z 283 / cmd/baha/application_stop_impact_test.go:169 | runWithIO | ja |
| TestApplicationStopHTTPUsesCurrentScopeAndCannotEscapeAuthorizedContext | cmd/baha/application_stop_impact_test.go:187 | GATE | B | HTTP stop did not require current impact acknowledgement: Managed-environment machine operations require an authent… | run 44850031032 / job 136678994688 Z 293 / cmd/baha/application_stop_impact_test.go:194 | domain fixture | ja |
| TestBug865ForeignOrganizationAndSessionAreIsolated | cmd/baha/bugs_864_871_regression_test.go:247 | ANDERER GRUND | D | isolated MCP target <nil> | run 44850031032 / job 136678994890 Z 288 / cmd/baha/bugs_864_871_regression_test.go:292 | runWithIO | ja |
| TestCLIJSONAndMCPShareApplicationOverviewAndDevelopmentDomain | cmd/baha/mcp_json_parity_test.go:14 | GATE | A | app.show MCP: &mcp.CallToolResult{Meta:mcp.Meta{"io.modelcontextprotocol/serverInfo":map[string]interface {}{"name"… | run 44850031032 / job 136678994688 Z 298 / cmd/baha/mcp_json_parity_test.go:49 | runWithIO | ja |
| TestClientConsentFailsClosedWithoutTerminal | cmd/baha/app_client_consent_test.go:13 | ANDERER GRUND | D | missing transparent method in prompt:  | run 44850031032 / job 136678994890 Z 293 / cmd/baha/app_client_consent_test.go:30 | direct call | ja |
| TestClientConsentRejectsForgedLongExpiry | cmd/baha/app_client_consent_test.go:63 | GATE | B | Operator authentication is not configured. | run 44850031032 / job 136678994648 Z 283 / cmd/baha/app_client_consent_test.go:67 | direct call | ja |
| TestClientConsentRememberedOnlyForExactScope | cmd/baha/app_client_consent_test.go:42 | GATE | B | Operator authentication is not configured. | run 44850031032 / job 136678994688 Z 303 / cmd/baha/app_client_consent_test.go:47 | direct call | ja |
| TestContextualCLIErrorHintsAndContracts | cmd/baha/bugs_858_860_regression_test.go:314 | ANDERER GRUND (Subtest-Beleg) | D | Error | Parent ohne eigene Fehlerzeile; 1 Belegzeile(n) im Block, z.B. job 136678994648 Z 291 / cmd/baha/bugs_858_860_regression_test.go:336 | runWithIO | ja |
| TestCore921MCPEditHandlerLevelNegatives | cmd/baha/registration_921_test.go:228 | GATE | C | invalid-phase: handler returned code "authentication_failed", want "validation_failed" (payload: {"contract_version… | run 44850031032 / job 136678994909 Z 288 / cmd/baha/registration_921_test.go:279 | shared-session MCP | ja |
| TestCore921MCPProposeReachesHandlerWithZeroWrites | cmd/baha/registration_921_test.go:157 | GATE | C | stale-snapshot propose must classify as conflict, got "authentication_failed" (payload: {"contract_version":"v1","e… | run 44850031032 / job 136678994890 Z 298 / cmd/baha/registration_921_test.go:208 | shared-session MCP | ja |
| TestCoreStopCLIJSONAndMCPExposeSameCurrentScopeWithoutEnvironmentConsentReuse | cmd/baha/control_plane_stop_impact_test.go:144 | GATE | A | MCP error drift: {"contract_version":"v1","error":{"code":"authentication_failed","message":"Managed-environment ma… | run 44850031032 / job 136678994890 Z 352 / cmd/baha/control_plane_stop_impact_test.go:161 | runWithIO | ja |
| TestCoreStopUsesStableScopeRequiresTwoAcknowledgementsAndBindsCredentialBytes | cmd/baha/control_plane_stop_impact_test.go:104 | GATE | B | Core stop plan: {Scope:{Version: Owner:{Owner: Reference: Subject: Revision: Destructive:false} PlanID: Complete:fa… | run 44850031032 / job 136678994688 Z 308 / cmd/baha/control_plane_stop_impact_test.go:108 | domain fixture | ja |
| TestCorelessAcceptanceDestroyConsentBindsCurrentDestructivePlan | cmd/baha/app_coreless_runtime_test.go:298 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994688 Z 313 / cmd/baha/app_coreless_runtime_test.go:302 | domain fixture | ja |
| TestCorelessPlanCLIJSONMCPParityAndStableIdentity | cmd/baha/app_coreless_machine_test.go:14 | GATE | A | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994648 Z 302 / cmd/baha/app_coreless_machine_test.go:20 | runWithIO | ja |
| TestCreateTargetDoesNotBecomeDefaultWithoutFlag | cmd/baha/target_hotfix_test.go:32 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994648 Z 307 / cmd/baha/target_hotfix_test.go:43 | direct call | ja |
| TestCreateTargetManagedApplicationPersistsImmutableGitSourceSelection | cmd/baha/app_create_target_test.go:85 | GATE | B | persist immutable remote Git selection: Managed-environment machine operations require an authenticated BaseHarbor … | run 44850031032 / job 136678994648 Z 312 / cmd/baha/app_create_target_test.go:98 | direct call | ja |
| TestCreateTargetManagedApplicationRegistersResolvableDeployment | cmd/baha/app_create_target_test.go:15 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 357 / cmd/baha/app_create_target_test.go:21 | direct call | ja |
| TestCreateTargetSupportsRemoteNodeConnectorAccess | cmd/baha/target_hotfix_test.go:149 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 362 / cmd/baha/target_hotfix_test.go:166 | direct call | ja |
| TestDeleteTargetBlocksAutomaticSelectionUntilExplicitChoice | cmd/baha/target_selection_test.go:123 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994909 Z 376 / cmd/baha/target_selection_test.go:135 | direct call | ja |
| TestDestroyImpactChangesWithExactConfigBytes | cmd/baha/runtime_destroy_impact_test.go:80 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 367 / cmd/baha/runtime_destroy_impact_test.go:89 | domain fixture | ja |
| TestDeterministicInitDoesNotPersistUnneededSourceSelection | cmd/baha/app_init_source_neutral_test.go:64 | GATE | A | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994688 Z 318 / cmd/baha/app_init_source_neutral_test.go:72 | runWithIO | ja |
| TestDeterministicInitPersistsAmbiguousSourceSelectionPositive | cmd/baha/app_init_source_neutral_test.go:79 | GATE | A | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 372 / cmd/baha/app_init_source_neutral_test.go:90 | runWithIO | ja |
| TestDevelopmentCredentialsMCPNeverReturnsProtectedValue | cmd/baha/mcp_platform_tools_test.go:59 | GATE | C | MCP development configuration failed: &mcp.CallToolResult{Meta:mcp.Meta{"io.modelcontextprotocol/serverInfo":map[st… | run 44850031032 / job 136678994648 Z 317 / cmd/baha/mcp_platform_tools_test.go:71 | shared-session MCP | ja |
| TestDockerTargetIntentCLIAndMachineConfiguration | cmd/baha/docker_engine_binding_test.go:86 | GATE | A | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994688 Z 323 / cmd/baha/docker_engine_binding_test.go:93 | runWithIO | ja |
| TestDoctorNotDeployedVersusIncomplete | cmd/baha/bugs_858_860_regression_test.go:247 | OHNE NACHWEIS | D? | — | nur Run-Marker (job 136678994909 Z 379); kein FAIL-Block im Log | direct .Run | ja |
| TestExistingTargetPolicyInvalidEditCannotMutate | cmd/baha/target_deployment_policy_edit_test.go:62 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 377 / cmd/baha/target_deployment_policy_edit_test.go:69 | direct call | ja |
| TestExistingTargetPolicyPreservesOverridesAndCoreBinding | cmd/baha/target_deployment_policy_edit_test.go:12 | GATE | B | set test policy: Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994648 Z 322 / cmd/baha/target_deployment_policy_edit_test.go:24 | direct call | ja |
| TestExternalProviderRemovalTransportsShareScopeAndExplicitStages | cmd/baha/provider_external_removal_test.go:32 | GATE (Subtest-Beleg) | C | — (nur Subtest-Beleg) | Parent ohne Fehler-Block; Subtest-Belege existieren, aber der parent-Zähler dieser Akte fuehrt die Subtest-Zeilen nicht einzeln (cohort = first-level). Belegtraeger: Parent ohne eigene Fehlerzeile; 6 Belegzeile(n) im Block, z.B. job 136678994688 Z 331 / cmd/baha/provider_external_removal_test.go:79 | shared-session MCP | ja |
| TestFreshRestoreRejectsNewSourceAndOwnerBeforeMutation | cmd/baha/app_restore_fresh_identity_test.go:165 | GATE (Subtest-Beleg) | B | — (nur Subtest-Beleg) | Parent ohne Fehler-Block; Subtest-Belege existieren, aber der parent-Zähler dieser Akte fuehrt die Subtest-Zeilen nicht einzeln (cohort = first-level). Belegtraeger: Parent ohne eigene Fehlerzeile; 16 Belegzeile(n) im Block, z.B. job 136678994909 Z 418 / cmd/baha/app_restore_fresh_identity_test.go:186 | direct .Run | ja |
| TestFreshRestoreStableConsentAndCanonicalIdentityRecovery | cmd/baha/app_restore_fresh_identity_test.go:19 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994909 Z 449 / cmd/baha/app_restore_fresh_identity_test.go:47 | direct call | ja |
| TestFullDestroyDryRunDoesNotMutateState | cmd/baha/runtime_destroy_all_test.go:19 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994648 Z 327 / cmd/baha/runtime_destroy_all_test.go:37 | direct call | ja |
| TestFullDestroyJSONReportsPreservedCAOnFailure | cmd/baha/runtime_destroy_all_test.go:254 | ANDERER GRUND | D | JSON did not report preserved CA: {"destroyed":false,"preview":true,"all":true,"application_source_and_data_preserv… | run 44850031032 / job 136678994688 Z 347 / cmd/baha/runtime_destroy_all_test.go:269 | direct call | ja |
| TestFullDestroyPreservesGlobalOwnershipOnHostCAFailure | cmd/baha/runtime_destroy_all_test.go:218 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 382 / cmd/baha/runtime_destroy_all_test.go:242 | direct call | ja |
| TestFullDestroyPreservesOperatorRecoveryFileWithoutReadingContents | cmd/baha/runtime_destroy_inventory_test.go:187 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994648 Z 332 / cmd/baha/runtime_destroy_inventory_test.go:208 | direct call | ja |
| TestFullDestroyRemovesOwnedLocalStateButPreservesSourceRepository | cmd/baha/runtime_destroy_all_test.go:134 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 387 / cmd/baha/runtime_destroy_all_test.go:158 | direct call | ja |
| TestFullDestroyYesCannotReplacePlanOrDeletionConsent | cmd/baha/runtime_destroy_impact_test.go:48 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 392 / cmd/baha/runtime_destroy_impact_test.go:59 | direct call | ja |
| TestGeneratedBootstrapConsentRetainsCurrentIntent | cmd/baha/core_installation_runtime_test.go:662 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994688 Z 352 / cmd/baha/core_installation_runtime_test.go:675 | direct call | ja |
| TestGuidedBackupFixtureRestoreRequiresItsOwnDestructiveScope | cmd/baha/app_backup_runtime_fixture_test.go:496 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994688 Z 357 / cmd/baha/app_backup_runtime_fixture_test.go:501 | domain fixture | ja |
| TestGuidedRepositoryRuntimeFixtureRegressionSuite | cmd/baha/repository_runtime_fixture_test.go:741 | OHNE NACHWEIS | D? | — | nur Run-Marker (job 136678994688 Z 360); kein FAIL-Block im Log | direct .Run | nein |
| TestGuidedWithdrawalPreferencesPreserveCanonicalOwners | cmd/baha/application_runtime_retirement_preferences_test.go:19 | GATE | B | full destroy child plan rejects saved preference: Managed-environment machine operations require an authenticated B… | run 44850031032 / job 136678994909 Z 454 / cmd/baha/application_runtime_retirement_preferences_test.go:119 | domain fixture | ja |
| TestInitializeRepositoryManifestForUpQuickCreatesDetectedContract | cmd/baha/repository_up_init_test.go:12 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 397 / cmd/baha/repository_up_init_test.go:34 | direct call | ja |
| TestInstallationChildScopeAfterEarlierSiblingRemoval | cmd/baha/installation_sibling_scope_test.go:15 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994648 Z 337 / cmd/baha/installation_sibling_scope_test.go:36 | domain fixture | ja |
| TestInstallationDestroyCLIJSONMCPShareScopeAndRejectAmbientConsent | cmd/baha/runtime_destroy_impact_test.go:156 | GATE | C | CLI destruction bypass: Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 402 / cmd/baha/runtime_destroy_impact_test.go:165 | shared-session MCP | ja |
| TestInstallationDestructionDelegatesOnlyDisplayedCurrentChildScope | cmd/baha/installation_application_scopes_test.go:12 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994909 Z 459 / cmd/baha/installation_application_scopes_test.go:16 | domain fixture | ja |
| TestInstallationPlanDisclosesUnregisteredLocalStateWithoutInventingRuntimeOwner | cmd/baha/installation_discovery_scope_test.go:13 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994648 Z 342 / cmd/baha/installation_discovery_scope_test.go:18 | domain fixture | ja |
| TestInstallationUnknownTargetRuntimeIsDisclosureNotDestructionAuthority | cmd/baha/installation_discovery_scope_test.go:62 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994648 Z 347 / cmd/baha/installation_discovery_scope_test.go:67 | domain fixture | ja |
| TestInteractiveInstallationAcknowledgementsRemainBoundForDelegation | cmd/baha/installation_application_scopes_test.go:46 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 407 / cmd/baha/installation_application_scopes_test.go:50 | domain fixture | ja |
| TestMCPAuthoringAssignsCanonicalIdentityWithoutClientID | cmd/baha/mcp_application_authoring_test.go:17 | GATE (Subtest-Beleg) | C | — (nur Subtest-Beleg) | Parent ohne Fehler-Block; Subtest-Belege existieren, aber der parent-Zähler dieser Akte fuehrt die Subtest-Zeilen nicht einzeln (cohort = first-level). Belegtraeger: Parent ohne eigene Fehlerzeile; 3 Belegzeile(n) im Block, z.B. job 136678994648 Z 355 / cmd/baha/mcp_application_authoring_test.go:35 | shared-session MCP | ja |
| TestMCPAuthoringWorkloadComposeIsOptional | cmd/baha/mcp_application_authoring_test.go:180 | GATE | C | valid intent without Compose rejected: <nil> {"_meta":{"io.modelcontextprotocol/serverInfo":{"name":"baseharbor","v… | run 44850031032 / job 136678994909 Z 464 / cmd/baha/mcp_application_authoring_test.go:195 | shared-session MCP | ja |
| TestMCPReadEntryExpectedPreconditions | cmd/baha/mcp_preconditions_test.go:57 | OHNE NACHWEIS | D? | — | nur Run-Marker (job 136678994648 Z 364); kein FAIL-Block im Log | shared-session MCP | ja |
| TestMCPRegistrationCIInProcessDiscoverAndInvoke | cmd/baha/registration_ci_readiness_test.go:96 | GATE | C | in-process MCP app.list invocation failed: &{Meta:map[io.modelcontextprotocol/serverInfo:map[name:baseharbor versio… | run 44850031032 / job 136678994890 Z 412 / cmd/baha/registration_ci_readiness_test.go:118 | shared-session MCP | ja |
| TestMCPStackCreateListShowShareCLIJSON | cmd/baha/mcp_stack_tools_test.go:14 | GATE | C | create: &mcp.CallToolResult{Meta:mcp.Meta{"io.modelcontextprotocol/serverInfo":map[string]interface {}{"name":"base… | run 44850031032 / job 136678994890 Z 417 / cmd/baha/mcp_stack_tools_test.go:24 | shared-session MCP | ja |
| TestMCPTargetCreateAndDeleteRequireCurrentConsentAndPreserveOwnedState | cmd/baha/mcp_target_mutation_test.go:15 | GATE | C | create: &mcp.CallToolResult{Meta:mcp.Meta{"io.modelcontextprotocol/serverInfo":map[string]interface {}{"name":"base… | run 44850031032 / job 136678994890 Z 422 / cmd/baha/mcp_target_mutation_test.go:21 | shared-session MCP | ja |
| TestMCPWorkspaceInitAndMapShareCLIJSONOperations | cmd/baha/mcp_workspace_mutation_test.go:45 | GATE | C | MCP init: &mcp.CallToolResult{Meta:mcp.Meta{"io.modelcontextprotocol/serverInfo":map[string]interface {}{"name":"ba… | run 44850031032 / job 136678994688 Z 376 / cmd/baha/mcp_workspace_mutation_test.go:52 | shared-session MCP | ja |
| TestMinimalRepositoryIdentityInitializationAndReadSurfaces | cmd/baha/app_repository_identity_test.go:32 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994688 Z 381 / cmd/baha/app_repository_identity_test.go:48 | direct call | ja |
| TestNamedMinimalSourceUsesSameWorkloadAndIdentityWithoutWrites | cmd/baha/app_registered_minimal_source_test.go:14 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994688 Z 386 / cmd/baha/app_registered_minimal_source_test.go:20 | direct call | ja |
| TestOperatorAuthBoundaryDevTrustedLocalAndManagedEnvironmentsFailClosed | cmd/baha/operator_auth_boundary_test.go:12 | GATE | B | dev trusted-local boundary unexpectedly required authentication: operator OIDC configuration is required for manage… | run 44850031032 / job 136678994890 Z 427 / cmd/baha/operator_auth_boundary_test.go:23 | direct call | nein |
| TestOrganizationCLIJSONAndMCPShareEffectiveResolution | cmd/baha/config_org_test.go:46 | ANDERER GRUND | D | organization inspect returned error: []mcp.Content{(*mcp.TextContent)(0x33be2b63a900)} | run 44850031032 / job 136678994688 Z 391 / cmd/baha/config_org_test.go:98 | runWithIO | ja |
| TestPersesLifecycleMCPSharedSeamRunsApplyLifecycle | cmd/baha/perses_lifecycle_transport_test.go:206 | ANDERER GRUND | D | the deferred CLI result must carry the deferred action before the parity comparison | run 44850031032 / job 136678994688 Z 396 / cmd/baha/perses_lifecycle_transport_test.go:274 | shared-session MCP | ja |
| TestPlatformDestructionAndHostTrustNeedApprovalBeforeRuntime | cmd/baha/mcp_platform_tools_test.go:43 | GATE | C | control-plane.destroy checked runtime before approval: {"_meta":{"io.modelcontextprotocol/serverInfo":{"name":"base… | run 44850031032 / job 136678994688 Z 416 / cmd/baha/mcp_platform_tools_test.go:54 | shared-session MCP | ja |
| TestRejectedApplyAndTargetTeardownKeepSourcesWithoutGhostApplyingState | cmd/baha/deployment_observation_test.go:19 | GATE | A | inactive registration: []deployment.DeploymentRecord(nil) Managed-environment machine operations require an authent… | run 44850031032 / job 136678994890 Z 432 / cmd/baha/deployment_observation_test.go:55 | runWithIO | ja |
| TestRemoteCoreTargetCreateBindsTenantAndNeverFallsBackToLocalDocker | cmd/baha/target_remote_core_client_test.go:15 | GATE | B | remote Core Target could not be configured: Managed-environment machine operations require an authenticated BaseHar… | run 44850031032 / job 136678994688 Z 421 / cmd/baha/target_remote_core_client_test.go:26 | direct call | ja |
| TestRepositoryAdoptionReusesRetainedCanonicalIdentity | cmd/baha/mcp_application_authoring_test.go:110 | GATE | B | retained retry owner changed: {Application: ApplicationID: Environment: Manifest: SourceSelection:} Managed-environ… | run 44850031032 / job 136678994688 Z 426 / cmd/baha/mcp_application_authoring_test.go:122 | direct call | ja |
| TestRepositoryReinitializationReusesActualIdentityOwners | cmd/baha/app_init_retained_identity_test.go:17 | GATE (Subtest-Beleg) | A | — (nur Subtest-Beleg) | Parent ohne Fehler-Block; Subtest-Belege existieren, aber der parent-Zähler dieser Akte fuehrt die Subtest-Zeilen nicht einzeln (cohort = first-level). Belegtraeger: Parent ohne eigene Fehlerzeile; 5 Belegzeile(n) im Block, z.B. job 136678994648 Z 378 / cmd/baha/app_init_retained_identity_test.go:71 | runWithIO | ja |
| TestRestoreBindsCurrentExternalReceiverAndAuthorization | cmd/baha/application_restore_external_receiver_test.go:15 | GATE (Subtest-Beleg) | B | — (nur Subtest-Beleg) | Parent ohne Fehler-Block; Subtest-Belege existieren, aber der parent-Zähler dieser Akte fuehrt die Subtest-Zeilen nicht einzeln (cohort = first-level). Belegtraeger: Parent ohne eigene Fehlerzeile; 8 Belegzeile(n) im Block, z.B. job 136678994688 Z 434 / cmd/baha/application_restore_external_receiver_test.go:40 | direct .Run | ja |
| TestRestoreBindsRegisteredReceiverMaterialWithoutSurvivingDelivery | cmd/baha/application_restore_registered_receiver_test.go:85 | GATE (Subtest-Beleg) | B | — (nur Subtest-Beleg) | Parent ohne Fehler-Block; Subtest-Belege existieren, aber der parent-Zähler dieser Akte fuehrt die Subtest-Zeilen nicht einzeln (cohort = first-level). Belegtraeger: Parent ohne eigene Fehlerzeile; 36 Belegzeile(n) im Block, z.B. job 136678994890 Z 440 / cmd/baha/application_restore_registered_receiver_test.go:98 | direct .Run | ja |
| TestRestoreRefusesBeforeRuntimeMutationAndBindsArchiveOwnerAndDataDecision | cmd/baha/application_restore_authorization_test.go:16 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994909 Z 469 / cmd/baha/application_restore_authorization_test.go:24 | domain fixture | ja |
| TestRestoreRequiresCurrentConsentBeforeAdmittingSupportedIdentityPlacement | cmd/baha/app_restore_fresh_identity_test.go:103 | GATE | B | technical admission hid recovery consequences Managed-environment machine operations require an authenticated BaseH… | run 44850031032 / job 136678994688 Z 460 / cmd/baha/app_restore_fresh_identity_test.go:130 | domain fixture | ja |
| TestRuntimeUpEnsuresRuntimeImageBeforeStartingCore | cmd/baha/core_runtime_image_preflight_test.go:18 | GATE | B | baha up did not stop at runtime image preflight: called=false err=Managed-environment machine operations require an… | run 44850031032 / job 136678994890 Z 481 / cmd/baha/core_runtime_image_preflight_test.go:39 | direct call | ja |
| TestRuntimeUpRequiresORASBeforeCoreBootstrap | cmd/baha/oras_setup_test.go:74 | GATE | B | baha up without ORAS error = Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 486 / cmd/baha/oras_setup_test.go:80 | direct call | ja |
| TestSecureProfileExportCommandPathAssemblesProductionWiring | cmd/baha/secure_profile_export_command_test.go:25 | GATE | B | baha app secure-profile export through the command tree failed: operator authentication needs interactive setup but… | run 44850031032 / job 136678994688 Z 465 / cmd/baha/secure_profile_export_command_test.go:125 | direct call | ja |
| TestSelectedCoreDeleteDataRequiresFreshIndependentConsent | cmd/baha/control_plane_destroy_test.go:119 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994648 Z 394 / cmd/baha/control_plane_destroy_test.go:120 | domain fixture | ja |
| TestSelectedCoreDeleteFailureRetainsOwnersAndRetriesOnlyRemainingResources | cmd/baha/control_plane_destroy_test.go:131 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994688 Z 470 / cmd/baha/control_plane_destroy_test.go:132 | domain fixture | ja |
| TestSelectedCoreDestroyPreservesDataSiblingAndOwnersAndAllowsRetry | cmd/baha/control_plane_destroy_test.go:95 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 491 / cmd/baha/control_plane_destroy_test.go:96 | domain fixture | ja |
| TestSelectedCoreStopFailureNeverAttemptsVolumeDeletion | cmd/baha/control_plane_destroy_test.go:154 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994688 Z 475 / cmd/baha/control_plane_destroy_test.go:155 | domain fixture | ja |
| TestStaleDestructionConsentRequiresRepreview | cmd/baha/application_lifecycle_lock_test.go:57 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 496 / cmd/baha/application_lifecycle_lock_test.go:79 | direct call | ja |
| TestStandalonePreflightCLIAndMCPRejectMissingWorkloadExposure | cmd/baha/adoption_bug_regression_test.go:100 | ANDERER GRUND | D | missing workload finding: main.applicationPreflightResult{Application:"", Environment:"", Passed:false, Checks:[]pr… | run 44850031032 / job 136678994648 Z 399 / cmd/baha/adoption_bug_regression_test.go:125 | runWithIO | ja |
| TestTUICoreNoTargetLoadsEveryView | cmd/baha/tui_tabs_regression_test.go:81 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 501 / cmd/baha/tui_tabs_regression_test.go:88 | direct call | ja |
| TestTUICoreOverviewInvokesSelectedTargetRuntimeInventory | cmd/baha/tui_tabs_regression_test.go:95 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 506 / cmd/baha/tui_tabs_regression_test.go:101 | direct call | ja |
| TestTargetDefinitionDetachAndRestorePreserveAppliedOwners | cmd/baha/target_definition_change_test.go:152 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 511 / cmd/baha/target_definition_change_test.go:165 | domain fixture | ja |
| TestTargetDefinitionDetachRefusesOwnerlessRecord | cmd/baha/target_definition_orphan_refusal_test.go:575 | GATE | B | detach must refuse via the collectable-orphan guard, got: Managed-environment machine operations require an authent… | run 44850031032 / job 136678994909 Z 474 / cmd/baha/target_definition_orphan_refusal_test.go:611 | direct call | ja |
| TestTargetDefinitionHonoursYesOnNonTTYForConfigOnlyDetach | cmd/baha/target_definition_change_test.go:52 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 516 / cmd/baha/target_definition_change_test.go:56 | domain fixture | ja |
| TestTargetDefinitionRefusesDetachWithoutYesOnNonTTY | cmd/baha/target_definition_change_test.go:82 | GATE | B | no --yes on non-TTY must fail closed: Managed-environment machine operations require an authenticated BaseHarbor op… | run 44850031032 / job 136678994648 Z 404 / cmd/baha/target_definition_change_test.go:88 | domain fixture | ja |
| TestTargetDefinitionRequiresTwoCurrentAcknowledgements | cmd/baha/target_definition_change_test.go:102 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994909 Z 479 / cmd/baha/target_definition_change_test.go:106 | domain fixture | ja |
| TestTargetDefinitionStaleMaterialCannotAuthorizeDetach | cmd/baha/target_definition_change_test.go:125 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994648 Z 409 / cmd/baha/target_definition_change_test.go:129 | domain fixture | ja |
| TestTargetDeleteHealPathReachesRecordWithOwnerRestored | cmd/baha/target_definition_orphan_refusal_test.go:376 | GATE | B | refusal did not name the attached record "11111111-1111-4111-8111-111111111111": Managed-environment machine operat… | run 44850031032 / job 136678994890 Z 521 / cmd/baha/target_definition_orphan_refusal_test.go:474 | direct call | ja |
| TestTargetDeleteProceedsWithoutOrphans | cmd/baha/target_definition_orphan_refusal_test.go:128 | GATE | B | clean Target refused detach: Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 526 / cmd/baha/target_definition_orphan_refusal_test.go:140 | direct call | ja |
| TestTargetDeleteRefusalIsJSONFriendly | cmd/baha/target_definition_orphan_refusal_test.go:149 | GATE | B | refusal is not a typed machine error: &machine.Error{Code:"authentication_failed", Message:"Managed-environment mac… | run 44850031032 / job 136678994909 Z 484 / cmd/baha/target_definition_orphan_refusal_test.go:164 | direct call | ja |
| TestTargetDeleteRefusesWhileCollectableOrphansAttached | cmd/baha/target_definition_orphan_refusal_test.go:83 | GATE | B | orphan detach refusal not surfaced as collectable-orphan error: &machine.Error{Code:"authentication_failed", Messag… | run 44850031032 / job 136678994648 Z 414 / cmd/baha/target_definition_orphan_refusal_test.go:103 | direct call | ja |
| TestTargetInspectionProjectsBuiltInAccessCapabilities | cmd/baha/target_hotfix_test.go:183 | ANDERER GRUND | D | target "edge-a" is not configured | run 44850031032 / job 136678994648 Z 419 / cmd/baha/target_hotfix_test.go:201 | direct call | ja |
| TestTrustStatusAbsentCoreInsideAndOutsideRepository | cmd/baha/trust_status_regression_test.go:14 | GATE (Subtest-Beleg) | B | — (nur Subtest-Beleg) | Parent ohne Fehler-Block; Subtest-Belege existieren, aber der parent-Zähler dieser Akte fuehrt die Subtest-Zeilen nicht einzeln (cohort = first-level). Belegtraeger: Parent ohne eigene Fehlerzeile; 3 Belegzeile(n) im Block, z.B. job 136678994648 Z 427 / cmd/baha/trust_status_regression_test.go:36 | direct .Run | ja |
| TestTrustStatusRetainsOwnedRecordsWithoutCore | cmd/baha/trust_status_regression_test.go:94 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994648 Z 438 / cmd/baha/trust_status_regression_test.go:105 | direct .Run | ja |
| TestTrustUninstallNoOwnershipIsSafeJSON | cmd/baha/trust_uninstall_test.go:57 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 531 / cmd/baha/trust_uninstall_test.go:63 | direct .Run | ja |
| TestTrustUninstallPromptCompleteAffirmativeApproves | cmd/baha/trust_uninstall_test.go:169 | GATE | B | complete affirmative should approve: Managed-environment machine operations require an authenticated BaseHarbor ope… | run 44850031032 / job 136678994688 Z 480 / cmd/baha/trust_uninstall_test.go:189 | direct .Run | ja |
| TestTrustUninstallPromptEOFAbortsCleanly | cmd/baha/trust_uninstall_test.go:202 | GATE | B | EOF surfaced raw read error instead of clean abort: Managed-environment machine operations require an authenticated… | run 44850031032 / job 136678994688 Z 485 / cmd/baha/trust_uninstall_test.go:215 | direct .Run | ja |
| TestTrustUninstallPromptEOFRejects | cmd/baha/trust_uninstall_test.go:144 | GATE | B | EOF surfaced raw read error instead of clean abort: Managed-environment machine operations require an authenticated… | run 44850031032 / job 136678994688 Z 490 / cmd/baha/trust_uninstall_test.go:157 | direct .Run | ja |
| TestTrustUninstallPromptUnterminatedAffirmativeEOFRejects | cmd/baha/trust_uninstall_test.go:119 | GATE | B | EOF surfaced raw read error instead of clean abort: Managed-environment machine operations require an authenticated… | run 44850031032 / job 136678994688 Z 495 / cmd/baha/trust_uninstall_test.go:132 | direct .Run | ja |
| TestTrustUninstallRefusesUnapprovedJSONWithOwnedRecord | cmd/baha/trust_uninstall_test.go:70 | GATE | B | missing approval guidance: Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994909 Z 489 / cmd/baha/trust_uninstall_test.go:84 | direct .Run | ja |
| TestTrustUninstallWizardDeclinePreservesOwnedState | cmd/baha/trust_uninstall_test.go:91 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994648 Z 443 / cmd/baha/trust_uninstall_test.go:104 | direct .Run | ja |
| TestUpNameResumesRegisteredDeploymentAcceptsParity | cmd/baha/runtime_ports_test.go:435 | GATE | B | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994890 Z 536 / cmd/baha/runtime_ports_test.go:440 | direct call | ja |
| TestUpNameResumesThroughCommandEntrypoint | cmd/baha/runtime_ports_test.go:316 | GATE | A | Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994688 Z 500 / cmd/baha/runtime_ports_test.go:334 | runWithIO | ja |
| TestWorkspaceMapBootstrapDoesNotGuessMultiComponentMapping | cmd/baha/app_workspace_bootstrap_test.go:94 | GATE | A | expected multi-component bootstrap error, got Managed-environment machine operations require an authenticated BaseH… | run 44850031032 / job 136678994648 Z 448 / cmd/baha/app_workspace_bootstrap_test.go:112 | runWithIO | ja |
| TestWorkspaceMapBootstrapRequiresStableGitOrigin | cmd/baha/app_workspace_bootstrap_test.go:69 | GATE | A | expected stable-origin error, got Managed-environment machine operations require an authenticated BaseHarbor operat… | run 44850031032 / job 136678994688 Z 505 / cmd/baha/app_workspace_bootstrap_test.go:87 | runWithIO | ja |
| TestWorkspaceMapBootstrapsFirstRepositorySource | cmd/baha/app_workspace_bootstrap_test.go:15 | GATE | A | workspace map bootstrap failed: Managed-environment machine operations require an authenticated BaseHarbor operator… | run 44850031032 / job 136678994648 Z 453 / cmd/baha/app_workspace_bootstrap_test.go:33 | runWithIO | ja |
| TestWorkspaceWizardCancelDoesNotWriteState | cmd/baha/app_workspace_wizard_test.go:108 | GATE | B | wizard failed: Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994909 Z 494 / cmd/baha/app_workspace_wizard_test.go:142 | direct call | ja |
| TestWorkspaceWizardCreatesPortableModelAndLocalMapping | cmd/baha/app_workspace_wizard_test.go:14 | GATE | B | wizard failed: Managed-environment machine operations require an authenticated BaseHarbor operator. | run 44850031032 / job 136678994688 Z 510 / cmd/baha/app_workspace_wizard_test.go:71 | direct call | ja |

## 3) Summenprobe (fünf klassen, wie gemeldet)

```
97 (GATE) + 7 (GATE via Subtest-Beleg) + 9 (ANDERER GRUND) + 1 (ANDERER GRUND via Subtest-Beleg) + 3 (OHNE NACHWEIS) = 117
```

Was der Coordinator als „97 GATE + 11 + 3 + 1 + 5" notierte, ist dieselbe Rechnung in anderer Gruppierung:
die 11 sind die „ohne eigene Eltern-Fehlerzeile"-Fälle (7 GATE-Subtest-Belege + 3 reine Run-Marker + 1
Andere-Ursache-Subtest-Beleg); ihre 5 passen nicht zur ausgezählten Cohorte — die hier stehende Fünferzahl
ist die nach Zeilen ausgezählte Wahrheit der Tabelle. Die Abzugsspalte (ast-basiert, b7dce1ee-Regeln):
A 14 / B 76 / C 14 / D 10 / D? 3 = 117; Heilungsstempel 115 ja / 2 nein.

Erkennungszeile je Klasse (was den Fall in der Tabelle ausmacht):

- GATE (97 Fälle): die wörtliche meldung ist genau „Managed-environment machine operations require an
  authenticated BaseHarbor operator." (Gate: `internal/operatorauth/authorization.go:285`, Flip-Commit
  `3653369a` aus #1717) oder eine der Operator-Auth-Varianten („Operator authentication is not configured",
  „operator authentication needs interactive setup", OIDC/authentication_failed-Meldungen). ast-typ egal.
- GATE via Subtest-Beleg (7 Fälle): Parent hat keine eigene Fehlerzeile im Log, aber mindestens ein
  Subtest-Trägerpaar `--- FAIL: Parent/Sub` + Meldung mit dem Gate-Text. Nachweistraeger nennt beide
  Zeilen (Parent-Block + Subtest-Zeile).
- ANDERER GRUND (9 Fälle): eine gehostete Fehlerzeile existiert, ihr Text ist NICHT das Gate. Namentlich
  und mit Message in der Tabelle: `TestAppListAllTargetsWorksAfterInstallationDestroy` (gelöschte
  Target-config — der 0428-210-Produktfehler), `TestTargetInspectionProjectsBuiltInAccessCapabilities`
  („target \"edge-a\" is not configured"), `TestClientConsentFailsClosedWithoutTerminal`,
  `TestFullDestroyJSONReportsPreservedCAOnFailure`, `TestOrganizationCLIJSONAndMCPShareEffectiveResolution`,
  `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation`, `TestBug865ForeignOrganizationAndSessionAreIsolated`,
  `TestPersesLifecycleMCPSharedSeamRunsApplyLifecycle`, `TestStandalonePreflightCLIAndMCPRejectMissingWorkloadExposure`.
- ANDERER GRUND via Subtest-Beleg (GENAU 1 Fall — Singleton): `TestContextualCLIErrorHintsAndContracts`,
  Parent-Block ohne eigene Meldung, ein Subtest-Träger mit Nicht-Gate-Text. Bitte beim nächsten Neuschitt
  nicht verlieren: einzelne Klassen verschwinden in Aggregaten.
- OHNE NACHWEIS (GENAU 3 Fälle — kleine Klasse, namentlich): `TestDoctorNotDeployedVersusIncomplete`
  (job 136678994909 Z 379), `TestGuidedRepositoryRuntimeFixtureRegressionSuite` (job 136678994688 Z 360),
  `TestMCPReadEntryExpectedPreconditions` (job 136678994648 Z 364). Grund je Fall: im Artefakt existiert
  nur der `=== RUN`-Marker — kein `--- FAIL`-Block, kein Subtest-FAIL, keine Fehlerzeile im Log, obwohl der
  Name in der Cohorte der Zelle als First-Level-Fail gemeldet wird (die Summen der Job-Statistiken zählen
  ihn; der Block selbst fehlt im Log-Artefakt). Das ist die Skip-/Log-Lücke: weder lokal nachprüfbar noch
  anderweitig gehostet belegt. Eigenbefund-Hinweis an den Coordinator: möglicher Kandidat für eine eigene
  Karte „log-capture-lücke bei X-parallel-fails", zuerst hier gefunden.

## 4) Klassifikations-algorithmus (≤ 10 Zeilen, wiederholbar)

- 1. Cohorte = alle `--- FAIL:`-Namen erster Ebene (vor dem ersten `/`) aus den vier Job-Log-Artefakten
  von run 44850031032, Zellen cli-0..3; Subtests aggregieren auf den Parent, nie doppelt.
- 2. Log-Sachverhalt: erste Fehlerzeile `datei.go:zeile: nachricht` im Parent-Block → enthält sie den
  Gate-Text → `GATE`, sonst → `ANDERER GRUND`.
- 3. Kein Eintrag im Parent-Block, aber Subtest-FAIL(s) mit Träger → Klasse aus Subtest-Meldung mit
  Suffix `(Subtest-Beleg)`.
- 4. Nur `=== RUN`-Marker, sonst nichts → `OHNE NACHWEIS` (nie aus Verlautbarung oder lokal geschaetzt).
- 5. Abzugsspalte: ast-typ der Test-Definition am develop-Anker — `runWithIO` → A,
  `shared-session MCP` → C, sonst GATE-fallend → B, Nicht-GATE → D, ohne Nachweis → D?.
- 6. Heilung: transitive Stempel-Kette gegen #1615-head-Blobs (testOperatorContext / runWithIOAsTestOperator
  / operatorAuthFixtureContext in erreichbarer Callpath) → ja/nein.

## 5) 89 vs 117 — warum „89" von der Karte muss (drei beweise)

- 1. `w217-classified.tsv` wurde nie publiziert: `git -C baseharbor-plan ls-tree -r --name-only origin/main
  | grep other-domain-test-split` zeigt ausschließlich .md-Akten (round-1.md, codex-review*.md) — keine TSV,
  kein Artefakt mit 89 Zeilen.
- 2. Die Sandbox-Pfade, die die 89 getragen hätten, existieren nicht mehr und nie auf einem Remote:
  `ls /tmp/w217-* /tmp/w206-rerun.json` → „No such file or directory" (dieser Session gemessen).
- 3. Es gibt keine Develop-Push-Go-unit-Zellen, die 89 ausgezählt haben könnten: die Develop-push-Läufe
  44769994971 und 44769994909 tragen ausschließlich `Runtime · Docker Core` / `Runtime · Podman Core`-Zellen;
  die cli-0..3-Matrix läuft nur in PR-Läufen.
- Fazit (Coordinator-ruling übernommen): 89 war eine nicht überprüfbare Sandbox-Zahl und ist als Wort in der
  Karte durch die 117 aus dem neutralen pfad ersetzt. Der Fehler steht in der Karten-Formulierung, nicht in
  einer Lane-Rechnung.

## 6) Zwei Methoden, zwei Cohorten — und welche frage sie beantworten

Die Deckungskarte b7dce1ee/w234 zählt 206 FAIL-Zeilen am develop-Stand und teilt sie statisch
(A=80/B=81/C=10/D=10). Diese Akte zählt 117 First-Level-Namen des gehosteten cli-Shard-Logs und prüft sie
gegen den #1615-head (transitive Stempel-Kette). Beide sagen: der Operator-auth-Gate heilt durch #1615.
Keine von beiden sagt, dass 0428-213/214/210 damit erledigt sind:

- 0428-213: Beweisklasse ANDERER NATUR — Testassertionen, die nur `err != nil` prüfen; kein Gate-Fall,
  heilt durch nichts, was #1615 tut.
- 0428-214: konstruktionsbedingt unerreichbarer ast — der Test stempelt seine eigene Autorität
  (`internal/operatorauth/context.go:54-57`) und beweist damit „AUTHORIZED", was die Produktion nie prüft.
- 0428-210: ein PRODUKTIONS-fehler in `app_commands.go` — das All-targets-Inventar hängt an gelöschter
  Target-config (genau die Meldung von `TestAppListAllTargetsWorksAfterInstallationDestroy` oben).

115/117 („geheilt"-spalte) ist DIESER Lane transitive Zählung, nicht die Karten-Klasse-A-Zählung des
w234-Entwurfs (114/117 bzw. 80). Verwechsle im nächsten Neuschitt nicht „GATE-Fall" mit „Beweis-/Produktions-fall".

## 7) Wo round-1 sich verzählt hat (die vier einwände des Urteils)

- 1. Einwand „38 ≠ 89": beide Zahlen waren Kohorten-Fehler. Die auditierte Cohorte ist 117 (diese Akte,
  §1); 89 und 38 hatten keinen Nachweistäger (§5).
- 2. Einwand „Gruppe 12 = 9": die round-1-Teilliste 3+2+2+2 zählte einen Test doppelt (er erschien in zwei
  Subgruppen). Der konsistente Wert ist 8 Fälle, und die 8 gehören zur Produktion `cmd/baha/core_network_binding.go:56`
  (Meldung „existing native network lacks a protected Core or shared backend owner"), hochgereicht über
  `cmd/baha/app_edit_apply_test.go:1253` („start real isolated Core for App Edit").
- 3. Einwand „keine zeilenweise inventur": behoben — §2.1, 117 Zeilen, jede genau einmal, mit
  nachweistäger-Artefakt-Pfad.
- 4. Einwand „gruppe 8 zuordnen": `cmd/baha/core_network_binding.go:56` (develop 40cb28c758b0 verifiziert),
  nicht eine Testdatei.

## 8) Der credential-fill-Hang (datei:zeile, ohne erfundene ursache)

Der in round-1 beobachtete Hang hat einen konkreten Produkt-pfad: `cmd/baha/app_inspect_remote.go:28`
erreicht `internal/credential/native/host.go:135` → `PreInteractiveNoPromptWithRunner` →
`internal/credential/native/gitcredential.go:49` (`s.runner().Invoke` von `git credential fill`,
argumente aus `helperCommand()`, `gitcredential.go:68`). Der `ExecRunner.Invoke` in `host.go:26` setzt
weder `GIT_TERMINAL_PROMPT=0` noch `GIT_ASKPASS=/bin/true` — genau diese Umgebung war der Hebel des
Reviewer-rerun, der den Hang wegnahm. STATE dazu: in den Log-Artefakten von 44850031032 gibt es keinen
solchen stall; der Befund bleibt eine lokale-beobachtung mit zugeordnetem produkt-pfad, kein CI-versagen.

## 9) Container-start fund (tooling-pfad, coordinator-directive go206/go206b)

Ein bulk `go test ./cmd/baha/` startet auf diesem host lifecycle-container: der Pfad läuft durch
`TestAppEditCommandCompleteProviderEditRunsRealLifecycle` in `cmd/baha/app_edit_apply_test.go`. Deshalb:
KEIN bulk-Lauf auf dem coordinator-host (die ambient `bh-docker-dev-shared-*`-Zerstörung ~03:0xZ ist der
Hintergrund); falls nötig nur benanntes `-run` mit
`-skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` und Vorankündigung
per QUESTION. Diese Lane hat null container gestartet (§10).

## 10) repo-rule compliance

- Read-only Mission: kein Produktcode, kein Commit in baseharbor, keine PR, kein `.github/**`, kein
  rerun/dispatch, keine Subagenten, kein `codeman agent post` an andere Sessions als den Coordinator.
- Kein lokales `go test` (bulk-verbot §9); Remote-Wahrheit nur via ls-remote/API/partieller Clone; das
  quarantäne-checkout workers/baseharbor wurde nicht zitiert.
- Publikation genau ein Pfad: `git add evidence/r28-welle4-2026-11-21/other-domain-test-split/round-2.md`
  (kein `git add -A`; das untracked `evidence/r28-welle4-2026-11-21/all-targets-config-loss/` gehört der
  210-Lane, unangetastet). Der von dieser Lane gestashte `stash@{0}`
  „lane-w206-protect-foreign-edit-appedit207" (fremde 207-Arbeitskopie) wird NICHT gepoppt oder gedroppt.

## 11) Cleanliness

- `docker ps -a` vorher: leer außer dem (von anderer Hand bereits entfernten) ambient-stapel — witness
  `/tmp/opencode/w206r2/docker_ps_before.txt` / `docker_ps_before_full.txt`.
- `docker ps -a` nachher: leer (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`-header nur) —
  witness `/tmp/opencode/w206r2/docker_ps_after.txt`. Diese Lane hat keine container, netzwerke, volumes
  oder state-verzeichnisse gestartet; der shared-stapel wurde nicht wiederhergestellt (owner-entscheidung).
- cleanliness: besenrein — kein eigener compose-project, keine hinterlassenen prozesse, scratch nur
  unter /tmp/opencode/w206r2 und /tmp/opencode/w206-0428-206-split-wt.

## Publishing witness

```
$ git -C baseharbor-plan add evidence/r28-welle4-2026-11-21/other-domain-test-split/round-2.md   (kein git add -A)
$ git -C baseharbor-plan commit  -> 76ad176457c0b48b955dec6e6ec24cfabc1bd58e
$ git -C baseharbor-plan push origin main
$ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main \
    | grep evidence/r28-welle4-2026-11-21/other-domain-test-split/round-2
evidence/r28-welle4-2026-11-21/other-domain-test-split/round-2.md
$ git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main
76ad176457c0b48b955dec6e6ec24cfabc1bd58e  refs/heads/main
```

The witness block itself rides commit 2 on top (origin/main moves accordingly); commit 1 `76ad1764…`
is the inventory body.

## END

END_DONE 0428-206-testsplit-recount: inventur 117/117 zeilenweise publiziert (evidence/r28-welle4-2026-11-21/other-domain-test-split/round-2.md), summenprobe 97+7+9+1+3=117, abzug A14/B76/C14/D10/D?3, heil-stempel 115/117 gegen #1615-head, kein kandidat (diagnosis-karte) — plan sha siehe ls-remote oben; coordinator bucht die karte auf wait.
