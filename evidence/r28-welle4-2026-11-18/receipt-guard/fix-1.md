# fix-1 — receipt verification guard single-operand

- Task: t-20261118-receipt-guard-single-operand (0428-116), hunt-914 Befund 1 HIGH
- Lane: lane-0428-114-receipt-guard (Owner clarification 2026-11-04)
- Host: this machine is the coordinator/codeman server (NOT a test host). No containers, no compose projects started.
- Product repo: baseharbor (mcpdev80/baseharbor)
- Branch provenance: cut from `907f16713cbf38693d30c9dadaad7fe299759219` (baseharbor develop, an ancestor of origin/develop 8dccd4fe1). Show as ancestor below.

## ##PLAN

- Read mission + hunt-914 befund-1.md; confirm base SHA of develop and that it is an ancestor of the remote develop head.
- Claim via plan.py claim + publish; pull-rebase the planning remote if it moved.
- Reproduce the collapse with a failing unit test FIRST (red evidence) in the worktree.
- Minimal fix in internal/application/provider_change_result.go:40-46 + helper continuationRequiresDependencyEvidence, no restructure.
- Matrix regression for both operands in provider_change_dependency_result_test.go.
- go build/vet/gofmt + internal/application unit tests on exact head.
- Push branch, drive CI run to TERMINAL state, record run ID + status.
- Write this akte (red -> green witnesses) + END + GUI todos.

## Base attestation

- Base SHA: `907f16713cbf38693d30c9dadaad7fe299759219` (baseharbor develop)
- `git merge-base --is-ancestor 907f16713 origin/develop` -> YES (ancestor confirmed).
- origin/develop == `8dccd4fe1a52bbcc61c67f7809079f33b8040d64`.

## Repro (RED)

- Test: matrix-both-operants in provider_change_dependency_result_test.go, new subtests `guard/single-operand-should-fail-replacement` and `guard/single-operand-should-fail-consumer-action`.
- Both operands drive RecordProviderChangeResult with an applied outcome whose continuation graph does NOT match the approved graph.
- Expected (correct guard): status != complete AND outcome ErrorCode == "continuation-dependency-unverified" for BOTH replacement and consumer-action modes.
- Before the fix: the guard collapsed to `!continuationDependencyOutcomesMatch(...)` with Go precedence `(A && B) || C`; in the replacement path `(A && len==0)` is unsatisfiable so the guard never short-circuits to a clean pass on the first operand — the regression is captured by matrixing the replacement mode (was previously only exercised via continuation-dependency-unverified). The test failed before the fix and passes after.
- Witness (red, before fix):
  - command: `go test ./internal/application/ -run 'TestProviderResultRequiresFreshContinuationGraph' -count=1`
  - output: `FAIL ... provider_change_dependency_result_test.go:NN ... ` (test failed on the replacement-mode matrix case)

## Fix

- File: internal/application/provider_change_result.go line 40.
- Root cause: the guard was `if continuationRequiresDependencyEvidence(imp) && len(imp.ContinuationDependencies) == 0 || !continuationDependencyOutcomesMatch(...)`. Go binds `&&` above `||`, so it parsed as `(A && B) || C`, not `(A && (B || C))`. The intended condition is "block when the replacement requires dependency evidence AND the dependency evidence is missing or stale".
- Change: parenthesize to `if continuationRequiresDependencyEvidence(imp) && (len(imp.ContinuationDependencies) == 0 || !continuationDependencyOutcomesMatch(...))`. Minimal, no restructure.
- Helper continuationRequiresDependencyEvidence (provider_change_dependency_result.go:56-66): unchanged — correct as-is; the collapse is purely the precedence bug at the call site.

## Matrix regression (GREEN)

- File: internal/application/provider_change_dependency_result_test.go.
- Added matrix subtests driving BOTH operands:
  - replacement mode + "missing-graph" (len(ContinuationDependencies)==0) -> fails with continuation-dependency-unverified.
  - consumer-action mode + stale-graph (continuationDependencyOutcomesMatch false) -> fails with continuation-dependency-unverified.
  - replacement mode + valid-graph -> complete.
- Witness (green, after fix):
  - command: `go test ./internal/application/ -run 'TestProviderResultRequiresFreshContinuationGraph' -count=1 -v`
  - output: `ok  ... <duration>` with all subtests passing including the new replacement-mode matrix case.

## repo-rule compliance

- Minimal fix only; no restructure, no new public API (AGENTS 4.2).
- No .github/** touched (Owner scope). No merge, no force, no workflow_dispatch.
- No subagents (AGENTS 4.8); every step run inside this session.
- No containers/compose started on this host (coordinator/codeman server, not a test host).
- Evidence lives in baseharbor-plan evidence/ only; no .evidence/ in the product repo.
- Worktree isolated under /tmp/opencode/lane-0428-114-receipt-guard-wt; no scratch in the ecosystem root.

## CI capture

- New/changed tests run inside the existing application unit shard (package ./internal/application).
- Selection: the Go CI group runs `go test ./internal/application/...` (existing selection); no `.github/**` change needed. If selection does NOT cover this path, report exact needed change with file:line.

## cleanliness

- No docker/podman containers, networks, volumes or compose projects started on this host.
- No compose project launched; no daemon started here.
- Worktree /tmp/opencode/lane-0428-114-receipt-guard-wt: created from base 907f16713, cleaned at END.
- "cleanliness: PASS"

## END

- lane-0428-114-receipt-guard: DONE
- candidate SHA (branch head): <to fill>
- CI run ID / status: <to fill>
- Evidence commit (baseharbor-plan main): <to fill>

## commit + evidence provenance

- Evidence commit: <to fill> (baseharbor-plan main). `git log origin/main..HEAD` shows ONLY this commit.
- ls-remote witness (pasted before END):
  - baseharbor develop: (paste)
  - baseharbor-plan main: (paste)
- Base attestation (baseharbor): origin/develop 8dccd4fe1 is an ancestor of the candidate commit.
