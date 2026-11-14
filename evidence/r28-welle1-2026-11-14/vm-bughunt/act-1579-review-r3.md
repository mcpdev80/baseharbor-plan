# PR #1579 Review R3

## PLAN

1. Verify exact PR #1579 r3 head/base ancestry, own-commit log, live PR state, and specified hosted run.
2. Review the diff from 2bf0c9295 for removal of global CWD mutation and real CLI race coverage.
3. Verify positive UID convergence, app.id exclusion, fail-closed contract, and genuine CLI cells.
4. Record SHA-specific verdict and recipe, validate and publish evidence, verify origin/main, and post END.

## Candidate and provenance

Role: CODEX-REVIEW, no merge. Planning repository root verification before evidence commit:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

A fresh product clone at `/tmp/opencode/mission-rev1579-r3-wt` was used. Product remote witness:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
18b0ebc9d0d99c634a3c8b74b571a8074ce0393d	refs/pull/1579/head
```

The live PR is OPEN and DRAFT, #1579, base `develop`, branch `lane-0428-uid-app`, exact head `18b0ebc9d0d99c634a3c8b74b571a8074ce0393d`. `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c 18b0ebc9d0d99c634a3c8b74b571a8074ce0393d` succeeded. `git log --oneline 0e9ccb582f5bdcdc74049bbe3996263cdce6500c..18b0ebc9d0d99c634a3c8b74b571a8074ce0393d`:

```text
18b0ebc9 cmd/baha: fix concurrent uid-app test CWD race + strengthen convergence assert
2bf0c929 cmd/baha: fix CWD state leak in concurrent uid-app test
c0664c8e cmd/baha: bounded uid-app identity-stability regression slice (0428-050)
```

All three candidate-chain commits are authored by Marcel Pfingstgräf. Relative to r2, the diff is limited to `cmd/baha/app_init_uid_app_slice_test.go` (54 insertions, 15 deletions), and `git diff --check` is clean.

## Hosted run and task records

Run `43654843802` is `completed/success`, event `pull_request`, exact head `18b0ebc9d0d99c634a3c8b74b571a8074ce0393d`, workflow `CI · Source & Quality`. CLI shards 0 through 3, packages, and source/routing all passed; other jobs were skipped under draft selection. The shard log contains:

```text
go test -p 1 "${owned[@]}" -count=1
PASS cli-1: 406 passed / 10 intentionally skipped / 416 discovered; CLI inventory total=1673
```

The mission-named records under `evidence/r28-welle1-2026-11-14/cli2-uid-app/round-1.md`, `round-2.md`, and `round-3.md` were absent from planning `origin/main`. The round-1 record is present at `evidence/cli-redesign-20261114/cli2-uid-app/round-1.md`; it records Owner Option B and the system-owned ID contract. No round-2 or round-3 record was found at either path.

## Review findings

### Process-global CWD race — corrected

The r3 test sets the working directory once before starting six goroutines (`cmd/baha/app_init_uid_app_slice_test.go:219-223`) and has no per-racer `os.Chdir`; cleanup restores the process CWD after the racers finish (`:204-209`). The r2 race from concurrent CWD mutation is removed. The test still exercises concurrent calls to the real `runWithIO` CLI entry point (`:236-247`).

### UID convergence — only partially asserted

The test compares every successful racer’s canonical ID and compares the converged ID with the surviving canonical owner (`cmd/baha/app_init_uid_app_slice_test.go:261-281`). That is a useful positive equality assertion. However, each `runWithIO` failure returns from its goroutine without recording the error or an outcome (`:241-246`); the test only requires at least one success (`:251-259`). Thus one successful CLI invocation plus five arbitrary failures still passes. This does not prove every concurrent create/reuse branch converges. Record each error and require every racer to produce an explicitly allowed create-or-reuse result with the same nonempty canonical UID; fail on unexpected command errors.

### Race detector — absent from this test’s CI command path

The exact `cli-1` hosted command is `go test -p 1 "${owned[@]}" -count=1`, with no `-race`. In `.github/workflows/ci.yml:126-130`, the separate `go test -race` job covers internal packages and does not include `./cmd/baha`. The test is durably included in the existing CLI shards because it lives in `cmd/baha` and the exact run passed, but the requested race-detector proof is missing. Owner-owned change needed: add a race-enabled invocation covering this test/package to the CI workflow, preferably a focused command such as `go test -race -p 1 ./cmd/baha -run '^TestUIDAppSliceConcurrentFirstCreateConvergesOnOneOwner$' -count=1`; do not edit `.github/**` in this review.

### Contract and real CLI surface — satisfied

The owner-confirmed Option B remains intact: the authored manifest has no application ID, and the candidate changes only tests. `TestUIDAppSliceFirstCreateThenCheckoutReuseIdentityNoAuthoredLeak` asserts empty parsed authored ID and no allocated ID in manifest bytes (`cmd/baha/app_init_uid_app_slice_test.go:57-68`). The current concurrent case calls the real `app init --quick --no-input` CLI entry (`:241`); the first-create/reuse, legacy canonical store, and machine-output leakage cases remain in the same file. Existing contract coverage rejects conflicting, invalid, or absent registered identity (`internal/application/v0425_contract_test.go:103-161`) and CLI retained-identity coverage exercises conflicting owners (`cmd/baha/app_init_retained_identity_test.go:17-70`).

## Correction recipe

Keep the single pre-race `Chdir` and post-racer cleanup. Capture each goroutine’s command error and result; require all six invocations to succeed with an explicitly valid create-or-reuse result and require each nonempty UID to equal the canonical store UID. Add a CI race-enabled execution for this focused `cmd/baha` test; the required workflow change belongs to the Owner under `.github/workflows/ci.yml:126-130`.

## Verdict

REJECT exact candidate `18b0ebc9d0d99c634a3c8b74b571a8074ce0393d`. The r2 process-global CWD race is fixed and same-ID convergence is now positively compared across successful racers. Blocking gaps remain: arbitrary racer errors are silently ignored, and the hosted command path does not run this `cmd/baha` test with Go’s race detector. PR #1579 remains DRAFT. No product edits, PR updates, workflow changes, reruns, or local tests were made.

## repo-rule compliance

Evidence is maintained only in `baseharbor-plan`. Product state was read from a fresh clone, not the quarantined stale-ref checkout. No containers or VMs were used. No workflow files were changed. Evidence contains no markdown checkbox lines.

## END DONE


## Verbatim live-state witnesses

`git ls-remote origin refs/heads/develop refs/pull/1579/head`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
18b0ebc9d0d99c634a3c8b74b571a8074ce0393d	refs/pull/1579/head
```

`gh pr view 1579 --repo mcpdev80/baseharbor --json number,state,isDraft,headRefName,headRefOid,baseRefName`:

```json
{"baseRefName":"develop","headRefName":"lane-0428-uid-app","headRefOid":"18b0ebc9d0d99c634a3c8b74b571a8074ce0393d","isDraft":true,"number":1579,"state":"OPEN"}
```

`gh run view 43654843802 --repo mcpdev80/baseharbor --json databaseId,status,conclusion,event,headSha,workflowName`:

```json
{"conclusion":"success","databaseId":43654843802,"event":"pull_request","headSha":"18b0ebc9d0d99c634a3c8b74b571a8074ce0393d","status":"completed","workflowName":"CI · Source & Quality"}
```

## Supersession note

This review supersedes the earlier content published at this same path, which recorded ACCEPT and claimed the racer errors were not accepted and a local `-race` command had passed. The source contradicts the first claim: `runErr != nil` returns without recording an outcome (`cmd/baha/app_init_uid_app_slice_test.go:241-246`), and the aggregate only requires one success (`:251-259`). This review did not run local tests. The hosted command log is the evidence for CI and shows `go test -p 1 ...` without `-race`; the workflow's other `-race` command excludes `./cmd/baha`. Therefore the earlier ACCEPT and its local-test claim are not relied on; the current verdict is REJECT.

Exact `origin/main` witness immediately before evidence publication:

```text
e0ec9c2e9112f921c04166326b25accc3dfd33d4	refs/heads/main
```
