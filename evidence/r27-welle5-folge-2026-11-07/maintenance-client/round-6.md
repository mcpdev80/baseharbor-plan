# 0427-034 maintenance client — round 6

Task: t-20261018-r27-maintenance-client · lane 0427-034-maintenance-r6 (flash, session 72cd7871) · PR #1428.
6th attempt on the same card. The reviewer recheck (act-1428-review.md, "R5 contradiction recheck",
planning origin/main 69c2c84979c4f3989f96a4f84e0a0064fc3e1b77) rejected the r5 contradiction with two
concrete code findings. This round fixes both in production code and in the matrix.

## PLAN

1. Create the numbered work plan in all visible places (todowrite: the tool is not exposed in this
   session, so per mission instruction leg (0) was skipped; board file
   workers/todos/0427-034-maintenance-r6.json created and ticked; this ## PLAN list). — done
2. Read the recheck text of act-1428-review.md verbatim from planning origin/main. — done
3. Verify the claim on planning origin/main (owner=lane-0427-034-maintenance-r6, active; the
   coordinator published the transition per owner ruling; verified after fetch). — done
4. Fettle the worktree from the named candidate branch head 396529860e1f; attest base SHAs and
   develop ancestry. — done
5. Add the real tombstone replay reader: production revision lookup consumes the committed
   tombstone after teardown; the maintenance replay route answers a committed revision idempotently,
   local and remote. — done
6. Fix the all-exit matrix: owner-failure rows carry the retry/replay oracle in the correct
   direction, the duplicated block is removed, the faithful owner tears down before failing. — done
7. Regression tests call the reader path (production lookup/route), not writer helpers. — done
8. Targeted local verification: maintenance package tests, causal mutant probes red, full-package
   diff against the same base is identical to base behavior. — done
9. Develop drift refresh (coord directive during work): merge origin/develop 0fe53052d into the
   candidate, re-verify ancestry and tests. — done
10. Push the named candidate branch (fast-forward, no force), ls-remote witness. — done
11. Watch the hosted CI run to a terminal state and record it here (self-run duty). — in progress
12. Publish this evidence to baseharbor-plan origin/main, verify it in origin/main, post END. — in progress

## Wrong-zone and root verification (mission mandate)

Output of `git -C /tmp/opencode/0427-034-maintenance-r6-plan rev-parse --show-toplevel`:

```text
/tmp/opencode/0427-034-maintenance-r6-plan
```

The clone's origin fetch/push is `https://github.com/mcpdev80/baseharbor-plan.git` (witnessed via
`git remote -v` above). The workers/baseharbor-plan directory was NOT used for evidence.

## Base attestation and provenance

- Refs fetched at worktree start: `refs/heads/develop` = `8a3f58da905fad52327d33466fde1d9568092519`,
  `refs/heads/lane/0427-maintenance-client-wt` = `396529860e1f349576190f435cb06e2b7b496866`
  (= PR #1428 head, same SHA, confirmed by `git ls-remote https://github.com/mcpdev80/baseharbor.git`).
- Branch cut: the candidate continues the named mission branch at `396529860e1f` (fast-forward from
  the r4 head; the mission names this branch and SHA as the basis). Ancestry of this cut base into
  the first commit: `4c37c8e6ab06e1f8cd1bf229f37a45a2e890a5f6^` chain includes `396529860e1f`
  (witness `git log --format='%H %an %s' origin/develop..HEAD` after the final push:
  `9548239d` → `efd09991` (merge) → `4c37c8e6` → `396529860e1f` → card's earlier rounds).
- `git merge-base --is-ancestor refs/remotes/origin/develop HEAD` at the cut base returned 0
  (develop `8a3f58da` is an ancestor of `396529860e1f`), witnessed during the worktree fettle.
- Own commits over the mission base: exactly one fix commit `4c37c8e6ab06e1f8cd1bf229f37a45a2e890a5f6`
  plus the base-refresh merge `efd099912225ad407fd36455c99f1b40d264038a` (see drift section). The
  other commits in `develop..head` are the card's own earlier-round commits on this same branch
  (r2–r4, documented in the card handoff), not a foreign candidate.
- Drift refresh (coordinator notice during CI observation): `origin/develop` moved to
  `0fe53052d00a8d440b499c66a6a65c0d54bae5a0` (PR #1438 integration). Merged into the candidate before
  the final push; `git merge-base --is-ancestor origin/develop HEAD` returns 0 at the pushed head
  `efd09991`. `8a3f58da` is an ancestor of `0fe53052` (witnessed). Post-merge the full candidate
  write-set vs develop is 12 files, all `cmd/baha/*maintenance*` or
  `internal/application/maintenance_*` (witness of `git diff --name-status origin/develop...HEAD` in
  the push transcript) — no `.github/**`, no scripts, no fixture collision paths; the #1436/#1435
  traces inside develop are base content, not this candidate's diff.

## What was wrong at 396529860e1f (reviewer recheck, read verbatim)

1. Retry oracle inverted/duplicated in `cmd/baha/app_maintenance_round4_test.go`: the
   `local-owner-failure` / `remote-owner-failure` rows did not set `retryableAfter`, the duplicated
   `if exit.retryableAfter` blocks asserted a FAILED commit (their comments say the retry must
   commit cleanly), and the only retry-enabled rows were history-append failures whose hook stayed
   armed — so both retry checks could only pass when the retry was refused.
2. The tombstone had no production replay reader: `loadMaintenanceRevision`
   (`internal/application/maintenance_history.go`) read only the current window and history beneath
   `stateRoot`, and `maintenanceTombstonePath` was used only by the writer and tests.

## What this round changes

- `internal/application/maintenance_history.go`
  - `loadMaintenanceRevision` gains the tombstone fallback: when the durable window/history reads
    fail with a missing root (the torn-down destroy condition) or the root holds no record of the
    revision for a deployment that no longer exists, the lookup consults the committed destroy
    tombstone via `maintenanceTombstoneRevision`, keyed by the (target, deploymentID) identity the
    state root names. Malformed, oversized, foreign (identity-mismatched) or contract-invalid
    tombstones fail closed. An unregistered reader is an explicit fail-closed error, never silence.
  - `SetMaintenanceTombstoneReplay(resolvePath, ownedRoot)` wires production; `ownedRoot` binds the
    fallback to installation-owned state roots only (path prefix under the data root + well-formed
    identity + the one-installation-owner rule via `VerifyDeploymentOwner`), so an arbitrary caller
    path can never be answered from a tombstone.
  - `LoadMaintenanceRevision` exported as the production replay lookup (the existing
    `LoadMaintenanceRevisionForTest` seam stays).
- `cmd/baha/app_maintenance_client.go`
  - `init()` registers the reader (path resolver + ownership predicate): the writer and reader now
    share one layout function so they cannot disagree.
  - New replay route: `applicationMaintenanceOptions.Revision` > 0 routes
    `submitApplicationMaintenance` to `replayApplicationMaintenance`, which answers the committed
    revision through `maintenanceRevisionReplay` (the seam onto
    `application.LoadMaintenanceRevision(resolved.stateRoot(), revision)`) and prints the
    machine-safe `maintenanceReplayView`. It invokes no lifecycle owner and writes nothing —
    idempotent by construction. An unknown revision fails closed. This is the 'maintenance
    status/replay reads the committed tombstone' route (command/flag registration itself stays
    with t-20261018-r27-public-surfaces, per its card boundary).
  - Destroy routes (local + remote) treat `errMaintenanceOperationAlreadyRecorded` from the
    up-front commit as the durable answer it is: the same destroy revision re-submitted resolves to
    the retained record instead of erroring or double-stamping.
- `cmd/baha/app_maintenance_round4_test.go` (the matrix fix)
  - The faithful owner now performs the real teardown and THEN reports the injected owner failure,
    so the rollback path is exercised against torn-down state.
  - Owner-failure rows carry `retryableAfter` (correct direction, once). The duplicated
    `if exit.retryableAfter` block is removed.
  - Success rows assert the committed destroy revision through the PRODUCTION replay lookup
    (reader path), never a bare `os.ReadFile`; the direct read survives only as a source check of
    the durable artifact content.
  - Failed rows additionally assert the aborted revision answers NOTHING through the production
    lookup, and the retry commits cleanly (isNew), which is the residue oracle.
  - New `TestApplicationMaintenanceHistoryRemovalMutantRedOnOwnerFailure`: the isolated mutant that
    keeps current-window rollback but disables ONLY the history-removal half makes the owner-failure
    regression red (residue answerable + retry refused), as the recheck recipe requires.
  - New `TestApplicationMaintenanceTombstoneReplayWiringIsLoadbearing`: unregistering the reader
    makes the production lookup fail closed — the no-reader mutant — and the replay route reports
    it. Green with production wiring.
  - New replay-route regressions (local, remote, unknown-revision): they call the reader route, not
    the writer helpers.

## Local verification

- `go build ./...`, `go vet ./cmd/baha ./internal/application`, gofmt clean on touched files.
- `go test ./cmd/baha ./internal/application -run Maintenance` — pass (post-merge, -count=1).
- Causal probes (throwaway source mutations, reverted immediately):
  - removing every `maintenanceTombstoneRevision` fallback → matrix success rows and the replay
    route regressions go RED (witness: "replay pass 0 failed: … no durable maintenance record at
    revision 1", matrix FAIL).
  - no-oping only the history-removal call in `RollbackMaintenanceAuthorityWindow` →
    `TestApplicationMaintenanceHistoryRemovalMutantRedOnOwnerFailure` goes RED (witness:
    "the fixed rollback left an answerable aborted revision: found=true").
- Full `go test ./cmd/baha` failure set on the candidate is byte-identical to the failure set on the
  current `origin/develop` (13 pre-existing init/owner-loan failures caused by polluted state on
  this coordinator host: `/home/marcel/.local/share/baseharbor/targets/p427-podman-boot/...` —
  environment noise, not product drift; diff witness `SAME-AS-NEW-DEVELOP`). Maintenance suites are
  green in both runs.

## CI capture statement (mission: new tests must run in GitHub CI)

All new tests live in `cmd/baha` / `internal/application` and are executed by the existing hosted
`PR · Validation · go-unit-tests` job (`go test ./...`), triggered on pull-request changes to this
PR. No `.github/**` change is needed or made.

## Hosted CI (self-run duty)

- Run `42427948430` on head `efd09991` — `PR · Source format` FAILED with the STATE line:
  `source readability: cmd/baha/app_maintenance_client.go has 898 lines (limit: 800; baseline ratchet: 0)`;
  the rest of the run was cancelled as superseded (in-progress go-unit-tests at cancellation).
  The r6 additions had pushed the client file past the repository size limit.
- Fix: commit `9548239d85254595054337b17736b3b8941d0133` splits the replay route into
  `cmd/baha/maintenance_replay.go` and the destroy-tombstone durability block into
  `cmd/baha/maintenance_tombstone.go`; no behavior change; `bash scripts/source-readability-audit.sh`
  passes locally before the push.
- Run `42428326653` ("CI · Source & Quality", PR #1428) on the exact terminal head `9548239d852`:
  completed SUCCESS. Terminal jobs (witness `gh run view --json jobs`): `PR · Source format`,
  `Workflow policy`, `PR · Trusted Plan`, `PR · Focused Python`, `PR · Validation · cli-gofmt`,
  `PR · Validation · go-build`, `PR · Validation · go-vet`, `PR · Validation · go-unit-tests`
  (the job that runs the new tests), `PR Selected Checks` — all success. Targeted HA docker/podman
  skipped (fixture-level unit card, no native paths touched). Observed to completion by this lane.

## repo-rule compliance

- One candidate, one branch: all work on `lane/0427-maintenance-client-wt`, pushed fast-forward
  (no force). No second branch was created.
- Delta confined to maintenance files; no command/schema registration, no `.github/**`, no shared
  fixtures touched; public-surface registration remains with t-20261018-r27-public-surfaces.
  The `PR · Source format` size failure was fixed INSIDE the same write-set (two new
  maintenance-prefixed files) — no Owner-scope change was needed.
- No subagents; no containers/VMs/runner actions (none needed: unit-level durable-state behavior).
- Test-run pollution (`conformance/provider/v1/testdata/external/go.mod` indirect-require churn
  from a local nested-module probe) was restored before the push and never committed.
- This evidence contains no markdown checkbox lines.

## Remote witnesses

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane/0427-maintenance-client-wt refs/pull/1428/head` after the final push:

```text
0fe53052d00a8d440b499c66a6a65c0d54bae5a0	refs/heads/develop
9548239d85254595054337b17736b3b8941d0133	refs/heads/lane/0427-maintenance-client-wt
9548239d85254595054337b17736b3b8941d0133	refs/pull/1428/head
```

## END

END_DONE 0427-034-maintenance-r6: tombstone replay reader wired into the production lookup + corrected retry/replay oracle in the all-exit matrix; candidate 9548239d85254595054337b17736b3b8941d0133 on PR #1428, develop 0fe53052d ancestor, CI run 42428326653 terminal success on the exact head.
