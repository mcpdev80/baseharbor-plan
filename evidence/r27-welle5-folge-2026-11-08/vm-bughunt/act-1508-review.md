# CODEX-REVIEW 0427-178 — PR #1508

## PLAN

1. Verify the exact PR head, develop base, ancestry, and hosted run.
2. Inspect the production batching path and the N=1/N=10 regression counter.
3. Check that per-deployment verification remains active and that 174/144 list classifications are covered.
4. Record a SHA-specific verdict and actionable correction recipe.
5. Publish this review to baseharbor-plan origin/main and report the plan commit.

## Candidate and hosted evidence

- Verdict target: PR #1508, head `dbb1df08069424265830a397ab41ee882fa36830`.
- Develop fetched from GitHub: `b3a8042d18ea60f162a32a51df34a499cad6a237`; `git merge-base --is-ancestor b3a8042d18ea60f162a32a51df34a499cad6a237 dbb1df08069424265830a397ab41ee882fa36830` returned 0.
- `git ls-remote` confirmed `refs/heads/develop` at `b3a8042d18ea60f162a32a51df34a499cad6a237` and `refs/pull/1508/head` at `dbb1df08069424265830a397ab41ee882fa36830`.
- Hosted run `42572608265` is terminal `completed/success` on the exact head. `PR Selected Checks` passed (job `129014172909`); `PR · Validation · deployment-package-tests` passed (job `129013376045`); `cli-guided-tests`, `cli-build`, `cli-vet`, `source-contracts`, `source format`, and `Focused Python` passed.
- Native Keycloak/Core, native destroy-retry, Selected Runtime, Targeted HA, and other non-selected jobs report `skipping`; these are not counted as passes. The deployment package regression is covered by the `pull_request` trigger for `develop`: `ci.yml` dispatches `deployment-package-tests` through the trusted validation runner, and `scripts/pr-check-runner.py` maps it to `go test ./internal/deployment/...`.
- Product diff against develop is limited to five `internal/deployment/*` files. No workflow files changed.
- Local focused check on the exact head: `go test ./internal/deployment -run 'Test(ListOwnerVerificationBatchedOncePerTarget|ListOwnerVerificationPreservesFailClosed|BatchCacheNeverSearchesDeploymentOwnership)$' -count=1` passed.

## Findings

### F1 — correction required: best-effort listing labels every owner failure as missing

`internal/deployment/deployment_list_owner_batch.go:123-126` wraps every `VerifyDeploymentOwnerBatched` error as `DeploymentRecordStateError{Kind: "missing"}`. That includes a tenant/access-scope denial returned from `resolveOwnerLoad`, as well as a foreign-owner error. The underlying error remains unwrap-able, but the list's public state classification says `missing` for all three situations. The new `TestListOwnerVerificationPreservesFailClosed` at `internal/deployment/deployment_list_owner_scale_test.go:103-149` covers only missing and foreign in the non-best-effort list; it does not prove the access-denied path remains distinct in the best-effort list fixture.

### F2 — correction required: required classification regression is incomplete

The scale fixture asserts `batch.loads == 1` for N=1, 5, and 10 (`deployment_list_owner_scale_test.go:40-48, 84-94`), and establishes the ordinary installation-load bound. The cache stores the verified installation only (`deployment_list_owner_batch.go:24-35, 48-67`), while `VerifyDeploymentOwnerBatched` re-runs the per-deployment directory conclusion for each record (`:81-95`); this supports the no-blind-cache requirement for ordinary Core-owned targets. However, the new regression contains no three-way list fixture for the 0427-174 access-denied, foreign, and missing outcomes. Its comments promise preservation of cards 174/144, but the actual new assertions cover only missing and foreign (`deployment_list_owner_scale_test.go:97-149`). The 0427-144 foreign-record-tolerance behavior is not exercised by this new scale fixture either.

The count is a direct counter increment immediately after `coreinstallation.Load` in `resolveOwnerLoad` (`deployment_store.go:169-173`), so it verifies the implementation's authoritative installation-file load count in the production list helper, rather than measuring wall time. It does not count tenant resolver invocations: the authorized Coreless path returns a nil installation, so `ownerBatch.loadOwner` has no cached owner to reuse and `resolveOwnerLoad` re-enters `TenantOwnerResolver` for each record (`deployment_store.go:142-160`; `deployment_list_owner_batch.go:57-60`). Whether that resolver work belongs in the acceptance's bounded engine-call metric needs to be made explicit in the regression. Do not cache authorization conclusions unless their validity is safe across the list operation.

## Verdict

**KORREKTUR** for candidate `dbb1df08069424265830a397ab41ee882fa36830`.

The normal Core installation load is batched and the focused CI job actually ran successfully on the exact head. Per-record directory ownership checks remain in the loop, so the implementation does not cache a per-deployment allow/deny result. Acceptance is still incomplete because best-effort warnings collapse access, foreign, and missing into the `missing` state label, and the new list regression does not distinguish all three 174 outcomes or demonstrate 144 foreign-record tolerance. The owner-load counter also does not observe tenant-resolver calls, leaving the measurement boundary ambiguous for Coreless targets.

## Actionable correction recipe

- File: `internal/deployment/deployment_list_owner_batch.go`, around lines 123-126. Preserve a truthful owner-failure classification when building best-effort warnings. Do not map access-denied or foreign-owner failures to `Kind: "missing"`; preserve the original typed cause and its `errors.Is`/`errors.As` identity.
- File: `internal/deployment/deployment_list_owner_scale_test.go`. Add a public batched-list fixture covering missing owner, foreign owner, and access-denied tenant scope. Assert each result's state kind and typed cause separately, and assert no protected record is returned. Add a foreign-record-tolerance control for the 144 behavior so batching cannot silently change that contract.
- File: `internal/deployment/deployment_list_owner_scale_test.go` and the narrow owner-resolution seam if required. Make the bounded counter observe actual authoritative owner-resolution work for both Core-owned and Coreless tenant fixtures. Include N=1 and N=10 and prove the count remains bounded without caching a stale authorization decision; if tenant authorization must still be checked per record, state and test the correct bound instead of claiming once-per-target engine work.
- Required test: focused deployment package test locally, then confirm the new tests execute in hosted `PR · Validation · deployment-package-tests` on the corrected exact head. That job is selected for `pull_request` targeting `develop` through the existing CI runner; no workflow edit is requested here.
- Stop criterion: do not accept until exact-head hosted `deployment-package-tests` and `PR Selected Checks` are terminal success, the list fixture distinguishes access-denied/foreign/missing while retaining 144 tolerance, and the measured call bound covers the owner-resolution paths included by the card.

## Evidence source and limitation

The card's linked hunt dossier `evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp4.md` documents BF-08 (per-record `coreinstallation.Load`, lock/stat/read) and the acceptance. The lane's `round-1.md` was not present at the initially named subdirectory; after syncing planning `origin/main`, the published dossier was found at `evidence/0427-178-listscale-owner-check-scaling/round-1.md` and reviewed. The dossier describes the implementation intent but is not a substitute for the source and exact-head run checks above.

## repo-rule compliance

- Review-only: no product files or workflow files changed.
- Candidate remained `dbb1df08069424265830a397ab41ee882fa36830` before and after review.
- Evidence is stored only in baseharbor-plan.
- No containers or compose projects were started.

END 0427-178 REVIEW — KORREKTUR; candidate `dbb1df08069424265830a397ab41ee882fa36830`.
