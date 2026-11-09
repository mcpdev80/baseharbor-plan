---
id: t-20261018-r27-journal-wiring
card_number: "0427-031"
card_short_title: "reconnect and reconcile"
areas: [remote]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle5 (w235, entlassen)
kanban_lane: closed
kanban_summary: Wire durable operation IDs into actual submit/poll/events and lifecycle correlation. Lost response does not submit again; server…
kanban_status: closed
kanban_title: "0427-031 · reconnect and reconcile"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-execution-journal, t-20261018-r27-mutation-lock, t-20261022-r27-ci-authority]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1393, mcpdev80/baseharbor#1392]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-2026-11-05/journal-wiring/round-1.md", "https://github.com/mcpdev80/baseharbor/pull/1393", "https://github.com/mcpdev80/baseharbor/actions/runs/42101103524"]
blocker: ""

---

- [x] t-20261018-r27-journal-wiring · Operations: reconnect and reconcile interrupted executions #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/remote #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (w235, entlassen) · **Priority:** normal  
    **PR:** [baseharbor#1393](https://github.com/mcpdev80/baseharbor/pull/1393), [baseharbor#1392](https://github.com/mcpdev80/baseharbor/pull/1392)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-2026-11-05/journal-wiring/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1393), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/42101103524)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-execution-journal](t-20261018-r27-execution-journal.md), [t-20261018-r27-mutation-lock](t-20261018-r27-mutation-lock.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md)  
**Required by:** [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-management-host](t-20261018-r27-management-host.md), [t-20261018-r27-remote-rollout](t-20261018-r27-remote-rollout.md), [t-20261018-r27-state-recovery](t-20261018-r27-state-recovery.md)  
**Owner:** coord-welle5 (w235, entlassen)  
**Priority:** normal  
**PRs:** [baseharbor#1393](https://github.com/mcpdev80/baseharbor/pull/1393), [baseharbor#1392](https://github.com/mcpdev80/baseharbor/pull/1392)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Wire durable operation IDs into actual submit/poll/events and lifecycle correlation. Lost response does not submit again; server restart marks interrupted work uncertain and observes owned state before any explicit retry. Actor-scoped reads, expiry/cancel semantics and bounded event cursor behavior survive reconnect; destructive approval is never replayed.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

internal/machinehttp/handler.go; streams.go; request.go; corresponding journal integration tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Actual HTTP handler restart/lost-response/event-cursor integration with fake bounded executor and durable store; targeted lifecycle tests. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

round 1 candidate PR #1392 head 3a5ce89011, hosted CI 42097435724 green (go-build/vet/unit-tests), evidence round-1.md

round 1 candidate PR #1392 head 3a5ce89011, hosted CI 42097435724 green (go-build/vet/unit-tests), evidence round-1.md

round 1 candidate; PR #1392 head 3a5ce89011; hosted CI 42097435724 green; evidence round-1.md

round 1 candidate; PR #1392 head 3a5ce89011; hosted CI 42097435724 green (go-build/vet/unit-tests); evidence round-1.md

round 1 candidate; PR #1392 head 3a5ce89011; hosted CI 42097435724 green; evidence round-1.md

## Runde 1 pruefbar 2026-11-05 (kopf 3fa46bc299b)
Nachgemessen: ls-remote echt==head, develop 3d8fc207de VORFAHR (rc=0 nach korrektur-runde), gehosteter
lauf 42101103524 TERMINAL SUCCESS am exakten kopf, akte round-1.md auf main. Produktion=echter
anwendungs-pfad, crash-wiederanlauf gruen, zweiprozess-ordnung gruen, beide mutanten rot.

## Befund doppel-PR: lane legte nach korrektur einen zweiten PR an (#1393), gh schloss #1392 automatisch.
Ein kandidat, ein zweig 3fa46bc299b — PR-verweis berichtigt, doppelanlegung als feier notiert (wiederholung
=> rotationsrunde).

## Rueckruf (1392a REJECT): crash-Zellen laufen NICHT durch die echte HTTP-handleExecute-naht mit
abgebrochenem kindprozess, und mutante A oeffnet nur einen unabhaengigen leeren temp-root (beweist nichts).
Rezept in review-1392a.md zeile 27ff. Scope/write-set waren gut.

## Runde 2 pruefbar 2026-11-05 (kopf ecae5f0d877)
Nachgemessen: ls-remote echt==head, develop VORFAHR, lauf 42116653735 TERMINAL SUCCESS am exakten kopf,
akte round-2.md auf main (commits b5fb91a+c0119f4). 1392a-punkte alle gesetzt: echte handleExecute-naht mit
kindprozess-SIGKILL, zweiprozess-ordnung, mutanten 2/2 ROT woertlich.

## Rueckruf (1393a REJECT, zwei punkte): (1) die 'zwei prozesse' zelle laeuft SERIELL (wartet prozess1
zu ende) statt gleichzeitig am selben persistenten journal; (2) mutante B editiert eine IN-MEMORY-slice statt
echtem write-verlust. Produktionsnaht+crash+remote waren BESTAETIGT. Rezept ab zeile 'Change' in review-1393a.md.

## Runde 3 pruefbar 2026-11-06 (kopf 67efc581614)
Nachgemessen: ls-remote echt==head, lauf 42130410241 TERMINAL SUCCESS am kopf, akte round-3.md auf main.
Basis: enthaelt develop a0441838de (flake-kur drin), die 6 develop-schritte DER NAECHSTEN merge-stufe
(geraete-kette) noch nicht — praeszedenz 1394: basisabgleich ist STUFE der merge-mission, konflikt in
machinehttp-/journal-dateien => STOP+MELDEN. 1393a-punkte beide geschlossen: echte gleichzeitigkeit (barriere)
+ mutante B auf echtem pfad, gegenprobe gruen.

## ACCEPT 2026-11-06 (1393b): merge-MISION UNTERWEGS (SHA 67efc581614a); schliesst bei develop-beleg.

## Rueckruf 2026-11-06 (merge-block, ECHTER DEFKT — kein flake): develop-merge-integration
efa1600c7537 faellt TERMINAL + rerun: TestSourceSnapshotDetectsChangeDuringRead :247 'MutationAcked never
fired on the mutated path' — die journal-verdrahtung stoert die neue write-ack-barre der geheilten kur
(zeitlicher/eingriffseffekt im production-walk). Die kur selbst funktioniert: sie faengt genau diesen fall.
Merge bleibt block bis gruen; PR #1393 offener kanditat auf gleichem zweig.

## Stand r4 (w207): write-set eigen 10x race gruen, coexist mit kur lokal gruen; GEHOSTET blockiert
durch kur-r7-rest (zeitlimitscher ack-wait, nicht dieser zweig). Merge wartet kur-r7.

## r4 END verifiziert 2026-11-06: head efa1600c7537 ls-remote echt, akte round-4.md auf main,
write-set eigen 10x race gruen, coexist belegt, CI-zeile woertlich. Lane freigegeben. Merge #1393 wartet
ausschliesslich kur-r7 (kausal-barriere, laeuft jetzt auf ihrem sitz).
