# 0427-173 round 8 — base-refresh onto develop 942111d5a (readability ratchet resolved by split)

**Card:** 0427-173 · `t-20261108-bughunt-app-prune-dangling-record`
**PR:** https://github.com/mcpdev80/baseharbor/pull/1505 (head `a42822f542436651a6f0df94f574574632648dc8`)
**Driving review (r7): KORREKTUR — content correct, HALT only because develop `942111d5a` was not an ancestor** (act-1505-review-r7.md, vm-bughunt/, plan)

## PLAN

- Rebase the 0427-173 prune branch onto develop `942111d5a` (single linear chain of 8 commits, no conflicts — the #174 permission-lies edits sit above my prune additions, resolved side-by-side).
- Preserve r7 drift-guard content byte-for-byte; keep `app_prune.go` / `app_prune_test.go` semantically unchanged.
- The rebase brought develop's #174 growth into `deployment_store.go` (798 → 838 lines), tripping `scripts/source-readability-audit.sh` regression ratchet. Resolve by splitting the cohesive drift-protected deletion (`DeleteDeploymentRecord` + `assertOnDiskIdentityMatches`) into a new `internal/deployment/deployment_identity_drift.go` — a refactor of my own file's organization, no semantic change, no `.github/**`.
- Local: gofmt/vet/build + readability audit + prune/destroy/maintenance/deployment-package green.
- Force-push with lease, observe hosted CI terminal on the exact head, publish round-8 evidence, END (terminal only).

## The r7 blocker (now cleared by rebase)

r7 head `67e723fb` was a linear child of develop `b3a8042d`. By the r8 window develop had moved to `942111d5a` (incorporating #1502/#1504/#1506). The r7 review confirmed the content correct; the only halt was that develop `942111d5a` was not my ancestor. r8 is a base-refresh only: rebase the 8-commit linear chain onto `942111d5a`, content unchanged.

## Rebase — side-by-side, no conflicts

`git rebase 942111d5a` replayed all 8 commits cleanly (no conflict markers). The overlap region is `internal/deployment/deployment_store.go`: develop's #174 (permission-lies: distinguishes access-denied / malformed / foreign) edits land at the top of the file; my r7 drift additions (`DeleteDeploymentRecord` / `assertOnDiskIdentityMatches`) sit at the bottom and are untouched. `app_context.go` #1506 classification merged in without conflict; verified identical between my r7 head and the rebased tree.

## The readability-ratchet fix — split, not rewrite

The DEVELOPMENT_GUIDELINES (§Code layout) require a non-test Go file ≤ 800 lines: "Split by responsibility before adding more behavior." develop `942111d5a` alone had `deployment_store.go` at 798 lines (already at the edge). The #174 block stacked ~19 lines above my unchanged r7 additions → 838, tripping the regression ratchet.

Fix: extract the cohesive drift-protected-deletion responsibility into a new file:

- `internal/deployment/deployment_identity_drift.go` (new, 58 lines): `DeleteDeploymentRecord` + `assertOnDiskIdentityMatches`.
- `deployment_store.go`: both functions removed verbatim (−47 lines: 19 + 28) and the now-unused `internal/machine` import dropped → 790 lines (≤ 800).

The two functions are **byte-identical** to the r7 originals (verified by `diff` against `git show 67e723fb:internal/deployment/deployment_store.go`): idempotency, `DEPLOYMENT_RECORD_MALFORMED`, `DEPLOYMENT_RECORD_VERSION`, and `IDENTITY_DRIFT` (`machine.ErrorOwnershipAmbiguous`) guards are unchanged. `DeleteDeploymentRecord` still calls `assertOnDiskIdentityMatches` in the same package — the registered MCP prune handler's resolve/authorize/mutate path is untouched. `app_prune.go` and `app_prune_test.go` are byte-identical to r7.

## Regression catches the fix (after split)

Neutering `assertOnDiskIdentityMatches` (return nil first line) in the new file makes the registered handler delete the drifted record → `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation` FAILS. Restoring → PASSES. The on-disk guard still rejects a post-authorization drift, not an in-memory comparison (172-r2).

## Local verification (after split + push prep)

```
$ go build ./...
BUILD OK
$ gofmt -l cmd/baha/app_prune.go cmd/baha/app_prune_test.go internal/deployment/deployment_store.go internal/deployment/deployment_identity_drift.go
(gofmt clean)
$ go vet ./internal/deployment/... ./cmd/baha/...
(no output)
$ bash scripts/source-readability-audit.sh
Source readability
Go file size       PASS (<= 800 lines or no worse than explicit baseline)
Function span      PASS (<= 200 lines or no worse than explicit baseline)
Regression ratchet PASS
$ go test ./internal/deployment/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/deployment	0.053s
$ go test ./cmd/baha/ -run 'TestAppPrune|TestDestroy|TestMaintenance|TestRepositoryAdopt|TestInstallation' -count=1
ok  	github.com/mcpdev80/baseharbor/cmd/baha	21.112s
$ go test ./cmd/baha/ -run 'TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation' -count=1
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.010s
```

`deployment_store.go` 790 lines (≤ 800); new file 58 lines. **No `.github/**`** touched. Files changed on the r8 chain vs develop: the full prune feature chain (`app_prune.go`, `app_prune_test.go`, `app_context.go`, `machine/contract.go`, docs) plus the two deployment files — a rebase, not new behavior.

> Note: the 16 `init`/`guided-init`/`app-edit` data-corruption tests (e.g. `TestDeterministicInitDoesNotPersistUnneededSourceSelection`) fail on clean develop `942111d5a` itself — pre-existing, unrelated to this change. They are not in scope for the prune drift fix and were not introduced by r8.

## Push + hosted CI — TERMINAL SUCCESS

Single linear integration chain directly on develop `942111d5a` (ancestor proven; `git merge-base --is-ancestor 942111d5a HEAD` ⇒ YES). Push:

- Push: `git push --force-with-lease origin r8-refresh:refs/heads/fix/0427-173-app-prune` ⇒ `b50fed12..a42822f5`
- Remote tip after push: `a42822f542436651a6f0df94f574574632648dc8`
- Working tree clean after push.

Hosted CI — run **42590616765**, head `a42822f5`, overall **completed / success**:

| Job | Conclusion |
| --- | --- |
| PR · Native impact selection | success |
| PR · Trusted Plan | success |
| PR · Source format | success |
| PR · Native destroy retry · podman | success |
| PR · Native destroy retry · docker | success |
| PR · Focused Python | success |
| PR · Validation · mkdocs-de-strict | success |
| PR · Validation · documentation-audit | success |
| PR · Validation · pages-candidate-build | success |
| PR · Validation · deployment-package-tests | success |
| PR · Validation · cli-gofmt | success |
| PR · Validation · go-unit-tests | success |
| PR · Validation · go-build | success |
| PR · Validation · go-vet | success |
| PR · Validation · mkdocs-en-strict | success |
| PR · Validation · wizard-registration-tests | success |
| PR Selected Checks | success |

No job failed. The previously-failing **PR · Source format** now passes (the readability ratchet is satisfied by the split); **go-unit-tests** is executed (success) and includes `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation`. `deployment-package-tests` (runs `internal/deployment` including the on-disk identity guard) is success. Skipped cells are legitimately skipped in this zone — native runtime cells need the isolated verified runtime prerequisite not available here (reported skipped, not green); contract/proof cells (Public Contracts, Consumer Pins, Exact Candidate, Demo Pin, Runner Interface, Selected Runtime, Native Keycloak/Core) are skipped because no shared contract changed.

## END

END_PASS 0427-173-r8: the r7 halt is cleared — the branch is rebased onto develop `942111d5a` (ancestor proven) with r7 drift-guard content preserved byte-for-byte. The readability ratchet tripped by #174's line growth was resolved by splitting the cohesive drift-protected-deletion responsibility into `internal/deployment/deployment_identity_drift.go` (no semantic change, no `.github/**`, `deployment_store.go` back to 790 lines ≤ 800). The handler (not the test) performs the mutation and refuses `IDENTITY_DRIFT`; the replacement record is left byte-identical. The regression is proven (neuter the guard → the handler deletes the drifted record and the test FAILS). Candidate `a42822f5` pushed to `fix/0427-173-app-prune` (linear chain on develop, no `.github/**`), hosted CI run **42590616765** terminal on that exact head (conclusion: success, no job failed). END only now, because the required hosted CI is terminal — END was not claimed as a pass until run 42590616765 completed.
