---
id: t-20261105-r27-snapshot-change-guard-deterministic
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: ""
owner: coord-welle4 (Lane w182, freigegeben)
kanban_status: review
kanban_lane: review
kanban_summary: "The change-during-read guard's regression test aborts the capture because a mutation is PROVEN to have been observed…"
kanban_title: "Sources: the change-during-read guard must fail deterministically, not by timing (0.01s flake observed in CI)"
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-candidate-pack]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1387]
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/candidate-pack/round-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/snapshot-flake/round-1.md"]
---

- [ ] t-20261105-r27-snapshot-change-guard-deterministic · Sources: the change-during-read guard must fail deterministically, not by timing (0.01s flake observed in CI) #task #release/v0-4-27 #status/review #view/review #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w182, freigegeben) · **Priority:** high  
    **PR:** [baseharbor#1387](https://github.com/mcpdev80/baseharbor/pull/1387)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/candidate-pack/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/snapshot-flake/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-candidate-pack](t-20261018-r27-candidate-pack.md)  
**Owner:** coord-welle4 (Lane w182, freigegeben)  
**Priority:** high  
**PRs:** [baseharbor#1387](https://github.com/mcpdev80/baseharbor/pull/1387)  
**Source:** 
<!-- /generated:links -->

## Goal

The change-during-read guard's regression test aborts the capture because a mutation is PROVEN to have
been observed (hook/event), not because the writer happened to land between two reads. One CI minute can
produce both green and red for the same commit today; that poisons every other chain's gate.

## Measured flake (2026-11-05, coordinator-run evidence)

- Head `3bb95cc794` run 41981861515: terminal SUCCESS (all jobs).
- Same head, run 41983173186 ~20 min later: terminal FAILURE, sole failing test
  `--- FAIL: TestSourceSnapshotDetectsChangeDuringRead (0.01s)` in `internal/development`
  (guard assertion at source_snapshot_test.go ~215-226; writer goroutine + close(started)/release channels).

## Scope

- In scope: `internal/development` snapshot capture/guard + its test synchronization (deterministic hook
  in the capture path, test-side channel/event — the same pattern that retired sleep-polling in
  `t-20261018-r27-execution-journal`).
- Out of scope: the capture's public behavior, other candidate-pack tests, `.github`.

## Acceptance

- The guard test passes with `-race -count=50` (repeatable), and a mutation that disables the guard hook
  makes it RED deterministically (literal output, mutant commit named).
- The quiet-tree companion test (`...NoGuardAbortWhenQuiet`) keeps its guarantees (no abort on still tree).
- Red-first: the -race -count=50 instability shown on the pre-fix head (this card's flake evidence above
  counts as the red baseline; add one local reproduction if timing allows).

## Required checks

- go test ./internal/development -count=1 + race-count=50 of the two named tests, build, vet, gofmt;
  hosted runs of the exact head to terminal, PR Selected Checks not skipped.

## Runde 1 pruefbar 2026-11-05 (kopf fa4067e3f40)
Nachgemessen: ls-remote echt==head, develop 42bfcb1cb4 VORFAHR (frischer schnitt), genau ein eigener
commit, write-set = die zwei dateien der karte; race-50 wiederholbar gruen; quiet-begleiter gruen;
lauf 42010882741 terminal am exakten kopf. MUTANTEN-HINWEIS fuer die pruefung: einzellauf-rot ueber
deadlock der beobachtungs-naht (hook aus => test haengt bis timeout) — formal rot, die pruefung soll
bewerten ob ein SAUBERER assertiver fehler gefordert wird statt haenge-tod.

## Rueckruf (1387a REJECT, ein punkt): mutante haengt statt zu scheitern
Race-50 und quiet sind gruen, blobs unveraendert — aber die hook-aus-Mutante laeuft ins GENERISCHE
paket-timeout. Runde 2: test-seitige bounded wartestelle + typisiertes signal, fail-fast mit BENANNTEN
fehler als einziges mutanten-rot.

## Runde 2 pruefbar 2026-11-05 (kopf d5ff9bc7b599)
Nachgemessen: ls-remote echt==head, develop Vorfahr, eigene commits, write-set = die zwei karten-dateien;
fail-fast mutante mit benanntem sentinel (0,007s statt 10min-hang), race-50 + quiet-20 gemeldet gruen,
lauf 42026851319 terminal SUCCESS am exakten kopf, round-2.md auf main (ad9...). Die zeit-basierte
gruen/rueckfall-klasse der karte ist damit behoben — entpoisoned alle PR-tore.

## Kopf-Wechsel 2026-11-05 (17:4x): kandidat ist jetzt 27cf86c3396
Die fertige Lane hatte ihre Runden-Akte versehentlich ALS COMMIT ins Produkt-Repo gelegt (92958471) und
zusaetzlich einen zweiten PR #1389 auf demselben zweig geoeffnet — beide Regelbrueche von mir bereinigt:
Doppel-PR geschlossen (nachweis: gleicher zweig), content-only-fehlablage VORWAERTS zurueckgenommen
(revert 27cf86c3, loescht NUR .evidence/snapshot-flake/round-2.md; die akte liegt korrekt im plan-repo).
Code-identitaet zu d5ff9bc7 bleibt, gate-lauf am neuen kopf laeuft. Abnahme 1387b gilt dem neuen kopf.
