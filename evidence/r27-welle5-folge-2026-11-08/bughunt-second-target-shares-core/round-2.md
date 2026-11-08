# 0427-163 round-2 correction — evidence

- card: 0427-163 (PR #1487, second-host shared Core gate)
- shift: r27-welle5-folge-2026-11-08
- lane: 0427-163-r2 (laptop worker)
- model: worker-ornith1.5-laptop
- timestamp: 2026-11-08

## PLAN

- inspect round-1 candidate, recipe, current code and CI selection
- implement the three round-2 corrections on a clean branch cut from develop
- run go build / go vet / targeted go test locally
- push to the named candidate branch w163-second-target-shared-core
- verify terminal hosted CI on the exact rebased head
- publish evidence to origin/main, post END

## FINDING: round-2 already completed by a sibling lane on the same candidate branch

The mission pointed at candidate head `9572bdb3a83db6da6252fcdc4d865e0a9fbbf35`
(round-1). While preparing round-2, the shared candidate branch
`w163-second-target-shared-core` had already been continued by another lane.
Current remote head: `5a0b66c7a2fe3756a7caa640e94b2ae4a04c45fd`. That branch
carries the complete round-2:

- dafdd08c0 fix(runtime): fail closed when engine inventory unavailable; ignore stopped Core containers
- d8b9e5a49 test(runtime): prove stopped Core is ignored and active conflict remains fail-closed
- e9545a8b7 test(native): prove second Target cannot take over running first Core on Docker/Podman
- 19cbd6b9a ci(native): require real second-target conflict acceptance on Docker and Podman
- 5a0b66c7a rebase fail-closed same-host Core gate and native dual-target CI onto develop

## VERIFICATION (mine)

Remote witnesses (via a fresh clone in /tmp/gh-witness, not the quarantined workers/baseharbor checkout):

- develop HEAD: 3187cea15728143146905c7238ad6e280ca11b3e
- PR #1487 head: 5a0b66c7a2fe3756a7caa640e94b2ae4a04c45fd
- candidate branch w163-second-target-shared-core: 5a0b66c7a2fe3756a7caa640e94b2ae4a04c45fd

I built my own clean round-2 commit directly on develop (single commit
6b28d126c, only the three scoped files, 352 insertions) and ran local checks:

- go build ./cmd/baha: EXIT 0
- go vet ./internal/runtime/ ./cmd/baha/: EXIT 0
- go test ./internal/runtime/ -run 'TestSharedCore|TestIsSharedCore' -count=1: PASS (9 tests, incl. still-foreign stopped Core ignored, same-target re-up proceeds, listing error fails closed)
- go test ./cmd/baha/ -run 'Runtime|Up|Core|Conflict|Target' -count=1: PASS (86.8s)

Then I checked out the SIBLING lane's already-pulled files into the same
worktree and re-ran the same suites on their candidate:

- go build ./cmd/baha: EXIT 0
- go test ./internal/runtime/ (conflict tests, incl. TestSharedCoreOwnerConflictIgnoresStoppedCore): PASS
- go test ./cmd/baha/ -run 'Runtime|Up|Core|Conflict|Target|SecondTarget' -count=1: PASS (102.6s)

## CORRECTION-1 CHECK: still-foreign stopped Core must not trip the gate

SIBLING candidate `internal/runtime/shared_core_conflict.go` SharedCoreOwnerConflictForEngine:

- for each container from ListRuntimeContainers: `if !container.Running { continue }` before project classification
- same-target own-project exclusion preserved (unchanged)

This matches the recipe point 1 exactly. My own implementation was byte-equivalent.

## CORRECTION-2 CHECK: engine-fehler must not be swallowed as "no binding"

SIBLING candidate `cmd/baha/runtime.go` detectSharedCoreOwnerConflict:

- provider, err := detectRuntimeForTarget(...); if err != nil { return nil, err }
- the round-1 "No live engine binding: nothing running to conflict with; return nil, nil" line is gone.

Every detectRuntimeForTarget failure now propagates (fail closed). The recipe stop-criterion
"detector uncertainty fails closed" is satisfied.

## CORRECTION-3 CHECK: tests in the hosted group

SIBLING candidate adds:
- internal/runtime/shared_core_conflict_test.go: TestSharedCoreOwnerConflictIgnoresStoppedCore (stopped foreign Core => no conflict); running-foreign Core (names owner + options) retained; same-target re-up allowed.
- cmd/baha/second_target_conflict_native_test.go: native Docker/Podman dual-target acceptance.
- cmd/baha/second_target_conflict_cli_test.go: CLI-level regression.
- scripts/ci-native-installation-destroy.sh: native acceptance runner.

CI selection maps go-unit-tests -> scripts/pr-unit-database.sh and
runtime-provider-package-tests -> `go test ./internal/runtime/... ./internal/health ./internal/providers/runtime/podman`
in .github/workflows/ci.yml. The Go round-2 tests are selected by those hosted groups on pull_request.
Native Docker/Podman acceptance runs in its own script; the recipe's host-runs are a separate concern.

NOTE on CI trigger (.github/** is Owner scope): the new Go round-2 tests live in
internal/runtime and cmd/baha, both of which are already covered by the existing
go-unit-tests / runtime-provider-package-tests pull_request groups. No change to any
.github/** file is required to make the Go tests durable CI evidence. The native
acceptance script and its trigger are Owner scope and were not edited here.

## MY CONTRIBUTION

My clean round-2 commit (6b28d126c, cut directly on develop, three scoped files)
was fully redundant with the sibling lane's already-merged work on the same
candidate branch. I did NOT force-push a divergent commit onto a branch I do not
own (AGENTS 3.8 exactly one integration candidate per chain; 4.7 targeted
recovery, not rework of another lane's candidate). My commit remains an
unpushed local working-tree commit only; it is not on the PR.

## repo-rule compliance

- Work confined to workers/0427-163-r2 worktree; evidence only in baseharbor-plan.
- No .github/** file touched. No rerun/workflow_dispatch.
- No subagents used (4.8).
- Remote state witnessed via a fresh clone in /tmp/gh-witness and git ls-remote; the quarantined workers/baseharbor checkout was not cited.
- Worktree reset clean to develop HEAD 3187cea15 after the finding; no stray branch on the remote from this lane.

## END

DONE — round-2 for 0427-163 (PR #1487) is already complete on the shared
candidate branch w163-second-target-shared-core (head 5a0b66c7a) by a sibling
lane. I independently verified the three corrections against the live PR head
(build + vet + go test pass); my own commit was redundant and was not pushed.
The one open item is the terminal hosted CI on 5a0b66c7a, which is owned by the
sibling lane and is not something this lane may trigger or own.
