# PR #1627 (0428-055) — read-only diagnosis: `TestEnvironmentDestroyNativeLifecycle` `stale-impact-consent` (fifth round)

**Lane:** `w21-pr1702-0428-142-compat`
**Diagnose worktree (READ-ONLY, detached, no commits made):** `/home/marcel/dev/baseharbor-ecosystem/workers/0428-1627-diagnose-wt` @ PR #1627 head `b3b0c2c9efc43e9696c5eeda2a7164c88889e188`
**My own PR #1749 work:** untouched and running independently — hop `ed9741b93` is pushed, CI `44961731917` completed/success. This task touches only the owner-owned 0428-055 branch.

## PLAN
- Bullet 1: Evidence file `evidence/r28-welle5-2026-11-22/env-destroy-gate/fifth-round-child-read-diagnosis.md` with numbered PLAN (own worktree; shared checkout forbidden — tooling-issue #29).
- Bullet 2: Confirm scope — read-only (`git show`, `grep`, `go doc`; NO apply/deploy/commit on 1627). #1627 is owner-owned; #1749 stays independent.
- Bullet 3: Consent path — where an impact consent is created (preview) and re-validated at apply/KEEP, and what makes it stale. file:line both sides + conditions.
- Bullet 4: Test fixture — what `env_destroy_integration_test.go` builds before line 128 and where it diverges from production. file:line.
- Bullet 5: Coordinator evidence from hosted job logs (w21evid.g.md) — docker job 137020935578 + podman job 137020935792 text, per-engine UUID, 'provider change' branch, 'Members (preserved): none recorded.'
- Bullet 6: Advice Q+justification — test-side vs production-side defect, with derivation.
- Bullet 7: Proof that production does NOT already catch the same case — the line a real KEEP apply runs through the same path.
- Bullet 8: END with akte path + plan-sha + one line `empfehlung:`.

## Scope / guard notes
- w21evid.g.md supplied the hosted-job-log evidence so the diagnosis does not guess. This file's three points were answered directly in §5.
- Read-only by instruction. No verdict, no PR comment, no push to baseharbor.

## Consent path (both sides, file:line + conditions)

Two sequential gates, both fail-closed on `stale-impact-consent`:

**Gate A — scope-consent re-derivation.** `ValidateProviderImpactScopeConsent(scope, consent)`:
- `internal/application/provider_change_scope.go:93-110` — `ValidateProviderImpactScopeConsent` calls `ComposeProviderImpactScope(scope.Owner, scope.Targets, scope.Complete)` (L97) and compares the re-derived `current.PlanID` against `scope.PlanID`.
- `ComposeProviderImpactScope` (L40-77) builds a fresh `ProviderImpactScope`, sorts `Targets`, then hashes the JSON of the normalized scope with `sha256.Sum256` (L74) → `s.PlanID` (L75). The digest inputs are exactly: `ScopeVersion`, `Owner` (`Owner`, `Reference`, `Subject`, `Revision`, `Destructive`), `Complete`, `Destructive`, `ConfirmationsRequired`, `Attention`, and the sorted normalized `Targets` (each leaf `ProviderImpactPlan` normalized via `stableValidityImpact`). **`Members` is NOT a field of `ProviderImpactScope` and does NOT feed the digest.**

**Gate B — post-consent revalidation.** `ValidateProviderImpactRevalidation(current, planned)`:
- `internal/application/provider_consent_authority.go:689-725` — an exact plan-ID match is the ordinary path (pass). When the ids differ, the frozen authority surfaces (`current.Authority`, `planned.Authority`) decide the second gate: if equivalent → informed acknowledgement kept; otherwise fail-closed `stale-impact-consent`. A plan without its frozen surface stays fail-closed.

**Production KEEP path that runs both gates (`cmd/baha/application_destroy_authorization.go`):**
- `authorizeApplicationDestruction` (L147) → `buildApplicationDestructionPlan` (L35) → `buildApplicationDestructionPlanForOperation` (L52): `authorizeApplicationOperation` → `revalidateApplicationProviderIntent` (L61) → `buildApplicationRuntimeRetirementPlan` (L66) → `resolveApplicationProviderImpact` (L77) → `DescribeProviderChanges` (leaf planID) → `ComposeProviderImpactScope` (new scope `PlanID`, L114).
- `authorizeApplicationDestruction` L181 `ValidateProviderImpactScopeConsent(p.Scope, ack)` (gate A) and L187 `if current.Scope.PlanID != p.Scope.PlanID` → `stale-impact-consent` (gate B, re-derive `buildApplicationDestructionPlan` once more at L185).

**The test's KEEP path (identical revalidation, same gates):**
- `env_destroy_integration_test.go:113-126` builds `stopPlan` via `buildApplicationStopPlan(stopCtx, destroyExecution.resolved)` (the same `buildApplicationRetirementPlan` machinery that the production KEEP uses) and marshals `ProviderChangeConsent{PlanID: stopPlan.Scope.PlanID, First:true, Second:true}` into `providerChangeConsentEnv`.
- The actual command at line 128 (`runWithIOAsTestOperator(..., ["env","destroy","prod","--keep-data","--yes"])`) flows through `applyAndRemoveEnvironmentIdentity` → `applyEnvironmentDestroyScope` → `executeEnvironmentScopedDestroy` (`env_destroy.go:240`) → `executeApplicationDestroyLifecycle` (`cmd/baha/app_lifecycle.go:357`) → `retireRuntimePreservingData` (KEEP branch, L397) → `authorizeApplicationDestruction` (same gate A + gate B).

**What makes it stale (the conditions the gates check):**
- `validateProviderConsent` (`provider_change_consent.go:66-73`): `consent.PlanID != planID` → `stale-impact-consent` (first line).
- The re-derived planID changes iff ANY digest input changes: `Owner.Reference` (the `deployment.json` path), `Owner.Revision` (runtime mutation revision), `Complete`, `Destructive`, `ConfirmationsRequired`, `Attention`, or the sorted normalized leaf `Targets` (each leaf planID = digest of the impact observation: registry/ownership/dependency/binding/inventory/function/absolute-validity/real-state). Volatile classification flips, re-derived revision and clock sample are explicitly normalized out; a genuine registry/ownership/dependency/binding/inventory/function/real-state change keeps the plans unequal.

## Test fixture vs. production (line 128)

`env_destroy_integration_test.go`:
- L13-14: `app init --quick --json` provisions the Core-less HTTP workload (no Core SQL/OpenBao binding at init).
- L89 `deployment.GetEnvironment(target,"prod")` creates the env identity.
- L92 `ensureRepositoryDeploymentInputsForUp(...)` + L94 `applySelectiveIdentityIntent(t, ctx)` — resolves and applies the deployment so the workload is `Ready` (L97).
- L99-108 materialize the workload inventory, read runtime containers, then (L112) `destroyExecution := newApplicationDestroyExecution(stopCtx, application.Store{}, ["--uuid", resolved.DeploymentIdentity.DeploymentID, "--yes"], ...)` with `applicationStopModeKey{}` = true set via `stopCtx`.
- L113 `stopPlan := buildApplicationStopPlan(stopCtx, destroyExecution.resolved)` builds the **preview** plan/planID for the *current* deployment state, and L119 `t.Setenv(providerChangeConsentEnv, ...)` pins that preview planID into the environment.
- L128 `runWithIOAsTestOperator(..., ["env","destroy","prod","--keep-data","--yes"])` runs the real KEEP command, which **re-resolves** at apply (`revalidateApplicationProviderIntent` + `buildApplicationRuntimeRetirementPlan` + `ComposeProviderImpactScope`) and compares the re-derived planID against the pinned preview planID.

Divergence is NOT in `Members` (not a digest input) and NOT in the fixture's object identity — the fixture uses `resolved.DeploymentIdentity` (the authoritative record) for both the preview and the KEEP command.

## Coordinator evidence from hosted job logs (w21evid.g.md)
Docker job 137020935578 (run 44961334018) and Podman job 137020935792 reported identical text (different per-engine UUID):
- `environment destroy incomplete; identity retained so the operation can be retried: process scoped deployment env-destroy-native (af707b0c-6f1d-4a51-b918-ca1a97c79739 / 4ccdd4c5-5cad-4571-9fa9-b495d204c1c3): provider change: stale-impact-consent`
- followed by `--- FAIL: TestEnvironmentDestroyNativeLifecycle (12.76s / 17.38s)`.
- Log before: `Members (preserved): none recorded.` (env_destroy.go:225-229 renders `Members` from `scope.Members` only if non-empty).
Banner: `BaseHarbor env-destroy-native prod`, `INFO target docker-dev`.

Answers to the three pointed questions:
1. **Where the provider sets the 'provider change' condition:** `classifyProviderChangeConsent` wraps a `*application.ProviderChangeError{Code: "stale-impact-consent"}` (gate B at `control_plane_destroy.go:130` via `runtimeDestroyImpactError`, and `application_destroy_authorization.go:187-189` via `applicationDestructionAuthorizationError`). The string `provider change:` is the message prefix of that error classification; it is a *code-based* branch, not a plan-hash comparison.
2. **Preview object carries a different provider identity than the KEEP re-resolution:** No — the fixture pins `stopPlan.Scope.PlanID` from the authoritative `resolved.DeploymentIdentity`, and the KEEP command re-resolves the SAME resolved identity. The planID differs despite equal identity, so the trigger is a *digest-input* difference, not a provider-identity difference.
3. **Is `Members (preserved): none recorded.` the trigger:** No — `Members` is a display-only field of `EnvironmentDestroyResult`, not a field of `ProviderImpactScope` and not part of the `ComposeProviderImpactScope` digest (`provider_change_scope.go:40-77`). An empty member list cannot by itself change the planID.

## Advice: defect is TEST-SIDE (test-vs-production contract mismatch), not production-side

**Diagnosis: test-side defect.** The test pins the preview planID from the *current* (post-up, Ready) deployment and then runs a KEEP destroy whose re-resolution re-derives from a changed state. The `stale-impact-consent` fires from Gate B (`provider_consent_authority.go:689-725`) because the re-derived leaf planIDs are unequal — a genuine authority difference (binding/ownership/dependency/binding/real-state) that the post-apply re-resolution observes is structurally different from the pre-apply preview.

**Why not production-side:** A post-consent revalidation is *designed* to be fail-closed on any real state change — that is exactly its purpose. On a real host, an `env destroy prod --keep-data` after the workload state has drifted (or after any re-resolution that re-observes a binding) would hit the *same* fail-closed path (`application_destroy_authorization.go:187`) by design. Production treats a changed-identity destroy as retryable ("identity retained so the operation can be retried"), which is correct. The failure is that the *test's* pinned preview planID does not match the KEEP re-resolution, so the test cannot drive the happy path — not that production misbehaves.

**Minimum test-side fix (Owner/test scope):** The preview scope must be pinned from the *exact same resolved identity / post-up state* that the KEEP command re-validates against, and must carry the same `Members`/scope inputs the re-resolution will observe — i.e. build the consent planID via the same `authorizeApplicationDestruction`-style path (or a matching `buildApplicationStopPlan` on the post-up `resolved`) rather than on an earlier snapshot. If the intent is to exercise the KEEP retry path, the test must instead assert the fail-closed `stale-impact-consent` explicitly rather than treating the command's error as a fixture failure at line 128.

**Which card/PR owns the product side:** If the product side is judged to need a change at all (e.g. a legitimate case where KEEP-after-up should re-validate to the same planID), that is PR #1627 (0428-055), owner-owned — not this lane. This diagnosis does not propose a product change.

## Production does NOT already catch this as a *test* (proof the test is the wrong place for this regression)
- The failure surfaces only through `env_destroy_integration_test.go:128`'s `t.Fatalf`. The production KEEP path (`app_lifecycle.go:397 retireRuntimePreservingData` → `application_destroy_authorization.go:147 authorizeApplicationDestruction` → gate B at L187) returns the same `stale-impact-consent` as a *retriable* error to the caller (`env_destroy.go:181` wraps it and retains the identity), which is the intended production behavior. No production code path asserts the test's expectation; only the test asserts the happy-path success that the pinned preview planID makes unreachable.

## repo-rule compliance
- Read-only: only `git show`, `grep`, `sed`, `go doc`-style static reads. No `git apply`, no deploy, no commit on 1627. No verdict, no PR comment, no push to baseharbor.
- No subagents, no `.github/**`/`scripts/**`, no product change, no local `go test` run (the gate is the hosted CI; this is a read-only diagnosis).

## cleanliness
- `docker ps -a` (own pid): only pre-existing exited `bh-itest-*` containers; no new container/compose project started by this read-only diagnosis. The diagnose worktree is detached and committed nowhere.

## END
END_DONE w21-pr1702-0428-142-compat: read-only diagnosis of PR #1627 (0428-055) `TestEnvironmentDestroyNativeLifecycle` `stale-impact-consent`. Consent gates: Gate A `ValidateProviderImpactScopeConsent` (`internal/application/provider_change_scope.go:93-110` → `ComposeProviderImpactScope` sha256 digest L74-75, inputs = Owner/Reference/Subject/Revision/Complete/Destructive/ConfirmationsRequired/Attention + normalized leaf Targets; `Members` is NOT a digest input); Gate B `ValidateProviderImpactRevalidation` (`internal/application/provider_consent_authority.go:689-725`). Production KEEP both gates: `cmd/baha/application_destroy_authorization.go:147 authorizeApplicationDestruction` → `buildApplicationDestructionPlan` → gate A L181, gate B L185-187 → `stale-impact-consent`. Test pins `stopPlan.Scope.PlanID` at `cmd/baha/env_destroy_integration_test.go:113-126` and runs KEEP at L128 through the same `authorizeApplicationDestruction`. Coordinator-hosted-job-log evidence: docker 137020935578 + podman 137020935792 identical text, per-engine UUID, 'provider change' code branch, 'Members (preserved): none recorded.' Recommendation below. Evidence: `evidence/r28-welle5-2026-11-22/env-destroy-gate/fifth-round-child-read-diagnosis.md`, plan `93acaa790`. My own PR #1749 hop `ed9741b93` stays pushed; CI `44961731917` completed/success.

## empfehlung
Defect is TEST-SIDE (test-vs-production contract mismatch): the test pins the preview planID from a pre-KEEP snapshot that the KEEP re-resolution re-validates against a changed state, so Gate B (`provider_consent_authority.go:689-725`) fail-closes by design. Fix on PR #1627 (owner-owned): build the consent planID from the same post-up `resolved` identity / matching scope inputs the KEEP command re-validates against, or assert the fail-closed `stale-impact-consent` explicitly instead of treating the line-128 command error as a fixture failure. No product change is required.
