# Round-3 evidence: drift hypothesis for card 0428-226 (single-consent authority) — NO verdict yet

Lane: `w21-pr1702-0428-142-compat`
Card: 0428-226 · `t-20261122-impact-consent-after-preview-contract`
Worktree (read-only, PR #1627 head): `/home/marcel/dev/baseharbor-ecosystem/workers/0428-226-consent-planid-wt` @ `b3b0c2c9efc43e9696c5eeda2a7164c88889e188`
My lane branch: `lane-0428-226-consent-digest` base develop `7d4351c6d645353b6b96c8d320b4c832d55f9047`
Owner branch (implementation): `cli2-env-delete` (PR #1627) — NOT touched by this lane (no write access, owner-implemented, AGENTS 2/3.1).

Purpose: per owner decision w21h, prepare the option-(b) drift report NOW so no time is lost if the exact-hosted coreless-lifecycle CI still returns `stale-impact-consent`. This akte holds ONLY proof (two building blocks), no verdict. A red CI run finalizes this into the drift report; a green run closes the card as "implemented, not analysed" (round-2, proposal (i)).

## Building block (i): the two failing exact-hosted jobs
Both prior exact-hosted coreless-lifecycle jobs failed identically (run 44961334018, event pull_request, head b3b0c2c9efc):
- Docker job 137020935578 (worker uuid `af707b0c-6f1d-4a51-b918-ca1a97c79739`):
  `env_destroy_integration_test.go:128: native env destroy: process scoped deployment env-destroy-native (af707b0c-6f1d-4a51-b918-ca1a97c79739): provider change: stale-impact-consent`
- Podman job 137020935792 (worker uuid `4ccdd4c5-5cad-4571-9fa9-b495d204c1c3`):
  `env_destroy_integration_test.go:128: native env destroy: process scoped deployment env-destroy-native (4ccdd4c5-5cad-4571-9fa9-b495d204c1c3): provider change: stale-impact-consent`
- Wrapper (both): `Environment destroy incomplete; identity retained so the operation can be retried: process scoped deployment env-destroy-native (<uuid>): provider change: stale-impact-consent`
- Immediately before: `Members (preserved): none recorded.` and banner `BaseHarbor · env-destroy-native · prod`, `INFO target docker-dev`.
- Failing keeper (code reading, matches round-2 akte `a9b295fcb`): `cmd/baha/application_stop_impact.go:207` `ValidateProviderImpactScopeConsent(plan.Scope, ack)` -> `internal/application/provider_change_consent.go:66` `validateProviderConsent` returns `stale-impact-consent` at `:68` when `consent.PlanID != planID`. The fixture pins `ProviderChangeConsent{PlanID: stopPlan.Scope.PlanID}` at `env_destroy_integration_test.go:119-121` (`t.Setenv(providerChangeConsentEnv, ...)`) and builds `stopPlan` at `:117` under `stopCtx`.

## Building block (ii): the live-runtime-observation hypothesis (file:line)
Both the fixture preview build and the apply build call `buildApplicationStopPlan` (`cmd/baha/application_stop_impact.go:28`), which calls `observeApplicationProviderFacts(ctx, applied)` (`cmd/baha/app_core_requirement.go:396`) -> `observeIdentityProviderFacts` (`cmd/baha/application_identity_observation.go:22`), which reads live runtime facts:
- `detectRuntimeForTarget(ctx, resolved.Target)` (`application_identity_observation.go:13`)
- `provider.ListRuntimeContainers(ctx)` (`application_identity_observation.go:17`)
- `provider.InspectProjectResources(ctx, files.Project, expected)` (`application_identity_observation.go:33`)
- then `observeSharedBackendProviderFacts` / `observeApplicationBrokerFacts` / `observeNativeBackendProviderFacts` / `observeApplicationExposureFacts` (`app_core_requirement.go`), each reading live registry/ownership/binding/inventory/real-state facts that feed the leaf planID digest.

The two observation points in the SAME invocation:
- Fixture preview build at `env_destroy_integration_test.go:113-117` (`newApplicationDestroyExecution(stopCtx,...)` + `buildApplicationStopPlan(stopCtx, destroyExecution.resolved)`).
- Apply-time build at `cmd/baha/application_stop_impact.go:178` (`authorizeApplicationStop` -> `buildApplicationStopPlan(ctx, resolved)`), reached via `cmd/baha/app_runtime_retirement.go:113` `retireRuntimePreservingData` -> `authorizeApplicationStop`.

Hypothesis (unverified, no verdict): between these two observation points the live-runtime fact set (`ListRuntimeContainers` / `InspectProjectResources` / backend/registry observations) differs, so the two `buildApplicationStopPlan` re-derivations produce different sha256 `Scope.PlanID` digests even under identical ctx state. The ctx-convergence fix in round-2 (`round-2-proposal-i.patch.md`) removes the only structural ctx asymmetry (`withApplicationInput`/explicit target override) but does NOT guarantee two identical observations at two different points; if the digest divergence is a genuine live-runtime drift, the fixture bind cannot close it and this is real state drift between two apply-time builds (option b).

## Not yet decided (explicitly)
- Whether the ctx-convergence alone closes the digest mismatch (would need the green exact-hosted coreless-lifecycle run).
- Whether the divergence is a live-runtime observation drift (option b, STOP + drift report, revalidation untouched per w21i point 1) or a ctx-state artifact (option i, fix in the fixture).
- Which of the two keepers (`authorizeApplicationStop:207` scope-consent vs `app_runtime_retirement.go:116` stop/retirement cross-bind) actually fired — the existing hosted logs cannot decide (markers m1/m2 absent from the structured-JSON test-output stream); a separate visible-output diagnostic run would be required, which the guard treats as a negative proof that escalates to the owner.

## Boundaries observed
- Read-only: `git show`, `git apply --check` (dry-run), `grep`, `sed`, `git diff --no-index`. No `git apply` (no write on cli2-env-delete), no deploy, no commit on #1627.
- No local `go test` / `go vet` / compile probe (owner sha256 d65b09b8ffed). No `.github/**`, no `scripts/**`. No subagents (AGENTS 4.8). No GitHub comment, no merge, no close.
- Evidence only in baseharbor-plan; this akte is a prepared drift report awaiting a red CI run to finalize.

## END
END_PENDING w21-pr1702-0428-142-compat: card 0428-226 round-3 drift evidence prepared (no verdict). Keeper: `authorizeApplicationStop:207` `ValidateProviderImpactScopeConsent` -> `validateProviderConsent` `internal/application/provider_change_consent.go:68` (stale-impact-consent); fixture pins preview `stopPlan.Scope.PlanID` at `env_destroy_integration_test.go:117/119-121` under `stopCtx`. Failing jobs 137020935578 (docker, af707b0c...) / 137020935792 (podman, 4ccdd4c5...), run 44961334018, head b3b0c2c9efc, both `env_destroy_integration_test.go:128 ... provider change: stale-impact-consent`. Hypothesis: two `buildApplicationStopPlan` observations (fixture :113-117 vs apply :178) of live-runtime facts (`observeIdentityProviderFacts` -> `ListRuntimeContainers`/`InspectProjectResources`, `app_core_requirement.go:396` / `application_identity_observation.go:22`) drift between points -> different `Scope.PlanID`. Fix (round-2, proposal i) ctx-convergence: `git apply --check` against b3b0c2c9efc passes clean (exit 0). Handoff to #1627 owner for cli2-env-delete push (this lane did not push). Watch integration/{docker,podman}/coreless-lifecycle to terminal: green => implemented, not analysed; red => STOP, finalize this drift report, revalidation untouched. Lane head `7d4351c6d645353b6b96c8d320b4c832d55f9047` (base develop `6209874428f08dc3e90d6e29a42b30683ce9932a`, no foreign commits). Waiting on owner push.
