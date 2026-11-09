# CODEX-REVIEW 0427-178 — PR #1509

## PLAN

1. Pin the live PR head, base head, ancestry, and hosted check run.
2. Inspect the exact diff and owner batching/classification paths against the 0427-178 acceptance points.
3. Confirm regression coverage and CI selection; run the focused deployment package tests locally.
4. Record the verdict, evidence, and any landing conditions; publish this review to planning origin/main.

## Candidate and remote witnesses

- Repository: `mcpdev80/baseharbor`.
- PR #1509 head: `03d144134292d4eae53c966c9f578bbd068d8358` (`refs/pull/1509/head`).
- Develop head fetched: `b3a8042d18ea60f162a32a51df34a499cad6a237` (`refs/heads/develop`).
- Replaced PR #1508 head: `dbb1df08069424265830a397ab41ee882fa36830` (`refs/pull/1508/head`); PR #1508 is closed.
- Ancestry: `git merge-base --is-ancestor b3a8042d18ea60f162a32a51df34a499cad6a237 03d144134292d4eae53c966c9f578bbd068d8358` returned 0. The same check for #1508 head against #1509 returned 0.
- Exact-head hosted run 42580378234: `completed`, `success`, head SHA `03d144134292d4eae53c966c9f578bbd068d8358`.
- `PR Selected Checks` passed (job 129037957651); `deployment-package-tests` passed (job 129037453848). The CLI build/guided/vet, source-contract, focused Python, source-format, and workflow-policy checks also passed. Unrelated native/runtime and consumer jobs reported skipped and are not counted as passing evidence.

## Review findings

### Best-effort classification remains truthful

`internal/deployment/deployment_list_owner_batch.go` classifies `ErrDeploymentOwnerMissing` as `missing`, `ErrDeploymentOwnerForeign` as `foreign`, and other typed failures as `access` in `classifyOwnerFailure`. The best-effort warning wraps the original error in `DeploymentRecordStateError`, preserving its cause for `errors.Is`. The regression `TestBatchedListClassifiesAccessForeignMissing` exercises all three classifications and checks preservation of the access error. `TestBatchedListForeignToleranceControl` separately confirms the foreign-owner path produces a `foreign` warning and does not return the protected record.

### The scaling witness measures actual owner-resolution work

The batch counter increments immediately after `coreinstallation.Load(targetRoot)` in `internal/deployment/deployment_store.go`, so the test observes authoritative installation reads, rather than timing or a mock estimate. `TestListOwnerVerificationBatchedOncePerTarget` checks N=1, 5, and 10 records with one load per target. `TestBatchedListOncePerTargetResolverBound` exercises the resolver-denied production path and likewise asserts one authoritative load for multiple records. This demonstrates the claimed bound on target-owner resolution.

### Batching does not reuse a per-record authorization result

`ownerBatch` retains only the resolved, loan-checked Core installation for one target. It does not cache a deployment-specific allow/deny result. `VerifyDeploymentOwnerBatched` invokes `verifyDeploymentOwnerAgainstInstallation` for each deployment ID, and `listDeploymentRecordsBatched` reads a record only after that check succeeds. Missing, foreign, and access failures remain fail-closed; best-effort mode emits a distinct warning and omits the affected record. The tenant resolver is grant-only: a non-grant falls through to the normal owner check, and no affirmative tenant authorization is inferred from a cached per-record result. The code therefore preserves the 174 fail-closed distinction and the foreign-record tolerance control while batching only the target identity load.

### Regression selection and execution

The new tests are in `internal/deployment/`, covered by `deployment-package-tests`, which runs `go test ./internal/deployment/...` in the PR validation workflow. The workflow routes that package group in `.github/workflows/ci.yml`; pull requests targeting develop select the validation group through the existing PR selector. No workflow file is changed by this candidate.

Local verification on the exact checked-out candidate:

- `go test ./internal/deployment/... -run 'TestListOwnerVerificationBatchedOncePerTarget|TestListOwnerVerificationPreservesFailClosed|TestBatchCacheNeverSearchesDeploymentOwnership|TestBatchedListClassifiesAccessForeignMissing|TestBatchedListForeignToleranceControl|TestBatchedListOncePerTargetResolverBound' -count=1` — passed.
- `go test ./internal/deployment/... -count=1` — passed.

## Verdict

**APPROVE.** The r2 changes address the classification issue while retaining the distinction between access, foreign, and missing states. The scaling evidence counts authoritative installation loads, and the implementation caches only the target-level resolved identity while checking every deployment record independently. The required package test group and selected checks passed on the exact candidate head.

Landing recipe: merge only the reviewed head `03d144134292d4eae53c966c9f578bbd068d8358` while it remains the PR head and the required checks remain successful. Do not describe skipped native/runtime jobs as green. After landing, verify the resulting develop head and its post-merge checks under the normal merge procedure.

Stop criterion: if the PR head changes, if `deployment-package-tests` or `PR Selected Checks` is no longer successful for this exact SHA, or if a new non-skipped required check is failing or pending, stop and review the new state before landing.
