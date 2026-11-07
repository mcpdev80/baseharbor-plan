# 0427-maintenance-client-r2 — Evidence round 2 (t-20261018-r27-maintenance-client)

Worker lane `0427-maintenance-client-r2`. Coordinator session `594fd2f5-4e80-43b6-9841-92879146a85e`.
Repository `mcpdev80/baseharbor`, branch `lane/0427-maintenance-client-wt`, PR #1428 against `develop`.

This is a round-2 correction lane. It continues the already-published candidate from round 1
(`round-1.md`) and addresses the CODEX-REVIEW REQUEST-CHANGES verdict (`act-1428-review.md`). It does
not invent a second candidate; it fixes the three defects on the same chain and pushes one coherent
candidate per chain.

## PLAN

- Read mission, review verdict, round-1 evidence, and all affected production files to pin the three defects.
- Confirm the published claim for this lane before any edit.
- Establish base: fetch origin/develop, attest the exact base SHA, prove ancestorship, show only own commits.
- Fix defect 1 (local destroy deletes state before window commit): commit the window before the owner removes it, roll back if the owner did not converge.
- Fix defect 2 (remote destroy omits the window): commit a durable window on the remote destroy route from the retained authority.
- Fix defect 3 (history append failure leaves an advanced current record with a missing historical revision): make latest-window and history recovery as one transaction with fail-closed history append and capacity preflight.
- Cover each defect with a causal mutant/regression test that is red before the fix and green after fix, kept inside go-unit-tests.
- Identify the CI job/trigger that runs the tests; report any .github/** need as a finding, not an edit.
- Local checks: go build, go vet, gofmt, focused maintenance go test, race gate.
- Commit the delta, push the branch, verify remote HEAD, re-run tests on the pushed ref.
- Observe the hosted PR CI run to its terminal state (run-id + status), record in evidence.
- Write this evidence, verify it is on origin/main, tear down any compose project, post END.

## Reality witnesses

- Planning repo (authoritative): `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, remote `https://github.com/mcpdev80/baseharbor-plan.git`. The `workers/baseharbor-plan` path was not touched.
- Planning origin at start of turn: `git ls-remote origin` -> `origin/main` = `2b08c9ab333fd1a5c94d6591777bd8ad6d6e7390`.
- Card state at start: `kanban_status: active`, `owner: lane-0427-maintenance-client-r2` on the planning remote. The claim precondition is satisfied by that published claim.
- Claim published by this lane: `python3 scripts/plan.py claim t-20261018-r27-maintenance-client --owner 0427-maintenance-client-r2` returned the active-owner message, confirming the existing published claim for this lane (not a second owner).
- Worktree: `/tmp/opencode/0427-maintenance-client-wt`, branch `lane/0427-maintenance-client-wt`.
- Base refresh (2026-11-07): the mission's cited base `812c99c88` was the round-1 candidate base and is still an ancestor, but `develop` advanced to `06e4b1eaa01fe10b3edb5f0ca59ce5232d110156` (#1431 merged). The working branch was `git rebase origin/develop` to stay drift-free. `git merge-base --is-ancestor origin/develop HEAD` succeeds; `git merge-base HEAD origin/develop` = `06e4b1eaa01fe10b3edb5f0ca59ce5232d110156`.
- Base SHA I attest and cite: `06e4b1eaa01fe10b3edb5f0ca59ce5232d110156` (new develop; an ancestor of HEAD).
- Ancestor proof (base is an ancestor of the working branch): `git merge-base --is-ancestor 06e4b1eaa01fe10b3edb5f0ca59ce5232d110156 HEAD` succeeds.
- Delta against develop is only this lane's maintenance files; the three #110/#1383-owned files were never in this lane's diff.
- Commits above the base are only this lane's own. `git log --format='%h %an %s' origin/develop..HEAD` lists exactly the three round-1 maintenance commits (`feat`, `docs`, `test`) plus this lane's round-2 fix commit; no foreign candidate commit is carried.

## The three defects (from act-1428-review.md) and the fixes

### Defect 1 — local destroy deletes the window before it is committed
- Cause: `runApplicationMaintenanceOperation` destroy path calls `maintenanceLifecycleOwner`, whose real
  owner (`executeApplicationDestroyLifecycle` -> `removeApplicationState` -> `deployment.DeleteDeploymentRecord`
  -> `os.RemoveAll(DeploymentRoot)`) removes the whole deployment root including `maintenance-authority.json`.
  Only afterwards does `commitApplicationMaintenanceWindow` call `applicationMaintenanceAuthority` ->
  `deployment.LoadDeploymentRecord`, which now fails because the deployment no longer exists. The destroy
  therefore reports a post-destroy persistence error instead of a durable success.
- Fix: a successful destroy commits the durable window from the retained in-memory authority captured **before**
  the owner runs, then rolls the window back if the owner did not converge. The commit happens before teardown,
  so the window survives; a failed or cancelled destroy reports nothing as a completed recovery point. The
  explicit `--yes` approval and the lifecycle consent are unchanged; only the ordering is corrected.

### Defect 2 — remote destroy omits the window
- Cause: `executeRemoteApplicationMaintenanceDestroy` returned the lifecycle owner's result directly and never
  committed a durable maintenance window, so a remote destroy left no durable record of the completed operation.
- Fix: after capturing the retained authority, commit the durable window up front, then run the owner; if the
  owner did not converge, roll the window back. Both routes now commit the window from the retained authority
  before teardown, so both leave a durable, queryable outcome instead of the round-1 behaviour (remote: no
  commit; local: commit after delete fails).

### Defect 3 — history append failure leaves an advanced current record with a missing historical revision
- Cause: `CommitMaintenanceAuthority` writes and atomically renames the latest `maintenance-authority.json`
  (advancing the current window) and only afterwards calls `appendMaintenanceHistory`. If the append fails
  (history over its 4 MiB limit, write/chmod/rename error), the current window is advanced while the historical
  entry is missing. A replay of the same revision resolves the current record as "already recorded" and does not
  repair the gap; a later commit supersedes it, leaving the older revision unanswerable.
- Fix: make the latest-window write and the history append recoverable as one transaction. A history append
  failure returns an explicit named error (`ErrMaintenanceHistoryAppendFailed`) that is not silently swallowed,
  so no partial state is reported as success (fail-closed). The current window is rolled back to what it held
  before the commit when the append fails, and bounded-history capacity is pref lighted before the irreversible
  current-window commit.

## Causal mutant / regression tests (6, all green; each mutant is red on revert)

- `TestApplicationMaintenanceDestroyCommitsWindowFromRetainedAuthority`: faithful owner deletes the deployment
  root; destroy returns nil and the window was committed before teardown (the round-1 reload-after-delete path
  is red).
- `TestApplicationMaintenanceRemoteDestroyCommitsWindow`: faithful remote owner deletes the deployment root;
  remote destroy returns nil with a committed window (the round-1 omit-the-commit path is red).
- `TestMaintenanceHistoryAppendFailureLeavesNoAdvancedCurrentRecord`: injected append failure rolls back the
  current window (rev stays 1); a retry after the write repairs history and the earlier revision is answerable.
- `TestMaintenanceHistoryCapacityPreflightFailsBeforeCommit`: a binding large enough to exceed the limit is
  refused before the current window advances.
- `TestMaintenanceHistoryAppendRollbackIsLoadbearing`: with the rollback a no-op, a failing append leaves the
  current window advanced (red); with the fix, it restores (green).
- `TestDestroyCommitRollbackIsLoadbearing`: with the rollback a no-op, a failed destroy leaves a completed
  recovery point (red); with the fix, it reports nothing (green).
- Each guard is fixed to its weakest plausible alternative and required to go red.

## CI coverage

- The tests run inside `go test ./cmd/baha` (ci.yml:122, pull_request on develop) and `go test ./...` unit job
  (ci.yml:340, pull_request on develop). The existing unit job already captures the card write-set; no .github/**
  change is required. If any selection needed a change it would be reported here as a finding with file:line, not
  applied.
- Hosted CI for the round-2 candidate, observed to terminal by this lane:
  - Run `42395015763` (PR #1428, event `pull_request`, head `a3416743b179f3b678f5bcd028eeb2121f638c30`)
    `completed/success`. `PR · Validation · go-unit-tests` passed in 9m8s on the exact candidate SHA;
    `PR · Validation · go-build`, `go-vet`, `cli-gofmt`, `PR · Source format`, `PR · Trusted Plan`,
    `PR · Focused Python`, and `PR Selected Checks` all passed. No runner, VM or compose infrastructure was
    touched; no .github/** file was edited.
  - The prior round-1 candidate SHA `d4d0f77c0` is superseded by this drift-free round-2 candidate; the round-1
    CI record `42386457934` (`completed/success` on `d4d0f77c0`) is a historical reference, not this candidate.

## repo-rule compliance

- Plan -> preflight -> apply -> verify. Ownership and consent unchanged: destroy still requires `--yes`; routing
  stays with the existing lifecycle owners; the client never builds a maintenance engine or reloads after delete.
- Secret protection unchanged; window records store digests, never paths or secret material.
- Write discipline: only `git add <file>` for card-owned maintenance files, never `git add -A`; no scratch
  scripts committed to the product branch.
- Isolation: work in the dedicated `/tmp/opencode` worktree; no containers or compose projects were started on
  this session host.
- No .github/** touched; no runner, VM, or compose infrastructure touched; no product writes outside the
  maintenance write-set; no main-branch or product-repo writes outside the card write-set.

## Host-side verification (this lane, before push)

- `go build ./...` -> OK.
- `go vet ./cmd/baha ./internal/application` -> clean.
- `gofmt -l cmd/baha/app_maintenance_client.go cmd/baha/app_maintenance_round2_test.go internal/application/maintenance_authority.go internal/application/maintenance_history.go` -> empty (all formatted).
- `go test -race -count=1 ./internal/application` -> ok.
- Focused maintenance + lifecycle operation tests (`./cmd/baha -run 'TestApplicationMaintenance|TestApplicationDestroy|TestApplicationUpdate|TestApplicationBackup|TestApplicationRestore'`) -> ok.
- Full `./cmd/baha -count=1` run: 13 pre-existing host-state failures identical to round-1 (`p427-podman-boot // [d38a7c3a-...]`, an ambient cross-lane Target config that some init/wizard tests resolve instead of their own). Reproduced identically on the clean base (`git stash -u`) so they are not a regression from this change; the hosted CI run does not show them.

## Handoff

- Candidate: branch `lane/0427-maintenance-client-wt`, head `a3416743b179f3b678f5bcd028eeb2121f638c30`, PR
  [baseharbor#1428](https://github.com/mcpdev80/baseharbor/pull/1428) against `develop` (`06e4b1eaa`). Drift-free
  (develop is an ancestor) and collision-free (delta is only the maintenance files).
- Hosted CI on the final SHA: run `42395015763` `completed/success`, observed to terminal by this lane.
- Public-surface registration (`commands.go`, machine contract) stays with `t-20261018-r27-public-surfaces`;
  this lane did not register the command.
- No compose/docker project was created by this lane. Cleanup: nothing to tear down on this session host.

## END

END_DONE 0427-maintenance-client-r2: three round-2 fixes landed on drift-free candidate a3416743b (PR#1428), six green tests + load-bearing mutants, hosted CI 42395015763 completed/success; card back to review pending CODEX re-review.
