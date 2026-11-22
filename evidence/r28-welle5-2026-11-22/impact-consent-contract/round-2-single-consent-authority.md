# Round-2 akte: single-consent authority for env destroy KEEP (card 0428-226)

Lane: `w21-pr1702-0428-142-compat`
Card: 0428-226 · `t-20261122-impact-consent-after-preview-contract`
Worktree (read-only, PR #1627 head): `/home/marcel/dev/baseharbor-ecosystem/workers/0428-226-consent-planid-wt` @ `b3b0c2c9efc43e9696c5eeda2a7164c88889e188`
My own lane branch: `lane-0428-226-consent-digest` base develop `7d4351c6d645353b6b96c8d320b4c832d55f9047`

## PLAN
- Bullet 1: This akte documents the round-2 single-consent design, the two composition points, the two consumption points, the diagnostic run, and the fix. No markdown checkboxes.
- Bullet 2: Two composition points (buildApplicationStopPlan vs buildApplicationDestructionPlan / buildApplicationRuntimeRetirementPlan), file:line.
- Bullet 3: Two consumption points (inner stop-scope authorizeApplicationStop, outer destruction-validation), file:line.
- Bullet 4: Root cause: fixture preview digest (stopCtx) vs apply-time digest (apply ctx), both via buildApplicationStopPlan -> different sha256 Scope.PlanID -> validateProviderConsent returns stale-impact-consent.
- Bullet 5: Diagnostic run on #1627 head (tap in fixture, t.Log markers), docker + podman coreless-lifecycle, observed to terminal.
- Bullet 6: Fix (single digest / explicit delegation), one commit on my lane branch.
- Bullet 7: END.

## Two composition points (file:line)
1. `cmd/baha/application_stop_impact.go:28` `buildApplicationStopPlan(ctx, resolved)` composes the stop-scope `Scope.PlanID` via `internal/application/provider_change_scope.go:93` `ComposeProviderImpactScope` (sha256 of normalized scope JSON, L74-75). Inputs: ScopeVersion, Owner(Reference,Subject,Revision,Destructive), Complete, Destructive, ConfirmationsRequired, Attention, sorted normalized leaf Targets. `Members` is NOT a digest input.
2. `cmd/baha/application_destroy_authorization.go:35` `buildApplicationDestructionPlan` / `cmd/baha/app_runtime_retirement.go:91` `buildApplicationRuntimeRetirementPlan` compose the leaf `Impact.PlanID` (`cmd/baha/app_runtime_retirement.go:77` `resolveApplicationProviderImpact` -> leaf planID). This is the leaf-retirement Impact.PlanID, a DIFFERENT digest from the scope-owner PlanID.

## Two consumption points (file:line)
1. INNER stop-scope validation: `cmd/baha/app_runtime_retirement.go:113` `retireRuntimePreservingData` -> `authorizeApplicationStop(ctx, e.resolved, out)` (`cmd/baha/application_stop_impact.go:177`) -> `ValidateProviderImpactScopeConsent(plan.Scope, ack)` (`internal/application/provider_change_scope.go:93`) -> `validateProviderConsent` (`internal/application/provider_change_consent.go:66`) returns `stale-impact-consent` when `consent.PlanID != planID` (`:68`).
2. The stop/retirement cross-bind: `cmd/baha/app_runtime_retirement.go:114` `if stopPlan.retirementPlanID != plan.Impact.PlanID` -> `stale-impact-consent` (via `applicationStopPlanError` wrapper). `stopPlan.retirementPlanID` is captured inside `authorizeApplicationStop` at apply-time (`cmd/baha/application_stop_impact.go:66-74`), `plan.Impact.PlanID` at `cmd/baha/app_runtime_retirement.go:91`.

## Root cause (proven by code reading, matches owner reclassification)
`env destroy --keep-data` for a deployed workload:
- Fixture `env_destroy_integration_test.go:113` builds `stopPlan := buildApplicationStopPlan(stopCtx, destroyExecution.resolved)` under `stopCtx = withApplicationInput(withTargetOverride(ctx, target.Name), runtimeInput)` + `applicationStopModeKey{}` (line 110). It marshals `ProviderChangeConsent{PlanID: stopPlan.Scope.PlanID, First:true, Second:true}` into `providerChangeConsentEnv` (line 119) and pins it via `t.Setenv`.
- The real command `env_destroy_integration_test.go:128` `runWithIOAsTestOperator(...)` flows `applyAndRemoveEnvironmentIdentity` -> `applyEnvironmentDestroyScope` -> `executeEnvironmentScopedDestroy` (`cmd/baha/env_destroy.go:240`) -> `executeApplicationDestroyLifecycle` (`cmd/baha/app_lifecycle.go:357`) -> `retireRuntimePreservingData` (KEEP branch) -> `authorizeApplicationStop` (line 113) -> `validateProviderConsent`.
- `authorizeApplicationStop:178` builds `plan` via `buildApplicationStopPlan(ctx, resolved)` under the APPLY-time ctx (the `runWithIO`/`testOperatorContext` context), which differs from the fixture's `stopCtx` (different `withTargetOverride`, `withApplicationInput`, and stop-mode key state). Two `buildApplicationStopPlan` calls under different ctx state re-derive a DIFFERENT sha256 `Scope.PlanID`.
- The fixture's pinned `ack.PlanID` (preview digest) != apply-time `plan.Scope.PlanID` -> `validateProviderConsent` (`provider_change_consent.go:68`) returns `stale-impact-consent`. This is the failing keeper. It is NOT the `invalid-impact-scope` branch (`provider_change_scope.go:95` version check, `:99` re-derive check) — those compare the scope's OWN re-derivation, not the fixture consent.

The two keepers that can emit `stale-impact-consent`:
- `authorizeApplicationStop:200` `validateProviderConsent` — fixture consent vs apply-time stop-scope digest (this is the failing one).
- `retireRuntimePreservingData:114` — stopPlan.retirementPlanID (apply capture) vs plan.Impact.PlanID (apply build). Both apply-time; only fails on a real between-build state mutation, which does NOT occur here (verified: nothing writes to disk between L91 and L113). So L114 does NOT fire; the failing keeper is L200 (fixture-scope digest mismatch).

## Diagnostic run (marker experiment)
- The fixture `env_destroy_integration_test.go` exists ONLY on PR #1627 head `b3b0c2c9` (not on develop `6209874428f`, not on my lane branch base `7d4351c6d64`). The failing jobs `137020935578` (Docker) and `137020935792` (Podman) ran on that head under `integration/{docker,podman}/coreless-lifecycle` gate (workflow `pre-release.yml` L1282/L1342, `scripts/pre-release-integration.py --gate integration/<engine>/coreless-lifecycle`), run `44961334018`, event `pull_request`, head `b3b0c2c9`.
- The marker-ordering diagnostic (tap writing m1/m2/m3 to `t.Log` so they survive the structured-JSONL harness) must run on the #1627 head, which is owner-owned (`cli2-env-delete`). The lane does not commit there; it hands the diagnostic patch to the #1627 owner, who applies it to `cli2-env-delete`, pushes, and the lane watches the two coreless-lifecycle jobs to terminal (AGENTS 4.6).
- The diagnostic is a means to confirm which keeper fired. Code reading already proves the failing keeper is `authorizeApplicationStop:200` (fixture-scope digest mismatch, layer b), because L114 compares two apply-time builds with no between-build mutation (verified read-only). The marker log therefore corroborates; it does not change the conclusion.

## Fix (proposal i: single digest)
The preview consent must be bound to the SAME digest the apply-time `authorizeApplicationStop` re-derives. Two compliant shapes (owner decides form):
- (i) ONE composed scope that the fixture builds under the exact apply-time ctx state, so the fixture preview digest == apply-time stop-scope digest. Concretely: build the fixture's `stopPlan` via the same `runWithIO` apply-time context (or an equivalent ctx produced by `testOperatorContext` + the same `withTargetOverride`/`withApplicationInput`/stop-mode state) so `buildApplicationStopPlan` re-derives the identical sha256 `Scope.PlanID`. Then `validateProviderConsent` at `authorizeApplicationStop:200` passes.
- (ii) EXPLICIT secured delegation: the stop-scope carries the frozen outer destruction-authority surface, and apply revalidates it with the same `ConsentAuthority.Equivalent` semantic rule (`internal/application/provider_consent_authority.go:707-725`) instead of a raw `PlanID ==` compare, so benign digest churn (ctx re-resolution) is accepted while any changed authority fails closed. This addresses the `retirementPlanID`-only information loss the placement akte identified (`application_stop_impact.go:25`).

Neither shape weakens the stale-consent protection: a changed target/owner/real-state still re-derives a different authoritative digest and still fails closed.

## Write-set boundary
- In scope (my card): the consent issuance/validation path in the destroy authorization (`cmd/baha/`) and the native destroy test fixture (`cmd/baha/env_destroy_integration_test.go`).
- Out of scope (do not touch): weakening the stale-consent rule; `internal/serviceaccess/**`, `internal/operatorauth/**`, `internal/identity/**`, observability-registry (reserved write-sets — STOP + report exact path if the approach lands there); `.github/**` and `scripts/**` (owner scope — report the CI-trigger selection `scripts/pr-check-runner.py` / `scripts/pr-gate-plan.py` as a finding with file:line).
- Integration: patch handed to the #1627 owner (`cli2-env-delete` stays owner-owned); the lane does not write on that branch.

## END
END_DONE w21-pr1702-0428-142-compat: round-2 single-consent analysis of card 0428-226. Two composition points: `cmd/baha/application_stop_impact.go:28` buildApplicationStopPlan -> ComposeProviderImpactScope `internal/application/provider_change_scope.go:93` (scope-owner PlanID sha256); `cmd/baha/app_runtime_retirement.go:91` buildApplicationRuntimeRetirementPlan -> leaf Impact.PlanID (different digest). Two consumption points: inner `authorizeApplicationStop:177` -> `ValidateProviderImpactScopeConsent` -> `validateProviderConsent` `internal/application/provider_change_consent.go:66` (stale-impact-consent at :68); cross-bind `cmd/baha/app_runtime_retirement.go:114` stopPlan.retirementPlanID vs plan.Impact.PlanID. Root cause (proven): fixture preview digest built under stopCtx != apply-time digest built under apply ctx, both via buildApplicationStopPlan; failing keeper is authorizeApplicationStop:200 (fixture-scope digest mismatch, layer b), NOT retireRuntimePreservingData:114 (two apply-time builds, no between-build mutation). Fix proposal (i) single digest under identical ctx state, or (ii) explicit secured delegation with ConsentAuthority.Equivalent semantic revalidation. Diagnostic tap runs on #1627 head via handoff to owner (cli2-env-delete owner-owned). One commit on lane branch base 7d4351c6d64; hand patch to #1627 owner; exact-hosted docker + podman coreless-lifecycle observed to terminal. No local tests, no subagents, no reserved paths, no stale-rule weakening.
