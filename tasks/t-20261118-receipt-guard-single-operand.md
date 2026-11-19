---
id: t-20261118-receipt-guard-single-operand
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
kanban_status: review
card_number: 0428-116
card_short_title: receipt verification guard
kanban_title: 0428-116 · receipt verification guard
owner: coord
wait_reason: ""
blocker: ""
prs: [mcpdev80/baseharbor#1686]

---
# t-20261118-receipt-guard-single-operand · receipt verification guard collapses to single operand

- [ ] t-20261118-receipt-guard-single-operand · receipt verification guard collapses to single operand #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** coord  
    **PR:** [baseharbor#1686](https://github.com/mcpdev80/baseharbor/pull/1686)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** coord  
**Priority:** not set  
**PRs:** [baseharbor#1686](https://github.com/mcpdev80/baseharbor/pull/1686)  
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

fix-1 akte red->green, CI 44409288750 SUCCESS

red->green guard-fix, exact-head run 44409288750 SUCCESS auf f1df8d7f6, matrix-regression beide operanten

red->green guard-fix, exact-head run 44409288750 SUCCESS auf f1df8d7f6, matrix-regression beide operanten
## Invariant ruling REVISED (coord, 2026-11-19 after reviewer re-trace)
Downgrade: no confirmed runtime defect at A=false (guard correctly skips continuation checks; the extra-edge acceptance is intentional current behavior). Finding stays as documentation mismatch. r2 scope: (a) fix the contradictory comment, (b) align test name + card phrasing with the intentional behavior, (c) PIN the current semantics in a matrix test (non-continuation fixture stays applied; continuation fixture fails on missing evidence) so a future fail-closed change must update this pin deliberately. Fail-closed enforcement, if ever wanted, belongs to 0428-120 (status honoring), not here.

## r2 empirical confirmation (lane 91d9173b, ca149b3)
Confirmed on PR #1686 head ca149b3: non-continuation applied receipt with a stray ghost edge -> `status=applied code=` (correct fix-1 guard); the un-parenthesised broken guard mislabels it `continuation-dependency-unverified` (red). Pin `TestProviderResultNonContinuationBehaviourPin` asserts both operands. Guard source unchanged.

r2 END: head 7459d615d (guard unveraendert), exact-run 44423543955 SUCCESS vom reviewer bestaetigt; evidence-widerspruch getilgt (retraction + revision-labels); coord-flag als geloest gekennzeichnet + CI-capture nachgetragen; Re-review geroutet
## Runtime debt (uebernommen aus 0428-113/#1680, Owner-Ausnahme 2026-11-18)
#1680 wurde ohne ORAS gemergt: die Runtime-Docker-/Podman-Evidence fuer den Loki-/Prometheus-Pfad ist offen (see evidence/1680.md). Diese karte (0428-114) ist ausdrueckliche Eigentuemerin dieser Debt; Abschluss erfordert ORAS-verfuegbare Runner-Cellen oder eine dokumentierte Alternative, bevor die Observability-Kette als voll qualifiziert gilt. Kein Block fuer den r3-guard-kandidaten selbst.
