# 0427-173 round 7 — drift hook placed in the post-authorization window

**Card:** 0427-173 · `t-20261108-bughunt-app-prune-dangling-record`
**PR:** https://github.com/mcpdev80/baseharbor/pull/1505 (head `67e723fbc1c8402d785f5ef4b2089a31de4f6b59`, single linear child of r6 `df9af471`, based directly on develop `b3a8042d18ea60f162a32a51df34a499cad6a237`)
**Driving review (r6): KORREKTUR** — the path and neighbors were correct; the one remaining blocker was the injection ORDER (act-1505-review-r6.md, vm-bughunt/, plan)

## PLAN

- Read r6 review; confirm the only blocker is drift injection timing.
- Fix 1: move `pruneDriftHook` from before `authorizeResolvedMCPOperation` to after it succeeds and immediately before the handler's own mutation (`executeApplicationPruneResolved`).
- Prove the regression catches the fix: neuter `assertOnDiskIdentityMatches` → the registered handler deletes the drifted record and the test FAILS; restore → PASSES.
- Base refresh: r7 already inherits develop ancestry from r6; confirm ancestor.
- Local: gofmt/vet/build + prune/destroy/maintenance/deployment-package subsets green.
- Push, observe hosted CI terminal on the exact head, publish round-7 evidence, END (terminal only).

## The r6 blocker (Lernfall 172-r2 — ordering is the seam)

The r6 review confirmed the registered-handler path and handler-owned mutation were exercised and the three neighboring storage protections (idempotency, malformed, version, drift) remained in source. The one blocker: in `cmd/baha/app_prune.go:428-430` (r6 head `df9af471`), the handler captured `authorizedIdentity`, invoked `pruneDriftHook`, and **only then** called `authorizeResolvedMCPOperation`. The hook rewrote the on-disk identity *before* the authorization function executed. Capturing a value named `authorizedIdentity` is not the completed authorization step. The test proved the handler saw a changed record after its initial resolution but did not prove a drift occurring after successful authorization and before the handler's mutation is rejected.

## The r7 fix — hook placement

`cmd/baha/app_prune.go` `registerMCPAppPruneTool`: the `pruneDriftHook` invocation moved from before `authorizeResolvedMCPOperation` to **after it succeeds and immediately before `executeApplicationPruneResolved`**:

```go
authorizedIdentity := resolved.DeploymentIdentity
if err := authorizeResolvedMCPOperation(ctx, "app.prune", resolved, ""); err != nil {
    return machineMCPFailure(err)
}
// Test seam ... fired after successful authorization (identity A is now
// authorized) and immediately before the handler's own mutation. ...
if pruneDriftHook != nil {
    pruneDriftHook()
}
outBuf, errOutBuf := &bytes.Buffer{}, &bytes.Buffer{}
_, rErr := executeApplicationPruneResolved(ctx, store, resolved, ..., &authorizedIdentity)
```

`pruneDriftHook` stays inside the registered handler and is nil by default (production path untouched). The test `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation` still drives the registered MCP prune handler end to end via the live in-memory client and `clientSession.CallTool`; the replacement is injected only through the handler seam **after** authorization; it asserts the handler's own mutation returns `IDENTITY_DRIFT`, leaves the replacement record byte-identical, and does not remove the directory. The test does not invoke `executeApplicationPruneResolved` or `DeleteDeploymentRecord` directly.

## Regression catches the fix

Neutering `assertOnDiskIdentityMatches` makes the registered handler delete the drifted record (the `IsError` refusal assertion FAILS). Restoring the guard makes it PASS. The test therefore proves the on-disk guard rejects a post-authorization drift, not merely an in-memory comparison (172-r2).

## Local verification (after fix)

```
$ go build ./...
BUILD OK
$ gofmt -l cmd/baha/app_prune.go internal/deployment/deployment_store.go cmd/baha/app_prune_test.go
(gofmt clean)
$ go test ./cmd/baha/ -run 'TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation|TestAppPruneMCPHappyPathRemovesUniquelyResolvedRecord' -count=1
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.027s
$ go test ./cmd/baha/ -run 'TestAppPrune|TestDestroy|TestMaintenance|TestRepositoryAdopt|TestInstallation' -count=1
ok  	github.com/mcpdev80/baseharbor/cmd/baha	19.257s
$ go test ./internal/deployment/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/deployment	0.048s
```

`internal/deployment/deployment_store.go` is 789 lines (≤ 800). Single linear integration commit touches exactly one file (`cmd/baha/app_prune.go`); **no `.github/**`** file is touched.

## Push + hosted CI — TERMINAL SUCCESS

Single linear integration commit directly on develop `b3a8042d` (ancestor proven; `git merge-base --is-ancestor origin/develop HEAD` ⇒ YES). Push:

- Push: `git push --force-with-lease origin HEAD:refs/heads/fix/0427-173-app-prune` ⇒ `df9af471..67e723fb`
- Remote tip after push: `67e723fbc1c8402d785f5ef4b2089a31de4f6b59`

Hosted CI — run **42581112177**, head `67e723fb`, overall **completed / success**:

| Job | Conclusion |
| --- | --- |
| PR · Native impact selection | success |
| PR · Source format | success |
| Workflow policy | success |
| PR · Trusted Plan | success |
| PR · Native destroy retry · podman | success |
| PR · Native destroy retry · docker | success |
| PR · Focused Python | success |
| PR · Validation · go-build | success |
| PR · Validation · mkdocs-de-strict | success |
| PR · Validation · documentation-audit | success |
| PR · Validation · go-vet | success |
| PR · Validation · deployment-package-tests | success |
| PR · Validation · cli-gofmt | success |
| PR · Validation · go-unit-tests | success |
| PR · Validation · mkdocs-en-strict | success |
| PR · Validation · pages-candidate-build | success |
| PR · Validation · wizard-registration-tests | success |
| PR Selected Checks | success |

No job failed. `deployment-package-tests` (which runs `internal/deployment` including the on-disk identity guard) is **success**, and `go-unit-tests` includes the rewritten `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation`. Skipped cells are legitimately skipped in this zone — native runtime cells need the isolated verified runtime prerequisite not available here and are reported as skipped, NOT as green. Contract/proof cells (Public Contracts, Consumer Pins, Exact Candidate) are skipped because the change is confined to the prune CLI + its tests; no shared contract changed.

## END

END_PASS 0427-173-r7: the r6 blocker is closed — `pruneDriftHook` now fires inside the registered MCP prune handler *after* `authorizeResolvedMCPOperation` succeeds and *immediately before* the handler's own mutation, so the drift is injected in the required post-authorization, pre-mutation window. The handler (not the test) performs the mutation call and the `IDENTITY_DRIFT` refusal; the replacement record is left byte-identical. The regression is proven (neuter the guard → the handler deletes the drifted record and the test FAILS). Candidate `67e723fb` pushed to `fix/0427-173-app-prune` (single linear integration commit on develop, no `.github/**`), hosted CI run **42581112177** terminal on that exact head (conclusion: success, no job failed). END only now, because the required hosted CI is terminal — END was not claimed as a pass until run 42581112177 completed.
