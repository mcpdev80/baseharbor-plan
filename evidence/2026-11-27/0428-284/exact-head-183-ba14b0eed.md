# ROLLE: REVIEW — Demo PR #183 exact-head review

Date: 2026-11-27  
Card: 0428-284  
Reviewer lane: `w255-0428-251-demo170codex`  
Reviewed PR head: `ba14b0eed4ebd747a2eb6bd14af470b910dd541c`  
Base ref and SHA: `develop` at `58ac70679efe5f7e95bd47d602841704fb9ffa67`  
Verdict: **CORRECTIONS**

## PLAN

1. Verify PR #183 is still open at the assigned full head and compare its exact diff against its `develop` base.
2. Verify the card's acceptance contract, final-round test changes, run-to-head evidence, and excluded push-run status.
3. Decide whether the digest-offset, CR-normalized transcript/log equality, and AST proof preserve the previously required final-drain assertion; record any concrete correction recipe.
4. Publish this review as a Plan evidence PR and record the exact-head Hosted Plan result. Do not edit or merge the demo candidate, close it, or start another run.
5. Verify the evidence path on live Plan main. If publication would require a forbidden merge, report that concrete blocker without bypassing it.

## Visible identity and source provenance

The exact card frontmatter read from Plan main is `owner: "w392-0428-284-demo183fix5"`. The executing reviewer uses the separate canonical identity `w255-0428-251-demo170codex`; Git user.email is `w255-0428-251-demo170codex@baseharbor.local`.

Literal commit invocation: `git -c user.name=w255-0428-251-demo170codex -c user.email=w255-0428-251-demo170codex@baseharbor.local commit -m 'review(0428-284): exact-head demo 183 final review'`.

Pre-push gate: `git show -s --format=%an HEAD` must print exactly `w255-0428-251-demo170codex`; verify `%cn` also matches.

The Plan repository remote was rechecked before preparing this Akte. Its remote lines are `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`. The isolated evidence worktree was cut detached from the exact Plan `main` SHA `d6d917c7b6f5378f5c355081afff0f5f0fc059c7`, matched by `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`; this is the required ancestor of the first evidence commit.

## Exact-head and hosted evidence

GitHub reports PR #183 OPEN, non-draft, base `develop` at `58ac70679efe5f7e95bd47d602841704fb9ffa67`, head `ba14b0eed4ebd747a2eb6bd14af470b910dd541c`, and `mergeStateStatus=CLEAN`. The exact diff from this base has two files only: `tests/guided/drive.py` and `tests/guided/test_consent_capture.py`. The round-6 comparison `335ef5e54c59d109837cb6ba9cd00a382b3e611f...ba14b0eed4ebd747a2eb6bd14af470b910dd541c` changes only `tests/guided/test_consent_capture.py` (+121/-29).

The Actions API query by the full head returned these two runs, both with `head_sha=ba14b0eed4ebd747a2eb6bd14af470b910dd541c`:

- Run `45965565557`: event `workflow_dispatch`, completed SUCCESS; job `Guided consent · production-path regressions` (job `140393294496`) completed SUCCESS. This is the authorized Hosted witness.
- Run `45963172402`: event `push`, completed FAILURE, workflow `.github/workflows/pr-config-matrix.yml`; its jobs endpoint returned `total_count=0`. It is excluded and is not a qualification run.

Both run IDs resolve to the assigned exact head; only the first is qualifying. No rerun or dispatch was initiated by this review.

## Scope and consent boundary

The exact PR file list is limited to the two `tests/guided/*` harness files. There is no `.github/**`, `ci.yml`, BaseHarbor Core, product authentication, authorization, or consent implementation change. `drive.run_tty` remains the test harness capture boundary; the earlier accepted diff reconciles its capture buffer against its own on-disk log. The round-6 forward delta touches only the regression test file. Fail-closed tests 22 and 23 are unchanged by that round-6 delta. The test helper `run_capture` invokes the real `drive.run_tty` path at `tests/guided/test_consent_capture.py:165-175`.

## Content review and verdict

The log-equivalence assertion is valuable: test_25 compares the returned transcript with the on-disk log after removing CR bytes, and separately requires the digest exactly once (`test_consent_capture.py:910-947`). On this real `run_capture` path the log file is created by `run_tty`, though the test currently guards the equality assertion with `if log_path.exists()` rather than failing if it is absent.

The round-6 replacement is **weaker than the prior branch-membership assertion**. `digest_start_offset >= 4096` at `test_consent_capture.py:839-848` proves only that the digest is after the first normal 4096-byte read. `run_tty` loops through `select()` and `os.read(master, 4096)` at `drive.py:342-364` before it calls `proc.poll()` at `:409-410`; therefore multiple normal-loop reads can consume the digest before the poll observes process exit. The exact test uses `delay=0.0, final_delay=0` at `test_consent_capture.py:851-860`, which does not force the digest into the later final-drain loop at `drive.py:409-427`.

The AST helper at `test_consent_capture.py:50-103` proves that some `bytes_read += ...` occurs in a `while` nested below an `if rc is not None`; it does not tie the test's digest bytes to that branch execution, nor assert that the same branch appends that chunk to `capture_buffer`. The test resets `drive.FINAL_DRAIN_CHUNKS` at `:861-862` but round 6 no longer asserts the counter. Consequently, full transcript/log equality can pass when the ordinary select loop captured all bytes and the final-drain reconciliation did not handle the digest. The negative-proof claim at `:827-833` is conditional on a final-drain chunk containing the digest and is not established by this test's current schedule.

Required correction recipe, limited to the same test harness write-set:

1. Make test_25 deterministic about the route: control the reader/poll sequence so a normal select read consumes the prefix, `proc.poll()` reports exit, and the digest-bearing unread bytes are then supplied to the actual `run_tty` final-drain loop. Avoid relying on `digest_offset > 4096` alone or on OS scheduling.
2. Assert the test observed the digest-bearing bytes in that drain branch and that removing the drain `bytes_read` accounting or reconciliation makes the test fail; retain the exactly-once digest assertion.
3. Make the CR-normalized log-equivalence check unconditional for the run and fail if the expected log file is missing.
4. Tighten the AST guard to identify the `while` directly inside the `if rc is not None` drain block and assert both the `capture_buffer` append and `bytes_read` update are in that loop.

These corrections preserve the approved test-only boundary. No consent/auth behavior change is requested. Hosted run `45965565557` is green on the exact head but does not cure this content gap; no product merge is authorized by this mission.

## Review comment witness

The ROLLE: REVIEW — CORRECTIONS comment was posted on BaseHarbor Demo PR #183 before any candidate action: https://github.com/mcpdev80/baseharbor-demo/pull/183#issuecomment-7213692529 (comment id `7213692529`).

## Plan evidence PR and publication constraint

The evidence-only Plan PR is #201, branch `w255-0428-251-demo170codex-183exactreview`. Its first candidate head `5b0cf15656958e51417c4fcc29a3f6b223ceedc2` had exact-head Hosted Plan Validate run `45966977620`, pull_request, completed SUCCESS. The first push was witnessed by `5b0cf15656958e51417c4fcc29a3f6b223ceedc2 refs/heads/w255-0428-251-demo170codex-183exactreview` from `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/w255-0428-251-demo170codex-183exactreview`.

This mission also explicitly says `KEIN gh pr merge`; the standing evidence-publication rule forbids direct writes to Plan main and requires the branch/PR route. Therefore this lane will not merge PR #201. The review is on #183 and the Akte is prepared on the scoped Plan PR, but the requested Plan-main publication and main commit SHA remain blocked pending an authorized reviewer/merge.

## No local execution

No local tests were run. This verdict is based on the exact GitHub diff, source readback, and Actions API evidence only.

## 4-field

- Mission lane label: `w255-0428-284-183exactreview`
- Executing canonical identity: `w255-0428-251-demo170codex`
- Repository and candidate: baseharbor-demo PR #183, head `ba14b0eed4ebd747a2eb6bd14af470b910dd541c`
- Evidence target: `evidence/2026-11-27/0428-284/exact-head-183-ba14b0eed.md`

END_BLOCKED w255-0428-251-demo170codex: CORRECTIONS posted on #183; Plan Akte is PR #201, and mission forbids gh pr merge so no Plan-main commit SHA is available.
