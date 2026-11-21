# Fifth #1627 failure analysis — consent after preview

## PLAN

1. Pin the analysis to exact #1627 head `b3b0c2c9efc43e9696c5eeda2a7164c88889e188` and failed Docker application job `137020935578` from run `44961334018`; no verdict or merge action.
2. Compare the five candidate heads `8de37f58caa`, `62dd38f9b6d`, `ac05cc4efbc`, `38be89aa4a0`, and `b3b0c2c9efc`, recording each round’s actual change.
3. Trace production consent creation in preview and validation during apply, with exact file:line references.
4. Classify the failure as fixture-side or product-side from the source and failure path; state uncertainty if source evidence is insufficient.
5. Publish this read-only analysis in Planning origin/main and leave #1627 without a verdict.


## Read-only fifth-failure analysis

Exact target: #1627 head `b3b0c2c9efc43e9696c5eeda2a7164c88889e188`, run `44961334018`. Docker application job `137020935578` and Podman application job `137020935792` completed failure; the overall run was still `in_progress` at last observation. Owner-provided hosted logs show both jobs failing `TestEnvironmentDestroyNativeLifecycle` with `Environment destroy incomplete; identity retained so the operation can be retried: process scoped deployment env-destroy-native (...): provider change: stale-impact-consent`; Docker deployment UUID `af707b0c-6f1d-4a51-b918-ca1a97c79739`, Podman UUID `4ccdd4c5-5cad-4571-9fa9-b495d204c1c3`. Both show `Members (preserved): none recorded.` and `INFO target docker-dev` / corresponding Podman target before `--- FAIL: TestEnvironmentDestroyNativeLifecycle`. The hosted command `gh run view --job ... --log-failed` said logs would be available when the run completes, so the quoted line is explicitly the Owner-provided log witness. No verdict or merge is made for #1627.

### Five candidate heads

1. `8de37f58caa` (`ci: validate env destroy against coreless gates`) adds selected Docker/Podman routing, selection logic, and routing tests; it does not change the failing consent implementation.
2. `62dd38f9b6d` is a merge of develop `42da7128`; it is a base hop, not a task-specific consent fix.
3. `ac05cc4efbc` (`test: authenticate env destroy native fixture`) adds `testOperatorContext` to the native test context and cleanup context.
4. `38be89aa4a0` (`test: bind env destroy consent to stop plan`) builds consent with the target/runtime-input context and `applicationStopModeKey`, using `buildApplicationStopPlan`.
5. `b3b0c2c9efc` (`test: prepare consent through destroy resolver`) further resolves using `newApplicationDestroyExecution` with the same `--uuid <deployment-id> --yes` selector used by the production child path, then builds the test consent from that resolved object.

### Preview-to-apply path and classification

The environment preview collects the environment-scoped member set in `cmd/baha/env_destroy.go:99-115`; unconfirmed JSON returns that plan at `:121-135`. The confirmed path installs runtime input and target at `:164-165`, then calls `applyAndRemoveEnvironmentIdentity` at `:170-175`. KEEP delegates each selected deployment by UUID to the existing application destroy lifecycle and sets stop mode at `cmd/baha/env_destroy.go:240-245`. The native fixture constructs its consent before invocation at `cmd/baha/env_destroy_integration_test.go:110-125` and invokes confirmed environment destroy at `:127-129`.

Inside the production lifecycle, stop mode reaches `authorizeApplicationDestruction` at `cmd/baha/app_lifecycle.go:380`; that function creates the production `applicationDestructionPlan`, validates the supplied provider consent at `cmd/baha/application_destroy_authorization.go:147-181`, then re-builds the current plan at `:183-188`. The test currently creates consent from a different plan builder: `buildApplicationStopPlan` at `cmd/baha/env_destroy_integration_test.go:117`, whereas production authorization consumes `buildApplicationDestructionPlanForOperation` via `buildApplicationDestructionPlan` at `cmd/baha/application_destroy_authorization.go:28-38,41-45`. The generated consent is then fed through `providerChangeConsentEnv` at test `:121-125`.

Assessment: **the evidence points first to a test-fixture plan mismatch**, not proof that every consent becomes stale when production resolves the UUID again. The fifth head aligned the fixture’s resolver and UUID selector with production, but it still derives consent with `buildApplicationStopPlan` while the production authorization path validates a `buildApplicationDestructionPlan` scope. The error is a `ProviderChangeError` (`internal/application/provider_change_consent.go:66-69`), and the logs alone do not identify whether it arose at supplied-consent validation (`application_destroy_authorization.go:180-181`) or the later in-call plan revalidation (`:187-188`). Thus the test’s plan-builder mismatch is the concrete remaining divergence; the failure does not establish a structural product defect in UUID re-resolution. To discriminate conclusively, a future test should obtain the exact consent scope from the same production authorization-plan builder and separately assert deterministic equality across its internal revalidation. This is analysis only, not REQUEST CHANGES or a verdict.

Cross-reference requested: `fifth-round-child-read-diagnosis.md`. That filename was not present in the local Planning evidence tree at review time, so this note does not copy or claim its contents.

## cleanliness

Read-only source inspection and hosted run observation only. No tests, containers, or compose projects were started.

END_BLOCKED codex-rev-1747: #1627 remains no-verdict; both named lifecycle jobs failed with stale-impact-consent and the overall run is not terminal.
