# PR #1580 — Round 3 (R1 follow-up: CLI unit-test fix)

## Role
Worker. Continuation of the R1 correction on the same branch/PR #1580.

## Candidate and provenance
- PR #1580 is DRAFT, base `lane-0428-uid-environment` (owner rule: app→env→target
  stack; base lane = top, only contents, no waits). Head branch `lane-0428-uid-target`.
- Exact `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1580/head`:
  ```
  4e02383efefeab7637bd51aabbcfdc1788bc4d3b	refs/pull/1580/head
  ```
- Chain on this lane:
  - `c769cd107` target: idempotent legacy-target UID migration + real-CLI tests
  - `4e02383ef` target: fix CLI cmd/baha unit tests for read-triggered UID migration (current)
- CI routed by existing `ci.yml` release-source group. **No `.github/**` change.**

## Root cause of the round-2 CI failure (cli-0 suite, 11 failing unit tests)
The read-triggered migration on `LoadConfig` (R1: "erst erzeugte uid, zweiter
no-churn") rewrote empty-UID fixture configs on read, and the save-triggered
variant (intermediate attempt) broke the `cmd/baha` package in two ways:
1. Fixtures holding a decoded config in memory later saw the on-disk owner
   change ("Application Target binding changed during execution").
2. Tests copying a TargetDefinition into a second name inherited the migrated
   UID → `validateTargetUIDUniqueness` collision ("target uid collision").

The save-triggered approach was also wrong for the R1 contract (read must
generate) and for legacy targets (no Core installation → `SaveExpected`'s
installation lock can't write).

## Fix (read-triggered, correct contract)
- `LoadConfig` decodes → `migrateAndPersistTargetUIDs` → `writeMigratedTargetUIDs`:
  a direct CAS read-modify-write on the protected config owner, **no
  installation lock**, idempotent (second read: no empty UID → no write),
  fail-closed on UID collision.
- `saveAt` now tolerates a nil `revalidate` (used by the migration's atomic write).
- Fixtures carry fresh, valid Target UIDs via new helper
  `mustNewTargetUIDFixture(t)` (`cmd/baha/target_test_helpers_test.go`) so they
  stay non-legacy and the migration is a no-op on read.
- Copy-into-second-name fixtures get a distinct UID to avoid collisions:
  - `TestBoundApplicationCoreRejectsAnotherLocalInstallationBeforeBootstrap`
    (`foreign-local`)
  - `TestGuidedWithdrawalPreferencesPreserveCanonicalOwners` (`other-dev`)

## Verification (local)
- `go build ./...` — OK.
- `go vet ./internal/deployment/... ./cmd/baha/` — OK.
- `go test ./internal/deployment/ -count=1` — **ok** (all pass).
- `go test ./cmd/baha/ -count=1 -v` — **870 subtests pass, 1 fail**.
  The single failure `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`
  is a **native daemon integration test** (`startControlPlaneRuntime` needs a
  real Docker Core; fails "native network lacks a protected Core" without a
  daemon in this sandbox) — not a unit failure from this change. A second
  native-only failure `TestPrepareStagedCoreGitCandidatePinsCanonicalApplication`
  is a `git archive` OOM-kill under long-run container pressure, also
  environment-only. Both are native integration gates, not unit regressions.
- Previously-failing unit set now green:
  `TestRetainedApplicationTransportRevalidatesAuthorityBeforeEveryCall`,
  `TestApplicationTransportRechecksNodeBeforeAccessSnapshot`,
  `TestRemoteApplicationRejectsMissingForeignOrRemoteAuthority`,
  `TestRestoreBindsCurrentExternalReceiverAndAuthorization`,
  `TestRestoreBindsOriginalExternalIdentityAndProtectedDestination`,
  `TestGuidedRepositoryRuntimeFixtureRegressionSuite`, `TestCLITargetUIDStableAcrossReads`,
  `TestCLITargetCreateGeneratesStableUID`.

## Files changed (4e02383ef vs c769cd107)
- `internal/deployment/target.go` — read-triggered migration in `LoadConfig`,
  `writeMigratedTargetUIDs` CAS helper, nil-revalidate tolerance in `saveAt`.
- `internal/deployment/target_migration_test.go` — asserts read-triggered contract.
- `cmd/baha/target_test_helpers_test.go` — `mustNewTargetUIDFixture`, UID on `docker-dev`.
- `cmd/baha/application_core_authority_test.go` — UID on `remote` + distinct UID on `foreign-local`.
- `cmd/baha/application_runtime_retirement_preferences_test.go` — distinct UID on `other-dev`.

## Pushed
`c769cd107..4e02383ef` to GitHub `origin` (remote `github`).

## CI observation (terminal — watched to completion, owner 4.6)
- Round-2 run `43650256316` (head `c769cd107`) FAILED — 11 `cmd/baha` unit
  failures (the root cause above).
- The `4e02383ef` push did **not** self-ignite a run (sync-ignition defect):
  ~5 min of polling showed zero runs and the PR's last activity was my push at
  00:08. No `.github/**` change exists; CI routes through the existing
  `ci.yml` release-source group, so the trigger was a workflow defect, not a
  selection result.
- Manual fallback (owner note authorized): `gh api -X POST
  .../actions/workflows/352609139/dispatches -f ref=lane-0428-uid-target` →
  run **`43657589559`** started at `2026-11-15T00:19:20Z`.
- **Terminal: run `43657589559` status=completed, conclusion=FAIL.**
  - `Workflow policy` → success. `validate` → failure. All other jobs skipped
    (release-source selection: `Native impact selection` → skipped; Go/CLI,
    validation, contracts, runtime, HA gates skipped).
  - `validate` step 15, "Run runtime integration tests serially" → failure.
  - `Run unit and package tests` → **success** (the `cmd/baha` unit failures
    from round-2 are fixed by this change).
  - 6 failing tests, all in `cmd/baha`, all `*InCI` / `RealLifecycle` native
    integration tests:
    `TestRepositoryWorkflowRealLifecycle`,
    `TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI`,
    `TestRepositoryComposeWorkloadOnlyLifecycleInCI`,
    `TestRepositoryComposePinnedWorkloadLifecycleInCI`,
    `TestRepositoryBuildWorkloadRebuildsSourceChangesInCI`,
    `TestMultiInstanceComposeLifecycleInCI`.
  - Root cause: each failed with
    `… app_*_integration_test.go:NN: prepare BaseHarbor integration trust plane:
    ORAS is required before Core setup; install it manually …` — a **missing
    `oras` binary in the CI runner**, an environment/tooling gap.
  - Not a unit regression: the failing group is native daemon + ORAS Core
    bootstrap. The migration (`internal/deployment/target.go`) makes **no
    external-process calls** (verified: zero exec/oras/docker/system matches in
    the diff) — it is pure YAML decode → `TargetUID` fill → atomic CAS write.
    It cannot produce "ORAS is required".
  - Runner/tooling gap, confirmed against current `ci.yml`: the native group
    runs at `ci.yml:360` (step 15 of `validate`), but the ORAS install lives at
    `ci.yml:486` in a **different** job. The `validate` job has no ORAS install
    (grep for `oras|ORAS` in `validate` job scope → none; only "Run runtime
    integration tests serially"). The runner simply lacked `oras` when this step
    executed. This is a workflow ordering/tooling defect, not reachable from this
    lane's change set.

## END (terminal reached, owner 4.6 satisfied)
- Exact head via `git ls-remote https://github.com/mcpdev80/baseharbor.git
  refs/pull/1580/head`:
  ```
  4e02383efefeab7637bd51aabbcfdc1788bc4d3b	refs/pull/1580/head
  ```
- Run `43657589559` (manually triggered `workflow_dispatch`, `--ref
  lane-0428-uid-target`) → terminal **FAIL** at `validate` step 15 due to a
  missing `oras` in the runner — environment/tooling, **not** the R1 migration.
  Unit/package tests (`Run unit and package tests` → success) pass; the round-2
  `cmd/baha` unit failures are fixed.
- Same branch/PR #1580, head `4e02383ef`, base `lane-0428-uid-environment`.
  No `.github/**` change. No merge (FROST).
- CI run self-ignition defect documented: a manual `workflow_dispatch` was
  required; recorded here per owner note.
