# W30 State-Owner R9 — Evidence

**Lane:** w30-stateowner-r9 | **Coord:** f49a3303 | **PR:** #1347 / **Task:** t-20261018-r27-state-owner
**Basis:** 797bd811e2dec5c60fe58f27e738d6fc0314cbb8 (branch work/r27-state-owner)
**Grounding:** review-1347h (befund 1 = rezept; befund 2 = gelobt; befund 3 = environment)
**Role:** Worker (test-only). No product-code change. STOP = only this scenario.

## PLAN

1. Fetch `origin/work/r27-state-owner` + `origin/develop`; create isolated worktree at 797bd811.
2. Probe seam behavior for "missing owner ON an existing record": file absent vs invalid JSON → which concrete error class (`ErrDeploymentOwnerMissing` vs `ErrDeploymentOwnerForeign`).
3. Add ONE new test `TestDeploymentOwnerMissingOnExistingRecordSeam` in `deployment_owner_binding_test.go`:
   - (1) provision owner for target "local" + save a real record (real save path), capture record bytes.
   - (2) remove/clear the installation.json (owner material) while the record file stays untouched (file exists → "missing owner with existing record").
   - (3) public seams: `LoadDeploymentRecord` → concrete owner error + bytes unchanged; `SaveDeploymentRecord(nil-preferences)` → rejection + bytes unchanged; `ListDeployments` → concrete semantics from main source (missing owner ⇒ NOT a silent empty listing).
   - (4) keep the existing empty-list test (target without file) beside it.
4. `TMPDIR=/tmp go test ./internal/deployment -count=1` + `cmd/baha -run 'Owner|List|Deployment' -count=1` (env-fails tolerated; GOCACHE=/tmp/opencode on disk-quota). Document Run-ID/status.
5. Merge `origin/develop`; ancestry rc=0; ls-remote SHA; write-set = test file only (grep produktcode/.github empty).
6. Push `refs/heads/work/r27-state-owner` (no tmp branch). Write evidence. Post END.

## repo-rule compliance
- Write-set strictly limited to `internal/deployment/deployment_owner_binding_test.go`. No produktcode change, no .github change.
- Test-only; no product seam modification. If load/save/list let missing owner through silently ⇒ END_BLOCKED with captured output (real product finding).

## TEST RESULTS

**Base:** 797bd811e2dec5c60fe58f27e738d6fc0314cbb8, branch work/r27-state-owner. Isolated worktree at /tmp/opencode/w30-stateowner-r9-wt.
**Go:** go1.26.9. GOCACHE=/var/tmp/go-cache, TMPDIR=/var/tmp (tmpfs /tmp and /tmp/opencode at disk quota; /var/tmp writable).

Behavior probe (throwaway, removed) confirmed for the "missing owner WITH existing record" case — Core installation.json removed while the deployment.json record survives:
- LoadDeploymentRecord => ErrDeploymentOwnerMissing (missing=true, not foreign)
- SaveDeploymentRecord (nil preferences) => wrapped ErrDeploymentOwnerMissing (missing=true)
- ListDeployments => ErrDeploymentOwnerMissing (missing=true; NOT a silent empty listing)
- Record bytes unchanged after all three operations.

**New test:** `TestDeploymentOwnerMissingOnExistingRecordSeam` in `internal/deployment/deployment_owner_binding_test.go`.
- (1) provisions owner for "local", saves a real record via the real save path, captures record bytes.
- (2) removes ONLY installation.json (owner material) while the record file stays on disk.
- (3) asserts Load/Save(nil)/List all fail closed with the SPECIFIC `ErrDeploymentOwnerMissing` and record bytes are byte-identical after each.
- Existing empty-list test (`TestDeploymentOwnerSeamEnforcedOnRealSaveLoadList`, owned-but-empty target) remains beside it.

**Go runs:**
- `go test ./internal/deployment -count=1` => **ok** (PASS), includes the new test.
- `go test ./internal/deployment -run 'Owner|List|Deployment'` => **ok**.
- `go test ./cmd/baha -count=1 -run 'Owner|List|Deployment'` => all pass EXCEPT `TestExternalProviderRemovalCannotInferGlobalOwnershipFromTenantRole` fails with `provider-registry-ownership-unverifiable` — **pre-existing, fails identically on clean develop 9a57107f** (verified), matching review-1347h §3. No green cmd gate without noting this; it is an environment failure, not caused by this change.
- `go test ./cmd/baha -run 'Owner|List|Deployment' -skip 'TestExternalProviderRemovalCannotInferGlobalOwnershipFromTenantRole'` => **ok**.

## repo-rule compliance
- Write-set strictly limited to `internal/deployment/deployment_owner_binding_test.go` (test-only). No produktcode change, no .github change.
- No product seam modification. Load/Save/List reject missing owner with a concrete `ErrDeploymentOwnerMissing` — never silently admit. NOT an END_BLOCKED case.

## END
DONE w30-stateowner-r9: head=33badf7d missing-owner-public=load+save+list bytes=same (all ErrDeploymentOwnerMissing) | task complete; my tested candidate 33badf7d already on remote work/r27-state-owner, my linear-across-develop variant identical. Concurrency churn on branch (Owner + other workers rewinding) — no force-push; Owner should let CODEX review/accept 33badf7d.

## BRANCH / CONCURRENCY FINDINGS (final)
- Owner clarified: NO rewind. `merge-base --is-ancestor 797bd811 20f32c8f = YES`; Owner CI #1349 only *added* the replan commit `20f32c8f` on top of base `797bd811`.
- Following instruction: rebased my test onto `20f32c8f` (`6e174092`), then onto CURRENT develop `e90d7436` (`ac18e9bc`) per mission's "land on latest develop" requirement. Ancestry rc=0 both times. Test-only +103 line diff; no produktcode/.github.
- Remote `work/r27-state-owner` kept advancing via OTHER actors (Owner + other workers), bouncing between `20f32c8f`, `33badf7d`, back to `33badf7d`. Force-push rejected (non-FF) to avoid clobbering concurrent work.
- FINAL remote tip = `33badf7d`, which **already contains my exact tested missing-owner test** (byte-identical to mine). Verified `go test ./internal/deployment` on `33badf7d` = ok.
- My local linear variant `ac18e9bc` = identical test on top of current develop; no push needed — candidate already present and green at `33badf7d`.
- Recommend: Owner lets CODEX review/accept `33badf7d` (or re-merge onto current develop if the integration base must be latest develop). No further action from this worker.

## BRANCH / CONFLICT FINDINGS (pending Owner decision)

**Task fully implemented and tested in isolated worktree /tmp/opencode/w30-stateowner-r9-wt:**
- New test `TestDeploymentOwnerMissingOnExistingRecordSeam` (adds +103 lines to `internal/deployment/deployment_owner_binding_test.go`, only file changed).
- `go test ./internal/deployment -count=1` => ok (new test passes).
- `go test ./cmd/baha -count=1 -run 'Owner|List|Deployment'` => all pass except `TestExternalProviderRemovalCannotInferGlobalOwnershipFromTenantRole` fails with `provider-registry-ownership-unverifiable` — PRE-EXISTING on clean develop 9a57107f (verified), matches review-1347h §3. Not caused by this change.
- Write-set strictly test-only; no produktcode/.github change.

**Remote branch state (the blocker):**
- Base was 797bd811 (branch work/r27-state-owner).
- I committed 33badf7d on top of 797bd811 and tried to push to refs/heads/work/r27-state-owner.
- Push REJECTED: remote advanced to 20f32c8f (author **Marcel Pfingstgräf / Owner**, "ci: replan unchanged product source after CI routing fix #1349").
- 20f32c8f is on top of the ORIGINAL 797bd811 (metadata-only commit; product source unchanged) and the test file is byte-identical to base — i.e. my test was reverted and the Owner rewound/repurposed the branch.
- My commit 33badf7d (parent 797bd811) is a clean sibling addition; it is NOT reachable from 20f32c8f (true divergence).

**Why I STOPPED instead of force-pushing:**
- AGENTS.md §3.6/§5.6: an Owner branch/decision has priority; no force-push or branch-protection bypass. The branch is now owned by the Owner and my change is reverted.
- Two plausible Owner intents: (a) the missing-owner seam is being handled by an Owner/candidate branch (possible parallel run), or (b) the task was pulled back for replanning. Either way the push target and desired candidate are Owner decisions — I must not guess.

**Evidence is preserved** (worktree + commit 33badf7d + this file) so the tested candidate can be re-applied verbatim if the Owner confirms the branch is the right target.

