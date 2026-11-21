ROLLE: REVIEW

Verdict: APPROVE CONTENT — merge remains gated on a final hop to the then-current `develop` and a successful exact-head required CI aggregate.

Review metadata: 2026-11-21 10:27 UTC; session ID not exposed; model GPT-6; backend Codex API.

## PLAN

1. Read the assignment and record this numbered plan in the live board and this evidence file.
2. Resolve the GitHub remote and verify current `develop`, PR #1739 head/base, exact CI run, and before/after candidate freeze.
3. Compare the exact PR diff against its measured `develop` merge-base; review only the two allowed files and task contract.
4. Verify authorization-before-tolerance ordering, destructive-path strictness, and the negative unauthenticated test.
5. Verify mutation evidence, test-to-shard execution, required per-job CI results, and skipped checks.
6. Record the verdict and final-hop merge instruction; publish only `review-2.md` and verify it on `origin/main`.

## Candidate and source witnesses

- PR: `mcpdev80/baseharbor#1739`; card `t-20261121-all-targets-config-loss` (`0428-210`); branch `0428-210-alltargets`; PR base `develop`.
- Exact PR head at review start and final remote recheck: `52866ae38f97d940a93e5e6c88b24ab3255ed838`.
- Product remote resolved by first Git command, `git remote -v` in `workers/baseharbor`: `origin git@github.com:mcpdev80/baseharbor.git` (fetch and push). All remote truth below was queried against `https://github.com/mcpdev80/baseharbor.git` or GitHub API.
- Planning repository remote, checked before the evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push).
- Direct command `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1739/head` returned:
  `4fa5293a49b7a6cd74c6513cf329dec15d08cfa9 refs/heads/develop`
  `52866ae38f97d940a93e5e6c88b24ab3255ed838 refs/pull/1739/head`
- `gh api repos/mcpdev80/baseharbor/pulls/1739 --jq '{state,draft,mergeable,mergeable_state,head:.head.sha,base:.base.sha,base_ref:.base.ref}'` returned `{"base":"72ebc9d10ec247f24853af579655fd95c387214b","base_ref":"develop","draft":false,"head":"52866ae38f97d940a93e5e6c88b24ab3255ed838","mergeable":true,"mergeable_state":"behind","state":"open"}`.
- `gh api repos/mcpdev80/baseharbor/compare/4fa5293a49b7a6cd74c6513cf329dec15d08cfa9...52866ae38f97d940a93e5e6c88b24ab3255ed838 --jq '{status,ahead_by,behind_by,total_commits,files:[.files[].filename],merge_base:.merge_base_commit.sha}'` returned `{"ahead_by":8,"behind_by":16,"files":["cmd/baha/app_commands.go","cmd/baha/app_list_all_targets_test.go"],"merge_base":"72ebc9d10ec247f24853af579655fd95c387214b","status":"diverged"}`. Thus current `develop` is not an ancestor of this candidate; the event-base run cannot serve as post-hop evidence against the current `develop` tip.
- Candidate freeze: start and final `refs/pull/1739/head` both resolved to `52866ae38f97d940a93e5e6c88b24ab3255ed838`; PR API reports the same head. This review made no product-repository changes.
- The exact changed-file list against the PR event merge-base `72ebc9d10ec247f24853af579655fd95c387214b` is `cmd/baha/app_commands.go` and `cmd/baha/app_list_all_targets_test.go`. The current-tip comparison reports the same two files.

## Finding 1 recheck: moving `develop` and exact-head CI

The old stale-run concern is resolved for the candidate SHA itself: run `44892971526` is a `pull_request` run with `head_sha=52866ae38f97d940a93e5e6c88b24ab3255ed838`, `status=completed`, and `conclusion=success`. Its PR event base snapshot is `72ebc9d10ec247f24853af579655fd95c387214b`. My fresh remote comparison shows `develop` has since advanced to `4fa5293a49b7a6cd74c6513cf329dec15d08cfa9` and the PR is now `behind` by 16 commits. This is a moving merge-window condition, not a content defect; it is not permission to merge the currently behind branch.

The current `develop` source at `cmd/baha/app_commands.go:126-136` preserves the `authorizeMCPOperation(ctx, "app.list", "", "dev", "", "")` route for `--all-targets`. The candidate retains that same authorization route at `:131-137`. The merge instruction below requires the lane to hop this single candidate once more immediately before merge and obtain the required terminal checks on the resulting exact head.

## Finding 2 recheck: authorization remains ahead of the tolerance

I read the exact candidate source through GitHub Contents API at SHA `52866ae38f97d940a93e5e6c88b24ab3255ed838`:

- `cmd/baha/app_commands.go:131-137` calls `authorizeMCPOperation` with `app.list` and managed `dev` environment for `allTargets`; the selected-target path still calls `authorizeCurrentMCPContext` and returns its error.
- The only `errors.Is(err, deployment.ErrConfigMissing)` check in this function is at `cmd/baha/app_commands.go:205`, after the authorization decision and after the inventory listing call. Only this read-only all-targets inventory error is converted to an empty inventory; other errors still return at `:209-210`.
- The exact candidate's `cmd/baha/mcp.go:295-320` attempts target resolution opportunistically when `target == ""` and ignores that optional resolution error, then reaches `ensureManagedEnvironmentOperatorBoundary`; when no authenticated operator is present it returns the gate error `Managed-environment machine operations require an authenticated BaseHarbor operator.` This confirms missing config does not short-circuit the authorization decision.
- `cmd/baha/app_list_all_targets_test.go:35-64` configures a Target, removes the actual `deployment.ConfigPath()`, invokes anonymous `app list --all-targets`, rejects nil success and rejects `deployment.ErrConfigMissing`, checks the gate text including the final period, and asserts no output was written. The authenticated regression at `:14-33` removes the same config and requires the empty all-targets inventory result.
- The gate-text assertion is `strings.EqualFold` against the complete literal, including the terminal period. The round-5 mutation record states that removing the terminal period makes the assertion fail and records the resulting text without the period. I reviewed this recorded mutation witness; I did not modify or mutate product code in this review.
- The code diff does not touch apply, destroy, retirement consent, or any other file. The selected-target authorization branch remains strict; the task contract's two-file write-set is respected.

No remaining authorization/config-loss finding.

## Card-required test and CI

The card binds `./cmd/baha/` Go unit shards through `PR Selected Checks`. Run `44892971526` is the required `pull_request` CI route and completed at `2026-11-21T10:14:40Z` with conclusion `success` on the exact source head above. I independently retrieved every executed per-job log; each result was successful. The run exposed 35 jobs total: 15 success (including the terminal aggregate) and 20 skipped, with zero failed jobs.

The exact-head native gate plan reported `unit_scope=full`, the six unit shards `cli-0`, `cli-1`, `cli-2`, `cli-3`, `packages`, and `owner`, and `runtime_required=false`, `integration_required=false`. `PR Selected Checks` completed successfully. `validate` was skipped by non-draft PR routing; it is not the selected aggregate. Runtime, HA, release, consumer, and candidate-added advisory cells were not required for this two-file CLI unit change. No required Go shard or validation job was skipped.

| Executed job | Job ID | Result | Retrieved log bytes |
| --- | ---: | --- | ---: |
| PR · Native gate plan | 136812562534 | success | 70063 |
| PR · Trusted Plan | 136812562561 | success | 122055 |
| Workflow policy | 136812562611 | success | 28393 |
| PR · Source format | 136812562630 | success | 89046 |
| PR · Focused Python | 136812608116 | success | 59405 |
| PR · Validation · go-vet | 136812608122 | success | 65257 |
| PR · Validation · go-build | 136812608134 | success | 66046 |
| PR · Validation · cli-gofmt | 136812608149 | success | 59421 |
| PR · Go unit · packages | 136812608241 | success | 65122 |
| PR · Go unit · owner | 136812608258 | success | 50653 |
| PR · Go unit · cli-1 | 136812608271 | success | 44205 |
| PR · Go unit · cli-0 | 136812608276 | success | 44099 |
| PR · Go unit · cli-2 | 136812608277 | success | 44208 |
| PR · Go unit · cli-3 | 136812608280 | success | 60952 |
| PR Selected Checks | 136813813138 | success | 103768 |

I read `scripts/pr-go-unit-shard.py` at the exact candidate SHA. It discovers the CLI tests, assigns each discovered name by SHA-256 to one of four shards, runs the selected names with `go test -json -run`, and fails closed unless every selected test has a `run` event and either `pass` or intentional `skip`. Recomputing that script's assignment gives `TestAppListAllTargetsWorksAfterInstallationDestroy => cli-0` and `TestAppListAllTargetsStillRequiresAuthorizationWithoutTargetConfig => cli-2`. The cli-0 and cli-2 job logs each report their shard `PASS`; therefore both tests are picked up by this same-PR CI route and passed on the exact candidate. I did not run local product tests in this read-only review.

## Merge instruction

The dependency `t-20261120-cli-operator-entrypoints` (`0428-204`, PR #1726) is already recorded as accepted/closed and its authorization path is present on current `develop`. In this window the order is therefore the prerequisite #1726 first (already satisfied), then #1739; dependent work must remain after #1739 in dependency order. The currently listed 0428-220 dependent card is marked superseded by 0428-204 in its task metadata and is not an additional merge step.

Before merging #1739, the lane must hop the same candidate branch `0428-210-alltargets` to the then-measured `develop` tip, verify that tip is an ancestor, reconfirm the diff remains within the two allowed files, then run and personally observe a fresh terminal `PR Selected Checks` success plus the card-required CLI shard(s) at that exact resulting head. If develop advances again before the merge, repeat the hop and exact-head gate. Keep the PR unmerged until those witnesses match the final candidate SHA. CODEX-MERGE is a separate role; this review did not merge or alter the PR.

## Cleanliness

- Before review: PID 762314; `docker ps -a` returned only `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`; no containers.
- After review: PID 846081; `docker ps -a` returned only `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`; no containers. No containers or compose projects were started by this review.

## Final remote recheck

At `2026-11-21 10:30:42 UTC`, `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1739/head` returned:

```text
4fa5293a49b7a6cd74c6513cf329dec15d08cfa9	refs/heads/develop
52866ae38f97d940a93e5e6c88b24ab3255ed838	refs/pull/1739/head
```

The accompanying PR API recheck remained `state=open`, `draft=false`, `mergeable=true`, `mergeable_state=behind`, with head `52866ae38f97d940a93e5e6c88b24ab3255ed838` and event base `72ebc9d10ec247f24853af579655fd95c387214b`.

## Repo-rule compliance

- Read-only against the product repository; no product files, workflow files, or branches were changed.
- No workflow rerun or dispatch, PR comment, merge, close, force-push, or subagent was used.
- The only publication from this review is this `review-2.md` evidence file.

## Evidence row

`evidence/r28-welle4-2026-11-21/all-targets-config-loss/review-2.md` records the SHA-specific review of PR #1739 at `52866ae38f97d940a93e5e6c88b24ab3255ed838`, run `44892971526`, and the final-hop-before-merge condition.

END REVIEW DONE — candidate SHA 52866ae38f97d940a93e5e6c88b24ab3255ed838.

## origin/main publication witness

Exact output of `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep 'evidence/r28-welle4-2026-11-21/all-targets-config-loss/review-2.md'` before this witness was appended:

```text
evidence/r28-welle4-2026-11-21/all-targets-config-loss/review-2.md
```
