# 0428-204 entry-point acceptance — 2026-11-21

Current source baseline: `c43d816120651c33a7a9c02f6ee805ae78440602` (local focused test source). The helper is test-only in `cmd/baha/test_operator_context_test.go`; hosted `PR · Validation · cli-build` passed at run `44887314441`, confirming production build remains separate. The local command below passed (34.679s):

```text
go test ./cmd/baha -run '^(TestMCPGenericClientDiscoversCompleteSemanticSurfaceAndExercisesReadOnlyTools|TestPersesLifecycleTransportActionMatrix|TestRestoreBindsOriginalExternalIdentityAndProtectedDestination|TestGuidedRepositoryRuntimeFixtureRegressionSuite)$' -count=1
```

| Entry-point class and fixture | Before: failing regression | After: source point and mapped gate | Hosted proof |
| --- | --- | --- | --- |
| `runWithIO` → `rootCommand().Execute` | `TestAppCreateListShowPlan` (`main_test.go:46`) and `TestSharedSecretsRuntimeFixtureUsesActualSourceOnlyInitialization` (`app_secrets_shared_runtime_test.go:25`) failed managed operator auth | `runWithIOAsTestOperator` (`test_operator_context_test.go:14`); test names hash to cli-0 and cli-2 | Run `44887314441`: `PR · Go unit · cli-0` job `136795363539` PASS and cli-2 job `136795363558` PASS |
| MCP server/client tool handler | `TestMCPGenericClientDiscoversCompleteSemanticSurfaceAndExercisesReadOnlyTools` failed when handler rebuilt the call context | `agent_mcp_test.go:88` passes `testOperatorContext`; test hashes to cli-0 | Run `44887314441`, cli-0 job `136795363539` PASS |
| Perses lifecycle transport | `TestPersesLifecycleTransportActionMatrix` failed when transport matrix built a fresh context | `perses_lifecycle_transport_test.go:53` applies helper in `persesMatrixContext`; test hashes to cli-0 | Run `44887314441`, cli-0 job `136795363539` PASS |
| Direct application restore | `TestRestoreBindsOriginalExternalIdentityAndProtectedDestination` failed on direct context creation | `application_restore_external_identity_test.go:83` applies helper before `machineNoninteractiveContext`; test hashes to cli-0 | Run `44887314441`, cli-0 job `136795363539` PASS |
| Repository apply fixture | `TestGuidedRepositoryRuntimeFixtureRegressionSuite` failed on direct fixture context | `repository_runtime_fixture_test.go:624` supplies helper at the shared apply-call boundary; test hashes to cli-0 | Run `44887314441`, cli-0 job `136795363539` PASS |

Exact hosted run [44887314441](https://github.com/mcpdev80/baseharbor/actions/runs/44887314441) at `f0f25e49753ad6b06b490072739437eeec42de8a` is terminal SUCCESS; all four CLI shards, build and aggregate `PR Selected Checks` passed. The complete set of entry-point regressions also passed in the local focused command at the source baseline above.
