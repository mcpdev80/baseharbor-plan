# 0427-048 public CLI/JSON/MCP/HTTP surface audit — 2026-11-13

## Result

The deliverable was already integrated on current `develop` at `1cbfaefe24e19ed6110a0cc68eb8b9b869880e52`; no duplicate product registration was added. The same source revision has the durable merge receipt [`evidence/receipts/commits/1cbfaefe24e19ed6110a0cc68eb8b9b869880e52.json`](receipts/commits/1cbfaefe24e19ed6110a0cc68eb8b9b869880e52.json), mapping merge commit `1cbfa...` to PR #1522. Per Maintainer's receipt convention, this is the durable green-at-merge proof; no ephemeral Actions run page is used as card evidence.

## Registration inventory

- CLI tree and typed JSON semantics: `cmd/baha/machine_coverage.go` maps every visible command to a semantic machine operation, alias, presentation surface, or explicit exclusion. `docs/reference/cli-machine-coverage.md` is generated from the real command tree and operation registry; the documentation test rejects drift and duplicate command paths.
- MCP: `newMCPServer` registers the grouped tools. `machineMCPTool` rejects missing canonical operations. `TestAgentDescribeJSON` checks operation/tool inventory; the in-process MCP client test checks full tool discovery, safety metadata and real read-only invocation. Registration readiness tests reject duplicate actual tool names and invoke `app.list`.
- HTTP: `cmd/baha/machine_http_operations.go` is the executor's exact support registry. `internal/machinehttp.New` derives discovery from that registry, preserving canonical safety/authorization metadata and rejecting unsupported operations. HTTP and tenant tests cover authenticated HTTPS, authorization denial before execution, and exact discoverability versus dispatch support.
- Accepted management-access profile import is consumed by the real onboarding path (`cmd/baha/onboarding.go` via `cmd/baha/connection_profile_codec.go` and `contracts/managementaccess/v1.Store`); focused tests cover validation-before-mutation, conflict rejection and destination binding.
- v0.4.27 inventory is limited to the operations supported by the existing Core authority: authenticated workstation onboarding; supported local/selected remote Docker and Podman initial app lifecycle; Target selection; status, consent and authorization. Generalized cross-environment promotion and advanced multi-candidate rollout remain v0.4.28 and are excluded.

## CI routing

`scripts/pr-check-runner.py` defines `wizard-registration-tests` as individually discovered registration families and fails if a required test is missing, skipped or not PASS. `scripts/pr-gate-plan.py` routes the registration test and reference files to this check (plus the relevant code/documentation checks). The matching existing test family is `TestAppRegistrationCI*`, `TestCommandTreeCI*`, `TestMachineCoverageCI*`, `TestMachineDocumentationTracksRegistryAndCommandTree`, `TestHumanCommandIndexTracksExactCommandMetadata` and `TestMCPRegistrationCI*`. No new CI workflow is needed.

## Exact-source verification

All commands below ran locally on `1cbfaefe24e19ed6110a0cc68eb8b9b869880e52`; each returned `ok`:

- `go test ./cmd/baha -run '^(TestAppRegistrationCICommandHelpAndJSONDiscovery|TestCommandTreeCIRouterPathsUnique|TestMachineCoverageCIRealTreeAndJSONClassification|TestMCPRegistrationCIInProcessDiscoverAndInvoke|TestMachineDocumentationTracksRegistryAndCommandTree|TestAgentDescribeJSON|TestMCPGenericClientDiscoversCompleteSemanticSurfaceAndExercisesReadOnlyTools|TestOnboardingImportValidatesBeforeMutation|TestOnboardingImportConflictFailsClosedWithoutReplacement|TestOnboardingImportStoreBindingRejectsForeignInstallation|TestHTTPAdvertisedReadOperationsReachInputValidation|TestHTTPActualCoreExecutorStartsAndAdvertisesCanonicalOperations)$' -count=1`
- `go test ./cmd/baha -run '^(TestExpectedPreconditionsShareTypedCLIMCPErrors|TestMCPReadEntryExpectedPreconditions)$' -count=1`
- `go test ./internal/machinehttp -run '^(TestViewerCannotAdmitMachineMutation|TestHandlerRequiresHTTPSAndAuthenticatedPrincipal|TestExecutionCannotBeReadByDifferentOperator|TestBrowserOriginAndExpiredPrincipalFailBeforeExecution|TestDiscoveryAndDispatchShareExactHTTPExecutionSupport)$' -count=1`
- `go test ./contracts/managementaccess/v1 -count=1`

No Docker/Podman journey is needed for this registration-only task; runtime lifecycle acceptance remains with its own gates.
