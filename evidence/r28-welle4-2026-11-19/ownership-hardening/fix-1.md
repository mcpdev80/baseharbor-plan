# fix 0428-119 — consent identity bound to stable authority (red -> green)

- Task: t-20261118-ownership-stale-consent-hardening (0428-119), hunt-916 finding (`evidence/r28-welle4-2026-11-18/hunt-ownership/befund-1.md`, 8 windows / 6 coverage gaps, DIAG-/consent-race class)
- Lane: flash worker session (codeman 9a898351), branch `lane-0428-119-consent-hard`
- PR: #1690 https://github.com/mcpdev80/baseharbor/pull/1690 (base develop)
- Candidate head: `d94cc67d235b720079c8db8f070c97550f647535`
- Host: this machine is the coordinator/codeman server (NOT a test host). No containers, no compose projects were started by this lane (R1 respected). The four `bh-local-shared-*` containers observed on this host are pre-existing ambient infrastructure, untouched.

## PLAN

- Claim card t-20261118-ownership-stale-consent-hardening via plan.py; push claim. — done (claim commit c55a8b4f, planning origin/main)
- Reality check: `git ls-remote` develop; read hunt-916 akte; fresh worktree at /tmp/opencode/w119-consent-hard-wt. — done
- RED regression tests for the documented coverage gap C3 (stale impact-consent window). — done (red witnesses below)
- Hardening: consent/ownership check sharpened — PlanID digest bound to consent authority; revalidation second gate. No outcomeMatchesImpact change (116 pin), no cmd/baha guard-path beyond the single revalidation site. — done
- Affected unit tests + build + vet. — done
- Push branch, PR base develop, exact-head run to TERMINAL. — done (CI · Source & Quality run 44437197853 completed/success at exact head)
- Publish this akte to baseharbor-plan origin/main + END. — final step

## Planning repo witness (wrong-zone check)

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` -> /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
- `git remote get-url origin` -> https://github.com/mcpdev80/baseharbor-plan.git

## Base attestation (branch provenance)

- Product truth witnesses (measured, `git ls-remote origin develop` in a fresh clone under /tmp/opencode):
  - first cut: develop == `8dccd4fe1a52bbcc61c67f7809079f33b8040d64` (worktree HEAD at clone time).
  - coordinator base-move directive 2026-11-19: develop advanced to `9a37b4bc6ba372af517ea00b8d93c2085a2d4f95` (PR #1663 merged). Ancestry: `git merge-base --is-ancestor 8dccd4fe1 9a37b4bc6` -> YES. Branch fast-forward-merged onto the new base before any commit/push.
  - final pre-push: develop advanced again to `7d343836447f976ec613fa4ae1cb09afcabbbbe0`. The branch merged onto it, one own commit on top:
    - `git merge-base --is-ancestor 7d343836447f976ec613fa4ae1cb09afcabbbbe0 HEAD` -> YES
    - `git log --oneline origin/develop..HEAD` -> `d94cc67d fix(0428-119): bind consent identity to stable authority, not observation churn` — ONLY this own commit (no foreign candidate carried).
- One candidate per chain: `lane-0428-119-consent-hard` is the only branch pushed for this card; `git ls-remote origin 'refs/heads/lane-0428-119*'` before push showed nothing, after push shows exactly `d94cc67d235b720079c8db8f070c97550f647535`.
- Ownership note (precedent recorded with coordinator 2026-11-19): the card's owner field shows `w99-0428-119 (codeman 9a898351)` from coordinator commit 63ef1961 — this is bookkeeping bridging for the plan.py-claim empty-owner defect and points at THIS lane's own session; my published claim is c55a8b4f. No second 119 lane exists.

## Mechanism (from the akte, confirmed in source at the tested bases)

- A-F1/B2 chain: an adapter error folds into `ProviderUnverifiable` (cmd/baha/app_core_requirement.go:126-128 Layer-1 default), the union preserves + `Complete=false` (internal/application/provider_union.go:159-168), and BOTH the fact `State` token and the derived observation `Revision` ride into the PlanID digest (internal/application/provider_change_digest.go:15-45, provider_change_plan.go). The post-consent revalidation (cmd/baha/application_provider_authorization.go:57) compared the RAW plan-id string, so a classifier flap or revision re-derivation between plan and re-plan livelocked every apply on `stale-impact-consent`.
- C3 gap: no unit simulated "same state, second observation errored" at the digest/revalidation level — only changed-state fixtures.

## Fix

1. `internal/application/provider_change_plan.go` — the digest input is canonicalized to the CONSENT AUTHORITY view before hashing:
   - `consentAuthorityDigestFacts`: a fact whose classification folded into `unverifiable` carries no state token; the concrete state the observation record proved replaces it, and only a provider with NO record keeps the unknown marker.
   - `consentAuthorityNormalize`: the plan-body Before/After realizations receive the same fold, so digest and frozen surface agree.
   - `consentAuthorityDependenciesKnown`: knowledge depends on what was proven (observation materials/inventory), not on nil-versus-empty normalization order.
   - `Plan.Authority` freezes the `ConsentAuthority` equivalence surface at computation time.
2. `internal/application/provider_consent_authority.go` (new) — `ConsentAuthority` (StableCore = canonicalized inputs + consequence projection with countdown samples stripped and classification-derived notices folded out; Samples = volatile knowledge folds, never marshaled into comparisons), `BuildConsentAuthority`, `ProviderImpactPlansConsentEquivalent`, `ValidateProviderImpactRevalidation` (exact plan-id first; frozen surfaces as second gate; fail-closed when a plan carries no surface).
3. `cmd/baha/application_provider_authorization.go` — the post-consent revalidation compares via `ValidateProviderImpactRevalidation`; genuine divergence keeps the exact fail-closed path and the existing diagnostic line.
4. `internal/application/provider_change_types.go` — internal `Authority *ConsentAuthority` field (unexported-typed, never serialized; PlanID wire semantics unchanged).

Conservative by construction: countdown samples remain excluded (existing digest rule); observation revision and wall-clock churn leave the core unchanged; registry content, ownership, dependency graph, bindings, material inventory/evidence, consumer functions, absolute validity and REAL runtime state changes keep plans unequal and consent stale.

- Pins honored: `outcomeMatchesImpact` (provider_change_result.go) untouched — 0428-116 semantics pin holds (non-continuation extra edge stays applied). `cmd/baha` guard paths untouched (0428-118 territory). No `.github/**` changes.

## Red -> green witnesses (116-convention: revision label + porcelain at timepoint)

- State RED — tests only, no source change, at merged develop `9a37b4bc6ba372af517ea00b8d93c2085a2d4f95`:
  - `git rev-parse HEAD`: `9a37b4bc6ba372af517ea00b8d93c2085a2d4f95`
  - `git status --porcelain`: `?? internal/application/provider_consent_oscillation_test.go`
  - command: `go test ./internal/application/ -run 'TestConsentSurvives' -count=1 -v`
  - output:
    - `--- FAIL: TestConsentSurvivesUnverifiableStateOscillation` — `provider_consent_oscillation_test.go: A-F1 livelock: transient unverifiable classification of unchanged authority invalidated informed consent: provider change: stale-impact-consent`
    - `--- PASS: TestConsentSurvivesObservationClockChurn` (the clock-window half was already digest-excluded upstream; retained as a boundary pin)
  - The equivalence-surface test `TestProviderImpactPlansConsentEquivalentStabilizesClassification` initially failed with `consent authority changed on a pure classification flip` before the fold was placed at the digest — both failure modes documented the window.
- State GREEN — candidate head `d94cc67d235b720079c8db8f070c97550f647535`, clean tree:
  - `git rev-parse HEAD`: `d94cc67d235b720079c8db8f070c97550f647535`
  - `git status --porcelain`: (empty)
  - command: `go test ./internal/application/ -run 'TestConsentSurvives|TestProviderImpactPlansConsentEquivalentStabilizesClassification' -count=1 -v` ->
    - `--- PASS: TestProviderImpactPlansConsentEquivalentStabilizesClassification`
    - `--- PASS: TestConsentSurvivesUnverifiableStateOscillation`
    - `--- PASS: TestConsentSurvivesObservationClockChurn`
    - `ok github.com/mcpdev80/baseharbor/internal/application 0.022s`
  - `go test ./internal/application/ -count=1` (full package) -> `ok ... 11.7s`
  - `go test ./cmd/baha/ -run 'TestAppEditApply|TestAppMachine|TestNoImpactPlan|TestRetirement|TestExternalProvider|TestProviderChange|TestCapabilityRemoval|TestTargetDefinition|TestAppRegistryPoison' -count=1` -> `ok ... 22.3s`
  - `go build ./...` -> OK; `go vet ./internal/application/ ./cmd/baha/` -> clean; `gofmt -l cmd/baha internal/application` -> clean; `go build -o /var/tmp/w119-baha ./cmd/baha` -> OK
  - note: the heavyweight `go test ./cmd/baha` FULL suite additionally runs host-integration lifecycles that need isolated runtimes (e.g. TestAppEditCommandCompleteProviderEditRunsRealLifecycle requires a protected Core in a native network); those are native-gate scope, not this lane's R1 host. They pass in the CI cli shards (all `PR · Go unit · cli-N` SUCCESS).
- Existing-behavior pins verified green at the candidate: `TestProviderImpactStaleApprovalAndOwnership` (validator identity stays raw plan-id), `TestMaterialValidityWindowBindsTransitionsWithoutCountdownChurn`, `TestProviderImpactIntentRemovalAndSamplingDoNotInventDemandOrStaleConsent`, `TestAppEditApplyConfirmedConsentSurfaceIgnoresOnlyEvidenceAndIdentity`, `TestAppMachineAdaptersStalePlanConsentAndCancellation`, `TestAppEditApplyStalePlanAndWrongConsentWriteNothing`.

## CI (eigenes-Run-Pflicht)

- Exact-head run: `CI · Source & Quality` run 44437197853 at head `d94cc67d235b720079c8db8f070c97550f647535` — TERMINAL `completed/success` (watched to completion by this lane).
- Job outcomes: Workflow policy, Trusted Plan, Source format, Native gate plan, Focused Python, Validation go-vet, go-build all SUCCESS; Go unit shards `packages`, `owner`, `cli-0`…`cli-3` SUCCESS; runtime/HA/release matrix jobs SKIPPED by the ordinary PR selection policy (no native-gate trigger on this path).
- PR #1690 rollup green; `gh pr view --json headRefOid,state` -> `d94cc67d… OPEN`.
- New tests are plain `go test ./internal/application/` members — executed by the CI groups `PR · Go unit · packages` (and the cli/owner shards) on every pull_request touching this package. No `.github/**` change needed (no Owner-scope finding).

## Scope decisions (contract calls made in-lane)

- The card's contract question ("whether unverifiable should FAIL CLOSED with a distinct error") was decided AGAINST a new error code: fail-closing on every unverifiable sample would break the developer-choice rule (`Complete=false never vetoes an informed developer's choice`, provider_change_consent.go) and turn livelock into deadlock for intermittently flaky observers. The hardening removes the churn from the consent identity itself (authority fold), closing B1/B2 without weakening any fail-closed check; genuine unknowns still surface via `Complete=false` + two-stage attention exactly as before. Rationale here + review on PR #1690.
- No shared helper and no `.github` change was needed, so the mission STOP condition did not apply.

## repo-rule compliance

- plan -> preflight -> apply -> verify preserved; this is a planning/authorization-semantics change inside the existing domain (no new lifecycle stage).
- CLI, JSON and MCP share domain semantics: all transports reach `authorizeApplicationProviderChanges`, so the single revalidation-site change covers them; machine adapters keep their raw plan-revision comparisons (transport contract unaffected).
- Mutations still refuse on any genuine authority divergence (fail closed); consent/confirmation code paths untouched.
- Evidence lives only in baseharbor-plan (this file); no product-repo evidence artifacts; no main-branch writes to product repos.

## Cleanliness

- No containers, compose projects, networks or volumes were created by this lane; nothing to bring down (R1: nothing started on this host). `ps`-witness: the only containers on this host are the pre-existing `bh-local-shared-*` ambient set.
- Worktree /tmp/opencode/w119-consent-hard-wt owns the candidate until merge; test residue (probe tests, runtime.env dirs created by unit runs inside the worktree, stray binary) removed before commit; `git status --porcelain` clean at the candidate.
- Scratch confined to /var/tmp and /tmp/opencode; nothing created in /home/marcel/dev/baseharbor-ecosystem outside the planning checkout's tracked paths.
- cleanliness: no lane-owned compose projects, no stray files in /home/marcel/dev/baseharbor-ecosystem; only evidence in baseharbor-plan.

## END

END_DONE mission-119-consent-hardening.md: candidate `d94cc67d235b720079c8db8f070c97550f647535` on PR #1690 (base develop 7d3438364), CI · Source & Quality run 44437197853 completed/success at exact head; red->green regression in internal/application (C3 window pinned both directions); 116/118 pins honored; evidence published to origin/main (witness below).
