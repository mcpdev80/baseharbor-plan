# Round 1 — uid-environment implementation brief (t-20261114-r28-cli2-uid-environment / card 0428-051)

- Shift: r28-welle1, 2026-11-14
- Worker lane: `lane-0428-uid-environment` (Owner-Direktive: Coordinator-Worker; this lane owns only this slice and its dedicated tests)
- Mission: `/tmp/opencode/mission-uid-environment.md` (line 8 evidence path, line 2 merge-frost DRAFT-only, base develop 0e9ccb582)
- Base product (`origin/develop`): `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (verified against fresh clone)
- Base plan (`origin/main`): `26a6d034314298cf6661affa6d89e1d7f1dec53f` (verified: `git ls-remote`)
- Card: `t-20261114-r28-cli2-uid-environment` (0428-051), state `active`, owner `lane-0428-uid-environment`, depends on `t-20261114-r28-cli2-contract` (accepted)
- Contract: `evidence/cli-redesign-20261114/contract/cli-command-contract-v1.md` §6 (env identity model) + brief §Owner decisions + command-map + code-entry-index
- Merge-frost (Owner directive 2026-11-14): NO merge to develop; PR DRAFT only (base develop); aeste/pushes allowed; no release/tag.

## PLAN

- Establish working brief (scope decision, base attestation, witnesses)
- Read contract + exact current lines before any change
- Implement internal/environment package (NewEnvironmentID/ValidateEnvironmentID, uniqueness/concurrent, rename stability, migration, multi-app/nodes)
- Wire internal/deployment/deployment_store.go interface (owned slice only; shared-file changes via coordinator)
- Add focused unit tests (uniqueness, concurrency, rename, migration) + CI mapping
- Local focused tests + vet + build at exact SHA
- Cut candidate branch from 0e9ccb582 + DRAFT PR (base develop)
- Hosted CI run on exact head (Owner scope; no rerun edit) + record run-id/PASS
- Push evidence to origin/main (ls-remote witness BEFORE END) + compose cleanup + END

## Scope decision (Owner-answered 2026-11-14)

- The product checkout `baseharbor` working-tree HEAD was `84f60778a` — an unpushed merge of 0427-175 worker work, NOT a descendant of `origin/develop`. NOT carried. This `84f60778a`/local `aff1532c` is a quarantined/local-artefactor reference (workers/baseharbor gesperrt — never cite; precedent w282/phantom-commits). Reported path for owner to close.
- Unpushed 175 branches: already merged upstream `bc839f054`; nothing to rescue.
- Cut `lane-0428-uid-environment` worktree EXACTLY at `0e9ccb582`; work under `/tmp/opencode/lane-0428-uid-environment-wt`.
- Evidence location: planning repo only (`evidence/r28-welle1-2026-11-14/cli2-uid-environment/`). No `.evidence/` in product repo.

## Base attestation

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `0e9ccb582f5bdcdc74049bbe3996263cdce6500c  refs/heads/develop`
- `git ls-remote https://github.com/mcpdev80/baseharbor.git HEAD` => `aff1532c2f6c6782a8c13afad83245d1351815e7  HEAD` (real GitHub deploy head; develop NOT ancestor of HEAD — develop has not merged into deploy head; expected).
- Worktree at exact base:
  - `cd /tmp/opencode/lane-0428-uid-environment-wt && git rev-parse HEAD` => `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`
  - `git merge-base --is-ancestor 0e9ccb582 HEAD` => PASSES (base is ancestor of first commit — to be re-verified at PR time).
- Plan repo remote verified: `git ls-remote origin` => `26a6d034314298cf6661affa6d89e1d7f1dec53f  refs/heads/main`.

## Contract facts (from cli-command-contract-v1.md §6 + brief)

- Environments, apps, targets each carry a STABLE ID; deployment IDs remain separate. Environment shared by many apps/nodes; an app may live in many environments. Distinguish env/target/app identity; no implicit shared data/credentials.
- Owner (brief line 14) wants a non-secret `app.id` committed in versioned `baseharbor.yaml`, generated at new/init, reused by another checkout/Core, historical ID preserved, conflicts rejected.
- This task: system-generated NONSECRET uid ONCE per environment, reuse existing uid on brownfield, stable identity across all paths. Independent of app/node/target/deployment. Ownership/locking + versioned storage.

## Current-state witnesses (exact lines before change)

- `app.id` already exists and is committed (contrary to brief line 14's "current develop omits ID" note — the codebase has evolved past v0.4.25):
  - `internal/application/identity.go` — `NewApplicationID()`, `MustNewApplicationID()`, `ValidateApplicationID()` (wraps `stableid.NewUUIDv4("application")` / `ValidateUUIDv4`).
  - `internal/application/manifest.go:228` — `New()` sets `ApplicationID: MustNewApplicationID()`.
  - `internal/application/manifest.go:20` — `Manifest.ApplicationID` field.
  - `internal/application/manifest_parse.go:270-272` — authored `app.id` rejected (`system-owned`); canonical parse preserves it (`manifest_parse.go:272`).
  - `internal/application/manifest_parse.go:62` — `ParseCanonicalYAML` validates the ID.
  - `internal/application/manifest_render.go:11` — render clears `ApplicationID` from authored serialization.
- Environment is currently a plain string selector (NOT an identity):
  - `internal/application/manifest.go` — `Manifest.Environment` string.
  - `internal/application/environment.go` — `ResolveRepositoryEnvironment` / `RepositoryEnvironmentSelection.Environment` (string), slug-validated via `validateSlug("environment", requested)`.
  - `internal/application/environment.go:207` — `RepositoryEnvironmentStateRoot` = `.<repo>/.baseharbor/environments/<env>` (explicit/multi-env case).
  - `internal/deployment/deployment_store.go:235` — `DeploymentIdentity.Environment` string; `Validate()` requires non-empty, no `/`.
  - `internal/application/environment_test.go` — existing tests, package `application`.
- `internal/stableid/id.go` — `NewUUIDv4(label)` / `ValidateUUIDv4(label, id)` (already used for app/deployment).
- CI: `ci.yml` runs `go test ./internal/... ./cmd/baha` — `internal/application` and `internal/deployment` are covered; `cmd/baha` env tests covered by the same job. New tests in `internal/environment` and `internal/deployment` are picked up by that existing job (NO `.github/**` change needed — confirmed by mapping the two new test files to existing paths).

## Implementation (r28 round-1) — DONE, tested, unverified-on-remote

- New package `internal/environment` (`environment.go`): `NewID()` / `MustNewID()` / `Validate()` / `ValidateNonEmpty()` + `Environment{ID,Name}` with `Rename` (ID preserved). UUIDv4 via stableid. Name slug-validated (mirrors target slug).
- New seam `internal/deployment/environment_identity.go`: `GetEnvironment(target, env)` / `EnvironmentID(target, env)` / `EnvironmentRecord{Target,Name,Identity}`. Home: `targets/<target>/.baseharbor/environments/<env>/environment.json` (OUTSIDE deployment-registry namespace `targets/<t>/deployments`).
  - First creation: MkdirAll primes the Target root (so the shared `WithDeploymentRegistryWriteLock` engages — see finding below), then takes the Target-wide registry write lock, re-checks, creates atomically via temp+rename, foreign-claim rejection at rename.
  - Idempotent: existing record returns unchanged (brownfield reuse). Renames never reach this seam with a new ID.
  - Non-blocking lock with bounded retry: concurrent first-registration losers retry (env creation is rare/cheap) and converge on the winner's ID; the winner's rename is the atomic single-source-of-truth.
- Tests: `internal/environment/environment_test.go` (9 tests) + `internal/deployment/environment_identity_test.go` (7 tests incl. 32-goroutine concurrent-registration atomicity + per-target isolation + brownfield reuse + namespace isolation + invalid-input fail-closed).
- LOCAL RESULTS (exact candidate SHA = 0e9ccb582 worktree HEAD):
  - `go build -buildvcs=false ./...` — OK
  - `go vet ./internal/environment/ ./internal/deployment/` — OK
  - `go test ./internal/application/ -count=1` — ok (2.7s)
  - `go test -race ./internal/deployment/ ./internal/environment/` — ok (2.5s / 1.2s)
  - `go test ./cmd/baha/ -run 'Test.*Environment|Test.*Env' -count=1` — ok (60.9s)
  - CI mapping: `internal/environment` + `internal/deployment` covered by existing `go test ./internal/... ./cmd/baha` (ci.yml). NO `.github/**` change required.

## Finding: shared registry lock does NOT engage until the Target root exists

- `internal/deployment/registry_lock.go:WithDeploymentRegistryWriteLock` runs `fn()` **lock-free** when `TargetStateRoot(target)` does not exist (`os.ErrNotExist` → `return fn()`). On the very first concurrent registration of a brand-new Target, all first-writers race through the UNLOCKED path and each writes its own identity — a genuine double-create hole.
- Fix applied in this seam: `GetEnvironment` calls `os.MkdirAll(filepath.Dir(home), 0o700)` BEFORE `WithDeploymentRegistryWriteLock`, priming the Target root so the lock engages. MkdirAll writes no record (never mutates observable state). This is safe: the lock is shared with `SaveDeploymentRecord` and unchanged here; the prime is idempotent.
- NOTE for Owner: the shared `WithDeploymentRegistryWriteLock` still has the "no lock until root exists" property. It is not a bug for deployments because a deployment's first registration is gated elsewhere; but a reviewer may want the same priming (or a lock-on-missing-root) there. **Reported as STATE — Owner scope, not edited.**

## TODO / unknowns (reported to Owner 2026-11-14)

- CLI wiring: whether `environment_id` must be surfaced via a new `env` command or only reachable through the deployment seam. The card's card-level entry point is `internal/environment` + `deployment_store.go` interface; this lane owns the seam and its tests. CLI UX (new `env` command, `-e/--environment` resolving to the durable ID) is reserved for the umbrella CLI-integration owner — **reported as STATE (file:line pending) — Owner scope, not edited.**
- Exact deployment-store interface method (if any) that should expose `EnvironmentID` to `cmd/baha` — confirmed NOT needed: the seam reads/writes the existing per-Target deployment-state home directly; `deployment_store.go` is unchanged.

## End-of-shift marker

- END status: in progress (round 1 brief established; implementation pending)
- Candidate SHA: none yet
- Next trigger: implement internal/environment package

## Round-1 implementation — DONE (2026-11-14)

- New package `internal/environment` (`environment.go`): `NewID()` / `MustNewID()` / `Validate()` / `ValidateNonEmpty()` + `Environment{ID,Name}` with stable UUIDv4 identity (via `stableid`) and slug-validated, renameable name. Rename never changes the ID.
- New seam `internal/deployment/environment_identity.go`: `GetEnvironment(target, env)` / `EnvironmentID(target, env)` / `EnvironmentRecord{Target,Name,Identity}`. Home: `targets/<target>/.baseharbor/environments/<env>/environment.json` (OUTSIDE the deployment-registry namespace `targets/<t>/deployments`).
  - First creation: primes the Target root with an idempotent `MkdirAll` (so the shared `WithDeploymentRegistryWriteLock` engages), takes the Target-wide registry write lock, re-checks, creates atomically via temp+rename with foreign-claim rejection.
  - Idempotent brownfield reuse; renames never reach the seam with a new ID.
  - Non-blocking lock with bounded retry: concurrent first-registration losers retry (env creation is rare/cheap) and converge on the winner's ID; the winner's rename is the atomic single-source-of-truth.
- Tests: 9 (`internal/environment/environment_test.go`) + 7 (`internal/deployment/environment_identity_test.go`): uniqueness, UUID shape, invalid-input fail-closed, rename-stability, 32-goroutine concurrent-registration atomicity, per-target isolation, brownfield reuse, namespace isolation.
- LOCAL RESULTS (exact candidate SHA = 0e9ccb582 worktree HEAD):
  - `go build -buildvcs=false ./...` — OK
  - `go vet ./internal/environment/ ./internal/deployment/` — OK
  - `go test ./internal/application/ -count=1` — ok (2.7s)
  - `go test -race ./internal/deployment/ ./internal/environment/` — ok (2.5s / 1.2s)
  - `go test ./cmd/baha/ -run 'Test.*Environment|Test.*Env' -count=1` — ok (60.9s)
  - CI mapping: `internal/environment` + `internal/deployment` covered by existing `go test ./internal/... ./cmd/baha` (ci.yml). NO `.github/**` change required.
- HOSTED CI (run id 43644615047, candidate SHA 670402fde, PR #1578, base develop):
  - Triggered by PR push (ci.yml `pull_request` + `push` triggers). NOT a rerun/dispatch (Owner scope).
  - Result: **completed / success**. Active jobs all `success`:
    - `PR · Draft source and routing` → success
    - `PR · Draft Go · cli-0` → success
    - `PR · Draft Go · cli-1` → success
    - `PR · Draft Go · cli-2` → success
    - `PR · Draft Go · packages` → success
    - `PR · Draft Go · cli-3` → success
    - (remaining jobs skipped — gated on non-draft / release branches)
  - Witness: `gh api repos/mcpdev80/baseharbor/actions/runs/43644615047/jobs --jq '.jobs[] | "\(.name)  \(.conclusion)"'` → all active jobs `success`.
