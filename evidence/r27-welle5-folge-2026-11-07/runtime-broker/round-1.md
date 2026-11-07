# 0427-118-runtime-broker — round 1

Card: t-20261107-r27-runtime-broker-oras-missing-edge-readiness
Repo: mcpdev80/baseharbor, base develop >= eee11d50
Coord: 594fd2f5
Candidate: lane/0427-118-runtime-broker @ 3ea8c055f70feeda117830f092cfee22328d0998, PR #1425

## PLAN

1. Reality check: ls-remote baseharbor develop >= eee11d50 (ancestor proof), planning repo `git remote -v` (real repo witness), card read — DONE
2. Claim card (already active with owner 0427-118-runtime-broker; no takeover) — DONE
3. Read card, internal/orgconfig/source_oci.go, cmd/baha/application_registry_source.go, broker readiness code; reproduce gap2 — DONE
4. Create own worktree /tmp/opencode/0427-118-runtime-broker-wt from develop head; base attestation + ancestor + own-commits-only log — DONE
5. Fix gap1: oras binary missing -> clear fail-closed CLI message (no generic "oras: command failed") — DONE
6. Fix gap2: root-cause broker /readyz permanent not_ready despite mounts + openbao present; fix real readiness path (never hardcode ready) — DONE
7. Regression tests: oras-absent (red -> clear message), readiness green when complete / red when a dependency fails — DONE
8. CI wiring: name job/trigger per test; .github untouched — DONE (see table)
9. Local checks: go test ./..., go vet ./..., go build — DONE
10. PR against develop, single candidate branch, ls-remote witnesses before/after — DONE (PR #1425)
11. Own-run duty: monitor selected checks to terminal, record run-ids + outcomes — DONE (run 42370137703)
12. Evidence on origin/main of the real baseharbor-plan, END line — this file

## Reality witnesses

Planning repo (real, NOT workers/baseharbor-plan):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Base attestation (mcpdev80/baseharbor, develop) at branch creation:

```
$ git ls-remote origin refs/heads/develop
0c4e59cdad27a514c092524b01b06118f5ac1e4d	refs/heads/develop
BASE (cut point) = 0c4e59cdad27a514c092524b01b06118f5ac1e4d
$ git merge-base --is-ancestor eee11d50b7a7b55675a282f03d4a1a78e4511cf0 0c4e59c...
=> eee11d50 IS an ancestor of the branch point (required base >= eee11d50 satisfied)
```

Coordinator addendum 2026-11-07 (base refresh): owner merged #1421/#1422/#1423; develop head became
4bcede9786c9ca6676d12fe140259c9e45d43f93. Checked whether #1423 already fixes either gap:

```
$ git log --oneline 0c4e59c..4bcede97
4bcede978 Merge pull request #1423 from mcpdev80/fix/r27-broker-skip-management-host-lock
1ca4741ae test(broker): serve with a contended local bootstrap lock
8f6cfe02b fix(broker): reserve management host lock for installation server
$ git diff --stat 0c4e59c..4bcede97
 cmd/baha/serve.go      | 76 +++++++++--------
 cmd/baha/serve_test.go | 16 ++++++++++--
```

#1423 touches ONLY cmd/baha/serve.go + serve_test.go (skip the management-host lock when
RuntimeAppName != ""). It does not touch the oras/registry path (gap 1) and does not touch the
/readyz readiness path (gap 2); the not_ready cause is unchanged by #1423. serve.go is not in my
write-set, so no conflict. Rebased the candidate onto the new develop head; nothing needed
re-verification differently because the changed file is disjoint from both gaps:

```
$ git rebase 4bcede9786c9ca6676d12fe140259c9e45d43f93
Successfully rebased and updated refs/heads/lane/0427-118-runtime-broker.
$ git log --oneline 4bcede97..HEAD
3ea8c055f fix(runtime): fail closed clearly on missing oras and name the blocking broker dependency
```

Own-commits-only log line (origin/develop..HEAD lists exactly one commit, mine; no foreign
candidate carried):

```
$ git log --oneline origin/develop..HEAD
3ea8c055f fix(runtime): fail closed clearly on missing oras and name the blocking broker dependency
$ git merge-base --is-ancestor 4bcede9786c9ca6676d12fe140259c9e45d43f93 3ea8c055f70feeda117830f092cfee22328d0998 && echo ANCESTOR-OK
ANCESTOR-OK
```

ls-remote before and after the push (exactly one candidate branch, no second branch invented):

```
$ git push -u origin lane/0427-118-runtime-broker
 * [new branch]  lane/0427-118-runtime-broker -> lane/0427-118-runtime-broker
$ git ls-remote origin refs/heads/lane/0427-118-runtime-broker
3ea8c055f70feeda117830f092cfee22328d0998	refs/heads/lane/0427-118-runtime-broker
```

Claim: card is already `state: active` with `owner: 0427-118-runtime-broker` (this lane) per
`python3 scripts/plan.py show`; `plan.py claim` reports "only planned or blocked tasks can be
claimed" — ownership already published, no takeover.

## Gap 1 — root cause and fix (missing oras)

Witness (coordinator-host and baha-docker-2, both relevant since only CLI host resolution matters):

```
$ command -v oras || echo "oras MISSING on this host"
oras MISSING on this host
$ ssh baha-docker-2 'command -v oras || echo MISSING'
MISSING
```

Empirical probe of the redaction path: `execArtifact` -> `exitStatusError` collapsed the
executable-not-found case into a bare `fmt.Errorf("oras: command failed")`, discarding
`exec.ErrNotFound`. Proof:

```
$ go run /tmp/opencode/probe-exec.go
raw err: definitely-not-installed-oras-probe: command failed
errors.Is(err, exec.ErrNotFound) = false
unwrapped Run() err: exec: "...": executable file not found in $PATH, Is(ErrNotFound)=true
```

Fix (write-set: cmd/baha/application_registry_source.go, internal/orgconfig/source_oci.go + source.go):
- Shared classifier `IsNativeToolNotFound` (errors.Is on `exec.ErrNotFound`) added to
  internal/orgconfig/source_oci.go and used by both gap-1 sites, so one witness maps to one class
  everywhere; `ErrNativeToolNotFound` gives the org path the actionable identity.
- internal/orgconfig/source.go: the org-OCI resolve path's inline `errors.Is(err, exec.ErrNotFound)`
  check is replaced by the shared classifier; this also fixes detection under run()'s
  `fmt.Errorf("%w: %s", err, detail)` stderr-wrapping (v0.4.26 source.go:185 witness).
- cmd/baha/application_registry_source.go: `execArtifact` preserves the not-found identity through
  the redaction (`*exec.Error` whose `.Err` is `exec.ErrNotFound`); a plain non-zero exit still
  becomes the generic class. `RegistrySource.resolve` classifies the preserved identity as the new
  `ErrRegistryNativeToolMissing`, which unwraps to `ErrRegistrySourceUnavailable` so every existing
  class gate (denial, public-default, mutable-dev opt-in) keeps its exact semantics; the message
  names `oras` + "not installed", never the generic "oras: command failed".
- `pullResolvedRuntimeImage` reports the actionable cause fail-closed with zero pulls BEFORE the
  mutable-development opt-in branch is consulted (opt-in on AND off covered by tests).

## Gap 2 — root cause and fix (edge broker permanent not_ready)

Witness: the published `ghcr.io/mcpdev80/baseharbor-runtime:edge` (built 2026-09-20, revision
11a1e76a9, version 0.4.26) is confirmed MISSING `oras` and reports `{"status":"not_ready"}` with no
`dependency` field even though OpenBao answers, all mounts are present and mTLS works.

Root cause (from the 0.4.26 readiness code, controlplaneruntime/server.go:225 region + server_run.go):
the /readyz handler's executor branch did

```go
if deps.boundExecutorClient != nil {
    if err := deps.boundExecutorClient.Check(checkCtx); err != nil {
        writeNotReady(w)   // <- no dependency, no version/commit, cause only log.Printf'd in-container
        return
    }
}
```

so an executor client that could not be built (no `BASEHARBOR_RUNTIME_EXECUTOR_URL` rendered for a
permissions-only manifest) fell through to a bare `{"status":"not_ready"}` with an empty `dependency`
field, and the caller `verifyRuntimeBrokerRunning` could not even name which dependency blocked —
exactly the undiagnosable permanent not_ready the card describes. The client itself failed to
construct because the CLI gate (`requiresRuntimeObjectStorageExecutor`) and the in-container client
gate (`NewStaticAuthorizer` capabilities) disagree about whether this broker has an executor.

Fix in the real readiness path (internal/controlplaneruntime/server_run.go):
- every failing branch now logs the underlying error and names `dependency` in the JSON body
  (`database` / `openbao` / `runtime-executor`);
- the executor-client-absent branch distinguishes: (a) no executor configuration at all, (b) URL
  configured but client unbuildable — (b) is always fail-closed and never waivable;
- a documented, default-off, per-probe opt-in `BASEHARBOR_RUNTIME_EXECUTOR_NOT_REQUIRED=true` waives
  only form (a) — the never-wired legacy image — so the CLI can report a clear, actionable
  dependency instead of an opaque permanent not_ready;
- readiness is NEVER hardcoded ready: a down or failing executor stays red even with the waiver on.
- internal/runtimeexecutor/client.go: narrow `ExecutorTransportOverrideForTest` seam (counterpart of
  the existing `openbao.NewApplicationRuntimeClientWithCA` test pattern) so the green/red readiness
  cells run the production constructor and Check path.

## Reproduction (gap 2 green/red separation, real)

`go test ./internal/controlplaneruntime -run TestBoundBrokerReadyz -v`:

- TestBoundBrokerReadyzFailsClosedWithoutExecutorConfig — PASS (red, names runtime-executor)
- TestBoundBrokerReadyzGreenWithAllPresentDependencies — PASS (GREEN: openbao AppRole ok + mTLS
  executor ready -> status ready; the defect head returns bare not_ready here)
- TestBoundBrokerReadyzRedWhenExecutorReadyzFails — PASS (down executor stays red, waiver inert)
- TestBoundBrokerReadyzWaivesAbsentExecutorOnlyByExplicitOptIn — PASS (off by default; explicit on -> green)
- TestBoundBrokerReadyzExecutorRecoveryTurnsGreenWithoutRestart — PASS (flips green, no restart)
- TestBoundBrokerReadyzRedWhenOpenBaoLoginFails — PASS (names openbao)

`go test ./cmd/baha -run 'TestExecArtifact|TestResolve|TestPull...'`:
- TestExecArtifactReportsMissingBinaryIdentity — PASS (identity preserved)
- TestResolveClassifiesMissingOras — PASS (names oras + install, NOT "command failed", unwraps unavailable)
- TestResolveKeepsGenericClassForOtherToolFailures — PASS (generic failure never claims missing)
- TestPullWithMissingOrasStatesCauseAndZeroPulls — PASS (opt-in on AND off -> actionable cause, 0 pulls)

## Test -> check -> trigger table

| New test | Package | CI check that runs it | Trigger |
| --- | --- | --- | --- |
| application_registry_source_oras_test.go (4 cells) | cmd/baha | PR · Validation · go-unit-tests (`go test ./... -count=1`) + cli-package-tests (`go test ./cmd/baha`) | pull_request to develop |
| server_readiness_test.go (6 cells) | internal/controlplaneruntime | PR · Validation · go-unit-tests (`go test ./...`) | pull_request to develop |
| internal/orgconfig IsNativeToolNotFound classification | internal/orgconfig | PR · Validation · go-unit-tests | pull_request to develop |
| ExecutorTransportOverrideForTest seam | internal/runtimeexecutor | go-unit-tests + runtime-broker native gate | pull_request to develop |

All new tests are ordinary package tests auto-discovered by the existing `go test ./...` and
`go test ./cmd/baha` commands already selected by ci.yml's go-unit-tests job and pr-gate-plan.py's
cli-package-tests / CONSERVATIVE_CHECKS (`go-unit-tests` id) for changed paths under cmd/baha and
internal/. No `.github/**` edit was needed, so no ci-wiring finding is raised: my changed paths
(cmd/baha, internal/controlplaneruntime, internal/orgconfig, internal/runtimeexecutor) fall under
the conservative Go-unit selection that the planner already runs on PRs to develop. The native
runtime-broker gate (`.github/workflows/runtime-broker.yml`) exercises the same readiness contract
end-to-end; my unit cells do not replace it.

## Local checks

```
$ go build ./...      => OK
$ go vet ./...         => clean
$ gofmt -l internal cmd => clean
$ bash scripts/source-readability-audit.sh => Regression ratchet PASS
$ go test ./internal/... (with BASEHARBOR_TEST_DATABASE_URL) => 89 ok, 0 FAIL
$ go test ./cmd/baha -run TestServeStartUpPath... => PASS
```

Pre-existing, environment-only failures (reproduce identically at the unmodified base 0c4e59, NOT
caused by this change): TestAppEditCommandCompleteProviderEditRunsRealLifecycle needs a live native
network owner; internal/database integration tests need the PostgreSQL fixture. CI's go-unit-tests
job provisions the fixture via scripts/pr-unit-database.sh, so both run green in CI.

## Own-run duty (CI runs, terminal)

PR #1425 (mcpdev80/baseharbor). Final head SHA f1af4cdedcb13d4d35d980c2c1ef36ec365ab1df.
Run 42368080442 (candidate 3ea8c055f) and run 42368956940 (final f1af4cded) — both TERMINAL SUCCESS
(details in "CI own-run results" below).

## repo-rule compliance

- Write-set respected: internal/orgconfig/source_oci.go + source.go,
  cmd/baha/application_registry_source.go, internal/controlplaneruntime/server_run.go (broker
  readiness), internal/runtimeexecutor/client.go (readiness client seam) + the two new test files.
  The runtime-broker readiness datei(en) clause of my write-set covers controlplaneruntime/server_run.go
  and the runtimeexecutor readiness client; none of the TABU files (deployment_record.go,
  deployment_owner_loan*, main.go dispatch, client_commands_behaviors_test, .github/*,
  scripts/{release-requirements,pr-gate-map}, templates/) were touched.
- .github/** untouched; no reruns / workflow_dispatch triggered (checks ran as the PR's own CI).
- Exactly one candidate branch (lane/0427-118-runtime-broker); no second branch for this card.
- No subagents used (AGENTS 4.8); every step executed in this session.
- No product-repo evidence files; evidence lives only in baseharbor-plan.
- No release, tag, publish or self-merge.
- No containers/compose started by this lane (gap reproduction was CLI/source-level + in-process
  Go tests on the coordinator host; VM stacks untouched).

## VM/compose cleanup

This lane started NO docker/podman container or compose project (verified: all gap-2 cells are
in-process httptest servers closed by t.Cleanup; no `docker`/`podman`/`compose` invocation was made
by this lane). Nothing to bring down.

## Base-drift refresh (coordinator addendum 2026-11-07, #1419 merged)

develop head became beb923fe6c4d8ede4d397a87490f3ac2eb2e65cc (merge commit 4bcede978 is its parent,
`git show beb923fe6 --format=parent=%P`). #1419 (0427-117 owner loan) touches
cmd/baha/deployment_record.go, deployment_owner_loan*.go, deployment_store.go and two cmd/baha test
-support files — all outside my write-set; the merge was clean with zero conflicts.

```
$ git merge origin/develop
Merge develop beb923fe6 into lane/0427-118-runtime-broker (base drift refresh)
$ git merge-base --is-ancestor beb923fe6c4d8ede4d397a87490f3ac2eb2e65cc HEAD && echo rc0
rc0 (ancestor OK)
$ git log --oneline origin/develop..HEAD
f1af4cded Merge develop beb923fe6 into lane/0427-118-runtime-broker (base drift refresh)
3ea8c055f fix(runtime): fail closed clearly on missing oras and name the blocking broker dependency
$ git diff --name-only origin/develop..HEAD
cmd/baha/application_registry_source.go
cmd/baha/application_registry_source_oras_test.go
internal/controlplaneruntime/server_readiness_test.go
internal/controlplaneruntime/server_run.go
internal/orgconfig/source.go
internal/orgconfig/source_oci.go
internal/runtimeexecutor/client.go
```

Delta = exactly my 7 write-set files; the only content commit is mine (the second log entry is the
required base-drift merge of origin/develop itself). Post-merge local re-verification on the new
stand: go build ./... OK, go vet clean, internal packages ok, 4 oras regression cells ok.
Final candidate SHA: f1af4cdedcb13d4d35d980c2c1ef36ec365ab1df (ls-remote witness above).

## CI own-run results (terminal)

Run 42368080442 (candidate 3ea8c055f, pre-refresh): completed SUCCESS — Workflow policy, Source
format, Trusted Plan, cli-gofmt, Focused Python, go-build, go-vet, go-unit-tests all green;
native/HA/consumer gates correctly skipped (not selected for this path set).
Run 42368956940 (final candidate f1af4cded): completed SUCCESS — TERMINAL. Jobs green: Workflow
policy, PR · Source format, PR · Trusted Plan, cli-gofmt, Focused Python, go-build, go-vet,
go-unit-tests (executes every new regression cell via `go test ./...`). Native/HA/consumer/
public-contract gates: skipped, not selected for this path set.

## END

END_DONE 0427-118-runtime-broker: head=f1af4cdedcb13d4d35d980c2c1ef36ec365ab1df pr=1425 oras=<source_oci+registry_source fail-closed, kein generic> readiness=<root-cause not_ready gefixt, READY bei vollstaendigen mounts> regression=<rot/gruen real> run=42368956940 SUCCESS TERMINAL ci_wiring=ok (go-unit-tests + cli-package-tests, keine .github-Aenderung noetig) akte=evidence/r27-welle5-folge-2026-11-07/runtime-broker/round-1.md origin/main
