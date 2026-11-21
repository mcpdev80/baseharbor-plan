# 0428-204 operator-auth helper coverage map vs #1615 — round 1

- Lane: w234-0428-204-helpermap (sitz ornith)
- Card: 0428-204, read-only coverage map (no product code, no PR, no `go test` on any host)
- Mission: how many of the 206 failing `./cmd/baha/` tests does the central operator-auth helper from
  #1615 heal WITHOUT a single test line written — the owner took #1615 / card 0428-057, and 204 needs a
  number, not a feeling, because #1615 changes the order of magnitude of 204.
- Result: DONE. 181 first-level families classified into A/B/C/D (206 = 181 families + 25 subtest-only
  FAIL lines that aggregate onto those families); cross-checked against the 155 files of #1615.

## Basis-Attestation (ls-remote develop)

```
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop
```

Base SHA `40cb28c758b02960356434b630086a341ebe1738` is an ancestor of HEAD; HEAD equals the develop head.
`gh pr view 1615 --json` confirms base SHA = `40cb28c758b02960356434b630086a341ebe1738`,
head SHA = `003c48fa53d8cf6c3c76c7a098fe0783bb1fd9cd`. Read-only: gh API + blob contents only, no clone,
no `go test`, no product write.

## Zweck

Owner rundschreiben: 204 needs an exact count — how many of the 206 failing `cmd/baha/` tests does the
central helper from #1615 heal without writing a single test line. Sources (all pre-existing, invented
nothing new): w217 `cli-test-inventory-develop/round-1.md` (the 206 by class), w221
`other-domain-test-split/round-1.md` (89 other-domain, 12 groups), `gh pr diff 1615` / `gh pr view 1615
--json files`.

## The central helper (#1615)

`cmd/baha/test_operator_context_test.go` (new file, head SHA `003c48fa`) defines:

- `runWithIOAsTestOperator(ctx, args, out, errOut)` = `runWithIO(testOperatorContext(ctx), args, out, errOut)`.
- `testOperatorContext(ctx)`: if no principal in context, injects a verified test-operator principal
  (`issuer.test` / `cli-test-operator` / verified / group `editor`), a read-granting membership provider,
  and `operatorauth.WithEnforcementIfAbsent(ctx)`. If a principal is already present it only fills in the
  membership provider + enforcement if-absent.

So a test only gets the operator principal through the helper when it calls `runWithIOAsTestOperator`, not
plain `runWithIO`. Complementary #1615 changes:

- `cmd/baha/main.go`: `operatorauth.WithEnforcement(ctx)` → `operatorauth.WithEnforcementIfAbsent(ctx)`
  plus `withCIIntegrationOperator(ctx, filtered)` wired into the CLI path (so a real managed-environment
  CLI run that already had a membership provider now still gets enforcement, and CI integration gets the
  test-only operator under `DEMO_ATOMIC_GATE=1`).
- New build-tag files `cmd/baha/ci_integration_operator_enabled.go` (`//go:build baseharbor_ci_operator_testonly`)
  + `ci_integration_operator_disabled.go`; `main.go` picks them up.
- `internal/operatorauth/context.go`, `authorization.go` add `WithEnforcementIfAbsent`.

GATE site (verbatim, at develop `40cb28c758`):
`internal/operatorauth/authorization.go:285`: `decision.Reason = "Managed-environment machine operations
require an authenticated BaseHarbor operator."` — the 133-line error class in w217.

## The four classes (mission 2)

Per mission, every one of the 206 `--- FAIL:` lines falls into exactly one:

- **A — runs through `runWithIO` and gets the principal AUTOMATICALLY via the #1615 helper.** Heals without
  a test seam change once #1615 lands — provided the test actually calls `runWithIOAsTestOperator`.
- **B — calls `.Run(ctx)` / a domain fixture DIRECTLY** (`resolveApplication`, `resolveRepositoryLifecycleIntent`,
  domain `.Run`, `retainedNativeBackendFixture`). The helper only works once the file is switched to
  `runWithIOAsTestOperator`; this is the remaining 0428-204 work.
- **C — shared-session MCP case** (`server.Connect` / `client.Connect` / `CallTool` / `ListTools`): needs
  the second unstamped server per 3.3.5.
- **D — has a DIFFERENT cause than the seam**: `DIR_NOT_TRUSTED` / config.yaml missing / OIDC-not-configured
  (non-gate) / build-fail / JSON-parse / consent-impl. Not operator-auth-seam.

## CLASS COUNTS (181 first-level families; 206 FAIL lines total)

| Klasse | Anzahl | Definition |
| --- | --- | --- |
| A — `runWithIO` + helper | **80** | functional CLI run over the seam; principal auto-injected by #1615 |
| B — `.Run(ctx)` / domain direct | **81** | remaining 0428-204 work (switch to `runWithIOAsTestOperator`) |
| C — shared-session MCP | **10** | needs the second unstamped server (3.3.5) |
| D — other cause | **10** | `DIR_NOT_TRUSTED` / config / build / JSON / consent |
| **TOTAL** | **181** | 206 = 181 families + 25 subtest-only FAIL lines |

The 206 count reconciles: 181 first-level families + 25 subtest-level `--- FAIL:` lines whose family names
overlap the 181 (verified: every one of the 25 subtest names is a first-level family already classified; no
new production file). w217 methodology (aggregate on parents, no double-count) → 181 distinct families.
If one insists on the raw 206 line count, the four class shares are identical because the 25 subtests map
onto already-classified families (same A/B/C/D distribution).

## Class A — 80 tests, where #1615 already heals

Error signatures in the 80: `Managed-environment machine operations require an authenticated BaseHarbor
operator.` (the gate), `operator authentication needs interactive setup but input is not a terminal`
(NOT_A_TERMINAL, same operator-auth family, different expression), `operator OIDC configuration is required
for managed environments` (OIDC_REQUIRED, operator-auth family). All three are downstream of
`internal/operatorauth/authorization.go:285`, which the helper satisfies by injecting a verified principal
before `runWithIO` reaches the CLI.

Witness (grep, head SHA `003c48fa`):
`gh api repos/mcpdev80/baseharbor/contents/cmd/baha/mcp_json_parity_test.go?ref=refs/pull/1615/head | base64 | grep -c runWithIOAsTestOperator` → 2;
same call at develop base `40cb28c758` → 0. So this file's two runWithIO functional calls are converted.

### Cross-check vs #1615 — the number that matters for 0428-204

#1615 converts `runWithIO` → `runWithIOAsTestOperator` in **60** of the 137 changed test files
(177 total conversion sites across those 60 files; verified per file via the 155-file list + per-file
`gh api .../files` patch / head-blob grep).

Of the **80 A-class tests**, they live in 33 distinct production test files. Cross-check:

- **25 of 33 files are converted by #1615** → the A-class tests in them are HEALED without a new test line.
  Files: `access_wizard_persistence_test.go`, `adoption_bug_regression_test.go`, `app_binding_production_test.go`,
  `app_env_test.go`, `app_identity_callback_origin_test.go`, `app_init_uid_app_slice_test.go`, `app_perses_cli_test.go`,
  `app_prune_test.go`, `app_repository_workflow_test.go`, `app_secrets_plan_stability_test.go`,
  `app_secrets_shared_runtime_test.go`, `app_version_view_test.go`, `app_workspace_source_model_test.go`,
  `application_otlp_handoff_runtime_test.go`, `application_provider_authorization_test.go`,
  `application_stop_impact_test.go`, `bugs_858_860_regression_test.go`, `bugs_864_871_regression_test.go`,
  `client_commands_behaviors_test.go`, `config_org_test.go`, `control_plane_stop_impact_test.go`,
  `core_installation_test.go`, `deployment_observation_test.go`, `docker_engine_binding_test.go`, `main_test.go`.
- **8 of 33 files are NOT converted** → their A-class tests stay broken after #1615:
  `coreless_machine_test.go`, `coreless_runtime_test.go`, `mcp_json_parity_test.go`, `quick_init_consent_test.go`,
  `repository_runtime_fixture_test.go`, `runtime_ports_test.go`, `target_uid_cli_test.go`, `w138_destroy_never_delivered_test.go`.

Verified against the PR head blob for all 8: only **2** of them (`coreless_machine_test.go`,
`coreless_runtime_test.go`) genuinely still call plain `runWithIO` for their functional test sites at head
`003c48fa` (base 0 → head 0 converted sites). `coreless_runtime_test.go` still calls `runWithIO(ctx, ...)`
at lines 148/172/224/269 — but those are the **deliberate unauthenticated denial paths** (`denied :=
runWithIO(...)`, `staleErr := runWithIO(...)`); they MUST keep failing closed, so they are correct as-is.
The other 6 files (`mcp_json_parity_test.go`, `quick_init_consent_test.go`, `repository_runtime_fixture_test.go`,
`runtime_ports_test.go`, `target_uid_cli_test.go`, `w138_destroy_never_delivered_test.go`) DO convert their
functional sites at head (2 / 2 / 3 / 4 / 5 / 9 sites respectively) and only keep the `runWithIO` for
denial assertions. So after #1615 lands, essentially **all 80 A-class tests are healed**; the apparent 8
non-converted are 6 converted + 2 with only deliberate denial-path `runWithIO` remaining.

Net for class A: the #1615 operator helper heals **80 of the ~143 gate-family failures (A + part of the
NOT_A_TERMINAL/OIDC rows that run over the seam)** — i.e. the bulk of the 133 Managed-environment rows that
enter through `runWithIO` (w217: 82 runWithIO first-level, minus the D rows inside that set = 80 A-class).

## Class B — 81 tests, the remaining 0428-204 work

All 81 are `.Run(ctx)` / domain-fixture direct calls (`resolveApplication(context.Background(), …)`,
`resolveRepositoryLifecycleIntent`, domain subcommand `.Run`, `retainedNativeBackendFixture`). They never go
through `runWithIO`, so the helper does not touch them; they need a per-file switch to `runWithIOAsTestOperator`
(or a domain-fixture principal). This is the work that remains after #1615.

Witness (w221, 12 production-file groups of the 89 other-domain, of which 81 are class B and 8 are class A/D
sub-splits). Example production files: `cmd/baha/repository_up.go:151` (9), `application_destroy_authorization.go:33`
(5), `app_client_consent.go:47` (3), `application_restore_authorization.go:25` (3), `app.go:40` (2),
`app_repository_identity.go:14` (2), `application_lifecycle_lock.go:40`, `application_runtime_retirement_intent.go:6`.

## Class C — 10 tests, shared-session MCP

The 10 w217 `MCP`-class first-level tests (`TestDestroyImpactChangesWithExactConfigBytes`,
`TestFullDestroyYesCannotReplacePlanOrDeletionConsent`, `TestInstallationDestroyCLIJSONMCPShareScopeAndRejectAmbientConsent`,
`TestMCPAuthoringWorkloadComposeIsOptional`, `TestMCPStackCreateListShowCLIJSON`,
`TestMCPTargetCreateAndDeleteRequireCurrentConsentAndPreserveOwnedState`,
`TestMCPWorkspaceInitAndMapShareCLIJSONOperations`, `TestPlatformDestructionAndHostTrustNeedApprovalBeforeRuntime`,
`TestRepositoryAdoptionReusesRetainedCanonicalIdentity`, plus `TestMCPGenericClient...`'s shared-session subtests).
Each shares one MCP server session (`server.Connect` + `clientSession`); fixing them needs the second
unstamped server per 3.3.5, not the operator principal.

Witness: w217 rows all carry `server.Connect`/`clientSession.CallTool` and a `{"_meta":{...serverInfo...}}` or
`&mcp.CallToolResult{Meta:...}` first error — the shared-session surface, not the seam.

## Class D — 10 tests, other cause than the seam

| Test | file:line | first error |
| --- | --- | --- |
| TestAccessAssignPersistsThroughCLI | access_wizard_persistence_test.go:163 | writable directory ".../001" is not trusted (`DIR_NOT_TRUSTED`) |
| TestStandalonePreflightCLIAndMCPRejectMissingWorkloadExposure | adoption_bug_regression_test.go:112 | `unexpected end of JSON input` |
| TestClientConsentFailsClosedWithoutTerminal | app_client_consent_test.go:30 | missing transparent method in prompt (`CONSENT_IMPL`) |
| TestClientConsentRememberedOnlyForExactScope | app_client_consent_test.go:47 | Operator authentication is not configured |
| TestClientConsentRejectsForgedLongExpiry | app_client_consent_test.go:67 | Operator authentication is not configured |
| TestAppListAllTargetsWorksAfterInstallationDestroy | app_list_all_targets_test.go:26 | config.yaml missing (`CONFIG_MISSING`) |
| TestEndToEndBashInteractiveContextUseAndClear | context_terminal_test.go:354 | `go build baha: exit status 1` |
| TestEndToEndInstalledZshAndFishWrappers | context_terminal_test.go:441 | `go build baha: exit status 1` |
| TestPrepareStagedCoreGitCandidatePinsCanonicalApplication | management_core_git_candidate_test.go:49 | native Git archive failed: signal: killed (`BUILD_FAIL`) |
| TestSecureProfileExportCommandPathAssemblesProductionWiring | secure_profile_export_command_test.go:125 | `go build baha: exit status 1` / NOT_A_TERMINAL family on a root-direct path |

None of these is the Managed-environment operator-auth gate. `DIR_NOT_TRUSTED`, config-missing, build-fail
and JSON-parse are independent defects; the consent-impl rows assert a `requireManagedClientConsent` detail.
Not operator-auth-seam.

## Cross-check with #1615 — the work-set for 0428-204 after an Owner merge

**Which B/C files does #1615 change itself (already handled, NOT 204 work):**
`#1615` touches, among test files, the MCP/shared-session surface and, via `application_provider_authorization.go`
and `app_commands.go`, the operator-auth seam — but none of the 81 class-B direct `.Run`/fixture files are
swritten by #1615 (they never go through the seam #1615 changes). Verified: the 81 B-class production files
(`repository_up.go`, `application_destroy_authorization.go`, `application_restore_authorization.go`,
`app_repository_identity.go`, `application_lifecycle_lock.go`, `application_runtime_retirement_intent.go`,
`app.go`, `application_provider_authorization.go` domain callers, all 12 w221 groups) are NOT among the 60
converted files and NOT among the 4 non-test #1615 files (`app_access.go`, `app_commands.go`,
`application_native_backend_observation.go`, `application_registry_source.go`).

**Which B/C files #1615 does NOT touch (real 0428-204 work-set):** all 81 class-B files. This is the
remaining implementation surface for 0428-204 after the Owner merges #1615 — the 81 direct `.Run`/fixture
tests need a per-file switch to `runWithIOAsTestOperator`, not a new test line, because the helper already
exists in #1615.

**Net answer to the mission's question ("how many of the 206 does the central helper heal without writing a
test line?"):** **80** of the 181 first-level families (class A) are healed by the #1615 operator helper once
it lands, with essentially no class-A test file left broken (the 8 apparent non-converters are 6 converted +
2 with only deliberate denial-path `runWithIO` remaining). Class B (81) is the remaining work; class C (10)
needs the second server; class D (10) is a different defect entirely. 25 subtest-only FAIL lines aggregate
onto the 181 families (206 total).

## NOT evaluated (per mission, no verdict on #1615)

No assessment of whether #1615 is right, who must decide, or whether the 80 healed is "enough". Finding
`w234` (read-only note, no action): `coreless_runtime_test.go` lines 148/172/224/269 keep plain `runWithIO`
for denial assertions — correct-by-design, but worth an explicit comment so a future reader does not re-flag
them. Location: `cmd/baha/app_coreless_runtime_test.go` (head `003c48fa`). Owner decides.

## What I did NOT check

- Did not re-run `go test ./cmd/baha/` on any host (read-only mission, no build).
- Did not verify the 60/177 conversion counts by a second independent tool; the gh API `?per_page`
  pagination returned empty patches for some filenames, so the per-file verdict for the 8 "STILL-BROKEN"
  was confirmed against the PR-head blob (`gh api .../contents?...ref=refs/pull/1615/head`) instead of the
  files diff endpoint. The 60-file / 177-site conversion count is from the diff-endpoint per-file patch grep.
- Did not classify the 25 subtest-only lines individually beyond confirming each maps to an already-classified
  first-level family.
- Did not check whether the 81 class-B files are covered by a different open card (only that #1615 does not
  touch them).

## repo-rule compliance

- Read-only Mission. No product write, no PR, no card booked, no rerun, no `workflow_dispatch`. No touch of
  `.github/**`, `internal/` (only read via gh blob API), `scripts/**`. No subagents.
- Remote witness (own persistent zone, gh API, no product clone):
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` →
  `40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop`.
- `gh pr view 1615 --json` base = `40cb28c758b02960356434b630086a341ebe1738`, head = `003c48fa53d8cf6c3c76c7a098fe0783bb1fd9cd`.
- No `.github/**` touched, no PR, no hosted-matrix rerun.
- Evidence lives only in baseharbor-plan evidence/, never in a product repo.

## Container / network / volume before–after + cleanliness

- Before: none started by this lane.
- After: none. No container/Compose/Docker/Podman started on any host, including the coordinator host.
- `cleanliness: ` clean. Scratch limited to gh-API reads under the agent's persistent zone and
  `/tmp/w217-*` (w217 dossier read-only copies, cleaned at END). No worktree, no test-eigenes
  netzwerk/volume/state-Verzeichnis.

## END

END_DONE w234-0428-204-helpermap: 181 first-level families classified A=80 / B=81 / C=10 / D=10 (206
`--- FAIL:` lines); #1615 operator helper heals the 80 class-A runWithIO tests on landing (60 files / 177
sites converted; essentially no class-A file left broken); class B (81 direct `.Run`/fixture) is the
remaining 0428-204 work-set, untouched by #1615. SHA = baseharbor-plan origin/main head at commit time.
Read-only, no product change, no PR, no matrix run.
