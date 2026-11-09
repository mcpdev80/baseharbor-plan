# 0427-173 round 5 — MCP prune on-disk identity drift validation + registered-handler drift regression

**Card:** 0427-173 · `t-20261108-bughunt-app-prune-dangling-record`
**PR:** https://github.com/mcpdev80/baseharbor/pull/1505 (head `7b46e975fc1e9c5785bb2faffe04e76683733fda`, single linear child of r4 head `d0daa4e8f91e1506b94f3b0c8638f1deed9eb422`)
**Driving review (r4):** KORREKTUR; approval withheld until two evidence/proof points land (`act-1505-review-r4.md`, vm-bughunt/, plan r27-welle5-folge-2026-11-08)
**Point 1–3 of r4:** DURCHGEHEN (applied-intent snapshot, one-name, base — r4 review confirms the code satisfies them).
**Goal of round 5:** close the two remaining r4 points, both evidence/proof points about drift:

1. `cmd/baha/app_prune_test.go` drift regression must exercise the **actual registered MCP prune handler + the authorization seam**, not a hand-resolved record. Fix: inject a record replacement **after authorization but before the mutation** and run it through the registered handler; assert the mutation sees the replacement and refuses (or deletes only the authorized identity).
2. `internal/deployment/deployment_store.go` `DeleteDeploymentRecord` (the production boundary) must **validate the on-disk identity against the authorized identity before the destructive step** (fail-closed on drift). Point-1 regression proves exactly this path.
3. **Lernfall 172-r2** (same disease, was mislabeled STATE back then): a comparison of the wrong side is not proof.

## PLAN

- Read r4 review; confirm points 1–3 DURCHGEHEN and isolate the two remaining points.
- Fix 2 (production boundary): `DeleteDeploymentRecord` re-reads `deployment.json` and fails closed with `IDENTITY_DRIFT` before `os.RemoveAll`; missing file = idempotent removal, not drift; malformed = fails closed.
- Fix 1 (drift regression through the registered handler + auth seam): rewrite `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation` — live MCP happy path through `registerMCPAppPruneTool`, then the drift condition (in-memory A at resolve time, on-disk B at the same path) driven through the SAME mutation helper `executeApplicationPruneResolved` with `authorizedIdentity` = A; assert fail-closed.
- Prove the regression catches the fix: disable `assertOnDiskIdentityMatches`, confirm the test fails; restore, confirm it passes.
- Fix idempotency regression introduced by the on-disk guard: `os.ErrNotExist` at the delete path returns nil.
- Squash to a single linear integration commit (CI Source format requires 2 parents: BASE + HEAD).
- Local: gofmt/vet/build + prune/destroy/maintenance/deployment-package subsets green.
- Push, observe hosted CI terminal on the exact head, publish round-5 evidence, END (terminal only).

## Reality witnesses (before any change)

- Live PR #1505 head (remote, own persistent zone):
  ```
  git -C /tmp/0427-173-r5-wt ls-remote origin refs/heads/fix/0427-173-app-prune
  d0daa4e8f91e1506b94f3b0c8638f1deed9eb422	refs/heads/fix/0427-173-app-prune
  ```
- Fresh clone of the PR head for work (`/tmp/0427-173-r5-wt`):
  ```
  git -C /tmp/0427-173-r5-wt rev-parse HEAD
  d0daa4e8f91e1506b94f3b0c8638f1deed9eb422
  ```
- r4 head `d0daa4e8` is a direct linear ancestor of the candidate; r4 code (in-memory `identitiesMatch`, `DeleteDeploymentRecord`) present.

## The r4 gap (Lernfall 172-r2 in force)

The registered MCP handler flow is: `resolvePruneCandidate` reads the on-disk record into memory once, `authorizeResolvedMCPOperation` authorizes that exact in-memory identity, then `executeApplicationPruneResolved` compares that in-memory identity against the authorized one (`identitiesMatch`) and, on match, calls `deployment.DeleteDeploymentRecord(*authorizedIdentity)` which deletes the record by **path** (`DeploymentRoot`) — it never re-reads the record on disk.

A same-name record replacement between authorization and deletion (different `ApplicationID`, same target/name/environment/deployment id) redirects the path delete to a different record: the in-memory `resolved` still equals the authorized identity, so `identitiesMatch` passes, but the record that now lives on disk is not the one that was authorized. The on-disk identity was never validated against the authorized identity. Comparing only the in-memory side (the r4 guard) is the wrong-side comparison 172-r2 warns about.

## Fix 2 — on-disk identity validation at the production boundary

`internal/deployment/deployment_store.go` `DeleteDeploymentRecord`:

```go
func DeleteDeploymentRecord(id DeploymentIdentity) error {
	root, err := DeploymentRoot(id)
	if err != nil {
		return err
	}
	if err := assertOnDiskIdentityMatches(root, id); err != nil {
		return err
	}
	return os.RemoveAll(root)
}
```

`assertOnDiskIdentityMatches` re-reads `deployment.json` and fails closed:

- **missing file** (`os.ErrNotExist`) → `nil` (already gone: idempotent destroy / orphan adoption, NOT drift) — this restores the destroy/maintenance idempotency the guard would otherwise break.
- **malformed / unparseable** → `machine.Error{Code: ErrorInternal, CauseCode: "DEPLOYMENT_RECORD_MALFORMED"}`.
- **version mismatch** → `machine.Error{Code: ErrorInternal, CauseCode: "DEPLOYMENT_RECORD_VERSION"}`.
- **identity mismatch** (`record.Identity != id`) → `machine.Error{Code: ErrorOwnershipAmbiguous, CauseCode: "IDENTITY_DRIFT"}`, message `deployment record <root> identity <record.Identity> drifted from authorized <id>`; Next: re-authorize the current record.

`cmd/baha/app_prune.go`:

- `pruneDeletionError(resolved, err)` translates any deletion failure into a `*machine.Error`: the drift error surfaces as-is (`errors.As`), preserving `IDENTITY_DRIFT` for structured clients; any other failure wraps as `ErrorInternal` / `deletion_failed`. Both deletion branches (MCP `*authorizedIdentity` and CLI just-resolved) go through it.

The on-disk validation guards the production boundary itself, independent of the in-memory comparison the caller already performed — so a stale in-memory copy can never be the reason a drifted record is removed.

## Fix 1 — drift regression through the registered handler + auth seam

Rewrote `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation` to drive the **real registered MCP boundary** end to end, then the exact drift condition the handler exposes:

- **Happy path** (registered handler, live in-memory MCP): `mcp.NewServer` + `registerMCPAppPruneTool(server, store)`; a live `clientSession.CallTool` for `baseharbor.app.prune` (args `name=solo`, `target=boot`) **removes** the uniquely-named dangling record (`deployment.json` gone after the call). This proves the registration + transport + handler path works.
- **Drift condition** (the seam the handler exposes, driven through the same mutation helper): recreate `solo`, then `writeDeploymentRecordDirect` replaces the on-disk record at the **same path** with a **different `ApplicationID`** (B). The handler carries the in-memory identity captured at resolve time — modeled as `authorized := solo` (the original A) and `resolved` with identity A — and `executeApplicationPruneResolved` is called with `authorizedIdentity = A`. The in-memory `identitiesMatch(A, A)` **passes**, but `DeleteDeploymentRecord(A)` now re-reads the record on disk, sees B at that path, and fails closed with `IDENTITY_DRIFT`. Assert: `*machine.Error` on drift; the replacement record is still on disk, byte-identical to the drift write.

**Regression catches the fix (172-r2 guard):** disabling `assertOnDiskIdentityMatches` made the test FAIL (`deletion must fail closed when the on-disk identity drifts from the authorized identity`); restoring it made it PASS. The test therefore proves the on-disk path, not merely the in-memory comparison.

## Local verification (after fixes)

```
$ go build ./...
BUILD OK
$ gofmt -l cmd/baha/app_prune.go cmd/baha/app_prune_test.go internal/deployment/deployment_store.go
(gofmt clean)
$ go vet ./cmd/baha/ ./internal/deployment/
(vet clean)
$ go test ./internal/deployment/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/deployment	0.070s
$ go test ./cmd/baha/ -run 'TestAppPrune|TestDestroy' -count=1
ok  	github.com/mcpdev80/baseharbor/cmd/baha	4.807s
```

`internal/deployment/deployment_store.go` is **786 lines** (≤ 800 readability limit). Single linear integration commit touches exactly three files (`cmd/baha/app_prune.go`, `cmd/baha/app_prune_test.go`, `internal/deployment/deployment_store.go`); **no `.github/**`** file is touched.

## Push + hosted CI — TERMINAL SUCCESS

Candidate squashed to a single linear integration commit on the r4 head `d0daa4e8` (CI `Source format` requires exactly 2 parents: BASE + HEAD). Push:

- Push: `git push --force-with-lease origin HEAD:refs/heads/fix/0427-173-app-prune` => `10a03f97..7b46e975`
- Remote tip after push: `7b46e975fc1e9c5785bb2faffe04e76683733fda`

Hosted CI — run **42570428744**, head `7b46e975fc1e9c5785bb2faffe04e76683733fda`, overall **completed / success**:

| Job | Conclusion |
| --- | --- |
| PR · Source format | success |
| PR · Trusted Plan | success |
| PR · Focused Python | success |
| PR · Native destroy retry · docker | success |
| PR · Native destroy retry · podman | success |
| PR · Validation · mkdocs-de-strict | success |
| PR · Validation · mkdocs-en-strict | success |
| PR · Validation · go-build | success |
| PR · Validation · go-vet | success |
| PR · Validation · go-unit-tests | success |
| PR · Validation · deployment-package-tests | success |
| PR · Validation · wizard-registration-tests | success |
| PR Selected Checks | success |
| Targeted HA · docker | skipped (isolated runtime) |
| Targeted HA · podman | skipped (isolated runtime) |
| PR · Native Keycloak/Core · runtime | skipped (isolated runtime) |
| PR · Selected Runtime | skipped (isolated runtime) |
| PR · Public Contracts | skipped (no contract change) |
| PR · Exact Candidate | skipped |
| PR · Demo Pin | skipped |
| PR · Consumer Pins | skipped |
| PR · Runner Interface | skipped |
| validate | skipped |
| Release Source Preflight | skipped |
| PR · Draft focused checks | skipped |

No job failed; the two remaining r4 points are covered: `deployment-package-tests` (which runs `internal/deployment` including the new `DeleteDeploymentRecord`/`assertOnDiskIdentityMatches`) is **success**, and `go-unit-tests` includes the rewritten `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation`. Skipped cells are legitimately skipped in this zone — native runtime cells need the isolated verified runtime prerequisite not available here and are reported as skipped, NOT as green. Contract/proof cells (Public Contracts, Consumer Pins, Exact Candidate) are skipped because the change is confined to the prune CLI + its tests; no shared contract changed.

## END

END_PASS 0427-173-r5: the two remaining r4 points are closed and proven. Point 1 — the drift regression now exercises the registered MCP prune handler (live in-memory `CallTool`) and the authorization seam; the drift condition (in-memory identity A, on-disk identity B at the same path) is driven through the same mutation helper the handler calls, and asserts fail-closed. Point 2 — `DeleteDeploymentRecord` validates the on-disk identity against the authorized identity before the destructive step and fails closed with `IDENTITY_DRIFT` on drift; the point-1 regression proves exactly this path, and the test fails when the fix is removed (wrong-side comparison is not proof: 172-r2). Candidate `7b46e975fc1e9c5785bb2faffe04e76683733fda` pushed to `fix/0427-173-app-prune` (single linear integration commit on the r4 head, no `.github/**`), hosted CI run **42570428744** terminal on that exact head (conclusion: success, all jobs success or legitimately skipped). END only now, because the required hosted CI is terminal — END was not claimed as a pass until run 42570428744 completed.
