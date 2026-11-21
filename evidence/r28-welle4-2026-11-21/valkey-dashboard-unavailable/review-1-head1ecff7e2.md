# PR #1714 review — head ecff7e2f575fb991fbe5c3c1c5f6785569d70228

ROLE: CODEX-REVIEW, reviewer-only. Mission: `/var/tmp/rev-1714-r1.md`.

## PLAN

1. Read rev-1714-r1 and record its exact head, acceptance criteria, and reviewer-only boundaries.
2. Verify the PR head/base, tree ancestry, changed paths, commit identities, and exact hosted run remotely.
3. Inspect Valkey selection labels, honest unavailable behavior, and golden query parity at file:line.
4. Verify both real-path regression directions and per-job execution evidence, then produce a verdict with remediation.
5. Render/check the evidence, publish it to Planning origin/main, verify the remote path, and record the end state.

## Remote candidate and provenance

The selected product remote `lane-origin` resolves to `https://github.com/mcpdev80/baseharbor.git`. Planning worktree remote, verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.

Fresh remote witness from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1714/head refs/heads/develop`:

```text
d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3 refs/heads/develop
ecff7e2f575fb991fbe5c3c1c5f6785569d70228 refs/pull/1714/head
```

Fetched the exact PR head and develop refs into `refs/review/pr1714` and `refs/review/develop`. Base count is 0; candidate count is 4; `git merge-base --is-ancestor refs/review/develop refs/review/pr1714` succeeded. The mission's prior candidate `8d8be417ef8` has tree `b71c37138b2afa2f7f6655ad937a69bf28db2a39`; current candidate tree is `3cda28ccd0f136c22b10a62ba0a3f5e6d9a4d67f`. They differ, so I inspected the full four-commit diff.

Changed paths:

```text
internal/metrics/perses_dashboards_valkey.go
internal/metrics/perses_dashboards_valkey_test.go
internal/metrics/testdata/perses-valkey/valkey-targets-verified.json
internal/metrics/testdata/perses-valkey/valkey-targets.json
```

Commit log and identities:

```text
ecff7e2f5 0428-183-realpos <0428-183-realpos@users.noreply.github.com> | Marcel Pfingstgräf <22537373+mcpdev80@users.noreply.github.com> | fix(0428-183 r3): valkey dashboard query on emitted baseharbor_provider label; report missing real verified producer
a11c44d7f 0428-183-realpos <0428-183@baseharbor.local> | Marcel Pfingstgräf <22537373+mcpdev80@users.noreply.github.com> | fix(0428-183 r4): drive valkey verified panel through injectable verification anchor, not finished enum
349372d7e worker <worker@baseharbor.local> | Marcel Pfingstgräf <22537373+mcpdev80@users.noreply.github.com> | fix(0428-183): verified Valkey dashboard carries a real query and contracts 0428-182
14403c777 worker <worker@baseharbor.local> | Marcel Pfingstgräf <22537373+mcpdev80@users.noreply.github.com> | fix(0428-183): valkey dashboard availability verified-gated
```

There are two author identities (`0428-183-realpos`, `worker`) and one committer identity (Marcel Pfingstgräf). The four commit bodies contain no accepted SHA certificate.

PR API state: #1714 OPEN, non-draft, mergeable, base `develop`, exact head `ecff7e2f575fb991fbe5c3c1c5f6785569d70228`.

## Valkey dashboard semantics

The emitted Prometheus target-group labels are set in `internal/metrics/prometheus_files.go:171-177`; `baseharbor_provider` is populated from `source.Provider`, while no `backend` label is emitted. The verified panel query now uses `up{baseharbor_provider="valkey"}` at `internal/metrics/perses_dashboards_valkey.go:258-278`. The exact emitted label is asserted by `internal/metrics/perses_dashboards_valkey_test.go:393-444`; the committed verified-dashboard golden carries the same query at `internal/metrics/testdata/perses-valkey/valkey-targets-verified.json:35`.

The producer reads Valkey's metrics status from `capability.ReferenceIntegrations()` at `perses_dashboards_valkey.go:210-245`. The current producer resolves `ObservabilityUnsupported`; the backend-verification function returns `ObservabilityVerifyNone` at `333-335`. The catalog emits a real dashboard only when status is `ObservabilitySupported` AND verification is `ObservabilityVerifyBackend`; all other combinations return an unavailable entry with no dashboard at `302-321`. The production `PersesValkeyDashboardAvailabilityResolved` caller reads both producer values at `459-464`. The serializer emits `DashboardUnavailable` and its reason for unavailable entries at `391-411`.

The negative production-path case `TestPersesValkeyDashboardAvailabilityResolvedUnavailableToday` calls `PersesValkeyDashboardAvailabilityResolved()` and asserts unavailable, no datasource, and `ObservabilityUnsupported` at `perses_dashboards_valkey_test.go:101-125`. This is honest unavailable behavior: no verified status is asserted when the verification function returns `ObservabilityVerifyNone`.

The positive branch regression `TestPersesValkeyDashboardVerifiedRealizesRealPanel` drives the shared availability/catalog and dashboard serialization path with an explicit supported + backend-verified test anchor at `perses_dashboards_valkey_test.go:301-349`; it confirms the available state and a real datasource/query. This injected positive is test-only. The production path remains unavailable today because its real producer returns unsupported and its real verification returns none. The fixture does not change production code.

Golden parity is present in both directions. `TestPersesValkeyDashboardVerifiedGolden` compares the complete marshalled dashboard bytes to the golden at test lines `355-370`; `TestPersesValkeyDashboardVerifiedQueryMatchesGoldenLine` pins the query line at `449-461`; the query implementation is at `perses_dashboards_valkey.go:276` and the golden line is `valkey-targets-verified.json:35`. The golden and source both carry the same `up{baseharbor_provider="valkey"}` query. The earlier unavailable golden remains reason-only and explicitly names `ObservabilityUnsupported`.

## Exact-head hosted run and regression execution

Run `44940738791` is `pull_request`, `completed/success`, and its head is exactly `ecff7e2f575fb991fbe5c3c1c5f6785569d70228`. Terminal aggregate `PR Selected Checks`, job `136958552540`, completed success at 2026-11-21T19:29:37Z. The run has 14 successful jobs, 21 skipped jobs, and 0 failed jobs.

The Go unit job `PR · Go unit · packages`, job `136957182124`, succeeded. Its log reports `ok github.com/mcpdev80/baseharbor/internal/metrics 0.568s` and `PASS all non-CLI Go package tests`. The package runner runs every non-CLI Go package with `go test -count=1` and no per-test filter, so the two source cases are in the executed package. The target cases are `TestPersesValkeyDashboardAvailabilityResolvedUnavailableToday` (negative production path) and `TestPersesValkeyDashboardVerifiedRealizesRealPanel` (positive injected verification path). Neither contains a skip branch.

The per-job log does not print either target test name or an individual test duration; searching the exact job log for both names and `no tests to run` returned no matches. It provides only the package duration `0.568s`, not the requested name-plus-duration evidence per case. Therefore actual package execution is established, but the mission's requested per-case log receipt is not present.

## Findings and remediation

1. REQUEST CHANGES — identity rule (card 0428-224). The candidate contains two authors (`0428-183-realpos`, `worker`) despite a single committer. Remedy: rewrite the complete four-commit PR range to one lane author identity, preserving the tree, or document a justified owner exception. The commit bodies contain no accepted SHA certificate, so author rewrite is permitted by the mission. Stop criterion: one author identity across the exact remote range, or a documented owner exception; then run exact-head required checks and re-review.

2. REQUEST CHANGES — per-case hosted evidence is incomplete. The exact-head package job ran and passed, but its log does not show each required test name and duration. Remedy: supply an authorized hosted per-job receipt that lists each of the two named cases, individual duration, and pass result on the exact head. No workflow or script change was made or requested in this review. Stop criterion: both required records appear for the exact reviewed head and are passing, not skipped.

## Verdict

REQUEST CHANGES for `ecff7e2f575fb991fbe5c3c1c5f6785569d70228`.

The security/status semantics are fail-closed and the emitted-label query matches the golden. The exact-head run and `PR Selected Checks` are terminal green, and the internal/metrics package executed. The candidate still violates the one-author identity requirement and lacks the mission's per-case log receipts. No product changes, comments, pushes, or merge actions were made.

executed-in-shard: yes

## repo-rule compliance

Reviewer-only. No local suite tests were run and no product files, workflows, scripts, or protected internal packages were modified. Evidence is confined to the Planning worktree.

## cleanliness

Docker inspection before: shell PID `3217437`; the eight listed `bh-itest-*` containers were all exited. No containers or compose projects were started or changed by this review. Docker inspection after: shell PID `3222309`; the same eight `bh-itest-*` containers remained exited. No container or compose-project state changed during this review.

END codex-rev-1747 DONE — REQUEST CHANGES: identity and per-case CI receipts remain outstanding; candidate `ecff7e2f575fb991fbe5c3c1c5f6785569d70228`.

## Publication witness

Exact output from `git ls-tree -r --name-only origin/main | grep 'evidence/r28-welle4-2026-11-21/valkey-dashboard-unavailable/review-1-head1ecff7e2.md'` after fetching `origin main`:

```text
evidence/r28-welle4-2026-11-21/valkey-dashboard-unavailable/review-1-head1ecff7e2.md
```
