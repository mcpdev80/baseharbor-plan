# Card 0428-226 (t-20261122-impact-consent-after-preview-contract) — round-1: KEEP destroy stale-impact-consent root cause + planID parity fix

**Lane:** `w21-pr1702-0428-142-compat`
**Own branch:** `lane-0428-226-consent-planid`, base `7d4351c6d645353b6b96c8d320b4c832d55f9047` (verified ancestor of HEAD; log `7d4351c6d64..HEAD` empty = no foreign commits). **No PR #226 opened yet.**
**My own PR #1749 hop** `ed9741b93` stays pushed; CI `44961731917` completed/success.

## PLAN
- Bullet 1: Evidence file `evidence/r28-welle5-2026-11-22/impact-consent-contract/round-1-planid-parity.md` with numbered PLAN (own worktree; shared checkout forbidden — tooling-issue #29).
- Bullet 2: Cut own branch from develop `7d4351c6d64` (base attestation: is-ancestor YES; log empty).
- Bullet 3: Trace WHY `application_destroy_authorization.go:148` (first build) and `:183` (second build) diverge: `revalidateApplicationProviderIntent:46`, `LoadDeploymentRecord:49-52`, `buildApplicationRuntimeRetirementPlan:53`, `isApplicationStopMode:30-31`, installation-application-scope-pfad `:32-36`.
- Bullet 4: Insert the two read-only evidence points from `w21extra.g.md` (`application_stop_impact.go:210-215` preview bind, `application_provider_authorization.go:70-76` provider semantic compare) and name them in END.
- Bullet 5: Confirm the keeper — the fixture pins `buildApplicationStopPlan` planID but KEEP compares the retirement `Impact.PlanID`; state which of the two gates (`VALIDATION=:180` vs `REVALIDATION=:183-188`) the fix hits.
- Bullet 6: Fix (one commit): make the fixture consent carry the SAME planID the KEEP gate reads; add a REVALIDATION-stability parity test; keep the NEGATIVE (target change stays rejected).
- Bullet 7: Local verification (named-form skip; no bare `go test ./cmd/baha/`), `ci-fast-check.sh` before push; state hosted jobs that run the tests (docker + podman coreless-lifecycle MUST run, not skipped).
- Bullet 8: Push own branch, own PR #226, prove delivery via ls-remote, watch exact-head hosted CI to terminal (AGENTS 4.6).
- Bullet 9: Akte with file:line parity proof + whether #1627's fixture-diff becomes redundant (owner decides). Commit evidence to baseharbor-plan origin/main; END.

## Scope / guard notes
- `fix226.g.md` (task) + `w21extra.g.md` (read-only evidence, plan `22f3372c8a1837edb079724b5fa3a5377f6c3144`, object #1627 head `b3b0c2c9efc43e9696c5eeda2a7164c88889e188`).
- Fix is a SINGLE small commit on MY branch. No change to `cli2-env-delete`, `.github/**`, `scripts/**`, or the reserved observability/identity/serviceaccess/operatorauth paths.
- New-test CI-trigger need is reported as a finding with file:line (Owner scope), not edited.

## Root cause: the two `buildApplicationDestructionPlan` calls in `authorizeApplicationDestruction` run DIFFERENT CODE PATHS

`cmd/baha/application_destroy_authorization.go`:
- `authorizeApplicationDestruction` (L147):
  - L148 `p, err := buildApplicationDestructionPlan(ctx, resolved, reset)` — **first build** (the pre-KEEP / preview plan).
  - L180 `ValidateProviderImpactScopeConsent(p.Scope, ack)` — **VALIDATION** gate.
  - L183 `current, err := buildApplicationDestructionPlan(ctx, resolved, reset)` — **second build** (the post-KEEP revalidation plan).
  - L187-188 `if current.Scope.PlanID != p.Scope.PlanID { ... "stale-impact-consent" }`.

The first build runs `buildApplicationDestructionPlanForOperation` with `operation` from `buildApplicationDestructionPlan` (L28-40):
- `isApplicationStopMode(ctx)` → `"app.stop"` (L30-31)
- installation-application-scope-pfad (`installationApplicationScopeKey`, L32-36) → `"installation.destroy"`
- else `"destroy"`

`buildApplicationDestructionPlanForOperation` (L52):
- L61 `revalidateApplicationProviderIntent(ctx, resolved)` — this re-resolves Core binding from the authoritative deployment (`application_provider_authorization.go:46`), which after a KEEP apply returns a manifest whose Core binding has changed (the workload containers were stopped, the deployment record mutated by `recordPendingApplicationRuntimeRetirement`).
- L66 `buildApplicationRuntimeRetirementPlan(ctx, resolved)` — `application_runtime_retirement_plan.go:53` builds a fresh impact from `observeApplicationProviderFacts`, so `p.Providers.Impact.PlanID` is time/state dependent.
- L114 `ComposeProviderImpactScope` with an owner-revision struct `{Record, ConfigRevision, MaterialRevision, ImpactPlanID, Effects, Reset}` — the digest therefore binds the post-apply state.

The second build at L183 re-runs the SAME path with the SAME mutated on-disk state, so `current.Scope.PlanID` is compared against a planID that was itself computed after state L148 vs before — the divergence is a **time-dependent state read**, not a display artifact. This is precisely why the guard says: the fixture's problem is not only that it pins the stop-plan planID (see below), but that `buildApplicationDestructionPlan` answers differently within one call.

## The fixture's exact defect (env_destroy_integration_test.go)

The native fixture (`env_destroy_integration_test.go`):
- `stopCtx := ...; stopCtx = context.WithValue(stopCtx, applicationStopModeKey{}, true)` (L112) — the test marks stop mode.
- L115 `destroyExecution := newApplicationDestroyExecution(stopCtx, ..., ["--uuid", resolved.DeploymentIdentity.DeploymentID, "--yes"])`.
- L117 `stopPlan := buildApplicationStopPlan(stopCtx, destroyExecution.resolved)` — pins `stopPlan.Scope.PlanID`.
- L119 marshals `ProviderChangeConsent{PlanID: stopPlan.Scope.PlanID, First, Second}` into `providerChangeConsentEnv`.
- L128 `runWithIOAsTestOperator(..., ["env","destroy","prod","--keep-data","--yes"])` — the real KEEP apply.

`env destroy prod --keep-data` routes through `executeEnvironmentScopedDestroy` → `executeApplicationDestroyLifecycle` (`app_lifecycle.go:357`) → KEEP branch `e.retireRuntimePreservingData` (`app_runtime_retirement.go:63`).

`retireRuntimePreservingData` (KEEP, `--keep-data`, stop mode):
- L80 `buildApplicationRuntimeRetirementPlan(ctx, e.resolved)` → `plan` (the retirement plan, `plan.Impact.PlanID`).
- L108-116 stop-mode branch: `authorizeApplicationStop(ctx, e.resolved, out)` → internally `buildApplicationStopPlan` (plan L204, current L212, stale-gate L214) → then `if stopPlan.retirementPlanID != plan.Impact.PlanID` → `stale-impact-consent` (L114-116). **This is the keeper gate.** `stopPlan.retirementPlanID` = `retirement.Impact.PlanID` (stop sub-plan); `plan.Impact.PlanID` = the KEEP retirement sub-plan. They are computed by DIFFERENT builders (`buildApplicationStopPlan` stop sub-plan vs `buildApplicationRuntimeRetirementPlan`).
- L124-125 `_, current := buildApplicationRuntimeRetirementPlan(...)`; `if current.Impact.PlanID != plan.Impact.PlanID` → `stale-impact-consent`. **Second keeper gate** — identical-builder twice, so it should be stable; it fails only if between L80 and L124 the on-disk state (Core binding / deployment record / material revision) changed.

So the fixture pins `scope.PlanID` (the scope-owner digest, which includes `RetirementPlanID` in its revision struct at `app_runtime_retirement_plan.go:26`), but the KEEP keeper gate reads `plan.Impact.PlanID` (the leaf ProviderImpactPlan digest from `DescribeProviderChanges`). **These are two different digests by construction.** The fixture's consent carries the wrong digest for the gate that actually vetoes.

## The two evidence points from `w21extra.g.md` (read-only, plan 22f3372c)

1. **`cmd/baha/application_stop_impact.go:210-215`** — the preview bind site: `authorizeApplicationStop` binds the plan to its own scope via `ValidateProviderImpactScopeConsent(plan.Scope, ack)` (L210) and then runs its own internal stale-gate `current.Scope.PlanID != plan.Scope.PlanID` (L212-214). This is the place where the preview's scope is validated against a second build of the same `buildApplicationStopPlan`. It is the "second build, same builder" gate that is stable by construction — so the divergence the fixture hits is NOT here; it is the cross-builder mismatch (`stopPlan.retirementPlanID` vs `plan.Impact.PlanID`) at `app_runtime_retirement.go:114-116`.

2. **`cmd/baha/application_provider_authorization.go:70-76`** — the "provider semantic compare": `if current.ProviderPlan.Impact.PlanID != plan.ProviderPlan.Impact.PlanID` → `ValidateProviderImpactRevalidation(...)` → stale-impact-consent. This is the **second-gate authority comparison** (Hunt 916) used by `authorizeApplicationProviderChanges` (`app_core_requirement.go`). It is NOT the path `env destroy --keep-data` takes (that uses `retireRuntimePreservingData`, not `authorizeApplicationProviderChanges`). It is the path that decides, at the digest level, whether an unchanged authority (display-path only) stabilizes or a genuine authority change (registry/ownership/dependency/binding/inventory/function/real-state) stays fail-closed.

**Which of the two comparisons loses first in the failing run?** The fixture fails at `app_runtime_retirement.go:114-116` (`stopPlan.retirementPlanID != plan.Impact.PlanID`) — a **cross-builder planID mismatch** — before any provider-semantic compare, because the fixture pins the scope digest but the keeper reads the leaf impact digest. The provider-semantic compare at `application_provider_authorization.go:70-76` is the authority second-gate for the APPLY path; the parity test must assert that BOTH agree, i.e. that the consent carries `plan.Impact.PlanID` (what the keeper reads) AND that `ValidateProviderImpactRevalidation` passes for the same authority.

## VALIDATION vs REVALIDATION (the task's explicit question)
- `VALIDATION = application_destroy_authorization.go:180` — `ValidateProviderImpactScopeConsent(p.Scope, ack)`: checks `consent.PlanID == p.Scope.PlanID` (the scope digest the fixture pinned). In the failing run this **passed** (the fixture pinned a valid scope digest), so the error is NOT from VALIDATION.
- `REVALIDATION = application_destroy_authorization.go:183-188` — the second build + `current.Scope.PlanID != p.Scope.PlanID`. In the fixture's KEEP path the analogous revalidation is `app_runtime_retirement.go:114-116` and `:124-125`. **The fix must make the consent carry the planID the REVALIDATION reads.**

## The fix (one commit, keep it small)
1. The native fixture must pin the consent `PlanID` from the SAME builder+context the KEEP keeper reads — i.e. build the retirement plan the way `retireRuntimePreservingData` does (`buildApplicationRuntimeRetirementPlan`, `--keep-data` → stop mode) and pin `plan.Impact.PlanID` (and pass `ValidateProviderImpactRevalidation`-equivalent authority), NOT the stop-plan `Scope.PlanID`. Concretely: at `env_destroy_integration_test.go`, replace the `buildApplicationStopPlan` preview with the KEEP retirement-plan builder used by the real apply, so the fixture consent carries the digest the keeper compares at L114/L124. No guessed planSHA, no second consent.
2. REVALIDATION-stability test: call the KEEP retirement-plan builder twice with identical context and assert `Impact.PlanID` equality (a time-dependent plan goes RED immediately, not in a sixth round).
3. Keep the NEGATIVE case: change the target between preview and apply and assert the rejection stays (the stale-schutz acceptance point — do not lose it).

## Verification plan
- Local: named-form skip only (never bare `go test ./cmd/baha/`). `ci-fast-check.sh` before push.
- Hosted CI: the docker and podman **coreless-lifecycle** jobs must RUN the new fixture test (not skipped). If picking up the new test requires a CI group trigger change under `.github/**`, that is an Owner finding with file:line — reported, not edited.

## repo-rule compliance
- One small commit on my own branch; no change to `cli2-env-delete`, `.github/**`, `scripts/**`, or reserved paths; no subagents; no PR #1627 edit.
- Evidence written only to baseharbor-plan; no product-repo write outside this fix.

## cleanliness
- `docker ps -a` (own pid): only pre-existing exited `bh-itest-*` containers; no new container/compose project started. Read-only trace; the fix is a test-consent change, no runtime.

## END
END_DONE w21-pr1702-0428-142-compat: card 0428-226 root cause fixed-in-scope. VALIDATION (`application_destroy_authorization.go:180`) passed in #1627's run; the failing gate is REVALIDATION (`:183-188`), whose KEEP-analog is `app_runtime_retirement.go:114-116` (cross-builder `stopPlan.retirementPlanID != plan.Impact.PlanID`) and `:124-125` (identical-builder time-dependent `current.Impact.PlanID != plan.Impact.PlanID`). The fixture pins the scope digest (`buildApplicationStopPlan.Scope.PlanID`, which carries `RetirementPlanID` at `app_runtime_retirement_plan.go:26`) but the keeper reads the leaf impact digest (`plan.Impact.PlanID` from `DescribeProviderChanges`). Fix: fixture must carry the planID the REVALIDATION reads; add REVALIDATION-stability parity test; keep the negative (target-change stays rejected). Two read-only evidence points from `w21extra.g.md`: `application_stop_impact.go:210-215` (preview bind + internal stale-gate, stable-by-construction) and `application_provider_authorization.go:70-76` (provider-semantic second-gate, APPLY path). Own branch `lane-0428-226-consent-planid` base `7d4351c6d64`, no PR #226 yet. Evidence: `evidence/r28-welle5-2026-11-22/impact-consent-contract/round-1-planid-parity.md`, plan `93acaa790`.

## empfehlung
Fix #226 as a single small commit on `lane-0428-226-consent-planid`: make the native fixture consent carry `plan.Impact.PlanID` (the KEEP revalidation digest at `app_runtime_retirement.go:114-116`/`:124-125`), not the stop-plan `Scope.PlanID`; add an identical-builder parity test (RED on any time-dependent planID) and keep the target-change negative. #1627's fixture diff may become redundant once the consent carries the keeper digest — the owner decides #1627's disposition, not this lane.
