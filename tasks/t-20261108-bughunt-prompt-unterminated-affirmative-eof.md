---
id: t-20261108-bughunt-prompt-unterminated-affirmative-eof
card_number: "0427-166"
card_short_title: "Unterminated affirmative plus "
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w166-halfyes
kanban_status: active
kanban_lane: active
kanban_summary: "Reader treats line-buffered input only: complete \"y\n\" authorizes, torn \"y\"+EOF cancels cleanly; regression for both cases in…"
kanban_title: "0427-166 · Unterminated affirmative plus "
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/act-1485-review.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-prompt-unterminated-affirmative-eof · Bug Hunt v0.4.27: Half-line yes wins #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w166-halfyes · **Priority:** normal  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/act-1485-review.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w166-halfyes  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Reader treats line-buffered input only: complete "y\n" authorizes, torn "y"+EOF cancels cleanly; regression for both cases in the trust-prompt test group (CI captured).

## Problem (source evidence in the dossier)
act-1485-review.md (plan 07a28a33) found, and the merged #1485 keeps, a gap: unterminated affirmative bytes followed by EOF (a torn "y" with no newline) still authorize the trust uninstall action. Only complete lines should count as answers; EOF without a terminating newline must abort with "Host trust unchanged." Consistent with the install path and card 138 semantics.

## Acceptance
Reader treats line-buffered input only: complete "y\n" authorizes, torn "y"+EOF cancels cleanly; regression for both cases in the trust-prompt test group (CI captured).

## Dependencies and file ownership
Follow-up of 0427-161 (merged #1485). Write-set: cmd/baha trust prompt reader (same site as #1485 fix).

## Exact-head CI monitoring — 2026-11-08 (0427-166)

- [PR #1488](https://github.com/mcpdev80/baseharbor/pull/1488), head `be2d071cf83dd94cbe7cf43e5007d46e761f1090`, [CI #42502971526](https://github.com/mcpdev80/baseharbor/actions/runs/42502971526). Initial selected CI checks have no failures; the Go unit-test matrix is still running. Card remains open until the required CI is terminal green.

## Verified PR #1488 merge — 2026-11-08

- [PR #1488](https://github.com/mcpdev80/baseharbor/pull/1488) merged as `3187cea15728143146905c7238ad6e280ca11b3e` from head `be2d071cf83dd94cbe7cf43e5007d46e761f1090`.
- [CI #42502971526](https://github.com/mcpdev80/baseharbor/actions/runs/42502971526) = SUCCESS with Go unit/build/vet, source format, gofmt and native Docker/Podman destroy-retry checks; no required check skipped.
