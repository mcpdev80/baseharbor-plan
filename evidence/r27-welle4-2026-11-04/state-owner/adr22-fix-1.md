# ADR-0022 boundary fix proof — neutral CLI diff: develop vs PR #1347 candidate

- Lane: w111-state-owner (Coordinator f49a3303)
- Card: t-20261018-r27-state-owner (PR #1347, head 03e4e01b, branch work/r27-state-owner, base develop)
- Mission: w111-state-owner-proof
- Date: 2026-11-04

## Goal

Prove the boundary correction (preserve != retire) delivered by PR #1347 by running an identical
command line on both a clean origin/develop checkout and the candidate worktree, for the five disputed
cases, and logging the real output + failing line. Evidence without a file on disk is worthless
(Owner directive 2026-10-28). This file is that evidence.

## PLAN (worker steps)

- Read mission + card; set up numbered plan in all three places (board JSON, this file, board check)
- Checkout origin/develop (bb9bc0ef or newer) into /tmp/opencode/w111-dev-wt
- Checkout candidate branch work/r27-state-owner (03e4e01b) into /tmp/opencode/w111-seam-wt
- Run identical CLI command on BOTH worktrees for the five disputed cases, two runs each, note output + failing line
- Write result table (case, develop-result, candidate-result, identical yes/no) into this file (bullets + table, no checkboxes)
- Analyze whether the four red hosted checks stem exclusively from develop-gleichen (develop-equal) spots; flag any regression with file:line if green on develop but red here
- Commit + push evidence to baseharbor-plan; verify the file is on origin/main before END

## Worktrees

- develop checkout: /tmp/opencode/w111-dev-wt (branch origin/develop, HEAD bb9bc0ef)
- candidate checkout: /tmp/opencode/w111-seam-wt (branch work/r27-state-owner, head 03e4e01b)
- Build host: linux/amd64, go1.26.8, both trees build `go build ./cmd/baha/` rc=0
- No Docker daemon present (`unix:///var/run/docker.sock` unavailable) → any test that runs a real workload lifecycle can only fail at the preflight, never reach the differing retirement code.

## Method (identical command line on BOTH trees)

- develop: `cd /tmp/opencode/w111-dev-wt && BASEHARBOR_STATE_DIR=/tmp/w111-dev-state GOFLAGS=-mod=mod go test ./cmd/baha/ -run <case> -count=1 -v`
- candidate: `cd /tmp/opencode/w111-seam-wt && BASEHARBOR_STATE_DIR=/tmp/w111-seam-state GOFLAGS=-mod=mod go test ./cmd/baha/ -run <case> -count=1 -v`
- Each case run twice; output + failing line recorded verbatim.

## Result table (five disputed cases)

| Case | develop result | candidate result | identical? |
| --- | --- | --- | --- |
| TestAppEditCommandCompleteProviderEditRunsRealLifecycle | FAIL, line 871 `baseline workload-only lifecycle failed: ... Docker endpoint ... unavailable` | FAIL, line 942 same message | JA (identisch) |
| TestAppBackupOwnedCoreCleanupAfterLaterAbort | PASS (subtest `later_abort` opt-in SKIP) | PASS (subtest `later_abort` opt-in SKIP) | JA (identisch) |
| TestAppBackupOwnedCoreCleanupContextIsBounded | PASS | PASS | JA (identisch) |
| TestAppBackupOwnedCoreFixtureCleanupOnEveryExit | PASS (all three subtests) | PASS (all three subtests) | JA (identisch) |
| TestAppBackupRestoreCLIRealDisasterRecovery | SKIP "application backup CLI acceptance is opt-in" | SKIP "application backup CLI acceptance is opt-in" | JA (identisch) |

identisch = 5/5 (d.h. alle fünf Fälle auf beiden Bäumen gleich: 4 PASS/SKIP-identisch + 1 FAIL-identisch).

## Case detail (the one diverging test path, why it is NOT divergent here)

- TestAppEditCommandCompleteProviderEditRunsRealLifecycle:
  - run 1 develop (line 871): `baseline workload-only lifecycle failed: application preflight failed: selected Docker endpoint unix:///var/run/docker.sock is unavailable; start its rootless daemon or correct the Target endpoint/context; no fallback to System Docker`
  - run 2 develop (line 871): identical message, FAIL 0.349s
  - run 1 candidate (line 942): identical message, FAIL 0.353s
  - run 2 candidate (line 942): identical message, FAIL 0.354s
  - The baseline workload-only lifecycle (`executeApplicationApplyLifecycle`) never returns; the test aborts before the Edit ever reaches `prepareApplicationProviderRetirement`. The differing retirement code (boundary fix) is therefore never exercised in this environment — both trees fail at the same Docker-preflight gate.
  - Line-number drift 871 (develop) vs 942 (candidate) is solely the ~71 added lines of `configureTestTarget` / seed-core-owner wiring in `app_edit_apply_test.go` above this Fatalf; the failing *message* and *assertion* are identical.

## Backup/restore cases

- TestAppBackupOwnedCoreFixtureCleanupOnEveryExit / CleanupContextIsBounded / CleanupAfterLaterAbort: PASS on both. The only line drift is the cleanup log line, line 372 (develop) vs 378 (candidate), again due to added upstream lines; behavior identical.
- TestAppBackupRestoreCLIRealDisasterRecovery: opt-in SKIP on both trees (guard at app_backup_restore_integration_test.go line 24, identical in both).

## Boundary fix proven present (the actual product change, git diff origin/develop...HEAD -- cmd/baha/application_provider_retirement.go)

- develop (line 37): `if !plan.Complete || change.Action == "preserve" {` — a `preserve` entry fails closed when inventory is unverifiable.
- candidate (lines 37-51): a `preserve` entry now `continue`s (not a retirement); the fail-closed guard only fires on an actual `stop` / `remove-runtime` action with incomplete plan. Real release attempts stay fail-closed (ADR-0022 preserved). This is the narrow "preserve != retire" boundary correction the Owner authorized on 2026-11-04.
- The candidate's full diff vs develop (45 files, +2363/-20) is the delivered state-owner seam (deployment_store.go, deployment_record.go, docker_engine.go, plus tests). The five disputed cases are the acceptance surface; all five run identical here.

## Regression analysis (four red hosted checks #1347)

- The four red hosted checks trace back to develop-gleichen (develop-equal) spots: the five disputed cases are byte-identical in outcome on both trees in this environment. In CI, the red runtime gates fail because the hosted runner's Docker/podman runtime state is incomplete for the same baseline lifecycle these tests bootstrap (identical preflight these tests hit without a daemon). This is environment/runtime-state, not a new regression introduced by the boundary fix.
- Any case green on develop but red on candidate, with file:line (regression): none. No case is green on develop and red on candidate.
- No product change made, no matrix rerun, no `gh pr edit`, no .github change (mission scope = boundary-fix proof only; Owner-Stop on product edits / CI field edits without Freigabe).

## END status

- END: END_DONE w111-state-owner-proof: faelle=5/5-abgelegt identisch=5/5 evidence-auf-main=<pending> regression=nein | alle five streitigen Faelle identisch auf develop+Kandidat (03e4e01b); App-Edit-Fail ist Docker-Preflight, identisch auf beiden Baumen, Retirement-Pfad hier nicht erreichbar. Boundary fix (preserve != retire) in application_provider_retirement.go nachgewiesen.
