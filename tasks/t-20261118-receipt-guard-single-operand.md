---
id: t-20261118-receipt-guard-single-operand
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
kanban_status: active
card_number: 0428-116
card_short_title: receipt verification guard
kanban_title: 0428-116 · receipt verification guard
owner: w1-lane-8a994dc2 (0428-116)
wait_reason: ""
blocker: ""

---
# t-20261118-receipt-guard-single-operand · receipt verification guard collapses to single operand

- [ ] t-20261118-receipt-guard-single-operand · receipt verification guard collapses to single operand #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** w1-lane-8a994dc2 (0428-116)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w1-lane-8a994dc2 (0428-116)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal
Fix `internal/application/provider_change_result.go:40-46`: the receipt verification guard collapses to a single operand, so a receipt can pass validation on one operand alone. Align the guard with the intended full verification condition.

## Scope
- Correct the guard logic in provider_change_result.go (and its helper continuationRequiresDependencyEvidence in provider_change_dependency.go if the collapse is there).
- Close the coverage gap: `provider_change_dependency_result_test.go` only drives one path — add matrix tests for both operands (single-operand-must-FAIL regression).
- New CI capture: tests run inside the existing application unit shard (no workflow changes needed — verify selection picks them up).

## Required checks
- go build/vet/gofmt, internal/application unit tests incl. new matrix cases on exact head.

## Dependencies and file ownership
- Source: hunt 914 Befund 1 (HIGH), evidence/r28-welle4-2026-11-18/hunt-authsurf/befund-1.md (origin/main f00ca1e4).

claim der guard-fix-lane; owner-feld fehlte im claim — ergaenzt, check wieder 0
