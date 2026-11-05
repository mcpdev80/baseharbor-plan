# CODEX-REVIEW — device lifecycle, PR #1394 round 2

- Review date: 2026-11-05
- Verdict: **REJECT** — the new HTTP lifecycle path works in a reviewer probe and the real production revocation guard is mutation-sensitive, but the required durable-registry-after-restart proof is absent.
- Candidate: `70acac6b226f6a84d958f0c47c10353610ed6c4d`
- Base: `develop` `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`; `git merge-base --is-ancestor origin/develop <candidate>` returned rc=0.
- PR #1394: open, branch `work/r27-device-lifecycle`; `git ls-remote origin refs/heads/work/r27-device-lifecycle` returned the exact candidate SHA.
- Hosted run [42115737016](https://github.com/mcpdev80/baseharbor/actions/runs/42115737016): terminal `completed / success` at the exact candidate.
- `git diff --name-only origin/develop...<candidate>` contains 14 paths, all within the device lifecycle contract, handler, authority, local issuer, registry store and associated tests. No `.github` paths.

## Verification

1. **HTTP lifecycle path:** source confirms `ProductionHandler.ServeHTTP` routes `/renew` and `/revoke`, and those handlers call `workstationlifecycle.RenewDevice` / `RevokeDevice` through the `authorityLifecycle` adapter with a `ScopeResolver`-bound scope. The checked-in `TestRenewPersistsNewSerial` drives `/enroll` then `/renew`, but uses `renewEnrollment` with an in-memory `ownerCapturingSerial` and an in-memory `persistedSeq`. `production_handler_test.go` has no `/revoke` test. I ran the checked-in renew persistence test successfully.
2. **Reviewer HTTP probe:** in an isolated candidate worktree I added and then removed a temporary probe test. It exercised the actual `ProductionHandler` with a real `serviceaccess.LocalIssuer`: `/bootstrap` → `/enroll` → `/renew` → `/revoke` → `/renew`. It passed: the renewed serial changed, became the owner serial, revoke made it revoked, and subsequent HTTP renew returned 403. The registry owner in this probe was in memory; this is not durable restart evidence and was not added to the candidate.
3. **A/B/C matrix and baseline control:** `go test -race -count=20 ./internal/workstationenrollment -run '^(TestRenewMatrixDoesNotTouchBAndC|TestRevokeMatrixDoesNotTouchBAndC|TestMutantSecurityCellRED)$'` — `ok` (5.341s). This is the unmutated green control and covers the A/B/C unit cells with the real CRL-backed LocalIssuer.
4. **Real production guard mutant:** in a separate isolated worktree I removed the current-leaf `RevokedStatus` guard from the production `Authority.Renew`, then ran `go test ./internal/workstationenrollment -run '^TestMutantSecurityCellRED$' -count=1`. It went red at `lifecycle_test.go:371`: `production Renew must refuse a revoked scope; the RevokedStatus guard is the security cell`. The mutation was confined to the disposable worktree. Thus the guard-removal test is discriminating against an actual production-code mutation; the unchanged candidate passed the same cell in the race-20 run.
5. **Renewed serial persistence after restart: not proven.** The checked-in `TestRenewPersistsNewSerial` reads a test double's in-memory `persistedSeq` and `ownerCapturingSerial`, not `WorkstationEnrollmentStore`. The database integration test exercises registry read/write generally, but does not do an HTTP renewal, reopen a second store after that renewal, and assert the renewed serial is still current. `BASEHARBOR_TEST_DATABASE_URL` is not configured here, so I could not run the PostgreSQL test. The required restart persistence cell therefore remains missing.
6. **Enrollment/authority boundary blobs:** `internal/workstationenrollment/store.go` is unchanged at blob `3885afe56432ba3b767429bfddf63f4a8a7455db`; `scope.go` unchanged at `cca602b838016506ea5e3f8b66b30c2c0debb855`; `internal/serviceaccess/authority.go` unchanged at `a69559e01f9b4bd7a6c3df38d9eb3f757cfe0dca`. The workstation lifecycle authority, handler and local issuer additions are in the task's bounded diff.

## Correction recipe

- Add a database-backed integration cell that performs the real authenticated HTTP enroll and renew, records the renewed serial through `RecordRegistryFact`, opens a fresh `WorkstationEnrollmentStore`/pool, reads `CurrentSerial`, and asserts it equals the renewed serial (and differs from the enrolled serial). Run it with the configured test PostgreSQL service.
- Add a checked-in HTTP `/revoke` plus post-revoke `/renew` regression, using a real CRL-backed issuer and the production handler; assert revoke targets only A and renewal is refused after revocation. The reviewer probe above is not a substitute for a committed regression.
- Keep the current production guard. Re-run these cells, the mutation red/control pair and hosted gates at the final exact SHA.

No candidate files changed. Temporary reviewer probe and mutation were isolated and removed. No PR action was performed.

## Remote publication witness

- After the initial evidence commit, `git ls-tree origin/main -- evidence/r27-welle5-2026-11-05/device-lifecycle/review-1394b.md` returned `100644 blob f78b37e3790e8906222d8ea550a80f4179283001 evidence/r27-welle5-2026-11-05/device-lifecycle/review-1394b.md` at `origin/main` `5838e11597cff7883bd6da3ab21e1a32874ac2d3`.
- This witness was added to the akte and pushed in a receipt commit; final fetch and `ls-tree origin/main` verified the updated file entry.
