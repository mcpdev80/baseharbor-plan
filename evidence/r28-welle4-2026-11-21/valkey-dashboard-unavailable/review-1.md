ROLLE: REVIEW

## PLAN

1. Verify current GitHub remote, PR #1714 head/base, and develop ancestry; record the exact candidate SHA. Done.
2. Inspect the availability decision and both unavailable/verified test paths with file and line evidence. Done.
3. Verify golden testdata provenance and query target labels; distinguish checked from not checked. Done.
4. Compare both mutation-proof tests against exact candidate `0afcaf374225b206789770499a7aa3b55daf807d`. Done.
5. Record exact-head checks, findings, verdict, and publish only this evidence file. In progress.
6. Post final status with review evidence commit SHA. Pending.

Review time: 2026-11-21 14:59 UTC.

## Candidate and ancestry

Product remote identity was checked first: `lane-origin https://github.com/mcpdev80/baseharbor.git`. The exact remote PR head is `0afcaf374225b206789770499a7aa3b55daf807d`, and the exact current develop head is `22fc68ebc0655874bc3f6aa886ff356dcad79624`. PR #1714 is open, `draft=false`, base `develop`, mergeable. The PR candidate's parent is `dea88c8f2caa2db93c1216c619993e444080a9d2`; that SHA is an ancestor of the candidate. `git rev-list --count <candidate>..<current-develop` is 4. Current develop is not an ancestor of this candidate; the candidate remains the exact pre-hop head this review was asked to assess. The base drift is not itself a content finding.

`git log --format='%H|%an|%s' current-develop..candidate` lists one commit: `0afcaf374225b206789770499a7aa3b55daf807d|0428-183-hopdev|hop(0428-183): rebase 1714 valkey onto develop dea88c8f2caa (layer verified-panel on RequiresAdapter base; fix golden + assertions to RequiresAdapter)`. Author matches the assigned lane. `git diff --name-only dea88c8f2caa...candidate` lists exactly:

- `internal/metrics/perses_dashboards_valkey.go`
- `internal/metrics/perses_dashboards_valkey_test.go`
- `internal/metrics/testdata/perses-valkey/valkey-targets-verified.json`

No tabu path is changed.

## Checks and durable test route

Run `44911551416` is `pull_request`, `completed/success`, exact head `0afcaf374225b206789770499a7aa3b55daf807d`. `PR Selected Checks` job `136869671199` and `PR · Trusted Plan` job `136868266230` pass. `PR · Go unit · cli-0`, `cli-1`, `cli-2`, `cli-3`, `owner`, and `packages` all pass. The packages job `136868330055` is `success`; its `Execute selected Go tests with isolated PostgreSQL` step is `success`, so the `internal/metrics` Go package test group ran on the reviewed head. No test count is claimed.

Attempt to retrieve the individual packages job log with `gh run view 44911551416 --job 136868330055 --log` returned `failed to get run log: zip: not a valid zip file`. Therefore no per-test log lines or per-test counts are claimed. No workflow rerun or new test run was started.

The test path is durable: `internal/metrics/**` is covered by `PR · Go unit · packages` on the `pull_request` trigger; that job and its test execution step succeeded at the exact reviewed head.

## Findings

### P1 — verified output test injects Supported instead of proving the real producer path

The production catalog path reads `persesValkeyResolvedSignalStatus()` (`internal/metrics/perses_dashboards_valkey.go:225-245`) and `persesValkeyDashboardCatalog()` passes that value into the fail-closed builder (`:284-314`). Only `ObservabilitySupported` yields a dashboard; all other statuses yield the unavailable entry (`:284-303`). The actual reference catalog at the candidate's base declares Valkey metrics `ObservabilityUnsupported` with `VerificationNone` (`internal/capability/reference.go:51-60`).

The negative proof is real: `TestPersesValkeyDashboardCatalogIsUnavailableOnly` calls the no-argument production catalog and asserts unavailable/no panels (`internal/metrics/perses_dashboards_valkey_test.go:19-36`). `TestPersesValkeyDashboardProducerReadsReferenceCatalog` pins the producer to the real reference status (`:177-201`). The three-state test also maps Unsupported to unavailable (`:155-168,246-277`).

The positive test is synthetic: `TestPersesValkeyDashboardVerifiedRealizesRealPanel` passes `capability.ObservabilitySupported` directly to `PersesValkeyDashboardAvailability` (`internal/metrics/perses_dashboards_valkey_test.go:285-319`), bypassing the producer. The candidate has no real supported Valkey metrics signal or source; its current reference status is Unsupported. This proves the builder can render a panel for a supplied enum, not that a verified Valkey signal reaches the normal dashboard path.

Recipe: test the normal producer/catalog path using an authoritative fixture that represents a contract-backed, backend-verified Valkey metrics signal, and assert the resulting public availability output and queryable dashboard. If no such Valkey signal/source contract exists, keep the catalog unavailable-only and do not claim a verified positive Valkey dashboard. Do not use a bare injected Supported status as the positive producer witness.

### P2 — the verified Prometheus query uses a label the target writer does not emit

The panel query is `up{job="baseharbor-providers", backend="valkey"}` (`internal/metrics/perses_dashboards_valkey.go:262-270`; golden JSON line 35). The provider target writer emits `job`, `baseharbor_provider`, `baseharbor_source`, `baseharbor_source_class`, and `baseharbor_metrics_path` (`internal/metrics/prometheus_files.go:171-182`); it does not emit `backend`. The existing Prometheus query builder selects provider up-series with `baseharbor_provider` and `baseharbor_source` (`internal/metrics/perses_prometheus_datasource.go:438-444`). The dashboard test only checks that serialized JSON contains the strings `datasource` and `query` (`perses_dashboards_valkey_test.go:310-319`), so it does not catch the invalid selector. No Valkey `MetricsSource` ID is present in the candidate tree, and the real catalog currently declares the signal unsupported.

Recipe: derive the query from a real registered Valkey source using emitted `baseharbor_provider` and exact `baseharbor_source` labels; assert the exact selector and schema-valid Perses payload in the golden test. Stop with the panel unavailable if no contract-backed source ID and query can be established. Do not describe an unverified/empty time series as a working positive dashboard.

### P3 — unavailable reason contradicts the reference contract

The candidate base's Valkey metrics signal is `ObservabilityUnsupported` with `ObservabilityVerifyNone` (`internal/capability/reference.go:59`). The candidate still reports `RequiresAdapter` in `persesValkeyUnavailableReason` (`internal/metrics/perses_dashboards_valkey.go:192`), comments on the producer (`:221-222`), and assertions in `perses_dashboards_valkey_test.go:150-152`. The prior round-3 hop evidence says these were intentionally changed to RequiresAdapter, but that claim does not match the actual tree at base `dea88c8` or the exact candidate.

Recipe: align the reason, comments, tests, and unavailable golden with `ObservabilityUnsupported` and `VerificationNone`. Keep separate states only where the reference contract defines them; do not relabel Unsupported as RequiresAdapter.

## Mutation proof review

The exact candidate contains both isolated mutation-guard tests: `TestPersesValkeyDashboardMutantPredicateRevertedIsolated` requires a Supported status to produce a dashboard (`perses_dashboards_valkey_test.go:204-220`), and `TestPersesValkeyDashboardMutantAvailabilityForcedIsolated` requires empty status to remain unavailable (`:223-236`). Both are in the changed test file at `0afcaf374...`, and the exact-head packages test step passed. These assertions cover the expected failure conditions in source. However, the round-3 evidence does not record applying either mutant and observing the test fail on `0afcaf374...`; it records the test names and ordinary suite result. The old review's mutation analysis was for `18e84809634e2b65cff8cdaaf8fd9d80f42c8906`. Per-job log retrieval for this head failed as recorded above, so no direct mutant-run result or per-test count is claimed. A direct exact-head mutation receipt remains required to close this acceptance point.

Recipe: apply the unavailable-to-available mutation and remove the verification predicate on the exact candidate SHA, recording the failing test and output for each. Do not reuse the older head's mutation evidence. Keep the tests in the `PR · Go unit · packages` pull_request route.

## Testdata provenance and live comparison

`git log --format='%h|%an|%ad' --date=iso-strict <candidate> -- internal/metrics/testdata/perses-valkey/valkey-targets-verified.json` returns `0afcaf374|0428-183-hopdev|2026-11-21T14:50:53+01:00`: the fixture was introduced by the candidate's own hop commit, not captured from a prior real `baha` output. `TestPersesValkeyDashboardVerifiedGolden` generates JSON from `persesValkeyDashboardCatalogWithStatus(ObservabilitySupported)` and compares it byte-for-byte to the fixture (`perses_dashboards_valkey_test.go:322-337`). The fixture repeats the candidate's `backend="valkey"` selector. A real `baha`/Valkey environment comparison was not performed; no new environment or infrastructure was started, and the reference contract currently has no supported Valkey metrics source.

## Verdict

REQUEST CHANGES at exact head `0afcaf374225b206789770499a7aa3b55daf807d` for the positive-path proof, invalid query label/source, stale contract wording, and missing exact-head mutation receipts. The current develop head is four commits newer, but this is not a request for changes based only on base drift; the content findings above remain on the reviewed head. Re-review after correcting these findings and then hop the candidate onto the then-current develop before merge. No merge, PR comment, product edit, or workflow action was made.

## cleanliness

Before: `docker ps -a`, pid 4028976; output was header only: `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`.
After: `docker ps -a`, pid 4038794; output was header only: `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`.

## repo-rule compliance

Read-only independent review. No product files, branches, PR comments, cards, workflows, or hosted checks were changed or triggered. No standalone product tests were run; the mandated local fast-check attempt and its failure are recorded below. No subagents were used. Planning repository remote was verified before evidence publication: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

## Validation state

The required pre-push `bash scripts/ci-fast-check.sh` completed with local failures caused by `/tmp` disk quota. The output included `error: copy-fd: write returned: Disk quota exceeded`, `fatal: cannot copy ... update.sample ... to /tmp/.../.git/hooks/update.sample: Disk quota exceeded`, and final `[Errno 122] Disk quota exceeded`; the Candidate advisory setup failed while the trusted base plan was reported unaffected. This is a local pre-push validation state, not a failure of PR #1714's hosted selected check, which passed at the exact candidate.

`python3 scripts/plan.py check` reported a separate existing error in an unrelated untracked file: `error: evidence/r28-welle4-2026-11-21/perses-status-backend-witness/round-9-genuine-witness.md: broken link 'docs/development/minimal-ci-receipts.md'`. That file is outside this review's write set and was not modified. The validator reported no error for this review file.

END codex-rev-1747 DONE: REQUEST CHANGES at candidate 0afcaf374225b206789770499a7aa3b55daf807d; exact-head evidence publication pending.
