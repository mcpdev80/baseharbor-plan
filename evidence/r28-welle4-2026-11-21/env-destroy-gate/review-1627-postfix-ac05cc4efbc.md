# CODEX-REVIEW — PR #1627 / card 0428-055, post-fix head

## PLAN

1. Read the updated exact-head instruction and verify PR #1627, develop, and #1736 live refs.
2. Inspect the post-fix native fixture changes and verify both workload preparation and cleanup receive the verified operator context.
3. Verify #1736 ancestry using `git merge-base --is-ancestor` on refs fetched from the resolved GitHub remote.
4. Observe run 44958801932 on the exact #1627 head through terminal `PR Selected Checks`; confirm both Docker and Podman Coreless application shards executed.
5. Issue the exact-head review verdict, state whether #1736 content is already included, and keep merge/close to the separate merge role.
6. Validate and publish only this evidence to Planning origin/main, verify the evidence path, update the board, and post END.

## Product refs and PR state

The resolved product GitHub remote is `https://github.com/mcpdev80/baseharbor.git`. Fresh `git ls-remote` output:

```text
ac05cc4efbcddf74cf46b5f80fb251f57a7a8f2d refs/heads/cli2-env-delete
42da7128e724a533349e93d3742cbd232ea48936 refs/heads/develop
ac05cc4efbcddf74cf46b5f80fb251f57a7a8f2d refs/pull/1627/head
1e2ba9d57868778d7c74ef68882f61bd1b01bb33 refs/pull/1736/head
```

PR #1627 is OPEN, non-draft, base `develop`, branch `cli2-env-delete`, head `ac05cc4efbcddf74cf46b5f80fb251f57a7a8f2d`; GitHub reports MERGEABLE with merge state BLOCKED while checks run. The current changed-path set is the environment-destroy implementation, tests, documentation indexes, and the three `scripts/**` gate/planner files. No workflow file was changed by this review.

## Post-fix native fixture

The only commit after the held candidate `62dd38f9b6d29a63789f3ae3efe6be7cb2b0aa90` is `ac05cc4efbcddf74cf46b5f80fb251f57a7a8f2d`, `test: authenticate env destroy native fixture`. Its exact diff changes only `cmd/baha/env_destroy_integration_test.go` by +2/-1:

```diff
ctx, cancel := context.WithTimeout(machineNoninteractiveContext(context.Background()), 8*time.Minute)
defer cancel()
ctx = testOperatorContext(ctx)
...
if err := destroySelectiveApplicationWithConsent(testOperatorContext(cleanupCtx)); err != nil {
```

At the exact head, `testOperatorContext` is defined in `cmd/baha/test_operator_context_test.go:18-29`. It preserves an existing principal while ensuring membership/enforcement, or creates a principal with `IssuerVerified: true` and installs it in context. `TestEnvironmentDestroyNativeLifecycle` applies this context before `ensureRepositoryDeploymentInputsForUp` at `cmd/baha/env_destroy_integration_test.go:29` and `:81`, and separately applies it to the cleanup callback at line 74. This addresses both operator-context failures named by the owner hold note.

## #1736 dependency ancestry

The shared product checkout remote was verified as `lane-origin https://github.com/mcpdev80/baseharbor.git` (fetch/push); the other configured aliases also resolved to that same GitHub URL. Fetched exact GitHub refs into review-only refs and ran:

```text
git merge-base --is-ancestor refs/review/codex-rev-1747/pr1736 refs/review/codex-rev-1747/pr1627
```

The command succeeded. The fetched refs resolved to #1736 `1e2ba9d57868778d7c74ef68882f61bd1b01bb33` and #1627 `ac05cc4efbcddf74cf46b5f80fb251f57a7a8f2d`; `git rev-list --count pr1736..pr1627` returned `25`. GitHub compare independently reports #1736 as the merge base of #1627 (status `ahead`, ahead 25, behind 0). Thus #1736's content is already contained in #1627 and needs no separate content merge. Planning may mark #1736 as superseded/contained only after #1627 meets acceptance; that state transition remains the owner's decision.

## Exact-head hosted run

Run `44958801932` is `pull_request` for the exact head `ac05cc4efbcddf74cf46b5f80fb251f57a7a8f2d`. At the final observation (2026-11-21 23:04 UTC) it remained `in_progress`, with no run update since 22:56:40 UTC. The trusted plan passed and reported “No narrow mapping: conservative checks selected,” so the broad fallback is active. Six selected Docker/Podman Coreless lifecycle shards remained `in_progress`, including both application shards; the terminal `PR Selected Checks` aggregate had not appeared. No verdict is issued while the exact-head run is nonterminal. The owner must resume review after run 44958801932 reaches terminal state; only then can success or the failing check name and log line be assessed. Runs `44957245330` and `44958293233` belong to pre-fix heads and are excluded from acceptance evidence.

## Prior prerequisite spot-check: PR #1750

At the specifically requested commit `332159321f746e4cbd8c0c72d2e6d0da0125b3cc`, GitHub reports only `cmd/baha/test_operator_context_test.go` changed; that patch adds a cleanup-time target-resolution diagnostic and does not touch the environment-destroy fixture. It did not supply verified operator context to both setup and cleanup. PR #1750's live head had already advanced to `a9de5414b47ff8988e8427974991a38528925f91`; this spot-check was not a verdict for that PR or its newer head.

## Current review status

Held pending terminal exact-head run `44958801932`; this is not an approval or a completed verdict. No merge, close, PR comment, local suite test, product edit, or workflow action was performed.

## repo-rule compliance

Reviewer-only. The GitHub Actions run is the only test execution relied on; no local suite tests or containers were started. Product content and CI routing were inspected read-only. #1714 remains REQUEST CHANGES for author identity only; #1749 remains REQUEST CHANGES pending w21's correction.

## cleanliness

Docker before this review, shell PID `670827`: the same eight listed `bh-itest-*` containers were already exited (exit codes 0, 130, or 143). Docker after the read-only review, shell PID `678577`: the same eight containers remained exited. Final Docker observation, shell PID `700289`: the same eight containers remained exited (seven exit 0; one exit 130; one exit 143—eight total, with the two nonzero codes among them). No containers or compose projects were started or changed.

END_BLOCKED codex-rev-1747: #1627 review remains held because exact-head CI run 44958801932 is still in progress; #1736 is already an ancestor and has no separate content merge; candidate `ac05cc4efbcddf74cf46b5f80fb251f57a7a8f2d`.

## Publication witness

Pending publication to Planning origin/main.

## Origin-main evidence path witness

Exact output of `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle4-2026-11-21/env-destroy-gate/review-1627-postfix-ac05cc4efbc.md`:

```text
evidence/r28-welle4-2026-11-21/env-destroy-gate/review-1627-postfix-ac05cc4efbc.md
```
