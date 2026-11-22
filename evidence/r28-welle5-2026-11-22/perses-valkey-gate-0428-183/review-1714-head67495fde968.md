# CODEX-REVIEW: PR #1714 exact-head hop

## PLAN

1. Verify that `67495fde96837846d9d2b26e8db5ad93b7b7c988` adds only develop content over `fc525970d4171e5e15a1a734a1a38193dcd55971`.
2. Inspect the producer path and regression test against the exact candidate.
3. Verify exact-head run `44989324573`, required package/metrics shards, and PR state.
4. Publish the verdict and supersede the prior-head evidence.
5. Verify planning evidence publication and post coordinator END.

Session marker: 1450c201
Review role: CODEX-REVIEW, read-only
Candidate: `67495fde96837846d9d2b26e8db5ad93b7b7c988`
Base develop: `1ff16925c4e141d732459a34ddf0b7f49128a214`

## Verdict

VERDICT: APPROVE

## Findings

- Additive hop: `git log fc525970d4171e5e15a1a734a1a38193dcd55971..67495fde96837846d9d2b26e8db5ad93b7b7c988` shows the hop commit and develop commit `1ff16925c4e`; `git diff fc525970d4171e5e15a1a734a1a38193dcd55971 67495fde96837846d9d2b26e8db5ad93b7b7c988` contains only the seven paths from develop PR #1755. The PR's own four-file diff against develop remains confined to `internal/metrics/perses_dashboards_valkey.go`, its test, and two Valkey testdata files. No new PR product or test edits were introduced by the hop.
- Producer path: the exact head contains the producer in `internal/metrics/perses_dashboards_valkey.go` (the mission's `cmd/baha/perses_dashboards_valkey.go` path is not present). `persesValkeyBackendVerified()` at lines 324–352 resolves the `baseharbor/valkey` metrics signal and verification from `capability.ReferenceIntegrations()`, using the same catalog as `persesValkeyResolvedSignalStatus()` at lines 225–250. The canonical availability producer at lines 471–481 passes both resolved values into the availability resolver. The fix is at the producer/availability source, rather than a CLI presenter.
- Regression: `TestPersesValkeyBackendVerifiedReadsReferenceCatalog` at `internal/metrics/perses_dashboards_valkey_test.go:486` exercises backend-verified, supported but unverified, and unsupported catalog states. Exact-head CI run `44989324573` includes the `internal/metrics` package in successful `PR · Go unit · packages` job `137106741719`; its log reports `ok github.com/mcpdev80/baseharbor/internal/metrics 0.490s`. The package job executes the regression test with the package suite.
- Protected files: the exact PR diff lists only `internal/metrics/perses_dashboards_valkey.go`, `internal/metrics/perses_dashboards_valkey_test.go`, and the two `internal/metrics/testdata/perses-valkey/*` files. `internal/observability/registry.go` and `internal/capability/perses_selection.go` are unchanged.
- The three previously named tests remain unchanged in the PR diff and are included in the green `internal/metrics` package suite: `TestWorkloadOnlyRegistersSharedSnapshotOnDeploy`, `TestServiceAppKeepsRuntimeSourceRegistrationOnDeploy`, and `TestVerifyProviderAndApplicationSourcesSkipsOnlySnapshotMetadata`.

## Hosted CI and PR state

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1714/head` returned develop `1ff16925c4e141d732459a34ddf0b7f49128a214` and PR head `67495fde96837846d9d2b26e8db5ad93b7b7c988`.
- Exact run `44989324573` completed SUCCESS at the exact candidate head. Required aggregate `PR Selected Checks` job `137107855881` completed SUCCESS.
- Relevant executed jobs: `PR · Source format` `137106702403` SUCCESS; `PR · Focused Python` `137106741658` SUCCESS; `PR · Go unit · packages` `137106741719` SUCCESS with the internal/metrics package result above. Native, release, and HA paths were skipped by selection; no selected-check failures are present.
- PR #1714 is OPEN, not draft, with `mergeStateStatus=CLEAN`.

## Repo-rule compliance

Read-only product review. No local tests run, no product files changed, no workflow dispatched, no PR comment, no merge or close. Planning evidence repository remote was verified before commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `(push)`.

## Cleanliness

Before review: PID `2484948`; `docker ps -a` returned no containers. No containers or compose projects were started.

## END codex-rev2-1736 DONE

APPROVE at `67495fde96837846d9d2b26e8db5ad93b7b7c988`; additive hop contains only develop PR #1755 content. Exact CI run `44989324573` completed SUCCESS.
