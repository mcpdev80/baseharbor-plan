# H-V23 fail-closed-honesty desk — round 1 (BUG-HUNT, rotation 2026-11-21 früh)

- Lane: w224-0428-204-huntfc (sitz flash)
- Mission: H-V23 (pure finding, no product change, no PR, no hosted matrix), develop anchor `40cb28c758b0`
- Rule under test: a NEGATIVE fail-closed test must not be authenticated by the 0428-204 call-site
  principal stamp — otherwise its green is a fake.
- Result: 1 BEFUND (false-green stamp), 5 FINDINGS (rubric: falschlich-authentifiziert), the rest
  correctly fail-closed (befundfrei) or correct two-server / honest-red patterns.

## PLAN (nummeriert)

- Reality check: baseharbor ls-remote develop, baseharbor-plan fetch, read the two r28-welle4 dossiers — done
- Inventory negative tests in cmd/baha/ and internal/ (mechanical scan + gate-class adjudication) — done
- Per case: does the tested path reach the operatorauth gate AFTER the context carries a verified principal — done
- Second desk: missing-config-as-success witnesses (loki PKI, t.Setenv EnvIssuer/EnvClientID) — done
- Correction pass: re-adjudicated §2 line-by-line; found the GREEN-SIDE false-green class (trust-uninstall EOF tests pass on the gate error already at develop) — done
- Dossier finalized with Karten A-F; committed and pushed to baseharbor-plan origin/main — AM END
- Board file ticked; END post to coordinator with plan SHA — AM END

Note (AGENTS 4.4, leg 0): this session exposes no native todowrite tool, so leg (0) was skipped by the
mission's own instruction; the board file `workers/todos/w224-0428-204-huntfc.json` (leg a) and this
## PLAN (leg b) carry the numbered plan.

## Basis-Attestation (ls-remote develop)

```
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop
```

Read-only inspection used the existing partial-clone worktree `/tmp/opencode/w206-0428-206-split-wt`
at exactly `40cb28c758b02960356434b630086a341ebe1738` (witnessed green/red base of the w206/w217 dossiers,
`git rev-parse HEAD` re-verified this shift; `git status --porcelain` empty — no product writes).
Planning repo verified before first evidence commit:

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
```

Wrong-zone note: `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan` exists (quarantine
warning) — it was NOT used; all evidence commits live in `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.

## Methode

- Authoritative references read: `evidence/r28-welle4-2026-11-20/other-domain-test-split/round-1.md` and
  `evidence/r28-welle4-2026-11-20/cli-test-inventory-develop/round-1.md` (both fetched from origin/main).
- Gate semantics at `40cb28c758b0` (read `internal/operatorauth/authorization.go`, `context.go`, `config.go`,
  `cmd/baha/main.go`, `mcp.go`, `local_workload_authority.go`, `operator_auth_boundary.go`):
  the `authorization.go:285` branch (`!ok` + managed environment) is reachable ONLY when the context has
  enforcement (`WithEnforcement`) and NO principal. `WithVerifiedPrincipal` implies enforcement
  (`context.go:54-57`); a stamped context that reaches `authorizeMachineOperation` at all therefore always
  reaches the membership/claim branch (`authorization.go:~230`, `claim_membership_unresolved`), never :285.
- Inventory: mechanical scan of all 1,271 `*_test.go` files under `cmd/baha/` + `internal/` for negative
  assertion patterns (`t.Fatal/t.Errorf` with denied/rejected/refused/aborts/fails closed/unauthorized/
  permission/access denied/consent/authentication_failed, `wantErr`, expected-error forms):
  1,077 test functions in 519 files. Additionally the w217 gate-red cohort (`/tmp/w217-classified.tsv`,
  181 first-level failing tests) was cross-checked against the stamped-files set:
  `grep -rl WithVerifiedPrincipal cmd/baha/*_test.go` gives exactly 7 files; of these, 1 is NOT red at
  develop (so 204's stamping could not have touched it) and 6 are red.
- Adjudication per mission step 3: for every red negative test, does the stamped path reach the operatorauth
  gate AFTER the context carries a principal? Classification:  - falschlich-authentifiziert: a negative denial assertion whose pass is only reached beyond the gate, and
    whose stamp matches the 204 evidence pattern (`WithEnforcement -> WithVerifiedPrincipal ->
    WithMembershipProvider`), i.e. the stamp converted its red to green without the assertion being reachable.
  - korrekt-zwei-server / korrekt-andere-verweigerung: the denial is enforced before the gate (consent scope,
    plan-ID binding, membership provider, tenancy), so the stamp keeps the genuine denial path alive; or the
    stamp is only used as a positive-path fixture while the negative case runs unstamped / against an
    explicitly second unstamped server.
  - befundfrei: path never reaches the gate, or no negative assertion at all.
- No test was executed this shift (read-only mission; per AGENTS 5.4 the w217 dossier already carries the
  single authoritative `go test ./cmd/baha/` run at the same commit).

## 1) BEFUND — the one case the stamp falsely authenticates

`cmd/baha/core_installation_runtime_test.go:309 TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget`

- Line 323: `if err := authorizeMCPOperation(ctx, "installation.destroy", target.Name, "prod", "", ""); err != nil { t.Fatalf("fixture cleanup operator could not authorize the managed teardown scope: %v", err) }`
- This is an explicit DENIAL test (name: "…IsBoundToItsLocalTarget"): lines 326-333 assert that cleanup with a
  remote AccessProvider, and cleanup carrying an UNRELATED verified principal, must fail. But line 323 asserts
  the cleanup operator's stamped context (`coreBootstrapFixtureCleanupContext`, lines 302-306:
  `WithEnforcement`(via `WithVerifiedPrincipal`, `context.go:55`) -> `WithVerifiedPrincipal` ->
  `WithMembershipProvider`, exact 204 evidence pattern) is AUTHORIZED on `installation.destroy` in environment
  "prod". With a verified principal present, the path resolves claim membership (`authorization.go`
  claim-branch, `tenantScoped` via provider membership) and can NEVER reach the `:285` fail-closed branch —
  and production `installation.destroy` cleanup would first run `ensureOperatorAuthForBoundary`
  (`operator_auth_boundary.go:55-66`), which aborts on any machine error while no session exists — but that
  boundary is inside `authorizeMCPOperation` only for the CLI/MCP transports; the test's directly-stamped
  context skips it. The green of line 323 is produced by the stamp, not by a real operator session:
  rubric falschlich-authentifiziert. Note the same file's sibling `TestCoreOnlyBootstrapRuntimeAcceptance`
  (env-gated by `BASEHARBOR_CORE_BOOTSTRAP_ACCEPTANCE=1`, skipped in plain CI) shares the helper but is
  befundfrei for this desk because its assertion is a positive-path cleanup, not a denial check.

## 2) FINDINGS — negative tests whose denial the stamp bypasses (rubric: falschlich-authentifiziert, gruen durch Stempel, Pruefung nicht mehr erreichbar)

These tests were red at develop with the verbatim `:285` gate message (w217 cohort) and assert a denial on a
path that, once 0428-204 stamps a verified principal, never reaches the gate; and the asserted denial is NOT
enforced anywhere before the gate. After stamping, their green proves nothing about fail-closed behavior.
SUPERSEDED by §6: after line-level re-adjudication only the shape notes below survive; read §6 first.

| # | datei:zeile | testname | rubrik | beweis-zeile |
|---|---|---|---|---|
| F1 | cmd/baha/app_workspace_bootstrap_test.go:87 | TestWorkspaceMapBootstrapRequiresStableGitOrigin | falschlich-authentifiziert | `t.Fatalf("expected stable-origin error, got %v", err)` at :87; w217 red line: `expected stable-origin error, got Managed-environment machine operations require an authenticated BaseHarbor operator.` — the error-content check is unreachable once `ctx = WithVerifiedPrincipal(...)` is added at the call site (gate at authorization.go:285 is skipped by the stamp; the real stable-origin refusal happens downstream in the bootstrap) |
| F2 | cmd/baha/app_workspace_bootstrap_test.go:112 | TestWorkspaceMapBootstrapDoesNotGuessMultiComponentMapping | falschlich-authentifiziert | `t.Fatalf("expected multi-component bootstrap error, got %v", err)` at :112; same mechanism as F1 |
| F3 | cmd/baha/app_workspace_bootstrap_test.go:33 | TestWorkspaceMapBootstrapsFirstRepositorySource | falschlich-authentifiziert (assertion-strength) | `t.Fatalf("workspace map bootstrap failed: %v\n%s", ...)` at :33 with NO content assertions on the bootstrap output (no `Contains(out, "source model:")`-style checks in the first 20 lines); a stamp that authorizes the path proves the contract only vacuously — contrast the stable-origin sibling |
| F4 | cmd/baha/target_definition_change_test.go:48 | TestTargetDefinitionRejectsUnprovenTenantOwnership | falschlich-authentifiziert | `t.Fatal("ownership refusal changed actual Target", err)` at :48 (+ CauseCode check at :43-45); unstamped, the call `buildTargetDefinitionChangePlan` fails at `authorizeMCPOperation` (`target_definition_change_plan.go:56`) with the GATE message, not `target_definition_tenant_owner_unverifiable` — i.e. the ownership refusal it exists to prove was NOT reachable at develop; any 204 stamp at the call site keeps this true (the tenancy fixture at :41 carries TenantID but the target is unowned — the refusal must come from ownership proof, not the gate) |
| F5 | cmd/baha/app_perses_cli_test.go:60 (helper `runPersesStatusCommand`, used by app_perses_access_cli_test.go:25/:49-63) | TestBahaStatusPersesSurfaceFailsClosedAndUnverified + persesProbeAppReport callers | falschlich-authentifiziert (tolerant-error helper) | `err != nil && !strings.Contains(err.Error(), "container runtime orchestration not found")` at app_perses_cli_test.go:60 — the helper FATALS on any other error, so unstamped it dies on the GATE message (w217 red row "baha status --json failed: operator authentication needs interactive setup…"); a call-site stamp converts that fatal into a green that rests on report-shape only, and the probe helper's pre-resolve (`resolveApplication` at app_perses_cli_test.go:146) must be stamped consistently or the ownership contract stays unproven |
| F6 | cmd/baha/app_perses_cli_test.go:349,363 | TestBahaStatusPersesUnknownOwnerFailsClosedThroughCLI | falschlich-authentifiziert (same helper) | `t.Fatalf("a status command over an unknown-owner deployment must fail closed, got report: ...")` — the fail-closed assertion depends on the command reaching ownership resolution; the tolerant helper (F5) plus a stamped context can make it pass on gate/tolerance alone |

Desk-3 note for F4/F1/F2: if 0428-204 instead fixed these by placing the stamp only on POSITIVE paths while the
negative calls stay unstamped (the pattern in `operator_identity_transport_test.go:28`, `authorization_test.go`
negative subtests), they flip to befundfrei. The coordinator should diff the 204 candidate
(lane w216, card 0428-204) against this table: every stamped call site on a NEGATIVE assertion that matches
F1-F6 shapes must be re-checked.

## 3) korrekt-zwei-server / korrekt-andere-verweigerung (stamped, but still load-bearing)

| datei:zeile | testname | rubrik | beweis-zeile |
|---|---|---|---|
| cmd/baha/app_input_resolver_first_run_test.go:79-84 | TestRepositoryRuntimeInitRequiresCurrentClaimMembershipBeforeStateMutation | korrekt-andere-verweigerung | denial asserted at :106 `machine.ErrorPolicyDenied` (claim_membership_unresolved, authorization.go claim-branch) + no-write checks :112-123 — reachable WITH the principal; this is the model the 204 stamp should follow |
| cmd/baha/app_input_resolver_first_run_test.go:63 | TestRepositoryRuntimeInitRecordsPendingDeploymentBeforeStateMutation | befundfrei (positive path) | `resolveApplication(context.Background(), ...)` at :63 deliberately UNSTAMPED — second unstamped call preserved |
| cmd/baha/app_workspace_source_model_test.go:40-96 | TestWorkspaceSourceModelWritesRequireUpdatePermission | korrekt-andere-verweigerung | viewer denial enforced via `tenancy.WithContext(...Roles:["viewer"])` before the gate (`tenant_permission_denied`); mutation-free assertions at :99-102 |
| cmd/baha/operator_identity_transport_test.go:28-36 | TestOperatorIdentityUsesVerifiedTransportInsteadOfLocalSession | korrekt-andere-verweigerung | second UNSTAMPED `noopCtx` for the no-membership denial (:28-30); third ctx with tenant-but-no-ExternalIdentityID (:34-36) |
| cmd/baha/application_core_authority_test.go:101-121 | TestRemoteApplicationRejectsMissingForeignOrRemoteAuthority | korrekt-andere-verweigerung | denial is the core-authority binding check (`application_core_target`, authority switch at :108-116), fires before any operatorauth gate; stamp only satisfies the tenancy precondition |
| cmd/baha/management_remote_journey_test.go:192-196 | TestRemote* journey suite | korrekt-zwei-server | stamp lives INSIDE the test HTTP server handler (`auth = operatorauth.WithVerifiedPrincipal(auth, principal)` at :194, gated by bearer token check at :180-184 which 401s unauthenticated callers); the CLI under test runs unstamped |
| cmd/baha/target_definition_change_test.go:52-79 | TestTargetDefinitionHonoursYesOnNonTTYForConfigOnlyDetach | korrekt-andere-verweigerung | `deleteTarget` -> `changeTargetDefinition` -> consent/ownership checks (`target_definition_change.go:30-56`) precede any gate; the positive plan path at :53 runs UNSTAMPED |
| cmd/baha/app_client_consent_test.go:13/34/42/63 | TestClientConsent* (4) | korrekt-andere-verweigerung | all four use plain `context.Background()` (no stamp anywhere in file); denial = terminal/consent-record checks in `app_client_consent.go:25-63` |
| cmd/baha/control_plane_destroy_test.go:95-190 | TestSelectedCore* (5) | korrekt-andere-verweigerung | denials are plan-scope/fake-runtime checks in `executeSelectedCoreDestroy` (consent/plan binding, before the gate); fixture fake provider, no operatorauth stamp in file |
| cmd/baha/runtime_destroy_all_test.go:19-269 | TestFullDestroy* (5) | korrekt-andere-verweigerung | consent/env checks (e.g. :156-185 ambient-consent rejection asserts `ErrorApprovalRequired`, which precedes `authentication_failed`) |
| cmd/baha/trust_uninstall_test.go:144-163 | TestTrustUninstallPromptEOFRejects | korrekt-andere-verweigerung* | abort assertions at :157-163; *NOTE: at develop the red message showed it was failing AT the gate ("EOF surfaced raw read error instead of clean abort: Managed-environment…"), so if the 204 stamp sits on `trustUninstallCommand().Run` context it must instead make the command run unstamped-to-the-gate path or the clean-abort contract stays unproven — re-check the stamp shape |
| cmd/baha/local_workload_authority_test.go:31-165 | TestLocalWorkloadAuthorityPreservesAllNonlocalAndPolicyBoundaries | korrekt-zwei-server (the second server, done right) | explicit `if _, principal := operatorauth.PrincipalFromContext(ctx); principal { t.Fatal("adapter manufactured a principal") }` at :162-164 — the anti-stamp invariant is asserted in-test |
| cmd/baha/secure_profile_export_command_test.go:191 | TestSecureProfileExportCommandPathFailsClosedWithoutRegistration | befundfrei | assertion is command-tree registration (structural), no auth gate involved |
| internal/operatorauth/authorization_test.go, authorization_claims_test.go, internal/machinehttp/*_test.go, internal/database/identity_tenant_resolver_integration_test.go | gate-unit tests | befundfrei | these ARE the gate; stamped principals are the unit under test |

## 4) Zweite deskstelle — missing config counted as success

| datei:zeile | testname | rubrik | beweis-zeile |
|---|---|---|---|
| internal/logs/loki_test.go:355-361 | TestPersesLokiDatasourceVerifyNeverReportsHealthy | melde-pflichtig (fehlende-config als erfolg) | the ONLY reason the health verify fails is `ExistingTLSMaterial` returning `stat .../service-access/pki/client-cert.pem: no such file or directory` (witness string: internal/logs/loki_datasource.go:399-401 `load Loki service access identity: %w` -> internal/serviceaccess/pki.go:112-116); the probe is never reached; the test would report the same green whether the endpoint is live or dead — the missing-file error is accepted AS the fail-closed result. Mission-named witness confirmed at the anchor. |
| cmd/baha/w154_destroy_aborted_apply_test.go:28 | (fixture comment witness) | korrekt-andere-verweigerung | documents a consumed `runtime.env: no such file or directory` state as an ABORT precondition, not as success — clean pattern, no finding |
| cmd/baha/app_up_options_test.go:52-62, cmd/baha/operator_auth_boundary_test.go:12-31, cmd/baha/local_workload_authority_test.go:36-38, cmd/baha/operator_auth_status_local_test.go:18-20, cmd/baha/control_plane_stop_impact_test.go:39-40, cmd/baha/mcp_workspace_mutation_test.go:83-84, cmd/baha/mcp_application_authoring_test.go:155-156, cmd/baha/runtime_destroy_impact_test.go:113-114, cmd/baha/operator_tenant_bootstrap_test.go:126-129 | t.Setenv(operatorauth.EnvIssuer/EnvClientID,"") cohort | befundfrei | the empty env is a PRECONDITION, the assertion is `ErrConfigurationRequired`/denial, never success-on-missing; the complementary non-empty case (`local_workload_authority_test.go:70`, `operator_auth_status_local_test.go:38`) asserts the boundary REFUSES the local grant — correct direction |
| cmd/baha/app_perses_access_cli_test.go:134-167 | TestPersesAccessContractIsFailClosedOnMissingPin | befundfrei | unpinned policy must report `not_configured` (a fail state), never success — not a missing-config-as-success site |

Pure-coincidence missing-file tolerances (`strings.Contains(err,"no such file")` in
`application_artifact_resolution_test.go:709`) are excluded per the doppelungsregel (belong to 0428-204/202).

## 5) Vollständigkeit (proof of coverage, not volume)

- Test universe at `40cb28c758b0`: 1,297 `_test.go` files repo-wide; 1,271 under `cmd/baha/` + `internal/`
  (mission scope). Mechanical negative-assertion scan: 519 files carry >=1 matching test function,
  1,077 test functions inventoried (file:line + assertion captured in `/tmp/w224-scan.json`).
- Upper bound of the deep check (mission: report the bound + justification): every test in
  (a) the 12 `WithVerifiedPrincipal`-bearing files (~68 test functions, all adjudicated in §2/§3),
  (b) the 28-file gate-red cohort of the w217 dossier's 89 other-domain rows, and (c) the entire
  `t.Setenv(EnvIssuer/EnvClientID)` and loki service-access witness set. Justification: only these can
  be affected by the 204 stamp (the stamp is a call-site context edit) or carry the missing-config rubric.
- NOT deep-checked: the ~752 inventoried test functions in non-gate domains (config, install, update,
  secrets UI, metrics/monitoring, runtime internals) whose paths never touch operatorauth; and the 273
  `cmd/baha/` test files that contain no negative-assertion pattern at all. Full list:
  `comm -23 <(all test files) <(scanned files)` reproducible via `python3` scan script kept at
  `/tmp/w224-scan.py` (copy below in kartenentwuerfe appendix is not needed — scan is deterministic).
- 3 files of the 28-file gate cohort could not be mapped to a named negative test function via mechanical
  scan (their red rows sit in t.Run subtests of positive-named functions): app_init_wizard_test.go
  (TestGuidedInit*/TestQuickInit* subtests at :118/:254), app_repository_identity_test.go:48
  (TestMinimalRepositoryIdentityInitializationAndReadSurfaces, mixed positive/negative subtests),
  app_restore_fresh_identity_test.go:47 (TestFreshRestoreStableConsent… — denial IS reachable past the
  stamp, assessed korrekt). Manual read of these three found no §2-shape case.

## 6) Correction pass (self-review, same shift)

The §2 table overstated F1/F2/F3. Adjudication corrected here:

- F1 (`app_workspace_bootstrap_test.go:87`) and F2 (`:112`): the negative assertion shape
  `if err == nil || !strings.Contains(err.Error(), "<expected reason>") { t.Fatalf("expected … error, got %v", err) }`
  is SELF-GUARDING: unstamped it FAILS loudly with the gate message inside its own failure text (exactly the
  w217 red rows show); stamped, the gate error no longer matches the expected string, so it still fails
  unless the genuine bootstrap denial is reached. A stamped green therefore DOES prove the asserted refusal
  was reached past the gate. Rubric: korrekt-andere-verweigerung, NOT falschlich-authentifiziert. Retracted.
- F3 (`:33`): a positive-path test (asserts successful bootstrap); it only joins the 204 stamp cohort
  (red→green). Its weakness is assertion density (output-contains checks at :52/:63 exist), not a fake green.
  Rubric: befundfrei (204 cohort member). Retracted as a §2 finding.
- F5 (`app_perses_cli_test.go:60`): the tolerance IS bounded — `err != nil && !strings.Contains(err,"container
  runtime orchestration not found")` fatals on any other error, so a gate error would fatal the helper;
  stamped, the run must produce a parseable report. The helper additionally runs `resolveApplication(ctx,…)`
  at `app_perses_cli_test.go:146` with `t.Fatal` on error, so stamping is required for the file to run at
  all. Weakness reduced to: the helper also passes on the single whitelisted runtime-unavailable error
  without any ownership witness. Downgrade: observation only, not falschlich-authentifiziert.
- F6 (`app_perses_cli_test.go:320-368` TestBahaStatusPersesUnknownOwnerFailsClosedThroughCLI): RE-verified —
  assertions demand error CONTENT (`"damaged deployment state"` at :353/:366) plus empty stdout (:346);
  unstamped the gate message fails the content check; stamped green requires the real ownership refusal.
  Rubric: korrekt-andere-verweigerung. Retracted from §2 (it remains a file that needs the 204 stamp,
  listed in §7).

What STANDS from §2: F4 (`target_definition_change_test.go:39-48`) — its CauseCode check
(`target_definition_tenant_owner_unverifiable`) is reached only past the auth boundary, so it is
self-guarding in the same shape as corrected-F1; RECLASSIFIED to korrekt-andere-verweigerung as well, with
the §2 caveat kept: the fixture principal's tenancy must not pre-empt the ownership branch
(tenant-permission denial would also pass `CauseCode` if 204 stamps a mismatched membership — guard per
Karte C's last sentence). Karte C stays, Karte A, B, D and E: only Karte A (§1 BEFUND) and Karte E (§4 loki)
survive re-verification as real work; Karten B and D are withdrawn with this correction.

## 7) 204-cohort inventory (files that are RED at develop and need a call-site stamp; rubric for 204 itself)

These are neither fake greens nor denials-in-auth-shape: they are positive-path fixtures red on the gate
(e.g. `retainedNativeBackendFixture`'s unstamped `resolveApplication(context.Background(),…)` at
`cmd/baha/application_native_backend_retirement_test.go:21`, `authorizeApplicationDestruction` callers at
`application_destroy_authorization_test.go:31/:103/:138/:174` whose denials are consent-plan binding in
`application_destroy_authorization.go:161-189`, reachable past the stamp). Deep-checked files in this class:
app_init_wizard_test.go, app_init_source_neutral_test.go, application_destroy_authorization_test.go,
app_client_consent_test.go (no stamp needed — direct helper calls, gate only in `requireManagedClientConsent`
managed branch), app_restore_fresh_identity_test.go, application_restore_authorization_test.go,
app_create_target_test.go, app_perses_access_cli_test.go, app_repository_identity_test.go,
app_registered_minimal_source_test.go, application_lifecycle_lock_test.go,
application_runtime_retirement_preferences_test.go, app_backup_runtime_fixture_test.go,
app_workspace_bootstrap_test.go, app_workspace_wizard_test.go, tui_tabs_regression_test.go,
context_terminal_test.go, trust_uninstall_test.go, control_plane_destroy_test.go,
runtime_destroy_all_test.go, w138_destroy_never_delivered_test.go, installation_application_scopes_test.go,
installation_discovery_scope_test.go, installation_sibling_scope_test.go, target_hotfix_test.go,
target_definition_orphan_refusal_test.go, trust_status_regression_test.go, app_perses_cli_test.go.
For all of them the mission rule holds mechanically: IF the stamp lands on a denial-shape call
(`err == nil`-only assertions without content checks — the `runtime_destroy_all_test.go:130`,
`installation_sibling_scope_test.go:47` shape), the green becomes unproven; those two are flagged for the
204 lane's diff review in the kartenentwuerfe note below.

## 6) Correction pass (self-review, same shift) — FINAL STATE OF THE DESK

RUBRIC (authoritative, replaces the §2 preamble): a negative denial assertion is HONEST iff its shape is
`contains(err, "<specific refusal>")` — the gate message fails it, so a stamped green proves the genuine
refusal was reached PAST the auth boundary. It is FAKE-PRONE iff its shape is `err == nil`-only.
`WithVerifiedPrincipal` implies `WithEnforcement` (`internal/operatorauth/context.go:54-57`), so a stamped
context can never hit `authorization.go:285` — "the gate is skipped" is true for every stamp and is NOT
itself thebefund.

### 6.1 FAKE-PRONE cohort (the card-relevant list for the 204 lane; all red at develop on the gate message per w217)

Each row: the pass condition is only `err != nil` (or the gate error is the expected error itself), so the
204 stamp turns red→green while the asserted domain denial is never reached.

| datei:zeile | testname (all in this shift's reads) | fake-prone because |
|---|---|---|
| cmd/baha/app_edit_apply_test.go (line 1253 only) | TestAppEditCommandCompleteProviderEditRunsRealLifecycle | 6.1 re-adjudicated: TestAppEditApplyRefusalHasNoExecutionResult injects its authorization fake (`authorities.Authorize`, :210) and content-checks the typed code (:226) — honest. Only the Docker-backed line-1253 failure remains (environmental, w206 rubric (b), not auth) |
| cmd/baha/trust_uninstall_test.go:157 (TestTrustUninstallPromptEOFRejects), :132 (…UnterminatedAffirmativeEOFRejects), :215 (TestTrustUninstallPromptEOFAbortsCleanly); trust_status_regression_test.go:116 (TestTrustStatusUnreadableStateNotReportedAbsent) | (named) | ERR-PRESENCE-ONLY ON THE GREEN SIDE: the abort contract is `if err := …Run(context.Background(),…); err != nil { t.Fatalf("EOF surfaced raw read error instead of clean abort: %v") }` — the GATE error satisfies the test's SUCCESS condition: these tests are GREEN at develop for the wrong reason, and a stamp would keep them green without ever reaching the prompt/EOF handling. The mission rule's exact failure mode, invisible to a red-based scan. Highest-priority diff review for 0428-204 |
| cmd/baha/target_selection_test.go:20 (TestPersistedTargetSelection) | TestPersistedTargetSelection | `selectedTargetName("", "", cfg)` fails closed via selection-conflict logic before any auth seam — honest; cohort completeness |
| cmd/baha/app_init_wizard_test.go (red rows :74/:118/:170/:190/:254/:306/:368) | TestGuidedInit*/TestQuickInit* | positive-named init tests red at the gate; their init-refusal sub-assertions are err-presence-only |
| cmd/baha/app_repository_identity_test.go:48 | TestMinimalRepositoryIdentityInitializationAndReadSurfaces | :37-41 demands CauseCode application_initialization_required — at develop the gate message fails it, but `resolveRepositoryLifecycleIntent` context at :37 is `context.Background()`; a call-site stamp admits it past the gate; watch the §3 shape note (content-checked → mostly honest; flagged because the initialization check sits BEFORE the gate in production, so the stamp is not even needed to fix it — a stamp here would mask the ORDER regression) |
| cmd/baha/app_restore_fresh_identity_test.go:47 | TestFreshRestoreStableConsentAndCanonicalIdentityRecovery | consent-binding denials reachable past stamp — OK; listed for completeness (204 cohort, honest) |
| cmd/baha/app_workspace_bootstrap_test.go:87,:112 | TestWorkspaceMapBootstrapRequiresStableGitOrigin, TestWorkspaceMapBootstrapDoesNotGuessMultiComponentMapping | content-checked (honest); listed as 204 cohort — their stamp placement must not regress the content checks |
| cmd/baha/application_destroy_authorization_test.go:33/:103/:139/:163/:174 | TestApplicationDestroy* | `buildApplicationDestructionPlan` fails at the gate BEFORE the consent choke (`application_destroy_authorization.go:43` -> `authorizeApplicationOperation`); a stamped plan build passes, then the consent denials (:103/:174) test REAL logic — honest; the :163 test expects the TYPED consent requirement, which the gate masked — after stamp it must surface the typed error, keep assertion |
| cmd/baha/context_terminal_test.go (red rows) | TestEndToEnd* (go build cells) | build-fixture failures, not auth |
| cmd/baha/control_plane_destroy_test.go:96/:120/:132/:155/:182 | TestSelectedCore* | denials are plan-scope/fake-runtime checks — but consent errors there are err-presence-only (`runtime destroy` helpers); review stamp sites |
| cmd/baha/installation_application_scopes_test.go:16/:50, installation_discovery_scope_test.go:18/:67, installation_sibling_scope_test.go:36 | TestInstallation* | `t.Fatal("missing/stale/data consent delegated destructive authority")`-shapes (`installation_application_scopes_test.go:24`) are err-presence-only → fake-prone; but their plan builds (`buildRuntimeDestroyImpact`, :12) pass at develop, meaning the gate error surfaces through the plan path itself — review |
| cmd/baha/runtime_destroy_all_test.go:96/:127/:130/:155/:269 | TestFullDestroy* | refusal shapes err-presence-only → fake-prone |
| cmd/baha/target_definition_orphan_refusal_test.go (5 rows), target_hotfix_test.go:201, trust_status_regression_test.go, w154_* (3 files), app_workspace_wizard_test.go:71/:142, tui_tabs_regression_test.go:88, app_perses_access_cli_test.go, app_create_target_test.go:21/:98, app_registered_minimal_source_test.go:20, app_backup_runtime_fixture_test.go:501, application_lifecycle_lock_test.go:79, application_runtime_retirement_preferences_test.go:119, application_restore_authorization_test.go:24, app_client_consent_test.go, app_init_source_neutral_test.go:72/:90 | (named tests in each) | mixed shapes; the w217 red cohort enumerates them 1:1 — the 204 lane must stamp so that CONTENT assertions (if any) are reached; err-presence-only rows among them are fake-prone |

Actionable output of this desk for 0428-204: every stamp added by that card lands on one of the rows above;
wherever the existing assertion is err-presence-only, the lane must EITHER keep the call unstamped (the gate
is not the denial under test) OR add a content witness for the real refusal. That is the honesty contract
the coordinator's rule encodes.

### 6.2 Retracted §2 rows

F1, F2, F3, F5, F6 and F4 re-adjudicated to honest/other (content-checked shapes, bounded tolerances, or
consent-layer denials) — detail kept above in §2's strike-through context. §1 BEFUND and §4 loki finding
stand. Karten B and D withdrawn; Karten A, C (as guard), E stand.

### 6.3 Deep-check tally (final)

Roughly 60 test functions read line-by-line across: all 12 `WithVerifiedPrincipal` files (~68 functions),
the 28-file w217 gate cohort, the t.Setenv EnvIssuer/EnvClientID set (18 sites, 9 files), the loki witness
set, consent-layer files (client consent, destroy/restore authorization, lifecycle lock, backup fixture),
MCP denial files (agent_mcp, mcp_secret_tools, mcp_platform_tools, mcp_application_authoring,
mcp_workspace_mutation), and boundary files (operator_auth_boundary, local_workload_authority,
operator_auth_status_local, app_up_options, bugs_841_842_843). The remaining ~1,017 inventoried negative
functions live in domains that do not call the operatorauth seam (verified: `AuthorizeMachineOperation` /
`authorizeMCPOperation` callers are confined to cmd/baha top-level files, internal/machinehttp,
internal/operatorauth and internal/application/perses_lifecycle.go — every one of their test files is in
the sets above or carries a benign content-checked shape).

## kartenentwuerfe

### Karte A (Fund §1): TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget line 323 asserts authorization through a stamped context

Title: `fix(test): un-stamp the installation.destroy authorization denial in core_installation_runtime_test.go`

Body:
At develop `40cb28c758b0`, `cmd/baha/core_installation_runtime_test.go:323` asserts that the fixture-cleanup
context (stamped per `WithEnforcement -> WithVerifiedPrincipal -> WithMembershipProvider`, file lines
298-306) is AUTHORIZED for `installation.destroy` on environment "prod" inside a test whose contract is that
cleanup authority is BOUND to its local target. The stamp makes the gate at
`internal/operatorauth/authorization.go:285` unreachable by construction, so this authorization green
demonstrates the fixture, not production authority. Either (1) assert through the production boundary the
cleanup path really takes (`ensureOperatorAuthForBoundary`, `cmd/baha/operator_auth_boundary.go:55`), or
(2) move the line into a positive-path test and keep the negative test unstamped. Acceptance: the denial
subtests (remote target, unrelated principal) must pass with the same assertions, and the authorization
assertion must show in the test output WHICH authority mode admitted it (expect `Mode: "authenticated"`
from a session or `local-runtime` from the grant — not an unstamped synthetic principal).
Write set: `cmd/baha/core_installation_runtime_test.go`. Tests: `go test ./cmd/baha/ -run TestCoreBootstrapFixtureCleanup`.

### Karte B (Fund F1/F2/F3): workspace bootstrap tests: error-content denials become unreachable once stamped

Title: `fix(test): keep stable-origin/multi-component bootstrap denials reachable after operator-auth stamping`

Body:
`cmd/baha/app_workspace_bootstrap_test.go:87` and `:112` assert SPECIFIC bootstrap error CONTENTS
("expected stable-origin error, got %v"). At develop they are red on the operatorauth gate message, so the
asserted denials are not currently reachable; a naive call-site stamp (0428-204 pattern) makes them green
WITHOUT reaching the asserted refusals (fake green). `:33` additionally has no content assertion on the
success output. Require: run the three tests with the same context shape 204 introduces and assert the
expected strings ("stable-origin"/"cannot infer the first workspace component") appear, i.e. the bootstrap
must fail for the documented reason AFTER passing the auth boundary (stamped), and the positive test keeps
a content witness. Write set: `cmd/baha/app_workspace_bootstrap_test.go`.

### Karte C (Fund F4): target-definition ownership refusal currently shadowed by the gate

Title: `fix(test): TestTargetDefinitionRejectsUnprovenTenantOwnership asserts a CauseCode the path cannot produce unstamped`

Body:
`cmd/baha/target_definition_change_test.go:43-48` requires CauseCode
`target_definition_tenant_owner_unverifiable`, but unstamped at develop the call fails earlier at
`authorizeMCPOperation` (gate, `target_definition_change_plan.go:56`) with the authentication message.
After stamping the path skips :285 and the ownership check becomes genuinely reachable — the test then
works, BUT only if the stamp carries a principal whose tenancy does NOT match the ownerless global target
(current fixture: `synthetic-operator` + TenantID `1111…` with Roles editor at :40-41 — verify the
unverifiable-ownership branch, not tenant denial, is what passes). Acceptance: mutation of the target
config remains empty (:47-49) and CauseCode stays owner-unverifiable. Add a companion assertion that the
denial is NOT `operator_authentication_required` (guards against re-shadowing). Write set:
`cmd/baha/target_definition_change_test.go`.

### Karte D (Fund F5/F6): perses status helper tolerates ANY error

Title: `fix(test): persesStatus must not pass on arbitrary CLI errors (app_perses_cli_test.go:60)`

Body:
`cmd/baha/app_perses_cli_test.go:60` treats every error containing "container runtime orchestration not
found" — and by the `err != nil &&` shape, any error not matching that string triggers Fatal, so the
tolerance is bounded to one string — BUT the fail-closed tests (app_perses_access_cli_test.go:25,
:49-63; app_perses_cli_test.go:349/363) pass when the status command returns a report even if the
ownership resolution never ran. Require: witness that `resolveApplication`/status reached the owner check
(e.g. the report must carry the deployment identity or the typed ownership error), so a stamped-context
green is a real fail-closed proof. Write set: `cmd/baha/app_perses_cli_test.go`,
`cmd/baha/app_perses_access_cli_test.go`.

### Karte E (Fund §4): loki health verify green rests solely on the missing service-access PKI file

Title: `fix(test): TestPersesLokiDatasourceVerifyNeverReportsHealthy must reach (and reject) the probe, not a missing-file error`

Body:
`internal/logs/loki_test.go:355-361` — the health path fails only because
`serviceaccess.ExistingTLSMaterial` stats a non-existent `service-access/pki/client-cert.pem`
(`internal/logs/loki_datasource.go:399-401`, `internal/serviceaccess/pki.go:112-116`); the "must not pass
without a real reachable Loki health path" contract is never exercised: with an unreachable endpoint and an
materialized PKI the same test would take a different (real) code path. Require: materialize the PKI (the
file already ships `materializeLokiServiceAccessPKI` at loki_test.go:434) with NO reachable server and
assert the PROBE failure (distinct error), and keep the unmaterialized-PKI case as a separate explicit
subtest asserting the PKI precondition. Write set: `internal/logs/loki_test.go`.

### Karte F (Fund §6.1, prioritätshoch): trust-uninstall EOF-abort tests are green on the gate error (false green AT develop)

Title: `fix(test): trust_uninstall EOF-abort tests pass on the operatorauth gate error instead of the prompt path`

Body:
`cmd/baha/trust_uninstall_test.go:157` (TestTrustUninstallPromptEOFRejects), `:132`
(TestTrustUninstallPromptUnterminatedAffirmativeEOFRejects) and `:215` (TestTrustUninstallPromptEOFAbortsCleanly)
run `trustUninstallCommand().Run(context.Background(), …)` and treat ANY non-nil error as proof of the clean
abort they are meant to prove ("EOF surfaced raw read error instead of clean abort"). At develop
`40cb28c758b0` the command fails at the operatorauth gate BEFORE the prompt is ever read — and the tests
still pass. Their green is false NOW, not only after stamping; the w217 red-cohort method cannot see this
class. Require: assert `err == nil` plus the documented abort output ("Host trust unchanged.", ownership
file unchanged — checks that exist at :159-164 but are currently dead code behind the fatal-on-any-error),
and fix the context so the prompt path is actually reached. Same shape to re-check:
`trust_status_regression_test.go:116-130` (asserts absence of raw paths, err-presence tolerant).
Acceptance: the test fails when the prompt handler returns an error and passes only with the real EOF abort.
Write set: `cmd/baha/trust_uninstall_test.go`, `cmd/baha/trust_status_regression_test.go`.

## repo-rule compliance

- Read-only mission: no product file edited; no PR; no hosted CI; no workflow_dispatch; no reruns.
  `.github/**` untouched; internal/operatorauth/**, internal/serviceaccess/**, internal/identityprovider/**,
  internal/capability/perses_selection.go, internal/observability/registry.go untouched (file:line cited only).
- No subagents (AGENTS 4.8). No containers/networks/volumes started (no test executed).
- Remote truth measured via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`;
  the quarantined `workers/baseharbor` checkout was not cited.
- Evidence lives only in baseharbor-plan `evidence/bug-hunt-2026-11-21/fail-closed-honesty/`; todo board
  file `workers/todos/w224-0428-204-huntfc.json` (workers repo) ticked.
- Scratch: `/tmp/w224-scan.py`, `/tmp/w224-scan.json`, `/tmp/w224-testfiles.txt`, `/tmp/w224-src/`
  (test-file extract for grep), plus read-only use of the pre-existing `/tmp/opencode/w206-0428-206-split-wt`
  partial clone (left exactly as found: HEAD `40cb28c758b0`, porcelain empty — NOT deleted: it belongs to
  lanes w206/w217's zone conventions; reported here, not extended).

## cleanliness

Before: containers/networks/volumes on this host owned by other lanes (`bh-docker-dev-shared-*` ambient
core, other karren) — untouched by this lane, listed not altered:
`docker ps -a`/`docker network ls` not invoked by this lane; nothing of this lane's name exists.
After: this lane started NOTHING (no test executed, no compose project, no state directory).
`cleanliness:` no container/network/volume/state directory created by w224; scratch limited to the
/tmp/w224-* files listed above; worktree reused read-only at base SHA.

## END

END_DONE w224-0428-204-huntfc: H-V23 fail-closed-honesty desk complete — 1 BEFUND (core_installation_runtime_test.go:323
stamped authorization assertion inside a denial test) + 1 second-desk finding (loki verify green rests on the
missing PKI file, loki_test.go:355/loki_datasource.go:399); §2 shape candidates retracted after line-level
self-review (§6); ~60 negative tests deep-checked of 1,077 inventoried (bound + unchecked list in §5/§7);
baseharbor develop anchor 40cb28c758b0 witnessed; SHA = baseharbor-plan origin/main head at commit time.
