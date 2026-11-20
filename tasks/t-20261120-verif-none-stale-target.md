---
id: t-20261120-verif-none-stale-target
card_number: "0428-203"
card_short_title: "Stale target on none switch"
type: bug
areas: [metrics, observability]
release: v0.4.28
version: ""
parent: ""
owner: w205-0428-203-staletgt
kanban_status: wait
kanban_lane: wait
kanban_summary: "When an already-verified metrics source switches its Verification mode to none while keeping the same source ID, the emitted…"
kanban_title: 0428-203 · Stale target on none switch
priority: normal
depends_on: [t-20261119-r28-app-source-verification-none-ignored]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1730]
sources: []
blocker: ""
wait_reason: "handoff abgeschlossen: PR #1730 head c90a73ac8128 == refs/pull/1730/head, base refs/heads/lane-0428-143-verify-none (stapel korrekt auf der basis-lane), draft=false, 2 dateien (internal/capability/integration_contract.go + internal/metrics/prometheus_verify_workload_only_test.go). run 44812049031 terminal = 8 success / 6 failure, an eigenem inhalt fehlerfrei: cli-0..3 = feld-gate 0428-198, packages (Loki-trio) = feld-gate 0428-202. befund war 'covered', abgeliefert als eine contract-zeile + eine regression ueber das echte TargetsDir, wart-semantics aus 0428-143 unveraendert. akte traegt PR-num-mer, head, base, run-id, conclusion je zelle + cleanliness-zeile."
resolution: ""
evidence: []
---

- [ ] t-20261120-verif-none-stale-target · Stale emitted target after Verification=none switch #task #release/v0-4-28 #status/wait #view/wait #area/metrics #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** w205-0428-203-staletgt · **Priority:** normal  
    **PR:** [baseharbor#1730](https://github.com/mcpdev80/baseharbor/pull/1730)  
    **Waiting:** handoff abgeschlossen: PR \#1730 head c90a73ac8128 == refs/pull/1730/head, base refs/heads/lane-0428-143-verify-none (stapel korrekt auf der basis-lane), draft=false, 2 dateien (internal/capability/integration\_contract.go + internal/metrics…  
    **Needs:** [t-20261119-r28-app-source-verification-none-ignored](t-20261119-r28-app-source-verification-none-ignored.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261119-r28-app-source-verification-none-ignored](t-20261119-r28-app-source-verification-none-ignored.md)  
**Owner:** w205-0428-203-staletgt  
**Priority:** normal  
**PRs:** [baseharbor#1730](https://github.com/mcpdev80/baseharbor/pull/1730)  
**Source:** 
<!-- /generated:links -->


## Goal

When an already-verified metrics source switches its `Verification` mode to `none` while keeping the same source ID,
the emitted scrape target must stop being reported. Today the target can remain in the emitted output (a stale
"up"-carrying entry) even though the new mode says "do not verify this source", so an operator keeps seeing a target
that the contract no longer covers.

## Why this exists (funds, not speculation)

Found while implementing 0428-143 (Option A: uniform `Verification=none` semantics). The lane recorded the finding
separately and out of its own write-set, per AGENTS 4.2 (a fix meets exactly the reported defect; surroundings are a
proposal, not a silent extra PR).

* Witnessed by an independent review of PR #1693: a same-ID source switched to `VerificationNone` still produced a
  stale emitted target.
* Contract text today lives at exactly one place, `internal/capability/integration_contract.go:242`, and it only
  validates the provider signal-liveness field - it says nothing about retiring output that was emitted before the
  mode changed.
* 0428-143 makes `none` mean "no verifier assertion" for BOTH source classes (the application loop now carries the
  same guard as the provider loop). That fixes the *waiting* behaviour. It does not by itself prove that an entry
  already emitted under the old mode is *dropped* on the next refresh.

## Scope and file ownership

Owner of this card may edit: `internal/metrics/prometheus_verify.go`, `internal/metrics/prometheus_files.go`
(exported-target assembly only), `internal/capability/integration_contract.go` (contract sentence for retiring
stale output) and their test files.

Locked, read-only: `internal/serviceaccess/**` (0428-202 sits on the owner's #1594/0428-053 rail),
`internal/observability/registry.go`, `internal/capability/perses_selection.go`, `internal/identityprovider/**`,
`internal/machine/**`, `internal/operatorauth/**`, `.github/**`.

## Acceptance

1. A regression test seeds a source with a concrete ID, emits its target under a verifying mode, switches the SAME id
   to `VerificationNone`, and asserts the target is NOT present in the emitted output afterwards - asserted through
   the real exported surface, not an internal helper.
2. The rule ("switching to `none` retires previously emitted output") is stated in exactly ONE place in
   `internal/capability/integration_contract.go`; no second file documents it.
3. The test is executed by the GitHub CI, and the card names which shard discovers it (per the CI intake rule of
   AGENTS 5.3).
4. Fail-closed behaviour elsewhere is unchanged: this card must not alter the verifier's waiting semantics that
   0428-143 fixed.
5. One hosted run at the exact head, observed by the owning lane until a terminal state (AGENTS 4.6). If
   `PR · Go unit · cli-0..3` fails with "Managed-environment machine operations require an authenticated BaseHarbor
   operator", that is the field-wide gate defect (card 0428-198, root `2af892e4e` in `internal/serviceaccess/policy.go`)
   and not this diff: record run id + the verbatim line and report `GATE-FAIL 0428-198`.

## Stop rules

* If retiring emitted output requires a change inside a locked path, STOP and report `file:line` (AGENTS 4.3).
* If the stale entry turns out to be an artifact of the test harness (a fixture that never refreshes), report it as a
  finding instead of shipping a product change.

## Dependencies

`depends_on: [t-20261119-r28-app-source-verification-none-ignored]` - this card builds on the uniform-semantics
decision of 0428-143; its lane must not re-litigate that decision, and the lane stacks on 0428-143's branch content
rather than waiting for a merge (one PR per card, stacks branch off the base lane's head).

ARBEITET JETZT, kante gegen session gemessen (w205-0428-203-staletgt, ornith, worktree aus dem KOEPF DER BASIS-LANE 0428-143 = refs/heads/lane-0428-143-verify-none head 809a8196e1cf, gemessen draft=false + ancestry auf develop 40cb28c758b0 JA). KARTE IST MEINE EIGENE ARBEIT AUS DER FUND->PFLICHT: der zweite befund von 0428-143 ('quelle wechselt bei gleicher id auf Verification=none, der zuvor emittierte target bleibt in der exportierten oberflaeche') hat jetzt goal, zeugen (review zu #1693 + integration_contract.go:242 prueft nur provider-signal-liveness), write-set, akzeptanz und stop-regeln - 0428-203, planned->active, damit der fund nicht verlorene arbeit bleibt (§3.3.5). STAPELREGEL, ausdrucklich im auftrag: PR-BASIS = refs/heads/lane-0428-143-verify-none, nicht develop, nicht ein paralleler nachfolger; gewartet wird auf inhalte, nie auf merges. ERSTE PFLICHT DER LANE: den fall REPRODUZIEREN bevor aenderung; ist er auf dem aktuellen stand schon vom vorlauf erledigt, meldet sie 'befund covered' mit beleg statt code zu aendern (§4.2). gateway-faelle: cli-0..3 + Selected Checks = 0428-198, packages = internal/logs Loki-trio = 0428-202 - benennen, nicht richten.

ARBEITET, PR SCHON DA - MESSEN UND NOTIERT: #1730 head c90a73ac8128, BASE refs/heads/lane-0428-143-verify-none (der stapel sitzt also korrekt auf der basis-lane, nicht auf develop und nicht auf einem parallelen nachfolger, §3.3.8), draft=false, 2 dateien: internal/capability/integration_contract.go + internal/metrics/prometheus_verify_workload_only_test.go. IHR BEFUND IST 'COVERED, NICHT UMGBAUT': die akte/der patch sagen, ein target mit fester id hoert nach dem wechsel auf Verification=none beim naechsten export AB (verwiesen wird auf internal/metrics/prometheus_files.go als ausfuehrende stelle), und die neue regression TestVerifyApplicationSourceVerificationNoneRetiresPreviouslyEmitted assertiert das ueber das ECHTE TargetsDir, nicht ueber eine interne hilfsfunktion; die wart-semantics aus 0428-143 bleiben ausdruecklich ungeaendert. checks am head: 4 success / 6 queued / 3 in_progress / 20 skipped - also noch kein terminalergebnis, karte bleibt active bis der run durch ist und die akte (evidence/r28-welle4-2026-11-20/verif-none-stale-target/round-1.md) run-id + conclusion traegt. wenn die required-zellen am feld-gate 0428-198 scheitern: wie in den anderen faellen 'GATE-FAIL 0428-198' + state-zeile, und der beweis aus dem kleinsten passenden gate (§5.4).
