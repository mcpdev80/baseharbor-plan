# PR #1750 exact-head independent review — 17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99

## PLAN

1. Read `/var/tmp/m/rev1750b.md.g` and its tail supplement; record the exact review contract and restrictions. DONE.
2. Refresh PR #1750 head/base and terminal hosted checks; inspect exact diff and ancestry. DONE.
3. Review the test-isolation changes, the 14-test diagnosis, operator authentication and consent boundaries without local tests. DONE.
4. Record the exact-head verdict and findings; do not change product code or PR state. DONE.
5. Run Planning validation, publish only review evidence, verify its remote path, update the board and post END.

## Review target and provenance

- Role: CODEX-REVIEW, read-only. PR: [#1750](https://github.com/mcpdev80/baseharbor/pull/1750), card 0428-223 / `t-20261121-develop-full-suite-red`.
- Exact candidate: `17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99`, branch `lane-0428-223-testcontext-target`, draft=true, state=open, mergeable=true, mergeStateStatus=clean at review.
- Exact base: `develop` at `82825e95a6f6083702d0ba5401d97f356085c722`. `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1750/head` returned `82825e95a6f6083702d0ba5401d97f356085c722 refs/heads/develop` and `17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99 refs/pull/1750/head`.
- GitHub compare reports `merge_base=82825e95a6f6083702d0ba5401d97f356085c722`, `status=ahead`, `ahead_by=4`; net diff has eight files, all under `cmd/baha/*_test.go`.
- The two implementation commits are `1588ee1be726a84501f5e513972f31dfad63aa34` and `4bd779b1501db00049c353b3865bd3ba75704aef`, authored by `0428-223-testctx`. `f16cef27f4dfb45db528226e573a38bde503b6cc` and this exact head are documented additive develop hops; the final merge commit carries exact develop as a parent. No foreign candidate is present.
- Planning mission supplement reported checksum prefix `04399079808b`; it restricts this review to no local tests and says not to touch #1752 or #1753.

## Findings

1. RESOLVED for selected required checks — the initial exact-head run `44982040951` had `PR Selected Checks` skipped, but a newer pull_request run `44982566548` on the same exact SHA completed successfully. `gh pr checks 1750 --required` now reports `PR Selected Checks pass` (job `137087212830`). Its aggregate completed the selected native-acceptance, complete selected Go-shard-coverage, and normal selected-job-result checks. This establishes the selected required aggregate on this SHA; it does not establish that unrelated runtime or validate jobs executed.
2. BLOCKING — the external runtime-consent finding remains unproven on this head. The earlier Podman data-capabilities witness is run `44975262053`, job `137064042865`, terminal failure. The Planning witness records `confirm-candidate` followed by `operator authentication needs interactive setup but input is not a terminal`. The current exact run skipped `PR · Selected Runtime`, so it does not show this gate passing. The changed files are test-support only and do not add a non-interactive credential or candidate-consent path for the separate CLI process used by that gate.
3. P2 — test temporary-directory cleanup is missing. `cmd/baha/test_operator_context_test.go:112-121` says the isolation directory is discarded with the test temporary root, but `hostConfigIsolationDir` calls `os.MkdirTemp` and never registers cleanup. When the persisted host selection is present, each call leaves a `baseharbor-0428-223-cfg-*` directory in the system temp directory. Use `t.TempDir()` or register `t.Cleanup` so repeated tests on persistent hosts remain clean.
4. PASS — no test softening or security bypass was found in the diff. It adds selection isolation before tests that lack a target fixture and strips leaked target environment from the self-executed child. It adds no `t.Skip`, weakened assertions, workflow changes or production-code changes. The existing in-process `runWithIOAsTestOperator` path uses a verified test principal and keeps `operatorauth.WithEnforcementIfAbsent`; its comment says unauthenticated-denial tests use `runWithIO` directly. This is not evidence that the separate data-capabilities runtime gate passed, as finding 2 records.

## Hosted evidence

- Run `44982040951` is terminal `completed/success` at exact head `17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99`; its selected aggregate was skipped. A newer exact-head pull_request run `44982566548` is terminal `completed/success` on the same SHA.
- Passing jobs: Draft source and routing `137084441293`; Draft Go cli-0 `137084441490`; cli-1 `137084441489`; cli-2 `137084441515`; cli-3 `137084441603`; packages `137084441619`.
- Shard receipts: cli-0 `460 passed / 13 intentionally skipped / 473 discovered`; cli-1 `441 / 10 / 451`; cli-2 `457 / 20 / 477`; cli-3 `426 / 16 / 442`, each reporting CLI inventory total 1843. The exact cli-3 log also shows the separate zsh/fish wrapper regression passing; that does not substitute for the skipped required aggregate or runtime gate.
- `gh pr checks --required` currently reports `PR Selected Checks pass` via run `44982566548`, job `137087212830`. In that run, `PR · Selected Runtime` job `137086100059` and `validate` job `137086050735` are skipped; the Podman target job `137086050775` and Docker target job `137086074835` are also skipped. These are not green receipts for the separate runtime-consent concern.
- The prior develop diagnosis classifies the 14 validate failures as test-fixture/environment leaks. The current Draft Go shards pass, but this exact run skips `validate`, so the current-base validate receipt is absent.

## Verdict

VERDICT: REQUEST CHANGES

The test-isolation edits are consistent with the recorded environment-leak diagnosis, and I found no weakened assertions or auth bypass. The selected required aggregate now passes on the exact head. Do not approve yet: the candidate does not provide the requested non-interactive operator-consent lane for the separate data-capabilities runtime path, and the exact-head runtime and validate jobs remain skipped. Also clean up the temp directory created by `hostConfigIsolationDir`.

## repo-rule compliance

- Read-only exact-head source and hosted-run review. No local tests, no product edits, no GitHub review/comment, no draft/ready change, no merge/close, no workflow dispatch, and no subagents.
- Planning repository remote verified before the first evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- Review used GitHub API/CLI refs and hosted logs, not the quarantined `/workers/baseharbor` checkout.
- `cleanliness: nothing started; docker ps -a before PID 2142367: empty`.

## cleanliness

- Before review: PID 2142367; `docker ps -a` returned only the table header, no containers.
- After review: PID 2170152; `docker ps -a` returned only the table header, no containers.

END codex-rev-1747 BLOCKED — #1750 exact-head review requests changes; required aggregate/runtime gates are skipped.

Planning evidence commit SHA: pending.

## PLAN — updated mission

134. Read /var/tmp/m/rev1750c.md.g and tail supplement; capture the updated exact-head review contract and restrictions.
135. Refresh PR #1750 head/base and terminal hosted checks, then inspect the exact candidate changes and provenance.
136. Reassess operator consent, test isolation, selected required checks, runtime/validate selection, and earlier findings without local tests.
137. Update the exact-head review evidence and run Planning validation; do not modify product code or PR state.
138. Publish only this review evidence, verify its path on Planning origin/main, update the board, and post END.

## Follow-up disposition

The review follow-up at `evidence/r28-welle5-2026-11-22/testcontext-0428-223/review-1750-head17f471cd3fe.md` classifies the temp-root omission as non-blocking P3 and confirms that the early return does not conceal the diagnosed 14-test root cause. Exact-head run `44982566548` passes `PR Selected Checks`; the final verdict is APPROVE. This follow-up supersedes the earlier skipped-aggregate statement in this historical review record.
