# Codex disposition: #1819 supersession and #1820 catalog provenance

## PLAN

1. Verify the live exact heads, PR bases, head-to-head tree delta, PR changed-file lists, and catalog row provenance for #1819 and #1820.
2. Decide whether #1819 has unique payload or is content-superseded by #1820, keeping the #1812 → #1819 → #1820 chain contract in view.
3. Classify the 27 catalog lines by checking their origin, presence on develop, and whether `scripts/pr-gate-coverage.json` is in #1820's own PR diff.
4. State the correct status and PR references for Plan cards 0428-273 and 0428-274, and separate the 0428-359/#136 family from the runtime-identity rows.
5. Publish this disposition in a single Akte-only Plan PR; obtain the exact-head Hosted Plan result and verify the Akte path on live Plan main before END.

## 4-Feld / identity

Lane: executing session `w255-0428-251-demo170codex`.  
Card: 0428-274; related existing card 0428-273.  
Repos and PRs: `mcpdev80/baseharbor-plan` evidence PR; `mcpdev80/baseharbor` #1819, #1820, #1822, and #1852.  
Role: CODEX-DECISION; no product edit, product merge, workflow action, or PR close performed by this act.

Plan repository remote verified before the first evidence commit using `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`. Exact relevant output:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

The isolated worktree was cut from Plan `origin/main` SHA `f2c91b01befe7123398da0046fed405b69c5e58f`, confirmed by `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` and worktree `HEAD` before branch creation. Plan main moved during setup; the candidate was fast-forwarded to live main before its first authored commit. The original cut SHA remains the provenance base and must be an ancestor of that first authored commit.

Card 0428-274 owner line, verbatim from Plan main at worktime: `owner: "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)`.

Card 0428-273 owner line, verbatim from Plan main at worktime: `owner: ""`.

Commit identity: `w255-0428-251-demo170codex <w255-0428-251-demo170codex@baseharbor.local>`. Literal invocation: `git -c user.name='w255-0428-251-demo170codex' -c user.email='w255-0428-251-demo170codex@baseharbor.local' commit -m 'review(0428-274): dispose #1819 and #1820 relationship'`. Before push, `git show -s --format=%an HEAD` must equal `w255-0428-251-demo170codex`; verify committer with `git show -s --format=%cn HEAD` as well.

## Verified facts

### Candidate content and supersession

* Live product refs at read time: develop `ea5218d72e263f21e79853b679af50074dab8c25`; #1819 head `b3c5055ad2566b639c2b0d4f4c2848b045221ebf`; #1820 head `8f6b2444bdc9baabf4f492e930533c7c36406979`.
* #1819 base is `28296a2e6e920592741c9397486358deac7e95b2`; #1820 base is `fcd449117e189c555c7530b9527cd22d3f6f25ff`.
* The head-to-head compare `b3c5055ad2566b639c2b0d4f4c2848b045221ebf...8f6b2444bdc9baabf4f492e930533c7c36406979` reports `ahead_by=11`, `behind_by=0`, merge base exactly `b3c5055ad2566b639c2b0d4f4c2848b045221ebf`, and one changed path: `scripts/pr-gate-coverage.json`, +27/-0. The 27 lines are three rows for runtime-identity workload lifecycle sources.
* The four product paths in both PRs are the same: `.github/workflows/pre-release-runtime-suite.yml`, `internal/application/runtime_postgres.go`, `internal/metrics/perses_dashboard_provision.go`, and `internal/metrics/perses_dashboard_provision_test.go`. The compare shows no product-file delta between these heads; #1820 carries the #1819 payload.
* Current GitHub state: #1819 is already closed unmerged at `2026-11-27T07:57:19Z`; its close comments 7212984198 and 7212984556 record supersession by #1820 and the four matching product blobs. #1820 remains open at the exact head above. This disposition independently confirms the content-superseded classification; it does not qualify or merge #1820.

### The 27 rows are trusted base content, not #1820 self-authorization

* PR #1852, titled `fix(0428-307 carrier): catalog runtime-identity workload gates`, merged to develop at `2026-11-25T21:23:48Z` as `fcd449117e189c555c7530b9527cd22d3f6f25ff`. Its sole changed path is `scripts/pr-gate-coverage.json`, with exactly +27/-0; its patch is the same three runtime-identity rows seen in the head-to-head compare.
* `fcd449117e189c555c7530b9527cd22d3f6f25ff` is #1820's recorded base SHA. #1820's own PR file list contains only the four product paths above and does not contain `scripts/pr-gate-coverage.json`. Therefore those 27 lines are already on the target base before #1820; they are not candidate-added rows authorizing their own candidate.
* Live develop contains each runtime-identity row exactly once: `source.internal_application_runtime_identity_workload_go` at `scripts/pr-gate-coverage.json:687-693`, `source.internal_application_runtime_identity_workload_fallback_test_go` at `:696-702`, and `source.internal_application_runtime_identity_workload_test_go` at `:705-711`. Each has `runtime_specific: true` and Docker plus Podman lifecycle surfaces.
* The originating row family belongs to existing card 0428-307 (`t-20261125-hunt37-runtime-identity-fallback`) and PR #1852. It is not part of #136's 0428-359 recovery-manifest catalog family. No additional row, baseline PR, or #136 edit is needed for these three paths.

### Cards 0428-273 and 0428-274

* The three 0428-273 rows for `runtime_postgres.go`, `perses_dashboard_provision.go`, and its test are present exactly once on live develop, delivered by baseline PR #1822 (merge `90086a1f938e106171b08c76e9bcbc98d89d1de4`, `2026-11-24T09:48:36Z`).
* The 0428-274 row `source.cmd_baha_app_broker_compat_test_go` for `cmd/baha/app_broker_compat_test.go` is also present exactly once on live develop from the same PR #1822.
* Board representation: both baseline cards 0428-273 and 0428-274 have completed source-row scope and should be `closed` with `resolution: accepted`; their `prs` field should reference the actual publisher #1822 and their evidence should link its HTTPS PR/merge witness. Do not use product #1819 or #1820 as the publisher for those rows. The #1819 implementation belongs to product card 0428-181 and is superseded by #1820; the #1820 implementation belongs to product card 0428-271. The 27 runtime-identity rows are traced under 0428-307/#1852. No card fields were edited in this decision-only Akte.

## Disposition

1. #1819 is content-superseded by #1820. The exact product payload is carried forward; no distinct #1819 file or product blob is lost. It does not need to remain as a separate merge step in the #1812 → #1819 → #1820 chain. The #1819 PR has already been closed unmerged as superseded; #1820 remains the carrier and still requires its own acceptance and hosted qualification.
2. The 27 rows are valid baseline content already delivered on develop by #1852. They are not a candidate-side self-authorization in #1820. Their card/PR provenance is 0428-307/#1852, not #136/0428-359.
3. Cards 0428-273 and 0428-274 should reflect their completed catalog-row work as closed/accepted with PR #1822 as publisher. The product consumer PRs remain referenced by their product cards, not treated as catalog publishers.

No product files, `.github/**` workflow, product PR state, or catalog rows were changed. No local tests were run.

## END

END_DONE w255-0428-251-demo170codex: #1819 content-superseded by #1820; 27 rows are trusted base from #1852; board disposition recorded in Plan PR evidence.

Before the first authored commit, this branch was fast-forwarded from the original cut SHA `f2c91b01befe7123398da0046fed405b69c5e58f` through the live Plan main tip `4a855876fc188d90c2d39cc5b972fd7b9374d5ed` to `3024a3cddb5014ee14d52c441811041f3823c2af`. The exact cut SHA remains an ancestor; no foreign candidate commit was introduced.
