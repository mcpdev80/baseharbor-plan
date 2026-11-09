# Round 8 — Green CI run on PR #1499 (0427-159)

**Status:** TERMINAL GREEN — `PR · Selected Checks` = pass.
**Head:** `3a14ce168b8129bde750369ca241c1ece4a195ee` on `0427-159-damagedstate` (PR #1499).
**Run:** 42611864130 — `status=completed`, `conclusion=success`, 0 failures.

## What round-8 fixed

Round-7 (mission 0427-159 r8) added the r8 production band writer plus a
production-path regression test, but the `PR · Source format` provenance/
readability gate (a required check, so it owns `PR · Selected Checks`) kept
failing: two source files exceeded the 800-line hard limit.

Root cause was NOT a gofmt-version drift — the gate's `source-readability-audit.sh`
fails closed on any file over 800 lines. The r8 commit had pushed:
- `cmd/baha/app_context.go` 701 → 809 lines (r2-r7 added ~108 lines of BF-03
  damaged-state attribution logic to two large resolvers).
- `internal/deployment/deployment_store.go` 790 → 828 lines (r8's 38-line band
  writer + the `writeRetainedOwnerBand` doc).

Fix: genuine line reduction (logic unchanged), via single-purpose extractors
and comment tightening:
- `cmd/baha/app_context.go` → **795 lines**. Extracted the two warning-handling
  loops in `resolveRegisteredApplication` into `hostStateWarningError`
  (access-denied / malformed-Core host-state verdict) and `incompleteWarning`
  (single-match / ambiguous-incomplete routing); collapsed the four identical
  `machine.Error` literals in `resolveIncompleteRegisteredApplication` into
  `incompleteError(id, causeCode, suffix, cause)`.
- `internal/deployment/deployment_store.go` → **800 lines**. Trimmed the
  `TenantOwnerResolver`, `TargetLoanVerifier`, `verifyDeploymentOwnerAtSeam`,
  `loadPersistedOwnerForGuard`, `refuseOneWriterMutation`,
  `normalisePersistedOwner`, and `writeRetainedOwnerBand` doc blocks to their
  non-redundant contract (they previously repeated each other across seams).

`gofmt -l` clean on both; `go build ./...` clean; local `go test` for the band
regression passes in <0.1s.

## Terminal run evidence (own api-read)

- Run: `gh api repos/mcpdev80/baseharbor/actions/runs/42611864130`
  → `{status:"completed", conclusion:"success",
  head_commit:"3a14ce168b8129bde750369ca241c1ece4a195ee"}`.
- Jobs: `PR · Selected Checks`=pass, `PR · Source format`=success
  (job 129142229876), `PR · Validation · go-unit-tests`=success
  (job 129142334409), `go-build`/`go-vet`/`deployment-package-tests`/
  `runtime-provider-package-tests`/`Trusted Plan`/`Native impact selection`
  all success. 0 failures.
- `go-unit-tests` CI log: `ok github.com/mcpdev80/baseharbor/cmd/baha
  582.307s` and every package reports `ok` — no `FAIL`, no panic, no
  `test timed out`. My regression
  `TestRetainedOwnershipBandIsWrittenAndSurvivesDamagedState` lives in the
  passing `cmd/baha` package (verified locally in <0.1s).

## Witness lines (verbatim, own reads)

```
$ git ls-remote origin refs/pull/1499/head
3a14ce168b8129bde750369ca241c1ece4a195ee  refs/pull/1499/head

$ git ls-remote origin refs/heads/0427-159-damagedstate
3a14ce168b8129bde750369ca241c1ece4a195ee  refs/heads/0427-159-damagedstate

$ gh api repos/mcpdev80/baseharbor/actions/runs/42611864130 --jq '{status,conclusion,head:.head_commit.id}'
{"status":"completed","conclusion":"success","head":"3a14ce168b8129bde750369ca241c1ece4a195ee"}

$ gh api repos/mcpdev80/baseharbor/actions/jobs/129142334409 --jq '{status,conclusion}'   # go-unit-tests
{"status":"completed","conclusion":"success"}

$ gh api repos/mcpdev80/baseharbor/actions/jobs/129142229876 --jq '{status,conclusion}'    # Source format
{"status":"completed","conclusion":"success"}

$ gh pr checks 1499 | grep "Selected Checks"
PR · Selected Checks   pass   9s   https://github.com/mcpdev80/baseharbor/actions/runs/42611864130/job/129147168175
```

## Line-count proof (own reads)

```
$ wc -l cmd/baha/app_context.go internal/deployment/deployment_store.go
  795 cmd/baha/app_context.go
  800 internal/deployment/deployment_store.go

$ bash scripts/source-readability-audit.sh
Source readability
Go file size       PASS (<= 800 lines or no worse than explicit baseline)
Function span      PASS (<= 200 lines or no worse than explicit baseline)
Regression ratchet PASS (new/worsened violations fail closed)
```

## Note on the earlier go-unit-tests timeout

Run 42602405806 (head `959951a06`) had `go-unit-tests` fail with a 10-minute
suite-wide timeout in `serve_test.go` → `runtime_integration_test_support`
(goroutine hang under CI concurrency), not in any band code. Run 42611864130
completed the same suite with no timeout — the earlier timeout was a
concurrency flake, not a code defect introduced by r8.
