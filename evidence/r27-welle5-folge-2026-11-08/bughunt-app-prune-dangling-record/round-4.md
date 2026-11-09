# 0427-173 round 4 — MCP identity stability, applied-intent byte snapshot, one-name docs, base refresh

**Card:** 0427-173 · `t-20261108-bughunt-app-prune-dangling-record`
**PR:** https://github.com/mcpdev80/baseharbor/pull/1505 (head `bcdede014979de5692b2879eb6ddcd17141c2677`)
**Reviewer verdict (r3):** KORREKTUR; approval withheld (act-1505-review-r3.md, vm-bughunt/, plan a236d382)
**Goal of round 4:** close the four open points of the r3 review: (1) carry the authorized deployment identity through authorization AND mutation, (2) snapshot record bytes before the CLI call, (3) remove stale `--uuid`/`-e` selector claims from prune, (4) integrate current develop HEAD `b3a8042d1`.

## PLAN

- Verify live PR head (bcdede01), develop (b3a8042d1), ancestry, candidate origin
- Fix 1: carry authorized resolved identity through authorization AND mutation (no re-resolve in MCP path); add drift regression
- Fix 2: read before-snapshot BEFORE runWithIO for applied-intent byte preservation
- Fix 3: prune stale --uuid/-e from app_prune.go (docs -e for OTHER commands stay)
- Fix 4: rebase candidate on current develop HEAD b3a8042d1
- Local tests: all prune + golden + doc tests green; go vet; go build; gofmt -l clean
- Push candidate, observe hosted CI terminal on exact head (native cells skipped allowed, report as skipped)
- Publish round-4 evidence to baseharbor-plan origin/main; END (terminal only)

## Reality witnesses (before any change)

- Live PR #1505 head (remote, own persistent zone):
  ```
  git -C /tmp/opencode/0427-173-r2-wt ls-remote origin refs/pull/1505/head
  bcdede014979de5692b2879eb6ddcd17141c2677	refs/pull/1505/head
  ```
- develop drift: live `git ls-remote origin develop` => `b3a8042d18ea60f162a32a51df34a499cad6a237`.
- Base attestation: candidate is cut from `bcdede01` (the exact PR #1505 head r3). `b3a8042d1` (current develop) is NOT yet an ancestor of the candidate — integrate before push.

## Fix 1 — MCP identity carried through authorization AND mutation

r3 re-resolved by name after authorization, so a same-name replacement on the
target between authorize and delete could redirect the deletion. Refactored
`executeApplicationPrune` to resolve once and delegate to a new
`executeApplicationPruneResolved(..., *deployment.DeploymentIdentity)`; the CLI
path passes `nil` and deletes the record it just resolved, the MCP path passes
the authorized identity and the deletion is guarded by `identitiesMatch`.

- `cmd/baha/app_prune.go`:
  - `identitiesMatch(resolved resolvedApplication, authorized deployment.DeploymentIdentity)` compares all five identity fields (Target, DeploymentID, ApplicationID, Application, Environment) and fails closed with `IDENTITY_DRIFT` / `machine.ErrorOwnershipAmbiguous` on drift.
  - `executeApplicationPruneResolved` deletes `*authorizedIdentity` when non-nil (guard first), else the just-resolved record.
  - MCP handler pins `authorizedIdentity := resolved.DeploymentIdentity` and passes `&authorizedIdentity` to `executeApplicationPruneResolved`.
- Regression (direct `executeApplicationPruneResolved` unit test `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation`): single uniquely-named record `solo` on `boot`, resolve+authorize it, then rewrite the SAME deployment dir on disk with a different `ApplicationID` (drift); re-resolve → resolved identity is drifted, authorized is original → assert `IDENTITY_DRIFT` cause, guarded message, and the drifted on-disk bytes unchanged after the refused prune. A happy-path MCP call (`TestAppPruneMCPHappyPathRemovesUniquelyResolvedRecord`) proves the normal path still removes a uniquely-resolved record.

## Fix 2 — applied-intent byte snapshot BEFORE the CLI call

`TestAppPruneRefusesDanglingRecordWithAppliedIntent` now reads the on-disk
record bytes as `before` BEFORE the `runWithIO` CLI call, asserts the call
refuses with the applied-intent guard, then asserts the on-disk bytes are
byte-identical to `before` (record preserved). The snapshot is captured before
any CLI side effect — the contract the r3 review asked for.

## Fix 3 — one-name contract made honest in docs

Removed the stale `--uuid`/`-e` selector claims from prune help/docs. The
parser `requirePruneName` already rejects ALL flags and accepts exactly one
positional name, so those claims were false. Kept the general `-e/--environment`
docs on OTHER commands intact (`-e` is only wrong for prune). Ambiguous-name
Next text now states prune refuses an ambiguous name until it selects exactly one
deployment, matching the parser.

## Fix 4 — base refresh on current develop

Candidate rebased from `bcdede01` onto develop HEAD `b3a8042d1` (target-delete
`--yes` non-TTY fix #1494). The develop commit touches only target-delete files
and golden/contract docs — no prune files — so the rebase was clean.

- New candidate head: `602bf1720ea77d2194c8b6b57739891d678022af`
- `git merge-base --is-ancestor b3a8042d1 HEAD` => YES
- `git diff bcdede01 origin/develop --stat` confDelta confined to target-delete + contract docs.

## Local verification (after Fix 4)

```
$ go build ./...
BUILD OK
$ gofmt -l cmd/baha/app_prune.go cmd/baha/app_prune_test.go
(gofmt clean)
$ go vet ./cmd/baha/
(vet clean)
$ go test ./cmd/baha/ -run 'TestAppPrune|Golden|Doc' -count=1
ok  	github.com/mcpdev80/baseharbor/cmd/baha	3.446s
```

All prune tests green:
`TestAppPrune*` (IsRegisteredAndRefusesLiveSource, RemovesDanglingRecord, RefusesMultipleMatches, RefusesRecordWithAppliedIntent, RefusesNoName, RefusesMultipleNames, JSONOnlyValid, HumanHasNoJSONTrailer, LiveSourceUnchangedOnRefusal, RefusesDanglingRecordWithAppliedIntent, MCPPreservesTargetOverride, MCPIdentityStabilityThroughAuthorizationAndMutation, MCPHappyPathRemovesUniquelyResolvedRecord) plus the golden and doc tests.

## Push + hosted CI — PENDING

Candidate rebased and locally verified. Not yet pushed. Hosted CI is terminal only after the push is observed on exact head `602bf1720…`. Native runtime cells skipped in this zone (isolated runtime prerequisite); skipped cells are reported here as skipped, not as green.

## END

END_PENDING 0427-173-r4: code complete, rebased onto develop, locally verified (build/vet/gofmt/test). Pending push + hosted CI terminal.
