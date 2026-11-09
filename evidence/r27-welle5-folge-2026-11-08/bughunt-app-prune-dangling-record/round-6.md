# 0427-173 round 6 — MCP prune drift through the registered handler + authorization seam

**Card:** 0427-173 · `t-20261108-bughunt-app-prune-dangling-record`
**PR:** https://github.com/mcpdev80/baseharbor/pull/1505 (head `df9af471dcd0b058ed7a59a36e6cb41279ed54475`, single linear child of develop `b3a8042d18ea60f162a32a51df34a499cad6a237`)
**Driving review (r5):** KORREKTUR; approval withheld until the drift regression runs through the registered MCP handler + authorization seam and develop ancestry is refreshed (`act-1505-review-r5.md`, vm-bughunt/, plan r27-welle5-folge-2026-11-08)
**Point 1 (r4) already DURCHGEHEN:** on-disk identity validation in `assertOnDiskIdentityMatches` before `os.RemoveAll` (fail-closed `IDENTITY_DRIFT` / `machine.ErrorOwnershipAmbiguous`).

## PLAN

- Read r5 review; confirm point 1 sits, isolate the two remaining points.
- Fix 1: drift regression runs through the registered MCP prune handler and its authorization seam — `pruneDriftHook` fires inside the handler after the authorized identity is captured and before the mutation; the handler (not the test) performs the mutation call and the `IDENTITY_DRIFT` refusal.
- Fix 2 (latent r5 idempotency regression): `assertOnDiskIdentityMatches` treats `os.ErrNotExist` as idempotent removal (nil), so a second destroy on an already-removed record no longer errors.
- Fix 3 (r5 point 4): split the combined condition so a valid-JSON wrong-version record reports the named cause `DEPLOYMENT_RECORD_VERSION` instead of `IDENTITY_DRIFT`.
- Prove the regression catches the fix: neuter `assertOnDiskIdentityMatches` → the registered handler deletes the drifted record and the test FAILS; restore → PASSES.
- Base refresh: rebase r6 onto develop `b3a8042d` (prove ancestor).
- Local: gofmt/vet/build + prune/destroy/maintenance/deployment-package subsets green.
- Push, observe hosted CI terminal on the exact head, publish round-6 evidence, END (terminal only).

## Reality witnesses (before any change)

- Live PR #1505 head (remote, own persistent zone):
  ```
  git -C /tmp/0427-173-r6-wt ls-remote origin refs/heads/fix/0427-173-app-prune
  f828b79be0c5a3e98c7a2fb77fc7d81071d38093	refs/heads/fix/0427-173-app-prune
  ```
- Live develop: `b3a8042d18ea60f162a32a51df34a499cad6a237`.
- Ancestry (pre-refresh): `git merge-base --is-ancestor b3a8042d1 HEAD` ⇒ exit 1 (r6 sat on r4 head `d0daa4e8`, not develop).

## The r5 gap (Lernfall 172-r2 in force)

The r5 drift regression mutated the on-disk record itself and then called `executeApplicationPruneResolved` directly with a hand-constructed in-memory identity A while the record on disk was B. That path bypasses `registerMCPAppPruneTool`, `authorizeResolvedMCPOperation`, and the registered handler's own resolve/authorize/mutate sequence — it proves the wrong seam. Comparing only an in-memory condition (the r5 guard) without running the drift through the registered handler is the wrong-side comparison 172-r2 warns about.

The registered handler flow: `resolvePruneCandidate` captures the authorized identity at its resolve (A), then `DeleteDeploymentRecord` re-reads the record on disk before the destructive step. The drift the on-disk validation catches is the record changing between that authorization capture and the delete.

## Fix 1 — drift regression THROUGH the registered handler + authorization seam

`cmd/baha/app_prune_test.go` `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation`:

- Drives the registered MCP prune handler end to end through the live in-memory MCP boundary: `mcp.NewServer` + `registerMCPAppPruneTool(server, store)`; a live `clientSession.CallTool` for `baseharbor.app.prune`.
- Injects the drift through a deterministic package-internal seam `pruneDriftHook` that fires **inside the registered handler** — after it captures the authorized identity (read #1, A) and **before** it runs the mutation. The seam rewrites the SAME deployment directory to a DIFFERENT application id (B).
- The handler authorizes A; `DeleteDeploymentRecord` re-reads B and fails closed with `IDENTITY_DRIFT` before `os.RemoveAll`. Assert: `result.IsError`, the refusal body names a drift cause, the seam fired, and the replacement record is byte-identical to the drift write (nothing removed).

```go
savedHook := pruneDriftHook
var drifted int32
var driftedBytes []byte
pruneDriftHook = func() {
	if atomic.AddInt32(&drifted, 1) != 1 {
		return
	}
	driftB := deployment.DeploymentRecord{ /* same path, different application_id */ }
	writeDeploymentRecordDirect(t, driftB)
	driftedBytes, _ = os.ReadFile(filepath.Join(deployDir, "deployment.json"))
}
t.Cleanup(func() { pruneDriftHook = savedHook })
result, callErr := clientSession.CallTool(... "baseharbor.app.prune" ...)
if drifted < 1 { t.Fatal("injected drift hook never fired ...") }
if !result.IsError { t.Fatal("handler must refuse with IDENTITY_DRIFT") }
```

The happy path (uniquely-named record removed through the same registered handler) is covered separately by `TestAppPruneMCPHappyPathRemovesUniquelyResolvedRecord`.

### The seam (production-safe, package-internal)

`cmd/baha/app_prune.go` `pruneDriftHook` fires inside `registerMCPAppPruneTool` after `authorizedIdentity := resolved.DeploymentIdentity` and before `authorizeResolvedMCPOperation` / `executeApplicationPruneResolved`:

```go
// pruneDriftHook is a package-internal test seam (production path keeps it nil, so
// no behaviour changes): it fires inside the registered MCP prune handler after the
// handler captures the authorized identity (the read that authorizes A) and before
// it runs the mutation. ... Style follows the existing cmd/baha observedAt seam.
var pruneDriftHook func()
...
authorizedIdentity := resolved.DeploymentIdentity
if pruneDriftHook != nil {
	pruneDriftHook()
}
if err := authorizeResolvedMCPOperation(ctx, "app.prune", resolved, ""); err != nil {
```

nil default ⇒ no production behaviour change; style follows the existing `observedAt`/`testHookAfterGuardRead` seams.

## Fix 2 — idempotency (latent r5 regression)

`internal/deployment/deployment_store.go` `assertOnDiskIdentityMatches` treats a missing `deployment.json` as idempotent removal (nil), so a second destroy on an already-removed record does not error — the on-disk guard must not fail closed when the record is already gone.

## Fix 3 — named version-mismatch cause (r5 point 4)

Split the combined condition so a valid-JSON record with a wrong `version` reports `DEPLOYMENT_RECORD_VERSION` (machine.ErrorInternal) and an identity mismatch reports `IDENTITY_DRIFT` (machine.ErrorOwnershipAmbiguous), instead of both reporting `IDENTITY_DRIFT`.

## Local verification (after fixes)

```
$ go build ./...
BUILD OK
$ gofmt -l cmd/baha/app_prune.go cmd/baha/app_prune_test.go internal/deployment/deployment_store.go
(gofmt clean)
$ go vet ./cmd/baha/ ./internal/deployment/
(vet clean)
$ go test ./cmd/baha/ -run 'TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation|TestAppPruneMCPHappyPathRemovesUniquelyResolvedRecord' -count=1
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.072s
$ go test ./cmd/baha/ -run 'TestAppPrune|TestDestroy|TestMaintenance|TestRepositoryAdopt|TestInstallation' -count=1
ok  	github.com/mcpdev80/baseharbor/cmd/baha	25.140s
$ go test ./internal/deployment/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/deployment	0.067s
```

`internal/deployment/deployment_store.go` is 789 lines (≤ 800). Single linear integration commit touches exactly three files (`cmd/baha/app_prune.go`, `cmd/baha/app_prune_test.go`, `internal/deployment/deployment_store.go`); **no `.github/**`** file is touched.

### Regression catches the fix

Neutering `assertOnDiskIdentityMatches` makes the registered handler delete the drifted record; the test FAILS (`registered MCP prune handler must refuse with IDENTITY_DRIFT ...`). Restoring the guard makes it PASS. The test therefore proves the on-disk path, not merely an in-memory comparison (172-r2).

## Push + hosted CI — TERMINAL SUCCESS

Candidate rebased onto develop `b3a8042d` (single linear integration commit directly on develop; `git merge-base --is-ancestor origin/develop HEAD` ⇒ YES). Push:

- Push: `git push --force-with-lease origin HEAD:refs/heads/fix/0427-173-app-prune` ⇒ `f828b79b..df9af471`
- Remote tip after push: `df9af471dc0b058ed7a59a36e6cb41279ed54475`

Hosted CI — run **42578280694**, head `df9af471dcd0b058ed7a59a36e6cb41279ed54475`, overall **completed / success**:

| Job | Conclusion |
| --- | --- |
| PR · Source format | success |
| PR · Validation · go-build | success |
| PR · Validation · go-vet | success |
| PR · Validation · go-unit-tests | success |
| PR · Validation · deployment-package-tests | success |
| PR Selected Checks | success |
| (all other jobs) | success or skipped |

No job failed. `deployment-package-tests` (which runs `internal/deployment` including the new `assertOnDiskIdentityMatches` and the version-mismatch split) is **success**, and `go-unit-tests` includes the rewritten `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation`. Skipped cells are legitimately skipped in this zone — native runtime cells need the isolated verified runtime prerequisite not available here and are reported as skipped, NOT as green. Contract/proof cells (Public Contracts, Consumer Pins, Exact Candidate) are skipped because the change is confined to the prune CLI + its tests; no shared contract changed.

## END

END_PASS 0427-173-r6: the r5 point 1 is closed — the drift regression now runs through the registered MCP prune handler and its authorization seam (the handler captures A, the injected `pruneDriftHook` replaces the record with B after authorization and before the handler's own mutation, and the handler refuses `IDENTITY_DRIFT`); point 2 — the base is refreshed (rebase onto develop `b3a8042d`, ancestor proven) with a fresh hosted run terminal on that exact head. Candidate `df9af471dc0b058ed7a59a36e6cb41279ed54475` pushed to `fix/0427-173-app-prune` (single linear integration commit on develop, no `.github/**`), hosted CI run **42578280694** terminal on that exact head (conclusion: success, no job failed). END only now, because the required hosted CI is terminal — END was not claimed as a pass until run 42578280694 completed.
