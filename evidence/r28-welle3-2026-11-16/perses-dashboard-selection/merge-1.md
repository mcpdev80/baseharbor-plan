# 0428-080 / PR #1590 — review, hopf and merge receipt

Date: 2026-11-17
Roles: CODEX-REVIEW, then mechanical hopf, then CODEX-MERGE
Planning task: `t-20261114-r28-perses-dashboard-selection`

## Candidate and hopf

- PR: https://github.com/mcpdev80/baseharbor/pull/1590
- Pre-hop head: `f611060cf5b1d3b21791ad79d7280f36b0e5f45d`; base develop: `ed55d893374b593a7a6032f0de496ca9920ad08d`.
- Fresh develop at hopf: `6cf121524da34ca11bc07ead0ab3c568d29e9c80` (#1678 merge). The #1590 branch was BEHIND; the old run 44037954501 was not reused.
- Isolated checkout: `/var/tmp/codex-welle2b-1590`; existing dirty product checkout was not modified.
- Incoming develop delta was exactly four #1678 files: `internal/apierror/error.go`, `internal/deployment/target.go`, `internal/machine/contract.go`, `internal/machine/contract_test.go`. No path overlap with #1590's `internal/capability/perses_selection.go` and `internal/capability/perses_selection_test.go`.
- Normal `git merge --no-edit refs/remotes/origin/develop` succeeded with no conflicts. Hopf commit: `8b5db6dab3a1ee87435fd2995feefbd95fb2b206`; parents are pre-hop PR head `f611060c…` and develop `6cf12152…`.
- Identity check: byte comparison of the old PR patch (`ed55d893...f611060c`) and new base-relative PR patch (`6cf12152...8b5db6da`) matched exactly. The hopf commit itself contains only the four incoming develop files. `git diff --check` on the hopf delta passed.
- Normal push published `8b5db6da…` to `lane-0428-080-r28-perses-selection`; remote `ls-remote` confirmed the exact SHA.

## Review

- Exact reviewed head: `8b5db6dab3a1ee87435fd2995feefbd95fb2b206`.
- Exact base: `develop` / `6cf121524da34ca11bc07ead0ab3c568d29e9c80`; PR API reported the same base/head pair.
- The complete selection diff remains the previously approved two-file change, byte-identical to the pre-hop candidate. It keeps Perses-native dashboard selection pinned to the accepted release and per-backend signal inventory, and scopes the identity-selection witness to the Keycloak identity dashboard. The non-forgeable witness regression checks that a caller-supplied `Available: true` without evidence fails closed; resolver construction from real signal/Target authorization is an explicit downstream contract, as recorded in the selection hunt and 078 handoff. Per the approved 0428-080 contract, that resolver implementation is outside this card.
- Review reference: batch15 approval and `evidence/r28-welle3-2026-11-16/hunt-selection/befund-1.md` (witness and dashboard scoping verified). No new content delta was introduced by the hopf.
- Verdict: **APPROVE**. No anomaly found in the exact candidate or its develop-only hopf delta.
- No unresolved review comments or threads were present. No GitHub review event was posted under the PR author's `mcpdev80` identity; verdict is recorded here.

## Exact-head CI

- Own run: https://github.com/mcpdev80/baseharbor/actions/runs/44040693658 — terminal `completed / success` on exact head `8b5db6dab3a1ee87435fd2995feefbd95fb2b206`.
- `PR Selected Checks`: SUCCESS from GitHub Actions integration 15368 on the same head.
- Selected and successful: native gate plan, Trusted Plan, source format, focused Python, Go unit shards `cli-0..3`, `packages`, `owner`, Go build and Go vet. Native runtime, HA, release-only and other non-selected jobs were skipped by CI selection.
- `ci-cost-note: run 44040693658, runner-minutes approx 21` (14 completed non-skipped jobs; summed job durations 1,247 seconds, rounded up to 21 minutes).
- At merge, PR state was OPEN, ready, `CLEAN`, exact head/base matched the recorded values; active required-check ruleset 25223521 required `PR Selected Checks` from integration 15368 and passed. Integration ruleset 23754541 was disabled.

## Merge and Planning

- Squash merge used expected-head guard: `gh pr merge 1590 --squash --match-head-commit 8b5db6dab3a1ee87435fd2995feefbd95fb2b206`.
- GitHub confirmed merge at `2026-11-17T07:48:20Z`; merge SHA `4094448543359a13ba312119304f1f70d3bc40a9`.
- Post-merge `ls-remote` confirmed develop at `4094448543359a13ba312119304f1f70d3bc40a9`.
- Task `t-20261114-r28-perses-dashboard-selection` set to closed/accepted with this receipt, PR, run and merge commit as evidence. Render/check completed before publication.
