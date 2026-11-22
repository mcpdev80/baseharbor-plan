# PR 1763 exact-head review

## PLAN

1. Verify GitHub run 45011815553 terminal status and confirm its tested head. Complete: the run is completed and successful on the exact PR head.
2. Inspect PR 1763 exact-head diff and sentinel-test coverage, including app_broker.go findings 1 and 2. Complete: the two-file diff and hosted test selection were reviewed.
3. Decide APPROVE or REQUEST CHANGES and sentinel-YES or native-NEEDS-242 sufficiency. Complete: REQUEST CHANGES; sentinel coverage is sufficient for the redaction regression, while native runtime coverage still needs task 0428-242.
4. Write and publish read-only review evidence on baseharbor-plan origin/main. Validation passed; publication in progress.
5. Post the required END status to coordinator. Pending publication.

## Scope

Read-only independent review of PR #1763. No product changes, PR comments, merge, close, workflow rerun, local product test, or test-host container was started. Product remote resolved to https://github.com/mcpdev80/baseharbor.git. Planning remote verification before evidence commit: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` first line was `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

## Candidate

GitHub reports PR #1763 OPEN, non-draft, targeting develop, branch lane-0428-240-broker-diagnostics, with head c698d1310ed5a2d5178affb956ba8af2051d0a5b. The live PR file list is cmd/baha/app_broker.go and cmd/baha/app_broker_diagnostics_test.go.

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1763/head refs/heads/lane-0428-240-broker-diagnostics` returned:

```text
8629450ef3c5198bb675331c12f56b2c9377aa1c refs/heads/develop
c698d1310ed5a2d5178affb956ba8af2051d0a5b refs/heads/lane-0428-240-broker-diagnostics
c698d1310ed5a2d5178affb956ba8af2051d0a5b refs/pull/1763/head
```

## Run 45011815553

Run URL: https://github.com/mcpdev80/baseharbor/actions/runs/45011815553. `gh run view` reports status completed, conclusion success, event pull_request, and head SHA c698d1310ed5a2d5178affb956ba8af2051d0a5b. The terminal PR Selected Checks job 137176892351 completed successfully; its log ends with `PR Selected Checks: PASS`.

The native gate plan job 137175578131 succeeded but selected an empty matrix; its aggregate reports runtime_required=false and matrix include not-required/static. `PR · Native · ${{ matrix.id }}` job 137175608612 was SKIPPED. Targeted Docker and Podman jobs 137175578673 and 137175578888 were also SKIPPED. These skipped jobs are not runtime evidence.

The PR Go unit jobs for cli-0 through cli-3, packages, and owner all completed successfully. TestRuntimeBrokerReadinessDiagnosticsNeverEchoesValueMarker hashes to cli-0 under the exact-head `scripts/pr-go-unit-shard.py` selection algorithm. That shard reports 466 passed, 13 intentionally skipped, and 479 discovered; the script fails if a selected test is missing or incomplete. The test has five marker cases, checks that `token=abc123` and `abc123` do not leak, and checks safe dependency/status signals. This is useful durable unit evidence for the redaction helper, not evidence of a real Docker or Podman readiness failure.

## Planning repository validation

`python3 scripts/plan.py check` completed with 681 tasks, 7 epics, 13 releases, and 24 decisions; 0 errors and 10 pre-existing dependency-order warnings. The evidence file contains no markdown checkbox markers.

## Findings

1. At `cmd/baha/app_broker.go:202-204`, the production broker readiness timeout enters the new diagnostics path. The hosted marker test calls `runtimeBrokerReadinessDiagnostics` through a fake provider, and the failure test calls `failRuntimeBrokerReadiness` directly; neither drives the production readiness timeout with a real broker. No selected native job exercised this branch.
2. At `cmd/baha/app_broker.go:223-231` and `:243-265`, the failure text combines container LogsProject output with an mTLS /readyz ExecProject probe. The tests verify these channels against synthetic fixture strings only. They do not show that a live Docker or Podman broker emits the dependency name through the actual CLI failure path.

The trusted develop catalog at SHA 8629450ef3c5198bb675331c12f56b2c9377aa1c has its components array beginning at `scripts/pr-gate-coverage.json:139`, native_checks beginning at line 2980, and existing Docker/Podman data-capabilities rows at lines 3056 and 3077. It has no component rows for app_broker.go or app_broker_diagnostics_test.go, which explains the empty native selection. The needed persistent route is the owner-scope 0428-242 catalog/native scenario change.

## Verdict

REQUEST CHANGES for exact head c698d1310ed5a2d5178affb956ba8af2051d0a5b. The sentinel test is sufficient for the value-redaction and dependency-name helper regression and was selected in the successful CLI unit shard. It does not replace the missing native execution of the production readiness-failure path. The skipped native matrix is explicitly not counted as a pass; task 0428-242 must provide the catalog route and a Docker/Podman scenario before the native evidence can be accepted.

sufficiency: sentinel-YES | native-NEEDS-242

## repo-rule compliance

This is a read-only CODEX-REVIEW. No product source, workflow, PR state, check rerun, comment, merge, or close action was performed. Only the assigned review evidence file and live todo board were updated. No local product tests were run.

## cleanliness

Before review, `docker ps -a` with shell PID 3747926 showed only the header and no containers. After review, `docker ps -a` with shell PID 3749053 showed only the header and no containers. This review started no container, compose project, network, or volume.

END_BLOCKED: REQUEST CHANGES; sentinel test covers redaction, but the skipped native matrix is not evidence and native coverage remains assigned to 0428-242. Candidate SHA c698d1310ed5a2d5178affb956ba8af2051d0a5b.
