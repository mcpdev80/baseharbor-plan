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

Product `git remote -v` resolved `lane-origin`, `origin`, and `upstream` to `https://github.com/mcpdev80/baseharbor.git`. Planning `git remote -v` before the evidence commit returned:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

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

Planning validation initially reported one schema error in the concurrently edited follow-up card. At final validation, `python3 scripts/plan.py check` completed with 0 errors and 11 warnings after the card-note issue was resolved concurrently; this review did not edit or stage that task note. The review evidence itself contains no Markdown checkbox lines.

## cleanliness

- Before: `docker ps -a --no-trunc`, shell PID 3178799; header only, no containers.
- After: `docker ps -a --no-trunc`, shell PID 3198042; header only, no containers.
- No Docker/Podman compose project was started. Product change was the authorized normal squash merge; no PR head or candidate branch was pushed or rewritten.

## ROLLE: MERGE

The exact-head review record was published to Planning origin/main before merge (review record commit `935196e281b8c6968bdb3b040d99e7802a715b9c`). Immediately before merge, the PR still had head `2be1136606d5c881badf317bd001f0024da1ea46`, base/current develop `15c652136b0fce19dd0ae286b341b38cac3f7854`, `PR Selected Checks` success from integration 15368, and the only red check was the known advisory job 137430774780. The branch-rules API required only `PR Selected Checks` (strict up-to-date); no bypass or override was used. Although GitHub reported mergeStateStatus `UNSTABLE` due to the known advisory, its required aggregate was green and the normal squash merge API accepted the merge.

`gh pr merge 1789 --repo mcpdev80/baseharbor --squash` completed normally. GitHub now reports PR #1789 closed/merged at `2026-11-23T01:41:46Z`, merge commit `e8acf740553f7218b259f4855f5b79f83f21ab6b`. The merge commit has parent `15c652136b0fce19dd0ae286b341b38cac3f7854`, the exact base SHA. Post-merge `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1789/head` returned:

```text
e8acf740553f7218b259f4855f5b79f83f21ab6b	refs/heads/develop
2be1136606d5c881badf317bd001f0024da1ea46	refs/pull/1789/head
```

The merge-triggered develop runs were observed to terminal success on the exact merge SHA:

- Runtime · Docker Core · develop: run 45096006175, `completed/success`, event `push`, head `e8acf740553f7218b259f4855f5b79f83f21ab6b`.
- Runtime · Podman Core · develop: run 45096006283, `completed/success`, event `push`, head `e8acf740553f7218b259f4855f5b79f83f21ab6b`.

No force push or protection bypass was used. Card relevance: #1789 fulfills the 0428-076 PromQL follow-up; the independent advisory deletion-classification repair remains separately tracked by 0428-253.

## Final verdict

CODEX-REVIEW: APPROVE exact head `2be1136606d5c881badf317bd001f0024da1ea46`.
CODEX-MERGE: MERGED normally by squash as `e8acf740553f7218b259f4855f5b79f83f21ab6b`; develop witness confirmed; post-merge Docker and Podman develop runs completed successfully. The advisory Candidate-added check remains non-blocking and is assigned to 0428-253.

END_DONE codex-rev-1747: #1789 reviewed and squash-merged; merge SHA e8acf740553f7218b259f4855f5b79f83f21ab6b; exact-head required run 45094339280 green, post-merge Docker/Podman runs 45096006175 and 45096006283 successful.

## origin/main evidence-path witness

Exact output of `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep 'evidence/r28-welle5-2026-11-22/promql-0428-076/review-merge-1789-2be1136.md'` after fetching origin/main:

```text
evidence/r28-welle5-2026-11-22/promql-0428-076/review-merge-1789-2be1136.md
```


## PLAN — #1789 re-review
- 287. Read PR #1789 review/merge contract and create the numbered plan in the live board and Planning evidence.
- 288. Verify GitHub remote, live PR/develop refs, ancestry, merge state, scoped diff, and candidate immutability.
- 289. Confirm catalog delta is exactly six PromQL removals and inherited ingress rows remain unchanged.
- 290. Verify exact-head run 45094339280 required checks and classify advisory Candidate-added failure.
- 291. Compare content since approved head 146ccf6, inspect hops/dedup/comment heals for regression.
- 292. Merge normally only if all review gates pass; otherwise record a file/change/test/stop remedy.
- 293. Verify merge SHA/develop refs and any merge-triggered runs; record cleanliness.
- 294. Validate and publish Planning evidence, update board, and post END.


## ROLLE: REVIEW — post-merge re-audit

Session: codex-rev-1747 (Codex / GPT-6-Luna); backend identifier is not exposed; review time: 2026-11-23 02:42 UTC.
Scope: `t-20261123-promql-ci-capture-followup` (0428-255), the #1789 follow-up arising from card 0428-076. This section records the current mission's independent re-audit and supersedes the earlier APPROVE as the review verdict; it does not rewrite the historical merge event.

### Remote candidate and merge state

The product remote names resolved to `https://github.com/mcpdev80/baseharbor.git`. The live `git ls-remote` result is:

```text
e8acf740553f7218b259f4855f5b79f83f21ab6b	refs/heads/develop
2be1136606d5c881badf317bd001f0024da1ea46	refs/pull/1789/head
```

GitHub reports PR #1789 closed/merged at `2026-11-23T01:41:46Z`, exact head `2be1136606d5c881badf317bd001f0024da1ea46`, and merge commit `e8acf740553f7218b259f4855f5b79f83f21ab6b`. The squash merge commit has parent `15c652136b0fce19dd0ae286b341b38cac3f7854`, the PR's recorded develop base. GitHub compare `15c652...2be113...` reports merge base `15c652...`, ahead 9, behind 0. The PR head remains unchanged after merge. No merge was attempted in this re-audit because the PR was already merged.

GitHub's exact PR file list and patches establish the equivalent of `git diff origin/develop...HEAD --name-only` at the recorded base `15c652...`:

```text
internal/metrics/perses_dashboards_promql_test.go
internal/metrics/perses_dashboards_test.go
scripts/pr-gate-coverage.json
scripts/test_pr_native_gate_plan.py
```

There is no `.github/**`, `go.mod`, or `go.sum` change. The deleted parser test and its catalog/plan references are removals; the remaining test-file change contains comments only. No production implementation file changed.

### Catalog and inherited ingress

I fetched and parsed `scripts/pr-gate-coverage.json` at the exact base and candidate through GitHub Contents API. Base: 220 component rows, 220 unique paths. Candidate: 219 rows, 219 unique paths. The path delta is one removal, `internal/metrics/perses_dashboards_promql_test.go`; additions: zero; modified rows: zero. The removed JSON component record is exactly the six-line PromQL catalog entry.

At both refs, `internal/operatorauth/local_runtime.go` and `internal/operatorauth/local_runtime_test.go` each retain Docker and Podman `data.capabilities` surfaces (four registrations total). `cmd/baha/app_access.go` and `cmd/baha/app_access_test.go` each retain those same two surfaces (two rows). No inherited ingress registration changed.

### Exact-head CI and known advisory

Run `45094339280` is completed/success for exact head `2be1136606d5c881badf317bd001f0024da1ea46`, event `pull_request`. `PR Selected Checks` job `137433654865`, `PR · Trusted Plan` job `137430693974`, `PR · Native gate plan` job `137430694168`, and selected native Docker/Podman observability jobs `137431464133` / `137431464039` are successful. The Go packages and required validation jobs are successful. Skipped unrelated release and targeted jobs are not counted as passes.

The sole red result is `PR · Candidate-added checks (advisory)`, job `137430774780`. Its failing line is:

```text
ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/metrics/perses_dashboards_promql_test.go (id source.internal_metrics_perses_dashboards_promql_test_go)
```

This is the documented deleted-source planner behavior assigned to 0428-253, and is advisory under the coordinator disposition. It does not change the required-check result. Merge-triggered develop runs `45096006175` (Docker Core) and `45096006283` (Podman Core) both completed/success on exact merge SHA `e8acf740553f7218b259f4855f5b79f83f21ab6b`.

### Finding and verdict

Finding F1, comment-heal acceptance not met: at `internal/metrics/perses_dashboards_test.go:320-326`, the negative-witness comment correctly says the default heuristic rejects both shapes, but line 325 then says the *removed* build-tagged real parser witness “stands in for the same two shapes.” That test file was deleted, so this sentence leaves a misleading/contradictory description in the surviving test source. The preceding comment at lines 262-267 accurately says the tagged witness is gone and Route b's heuristic covers these shapes; the function comment should likewise name the surviving heuristic as the witness.

Repair recipe: in `internal/metrics/perses_dashboards_test.go`, replace the final sentence of the comment above `TestPersesInvalidTrailingMatcherIsRejected` with a statement that the default-build heuristic is the surviving witness and the tagged real-parser test was removed because `promqlparser` was never wired into `go.mod`. Keep executable behavior unchanged. If a correction is made, verify `TestPersesInvalidTrailingMatcherIsRejected` remains exercised by the existing Go packages shard and require its exact-head CI run; stop if that route no longer selects it. This is a post-merge finding: GitHub had already merged the candidate before this re-audit, so I made no product-repository edit and did not attempt to alter or revert the merge.

VERDICT: REQUEST CHANGES for exact head `2be1136606d5c881badf317bd001f0024da1ea46` because the surviving comment does not fully heal the deleted-test reference. The earlier APPROVE and normal squash merge remain historical facts, but this re-audit does not affirm that the comment criterion passed.

## cleanliness

- Before re-audit: `docker ps -a --no-trunc`, shell PID 3354138; header only, no containers.
- After re-audit: `docker ps -a --no-trunc`, shell PID 3356665; header only, no containers. No Docker or Podman command started a container or compose project.

END_BLOCKED codex-rev-1747: post-merge re-audit found stale deleted-witness wording at `internal/metrics/perses_dashboards_test.go:325`; PR was already merged as `e8acf740553f7218b259f4855f5b79f83f21ab6b`.

## origin/main evidence-path witness

Exact output of evidence/r28-welle5-2026-11-22/promql-0428-076/review-merge-1789-2be1136.md before publishing this re-audit:

```text
evidence/r28-welle5-2026-11-22/promql-0428-076/review-merge-1789-2be1136.md
```
