---
id: t-20261118-receipt-guard-single-operand
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
kanban_status: closed
card_number: 0428-116
card_short_title: receipt verification guard
kanban_title: 0428-116 · receipt verification guard
owner: w01-0428-116r4 (codeman 4d606ac2)
wait_reason: ""
blocker: ""
prs: [mcpdev80/baseharbor#1686]
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1686", "https://github.com/mcpdev80/baseharbor/actions/runs/44438849188", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/receipt-guard/r4-1.md", "https://github.com/mcpdev80/baseharbor/commit/40b9901398a6bae5b92ee45494ef3b70f192a2a7"]
resolution: accepted

---
# t-20261118-receipt-guard-single-operand · receipt verification guard collapses to single operand

- [x] t-20261118-receipt-guard-single-operand · receipt verification guard collapses to single operand #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** w01-0428-116r4 (codeman 4d606ac2)  
    **PR:** [baseharbor#1686](https://github.com/mcpdev80/baseharbor/pull/1686)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1686), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44438849188), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/receipt-guard/r4-1.md), [proof 4](https://github.com/mcpdev80/baseharbor/commit/40b9901398a6bae5b92ee45494ef3b70f192a2a7)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w01-0428-116r4 (codeman 4d606ac2)  
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

r3 END akzeptiert: merge-head 304673c28 (eltern 7459d615d+9a37b4bc, monoton, kein force), guard/test byte-identisch zu r2, exact-run 44429419752 SUCCESS, akte ddb1174d mit revision-labels; stale r3-1.md getilgt. 'behind' nur durch #1677-merge — merge-fenster-rebase steht wie bei den anderen. Routing an CODEX-REVIEW

REOPEN nach abnahme-entscheid (2026-11-19, reviewer unter owner-delegation): invariant FINAL fail-closed — applied non-continuation receipt mit unerwartetem continuation-edge faellt. mein downgrading ruling (2f35cf72) ist damit ueberstimmt: es war koordinatorenruling, der abnahmebefund + urspruenglicher akzeptanzsatz 'single-operand must FAIL' tragen. r4-lane fuehrt hopf auf de53246585 + guard-schaerfung + pin-umkehr + matrix-regression aus; alter head 304673c28 nicht merge-bar
## Invariant ruling FINAL (abnahme-instanz, 2026-11-19, unter owner-delegation)
FAIL CLOSED overrides both coord rulings: an applied non-continuation receipt carrying an unexpected continuation edge must fail (partial/error + grund). Grundlagen: sicherheitskonzept (secure-by-design) + urspruenglicher akzeptanzsatz der karte. Die downgrades (2f35cf72 applied/intentional) sind gegenstandslos. Umsetzung: schmale matcher-validierung + matrix-regression beide zweige, pin-umkehr. Pruefung laeuft in lane 4d606ac2 (hopf auf de53246585 inbegriffen).
## Acceptance contract detail (abnahme, 2026-11-19)
Fail-closed regression must assert BOTH: Status==failed AND ErrorCode=='actual-disposition-differs' (non-continuation ghost edge); continuation branch keeps its missing-evidence code. Base must contain current develop at push time (coordination note: normal merge, monotonic).

r4 END akzeptiert: head 96ac1b2e mit normalem develop-merge 7d343836 (monoton), fail-closed guard + exact ErrorCode-MATRIX (failed + actual-disposition-differs, reviewer-gegenprueft), run 44438849188 SUCCESS, r4-1.md am band 20d206e5 + r2-1.md ce9890-stornierung. Merge-fenster: review-finaliteit obliegt CODEX

Codex reviewer: current exact head 96ac1b2e independently reviewed; fail-closed matrix asserts failed plus actual-disposition-differs; run 44438849188 terminal SUCCESS; base current develop 7d34383644. Source/tests accepted; merge gate passed.

Accepted by independent Codex review at exact head 96ac1b2e; exact run 44438849188 SUCCESS; merge 40b9901398a6bae5b92ee45494ef3b70f192a2a7 verified as develop.
