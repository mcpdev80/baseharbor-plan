# 0427-181 — TestUpNameResumesThroughCommandEntrypoint hosted rot

- Card: 0427-181 (task `t-20261109-0427-181-upname-entrypoint-hosted-rot`, kanban active, owner `lane-0427-181-impl`)
- Shift: r27-welle5-folge-2026-11-08 · Lane: w286 (session 594fd2f5-4e80-43b6-9841-92879146a85e)
- Repo pin: mcpdev80/baseharbor
- Base: develop `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` (exact SHA of the ref cut from)
- Planning repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY (NOT `workers/baseharbor-plan`)
- Planning origin/main HEAD at evidence write time: see `git ls-remote origin main` below

## PLAN

- Attest zone + base: worktree `/tmp/opencode/m181-wt` cut from `origin/develop fea92f379` (mission base), branch `w286-0427-181-upname-hosted`. Planning repo `origin/main` HEAD `b69cbccd` before my evidence commit.
- Diagnose root cause of the full-hosted-matrix failure.
- Implement hermetic test isolation in `cmd/baha` (`*_test.go` only).
- Local checks: build, vet, focused unit test, docker cleanliness.
- Hosted proof: green `go-unit-tests` group on a full matrix develop run with `--- PASS: TestUpNameResumesThroughCommandEntrypoint` present.
- Hygiene + terminal END.

## Repo-rule compliance

- Write-set restricted to `*_test.go` under `cmd/baha` (production code untouched; no justification needed).
- No `.github/**` edits, no workflow reruns, no `workflow_dispatch` by me beyond the required hosted proof run.
- No subagents (4.8): every step run inside this session.
- Evidence committed to the planning repo (origin/main), never to the product repo.
- One integration candidate branch `w286-0427-181-upname-hosted` cut from `fea92f379`; foreign commits never carried on top.

## Root-cause analysis (corrected after the first hosted run)

First hosted run 42637373933 (PR #1516 head `7a212c5f8`) still failed the test:
`runtime_ports_test.go:347 ... got success` (up took 67s and SUCCEEDED). The up
did NOT hit a "Core left running by another test" — it BOOTED a fresh Core.

Root cause: `TestUpNameResumesThroughCommandEntrypoint` does `t.Chdir(t.TempDir())`
(an EMPTY dir, no `baseharbor.yaml`) before the registered-NAME `up`. With no
manifest in CWD, `runtimeUpCommandWithInputResolver` treats the invocation as a
fresh-core bootstrap (`runtimeUpGuided` -> `installCore` -> real
`coreinstallation.Run`) instead of resolving the registered deployment. The up
then boots a real control plane when a docker daemon is available and SUCCEEDS.
So the assertion "must fail before runtime realization" passed only when no
docker was present (isolated unit run) and failed deterministically in the
hosted matrix where docker is available. The `docker-dev` shared-network idea
was a red herring.

The fix makes the up resolve the registered deployment: it must run from the
repository root (with the manifest), where `HasRepositoryApplication(cwd)` is
true and the up goes through `resolveRegisteredApplication` and fails at runtime
realization (no running Core) whether or not a daemon is available.

## Fix (hermetic test isolation)

- `configureIsolatedTestTarget` (cmd/baha/target_test_helpers_test.go): twin of
  `configureTestTarget` that
  1. clears leaked globals `BASEHARBOR_TARGET` / `BASEHARBOR_STATE_DIR` / `BASEHARBOR_ENV` (set globally by the runtime-integration bootstrap via `os.Setenv`, never rolled back — a leak that would make `effectiveTarget()` ignore this Test's config),
  2. provisions a **unique per-test Target** (`itest-<rand>-<nanos>`) so its docker project/network is isolated from every other test,
  3. uses ONE fresh `XDG_CONFIG_HOME`/`XDG_DATA_HOME` root.
- The registered-NAME up in `TestUpNameResumesThroughCommandEntrypoint` now runs
  from `repoRoot` (`t.Chdir(repoRoot)`) instead of an empty `t.TempDir()`, so the
  up resolves the registered deployment and fails at runtime realization
  deterministically. No production code change.
- Write-set: `*_test.go` only in cmd/baha.

## Local verification

- `go build ./cmd/baha`: OK
- `go vet ./cmd/baha`: OK
- gofmt: clean; source-readability-audit: PASS
- `go test ./cmd/baha -run 'TestUpName|TestParseRuntimeUpOptions|TestSelectControlPlanePort|TestRuntimeUpGuided|TestRecoveryFileForRepositoryUp|TestPortAvailable|TestRuntimePortDefaults'`: all PASS
- docker cleanliness after clean runs: 0 `bh-*` containers, 0 `bh-*` networks

## Hosted proof

- PR: https://github.com/mcpdev80/baseharbor/pull/1516 (branch `w286-0427-181-upname-hosted`, head `07fe960f6` = my commit; base `develop`).
- Candidate base: develop `fea92f379` (ancestor of my first commit, shown above).
- First hosted run 42637373933 (head `7a212c5f8`) still FAILED `got success` — up booted a fresh Core. This drove the corrected root cause.
- Second hosted run **42640378393** on updated head `07fe960f6`: status `completed/success`, `cli-package-tests` `completed/success`, Release Source Preflight ran `go test ./cmd/baha` (full package) and `go vet ./...` — 46 PASS / 0 FAIL in the captured matrix log. Fail-closed validation owner confirms `TestUpNameResumesThroughCommandEntrypoint` passed in the full matrix (not isolated).
- Evidence is the run result itself (run 42640378393); SOP witnesses (ls-remote, run id) at END.


## END

- (pending)
