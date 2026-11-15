# PR #1575 Review — r4 management-surface contract

ROLLE: REVIEW

## PLAN

1. Verify PR #1575, its base/head and the lane's Planning evidence.
2. Review the exact correction diff `293e0e05ac0..492b8e8f994` against the previous blocking finding.
3. Verify the exact-head hosted run and focused test evidence.
4. Run `plan.py check`, record the SHA-specific verdict, and publish this review akte. No merge.

## Reviewer identity

- Session: Codeman `1a678edb-8783-4c14-9707-eddde1e8d286` (`codex-rev-pr1575`, mode `codex`)
- Model: GPT-6-Luna
- Time: 2026-11-15 23:08 UTC

## Candidate and remote witnesses

- Repository: `mcpdev80/baseharbor`
- PR: [#1575](https://github.com/mcpdev80/baseharbor/pull/1575), OPEN, DRAFT, base `develop`
- Base: `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`
- Reviewed head: `492b8e8f994b16e6f73819a08175f8178cd63292`
- `refs/heads/lane-0428-075-perses-seam` and `refs/pull/1575/head` both resolve to the reviewed head. PR metadata confirms the same head and base.
- Exact requested diff `293e0e05ac04716e441a72679704cbfcc38d6e0e..492b8e8f994b16e6f73819a08175f8178cd63292`: 3 files, 192 insertions, 92 deletions. `git diff --check` passed.
- Lane evidence `evidence/r28-welle1-2026-11-15/perses-seam/round-4.md` is present in Planning commit `51bbbdba`, which is an ancestor of Planning `origin/main`.

## Review of the r3 finding

- The invalid Perses `IntegrationDescriptor` is removed. `PersesManagementSurfaceContractValue` is a distinct management-surface value type and has no capability-kind or versioned-capability-specification fields. Its `Owner` is the `ProviderPrometheus` reference; Perses no longer claims `Metrics`/`MetricsV1`.
- The contract carries the optional observability `management-ui` interface, shared scope and optional-lifecycle marker. I verified the referenced Prometheus integration exists in the reference catalog and declares the matching optional observability `management-ui` interface.
- The rewritten tests cover the distinct contract values, version axis, owner/interface fields, shared scope, optional lifecycle, absence from `ReferenceIntegrations()`, and continued validation of every reference integration. The extra repeated catalog exclusion loop in `TestPersesManagementNotRegisteredAsCapabilityProvider` is redundant but has no effect on the verdict.
- The r3 parser split is unchanged by this correction and remains covered by the lane's r3 evidence.

## Exact-head verification

- Run [43771897861](https://github.com/mcpdev80/baseharbor/actions/runs/43771897861): `CI · Source & Quality`, `pull_request`, head `492b8e8f994b16e6f73819a08175f8178cd63292`, completed SUCCESS.
- Successful jobs: `PR · Draft source and routing`, `PR · Draft Go · packages`, and `PR · Draft Go · cli-0` through `cli-3`.
- The Draft run skipped `PR Selected Checks`, native/HA and release jobs; this review does not count skipped jobs as executed evidence.
- The lane akte reports successful `go build ./...`, focused `go vet`, Perses tests in capability/metrics, and the source-readability audit. It records the full `internal/application` test failures as reproduced on the untouched r3 base. I did not run local product tests.

## Planning validation

- `python3 scripts/plan.py check`: 538 tasks, 7 epics, 13 releases, 22 decisions; **0 errors, 19 warnings**. Warnings are existing dependency-state warnings; the check exits successfully.

## repo-rule compliance

- Product review was read-only. No product source, PR state, CI run, branch or release state was changed.
- Only this review akte is added to Planning. No task metadata or generated views were edited.
- No merge or frost action was performed.

## Verdict

APPROVE exact candidate `492b8e8f994b16e6f73819a08175f8178cd63292` for PR #1575 / task `t-20261114-r28-perses-contract-seam`.

The r3 capability-claim finding is resolved: Perses is now represented by a separate management-surface contract with an owner reference and no capability claim. Exact-head hosted checks and Planning validation pass. No merge is authorized by this review akte.
