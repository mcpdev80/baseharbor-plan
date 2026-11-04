## PLAN

1. Refresh and record ownership, PR #1373, task branch, and `develop` base; work in an isolated worktree.
2. Add red-first regressions for request identity/content binding, retained-journal index reconstruction, and durable journal visibility before execution effects.
3. Implement the smallest changes within `internal/machinehttp` so request identity, typed rejection, reconnect outcomes, and effect ordering match review-1373a; preserve bounded payload-free retention and accurately bound guarantee wording.
4. Run the red probes before implementation and the focused regressions after implementation; then run the required package suite, `go build ./...`, gofmt, and vet.
5. Commit the correction, verify `origin/develop` is an ancestor, push the branch, capture literal `git ls-remote` evidence, and leave PR #1373 draft.
6. Record results and repository-rule compliance here; hand off to coordinator f49a3303 for independent review. This worker does not issue a review verdict or merge.

## Baseline

- Role: CODEX-WORKER; implementation only, no review verdict and no merge.
- Task: `t-20261018-r27-execution-journal`; the published ownership transition names this session as sole writer for the correction round.
- PR #1373: open draft; source head before this round `0ce814d0a9bce5f6ff66f4688c1af8590bcf90fc`.
- `origin/develop`: `ecbb88545f96473986f8f41394cffce58b97d2df`.
- Isolated worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/.tmp/baseharbor-journal-r2`.

## Review recipes and evidence

- Recipe 1: `Idempotency-Key` supplies a per-request identity distinct from semantic `operation_id`. The journal stores request ID, semantic operation, actor, context, and SHA-256 of raw request input; raw input and outputs remain excluded. Same key with changed operation/actor/context/input returns typed `validation_failed` before append. A fresh key for the same semantic operation creates another execution.
- Recipe 2: `load()` rebuilds the request index from retained journal lines and rejects malformed or inconsistent persisted commitments. Disk-backed HTTP regression verifies same-key reconnect after handler/store reopen returns the same `ExecutionID` with unchanged line count; changed input after reopen returns typed validation failure with unchanged line count.
- Recipe 3: store creation returns whether an execution is new. The handler returns an existing execution without starting another `runExecution`; typed validation errors are mapped directly to HTTP 400 instead of being wrapped as internal. HTTP regressions assert the executor is called once across reconnect and changed-content rejection.
- Recipe 4: the executor-order regression reads the journal from inside the first executor call and confirms request ID and input digest are readable while raw test input is absent. Journal append already completes write, sync, and close before handler scheduling.
- Recipe 5: reconnect comments now state the retained request-identity guarantee and explicitly disclaim exactly-once external effects across crashes. No tests were removed.

## Red-first record

- Before implementation, ran `GOCACHE=/home/marcel/dev/baseharbor-ecosystem/.gocache go test ./internal/machinehttp -run 'TestRequestIdentityBindsFullInputAndAllowsFreshSemanticRequest|TestRequestIdentityIndexSurvivesJournalReopen|TestJournalCommitReadableBeforeExecutorStarts' -count=1`.
- Expected red result: all three regressions failed. Changed input was accepted with HTTP 202; reconnect after journal reopen returned a different execution ID; and the executor could not find the request commitment in the journal.
- A preceding attempt with the environment's default GOCACHE did not reach tests because `/home/marcel/gocache-root` was read-only. The explicit workspace cache then produced the red result above.

## Checks

- Focused regressions after implementation: PASS.
- `GOCACHE=/home/marcel/dev/baseharbor-ecosystem/.gocache go test ./internal/machinehttp -count=1 -timeout 8m`: PASS (31.653s).
- `GOCACHE=/home/marcel/dev/baseharbor-ecosystem/.gocache go build ./...`: PASS.
- `GOCACHE=/home/marcel/dev/baseharbor-ecosystem/.gocache go vet ./...`: PASS.
- `gofmt -d` for all six changed Go files: empty.
- `git diff --check`: PASS.
- Hosted CI has not been run or claimed green. PR #1373 remains draft; draft policy may skip selected product checks.

## repo-rule compliance

- Product changes and tests are limited to `internal/machinehttp/`; no `cmd/baha`, `internal/delivery`, or `.github/workflow` files changed.
- Work was isolated from the other active BaseHarbor checkout. No tests were deleted, no force push or merge performed, and no review verdict is issued by this worker.
- The candidate will be pushed only after a fresh remote check proves `origin/develop` is an ancestor. The exact `git ls-remote` output and final candidate SHA will be appended below.

## Push and hosted run

- Candidate commit: `11ed442eeda148b199f097cd04c4cde89e4429da` (`fix(machinehttp): bind journal entries to request identity`).
- Immediately before push, refreshed `origin/develop` and verified it is an ancestor of the candidate. GitHub account: `mcpdev80`.
- Push completed to `work/r27-execution-journal`; PR #1373 remains OPEN and DRAFT, base `develop`, head `11ed442eeda148b199f097cd04c4cde89e4429da`.
- Hosted run `41854142216` for exact head `11ed442eeda148b199f097cd04c4cde89e4429da`: terminal `success`, observed with `gh run watch`. `Workflow policy` and `PR · Source format` succeeded. `PR Selected Checks` was `SKIPPED`; validate, selected product/runtime, Docker, Podman and release-preflight jobs were also skipped under draft policy. No hosted product-test gate is claimed green.
- Literal post-push remote evidence:

```text
ecbb88545f96473986f8f41394cffce58b97d2df\trefs/heads/develop
11ed442eeda148b199f097cd04c4cde89e4429da\trefs/heads/work/r27-execution-journal
11ed442eeda148b199f097cd04c4cde89e4429da\trefs/pull/1373/head
```

## END

END_DONE cx01-journal-r2: head=11ed442e r1=rot->gruen r2=index-aus-log r3=pfad-unterscheidbar r4=reihenfolge-belegt r5=wortlaut lsremote=11ed442e | PR #1373 aktualisiert und bleibt Draft; lokale Pflichtchecks sowie Draft-Format/Workflow erfolgreich, PR Selected Checks und Produktgates uebersprungen. Übergabe an f49a3303 zur unabhängigen Abnahme.
