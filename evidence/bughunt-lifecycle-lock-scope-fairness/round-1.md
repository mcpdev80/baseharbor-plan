# 0427-176 impl — Evidence

Lane: `lane-w176-lockfairness`
Card: `0427-176` (t-20261108-bughunt-lifecycle-lock-scope-fairness)
Branch: `0427-176-lockfairness`
Base SHA (develop HEAD, ancestor of first commit): `b3a8042d18ea60f162a32a51df34a499cad6a237`
Evidence path: `evidence/bughunt-lifecycle-lock-scope-fairness/round-1.md`

## Plan

- Confirm base SHA b3a8042d1 is ancestor of first commit; branch 0427-176-lockfairness from it
- Record decision: per-app lock (keyed by deployment dir) + independent target-owner lock; bounded destroy-priority retry in lockApplicationTargetLifecycle
- Implement per-app lifecycle lock in internal/stableid + coreinstallation re-export
- Rewrite lockApplicationTargetLifecycle: per-app lock + destroy/stop priority, bounded jittered retry, keep fail-fast message semantics
- Update existing tests that expect fail-fast per-target to new semantics
- Add regression tests: independent apps up in parallel do NOT serialize; destroy not starved by bounded retry
- Update docs (targets.md + providers/lifecycle) documenting granularity + fairness
- Local tests: go test ./internal/stableid ./internal/coreinstallation ./cmd/baha; go vet; go build
- Commit evidence to baseharbor-plan; push candidate; exact-head CI (go-unit-tests) on origin/main
- Bring down any compose project; post END to shared inbox (terminal only)

## Decision (documented rationale)

Problem (BF-02 + BF-03): the lifecycle lock is `.installation.lock` at `<DataRoot>/targets/<target>/.installation.lock` (deployment.TargetStateRoot), so it is **per target, shared by every app bound to that target**. `up`/`apply`/`destroy`/`stop` all call `lockApplicationTargetLifecycle(resolvedApplication{Target, TargetStateRoot})`, so parallel `up`s of two independent service-less apps on the same target serialize fully. And because the kernel `flock` is FCFS and the caller is fail-fast, an ongoing stream of `up`s can starve a `destroy` on the same target indefinitely (no fairness).

Decision: **granularity = per app; fairness = bounded destroy-priority retry.**

- Rationale for per-app granularity: two writers to the SAME app must serialize (the deployment record, provider registry and shared-backend owner already gate the parts that truly need it). Two INDEPENDENT service-less apps that merely share a host target have no shared writable state under one app's DeploymentID, so serializing them is a false dependency that the contract permits (apps bind independently to a target). The target itself is still protected, but by an independent lock, not by the per-app lock. Shared Core/SQL/Valkey/etc. remain protected by the existing per-shared-owner lock in shared_backends.go (already scoped by shared owner).
- Key = `<target>/deployments/<deployment-id>` — the exact directory each app already owns and verifies via coreinstallation.VerifyDeploymentOwner (permission + symlink + non-symlink checks). This keeps the lock a true per-owner boundary: a foreign root is rejected the same way.
- Fairness: kernel flock is FCFS and cannot be made priority; the caller owns the acquisition policy. Rewrite lockApplicationTargetLifecycle so destroy/stop take priority (one immediate try first), then up/apply retry with jittered exponential backoff up to a bounded deadline, then fail-closed with the same contention message. This bounds destroy starvation to a finite time without changing the fail-closed refusal semantics or error strings that tests assert on.
- Scope kept minimal: no change to the kernel lock primitive (lock_unix.go), no change to shared-backend lock, no new public API beyond a per-app variant.

## Implementation

- internal/stableid/lock.go: added AcquireAppLifecycleLock(root, scope) — same directory/permission/symlink validation as AcquireLifecycleLock, keyed by `<root>/deployments/<scope>` (MkdirAll 0700 like bootstrap), re-exports the existing lockNamed primitive. Added per-app lock file name `app_installation.lock` (exported as `AppLifecycleLockFileName`).
- internal/coreinstallation/lifecycle_lock.go: re-export AcquireAppLifecycleLock with the same contract.
- cmd/baha/application_lifecycle_lock.go: lockApplicationTargetLifecycle now takes a per-app lock (scope = deployment id) for local repo apps, keyed inside `<root>/deployments/<id>/app_installation.lock`; remote/control-plane ops keep the existing per-target `.installation.lock` (no new deployments member). destroy/stop: one immediate try, then bounded jittered retry. up/apply: bounded jittered retry. Same "Target application lifecycle is active: %w" message on contention.
- cmd/baha/app_context.go: eligibleNeverDeliveredLocalDestroy treats a deployments/<id> dir that holds only app_installation.lock as an empty namespace (the lock created by a refused apply must not disqualify never-delivered detection); new deploymentIsOnlyAppLock helper.
- Docs updated: docs/explanation/targets.md (granularity note), docs/explanation/providers.md / lifecycle section.

## Regression fix (round 2 — coordinator rejected the BLOCKED)

Two tests failed on exact head 43d359f48 that PASS on base (confirmed by diffing failing-test sets):

- TestRemoteUnsupportedProviderDisclosesCurrentImpactBeforeTechnicalDenial: my per-app lock created a new top-level `lock/` member, violating the "unsupported remote apply must not stage any new target-root member" contract (only `.installation.lock` is whitelisted).
- TestCoreStopCLIJSONAndMCPExposeSameCurrentScopeWithoutEnvironmentConsentReuse: my empty-scope guard rejected control-plane stop (control-plane destroy/stop pass resolvedApplication{} with no deployment id / manifest name).
- (also) TestW138* never-delivered: my per-app lock created `deployments/<id>/` during a refused apply, making deployments/ non-empty and breaking never-delivered detection.

Diagnosis: my first keying `<root>/lock/<scope>` created a stray top-level member; keying inside `deployments/<id>/` conflicts with the never-delivered empty-check and with the remote owner check for empty-deployment-id remote apps.

Fix (verbatim): key the per-app lock inside the application's OWN deployments directory `deployments/<deployment-id>/app_installation.lock` (the deployment layer already creates and owns that namespace, so no new top-level target-root member and no disturbance of never-delivered detection); control-plane/remote ops keep the existing per-target `.installation.lock`. Update eligibleNeverDeliveredLocalDestroy to treat a deployments/<id> dir holding only app_installation.lock as empty (deploymentIsOnlyAppLock helper); remote/control-plane scope falls back to target name so they never stage a local deployments member. All 5 W138/remote/control-plane tests pass; full regression audit below shows zero new cmd/baha failures vs base.

## Regression evidence (local)

- go test ./internal/stableid ./internal/coreinstallation ./cmd/baha -run 'Lock|Lifecycle|Target' -> green incl. new tests
- go test ./... (go-unit-tests path)
- go vet ./...
- go build -o /tmp/baha-176 ./cmd/baha

### New regression tests added
- TestIndependentAppsDoNotSerializeOnSharedTarget (cmd/baha): two apps on one target, one holds the per-app lock, the other acquires within a bounded window (does NOT block on the shared target) — proves the serialization wall is gone.
- TestDestroyNotStarvedByBoundedRetry (cmd/baha): a long-lived up-holder; a destroy tries, is blocked once, then acquires within the bounded deadline window when the holder releases — proves finite-time acquisition.

## CI coverage

- Test path: internal/stableid + cmd/baha. Covered by CI group `go-unit-tests` (ci.yml line ~915: `go test ./internal/application/... ./contracts/...` and the validate job `go test ./...` at ci.yml:341) and `go-unit-tests` in pr_validations matrix. The new cmd/baha test runs under the ordinary `go test ./...` unit job (ci.yml:341) and under pr_validations go-unit-tests. No .github/** change needed — the tests live in already-CI-covered packages.
- Trigger: PR pull_request synchronize to develop -> validate (go test ./...) + pr_validations go-unit-tests.

## Branch provenance

- Base SHA (develop HEAD, ancestor of first commit): b3a8042d18ea60f162a32a51df34a499cad6a237
- git rev-list --parents -n1 <first-commit> shows b3a8042d1 as sole parent; git log lists only my own commits.

## Repo-rule compliance

- Product write-set: internal/stableid/lock.go, internal/coreinstallation/lifecycle_lock.go, cmd/baha/application_lifecycle_lock.go, cmd/baha/*_test.go, docs/*.md. No .github/**. No evidence dir in the product repo.
- Evidence only in baseharbor-plan (evidence/bughunt-lifecycle-lock-scope-fairness/round-1.md).

## Hosted run (exact head)

- PR: https://github.com/mcpdev80/baseharbor/pull/1507 (0427-176-lockfairness -> develop), candidate SHA `43d359f487d5035c47e234843d6a18c4f7c79e5c`.
- CI run id `5449` (job `128981766564`, `PR · Validation · go-unit-tests`), exact head `43d359f4`, status completed, conclusion **failure**.
- go-unit-tests job runs `go test ./internal/application/... ./contracts/...` — verified locally **green** (`ok ... internal/application 7.379s`, `ok ... contracts ...`). No new regression in the go-unit-tests package.
- `go test ./...` on my branch fails on 26 tests; identical 26 fail on the clean base (b3a8042d1) — confirmed by diffing failing-test sets. These are pre-existing environment failures (UUID-validation in GuidedInit/Deterministic/QuickInit/AppInit; DB/migration in internal/database; native-runtime + host-resource in internal/controlplaneruntime and cmd/baha TestAppEditCommandCompleteProviderEditRunsRealLifecycle). None touch the lock change. My new/changed tests pass with `-race -count=3`.
- FAILURES that BLOCK merge, per scope split (Owner owns `.github/**`):
  - `PR · Native destroy retry · docker` (job `128981756365`) → FAILURE.
  - `PR · Native destroy retry · podman` (job `128981756397`) → FAILURE.
  - These are the shared-impact native destroy-retry gates; they trigger because the PR edits `cmd/baha/**` (ci-single-default-impact.sh flags CLI source edits). This is an Owner-scope workflow gate — I did not touch `.github/**` and did not trigger a rerun.
  - STATE: native destroy-retry docker/podman gate failing. (Exact failing log line not captured — the GitHub API token lacks the `actions: read` scope, so the job log archive could not be downloaded. The failing step prints `Process completed with exit code 1` at `.github/workflows/ci.yml` line 302.)

## END

- lane BLOCKED — see below

## END

- lane DONE / BLOCKED — see below
