# w165 Execution-Journal R5 Evidence — sleep-free terminal end-state test

Lane w165 (worker). Coordinator f49a3303. Card t-20261018-r27-execution-journal, RUNDE 5.
Repo baseharbor. Branch work/r27-execution-journal, PR #1373. Evidence base r27-welle4-2026-11-04.

## PLAN

- Confirm branch/worktree HEAD 52e972fdbd2 matches PR #1373
- Read execution_request_identity_test.go waitForCondition helper (lines 22-50, 243-249)
- Design channel/event ordering proving executor completion + terminal journal persist before 202 return (no time.Sleep polling)
- Implement in own worktree; write-set stays on internal/machinehttp test files
- Run focused tests -race -count=20 -> all pass
- Mutation probe (throwaway worktree): go h.runExecution(...) => end-state test fails 20/20; restore clean diff
- Commit + push on named branch work/r27-execution-journal; update PR #1373 head
- Verify PR-gated hosted CI on new head (own-run duty); capture Run-ID + status; never touch .github workflows
- Final evidence with SHA, test output, mutation witness, CI witness; post codeman agent post END_DONE

## Repo-rule compliance

- Write-set restricted to ONE file: `internal/machinehttp/execution_request_identity_test.go` (task scope). No `.github`, no workflow, no product non-test file touched.
- Branch provenance: commit `ae53e628` is a direct child of PR head `52e972fd` (its only parent). `git ls-remote origin work/r27-execution-journal` = `ae53e628016d84830007ef9a0b91e7d815f3c0f0`. Only my single commit is in `git log origin/52e972fd..HEAD` (only my own commits; no foreign candidate carried on top). One integration candidate per chain — no second branch invented.
- Hosted run: auth tokens/pins/ENV from system/owner; this lane set none. CI run `41980078748` was observed terminal, not self-triggered via workflow_dispatch (mission scope split: `.github` untouched, no rerun dispatched).
- No subagents used; every step executed inside this session.
- Stray untracked files (`.gopath/`, `.w152/`, `internal/coreinstallation/selection.go`, `selection_test.go`, `w168_boundary_probe_test.go`) belong to other lanes; left untouched (AGENTS 5.6).

## What changed

The terminal end-state test read the terminal journal line inside a `waitForCondition` `time.Sleep(time.Millisecond)` poll loop (lines 243-249). The store commits persist-before-publish under its lock (`store.go` `update()`): `succeed()`/`fail()` write the journal line via `appendJournalLocked` (persist) and THEN append the terminal event to `record.events` (`emitLocked`) — all synchronously before `runExecution` returns. So the terminal event can appear in the history returned by `subscribe()` only after the journal line is durably written.

Fix (12 insertions / 12 deletions in one file): replaced the poll block with a single direct `os.ReadFile` of the journal after the terminal event is already proven present in history. Comment block updated to state the persist-before-publish proof. No `time.Sleep` remains in the terminal verification path.

## Test requirement (verified)

- Focused tests, `-race -count=20`, all PASS:
  `go test ./internal/machinehttp/ -run 'TestTerminalStateCommittedBefore202Response|TestTerminalStateBackgroundMutationFails|TestRunExecutionPropagatesTerminalPersistFailure|TestRequestIdentityIndexSurvivesJournalReopen|TestRequestIdentityBindsFullInputAndAllowsFreshSemanticRequest' -race -count=20` -> `ok github.com/mcpdev80/baseharbor/internal/machinehttp 15.443s`
- Full package non-race: `go test ./internal/machinehttp/ -count=1` -> `ok 29.201s`. (Full `-race` on the whole package is a very slow cold compile on this host; the focused `-race -count=20` above is the definitive race proof on the affected tests and passed.)
- No `time.Sleep` in the terminal path: `grep -n "time.Sleep" internal/machinehttp/execution_request_identity_test.go` returns only the helper's own doc line + the helper body (still used legitimately by `TestRequestIdentityBindsFullInputAndAllowsFreshSemanticRequest` and `TestRequestIdentityIndexSurvivesJournalReopen` for executor-start/reconnect waits, NOT the terminal end-state path).

## Mutation witness (stop-trip counter-probe)

In an isolated throwaway worktree (`git worktree add` on the named branch) I (1) copied the fixed `execution_request_identity_test.go` in and (2) mutated `handler.go` line 215 from `runErr := h.runExecution(...)` to `go h.runExecution(...)` with the now-unused `log` import removed. Result:

- `TestTerminalStateCommittedBefore202Response` FAILS 20/20 runs with:
  `execution_request_identity_test.go:243: no terminal event recorded on 202 tail (terminal state not durably committed)`
- 0 PASS. The backgrounded goroutine cannot place the terminal event in `record.events` synchronously before the check, exactly the stop condition.

The mutation was confined to the throwaway worktree and removed; the candidate branch diff is clean (only the intended 12/12 test-comment change).

## CI witness (initial head)

PR #1373 head on GitHub = `ae53e628016d84830007ef9a0b91e7d815f3c0f0` (PR #1373, open).
CI run `41980078748` (hosted GitHub shared runner; this lane set no auth/tokens):

- PR · Validation · go-build: success
- PR · Validation · go-vet: success
- PR · Validation · go-unit-tests: success
- PR · Source format: success
- Workflow policy: success
- PR · Trusted Plan: success
- PR · Selected Runtime / Public Contracts / Exact Candidate / Consumer Pins / Demo Pin / Runner Interface: skipped (not triggered for this path)
- Targeted HA podman/docker: skipped
- validate / Release Source Preflight: skipped

## Base refresh into develop (Owner directive 2026-11-05, KOORD-LETZTER SCHRITT)

Develop head `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7` was NOT an ancestor of my
pre-merge head `ae53e628` (my PR base was an older merge `52e972fd`). Finalized per
coordination: `git merge origin/develop` into `work/r27-execution-journal`.

- Merge commit: `2b997f3c19e8677a019265fe1a74132d3024ead6` ("Merge remote-tracking
  branch 'origin/develop' into work/r27-execution-journal"), parents
  `ae53e628016d84830007ef9a0b91e7d815f3c0f0` and `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7`.
- Ancestry witnesses:
  - `git merge-base --is-ancestor 24c7d049… HEAD` → rc=0 (develop is an ancestor of the merge).
  - `git merge-base --is-ancestor ae53e628… HEAD` → rc=0 (my fix carried into the merge).
  - `git log --oneline origin/develop..HEAD` lists ONLY my own commit `ae53e628` on top of
    develop (all other entries are pre-existing candidate history) — no foreign candidate carried on top.
- Clean auto-merge, no conflicts (`git diff --name-only --diff-filter=U` empty).
- New GitHub head (literal `git ls-remote origin work/r27-execution-journal`):
  `2b997f3c19e8677a019265fe1a74132d3024ead6`.

Re-verification on the merge head:

- `go test ./internal/machinehttp/ -count=1` → `ok 36.252s`.
- Focused `-race -count=20` → `ok 61.061s`.
- Fix still present after merge: `read it directly, no poll` at `execution_request_identity_test.go:245`.

CI run `41981442440` on new head `2b997f3c` (hosted GitHub shared runner; no auth/tokens set by this lane):

- PR · Validation · go-build: success
- PR · Validation · go-vet: success
- PR · Validation · go-unit-tests: success
- PR · Source format: success
- Workflow policy: success
- PR · Trusted Plan: success
- PR · Focused Python: success
- PR · Selected Runtime / Public Contracts / Exact Candidate / Consumer Pins / Demo Pin / Runner Interface: skipped
- Targeted HA podman/docker: skipped
- validate / Release Source Preflight: skipped

## END

DONE — w165-journal-r5: sleep removed from the terminal end-state test; `-race -count=20` green; mutation probe fails 20/20 (discriminator intact); CI 41980078748 (head ae53e628) build/vet/unit-tests green; base refreshed into develop (merge 2b997f3c, develop 24c7d049 ancestor rc=0, only my commit ae53e628 on top), CI 41981442440 green on new head.
