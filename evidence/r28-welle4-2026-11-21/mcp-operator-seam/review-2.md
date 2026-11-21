ROLLE: REVIEW

Verdikt: REQUEST CHANGES

Review metadata: session ID not exposed by this interface; model GPT-6; backend Codex API; review time 2026-11-21 08:15 UTC.

## PLAN

1. Read the mission and establish the exact PR, base, candidate SHA, remote refs, and ancestry.
2. Read the card contract, candidate evidence, and prior review; inspect only the candidate write-set and exact test path.
3. Verify success and anonymous denial assertions, exact error message, missing principal, and both mutation directions.
4. Inspect exact-head required CI job logs, compare failure cases with same-base runs, and classify skipped checks.
5. Verify no protected paths changed and record host cleanliness before/after.
6. Write the literal verdict and actionable recipes; publish only this review file and verify published evidence and frozen PR SHA.

## Candidate and freeze

- PR: mcpdev80/baseharbor #1741, card t-20261121-mcp-operator-seam-uncovered (0428-218).
- PR head before review: fb5a5deaf36ba160b527019a3ef4eea85060905d.
- PR base: lane-0428-198-cli-shard-operator-env at e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4.
- GitHub PR API: open, draft=false, updated_at 2026-11-21T07:54:50Z; head and base match the values above.
- Product remote: `origin git@github.com:mcpdev80/baseharbor.git` for fetch and push, resolved by `git -C workers/baseharbor remote -v`; all product ref truth below is from the GitHub HTTPS remote.
- Exact remote refs:
  `fb5a5deaf36ba160b527019a3ef4eea85060905d refs/heads/lane-0428-218-mcp-operator-seam`
  `fb5a5deaf36ba160b527019a3ef4eea85060905d refs/pull/1741/head`
- GitHub compare e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4...fb5a5deaf36ba160b527019a3ef4eea85060905d: `ahead_by=2`, `behind_by=0`, `merge_base=e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4`, status `ahead`. Both candidate commits are card-related; the two-commit diff is based directly on the listed base.
- PR head after review: fb5a5deaf36ba160b527019a3ef4eea85060905d.
- PR head before/after review = fb5a5deaf36ba160b527019a3ef4eea85060905d/fb5a5deaf36ba160b527019a3ef4eea85060905d.
- Read-only review. No product files changed.

## Contract and diff

The card requires the anonymous `prod` MCP mutation to reach the production operator-auth refusal, pin its verbatim message, and remain opposite the stamped operator success. The exact current source in `internal/operatorauth/authorization.go:285` is `Managed-environment machine operations require an authenticated BaseHarbor operator.`; `cmd/baha/mcp.go` maps that reason into the MCP machine error. The period is part of the current production string and is asserted by the candidate.

GitHub compare reports exactly one changed path: `cmd/baha/mcp_operator_seam_test.go`. No product implementation, `.github/**`, `scripts/**`, `internal/operatorauth/**`, `internal/identityprovider/**`, or `internal/serviceaccess/**` file changed. This is within the review write-set.

The candidate test `TestMCPOperatorSeamReachesGateBothDirections` creates a `prod` workspace fixture, changes into its manifest directory, and calls `baseharbor.target.create` via the in-memory MCP client/session `CallTool` in both contexts. The stamped context must succeed. The anonymous, fixture-opted-out context must return an MCP error with `authentication_failed`; the test decodes `error.message` and checks exact equality with the source string above. It also checks that the anonymous context has no verified `PrincipalFromContext`, the stamped output is not authentication-failed, and the two outputs differ. This is a real handler/transport test, not a direct helper assertion.

## Acceptance review

1. Reachability and both outcomes: PASS. The same managed `target.create` call travels through `CallTool` for stamped and anonymous contexts. The `prod` fixture selects the managed-environment path. The stamped operation must succeed; the anonymous operation must return a structured error.
2. Exact message and principal state: PASS. The decoded `Error.Message` equality matches the production source, including its terminal period. `Error.Code == authentication_failed` and the absence of an operator principal are retained. This closes review-1 Finding 1.
3. Mutations: PASS by test sensitivity, with one demonstrated run. Round-2 lane evidence records a governed mutant where the product denial text was changed: the exact message assertion fails in this test; restoring the source returns it to green. The anonymous gate-diversion condition is independently guarded in the committed test logic: if the anonymous request no longer receives the gate denial, the `IsError`, typed-code, and exact-message assertions fail. The lane evidence does not record a separate executed gate-diversion mutant; I did not mutate or run local tests in this read-only review.
4. CI routing: PASS. Exact-head job `PR · Go unit · cli-3`, job `136780430782`, completed success and executes this test. The run also reports `PR · Trusted Plan` and `PR · Native gate plan` success. The test path is covered by the Go unit shard selection.
5. Required checks: FAIL. Exact-head run 44882418434 completed with conclusion `failure`; terminal `PR Selected Checks` job 136781570119 is failure. cli-0 job 136780430791 and packages job 136780430748 are failure. The six Go unit cells did execute; cli-1, cli-2, cli-3, and owner succeeded. There are 20 skipped path-filtered cells; this test-only Go diff does not select the unrelated native runtime/release cells. Skipped is not counted as success.

## Hosted CI evidence and byte counts

Exact candidate run 44882418434 is a completed pull_request run on fb5a5deaf36ba160b527019a3ef4eea85060905d (started 2026-11-21T07:54:55Z, terminal at 08:00:25Z).

The three requested exact-head retrieval byte counts are:

- `gh run view 44882418434 --repo mcpdev80/baseharbor --log`: 894134 stdout bytes.
- `gh run view 44882418434 --repo mcpdev80/baseharbor --log-failed`: 35949 stdout bytes.
- Per-job `gh run view --job <id> --log`: cli-0 job 136780430791 = 45764 bytes; packages job 136780430748 = 66915 bytes; cli-3 job 136780430782 = 44206 bytes. Per-job logs, not the aggregate transcript, are used for the failure counts below.

First-level failing test names from the individual candidate jobs:

- cli-0: one distinct test, `TestAppListAllTargetsWorksAfterInstallationDestroy`; log says the inventory depended on deleted Target config `docker-dev` and configured `config.yaml` is missing.
- packages: three distinct tests: `TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource` (`loki_test.go:522`, missing `providers/loki/shared/service-access/pki/client-cert.pem`), `TestPersesLokiDatasourceMultiSourcePartialMatchability` (`loki_test.go:586`, same missing file), and `TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed` (`loki_test.go:633`, expected 2 per-source queries but got 0).

Same-base comparison is run 44867737078 on the exact base SHA e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4. Its individual job-log retrievals were available through the GitHub Actions job-log API after `gh run view --job ... --log` returned zero bytes for those old jobs. Baseline cli-0 job 136735244280 contained the same one distinct first-level failing test name; baseline packages job 136735244287 contained the same three distinct test names and corresponding failure lines. API job-log byte counts were 23040 bytes for baseline cli-0 and 34610 bytes for baseline packages; candidate API job logs were 23040 and 34611 bytes respectively. These are inherited failures (cli-0: 0428-210 / #1739; packages: owner stack #1615), not introduced by this one-file test diff. This classification does not change the failed aggregate state.

## Finding and recipe

Finding 1 — required exact-head aggregate remains failed due to same-base inherited failures.

- State: `PR Selected Checks` run 44882418434 is failure. The failed jobs and first-level test names are listed above and reproduce on same-base run 44867737078. The candidate's own cli-3 test job is successful, but that does not make the aggregate green.
- File/change: no change is indicated in this card's allowed test-only write-set. Resolve `TestAppListAllTargetsWorksAfterInstallationDestroy` in the 0428-210/#1739 owner path and the three Perses multi-source fixture failures in the #1615 owner stack. If the base or required-plan must change to unblock this chain, that is a coordinator action outside this card's write-set; do not edit those files here.
- Test requirement: run a new exact-head hosted PR check after the upstream failures are resolved. Require cli-3 to execute `TestMCPOperatorSeamReachesGateBothDirections`, require the previously failing cli-0/packages jobs to execute and succeed, and require terminal `PR Selected Checks` success.
- Stop criterion: keep this verdict at REQUEST CHANGES while the exact-head required aggregate is failed, skipped, or queued. Re-review only after a newer frozen candidate has a terminal successful aggregate and the test job is executed.

No code-level finding remains against the submitted test change. The only blocker in this review is the failed required aggregate; do not relabel inherited failures as candidate success.

## Cleanliness

- Before review: PID 4108221; `docker ps -a` returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`), with no containers.
- After review: PID 3995017; `docker ps -a` returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`), with no containers. No containers or compose projects were started by this review.

## Review limits

No local tests were run. No workflow was edited or dispatched. No PR comment, merge, force-push, or close action was taken. Session ID is not exposed by this interface.

END REVIEW DONE — candidate SHA fb5a5deaf36ba160b527019a3ef4eea85060905d.
