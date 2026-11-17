# 0428-111 / PR #1678 — review and merge receipt

Date: 2026-11-17
Roles: CODEX-REVIEW, then CODEX-MERGE (sequential)
Planning task: `t-20261117-hunt-uid-docs-111`

## Exact candidate and review

- PR: https://github.com/mcpdev80/baseharbor/pull/1678
- Reviewed head: `f17c929674874093f10c049fe8f765ecff8365c9`
- Exact base: `develop` / `ed55d893374b593a7a6032f0de496ca9920ad08d`; the candidate commit has this exact parent, and PR base API reported the same SHA.
- PR was open, ready (not draft), mergeable, and `CLEAN`; one candidate commit, four changed files: `internal/apierror/error.go`, `internal/deployment/target.go`, `internal/machine/contract.go`, `internal/machine/contract_test.go`.
- Reviewer: Codex in this mission session; PR author: `mcpdev80`. No GitHub review event/comment was posted because this account authored the PR; verdict is recorded here. The develop integration ruleset 23754541 was disabled. The active required-check ruleset 25223521 remained enforced.
- Verdict: **APPROVE**. The change keeps config sentinels in the leaf `apierror` package, re-exports the identical values from deployment, and maps both with `errors.Is` in `machine.Classify` to `source_missing` with actionable guidance. The wrapping preserves the original error text. Regression coverage checks missing and empty config cases, message preservation, and the existing generic-error `internal_error` counterexample. The diff stays within the declared classify-layer scope; no anomaly found.
- No unresolved review comments or threads were present.

## Verification

- Exact-head workflow run: https://github.com/mcpdev80/baseharbor/actions/runs/44037527494 — terminal `completed / success` on `f17c929674874093f10c049fe8f765ecff8365c9`.
- `PR Selected Checks`: SUCCESS, GitHub Actions integration 15368, exact same head.
- Selected Go unit shards (`cli-0..3`, `packages`, `owner`), deployment package tests, Go build, Go vet, source format, native gate plan, Trusted Plan, exact candidate, and Docker lifecycle all succeeded. Non-selected jobs were skipped by CI selection.
- `ci-cost-note: run 44037527494, runner-minutes approx 30` (19 completed non-skipped jobs; summed job durations 1,791 seconds, rounded up to 30 minutes).

## Merge

- Merged by squash with expected-head guard: `gh pr merge 1678 --squash --match-head-commit f17c929674874093f10c049fe8f765ecff8365c9`.
- GitHub confirmed merged at `2026-11-17T07:32:27Z`; merge commit: `6cf121524da34ca11bc07ead0ab3c568d29e9c80`.
- Post-merge `ls-remote` confirmed `develop` at `6cf121524da34ca11bc07ead0ab3c568d29e9c80`.
- Planning task `t-20261117-hunt-uid-docs-111` updated to closed/accepted with PR, run, merge commit and this receipt as evidence; rendered and checked before publication.

The product checkout contained unrelated uncommitted changes from concurrent work. Review used GitHub's immutable PR diff/API; those workspace changes were left untouched.
