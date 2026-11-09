# CODEX-REVIEW 0427-173 r5 — PR #1505

ROLLE: REVIEW
URTEIL: korrektur

## PLAN

1. Verify the live PR head, current develop base, ancestry, and exact hosted run.
2. Trace the registered MCP handler and inspect whether the mutation regression injects drift after authorization through that path.
3. Verify the on-disk identity guard and run the focused regression; distinguish executed jobs from skipped jobs.
4. Publish the SHA-specific verdict and correction recipe in the planning evidence vault.

## Candidate and ancestry

Repository: `mcpdev80/baseharbor`; PR #1505; task 0427-173.

- PR head: `7b46e975fc1e9c5785bb2faffe04e76683733fda`.
- Live `develop` and current PR base SHA: `b3a8042d18ea60f162a32a51df34a499cad6a237`.
- `git merge-base --is-ancestor b3a8042d18ea60f162a32a51df34a499cad6a237 7b46e975fc1e9c5785bb2faffe04e76683733fda`: exit 1.
- Merge base is still `20902f0a6ab016fd8fe6a501751e1becc5f334dd`. Head `7b46e975` is a direct child of r4 `d0daa4e8`; r5 adds one commit and does not integrate current develop.
- The product delta from r4 is limited to `cmd/baha/app_prune.go`, `cmd/baha/app_prune_test.go`, and `internal/deployment/deployment_store.go`; no `.github/**` file is changed. The candidate is open and GitHub reports mergeable, but the requested base ancestry is absent.

## Findings

### 1. On-disk identity validation is implemented and the helper-level drift case passes

The production delete boundary `internal/deployment/deployment_store.go:623-631` calls `assertOnDiskIdentityMatches` immediately before `os.RemoveAll`. That helper rereads `deployment.json` at `:641-656`; a different identity returns a fail-closed `IDENTITY_DRIFT` machine error before directory removal. The registered handler at `cmd/baha/app_prune.go:395-419` resolves once, authorizes at `:410`, and passes the same resolved object and pinned identity to the mutation helper at `:414`.

The focused local test passed:

```text
go test ./cmd/baha -run '^TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation$' -count=1
ok   github.com/mcpdev80/baseharbor/cmd/baha 0.012s
```

### 2. The required drift injection does not run through the registered handler and authorization seam

`TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation` at `cmd/baha/app_prune_test.go:708-736` first uses the registered MCP handler for an ordinary happy-path deletion. It then recreates the fixture, writes a changed record directly at `:745-753`, and captures its bytes at `:755-759`. The drift assertion constructs in-memory identity A at `:765-776` and calls `executeApplicationPruneResolved` directly at `:779`.

That second half does not invoke `registerMCPAppPruneTool`, `authorizeResolvedMCPOperation`, or the registered handler's resolve/authorize/mutate sequence. The mutation is written before the direct helper invocation, not injected after authorization while the actual handler is paused before mutation. It proves that the delete helper rejects on-disk identity B when passed identity A, but it does not prove the exact required registered-handler plus authorization-seam path. The round-5 dossier describes this as exercising the “registered handler + auth seam”; source lines `:738-779` show that claim is broader than the test.

### 3. Develop ancestry remains unrefreshed

GitHub reports the current PR base SHA as `b3a8042d18ea60f162a32a51df34a499cad6a237`, matching live `refs/heads/develop`. The exact head's parent is r4 `d0daa4e8`, and the ancestry test exits 1. Run `42570428744` verifies the code at the exact head but cannot satisfy the missing base-refresh requirement.

### 4. Hosted state and native-cell truth

Run `42570428744` is terminal `completed/success` on exact head `7b46e975fc1e9c5785bb2faffe04e76683733fda`, event `pull_request`. `PR Selected Checks` passed (job `129009270859`); `PR · Validation · go-unit-tests` passed (job `129006384169`); `PR · Validation · deployment-package-tests` passed (job `129006384163`). There are 14 successful jobs and 12 skipped jobs, with no failed or pending job.

Native destroy-retry Docker and Podman executed and passed (jobs `129006368826`, `129006368704`). Targeted HA Docker/Podman, Native Keycloak/Core, and Selected Runtime were skipped; those cells are not green executions. No workflow rerun or dispatch was triggered.

The round-5 dossier also says a record-version mismatch maps to `DEPLOYMENT_RECORD_VERSION`, but the current implementation's combined condition at `deployment_store.go:650-654` reports `IDENTITY_DRIFT` for a valid JSON record with a wrong version and matching identity. This remains fail-closed, but the dossier's stated cause is inaccurate.

## Actionable correction recipe

- In `cmd/baha/app_prune_test.go:708-800`, inject record replacement after `authorizeResolvedMCPOperation` returns and before the registered MCP handler enters the mutation call. Use a deterministic test seam around authorization or the handler's mutation callback; invoke `registerMCPAppPruneTool` through the in-memory MCP client for the drift case itself. Assert that the handler returns `IDENTITY_DRIFT`, the replacement file remains byte-identical to a snapshot captured before mutation, and no directory is removed.
- Keep `internal/deployment/deployment_store.go:623-656` as the delete-boundary guard; make the injected test fail if `assertOnDiskIdentityMatches` is disabled. Align the round-5 dossier's version-mismatch description with the actual error cause or give version mismatch its stated named error.
- Integrate current develop `b3a8042d18ea60f162a32a51df34a499cad6a237`; verify it is an ancestor of the new head. Obtain a terminal hosted run and `PR Selected Checks` success on that exact refreshed head. Report skipped native cells as skipped.
- Stop when the registered MCP request itself performs the authorization, the injected disk replacement occurs after authorization and before its mutation, the exact identity drift is refused without changing the replacement, current develop ancestry is proven, and required exact-head checks pass.

## repo-rule compliance

- Product repository review was read-only; no candidate files were changed.
- Evidence is stored in canonical `baseharbor-plan`, origin `https://github.com/mcpdev80/baseharbor-plan.git`.
- No workflow file was edited and no CI rerun or dispatch was triggered.

END_DONE 0427-173-r5-review: KORREKTUR PR #1505 head 7b46e975; on-disk identity validation works, but the drift test bypasses the registered MCP authorization path and develop b3a8042d1 is not an ancestor; run 42570428744 success with HA/Keycloak/Selected Runtime skipped.
