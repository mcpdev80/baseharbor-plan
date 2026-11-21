---
id: t-20261121-loki-verify-probe
card_number: "0428-212"
card_short_title: "0428-212 loki health"
type: bug
areas: [observability]
release: v0.4.28
version: ""
parent: ""
owner: w235-0428-212-lokifix2
kanban_status: review
kanban_lane: review
kanban_summary: "TestPersesLokiDatasourceVerifyNeverReportsHealthy proves the health path rejects an unreachable Loki, not merely a missing…"
kanban_title: 0428-212 · 0428-212 loki health
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1734]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261121-loki-verify-probe · loki health verify must reach the probe, not a missing-file exit #task #release/v0-4-28 #status/review #view/review #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** w235-0428-212-lokifix2 · **Priority:** high  
    **PR:** [baseharbor#1734](https://github.com/mcpdev80/baseharbor/pull/1734)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w235-0428-212-lokifix2  
**Priority:** high  
**PRs:** [baseharbor#1734](https://github.com/mcpdev80/baseharbor/pull/1734)  
**Source:** 
<!-- /generated:links -->

## Goal

`TestPersesLokiDatasourceVerifyNeverReportsHealthy` proves the health path rejects an **unreachable Loki**, not merely a
missing certificate file: one subtest materializes the service-access PKI and asserts the probe failure, the unmaterialized
case stays an explicit precondition subtest.

## Why

H-V23 found the one real defect in the loki witness set (akte
`evidence/bug-hunt-2026-11-21/fail-closed-honesty/round-1.md`, section 4 and Karte E): at `internal/logs/loki_test.go:355-361`
the unhealthy result comes from `serviceaccess.ExistingTLSMaterial` stat-ing a non-existent
`service-access/pki/client-cert.pem` (`internal/logs/loki_datasource.go:399-401`, `internal/serviceaccess/pki.go:112-116`).
The contract "never reports healthy without a reachable Loki" is therefore never exercised.

## Scope

Allowed write-set:

- `internal/logs/loki_test.go` (uses the existing `materializeLokiServiceAccessPKI` helper at `:434`)

Forbidden: `internal/serviceaccess/**` (Owner rail, file:line findings only), `internal/logs/loki_datasource.go`
(production behaviour stays), `.github/**`, `cmd/baha/**` (0428-204 owns that directory while it runs).

## Acceptance criteria

1. Two named subtests: materialized PKI plus unreachable endpoint asserts the probe error by type or content, distinct from
   the missing-file error; unmaterialized PKI asserts the precondition error explicitly.
2. Neither subtest may pass on "some error occurred": each asserts the expected failure identity.
3. Evidence quotes the failing output before and the passing output after, with the exact candidate head.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | Go unit shards for `./internal/logs/` (PR Selected Checks) |
| Test identifier | `0428-212` |
| Route | `auto-discovery` |

## Stop and report

If the probe cannot be reached without changing `internal/serviceaccess/**`, stop and report file:line.

## Handoff

Branch, PR, exact head SHA, terminal hosted run id, evidence
`evidence/r28-welle4-2026-11-21/loki-verify-probe/round-1.md`.

COMMISSIONED from hunt H-V23 Karte E: split internal/logs/loki_test.go into (a) materialized PKI + unreachable endpoint asserting the PROBE refusal and (b) an explicit unmaterialized-PKI precondition case. Told to stay off internal/logs/loki_datasource.go (0428-204 named it once) and to stack onto the 204 branch instead of touching the seam.

HANDOFF (w227-0428-212-lokiprobe, newest first): candidate published as PR https://github.com/mcpdev80/baseharbor/pull/1734 (head 75770bd2d0434bfed11d7c1b106064a5a08d5a51, base develop 40cb28c758b02960356434b630086a341ebe1738, draft=false) plus akte evidence/r28-welle4-2026-11-21/loki-verify-probe/round-1.md. Terminal hosted run 44845451055 observed to completion: `PR · Go unit · packages` SUCCESS at the exact head (the required shard), `owner`/plan/format/vet/build/Python success; `cli-0..3` red with the develop-inherited cmd/baha failures — GATE-FAIL 0428-204, allowed per mission. All THREE client-cert.pem fixture failures named in the owner addendum heal at this head (3/3), plus the card's own vacuous witness split into two named subtests. Open points: none for this card; #1732 (0428-202) overlaps content-side in the same fixture helper and resolves at merge time on whichever lands first.

HANDOFF COMPLETE: PR #1734 (head 75770bd2d043, base develop 40cb28c758b0, draft=false) + akte evidence/r28-welle4-2026-11-21/loki-verify-probe/round-1.md on plan main (plan-sha 04da627d). All three client-cert.pem fixture sites fixed and the card test split into probe-rejection vs precondition subtests, exactly the contract. Measured by coordinator on run 44845451055 (terminal): 'Go unit · packages' and 'Go unit · owner' GREEN at the exact head, cli-0..3 still red and correctly labelled by the lane as GATE-FAIL 0428-204 (develop-inherited), not as this card's failure. NEW CONSEQUENCE FOR THE WINDOW: packages green at this head means #1732 (0428-202) may be superseded in content - comparison commissioned, see card 0428-202.

CODEX-REVIEW REQUEST CHANGES at 75770bd2 (review-1.md, ROLLE REVIEW, head unchanged before/after): the new subtests are content/type bound, but two existing refusals in the same Loki health family still pass on ANY error - loki_test.go:343-350 (err != nil only) and :466-481 (PKI left unmaterialized). That is the honesty rubric of this day catching a real case. Correction round commissioned in a fresh lane on branch from the exact candidate head; the reviewer states explicitly that the red CLI cells are NOT this card content problem (GATE-FAIL 0428-204 acknowledged).

review to active after CODEX REQUEST CHANGES (2599561f): two existing Loki refusals check only err != nil at loki_test.go:343-350 and :466-481. correction in w235 (89245a26); r2 head 45d181ab4089 is a descendant of 75770bd2d043, so a fast-forward push to the original lane branch keeps PR 1734 as the single PR for this card.

korrektur geliefert: w235 fast-forwardete den ursprünglichen branch auf 45d181ab4089 (nachkomme von 75770bd2d043, gemessen merge-base --is-ancestor = 0), PR-head bewegt, develop ancestor. re-review angestossen in derselben reviewer-session.

korrektur geliefert: w235 fast-forwardete den urspruenglichen lane-branch auf 45d181ab4089 (nachkomme von 75770bd2d043, von mir gemessen 'merge-base --is-ancestor' = 0), PR-head bewegt, develop ancestor. gehosteter versuch 44853938826 terminal: packages/build/vet/owner GREEN, cli-0..3 RED = geerbt (karten 0428-204/215), nicht inhalt. akte round-2.md plan main 4857b2a5. re-review angestossen.

CODEX-REVIEW runde 2 = APPROVE an head 45d181ab4089 (plan fd7b27ba, path witness 6dc43162, review-2.md): beide verweigerungen nennen jetzt ihren grund, assertions sind produktions-erreichbar, nur die karten-eigene datei geaendert, vier commits als eine fast-forward-kette, kein zweiter PR. 'PR Selected Checks' bleibt rot an den geerbten cli-shards (main_test.go:60 'Managed-environment machine operations require an authenticated BaseHarbor operator') - der reviewer haelt das ausdruecklich fuer NICHT-inhalt dieser karte. die karte bleibt 'review' bis zum merge, weil das native schema kein 'accepted' als spalte kennt.
