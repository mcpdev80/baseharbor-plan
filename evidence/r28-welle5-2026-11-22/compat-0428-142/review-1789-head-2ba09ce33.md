# ROLLE: REVIEW — PR #1789 re-review

Session: codex-rev-1747 (Codex / GPT-6-Luna); backend: Codeman-managed Codex runtime (inference backend identifier is not exposed); review time: 2026-11-23 UTC.

Candidate: exact PR head `146ccf6fd67c285a33dbc06a7d061806228550ce`; base SHA `c6a7138ce2bf7de88f45f2a68e5168c835601a16`.

## PLAN

1. Verify live PR/base/head and exact diff; compare candidate before and after review.
2. Confirm inherited #1790 ingress rows and no production implementation, go.mod, or workflow changes.
3. Inspect exact-head run 45089780959 required gates and advisory job failure details.
4. Recheck PromQL regression coverage and the zero-parser-use claim.
5. Record verdict, advisory classification, state discrepancy and follow-up recipe; publish evidence and post END without merging.

## Live state and candidate immutability

The product checkout remote guard (`git remote -v`) resolved `lane-origin`, `origin`, and `upstream` to `https://github.com/mcpdev80/baseharbor.git`.

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1789/head`, before and after review, returned the same values:

```text
b9e69b14a7c8c7e1ccf9176b0762bacecdecee5e	refs/heads/develop
146ccf6fd67c285a33dbc06a7d061806228550ce	refs/pull/1789/head
```

PR API: #1789 remains open, ready (`draft: false`), base ref `develop` at `c6a7138ce2bf7de88f45f2a68e5168c835601a16`, head `146ccf6fd67c285a33dbc06a7d061806228550ce`, not merged, and mergeable. Develop has advanced to `b9e69b14a7c8c7e1ccf9176b0762bacecdecee5e` since this PR’s base; this review did not hop or update the candidate.

The commit ancestry API confirms `2ba09ce33784943dceef9050fce5f4d50bb53b21` is the base-ingress hop, followed by `b9af4ec9b32a9418f47ec40b2a504c0c442fbb96`, followed by the reviewed head `146ccf6fd67c285a33dbc06a7d061806228550ce`. The latter two commits touch only comment text in `internal/metrics/perses_dashboards_test.go`; neither changes executable code.

The PR Files API lists four paths, not three: deleted `internal/metrics/perses_dashboards_promql_test.go`; modified `internal/metrics/perses_dashboards_test.go`; modified `scripts/pr-gate-coverage.json`; modified `scripts/test_pr_native_gate_plan.py`. The extra test-file path contains comment-only cleanup. There are no `go.mod`, `go.sum`, production implementation, or `.github/**` changes. The “same three files” wording in the mission omits this expected comments-only test file; no functional-scope expansion is present.

At the reviewed head, all three #1790 rows are present in `scripts/pr-gate-coverage.json` exactly as at base `c6a7138ce2bf7de88f45f2a68e5168c835601a16`; the manifest release remains `v0.4.27`. The rows cover `internal/operatorauth/local_runtime.go`, `internal/operatorauth/local_runtime_test.go`, and `cmd/baha/control_plane_single_native_ci_test.go`, each with `runtime_specific: true` and the Docker and Podman atomic data-capabilities surfaces. The PR’s catalog hunk removes only the obsolete PromQL test-path row; it does not remove any #1790 ingress row.

## Exact-head hosted run

The mission’s run number 45088996723 is not the run for this head: GitHub reports it completed/cancelled at the prior head `b9af4ec9b32a9418f47ec40b2a504c0c442fbb96`. GitHub’s later exact-head run is [45089780959](https://github.com/mcpdev80/baseharbor/actions/runs/45089780959), `completed/success`, event `pull_request`, head exactly `146ccf6fd67c285a33dbc06a7d061806228550ce`.

- `PR Selected Checks`: success from GitHub App integration 15368 (job 137419718437).
- Selected Docker observability: success (job 137417288915).
- Selected Podman observability: success (job 137417288995).
- Go unit `packages`: success (job 137416844639); CLI shards `cli-0` through `cli-3` and `owner` also succeeded.
- Trusted Plan, Native gate plan, Source format, Focused Python, Exact Candidate, Runner Interface, Demo Pin, Workflow policy, and the required validation jobs succeeded.
- Unrelated release/runtime matrix jobs that were skipped are not counted as passes.

The advisory job number in the mission, 137410039120, belongs to earlier run 45087659802 at head `2ba09ce33784943dceef9050fce5f4d50bb53b21`. At the reviewed exact head, the same check is job 137416844458 and failed. It is explicitly named `PR · Candidate-added checks (advisory)`, outside the base required plan; the exact-head required aggregate remains green.

The exact-head advisory log reports:

```text
ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/metrics/perses_dashboards_promql_test.go (id source.internal_metrics_perses_dashboards_promql_test_go)
##[error]Process completed with exit code 1.
```

Cause: this PR deletes the tagged source file and its catalog row. The candidate-added planner re-scans the deleted path as an unowned source change instead of treating a deletion as resolved by removal. Required Trusted Plan is green against the trusted base; this candidate-added check is advisory and non-blocking under the CI policy. Planning task 0428-253, `tasks/t-20261123-planner-deleted-source-advisory.md`, already tracks the follow-up. No workflow or planner change was made in this review.

## PromQL cross-check

At the exact head, `internal/metrics/perses_dashboards_promql_test.go` is absent. `go.mod` and `go.sum` contain no `github.com/prometheus/prometheus/promql/parser` import/dependency. The active default-build `assertValidPromQL` calls `checkClosedPromQLSelector`, requires the application and environment matchers, and checks dashboard variables. `TestPersesInvalidTrailingMatcherIsRejected` asserts rejection of both an unclosed selector and a trailing bare `up` token. The helper requires a closing `}` and requires every comma-separated matcher token to contain `=`. This covers the stated malformed-selector regressions with the default-build heuristic; it is not a full PromQL parser.

The exact-head Go unit `packages` job log contains one `internal/metrics` package result (`ok github.com/mcpdev80/baseharbor/internal/metrics 0.946s`) and zero `promqlparser` hits. The source comments still mention the removed build tag; there are zero active parser imports, tagged parser-test files, or parser-tag test executions.

## Verdict and actionable recipe

VERDICT: APPROVE for exact head `146ccf6fd67c285a33dbc06a7d061806228550ce`. Required exact-head checks are green, the three ingress rows remain intact, and the only post-ingress edits in the latest two commits are comments. Advisory failure is expected and non-blocking, with the deleted-source behavior already assigned to card 0428-253.

Recipe for that follow-up: make the candidate planner classify a deleted source path before requiring a coverage owner, then add a CI-executed regression where a PR deletes a source and its catalog row while preserving fail-loud behavior for an unowned path that still exists. Do not weaken Trusted Plan or change `.github/**` in this review.

No merge was performed; the mission reserves merge for a later owner-started action. The candidate ref was unchanged before and after review. This review made no product edits, workflow dispatch, rerun, or container changes.

## cleanliness

- Before: `docker ps -a --no-trunc`, shell PID 3016236; header only, no containers.
- After: `docker ps -a --no-trunc`, shell PID 3037349; header only, no containers.
- No Docker/Podman compose project was started.

Planning validation: `python3 scripts/plan.py check` completed with 0 errors and 11 warnings (existing dependency/status warnings). Evidence contains no Markdown checkbox lines.

END_DONE codex-rev-1747: REVIEW APPROVE #1789 exact head 146ccf6fd67c285a33dbc06a7d061806228550ce; required run 45089780959 green; candidate-added failure is advisory and tracked by 0428-253; no merge.

## origin/main witness

Exact output of `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep 'evidence/r28-welle5-2026-11-22/compat-0428-142/review-1789-head-2ba09ce33.md'` after fetching origin/main:

```text
evidence/r28-welle5-2026-11-22/compat-0428-142/review-1789-head-2ba09ce33.md
```
