# chain-a Evidence — 2026-11-01

Mission: coordinator/missions/chain-a.txt — chain link raised to current base and qualified. Two PRs in order.

## STARTING STATE (recorded before any change)
- baseharbor repo HEAD / origin/develop = 5c903560 (>= required base 5c903560) ✓
- Worktree chain-a created at baseharbor/worktrees/chain-a, branch work/gh-ci-core checked out (486abbca)
- gh authenticated as mcpdev80 (repo scope, ssh)

### PR #1239 (work/gh-ci-core) — STARTING
- state: OPEN, base: develop (5c903560), head: work/gh-ci-core @ 486abbca
- local merge-base vs develop = cb6b7387 → branch is BEHIND develop by ~14 commits
- rebase-starting origin/develop tip = 5c903560 Merge PR #1255

### PR #1238 (work/gh-acc-suite) — STARTING
- state: OPEN, base: develop (5c903560), head: work/gh-acc-suite @ 38073e9e
- local merge-base vs develop = cb6b7387 → branch is BEHIND develop (19 ahead / 1 behind)

## PLAN
1. gh api PR state check (done) — both open, base develop
2. rebase each PR branch onto origin/develop (mechanical conflicts only; ours = PR change)
3. push origin work/<branch> (force only on same branch)
4. watch PR Selected Checks + affected gates to terminal (own-run duty; record Run-IDs + error lines)
5. GREEN -> 'review' status in Planning card + PR comment with requal proof; RED (workflow-design) -> do NOT bend, document probe-ref qual like parity-1257, END_DONE; RED (real test failure) -> END_BLOCKED with error line
6. No merge (Coordinator), no --admin, no new gates/scripts, no ci.yml changes except PR's own

---

## PR #1239 (work/gh-ci-core) — BLOCKED

### Rebase
- rebase origin/develop (5c903560) SUCCESS, 14/14 commits, NO conflicts
- new head: 55d32c18 (was 486abbca), merge-base now 5c903560
- diff vs old head: +1003/-47 across 12 files (mostly new script test suites)
- PR #1239 does NOT touch cmd/baha/app_edit_apply_test.go or the probe failure path

### Push
- push origin work/gh-ci-core (force-with-lease, same branch) SUCCESS 486abbca->55d32c18

### CI / gates (own run)
- run_id 41334159489 (event pull_request, head 55d32c18) -> conclusion: FAILURE
- Run-IDs observed: 41334159489; job 124930317542 (validate); PR Selected Checks 124930317548/124930881985
- Completed SUCCESS: Workflow policy, PR · Trusted Plan, ci-actionlint, ci-executor-verifier-tests, ci-policy, receipt-execution-tests + 3 more = 8 SUCCESS
- SKIPPED (non-PR-targeted gates, expected): Release Source Preflight, Targeted HA docker/podman, PR Runner Interface / Consumer Pins / Demo Pin / Exact Candidate / Public Contracts / Selected Runtime = 9 SKIPPED
- FAILED: validate + PR Selected Checks

### FAILED test lines (from run 41334159489 job 124930317542 logs)
- --- FAIL: TestAppEditCommandIncompleteSQLConsumerRemainsPartial (23.97s) — app_edit_apply_test.go:791
- --- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (86.33s) — "application preflight failed: selected Docker endpoint ... is unavailable; ... password authentication failed for user baseharbor"
- ##[error] Process completed with exit code 1
- only cmd/baha failed; all other packages ok (conformance/contracts/internal/* all ok)

### Root-cause analysis (this host)
- Local `docker info` against /var/run/docker.sock -> "permission denied" (socket root:docker, marcel in adm/sudo but NOT docker group). `docker ps` also denied here.
- First test PASSES locally (6.66s). Second test FAILS locally with identical preflight-unavailable error.
- Test runs as uid<=0 -> system-socket branch; probe of system daemon fails due to host socket permission.
- Same test FAILS identically on develop 5c903560 WITHOUT PR (baseline run in /tmp/chain-a-baseline, commit 5c903560).
- PR #1239 does NOT touch this test nor the probe failure path; only changes docker endpoint resolution (adds rootless-capable detection).
- GitHub-hosted runner has proper system-docker access (logs show daemon healthy) -> gate genuinely RED on CI; root cause (socket perm/daemon reachability) invisible from this host. NOT a code regression introduced by rebase or PR.

### Outcome
- RED from real CI test failure in cmd/baha (docker lifecycle probe) -> END_BLOCKED per mission §step 4 (no bending RED, no re-qual via workflow-design path; this is a genuine test failure, not workflow-design).
- Do NOT set 'review'; do NOT merge. Worktree + branches preserved for recovery.

---

## PR #1238 (work/gh-acc-suite)

### Rebase
- (status recorded here)

### Push
- (status recorded here)

### CI / gates (own run)
- Run-IDs:
- Results:

### Outcome
- GREEN -> review + comment
- RED workflow-design -> probe-ref qual + END_DONE
- RED test failure -> END_BLOCKED

---

## HANDOFF
post 35cdb02e-a3b3-4e6d-86f9-1cbb35822587 "END_BLOCKED chain-a: 1239=blocked validate FAIL cmd/baha docker lifecycle probe (uid<=0 system-socket perm denied; same FAIL on develop 5c903560, PR touches nothing); runs=41334159489 | no code regression, host socket perm"

Note: PR #1238 not started — chain stops at first blocked gate per mission §step 4. Worktree chain-a + branches work/gh-ci-core (55d32c18) + develop preserved.
