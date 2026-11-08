---
id: t-20261018-r27-maintenance-client
card_number: "0427-034"
card_short_title: "submit maintenance operations"
areas: [remote]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: lane-0427-034-maintenance-r6
kanban_lane: closed
kanban_summary: Route update/backup/restore/destroy through the selected authority and existing lifecycle/consent owners. Archive…
kanban_status: closed
kanban_title: "0427-034 · submit maintenance operations"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-client-commands, t-20261018-r27-state-recovery, t-20261022-r27-ci-runtime]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1428]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/commit/419b0211317bab63cb0fa66d07892488685d3ed8"]
wait_reason: ""

---

- [x] t-20261018-r27-maintenance-client · CLI: submit maintenance operations without workstation path assumptions #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/remote #kind/task
    <!-- generated:card -->
    **Owner:** lane-0427-034-maintenance-r6 · **Priority:** normal  
    **PR:** [baseharbor#1428](https://github.com/mcpdev80/baseharbor/pull/1428)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/419b0211317bab63cb0fa66d07892488685d3ed8)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-state-recovery](t-20261018-r27-state-recovery.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Required by:** [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261018-r27-team-proof](t-20261018-r27-team-proof.md)  
**Owner:** lane-0427-034-maintenance-r6  
**Priority:** normal  
**PRs:** [baseharbor#1428](https://github.com/mcpdev80/baseharbor/pull/1428)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Route update/backup/restore/destroy through the selected authority and existing lifecycle/consent owners. Archive upload/download and secret input references are explicit safe channels; a laptop filename is never interpreted as a server-local path. Preserve secret-safe machine behavior, recovery choices and typed double consent; lost response follows the same durable operation. Preserve existing Git/workspace source-acquisition ownership: a source snapshot is not a Git checkout; update must resolve/submit the intended next candidate, not run fetch against an invented server repository. Capability discovery rejects unsupported native maintenance explicitly; routing alone is not proof of remote backup support. No new backup engine or automatic replay.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

bounded remote-maintenance CLI adapters/tests; existing machine maintenance input records only after agreement with public-surfaces owner. No other task owns these files concurrently; shared command/contract registrations remain with public-surfaces.

## Required checks

Actual CLI->TLS API tests with different local/server filesystem roots, archive transfer integrity, safe secret input, denial/cancel/expiry and lost response; use fixtures, not full backup journeys. No automatic full matrix or self-approved trust exemption.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

PR#1428 head 2e371f5fc GELIEFERT aber NICHT review-ready: DRIFT (develop 812c99c88 nicht vorfahr) + SCHREIBSATZ-KOLLISION mit #110 (app_repository/app_workload_integration + repository_runtime_fixture = #110/#1383 owned) + CI 1-pending (lane geparkt ohne END, 4.6). korrektur dispatched: rebase + 3 dateien raus + CI terminal + END. karte active.

r2 drift-frei (head d4d0f77c0, develop 812c99c88 vorfahr), #110-collision behoben (delta nur 9 maintenance-dateien), CI run 42386457934 terminal success (9 pass, selbst beobachtet). CODEX-REVIEW. offene findings: public-surfaces-registrierung(1), kein .github-bedarf(2).

CODEX-REVIEW r1 = REQUEST-CHANGES (local destroy reihenfolge window<->authority, remote destroy laesst window weg, history-append verlust riskiert replay-kontinuitaet). frische korrektur-bahn fd89eda0 (orig lane freigegeben, kandidat von origin#1428 abgeholt). 3 punkte + causal mutants.

r2 alle 3 behebungen: destroy committet window ausbehaltener authority VOR teardown (local+remote), fail-closed history append mit rollback+capacity preflight. head a3416743b drift-frei (develop 06e4b1eaa), kollisionsfrei, delta nur maintenance_*, CI run 42395015763 terminal 9-pass, 6 gruen + last-bearing mutants. CODEX re-review.

RE-REVIEW r2 = REQUEST-CHANGES (2. bounce auf destroy-ablauf): (1) teardown loescht jetzt ein ZU-FRUEH vorgelegtes window, (2) failed destroy kann history-residue hinterlassen, (3) capacity preflight prueft ALTEN statt ZIEL-zustand. STRATEGIE-WECHSEL (3.6 zwei erfolgslose korrekturen): nicht weiter punktweise patchen — destroy als ATOMARE zustandsmaschine modellieren (commit->teardown->history-append als eine transaktionale folge) + eine table-driven regression ueber ALLE ausgaenge (success/failed-destroy/teardown-error). review act-1428-review.md origin/main bcf251f25. pool voll -> queue, bahn wenn sitz frei.

r3 (2.bounce destroy) mit STRATEGIE-WECHSEL: atomare zustandsmaschine (commit->teardown->append) + table-driven regression alle ausgaenge, statt punkt-patch. lane ea81397a busy. board: aktiver worker.

r3 endgueltig auf PR#1428 head 165405832: drift-frei, r3-vollstaendig (state-machine + round3-tests), CI TERMINAL 9-pass, evidence origin/main 31ee442c. lane stand zweimal ohne END (coord hat run-beobachtung uebernommen, dokumentiert); transport-notiz der lane: force-ausweich auf eigenem branch nach spurious up-to-date — befunl gering (eigener lane-branch), finaler sha gegen develop geprueft. CODEX-REVIEW.

r3 review REQUEST-CHANGES (3.bounce): stale destroy-tombstone (reload nach erfolg) + all-exit matrix fehlt — rezept liegt in act-1428-review.md section 'actionable recipe' auf origin/main 5eddad3b. r4 auf frischer laptop-lane 36e03dd3. karte active MIT worker.

r4 VOLL geliefert: head 39652986 auf PR#1428 (fast-forward, ls-remote bezeugt), CI run 42416537555 TERMINAL success auf finaler sha, drift-frei, delta nur maintenance-dateien. beide review-punkte behoben: commitiertes destroy-tombstone ohne reload (local+remote) + all-exit matrix 7 zeilen table-driven. CODEX-REVIEW.

r4 review REQUEST-CHANGES (4.bounce): retry-oracle invertiert + tombstone-replay pfad fehlt — beide mechanisch, rezept in act-1428-review.md. r5 auf laptop (52277f38). Eskalation an owner ankuendigt falls r5 erneut bounce auf gleichem thema.

r5 = prove-only widerspruch: beide r4-review-punkte seien in head 396529860e1f laengs implementiert; mutation-red-probes + datei:zeilen in round-5.md. KANDIDAT UNVERAENDERT. reviewer-recheck noetig: widerlegen (file:line repro) oder zuruecknehmen+approve.

r5-widerspruch durch reviewer-recheck ZURUECKGWIESEN (2 code-befunde: oracle invertiert/dupliziert + tombstone OHNE production-replay-reader). r6 auf flash (72cd7871). karte active. PRÄZEDENZ: 5 bounces — bei ratlos-frage sofort QUESTION, nicht raten.

r5-widerspruch durch reviewer-recheck ZURUECKGEWIESEN (oracle invertiert/dupliziert + tombstone ohne production-replay-reader). r6 auf flash 72cd7871. 5.bounce-praezedenz: ratlos => QUESTION, nicht raten.
