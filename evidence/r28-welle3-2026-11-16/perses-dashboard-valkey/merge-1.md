# Welle2c object 2 — merge receipt

Date: 2026-11-17
Task: PR #1604, live task `0428-081` / `t-20261114-r28-perses-dashboard-valkey` (owner `w081`). The mission mistakenly labels #1604 as 0428-079 messaging; that separate card still references #1603. Review and merge followed the owner's explicit instruction to continue with PR #1604 and the actual 0428-081 contract.

## Review and gates

- CODEX-REVIEW verdict: APPROVE in [`review-1.md`](review-1.md), published before merge.
- Reviewed exact PR head: `beb4402892c40b8d630cc051173de62c37054a3b`.
- Exact-head run `44049695785`: terminal SUCCESS. `PR Selected Checks` SUCCESS from GitHub Actions integration 15368. Policy, native gate plan, source format, trusted plan, focused Python, build, vet, all selected Go unit shards and aggregate selected check succeeded. Trusted plan skipped unrelated runtime/release gates.
- `ci-cost-note: run 44049695785, runner-minutes approx 20` (1,155 summed job-seconds).
- Before merge `ls-remote`: develop `0ec4706b12c8fa869a2c23db18b6cab4f91f2178`; PR branch `wt-0428-081` `beb4402892c40b8d630cc051173de62c37054a3b`.
- `mergeable=true`, `mergeable_state=clean`; no open comments or unresolved review threads.
- Expected-head guard: `gh pr merge 1604 --squash --match-head-commit beb4402892c40b8d630cc051173de62c37054a3b`.

## Merge result

- PR #1604 merged by `mcpdev80` at `2026-11-17T08:54:27Z`.
- Squash merge SHA: `62eaea2c8c5b29f73db03ae9b3e7efaf772e4458`.
- Merge commit has one parent: develop `0ec4706b12c8fa869a2c23db18b6cab4f91f2178`.
- After merge, fresh `ls-remote` verification is recorded in the object END post and will serve as the base for object 3.
- Merge form: squash, satisfying the current develop merge method. Object 1's owner-side 2-parent merge (`0ec4706b`, #1679) remains accurately recorded in `trace-probe-adapter-gap/merge-1.md` as an owner merge outside this session, per owner disposition.

END welle2c object 2: CODEX-REVIEW APPROVE; PR #1604 squash-merged with expected-head guard; run and cost recorded; task-card mapping discrepancy disclosed.
