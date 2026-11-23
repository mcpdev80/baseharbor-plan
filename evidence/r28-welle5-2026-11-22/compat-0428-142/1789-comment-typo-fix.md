# 0428-076 / #1789 comment-typo-fix: clean English in promqlparser-witness comments

lane: w21-pr1702-0428-142-compat
session: 0847d100
card: 0428-076 / PR #1789 — drop dead promqlparser-tagged perses witness from default build
candidate head: 146ccf6fd67c285a33dbc06a7d061806228550ce (typo-fix commit on top of hop 2 ba09ce33)
base develop SHA: c6a7138ce2bf7de88f45f2a68e5168c835601a16 (#1790 ingress; catalog now carries local_runtime rows)
PR #1789: https://github.com/mcpdev80/baseharbor/pull/1789 (open / READY, base develop)
hosted CI run: 45089780959 (head 146ccf6f) — FULL required plan, SUCCESS
status: END_DONE (typo round complete; advisory candidate-added red, non-blocking)

## PLAN

1. Read mission m_0847_1789typo.md.g (owner typo round): my two reworded comments at internal/metrics/perses_dashboards_test.go:265 and :323 contain "getaggregated" (German-English kauderwelsch). Reword both to clean English. No other line touched.
2. git diff == exactly the two comment blocks; go vet ./internal/metrics/ local.
3. One commit push (head changes, run 45088996723 becomes obsolete — stop polling). ls-remote witness. EXACT full hosted CI to terminal (required green expected; advisory candidate-added may stay red per card 0428-253 — document, do not fix).
4. PR stays READY, no merge. akte evidence/r28-welle5-2026-11-22/compat-0428-142/1789-comment-typo-fix.md.

## BEFUND — what I did

The owner (mission m_0847_1789typo.md.g) found that my two reworded comments in internal/metrics/perses_dashboards_test.go still contained "getaggregated" (a German-English kauderwelsch). The maintained prose in this repo is English. I corrected both to clean English:

- Line 265 (assertValidPromQL comment): "The removed build-tagged real Prometheus parser witness (the promqlparser tag was never wired into go.mod) is gone; Route b covers r1/r2 here with the default-build assertValidPromQL heuristic instead."
- Line 325 (TestPersesInvalidTrailingMatcherIsRejected comment): "The removed build-tagged real Prometheus parser witness (the promqlparser tag was never wired into go.mod) stands in for the same two shapes."

Only these two comment blocks changed; no code, no file restore, no second file. Write-set stays *_test.go.

## git diff (only the two comment blocks)

diff --git a/internal/metrics/perses_dashboards_test.go b/internal/metrics/perses_dashboards_test.go
-// r2 missing-brace findings). The getaggregated Prometheus PromQL parser witness
-// (perses_dashboards_promql_test.go, build-tagged `promqlparser`) was removed:
-// the `promqlparser` tag was never in go.mod, so Route b covers r1/r2 here with
-// the default-build assertValidPromQL heuristic instead.
+// r2 missing-brace findings). The removed build-tagged real Prometheus parser
+// witness (the promqlparser tag was never wired into go.mod) is gone; Route b
+// covers r1/r2 here with the default-build assertValidPromQL heuristic instead.
-// getaggregated Prometheus PromQL parser witness (perses_dashboards_promql_test.go,
-// build-tagged `promqlparser`) was removed: the tag was never in go.mod, so this
-// default-build witness stands in for the same two shapes.
+// removed build-tagged real Prometheus parser witness (the promqlparser tag was
+// never wired into go.mod) stands in for the same two shapes.

git diff --name-only == internal/metrics/perses_dashboards_test.go (one file only).
No "getaggregated" remains (grep == none).

## LOCAL CHECKS

- go vet ./internal/metrics/ : clean
- go build ./internal/metrics/ : ok
- gofmt -l internal/metrics/perses_dashboards_test.go : clean (empty output)
- go test ./internal/metrics/ (default build) : ok (run locally via the sanctioned named form; the default build has no promqlparser tag)

## HOSTED CI — run 45089780959 (head 146ccf6f)

REQUIRED BASE-PLAN GATES — all success:
- PR · Trusted Plan -> success (base c6a7138ce now carries the #1753 local_runtime.go + local_runtime_test.go rows, so TP passes on #1789)
- PR · Go unit · cli-0 / cli-1 / cli-2 / cli-3 / owner / packages -> success (this PR's required coverage)
- PR · Validation · go-build -> success
- PR · Validation · go-vet -> success
- PR · Validation · ci-policy / ci-executor-tests / receipt-execution-tests -> success
- PR · Native gate plan -> success
- PR · Source format -> success
- PR · Focused Python -> success
- PR · Exact Candidate -> success
- PR · Runner Interface -> success
- PR · Workflow policy -> success
- PR · Demo Pin -> success

ADVISORY JOB (non-blocking):
- PR · Candidate-added checks (advisory) -> FAILURE. Per CI policy (Owner directive 2026-11-19) this is advisory only: it reports but cannot block this PR; it binds later PRs only after merge. It flags the deleted internal/metrics/perses_dashboards_promql_test.go as uncataloged source (the base catalog guardian sees the removal but the advisory planner re-scans the diff). Mission instruction (card 0428-253): advisory red may stay red per card — document, do not fix. The deletion IS correct: the file's catalog entry was removed by this PR and the file itself no longer exists.

## END lane

END_DONE (typo round complete) — PR #1789 / card 0428-076. Both stale/getaggregated comments in internal/metrics/perses_dashboards_test.go reworded to clean English (no code, no file restore, write-set stays *_test.go). New head 146ccf6f, pushed to codex/0428-076-promql-ci-capture. PR stays READY (draft=false). Hosted CI run 45089780959 (full required plan) SUCCESS: all required base-plan gates green including PR · Trusted Plan and PR · Go unit (cli-0..3, owner, packages). Advisory PR · Candidate-added checks red (non-blocking, documented per card 0428-253). No merge. akte published to baseharbor-plan origin/main.

## cleanliness

- Hop worktrees: /tmp/opencode/1789-final-hop-wt (hop 1), /tmp/opencode/1789-hop2-wt (hop 2 + typo-fix). Both outside ecosystem root; removed at END.
- No content edit to local_runtime.go, no .github touch, no go.mod change. Write-set stays *_test.go (perses_dashboards_test.go only).
- No docker/podman compose projects started (git/gh read-only verification of hosted CI; no containers on the coordinator host).
- git ps -a witness: none started (no docker/podman daemon contact).
- Temporary CI log files fetched via gh api to /tmp/opencode (outside ecosystem root).
