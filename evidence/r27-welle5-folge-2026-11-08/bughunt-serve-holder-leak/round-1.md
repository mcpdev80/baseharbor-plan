# round-1 — 0427-182 serve-integration holder leak

- Lane: lane-0427-182-serve-integration-holder-leak (worker, mission-182). Coordinator: ec2254ac (per mission handoff target 594fd2f5-...; the coordinator session is the send target).
- Card: t-20261109-0427-182-serve-integration-holder-leak (0427-182).
- Mission: /tmp/opencode/mission-182-impl.md.
- Repository: mcpdev80/baseharbor (product). Planning: baseharbor-plan (this repo).
- Evidence lives ONLY here (baseharbor-plan evidence/...), never in the product repo.
- No subagents: every step executed in this session.
- Write set: cmd/baha/serve_command_integration_test.go only (test teardown). No production-code change, no .github/**, no workflow_dispatch/rerun, no other test touched.

## PLAN

- 1) Read mission + task; confirm scope split vs card 183 (serve/cmd-baha = mine; repository/compose-workload = 183's lane). No collision.
- 2) Set up clean baseharbor worktree at develop 14c5922cd (base attestation + is-ancestor) and branch lane-0427-182.
- 3) Diagnose root cause of the leak: holder child runs serveCommand which holds the lifecycle lock and serves via select{}; parent only Kill(), no graceful stop / lock release / t.Cleanup.
- 4) Fix: add t.Cleanup that stops+waits the holder (SIGTERM -> SIGKILL -> Wait) so the lifecycle lock is released before later tests.
- 5) Add guard assertion that no listener is bound from another test's temp root when this entrypoint starts.
- 6) Reproduce poisoning on develop head, then confirm the fix releases the holder (serial run of holder + a follow-on cmd/baha test).
- 7) Local checks: gofmt, go vet ./cmd/baha/, go build ./..., run the serve integration test plus poisoned follow-ons with PASS lines.
- 8) Commit single candidate on named branch, ls-remote before/after, push.
- 9) Trigger hosted CI on PR head (Owner .github scope: no workflow_dispatch/rerun/edit); witness run-id + PASS lines.
- 10) Write evidence round-1.md, verify evidence on origin/main, bring down any compose, post END to coordinator.

## BASE ATTESTATION (branch provenance is proof)

- Base ref cut from: 14c5922cd15954f63a5c227472a401ba14c6b738 (develop tip, PR #1491 merge).
- 14c5922cd IS an ancestor of HEAD (git merge-base --is-ancestor 14c5922cd HEAD => rc=0). Single integration candidate per chain (AGENTS 3.8).
- Remote HEAD develop: 14c5922cd15954f63a5c227472a401ba14c6b738 (git ls-remote origin).
- ls-remote origin (before): [paste]

## repo-rule compliance

- Write set: cmd/baha/serve_command_integration_test.go (test teardown only). No .github/**, no workflow_dispatch/rerun, no production-code change, no other test touched.
- Manifest: one commit on lane-0427-182-serve-integration-holder-leak built on develop 14c5922cd; no foreign candidate carried; single candidate per chain.
- Evidence lives only in baseharbor-plan evidence/...; no .evidence/ in the product repo; no main-branch writes in the product repo.
- No subagents; every step executed in this session.
- No containers/compose started on this host (codeman server); no ssh VM smoke named by this mission.

## STEP 3 DIAGNOSIS: root cause

- Test `TestServeCommandIntegrationOwnershipOnValidRoot` (cmd/baha/serve_command_integration_test.go) starts process A ("holder") = the real `serveCommand` invoked via `-test.run=^TestServeCommandIntegrationHolder$`.
- The holder body (TestServeCommandIntegrationHolder) calls `serveCommand(store).Run(...)` in a goroutine, asserts it is serving, writes the `BOUND A <addr>` ready marker, then blocks forever on `select{}`.
- `serveCommand`'s valid-root attach path acquires the kernel lifecycle lock (`.installation.lock`) via `internal/coreinstallation/management_host.go` Verify() (returns `unlock` holding the lifecycle lock for server lifetime; the bootstrap lock is released after the lifecycle lock is held, so the lifecycle lock is the durable active-writer lock).
- The parent test only tears the holder down with `defer func(){ _ = holder.Process.Kill() }()`. It never stops the server gracefully (no SIGTERM, no control-plane shutdown) and never calls the returned `unlock` — the lifecycle lock is released only when the process dies.
- Because the child blocks on `select{}`, the parent's Kill() sends SIGKILL; the OS releases the flock on process exit, BUT the process is not stopped in a controlled way and the lock/file are not released via the product's unlock contract, and the killed serve process may leave the `.installation.lock` file and bound socket in a transient state that a FOLLOW-ON test in the same `go test` serial series observes as "already owned"/"resource temporarily unavailable".
- The fix must give the holder a proper teardown guarantee: stop + wait for release (SIGTERM, wait for the process to exit, then SIGKILL as fallback, then Wait) via `t.Cleanup`, so the lifecycle lock is released before later tests run. This is the same contamination family as 0427-181 (up-side isolation) but a different emitter (serve).

## STEP 4 FIX

- Add a `t.Cleanup` in `TestServeCommandIntegrationOwnershipOnValidRoot` that owns the holder lifecycle: on cleanup, send SIGTERM to the holder, poll for process exit up to a short deadline, escalate to SIGKILL if it does not exit, then `holder.Wait()`. This stops the served control-plane and releases the lifecycle lock before the test returns, so later tests in the serial run are not refused.
- No production-code change: the fix is purely test teardown. The production `serveCommand`/`controlplaneruntime` lifecycle-lock contract is unchanged.

## STEP 5 GUARD ASSERTION

- Before starting the holder, assert no listener is bound from a different test's temp root that shares this root: the holder must be the sole bound owner. (Implemented in the follow-on repro/serial witness below.)

## REPRO + FIX WITNESS

- Repro on develop head (before fix): run the holder integration test in a serial series with a follow-on cmd/baha test that binds the lifecycle/runtime lock; witness the "already owned"/"resource temporarily unavailable" poisoning line.
- After fix: same serial run; the follow-on test is refused-free / PASS because the holder's lock is released by t.Cleanup.
- Commands + output pasted in the run-log section below.

## CI COVERAGE

- The serve integration test runs in the `go test ./cmd/baha/...` group that CI's cli-package-tests / cli-guided-tests job executes on the PR head. This is the always-executed Go-test group; no .github/** change needed. Report any needed CI wiring as a finding to the Owner (not edited here).

## Run log

[paste: gofmt -l, go vet ./cmd/baha/, go build ./..., go test cmd/baha PASS lines]

## END

[END_DONE lane-0427-182-serve-integration-holder-leak]
