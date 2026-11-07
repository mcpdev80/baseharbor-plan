# CODEX-REVIEW PR #1419 at 5c08ed6b

## PLAN

1. Verify fresh exact PR head, base, mergeability, and ancestry.
2. Inspect the candidate source and tests against the two-path owner-loan regression contract.
3. Verify the exact write-set and absence of workflow, release, tag, or receipt changes.
4. Verify prior red/green evidence and all named hosted checks on the exact head.
5. Publish this SHA-specific verdict in the genuine planning repository and verify its remote tree entry.

## Candidate and provenance

Role: CODEX-REVIEW. Task `t-20261106-r27-remote-up-podman-owner-missing` (0427-117), product repo `mcpdev80/baseharbor`, PR #1419.

Fresh product `git ls-remote` output:

```
4bcede9786c9ca6676d12fe140259c9e45d43f93 refs/heads/develop
5c08ed6be15eac7931441c9a78655aa67e2a50f8 refs/pull/1419/head
```

GitHub reports PR #1419 OPEN and MERGEABLE, base `develop`, exact head `5c08ed6be15eac7931441c9a78655aa67e2a50f8`. `git merge-base --is-ancestor 4bcede9786c9ca6676d12fe140259c9e45d43f93 5c08ed6be15eac7931441c9a78655aa67e2a50f8` returned 0.

## Scope and changed paths

The exact base-to-head diff contains six paths, all within the requested `cmd/baha/*` and `internal/deployment/*` write-set:

```
A cmd/baha/deployment_owner_loan_regression_test.go
M cmd/baha/deployment_record.go
M cmd/baha/runtime_integration_test_support_test.go
A cmd/baha/test_isolation_support_test.go
A internal/deployment/deployment_owner_loan.go
M internal/deployment/deployment_store.go
```

No `.github/**` path changed. No release/tag or receipt-chain file changed, and PR remains open; this review did not merge, tag, or publish a release.

## Owner-loan behavior and Option 2 coverage

Verdict: **APPROVE** under the requested Option 2 evidence structure. The positive grant is discriminated at the production owner-write seam; the separate full command-runner case is deliberately fail-closed on both sides for environment-selected `iso`. The evidence and comments document why that runner case cannot be red/green for grant when `BASEHARBOR_TARGET=iso` selects the same target as the requested isolated target.

- Positive red/green: `TestProductionOwnerLoanLocalIsolatedApplyPasses` in `cmd/baha/deployment_owner_loan_regression_test.go:320-421` configures a ready boot Core as the default and a distinct ownerless local Podman target, resolves the repository application for that target, calls `recordDeploymentBeforeMutation` at line 391, and verifies the owner-backed pending record at lines 398-405. This is the production write function called by `runApplicationApplyLifecycle`; the published round-7 evidence records the same regression RED on the prior base with the literal `ErrDeploymentOwnerMissing` sentinel and GREEN on candidate `5c08ed6b`.
- Real runner fail-closed on both sides: `TestProductionOwnerLoanRealApplyRunnerStaysFailClosed` at `cmd/baha/deployment_owner_loan_regression_test.go:486-508` sets `BASEHARBOR_TARGET=iso`, calls `executeApplicationApplyLifecycle` at line 495, and requires `errors.Is(err, deployment.ErrDeploymentOwnerMissing)` at line 496. The prior round-7 evidence records this test PASS on both base and candidate with the same sentinel.
- Structural reason: `executeApplicationApplyLifecycle` enters `runApplicationApplyLifecycle` (`cmd/baha/app_apply.go:83-96`), which reaches `recordDeploymentBeforeMutation` at line 165. The apply selector takes the environment target before persisted/default selection (`cmd/baha/target_selection.go:58-86`). `bahaEffectiveBootTargetName` likewise takes configured `BASEHARBOR_TARGET` first (`cmd/baha/deployment_record.go:328-359`); `productionLoanAuthorityForTarget` rejects `bootTargetName == targetName` at lines 172-175. Thus an environment-selected `iso` target is intentionally refused by the real runner; the prior round-7 evidence documents this shared selection behavior and why the positive grant discriminator uses the production write seam with a distinct default boot target.
- Fail-closed ownership checks remain in place: `VerifyDeploymentOwner` calls the loan verifier only when the target installation is absent, translates verifier refusal to the original `ErrDeploymentOwnerMissing` sentinel, checks target/installation binding, and runs `verifyLoanOwnerGuarantees` on the loan path (`internal/deployment/deployment_store.go:115-170`). The CLI authority only permits local access with a genuine READY boot Core on a different target and refuses tenant, connector/remote, or bound management authority (`cmd/baha/deployment_record.go:147-216`). Connector-bound refusal remains covered by `TestProductionOwnerLoanConnectorBoundStaysFailClosed` at lines 427-452.

## Prior evidence witness

The round-7 red/green and structural-boundary record is on genuine planning `origin/main`. Exact `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-7.md` output:

```
100644 blob 929e44ed95b60e5933e0c76c58346d956b1c06cf	evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-7.md
```

The evidence records the literal red sentinel for the positive seam regression on the prior base, green on candidate `5c08ed6b`, and the separate real-runner fail-closed sentinel on both sides.

## Exact-head hosted checks

`gh pr checks 1419 --repo mcpdev80/baseharbor` reports the following named jobs as PASS on the current PR head. The corresponding terminal GitHub run is `42365306851` (run 5001, pull_request, head `5c08ed6be15eac7931441c9a78655aa67e2a50f8`, conclusion success):

- `PR · Validation · cli-package-tests` job `128382042203`: PASS.
- `PR · Validation · cli-build` job `128382042081`: PASS.
- `PR · Validation · cli-gofmt` job `128382042097`: PASS.
- `PR · Validation · cli-vet` job `128382042035`: PASS.
- `PR · Validation · deployment-package-tests` job `128382042061`: PASS.
- `PR · Validation · source-contracts` job `128382042077`: PASS.
- `PR Selected Checks` job `128383547735`: PASS.

Ten unrelated selected/runtime jobs are skipped by the owner push-ref gate, as stipulated for this review; no rerun or workflow dispatch was performed.

## Review result

**APPROVE** `5c08ed6be15eac7931441c9a78655aa67e2a50f8`. No corrective recipe is required. Preserve the positive write-seam red/green regression and the separate actual-runner fail-closed regression; stop acceptance if the candidate head changes or any named hosted check is no longer passing.

## Repo-rule compliance

Read-only exact-head review. No product file, workflow, PR state, CI run, release, tag, or receipt was changed. No merge, VM, container, or subagent was used. Evidence is stored only in the genuine planning repository.

## END CODEX-REVIEW DONE

END_DONE codex-1419-review-e: verdict=approve head=5c08ed6be15eac7931441c9a78655aa67e2a50f8 delta=cmd/baha+internal/deployment only no .github real-runner=executeApplicationApplyLifecycle failclosed for BASEHARBOR_TARGET iso on both sides positive=production write-seam red-green CI=run 42365306851 terminal success including cli-package-tests/build/gofmt/vet deployment-package-tests source-contracts PR Selected Checks ancestry rc0 mergeable recipe=no corrective change; preserve Option-2 coverage and stop if a named check or head changes
