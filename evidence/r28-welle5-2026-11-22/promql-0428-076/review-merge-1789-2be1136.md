# ROLLE: REVIEW — PR #1789

Session: codex-rev-1747 (Codex / GPT-6-Luna); backend: Codeman-managed Codex runtime (inference backend identifier not exposed); review time: 2026-11-23 01:39 UTC.
Task: 0428-076, follow-up `t-20261123-promql-ci-capture-followup`.
Candidate: `2be1136606d5c881badf317bd001f0024da1ea46`; base/develop `15c652136b0fce19dd0ae286b341b38cac3f7854`.

## PLAN

1. Read the #1789 review/merge contract and create this numbered plan and the live board plan.
2. Verify GitHub remotes, exact PR head/base/current develop, ancestry, diff and merge state.
3. Check catalog delta and required inherited ingress rows.
4. Verify exact-head CI and classify the advisory Candidate-added failure.
5. Compare content to approved head 146ccf6 and inspect the lineage for regressions.
6. Record an exact-head review decision; merge normally only if all gates pass and GitHub allows it without bypass.
7. Validate and publish evidence, verify merge/develop refs, update the board and post END.

## Scope and live refs

Product `git remote -v` resolved `lane-origin`, `origin`, and `upstream` to `https://github.com/mcpdev80/baseharbor.git`. Planning remote, verified before this evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push.

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1789/head` at review start:

```text
15c652136b0fce19dd0ae286b341b38cac3f7854	refs/heads/develop
2be1136606d5c881badf317bd001f0024da1ea46	refs/pull/1789/head
```

GitHub PR API reports #1789 open, ready (not draft), base `develop` at the exact current develop SHA `15c652136b0fce19dd0ae286b341b38cac3f7854`, head `2be1136606d5c881badf317bd001f0024da1ea46`, mergeable true, not merged. Compare `15c652... ... 2be113...` reports ahead by 9 and behind by 0, confirming the base is contained in the candidate.

PR API lists exactly four changed paths: deleted `internal/metrics/perses_dashboards_promql_test.go`; modified `internal/metrics/perses_dashboards_test.go`; modified `scripts/pr-gate-coverage.json`; modified `scripts/test_pr_native_gate_plan.py`. There is no `.github/**`, `go.mod`, or `go.sum` change. The Go test-file hunk heals comments only; no product implementation logic changed.

## Catalog and ingress comparison

Catalog JSON fetched at exact base and candidate has release `v0.4.27` at both refs. Base has 220 component rows; candidate has 219. Component comparison:

- added rows: none;
- changed rows: none;
- removed row: only `internal/metrics/perses_dashboards_promql_test.go`;
- manifest patch: 0 additions, 6 deletions, exactly the obsolete PromQL component row.

Inherited ingress registrations are intact and equal at base and candidate:

- Two `internal/operatorauth/local_runtime` component rows (`local_runtime.go` and `local_runtime_test.go`) retain both Docker and Podman atomic data-capabilities surfaces: four runtime-surface registrations total.
- Two `cmd/baha/app_access` component rows (`app_access.go` and `app_access_test.go`) remain registered.
- All four rows are inherited from develop; the PR does not add, edit, or delete any of them.

## Lineage and content delta

GitHub commit ancestry confirms the chain from the last approved head `146ccf6fd67c285a33dbc06a7d061806228550ce` through comment-only correction heads `b9af4ec9b32a9418f47ec40b2a504c0c442fbb96` and `146ccf6...`, then the develop hops `469947501944603bd08aab1b3fb02a0474a5f1ec` and `2be1136606d5c881badf317bd001f0024da1ea46`. The final merge commit’s parents are `469947...` and current develop `15c652...`.

The intervening develop commits are additive base content: `b9e69b14...` is the #1765 bootstrap-target-before-selection fix and `15c652...` is the #1791 app_access catalog ingress. The current PR diff against its exact base remains the requested PromQL removal, comment heals, and test-inventory/catalog cleanup. The catalog delta is exactly the six PromQL deletions with no additions; no ingress regression or new candidate-only functional defect was found.

## Exact-head CI and advisory classification

[Run 45094339280](https://github.com/mcpdev80/baseharbor/actions/runs/45094339280) is completed/success, event `pull_request`, exact head `2be1136606d5c881badf317bd001f0024da1ea46`.

- `PR Selected Checks`: success, GitHub App integration 15368, job 137433654865.
- Selected Docker observability: success, job 137431464133.
- Selected Podman observability: success, job 137431464039.
- `PR · Trusted Plan`, `PR · Native gate plan`, `PR · Source format`, `PR · Focused Python`, `PR · Go unit · packages`, CLI shards, exact candidate, runner interface, Demo Pin, and validation jobs completed successfully.
- Release/runtime jobs shown as skipped are not represented as passes and are not required for this change.

The sole failing check is `PR · Candidate-added checks (advisory)`, job 137430774780 in the same run. The exact log line is:

```text
ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/metrics/perses_dashboards_promql_test.go (id source.internal_metrics_perses_dashboards_promql_test_go)
##[error]Process completed with exit code 1.
```

This is the known deleted-source advisory tracked by `t-20261123-planner-deleted-source-advisory` (0428-253): the candidate-added planner re-scans a removed file after the PR removes both the file and its coverage row. The coordinator disposition classifies it as advisory/non-blocking; the exact required aggregate and Trusted Plan pass. No workflow rerun, workflow dispatch, or `.github/**` change was made.

## Merge gate and review verdict

The branch-rules API reports required status `PR Selected Checks` from integration 15368 with strict up-to-date policy. That required aggregate is green on the exact head, and the PR base equals current develop. GitHub GraphQL reports `mergeStateStatus: UNSTABLE` while all required checks are green; the only failing check is the documented advisory job. This evidence does not treat the advisory as a required failure and does not authorize any bypass. I will attempt only the normal squash merge after this exact-head review record is published; if GitHub refuses the normal merge, no bypass will be used.

VERDICT: APPROVE for exact head `2be1136606d5c881badf317bd001f0024da1ea46`. The delete-only catalog change is exact, ingress rows remain intact, current-base required CI succeeded, and the advisory failure is the separately tracked 0428-253 deleted-source case.

Follow-up recipe for 0428-253: make the candidate planner classify deletion before requiring a source owner, then add a regression proving a deleted source plus removed catalog row passes the advisory while an unowned source that remains present still fails. Do not weaken Trusted Plan.

Planning check: `python3 scripts/plan.py render && python3 scripts/plan.py check` found 1 unrelated schema error in the concurrent task note `tasks/t-20261123-promql-ci-capture-followup.md`: its card line is `- [ ] Merge proof for PR #1789...` and fails the required generated-card format. That tracked file has concurrent Coordinator edits; this review did not modify or stage it. The review evidence itself contains no Markdown checkbox lines.

## cleanliness

- Before: `docker ps -a --no-trunc`, shell PID 3178799; header only, no containers.
- No Docker/Podman compose project was started.
- This review has not changed product files or PR refs; merge is pending the normal GitHub merge operation.

END REVIEW_APPROVE codex-rev-1747: exact-head #1789 review passed; normal merge pending, candidate 2be1136606d5c881badf317bd001f0024da1ea46.
