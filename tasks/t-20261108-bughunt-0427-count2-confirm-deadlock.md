---
id: t-20261108-bughunt-0427-count2-confirm-deadlock
card_number: "0427-135"
card_short_title: "Wiederholtest hängt (count=2)"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w135-count2
kanban_status: active
kanban_lane: active
kanban_summary: Ein sauberer go test -count=2 (ohne ambient Core) endet terminierend statt zu blockieren; der Bestätigungspfad leaket keine…
kanban_title: "0427-135 · Wiederholtest hängt (count=2)"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-07/compose-host-isolation/round-9.md"]
---
- [ ] t-20261108-bughunt-0427-count2-confirm-deadlock · Bug Hunt v0.4.27: Wiederholtest-Hänger im Bestätigungspfad #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w135-count2 · **Priority:** normal  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-07/compose-host-isolation/round-9.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w135-count2  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Ein sauberer `go test -count=2` (ohne ambient Core) endet terminierend statt zu blockieren; der Bestätigungspfad leaket keine pipe-haltende Goroutine. Regression im CI-erfassten Pfad.

## Problem (Fund aus Compose-Akzeptanz, Runde 9, F1)
`recordDeploymentBeforeMutation` (cmd/baha deployment_record :551, consent==nil-Zweig) hinterlässt auf einem tatsächlich sauberen Host einen Goroutine, der eine Pipe hält — `go test` terminiert nie, `-count=2` blockiert. Kontaminiertes Bild (ambient Core löst confirm) ist grün; `-count=1` auf frischen Runnern ist grün => CI fing es nie. Transkripte: /tmp/c2-matrix.out (Lane 0427-110).

## Acceptance
- Deterministischer Repro (count=2, sauberer host) als test oder dokumentierter CI-pfad; Fix im confirm-retry lifecycle; keine leakende goroutine nach fehlgeschlagenem/abgebrochenem confirm.

## Dependencies and file ownership
Keine. Write-set: cmd/baha (deployment_record/confirm lifecycle) + tests.

## Resolution (dropped 2026-11-08)
Not a product defect. Triple-negative reproduction: develop 07ae6c3e9 and the compose WIP head e291fba9a both terminate under clean `-count=2`; SIGQUIT dumps show no pipe-waiting goroutine. The original hang witness came from invalidated FIFO cells plus ambient load on the compose host (round-1.md details). No product change, no PR.
