# ROLLE: REVIEW (CODEX-REVIEW) — PR 1789 / 0428-076

## PLAN

1. Capture the exact target, scope, acceptance points, and evidence destination.
2. Verify current GitHub refs, exact PR diff, and candidate immutability.
3. Inspect the deleted tagged test, go.mod at base, and default-build selector validation.
4. Verify exact-head hosted run 45078492469, executed package list, and parser-tag hit count.
5. Compare catalog rows, record verdict and recipe, validate and publish the evidence, then post END.

## Session and review target

Session ID `fecbada9-9fd8-4df4-9305-d49b53a6e7a7`, lane `codex-rev-1747`; model `GPT-6-Luna` as reported by Codeman; backend `codex` mode (the runtime metadata does not expose a separate provider/backend identifier); review time `2026-11-22 22:53:37 UTC`.

PR #1789 is open and draft. Exact head: `2edc757079e27617f44e24fc02daf4e37db1e58a`. PR-recorded base: `b48ac03ef75165c4e50a4a29d5ef0197af3444da`. At review time, fresh remote `develop` was `cace61802dcd8b5ab449951085050474146d9276`, so the PR base is older than current develop. The exact candidate head and current develop refs were identical at the beginning and end of review; the candidate was not modified. The product remote names resolved to `https://github.com/mcpdev80/baseharbor.git`; direct URL witnesses were used.

Remote refs after review:

- `cace61802dcd8b5ab449951085050474146d9276 refs/heads/develop`
- `2edc757079e27617f44e24fc02daf4e37db1e58a refs/pull/1789/head`

The PR base is an ancestor of the exact candidate. Exact base-to-head diff (`git diff b48ac03ef75165c4e50a4a29d5ef0197af3444da...2edc757079e27617f44e24fc02daf4e37db1e58a --name-only`) is exactly:

- `internal/metrics/perses_dashboards_promql_test.go` (deleted)
- `scripts/pr-gate-coverage.json`
- `scripts/test_pr_native_gate_plan.py`

No `go.mod`, `.github/**`, or product implementation file changes. `git show --stat` identifies the exact head as a merge commit with parents `d7c109dc153822e2b50b62bfba52cda3c179f820` and the PR base `b48ac03ef75165c4e50a4a29d5ef0197af3444da`; its first-parent stat lists five `cmd/baha` files inherited from the merged develop parent. Those are not in the PR base-to-head diff above.

## Deleted test and retained default coverage

The deleted `internal/metrics/perses_dashboards_promql_test.go` begins with `//go:build promqlparser` and imports `github.com/prometheus/prometheus/promql/parser`. The PR base `go.mod` contains no `github.com/prometheus/prometheus` entry. Thus the file is excluded from the default build and its parser import is not a dependency available to that build.

Default-build selector validation remains in `internal/metrics/perses_dashboards_test.go`: dashboard queries call `assertValidPromQL` at line 216; the helper calls `checkClosedPromQLSelector` and checks the required application/environment matchers at lines 262-282. `TestPersesInvalidTrailingMatcherIsRejected` exercises missing-brace and trailing-token forms through `checkClosedPromQLSelector` at lines 319-335. This file has no build constraint, and the hosted default package job below executes it.

## Hosted run evidence

Run `45078492469` is terminal `completed / success`, event `pull_request`, and has exact head `2edc757079e27617f44e24fc02daf4e37db1e58a` ([run](https://github.com/mcpdev80/baseharbor/actions/runs/45078492469)). `PR Draft Go · packages` job `137381018090` completed successfully and logged `go test -p 1 "${owned[@]}" -count=1`, package `./internal/metrics`, and `ok github.com/mcpdev80/baseharbor/internal/metrics 1.242s`. The job log contained one `./internal/metrics` package-list hit and zero `promqlparser` hits. This proves the default package is executed without the tag. Because the PR is draft, the full selected-check/native/release jobs shown as skipped are not claimed as passes; this review does not approve a merge.

## Catalog scope

The exact PR diff removes only the six-line `source.internal.metrics.perses.dashboards.promql.test.go` entry from `scripts/pr-gate-coverage.json` and the corresponding one path from `scripts/test_pr_native_gate_plan.py`. Comparing the internal/metrics source IDs at current develop with the exact PR head showed the sole removed ID is that PromQL-tagged test. The dashboard, helper, default test, `0428-076` native test, and testdata rows remain; no unrelated rows from #1771 or #1784-86 were removed.

## Verdict

APPROVE for exact candidate `2edc757079e27617f44e24fc02daf4e37db1e58a`. The deleted parser witness is build-tagged and its dependency is absent from the PR base `go.mod`; default selector and malformed-shape checks remain package-discovered and were executed in the exact-head hosted package job. The exact PR diff is limited to the three contracted files.

## Solution recipe

No blocking edit is required. Keep the default selector validation and malformed-shape regression in `internal/metrics/perses_dashboards_test.go`; retain normal default-package discovery through `PR Draft Go · packages` on the `pull_request` trigger. Do not add `go.mod` dependencies or restore a tagged parser shard for this cleanup. Stop approval if the default selector checks are removed, the `internal/metrics` package is skipped by the reachable CI job, or the exact PR diff adds files outside the three-file contract. The draft run's skipped full-matrix checks remain unverified and are not merge evidence.

## Repo-rule compliance

Read-only independent review. No product edits, candidate push, local product tests, GitHub review/comment, merge, close, workflow rerun, or subagent action. PR #1789 remains draft.

## cleanliness

Before review, `docker ps -a --no-trunc` with shell PID 2659316 showed only the header and no containers. After review, the same command with shell PID 2662599 also showed only the header and no containers. No container or compose project was started.

## END_DONE

END_DONE: APPROVE for exact head `2edc757079e27617f44e24fc02daf4e37db1e58a`; PR #1789 remains draft and no merge or GitHub review submission was made.
