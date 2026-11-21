ROLLE: REVIEW

Verdikt: REQUEST CHANGES

Review metadata: session ID not exposed by this interface; model GPT-6; backend Codex API; review time 2026-11-21 08:56 UTC.

## PLAN

1. Read the mission and record the numbered plan in the live board and this evidence file.
2. Resolve the GitHub remote and verify PR #1739 head/base, develop and PR refs, ancestry, and unchanged review freeze.
3. Read the 0428-210 contract and candidate evidence; inspect the exact test and production all-targets read/destroy paths.
4. Verify the test reaches the real inventory path and that removing only the read tolerance makes it fail.
5. Verify destroy/apply still reject missing config, inspect exact-head per-job CI logs and required/skipped states, and assess the window inheritance hop.
6. Record cleanliness, verdict, and any actionable recipe; publish only review-1.md and verify origin/main plus frozen candidate SHA.

## Candidate and freeze

- PR: mcpdev80/baseharbor #1739, card t-20261121-all-targets-config-loss (0428-210).
- PR head before review: 6442955f4cf06e09583634eb90410d5fedf83b85.
- PR base: `develop`; the PR API base snapshot is 7fbb2d2c6c6410ca5f23e52e0dc2362ccdb30981.
- Product remote first git action: `origin git@github.com:mcpdev80/baseharbor.git` for fetch and push, from `git -C workers/baseharbor remote -v`. Product ref truth was checked through the GitHub HTTPS URL.
- Remote refs at review start:
  `5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef refs/heads/develop` (initial read)
  `c2c94ad115ffa33e91efcd1be1fae6fc2bba7046 refs/heads/develop` (final verification)
  `6442955f4cf06e09583634eb90410d5fedf83b85 refs/pull/1739/head` (before and after review)
- PR head after review: 6442955f4cf06e09583634eb90410d5fedf83b85.
- PR head before/after review = 6442955f4cf06e09583634eb90410d5fedf83b85/6442955f4cf06e09583634eb90410d5fedf83b85.
- Initial compare `develop...6442955f4cf06e09583634eb90410d5fedf83b85`: `ahead_by=1`, `behind_by=15`, merge base `9bd76324ec6d1364f512d718cb82f1fffc9105a4`, status `diverged`. At final verification, develop had advanced again to `c2c94ad115ffa33e91efcd1be1fae6fc2bba7046` (merge of #1731, created 08:55:25Z); compare was `ahead_by=1`, `behind_by=20`, same merge base `9bd76324ec6d1364f512d718cb82f1fffc9105a4`, status `diverged`.
- PR API at final verification reports `mergeable=null`, `mergeable_state=unknown`, `draft=false`, state open. The successful run ended at 08:35:58Z, before both the 5b26be1 commit (08:42:24Z) and the c2c94ad commit. The exact-head run was green when observed, but it is not evidence against the current develop tip.
- Exact PR diff: one changed file, `cmd/baha/app_commands.go`.
- Read-only review. No product files changed.

## Contract, reachability, and regression

The card requires `TestAppListAllTargetsWorksAfterInstallationDestroy` to pass after the Target config is deleted, for the actual `baha app list --all-targets` inventory path. It must not depend on a test-only bypass. The test at `cmd/baha/app_list_all_targets_test.go:12-30` configures a Target, removes the actual `deployment.ConfigPath()` file at lines 15-20, then invokes `appListCommand().Run(..., []string{"--all-targets"}, ...)` at line 24 and checks the empty-inventory result. There is no tolerance flag or injected config switch. `testOperatorContext` provides the operator fixture; it does not create or preserve the deleted Target config.

In the candidate's `cmd/baha/app_commands.go:137-143`, only the `allTargets` branch ignores an error when `errors.Is(err, deployment.ErrConfigMissing)`; other errors return. The selected-target branch at lines 133-136 still returns any authorization/config error. The CLI unit shard script at the exact candidate uses the SHA256 test-name sharding scheme; `TestAppListAllTargetsWorksAfterInstallationDestroy` maps to cli-0. The round-1 evidence records the same test failing at `app_list_all_targets_test.go:26` when the tolerance was removed and passing with the change. I did not mutate or run tests in this read-only review.

Destruction semantics: PASS as scoped. The patch is in the read-only `app list` path and only its `--all-targets` branch tolerates `ErrConfigMissing`. The selected-target arm remains strict, and the PR diff changes no destroy/apply/retirement code. This does not resolve the separate operator-auth regression described below.

## Exact-head hosted run and per-job logs

Run 44885264462 (`CI · Source & Quality`) was pull_request, head 6442955f4cf06e09583634eb90410d5fedf83b85, completed success at 2026-11-21T08:35:58Z. The check-run result was 14 success, 20 skipped, 0 failure. `PR Selected Checks` succeeded; Trusted Plan, Native gate plan, Workflow policy, Source format, Focused Python, go-build, go-vet and all six Go unit jobs also succeeded. The skipped checks were path-filtered; this diff changes only `cmd/baha/app_commands.go`, and no required Go unit or validation job was skipped.

I retrieved each executed job using `gh run view 44885264462 --repo mcpdev80/baseharbor --job <id> --log` and recorded its stdout byte count:

| Job | Job ID | Result | Log bytes |
| --- | --- | --- | ---: |
| PR · Native gate plan | 136789067820 | success | 71456 |
| PR · Trusted Plan | 136789068018 | success | 123383 |
| Workflow policy | 136789068107 | success | 28401 |
| PR · Source format | 136789068113 | success | 90666 |
| PR · Focused Python | 136789143716 | success | 59407 |
| PR · Validation · go-vet | 136789143755 | success | 65267 |
| PR · Go unit · cli-0 | 136789143797 | success | 44090 |
| PR · Go unit · cli-1 | 136789143796 | success | 44208 |
| PR · Go unit · cli-2 | 136789143756 | success | 44205 |
| PR · Go unit · cli-3 | 136789143817 | success | 44208 |
| PR · Go unit · packages | 136789143777 | success | 65123 |
| PR · Go unit · owner | 136789143769 | success | 50651 |
| PR · Validation · go-build | 136789143800 | success | 66043 |

The cli-0 per-job log reports `PASS cli-0: 452 passed / 13 intentionally skipped / 465 discovered`. The shard script maps the named all-targets test to cli-0. The Native gate plan succeeded; no Docker/Podman or runtime gate is required for this one-file CLI diff. I did not rely on the aggregate log to identify test names or count failures.

## Window inheritance hop

With this fix merged into develop and the stacked lanes rebased onto it, the specific cli-0 inheritance at #1737/#1738/#1741 disappears: `TestAppListAllTargetsWorksAfterInstallationDestroy` passes in cli-0 at this candidate, and the fix is in `cmd/baha/app_commands.go`. That describes this one failure only; it does not claim those PRs have no other blockers.

## Findings and recipes

Finding 1 — the candidate is behind the current develop tip, so its green run is stale for the current integration point.

- Evidence: current develop was 5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef at the initial comparison and c2c94ad115ffa33e91efcd1be1fae6fc2bba7046 at final verification; candidate merge base is 9bd76324ec6d1364f512d718cb82f1fffc9105a4; compare reports 15 commits behind and `mergeable_state=behind`. The green run ended before the current develop commit was created.
- File/change: rebase or otherwise hop the single candidate onto current `develop` in `cmd/baha/app_commands.go`, resolving the conflict without discarding the current develop authorization path described in Finding 2. Keep the candidate one commit over the exact current base if that remains the card's intended stack shape.
- Test requirement: re-run the named regression and the required CLI shard on the rebased candidate; obtain a new terminal `PR Selected Checks` success at that exact head. Reconfirm the 0428-210 test executes in cli-0.
- Stop criterion: do not accept or merge while compare reports the candidate behind current develop or the exact-current-base required aggregate is absent, skipped, queued, or failed.

Finding 2 — rebase resolution drops the current #1615 operator-auth check for `--all-targets` and swallows its config-resolution failure.

- Evidence: current develop at 5b26be1ccfc5 has the all-targets branch in `cmd/baha/app_commands.go:126-136` calling `authorizeMCPOperation(ctx, "app.list", "", "dev", "", "")`. The candidate diff removes that branch and uses `authorizeCurrentMCPContext` at lines 137-143 instead. In `cmd/baha/mcp.go:372-393`, `authorizeCurrentMCPContext` resolves `effectiveTarget` and returns its error before it reaches `authorizeMCPOperation`. The candidate then ignores `ErrConfigMissing` and continues to list inventory. Consequently a missing Target config can bypass the operator-auth boundary that current develop deliberately applies to the installation-wide read. This is not a destroy/apply change, but it changes authorization semantics for the all-targets read.
- File/change: `cmd/baha/app_commands.go:126-143`. On the rebase, preserve the current develop `authorizeMCPOperation` all-targets authorization path. Do not catch an error that is returned before the operator authorization check. Since that current path handles a missing effective Target while still enforcing the managed-environment operator boundary, verify whether the card's tolerance patch is still needed; if not, coordinate superseding/closing the now-satisfied bug card rather than reverting the authorization behavior.
- Test requirement: retain the installed-then-destroyed all-targets regression and add/retain a negative anonymous-context assertion proving that the missing-config inventory is still denied with the operator-auth error; the authenticated fixture must still receive the empty inventory. Selected-target, apply, and destroy behavior must remain strict.
- Stop criterion: do not accept a candidate that returns inventory after swallowing `ErrConfigMissing` before operator authentication. Stop when current develop authorization is preserved, the authenticated regression passes, anonymous access is denied, and exact-current-base required CI is successful. If preserving current develop means this card's product change is redundant, stop for owner/coordinator card disposition rather than merging a security regression.

## Cleanliness

- Before review: PID 4191886; `docker ps -a` returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`), no containers.
- After review: PID 26097; `docker ps -a` returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`), no containers. No containers or compose projects were started by this review.

## Review limits

No local tests were run. No workflow was edited or dispatched. No PR comment, merge, force-push, or close action was taken. Session ID is not exposed by this interface.

END REVIEW DONE — candidate SHA 6442955f4cf06e09583634eb90410d5fedf83b85.

## Planning remote

Before the evidence commit, `git -C baseharbor-plan remote -v` showed `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push.
