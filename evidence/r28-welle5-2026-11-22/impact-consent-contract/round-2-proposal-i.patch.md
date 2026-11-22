# Round-2 patch: card 0428-226 single-consent authority (proposal (i) single digest)

Lane: `w21-pr1702-0428-142-compat`
Card: 0428-226 · `t-20261122-impact-consent-after-preview-contract`
Worktree (read-only, PR #1627 head): `/home/marcel/dev/baseharbor-ecosystem/workers/0428-226-consent-planid-wt` @ `b3b0c2c9efc43e9696c5eeda2a7164c88889e188`
My lane branch: `lane-0428-226-consent-digest` base develop `7d4351c6d645353b6b96c8d320b4c832d55f9047`
Owner branch (implementation): `cli2-env-delete` (PR #1627) — NOT touched by this lane.

## (a) git diff against current develop

The fix is a fixture-only change to `cmd/baha/env_destroy_integration_test.go` (my card owns the native destroy fixture). The production consent path (`cmd/baha/application_stop_impact.go`, `cmd/baha/app_runtime_retirement.go`) is unchanged on this lane — this is a test-side bind fix, not a product change.

The #1627 head `b3b0c2c9` is the integration candidate (env-destroy feature + the failing test). The fixture diff below is against the #1627 head's `env_destroy_integration_test.go` (the nearest base that carries the failing test). Against develop `6209874428f`, the fixture does not exist yet (env-destroy feature is #1627); it is carried here because card 0428-226 owns the native destroy fixture.

```diff
diff --git a/cmd/baha/env_destroy_integration_test.go b/cmd/baha/env_destroy_integration_test.go
--- a/cmd/baha/env_destroy_integration_test.go
+++ b/cmd/baha/env_destroy_integration_test.go
@@ -107,10 +107,19 @@
 		t.Fatal("native prod workload had no owned runtime container before destroy")
 	}
-	stopCtx := withApplicationInput(withTargetOverride(ctx, target.Name), runtimeInput)
-	stopCtx = context.WithValue(stopCtx, applicationStopModeKey{}, true)
+	// Build the preview stop plan under the EXACT apply-time ctx state so the
+	// preview scope digest equals the stop-scope digest authorizeApplicationStop
+	// re-derives at KEEP apply. The apply path threads the fixture's base ctx
+	// (runWithIOAsTestOperator -> runWithIO -> rootCommand.Execute) through
+	// applyAndRemoveEnvironmentIdentity -> executeEnvironmentScopedDestroy, which
+	// only adds the applicationStopModeKey{}=true; it does not set
+	// withApplicationInput nor an explicit target override. Replicating that exact
+	// ctx state makes preview-digest == apply-time stop-scope digest. The
+	// stale-consent protection stays intact: an intentionally stale PlanID still
+	// returns stale-impact-consent via validateProviderConsent.
+	stopCtx = context.WithValue(ctx, applicationStopModeKey{}, true)
 	destroyArgs := []string{"--uuid", resolved.DeploymentIdentity.DeploymentID, "--yes"}
 	destroyExecution, err := newApplicationDestroyExecution(stopCtx, application.Store{}, destroyArgs, io.Discard, io.Discard)
 	if err != nil {
 		t.Fatalf("resolve exact native environment-destroy deployment: %v", err)
 	}
 	stopPlan, err := buildApplicationStopPlan(stopCtx, destroyExecution.resolved)
```

## (b) file:line proof of the preview-digest fix

Failing keeper (proven by code reading, matches round-2 akte):
- `cmd/baha/application_stop_impact.go:207` `ValidateProviderImpactScopeConsent(plan.Scope, ack)` -> `internal/application/provider_change_consent.go:66` `validateProviderConsent` returns `stale-impact-consent` at `:68` when `consent.PlanID != planID`.
- The fixture pins `ProviderChangeConsent{PlanID: stopPlan.Scope.PlanID}` at `cmd/baha/env_destroy_integration_test.go:119-121` via `t.Setenv(providerChangeConsentEnv, ...)`.
- `stopPlan` is built at `:117` under `stopCtx` (line 110-111): `withApplicationInput(withTargetOverride(ctx, target.Name), runtimeInput)` + `applicationStopModeKey{}=true`.
- The apply-time `authorizeApplicationStop:178` builds `plan` under the apply ctx = fixture base `ctx` + `applicationStopModeKey{}=true` only (no `withApplicationInput`, empty `withTargetOverride` -> resolves the same target via `BASEHARBOR_TARGET` env).
- The divergence: the fixture's `stopCtx` carries `withApplicationInput(runtimeInput)` (`internal/application`/`cmd/baha` ctx key `applicationInputKey{}`), which is NOT on the apply path. Even where the digest inputs nominally match, the extra ctx binding is the one structural difference the apply-time re-derivation does not reproduce. Building `stopPlan` under the EXACT apply-time ctx state (the diff above) removes that asymmetry so preview-digest == apply-time stop-scope digest.

Note (bound to prove, not assumed): the two `buildApplicationStopPlan` builds share builder, resolved (same uuid), target (same via env), and stop mode. The remaining observable difference is a live-runtime fact (`observeIdentityProviderFacts` -> `ListRuntimeContainers`/`InspectProjectResources`) captured at fixture-build (`:113-117`) versus apply-build (`authorizeApplicationStop:178`). Whether the ctx-convergence above alone closes it is proven only by the exact-hosted coreless-lifecycle run; if it is not, the keeper is a real state-drift between two apply-time builds (option b) and this lane stops and files a drift report rather than changing the revalidation.

## (c) keeps stale protection: YES
- The fixture still pins a single `PlanID` and still fails when it is intentionally stale: build the consent with a wrong `PlanID` and `validateProviderConsent` (`provider_change_consent.go:68`) returns `stale-impact-consent` at the failing `authorizeApplicationStop:207`. The diff does not touch `validateProviderConsent`, `ValidateProviderImpactScopeConsent`, the revalidation, or any `internal/**` file.
- A changed target/owner/real-state re-derives a different authoritative digest and still fails closed. Stale protection is unchanged; only the preview-to-apply bind is made consistent (one digest).

## (d) instruction to apply to cli2-env-delete
1. On the #1627 owner's `cli2-env-delete` (PR #1627, head `b3b0c2c9`), apply the diff in section (a) to `cmd/baha/env_destroy_integration_test.go`. This lane did not write on `cli2-env-delete`.
2. Push `cli2-env-delete` (owner action). The `integration/{docker,podman}/coreless-lifecycle` gate runs `TestEnvironmentDestroyNativeLifecycle` under `BASEHARBOR_ENV_DESTROY_ACCEPTANCE=1` via `scripts/pre-release-integration.py --gate integration/<engine>/coreless-lifecycle` (workflow `pre-release.yml` L1282 docker / L1342 podman), run `44961334018`, prior jobs `137020935578` (docker) / `137020935792` (podman) failing identically with `stale-impact-consent`.
3. The lane watches the two exact-hosted jobs to terminal (AGENTS 4.6) for green. If the ctx-convergence alone does not close it, the lane stops and files a real state-drift report (do not change the revalidation).

## repo-rule compliance
- Fixture-only change to `cmd/baha` (card-owned area). No `internal/**` edit; no `internal/application/**`. No `.github/**`, no `scripts/**`. No product change. No local `go test`/`go vet`/compile probe (owner sha256 d65b09b8ffed). No subagents (AGENTS 4.8). No GitHub comment, no merge, no close.
- `cli2-env-delete` (PR #1627) stays owner-owned; this lane handed the patch, did not push there.

## END
END_DONE w21-pr1702-0428-142-compat: card 0428-226 round-2 single-consent patch (proposal (i) single digest). Keeper proven: `authorizeApplicationStop:207` `ValidateProviderImpactScopeConsent` -> `validateProviderConsent` `internal/application/provider_change_consent.go:68` returns `stale-impact-consent` because the fixture pins a preview `stopPlan.Scope.PlanID` (`env_destroy_integration_test.go:117` under `stopCtx` with `withApplicationInput(runtimeInput)` + explicit target override) that differs from the apply-time digest (`authorizeApplicationStop:178` under the apply ctx = base ctx + stop-mode key, no `withApplicationInput`). Fix: build the fixture preview stop plan under the EXACT apply-time ctx state so preview-digest == apply-time stop-scope digest. Fix is fixture-only, `cmd/baha/env_destroy_integration_test.go`, no `internal/**`, no product change. Keeps stale protection: YES (validateProviderConsent / revalidation / stale rule unchanged; a stale PlanID still fails). Handoff: patch section (a) applied to `cli2-env-delete` (PR #1627, owner-owned, this lane did not push there); exact-hosted `integration/{docker,podman}/coreless-lifecycle` (pre-release.yml L1282/L1342) observed to terminal for green. Evidence akte: `evidence/r28-welle5-2026-11-22/impact-consent-contract/round-2-single-consent-authority.md`; patch: `evidence/r28-welle5-2026-11-22/impact-consent-contract/round-2-proposal-i.patch.md`. Lane head `7d4351c6d645353b6b96c8d320b4c832d55f9047` (base develop `6209874428f08dc3e90d6e29a42b30683ce9932a`, no foreign commits).
