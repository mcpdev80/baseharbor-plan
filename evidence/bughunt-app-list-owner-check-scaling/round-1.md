# 0427-178 round-1 — app-list owner-verification batch (bughunt BF-08)

Shift: worker w178-listscale (Ornith-Laptop) · Date: 2026-11-09
Card: t-20261108-bughunt-app-list-owner-check-scaling (0427-178)
Branch: 0427-178-listscale (cut from b3a8042d18ea60f162a32a51df34a499cad6a237 = origin/develop HEAD)
Base: b3a8042d1 — ancestry PASS (is an ancestor of HEAD)
Plan repo origin/main HEAD: cedc561032282c7e6cecb48452287f74eb1d1cea
Repo: mcpdev80/baseharbor (product), worktree /tmp/opencode/0427-178-listscale-wt

## PLAN
- diagnose O(n) owner verification in `app list`
- implement batch: load Core installation once per Target, cache only the verified *coreinstallation.State; per-deployment conclusion still fails closed
- add CI-covered regression test (internal/deployment/ -> deployment-package-tests)
- local checks: go test / vet / build / source-readability-audit / gofmt
- commit my changed files only, push branch, PR against develop, evidence here only

## Diagnosis (BF-08)
`app list` -> `listAllDeployments` -> `listDeploymentRecords` -> `verifyDeploymentOwnerAtSeam` -> `VerifyDeploymentOwner` -> `coreinstallation.Load` reads installation.json on EVERY loop iteration. For N records this is O(n) engine/file reads, so the list slows with every added record. File refs: internal/deployment/deployment_list.go:73 (`verifyDeploymentOwnerAtSeam` in the loop), internal/deployment/deployment_store.go:115 (`coreinstallation.Load`), deployment_list.go:57 (`listDeploymentRecords`). Fundakte: evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp4.md BF-08.

## Decision (acceptance 1)
Batch the per-Target Core-installation load. `listDeploymentRecords` now walks via a new `ownerBatch` (internal/deployment/deployment_list_owner_batch.go). The batch resolves the Target's Core installation ONCE per Target and caches only the already-verified `*coreinstallation.State`, keyed by Target. The per-deployment ownership conclusion (card 174 access/foreign/missing and card 144 foreign-tolerance) still runs against every record at the storage seam — the cache is searched by Target, NEVER over a deployment's ownership, so a cached installation can never grant access a fresh check would deny. Fail-closed semantics of cards 174 and 144 are byte-identical: missing -> ErrDeploymentOwnerMissing, foreign installation -> ErrDeploymentOwnerForeign. The tenant grant hook and the owner-loan seam (card 0427-117) are applied through `resolveOwnerLoad` exactly as the single-record path.

Implementation:
- `resolveOwnerLoad(targetName, targetRoot, ownerBatch)` extracts the tenant-hook + authoritative load + loan seam from `VerifyDeploymentOwner`. When `ownerBatch != nil` it caches the resolved installation on first resolve and reuses it; `loads` (authoritative disk reads) increments once per Target, not per record.
- `ownerBatch.loadOwner()` -> `VerifyDeploymentOwnerBatched` -> `verifyDeploymentOwnerAgainstInstallation` re-runs the per-deployment directory conclusion.
- `VerifyDeploymentOwnerAgainstOwner` now delegates to `verifyDeploymentOwnerAgainstInstallation` (shared helper), no behaviour change.

## Regression test (acceptance 2)
New: internal/deployment/deployment_list_owner_scale_test.go (CI-covered — lives under internal/deployment/, so the `deployment-package-tests` job `go test ./internal/deployment/...` runs it; no .github/** edit needed).
- `TestListOwnerVerificationBatchedOncePerTarget`: provisions N=1, 5, 10 records under one owned Target and asserts the batch reads installation.json exactly once (`batch.loads == 1`) for every N — the documented estimate bound (once per Target, not once per record).
- `TestListOwnerVerificationPreservesFailClosed`: missing owner -> ErrDeploymentOwnerMissing, foreign owner -> ErrDeploymentOwnerForeign through the batched list.
- `TestBatchCacheNeverSearchesDeploymentOwnership`: cached State equals authoritative; single authoritative read per Target.

## Correctness (acceptance 3)
Correctness-first. The batch caches only the resolved installation State; the per-deployment conclusion is never cached. All existing deployment + cmd/baha owner/loan tests pass:
- internal/deployment: PASS (go test ./internal/deployment/...)
- cmd/baha loan seam: TestProductionOwnerLoanLocalIsolatedApplyPasses, TestProductionOwnerLoanConnectorBoundStaysFailClosed, TestProductionOwnerLoanUnmarkedLocalStaysFailClosed, TestProductionOwnerLoanRealApplyRunnerStaysFailClosed — PASS
- cmd/baha node disconnect: TestNodeDisconnectRetainsOwnersAndReportsActualRevocation, TestNodeDisconnectRevalidatesRenewalAndOwnerChangesBeforeRevocation, TestNodeDisconnectRejectsForeignRedirectedAndChangedRecoveryOwners — PASS
- source-readability-audit.sh: Go file size PASS (deployment_store.go = 790 lines <= 800), function span PASS, regression ratchet PASS
- go vet ./internal/deployment/...: clean; gofmt: clean

## Pre-existing failures (NOT my regression)
`TestAppInit*`, `TestGuidedInit*`, `TestQuickInit*`, `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` fail identically on the clean base (b3a8042d1) with the same error: `corrupt deployment state for p427-podman-boot/gone/dev ... application id "00000000-..." must be a UUIDv4`. Verified on a fresh clone of b3a8042d1. These are pre-existing, unrelated to the owner-verification batching.

## CI coverage
`deployment-package-tests` (ci.yml:964) runs `go test ./internal/deployment/...` via scripts/pr-incremental-reuse.go:31. My test files live under internal/deployment/ so the CI job runs them under that trigger. No .github/** change required (Owner scope). No rerun triggered.

## Hosted
Per mission, 172-domains is STATE/skip; no hosted run required for this card. Not triggered.

## Commit + PR
- Product commit: `dbb1df08069424265830a397ab41ee882fa36830` on branch `0427-178-listscale` (author Marcel Pfingstgräf <dev@pfingstgraef.eu>, matching repo convention). Log after base shows ONLY this commit.
- PR: https://github.com/mcpdev80/baseharbor/pull/1508, against develop, state OPEN, MERGEABLE, mergeStateStatus CLEAN, single commit dbb1df08.
- Evidence commit: `c5ed802505eafe3093d94aa6eeb4b552df969460` pushed to origin/main (planning repo). ls-remote origin/main confirms c5ed8025.

## Cleanliness
No containers/compose projects started. No orphaned runtimes. State dir isolated under /tmp/opencode/0427-178-listscale-wt.

## Repo-rule compliance
- Write-set: internal/deployment/deployment_list.go, deployment_store.go, deployment_owner_loan.go (modified), deployment_list_owner_batch.go, deployment_list_owner_scale_test.go (new). All under internal/deployment/. No .github/** edited.
- Branch provenance: cut from b3a8042d1 (origin/develop HEAD); ancestry PASS. Only my own commits on this branch.
- Evidence lives only in baseharbor-plan (planning repo) at evidence/bughunt-app-list-owner-check-scaling/round-1.md, pushed to origin/main. No evidence files in the product repo.
- No subagents (Owner directive 2026-11-04). All steps run in this session.
- One integration candidate per chain: single branch 0427-178-listscale.

## Status: DONE — implementation + tests + commit + PR + evidence all complete
