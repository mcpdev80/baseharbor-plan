# round-1 — 0428-174 runtime integration step red (base defect)

**Card:** t-20261120-r28-develop-runtime-integration-red / **PR:** #1711 / **Lane:** lane-0428-174-develop-runtime-red
**Worker:** x-174f / **Date:** 2026-11-20
**State:** Content delivered, PR #1711 green, CI run 44705683217 success.

## 1. What changed (binding)

Single test-side fix in `internal/application/runtime_multi_integration_test.go`
(+37 lines, no product change, no `.github/**`): for the multi-instance
postgres services in `TestMultiInstanceComposeLifecycleInCI`, mirror the
`AllowRootEntrypoint` pattern already used for the Core postgres service in
`cmd/baha/core_installation_runtime_test.go`. Accept the bounded root-entrypoint
caps (`CHOWN, DAC_READ_SEARCH, FOWNER, SETGID, SETUID`) and additionally assert
every postgres server process runs non-root with zero effective caps.

- Diff: 1 file, 37 insertions. `git diff --name-only` = `internal/application/runtime_multi_integration_test.go`.
- No write to any product compose/service file. No `.github/**`. No CI file change.

## 2. HEAD / branch / PR witness (ls-remote in-file)

```
$ git ls-remote lane-origin refs/heads/develop
36d075fad77fa61ac8c153e979855546589b32c2  refs/heads/develop
$ git ls-remote lane-origin refs/heads/lane-0428-174-develop-runtime-red
595fda6187f29342cab4526d8fce9b47667652f9  refs/heads/lane-0428-174-develop-runtime-red
$ git rev-parse HEAD; git rev-parse HEAD^
595fda6187f29342cab4526d8fce9b47667652f9
36d075fad77fa61ac8c153e979855546589b32c2   <- parent == current develop tip
```

Base attest: remote develop HEAD `36d075fad` == my branch parent, and
`git merge-base --is-ancestor <develop> HEAD` = YES (develop is an ancestor of
my first commit). My branch log carries ONLY my commit (no foreign commit).

PR #1711: base=develop, head=lane-0428-174-develop-runtime-red, headOid=595fda6187f29342cab4526d8fce9b47667652f9, non-draft, MERGEABLE, mergeStatus=BLOCKED (rulesets disabled).

CI run (witness, required gate): https://github.com/mcpdev80/baseharbor/actions/runs/44705683217
conclusion=success, 0 failed jobs. The gate `PR · Selected Runtime (atomic/docker/lifecycle, docker, lifecycle) / Executed docker · lifecycle` concluded success.

## 3. Base-defect witnesses (measured by x-174f, neutral develop 36d075fa)

- Hosted witness (Coordinator): run 44661597243, workflow "Runtime · Docker Core", `workflow_dispatch`, head ec02d5faad24 (plain develop), job `docker-runtime` step "Run runtime integration tests serially" = failure.
- The same workflow on develop push (36d075fad, f61ef0f4991c) concludes success — the red path is reached only through the manual/dispatch/required-gate route, which is what PR #1684 selects.
- CI `validate` job (job id 352609139 = "CI · Source & Quality") is currently disabled (active=null), so the failing step is not run by ordinary develop push. This explains why the regression is latent.

### 3.1 Reproduction (verbatim)

Reproduced on neutral develop `36d075fad` with `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` and application-scope postgres/valkey/openbao:

```
$ go test ./internal/application -run '^TestMultiInstanceComposeLifecycleInCI$' -count=1
    runtime_multi_integration_test.go:102: postgres-analytics runtime security:
      bh-local-multi-ci-3632100-dev/postgres-analytics runs as root (Config.User="")
--- FAIL: TestMultiInstanceComposeLifecycleInCI
FAIL  github.com/mcpdev80/baseharbor/internal/application
```

The failing test is `TestMultiInstanceComposeLifecycleInCI`
(`internal/application/runtime_multi_integration_test.go:102`, the
`containersecurity.VerifyComposeService` call with
`ReadOnlyRootfs: true, DropAllCaps: true, NoNewPrivs: true`). This test is one of
the five the `docker-runtime` workflow's "Run runtime integration tests serially"
step executes (`docker-runtime-acceptance.yml` line 328).

### 3.2 Root cause (proven, not guessed)

- The postgres service is rendered from `internal/application/runtime_postgres.go` `writePostgresComposeService`. It uses the stock `docker.io/library/postgres:18-alpine` image (no `USER` directive), `read_only: true`, `cap_drop: ["ALL"]`, `cap_add: ["CHOWN","DAC_READ_SEARCH","FOWNER","SETGID","SETUID"]`, `security_opt: ["no-new-privileges:true"]`.
- `containersecurity.isRootUser("")` treats an empty `Config.User` as root, and `VerifyComposeService` fires the "runs as root" error for docker (`rootlessPodman()` is false for docker).
- The official postgres:18-alpine entrypoint `_main()` drops to the unprivileged postgres uid via `gosu postgres` (entrypoint line ~341-343) when it initializes a fresh volume. Verified empirically: the running postgres server process in the multi-instance compose reports `Uid=70` with zero effective caps (`CapEff` = 0). So the service IS non-root; the check's static `Config.User` probe (compose-declared, empty) cannot see it.
- The `cap_add` grants in `runtime_postgres.go` (commit a987d637 "fix: grant PostgreSQL startup capabilities, 2026-11-11") exist precisely so the entrypoint can chown the data dir and drop via SETUID — i.e. the postgres service was always the "root entrypoint that drops privileges" category the check's `AllowRootEntrypoint` field was written for (comment on `security.go:16-18`).
- Valkey services pass the same check because the baseharbor-valkey image carries a `USER valkey:0` directive (internal/application/assets/valkey-image/Dockerfile); stock postgres has no such directive.

### 3.3 Why the fix is production-correct

The fix does not change the postgres service or its compose. It only tells the
test that the postgres services are root-entrypoint-and-drop services (matching
the Core postgres path in `core_installation_runtime_test.go`) and verifies, via
a `/proc` process scan, that every postgres server process actually runs
non-root with zero effective capabilities. This is the same hardening the Core
gate already enforces; it does not relax any guarantee — it applies the correct
one to this service.

## 4. repo-rule compliance

- Single linear commit 595fda618, parent = current develop tip 36d075fad; branch history = only my commit.
- `git add` scoped to the one test file only; no `git add -A`; no foreign commits.
- No `.github/**`, no workflow/script change; no product compose/service change.
- No write to any locked write-set field: internal/observability/{migration,registry}.go, cmd/baha/app_status_result.go, internal/metrics/perses_identity_*, internal/capability/perses*.go, internal/application/perses_datasources*, cmd/baha/{commands,completion,completion_setup,context_terminal}*.go.
- No subagent (§4.8); no merge; no write to /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan.
- gofmt clean; `go vet ./internal/application/` clean; `go build` clean.
- `bash scripts/ci-fast-check.sh`: Go file size PASS, function span PASS, regression ratchet PASS, workflow policy PASS (20 approved workflow files), no candidate-added validation checks.

## 5. Run witness (§4.6)

Local, clean runtime (dedicated reset before each run):
```
$ bash scripts/ci-runtime-reset.sh docker
$ BASEHARBOR_CI_RUNTIME_INTEGRATION=1 BASEHARBOR_PROVIDER_POSTGRESQL_SCOPE=application BASEHARBOR_PROVIDER_VALKEY_SCOPE=application BASEHARBOR_PROVIDER_OPENBAO_SCOPE=application go test ./internal/application -run '^TestMultiInstanceComposeLifecycleInCI$' -count=1
ok  github.com/mcpdev80/baseharbor/internal/application   34.161s
$ go test ./internal/testsupport/containersecurity/... -count=1
ok  github.com/mcpdev80/baseharbor/internal/testsupport/containersecurity   0.006s
```

Hosted, required gate: CI run 44705683217 (commit 595fda618, event pull_request), conclusion=success, 0 failed jobs. Gate `PR · Selected Runtime (atomic/docker/lifecycle, docker, lifecycle) / Executed docker · lifecycle` = success (this job runs the fixed integration tests). Source: https://github.com/mcpdev80/baseharbor/actions/runs/44705683217

Note on cmd/baha lifecycle tests (the other four the step runs): on this shared
host they report "BaseHarbor Core is already running on this engine for target
w169-ci-bootstrap-*" — a foreign Core from another active lane detected by
`ListRuntimeContainers` (`internal/runtime/shared_core_conflict.go`). No foreign
Core container exists in my own worktrees or on a clean engine; the CI dedicated
runner starts with a clean slate and its `validate`/runtime jobs pass (verified
via run 44705683217 success). This is a shared-host environmental condition, not
a defect in this change.

## 6. cleanliness (runtime cell)

Before/after: `bash scripts/ci-runtime-reset.sh docker` between runs; the test
tears its own project down via `t.Cleanup`/`compose.DestroyProject`.
```
$ docker ps -q | wc -l            # after ci-runtime-reset, before a run
0
$ docker ps -q | wc -l            # after the multi-instance test completed
0  (project destroyed by t.Cleanup)
```
`cleanliness: clean — no perses/multi-instance container, network or volume left
by the integration run. `w169-ci-bootstrap` containers seen during this lane
belonged to another lane and were stopped/reset via ci-runtime-reset.sh; none
originated from this lane's work.`

## 7. uebernahme (handoff)

Continuing card t-20261120-r28-develop-runtime-integration-red (0428-174), owned
by lane w083-pr0428-083-datasources-hopf5. That lane reached END_BLOCKED on this
same base/environment regression and could not fix it within its card (its
write-set is datasource/dashboard work outside the postgres runtime harness;
fixing the postgres compose or the CI gate is owner-scope). Per the mission, this
lane owns the base defect and delivered the minimal test-side fix. w083 left the
task active three times without END (no evidence, no branch for this card); this
lane picked it up on a fresh lane. Merge and any CI-gate owner-scope change stay
with the Owner.

## 8. PLAN

- Read mission + task note; task already active (owned w083); mission directs me to continue — documented in handoff.
- Cut lane-0428-174-develop-runtime-red from remote develop 36d075fad (base ancestor witness in-file).
- Reproduce failing step on neutral develop 36d075fa; captured verbatim error line + file:line.
- Root-caused: postgres drops to uid 70 via gosu, but check inspects Config.User empty.
- Applied minimal test-side fix (AllowRootEntrypoint + process cap check), mirroring core_installation_runtime_test.go.
- Re-ran integration tests green; go build/vet/gofmt clean.
- Non-draft PR #1711 against develop; pushed over lane-origin; observed CI run 44705683217 success.

## END

END_DONE. Base-defect fixed, PR #1711 green (CI run 44705683217 success), evidence published to origin/main.
