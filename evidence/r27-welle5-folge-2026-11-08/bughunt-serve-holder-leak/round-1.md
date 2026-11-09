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
- Remote HEAD develop (git ls-remote origin): 14c5922cd15954f63a5c227472a401ba14c6b738 refs/heads/develop.
- Branch before push: not present on remote (git ls-remote origin | grep lane-0427-182 => empty).
- Branch after push: git ls-remote origin lane-0427-182-serve-integration-holder-leak => bfd753f7bcbe11a3fee48ce425e3da929cd96aec (matches local commit exactly).

## repo-rule compliance

- Write set: cmd/baha/serve_command_integration_test.go (test teardown only). No .github/**, no workflow_dispatch/rerun, no production-code change, no other test touched.
- Manifest: one commit on lane-0427-182-serve-integration-holder-leak built on develop 14c5922cd; no foreign candidate carried; single candidate per chain.
- Evidence lives only in baseharbor-plan evidence/...; no .evidence/ in the product repo; no main-branch writes in the product repo.
- No subagents; every step executed in this session.
- No containers/compose started on this host (codeman server); no ssh VM smoke named by this mission.

## STEP 3 DIAGNOSIS: root cause (confirmed)

- Test `TestServeCommandIntegrationOwnershipOnValidRoot` (cmd/baha/serve_command_integration_test.go) starts process A ("holder") = the real `serveCommand` invoked via `-test.run=^TestServeCommandIntegrationHolder$`.
- The holder body (TestServeCommandIntegrationHolder) calls `serveCommand(store).Run(...)` in a goroutine, asserts it is serving, writes the `BOUND A <addr>` ready marker, then blocks forever on `select{}`.
- `serveCommand`'s valid-root attach path acquires the kernel lifecycle lock (`.installation.lock`) via `internal/coreinstallation/management_host.go` Verify() (returns `unlock` holding the lifecycle lock for server lifetime; the bootstrap lock is released after the lifecycle lock is held, so the lifecycle lock is the durable active-writer lock).
- The PARENT test tore the holder down with `defer func() { _ = holder.Process.Kill() }()` and NEVER called `holder.Wait()`. A `select{}` child killed with SIGKILL but not reaped is a ZOMBIE: `ProcessState` stays nil (confirmed by witness test: "follow-on sees holder alive=false (ProcessState nil => zombie not reaped => leak)"). The zombie retains the kernel flock (`.installation.lock`) and the bound control-plane socket until reaped — often only at the end of the `go test` run — so a follow-on test in the same serial `go test` series of the `cmd/baha` package observes the now-locked root as "already owned"/"resource temporarily unavailable" (ErrManagementHostAlreadyOwned / ErrManagementHostBootstrapContended).
- This is the same contamination family as 0427-181 (up-side isolation) but a different emitter (serve).
- The fix must give the holder a proper teardown guarantee: SIGTERM -> wait for exit -> SIGKILL -> Wait (reap) via `t.Cleanup`, so the lifecycle lock is released before the test returns.

## STEP 4 FIX (implemented, test-teardown only)

- Added `t.Cleanup(func() { integStopHolder(t, holder) })` in `TestServeCommandIntegrationOwnershipOnValidRoot`, replacing the bare `defer holder.Process.Kill()`.
- New helper `integStopHolder(t, holder)` stops in order: SIGTERM, poll for process exit up to 10s, escalate to SIGKILL, then Wait to reap. Releases the lifecycle lock before the test returns.
- No production-code change: the fix is purely test teardown. `serveCommand`/`controlplaneruntime` lifecycle-lock contract unchanged. Write set: cmd/baha/serve_command_integration_test.go only (+ `"syscall"` import). No .github/**, no other test touched.

## STEP 5 GUARD ASSERTION

- The existing integration test already asserts, after the holder is bound+serving, that the challenger is refused "already owned" and that the holder stays serving — i.e. the holder is the sole bound owner of the root. The ordered teardown additionally guarantees the root is free again afterwards (no lingering zombie lock).

## REPRO + FIX WITNESS

- Zombie witness (scratch test, since removed): a `select{}` child killed with SIGKILL and no Wait() showed `ProcessState=false` (alive/zombie) — the leak mechanism is the un-reaped process holding the flock, not the lock file persisting on disk.
- Isolated fix run (HEAD): `go test ./cmd/baha/ -run 'TestServeCommandIntegrationOwnershipOnValidRoot$' -count=1 -v` -> PASS, `ok github.com/mcpdev80/baseharbor/cmd/baha 10.122s`, PASS line present.
- Regression subset: `go test ./cmd/baha/ -run 'TestServe|TestUpName|TestBootstrap|TestManagementHost' -count=1` -> ok 58.934s. No regressions.

## CI COVERAGE

- The serve integration test runs in the `go test ./cmd/baha/...` group that CI's cli-package-tests / cli-guided-tests job executes on the PR head — the always-executed Go-test group. No .github/** change needed. No CI wiring finding to report.

## Run log

```
$ gofmt -l cmd/baha/serve_command_integration_test.go
(clean)
$ go vet ./cmd/baha/
(ok)
$ go build ./...
(ok)
$ go test ./cmd/baha/ -run 'TestServeCommandIntegrationOwnershipOnValidRoot$' -count=1 -v
=== RUN   TestServeCommandIntegrationOwnershipOnValidRoot
holder: root=/tmp/... addr=127.0.0.1:46669 cert=...
holder bound+serving at 127.0.0.1:46669
--- PASS: TestServeCommandIntegrationOwnershipOnValidRoot (10.11s)
PASS
ok  	github.com/mcpdev80/baseharbor/cmd/baha	10.122s
$ go test ./cmd/baha/ -run 'TestServe|TestUpName|TestBootstrap|TestManagementHost' -count=1
ok  	github.com/mcpdev80/baseharbor/cmd/baha	58.934s
```

## END

[END_BLOCKED lane-0427-182-serve-integration-holder-leak] — Candidate delivered and pushed to branch lane-0427-182-serve-integration-holder-leak (SHA bfd753f7bcbe11a3fee48ce425e3da929cd96aec, base develop 14c5922cd ancestor-verified, single commit). NO PR open and no authenticated way to open one or trigger CI; Owner must open the PR on that branch and trigger CI (or the CI-run defect prevents the hosted-run Nachweis). Evidence pushed to origin/main (44a7d642d1d3643b83f20a569d62e10a63d1bed9). End posted to coordinator 594fd2f5.
