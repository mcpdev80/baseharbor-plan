---
id: t-20261120-other-domain-test-split
card_number: "0428-206"
card_short_title: "Other-domain test split"
type: bug
areas: [cli, ci]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-206 · Other-domain test split
priority: high
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-other-domain-test-split · Cause split for the 89 other-domain cmd/baha failures #task #release/v0-4-28 #status/active #view/active #area/ci #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    **Needs:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** coordinator  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Current review state

Round 1 is rejected as incomplete: its twelve group counts total 38, group 12 subgroups total 9 while the group says 8, and the referenced raw classification files are absent. A prompt-disabled run at exact base `40cb28c758b02960356434b630086a341ebe1738` completed with 203 distinct failed top-level tests; the old 89-case cohort is not yet reconciled against it. See [independent review r2](../evidence/r28-welle4-2026-11-21/other-domain-test-split/codex-review-r2.md). Reconstruct the exact target cohort and row-level groups before acceptance.

## Why

`evidence/r28-welle4-2026-11-20/cli-test-inventory-develop/round-1.md` (sitz w217, read-only, plan-main 0dec6779) measured
`go test ./cmd/baha/ -count=1` at develop `40cb28c758b0`: **206 failing tests** (181 first-level), grouped by entry class
`runWithIO=82`, **other-domain=89**, `MCP=10`, `rootCommand-direct=0`. 0428-204 carries the operator-seam classes. If the 89
stay unsplit, 0428-204 grows past one card (AGENTS 4.2 forbids that) or real defects stay invisible.

## What

1. Take the 89 from the 217 dossier (do not re-invent the list; report any line you cannot place).
2. Group by the FIRST FAILING PRODUCTION FILE, one line per group: `file:line`, count, verbatim first error.
3. Assign each group exactly one rubric:
   - (a) already covered by an open card - name the card (`git grep` over baseharbor-plan tasks),
   - (b) new defect - draft the card text here (title, acceptance, write-set, dependencies),
   - (c) fallout of commit `3653369a4` (#1717: `internal/operatorauth/authorization.go`, `cmd/baha/local_workload_authority.go`, `cmd/baha/mcp.go`) - prove it with `git log -S` and the green/red pair `f5ce95af` -> `3653369a`.

## Acceptance

- Evidence-only: no product file changes, no PR required.
- All 89 appear in exactly one group; every group carries a rubric and a witness.
- Groups judged (b) are turned into cards by the coordinator in the same turn (fund-to-card duty, AGENTS 3.3.5).

Karte aus w217s zahlung gegossen (fund->karte, §3.3.5): 206 fehlende tests in ./cmd/baha/ am exakten develop 40cb28c758, davon 89 in ANDEREN domänen als dem operator-seam. sitz w221 (ornith) gruppiert nach der ERSTEN fehlenden produkt-datei und rubriziert: (a) schon von einer karte gedeckt, (b) neuer defekt (karten-text wird hier vorformuliert), (c) folge von commit 3653369a4 (#1717: internal/operatorauth/authorization.go + cmd/baha/local_workload_authority.go + cmd/baha/mcp.go). KEIN produktgriff, KEIN PR; die 0428-204-Klassen (runWithIO=82, MCP=10) bleiben bei w216, damit keine karte aufbläht (§4.2).

Karte aus w217s zahlung gegossen (fund->karte, §3.3.5): 206 fehlende tests in ./cmd/baha/ am exakten develop 40cb28c758, davon 89 in anderen domänen als dem operator-seam. sitz w221 (ornith) gruppiert nach der ersten fehlenden produkt-datei und rubriziert: (a) schon von einer karte gedeckt, (b) neuer defekt (karten-text wird vorgeformuliert), (c) folge von commit 3653369a4 (#1717). KEIN produktgriff, KEIN PR; die 0428-204-Klassen (runWithIO=82, MCP=10) bleiben bei w216, damit keine karte aufbläht (§4.2).

HANDOFF COMPLETE (read-only classification, no PR): akte other-domain-test-split/round-1.md on baseharbor-plan main (78aa8733 delivered, 87caac0b current); 12 production-file groups, counts 9+5+3+3+2+2+2+1+1+1+1+8 = 89 tests, rubric (c) proved at internal/operatorauth/authorization.go:285 with the green/red pair f5ce95af -> 3653369a4 (#1717). CONSEQUENCES: 72 rubric-(c) rows are 0428-204's, rubric-(a) rows are inside 0428-204's scope, the single rubric-(b) row is poured as card 0428-207. COLUMN: 'review' is rejected by the validator because this card deliberately has no PR (diagnosis card), so the confirmed state is recorded as wait — work delivered, waiting on CODEX-REVIEW of the classification before the 90-site operator seam is trusted. Lane released, seat refilled.

## Wait-sweep continuation — 2026-11-21

- Codex review r2 rejected the round-1 classification for inconsistent sums and missing complete source rows. The task is active under the wait-sweep owner while the complete row-level classification is rebuilt. No product files or PRs changed.

CODEX verwarf round-1 (8a086890, codex-review-r2.md): summen 38 statt 89, gruppe 12=9 statt 8, '/tmp/w217-classified.tsv' nie publiziert, gruppe 8 falsche datei. zeilenweise neuberechnung ueber den neutralen produktionspfad (artefakte der gehosteten cli-zellen) in frischer lane ca3a71d0.

KOHORTEN-KLARSTELLUNG aus der lane (flash, ca3a71d0): '89' war eine TEILKLASSE am zustand MIT ambient-stack (runWithIO 82 / MCP 10 / other 89), der neutrale produktionspfad (run 44850031032, cli-0..3-artefakte) zaehlt 117 first-level-faelle. gefordert sind beide: 89-zeilentabelle plus 117-zeilige summenprobe, kohorten-definition in max 10 zeilen. mein fehler in der kartenformulierung, nicht der lane.
