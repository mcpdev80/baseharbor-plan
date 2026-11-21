# CODEX-REVIEW — PR #1714 / card 0428-183

## PLAN

1. Verify the product GitHub remote and refresh PR #1714 refs, current base, open/merge state, and the exact tested head/run.
2. Inspect the candidate source and diff to establish whether dashboard flags are written only after publication is proven and the result is unavailable-only.
3. Inspect the author and committer for each commit at the live head; determine whether another identity is included and whether any hop commit adds identity.
4. Write a review-only verdict with exact source, CI, identity, and predecessor evidence; preserve the earlier review and owner-hop records.
5. Publish only this evidence to verified Planning `origin/main`, capture the remote path witness, and post END.

## Remote state and candidate

Planning worktree remote, verified before evidence publication: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`. The selected product remote is `https://github.com/mcpdev80/baseharbor.git`. Fresh `git ls-remote` output:

```text
42da7128e724a533349e93d3742cbd232ea48936 refs/heads/develop
ecff7e2f575fb991fbe5c3c1c5f6785569d70228 refs/heads/lane-0428-183-valkey-dashboard-gate
ecff7e2f575fb991fbe5c3c1c5f6785569d70228 refs/pull/1714/head
```

PR #1714 is OPEN, non-draft, base `develop`, branch `lane-0428-183-valkey-dashboard-gate`, head `ecff7e2f575fb991fbe5c3c1c5f6785569d70228`, `MERGEABLE`, and reports `BEHIND`. The live develop SHA is `42da7128e724a533349e93d3742cbd232ea48936`. GitHub compare against develop reports merge base `d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3`, candidate ahead by 4 and behind by 19 (`diverged`). The earlier mission base SHA `513488eeb6d788f0e5eec054be89807505f05e08` is not the current develop head.

Changed paths are exactly:

```text
internal/metrics/perses_dashboards_valkey.go
internal/metrics/perses_dashboards_valkey_test.go
internal/metrics/testdata/perses-valkey/valkey-targets-verified.json
internal/metrics/testdata/perses-valkey/valkey-targets.json
```

## Valkey availability semantics

At `internal/metrics/perses_dashboards_valkey.go:225-244`, the production status producer reads the `baseharbor/valkey` metrics signal from the reference integrations catalog. At lines 302-321 the catalog creates a dashboard entry only for `ObservabilitySupported` plus `ObservabilityVerifyBackend`; every other combination returns `Unavailable: true` and a concrete reason. The shipped backend-verification producer at lines 324-335 currently returns `ObservabilityVerifyNone`, so the present production catalog is unavailable-only. `persesValkeyDashboardCatalog()` supplies both real producers at lines 344-349. The CLI availability conversion at lines 434-450 derives its `available`/`unavailable` flag from that same catalog entry; `PersesValkeyDashboardAvailabilityResolved()` wires the real producers at lines 453-464. The serializer at lines 395-411 emits the reason document for unavailable entries and the dashboard only for the verified branch.

The exact-head tests include the production unavailable case `TestPersesValkeyDashboardAvailabilityResolvedUnavailableToday` (test file line 107), the verified gate `TestPersesValkeyDashboardAvailabilityVerifiedGated` (line 234), both isolated mutation regressions (lines 265 and 290), and the real verified dashboard regression (line 308). The candidate’s behavior matches the requested unavailable-only contract today and only promotes a dashboard/availability flag when the status and backend verification predicate both prove it.

## Commit identity review

GitHub’s commit API reports these commits, in order, all with one parent each:

```text
14403c77702bc45c668aa8a232fda1b5ba97ec9a | author worker <worker@baseharbor.local> | committer Marcel Pfingstgräf <22537373+mcpdev80@users.noreply.github.com>
349372d7e07e839237eb5936c495527f834b7358 | author worker <worker@baseharbor.local> | committer Marcel Pfingstgräf <22537373+mcpdev80@users.noreply.github.com>
a11c44d7f87510a02893c27d93eb0a0eff4c856b | author 0428-183-realpos <0428-183@baseharbor.local> | committer Marcel Pfingstgräf <22537373+mcpdev80@users.noreply.github.com>
ecff7e2f575fb991fbe5c3c1c5f6785569d70228 | author 0428-183-realpos <0428-183-realpos@users.noreply.github.com> | committer Marcel Pfingstgräf <22537373+mcpdev80@users.noreply.github.com>
```

There are two author identities (`worker` and `0428-183-realpos`) and one committer identity. The four listed commits are linear; no hop merge commit is present. A hop merge commit itself would add no authors, but it also would not erase the two author identities already in this candidate. The previous `handoff-owner-hop.md` explicitly says the Owner’s hop candidate was taken while the identity rewrite was expected; this exact live history shows that correction was not delivered.

## Exact-head hosted run

Run `44940738791` is `pull_request`, `completed/success`, and its head SHA is exactly `ecff7e2f575fb991fbe5c3c1c5f6785569d70228`; it completed at `2026-11-21T19:29:37Z`. This corrects the queue note’s description of the run as old: the current branch and PR refs still point to this exact SHA. `PR Selected Checks`, job `136958552540`, completed successfully. `PR · Go unit · packages`, job `136957182124`, completed successfully; the run also passed `PR · Trusted Plan`, focused Python, go-vet, go-build, Go unit shards cli-0/1/2/3 and owner, source format, and native gate plan. The run had 14 successful jobs and 21 skipped jobs, with no failures; skipped jobs are not treated as passes.

The candidate is now behind the live develop ref, but this review did not change `.github/workflows/ci.yml`, the planner, or `scripts/test_pr_*` / `scripts/test_ci_*`, and the task did not require a current-base refresh. The exact-head successful run therefore remains the relevant hosted evidence for this unchanged candidate. No new run was triggered.

## Predecessors

The earlier `review-1-head1ecff7e2.md` and `handoff-owner-hop.md` remain on Planning `origin/main` and were not modified. The task note still records the card in `wait` pending the independent review findings; this review does not change task state.

## Verdict and finding

REQUEST CHANGES — author identity only, for card 0428-224. The exact candidate still carries the `worker` author alongside `0428-183-realpos`. Remedy: rewrite the four-commit range to one authorized author identity while preserving the tree, then provide the exact new head and its terminal required checks for re-review.

The requested Valkey semantics are satisfied: production remains explicitly unavailable today, and the availability/dashboard promotion predicate requires both supported status and backend verification. The exact-head hosted aggregate and package job passed. No separate functional finding is raised in this verdict.

## repo-rule compliance

Reviewer-only. No product files, workflows, scripts, PR comments, pushes, or merge actions were made. No local suite tests were run. Evidence is confined to the Planning worktree. The fetched comparison in `/tmp/planreview-rev1714-head` was removed after it proved unsuitable for ancestry measurement; remote state conclusions above rely on GitHub API/`ls-remote` witnesses, not that scratch fetch.

## cleanliness

`docker ps -a` before review: PID 3222309; eight listed `bh-itest-*` containers were already exited. `docker ps -a` after review: PID 3260182; the same eight containers were exited. This review started or changed no containers or compose projects.

END codex-rev-1747 DONE — REQUEST CHANGES for the two-author identity at candidate `ecff7e2f575fb991fbe5c3c1c5f6785569d70228`; exact-head run `44940738791` completed successfully.

## Publication witness

Pending publication of this evidence to verified Planning `origin/main`.
