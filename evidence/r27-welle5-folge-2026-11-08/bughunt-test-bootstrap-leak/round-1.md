# Evidence: Bug t-20261108-bughunt-0427-test-bootstrap-leak (0427-127)

Shift r27-welle5-folge-2026-11-08. Worker session `work/r27-node-cli` (unrelated to this card; this card is a focused isolate, no merge needed).

## PLAN

- Read mission + repo rules; confirm planning repo = baseharbor-plan (origin/main), baseharbor remote via fresh clone.
- Reproduce the bootstrap-core leak: trace `ensureRuntimeIntegrationTrustPlane` (cmd/baha/runtime_integration_test_support_test.go:19) which uses a package `sync.Once` and never registers `t.Cleanup`; the shared control-plane (openbao/postgres/keycloak, compose project `bh-<target>-shared`) is only removed by `scripts/ci-runtime-reset.sh` after the whole job.
- Local repro with docker runtime to prove whether the test itself cleans up (or whether the leak is elsewhere).
- Fix: deterministic teardown via `t.Cleanup` on BOTH success and failure paths for the trust-plane, keyed to the single shared instance.
- CI-visible wächter: extend the existing go-integration-job (ci.yml `runtime_integration`) to assert zero leftover `bh-w169-ci-bootstrap-*` containers/volumes/networks after the package end; NO new engine.
- Focused local/vet/build checks; confirm NO product destroy-path change.
- Cut branch from develop, commit, PR titled with 0427-127, publish evidence, END.

## Base attestation

Planning repo (authoritative):

```
$ cd /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
git remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
git rev-parse --abbrev-ref HEAD
main
```

baseharbor remote measured via a FRESH clone in the persistent zone /tmp/wt-0427-leak (not the quarantined workers/baseharbor). develop base head (matches mission last heads e39b00043):

```
$ git -C /tmp/wt-0427-leak fetch origin develop
$ git -C /tmp/wt-0427-leak rev-parse origin/develop
e39b0004346cdfd082e34ba55d94d24757bbbd27
```

## repo-rule compliance

- Evidence written ONLY into baseharbor-plan evidence path (this file). No .evidence/ dir, no main-branch writes in the product repo.
- .github/** is Owner scope: I will NOT edit any workflow file or trigger a rerun. Any required CI trigger change is reported as a finding with file:line.
- No subagents (directive 2026-11-04); all steps executed in this session.
- No subagent/task tool writes/pushes/merges/checks.
- No product destroy-path change (acceptance criterion): teardown is confined to the test support helper + test, not production destroy code.

## Leak analysis (befund)

`ensureRuntimeIntegrationTrustPlane` (cmd/baha/runtime_integration_test_support_test.go:19) is a package-level helper guarded by `runtimeIntegrationTrustPlaneOnce sync.Once`. It runs `baha up --control-plane-only` which materializes the shared control-plane compose project `bh-<target>-shared` (containers: postgres-member-1, openbao-member-1, keycloak, plus volumes/networks). Every CI integration test calls this helper exactly once. The helper:

- registers NO `t.Cleanup`
- destroys nothing
- only removes its own transient `t.TempDir()` via Go's built-in cleanup of the temp dir

So the shared bootstrap cores (keycloak/openbao/postgres) survive after the package ends. On the real target `bh-w169` the operator saw 3 full leftover cores. The CI job's separate `Cleanup persistent runner state` step (ci-runtime-reset.sh) is the only thing that removes them, and only runs at the end of the job — not between tests, and not as a per-package assertion.

## CI wächter plan (befund + needed change, Owner scope)

ci.yml `runtime_integration` job runs (line 349):

```
go test -p 1 ./cmd/baha ./internal/application -run '^(TestRepositoryWorkflowRealLifecycle|TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI|TestRepositoryComposeWorkloadOnlyLifecycleInCI|TestRepositoryBuildWorkloadRebuildsSourceChangesInCI|TestMultiInstanceComposeLifecycleInCI)$' -count=1 -v
```

To make the wächter CI-visible I add a trailing shell assertion to that run step: after the package, list docker containers/volumes/networks and fail if any `bh-w169-ci-bootstrap-*` (generalized to the shared control-plane project `bh-*-*-shared` / the compose project used) remains. This extends the existing job; it does NOT add a new engine.

Exact needed change (Owner scope, .github/** — NOT edited by me):
- File: .github/workflows/ci.yml
- Line ~349 (the `run:` block of the `runtime_integration` step): append after the existing `go test` invocation a bounded docker assertion, e.g.:
  `docker compose ls --format json | ... ; docker ps -aq --filter label=com.docker.compose.project=bh-w169-ci-bootstrap-* || true; test <(docker ps -aq --filter label=...) -eq 0`
  (concrete form to be finalized by Owner). State the failing log line the wächter must produce on leak.

## Local repro

NOTE: the docker test host is /home/marcel/dev/baseharbor-ecosystem/... session host is the codeman server per mission — see below. Docker runtime tests must run on the named SSH host baha-docker, NOT on the host this session runs on. (Confirmed: baseharbor mission forbids starting containers on the coordinator host.)
