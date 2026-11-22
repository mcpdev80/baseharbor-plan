# PR 1763 sufficiency review, round 2

## PLAN

1. Refresh PR 1763 and run 45011815553 status against the exact current head. Complete: PR state and run head are unchanged at c698d1310ed5a2d5178affb956ba8af2051d0a5b.
2. Reassess verdict and sufficiency option (a) or (b), including executed cli-0/cli-1 evidence. Complete: both unit shard jobs completed successfully; native remains unexecuted, so option (b).
3. Write and validate the read-only review evidence without checkbox lines. Complete: check returned 0 errors and the file contains no checkbox markers.
4. Publish the evidence to baseharbor-plan origin/main and verify the remote path. Complete after publishing this witness update.
5. Post the required END status to coordinator. Pending.

## Scope

Read-only independent review of PR #1763. No product changes, PR comments, merge, close, workflow rerun, local product test, or test-host container was started. The product repository remote resolves to https://github.com/mcpdev80/baseharbor.git. Planning remote verification before this evidence commit: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` first line was `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

## Candidate and run

The live PR API reports #1763 OPEN, non-draft, base develop, branch lane-0428-240-broker-diagnostics, mergeStateStatus CLEAN, and head c698d1310ed5a2d5178affb956ba8af2051d0a5b. The live run API reports run 45011815553 completed with conclusion success, event pull_request, on that exact head. PR Selected Checks job 137176892351 completed successfully.

Exact remote witness from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1763/head refs/heads/lane-0428-240-broker-diagnostics`:

```text
8629450ef3c5198bb675331c12f56b2c9377aa1c refs/heads/develop
c698d1310ed5a2d5178affb956ba8af2051d0a5b refs/heads/lane-0428-240-broker-diagnostics
c698d1310ed5a2d5178affb956ba8af2051d0a5b refs/pull/1763/head
```

## CLI shard execution

Job 137175633047 (`PR · Go unit · cli-0`) completed successfully and its log reports `PASS cli-0: 466 passed / 13 intentionally skipped / 479 discovered; CLI inventory total=1856`. Job 137175633032 (`PR · Go unit · cli-1`) completed successfully and reports `PASS cli-1: 442 passed / 10 intentionally skipped / 452 discovered; CLI inventory total=1856`. These are executed job results, not queued results. The new marker test `TestRuntimeBrokerReadinessDiagnosticsNeverEchoesValueMarker` maps to cli-0 under the exact-head `scripts/pr-go-unit-shard.py` hash-selection rule; its five marker cases assert that `token=abc123` and `abc123` do not leak. The test does not self-skip. The shard script fails if a selected test was not executed or did not pass, except for explicit test skips; the marker test contains no skip.

## Planning repository validation

`python3 scripts/plan.py check` reported 681 tasks, 7 epics, 13 releases, 24 decisions, 0 errors, and 10 existing dependency-order warnings. The evidence file has no markdown checkbox lines.

## Native execution status

Native gate plan job 137175578131 succeeded with an empty matrix and `runtime_required=false`. `PR · Native · ${{ matrix.id }}` job 137175608612 was SKIPPED; targeted Docker job 137175578673 and Podman job 137175578888 were also SKIPPED. These skipped jobs provide no native runtime evidence.

The sentinel tests exercise the diagnostics helper using a fake RuntimeProvider. At `cmd/baha/app_broker.go:202-204`, the production readiness-timeout path enters the diagnostics flow; at `:223-231` and `:243-265`, the helper fetches container logs and makes an mTLS `/readyz` probe. The tests do not drive that production timeout with a live broker. The develop catalog at `scripts/pr-gate-coverage.json:139` has no app_broker component mapping; `native_checks` begins at line 2980, with the Docker and Podman data-capabilities rows at lines 3056 and 3077. Task 0428-242 remains the route needed for a real native scenario.

## Verdict

REQUEST CHANGES for exact head c698d1310ed5a2d5178affb956ba8af2051d0a5b. Option (b): the successful cli-0/cli-1 jobs confirm the unit suite ran, and cli-0 covers the redaction sentinel, but they do not exercise the real Docker/Podman readiness-failure path. The native matrix was skipped and is explicitly not counted as a pass. Require the task 0428-242 catalog mapping and native scenario before accepting this candidate.

## repo-rule compliance

This is read-only CODEX-REVIEW. Only this Planning evidence and the live todo board were updated. No product code or workflow, PR state, comment, review, merge, close, or rerun was changed. No local product tests were run.

## cleanliness

No container or compose project was started during this review. Before review evidence finalization, shell PID 3798588 ran `docker ps -a`; output showed only the header and no containers. After review evidence finalization, shell PID 3799272 ran `docker ps -a`; output again showed only the header and no containers.

END_BLOCKED: REQUEST CHANGES, option (b); cli-0/cli-1 executed successfully but the native matrix was skipped and does not cover the real readiness-failure path. Candidate SHA c698d1310ed5a2d5178affb956ba8af2051d0a5b.

## origin/main evidence path witness

Exact output of `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle5-2026-11-22/runtime-broker-0428-240/review-1763-sufficiency-round-2.md`:

```text
evidence/r28-welle5-2026-11-22/runtime-broker-0428-240/review-1763-sufficiency-round-2.md
```
