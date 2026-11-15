# PR #1579 Review R4

## PLAN

1. Verify exact PR #1579 r4 head/base ancestry, candidate-chain log, live PR state, and specified pull_request run.
2. Review the diff from 18b0ebc9d and verify all parallel racer errors are captured and positively checked.
3. Assess whether the concurrent CLI test is race-detector-ready; verify app.id exclusion and fail-closed identity contract.
4. Record exact-SHA verdict and recipe, validate/publish evidence, verify origin/main, and post END.


## Candidate and provenance

Role: CODEX-REVIEW r4; no merge. Planning repository root verified before evidence commit:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

Fresh product clone: `/tmp/opencode/mission-rev1579-r4-wt`. Exact product remote witness from `git ls-remote origin refs/heads/develop refs/pull/1579/head`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9	refs/pull/1579/head
```

PR #1579 is OPEN and DRAFT, base `develop`, branch `lane-0428-uid-app`, exact head `2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9`. `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c 2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9` succeeded. Exact PR JSON:

```json
{"baseRefName":"develop","headRefName":"lane-0428-uid-app","headRefOid":"2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9","isDraft":true,"number":1579,"state":"OPEN"}
```

The base-to-head log contains only the four commits in this #1579 candidate chain; no unrelated candidate is present:

```text
2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9 Marcel Pfingstgräf <dev@pfingstgraef.eu> cmd/baha: race store Create for single-owner convergence (0428-050 r3)
18b0ebc9d0d99c634a3c8b74b571a8074ce0393d Marcel Pfingstgräf <dev@pfingstgraef.eu> cmd/baha: fix concurrent uid-app test CWD race + strengthen convergence assert
2bf0c929506a5b0e64b7359a6fc8711ab3f48526 Marcel Pfingstgräf <dev@pfingstgraef.eu> cmd/baha: fix CWD state leak in concurrent uid-app test
c0664c8e49e4efb56ea69cc793b94da7cc270765 Marcel Pfingstgräf <dev@pfingstgraef.eu> cmd/baha: bounded uid-app identity-stability regression slice (0428-050)
```

The r4 diff from `18b0ebc9d0d99c634a3c8b74b571a8074ce0393d` changes only `cmd/baha/app_init_uid_app_slice_test.go` (60 insertions, 63 deletions); `git diff --check` is clean.

## Exact pull_request run

Exact `gh run view 43663162473 --repo mcpdev80/baseharbor --json databaseId,status,conclusion,event,headSha,workflowName` output:

```json
{"conclusion":"success","databaseId":43663162473,"event":"pull_request","headSha":"2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9","status":"completed","workflowName":"CI · Source & Quality"}
```

Active jobs `PR · Draft source and routing`, `PR · Draft Go · cli-0`, `cli-1`, `cli-2`, `cli-3`, and `packages` all concluded success on this exact head. Remaining jobs were skipped under draft selection. No failing pull-request check was observed; no rerun or workflow dispatch was initiated. The ambient Q-RUNTIME `workflow_dispatch` integration failure was not assessed, per mission.

The `cli-1` job log includes:

```text
go test -p 1 "${owned[@]}" -count=1
PASS cli-1: 406 passed / 10 intentionally skipped / 416 discovered; CLI inventory total=1673
```

## R3 recipe review

### Concurrent errors and positive convergence — fixed

The revised test races the documented atomic `application.Store.Create` primitive rather than concurrently invoking CLI entry points (the process-wide CWD and CLI conflict behavior made concurrent `app init` an invalid success criterion; this rationale is recorded in the alternate round-3 evidence below). Every goroutine stores either its `Create` error or its winning UID in its own result slot (`cmd/baha/app_init_uid_app_slice_test.go:221-241`). After the wait, the test rejects every error except the expected fail-closed `application.ErrExists` (`:245-250`), requires exactly one nonempty winner (`:253-270`), requires exactly one canonical owner (`:272-289`), and compares the winning UID to the stored UID (`:291-292`). Arbitrary racer failures can no longer be ignored while another racer makes the test pass.

The `application.NewApplicationID()` error is assigned to `_` at `:231`; if allocation fails, `Store.Create` rejects the empty ID (`internal/application/store.go:38-46`), its error is stored in the racer outcome, and the unexpected error fails the aggregate check at `:247-250`. This does not permit a false pass, though capturing that error directly would make the failure clearer.

The mission-named `evidence/r28-welle1-2026-11-14/cli2-uid-app/round-1.md`, `round-2.md`, and `round-3.md` are absent from planning `origin/main`. The r3 report exists at the alternate path `evidence/cli-redesign-20261114/cli2-uid-app/round-3.md`. It explains that the store-level atomic `Create` is the single-owner convergence primitive named in Owner Option B, and that concurrent CLI init correctly refuses a second initialization rather than returning six successful create/reuse outcomes.

### Race detector readiness — content passes; hosted workflow hint only

I ran the focused test against the exact fresh-clone candidate:

```text
go test -race ./cmd/baha -run '^TestUIDAppSliceConcurrentFirstCreateConvergesOnOneOwner$' -count=1
ok  github.com/mcpdev80/baseharbor/cmd/baha  1.046s
```

The test avoids concurrent `os.Chdir`, writes each goroutine's result to a distinct slice element, waits before reading results, and invokes `Store.Create` with separate IDs against one shared store. It runs cleanly under Go's race detector.

The exact hosted CLI shard command above does not include `-race`. The owner-owned race command in `.github/workflows/ci.yml:126-131` currently runs `-race` for internal packages and only `TestNodeDisconnect` in `cmd/baha`; it does not include this test. This is a nonblocking workflow hint, not a rejection of the lane content: the required addition belongs to the Owner, and no `.github/**` file was edited. The test remains picked up by the existing `cmd/baha` CLI shards on `pull_request`.

### app.id and fail-closed identity contract — preserved

The r4 diff is test-only. Existing CLI coverage continues to assert the generated system ID is absent from authored `baseharbor.yaml` bytes and the parsed authored `ApplicationID` (`cmd/baha/app_init_uid_app_slice_test.go:58-68`), with checkout reuse and one-owner checks at `:71-110`. Existing identity contract tests reject missing, invalid, or ambiguous ownership and conflicting replacement (`internal/application/v0425_contract_test.go:142-159`); retained-owner CLI coverage rejects conflicting owners (`cmd/baha/app_init_retained_identity_test.go:17-75`). The new concurrent test accepts only the explicit duplicate-owner sentinel from losing racers.

## Verdict

APPROVE exact candidate `2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9`. The goroutine errors are recorded and positively classified, exactly one winner/owner is required, the UID is compared to stored state, and the focused test passes under `-race`. The existing race workflow does not yet execute this test; record the `.github/workflows/ci.yml:126-131` change as an Owner-scope hint, not as a candidate blocker. The authored-manifest exclusion and fail-closed identity contract remain intact. PR #1579 stays DRAFT; no merge, PR update, workflow edit, or rerun was performed.

## repo-rule compliance

Review used a fresh product clone; no quarantined checkout, product edit, PR action, workflow change, rerun, container, or VM was used. Evidence is stored only in the actual planning repository. No markdown checkbox lines appear in this evidence.


## Planning validation STATE

`python3 scripts/plan.py render && python3 scripts/plan.py check` and a separate `python3 scripts/plan.py check` fail on unrelated task metadata before validating this evidence. The failure is `scripts/plan.py:883` / `short_ref`: `ValueError: not enough values to unpack (expected 2, got 1)`. Five task cards use a URL without the required `repo#number` in `sources` at line 19: `tasks/t-20261115-bughunt-d28-app-new-reg.md`, `tasks/t-20261115-bughunt-d28-bad-config-quiet.md`, `tasks/t-20261115-bughunt-d28-i18n-achtung.md`, `tasks/t-20261115-bughunt-d28-state-dir-target.md`, and `tasks/t-20261115-bughunt-d28-tmp-selection.md`. Their metadata is outside this review and was not changed. The evidence file passes `git diff --check` and the no-checkbox scan.

END mission-rev1579-r4.md DONE — APPROVE candidate 2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9.

Exact `origin/main` witness immediately before evidence publication:

```text
6d3e00daeb49c181e6c2d9c0771e6db52cece369	refs/heads/main
```
