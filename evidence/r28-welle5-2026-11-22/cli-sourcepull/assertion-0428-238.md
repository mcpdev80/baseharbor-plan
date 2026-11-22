# 0428-238 test fix: two-sided KEEP invariance assertion on PR #1627

Card: t-20261122-env-destroy-native-assertion-contract (0428-238, hangs off 0428-055)
Lane: w27-pr1627-0428-061-pull
Shift: r28-welle5-2026-11-22
Status: END_DONE — test-only fix applied, hosted run passed on both engines, evidence published.

## PLAN

- Read mission fix238.md + tail. Fix on PR 1627 (branch cli2-env-delete, head bfd01276ff2), card 0428-238. Owner decision: test expectation was wrong, NO product defect proven. Evidence run 44995034290 (7228), TestEnvironmentDestroyNativeLifecycle failed on BOTH engines - docker job 137124194466, podman job 137124193912 at env_destroy_integration_test.go:136 'KEEP must retain the stopped deployment owner: found=true state=runtime-retired ready=false err=<nil>'.
- Contract the assertion must model: executeEnvironmentScopedDestroy reuses the existing app-stop mode (cmd/baha/env_destroy_integration_test.go:136 context), not a new destroy-state transition. cmd/baha/app_coreless_runtime_test.go:209 and cmd/baha/app_capability_runtime_test.go:314 both require the persisted deploy-record with Observed.State=runtime-retired while the user-facing app-status resolver reports 'stopped'.
- Step 1 ls-remote + develop 52a3c5446f41a1dd8678d99875e4cb1eee67874c, branch cli2-env-delete.
- Step 2 pull the assertion in env_destroy_integration_test.go to BOTH halves of the invariance: resolved app-status reports 'stopped' AND retained deploy-record reports 'runtime-retired'. Only the test file changes.
- Step 3 STOP if product semantics were needed — the Owner forbids forcing the persisted state to 'stopped' without a broad contract decision. NO product semantics needed: the persisted state stays 'runtime-retired' per Owner; only the test assertion was corrected to match the contract.
- Step 4 push no force, watch hosted PR run to terminal: run-id, failed count, docker AND podman env-destroy job-ids (both must be SUCCESS).
- Step 5 akte this file with ## PLAN + two gate job-ids, publish to origin/main.
- Step 6 END: new head, run-id, terminalstatus, failed count, two gate job-ids, 'cleanliness:' line.

## ROOT CAUSE

The assertion at env_destroy_integration_test.go:136 hard-coded `record.Observed.State != "stopped"`, but executeEnvironmentScopedDestroy intentionally leaves the deployment owner persisted as `runtime-retired` (the app-stop mode retires, it does not delete). The user-facing status correctly reports `stopped`. The single-state assertion failed on both engines at the record read; the invariance is two-sided: status == 'stopped' AND record == 'runtime-retired'.

## FIX (test-only, within write-set)

The CI already landed the two-sided fix on cli2-env-delete (commit fe4027f, fast-forward of the 52a3c544 base):

- Line 135: `record.Observed.State != "runtime-retired"` (retained-owner half) — message "KEEP must retain the runtime-retired deployment owner".
- Line 139: `status.State != "stopped"` (user-status half) via `collectResolvedApplicationStatus(ctx, resolved)` — message "KEEP must report the retained deployment as stopped".

Both halves model the contract; only cmd/baha/env_destroy_integration_test.go changed. Build clean (go build ./cmd/baha/), gofmt clean, TestEnvironmentDestroyNativeLifecycle passes locally with `-run '^TestEnvironmentDestroyNativeLifecycle$' -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"`.

## HOSTED RUN EVIDENCE

- New run: 7232, run-id 44996713389, head fe4027f7986502a825b2c701fb53725f39434435, conclusion SUCCESS, 19 success / 11 skipped / 0 failed.
- docker env-destroy gate: PR · Selected Core-less · docker · integration_docker_coreless-lifecycle · application.txt — `--- PASS: TestEnvironmentDestroyNativeLifecycle (12.91s)` at line 154.
- podman env-destroy gate: PR · Selected Core-less · podman · integration_podman_coreless-lifecycle · application.txt — `--- PASS: TestEnvironmentDestroyNativeLifecycle (16.98s)` at line 154.
- The mission's two gate job-ids 137124194466 (docker) and 137124193912 (podman) are the OLD failing run 44995034290's (7228). The NEW run's matrix child job-ids differ; the env-destroy gates ran inside the PR · Selected Core-less matrix job and both concluded success (verified via the run's own log files, no skipped, no FAIL).

## repo-rule compliance

- No subagents; every step executed inside this session (AGENTS 4.8).
- Test-only change within the card's write-set; NO product code edited (no cmd/baha/*.go beyond the test file).
- No .github/** or scripts/** edits; no merge/close/ready; no GitHub comments.
- Push no force; head advanced via fast-forward fe4027f (base 52a3c544 is an ancestor).
- Evidence file lives only in baseharbor-plan; no .evidence/ in the product repo.

## cleanliness

- No docker/podman compose projects or lifecycle containers started by this lane.
- Local `go test` ran with the named `-run` form and the skip guard; no bare `go test ./cmd/baha/`.
- docker ps -a witness: (none started this lane). Worktree /tmp/hop-52a3c544-wt left at detached head fe4027f; stray `baha` binary removed before commit.

## END

lane: w27-pr1627-0428-061-pull
status: END_DONE
new head: fe4027f7986502a825b2c701fb53725f39434435 (cli2-env-delete, fast-forward of develop 52a3c5446f41a1dd8678d99875e4cb1eee67874c)
run-id: 44996713389 (PR #1627, run 7232)
terminalstatus: SUCCESS — 19 success / 11 skipped / 0 failed
failed count: 0
two gate job-ids: docker env-destroy gate PASS in 'PR · Selected Core-less · docker · application.txt' (TestEnvironmentDestroyNativeLifecycle 12.91s, line 154); podman env-destroy gate PASS in 'PR · Selected Core-less · podman · application.txt' (TestEnvironmentDestroyNativeLifecycle 16.98s, line 154). (Mission's old job-ids 137124194466/137124193912 belong to prior failing run 44995034290.)
cleanliness: no containers/compose started; named go test with skip guard; stray baha binary removed; worktree detached at fe4027f.
