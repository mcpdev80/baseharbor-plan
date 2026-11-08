---
id: t-20261018-r27-node-streams
card_number: "0427-041"
card_short_title: "bound log replay and terminal"
areas: [connector]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: coord-welle5 (Lane w215, freigegeben)
kanban_lane: closed
kanban_summary: "Preserve existing logs/exec/PTY/metrics implementation; prove cursor expiry, at-least-once replay, stream limits/deadlines and…"
kanban_status: closed
kanban_title: "0427-041 · bound log replay and terminal"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-node-trust, t-20261022-r27-ci-runtime, t-20261105-r27-test-wire-helper]
repos: [mcpdev80/baseharbor-node-connector]
prs: [mcpdev80/baseharbor-node-connector#22]
sources: ["mcpdev80/baseharbor-node-connector#3"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-node-connector/pull/22"]
---

- [x] t-20261018-r27-node-streams · Connector: bound log replay and terminal cancellation #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/connector #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (Lane w215, freigegeben) · **Priority:** normal  
    **PR:** [baseharbor-node-connector#22](https://github.com/mcpdev80/baseharbor-node-connector/pull/22)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-node-connector/pull/22)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-node-trust](t-20261018-r27-node-trust.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md), [t-20261105-r27-test-wire-helper](t-20261105-r27-test-wire-helper.md)  
**Required by:** [nc-3](nc-3-core-enrollment-remote-runtime-acceptance.md), [t-20261018-r27-remote-podman-web](t-20261018-r27-remote-podman-web.md)  
**Owner:** coord-welle5 (Lane w215, freigegeben)  
**Priority:** normal  
**PRs:** [baseharbor-node-connector#22](https://github.com/mcpdev80/baseharbor-node-connector/pull/22)  
**Source:** [baseharbor-node-connector#3](https://github.com/mcpdev80/baseharbor-node-connector/issues/3)
<!-- /generated:links -->

## Outcome and acceptance

Preserve existing logs/exec/PTY/metrics implementation; prove cursor expiry, at-least-once replay, stream limits/deadlines and cancel. A disconnected PTY cannot resume another process; attribution and foreign resource protections retained.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

Connector internal/connector/target_access_stream.go stream_replay.go; internal/targetaccess/streams.go; component tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Focused stream/protocol tests plus one bounded real log/PTY smoke; no repeated full lifecycle. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Delivered 2026-11-05 (Lane w153) for Codex REVIEW. Four cases prove cursor expiry (loss-free replay), at-least-once resume at cursor boundary, terminal deadline clean end, and client cancellation with no ghost session — against the real `ServeLogStream` chain via the exported `targetaccess.NewHandshakePair` over a real `net.Pipe` mTLS line; chain driven through a fake `docker` on PATH, **no product code changed** (name-only). Required checks green locally; hosted CI on PR #22 observed to terminal (Test·Vet·Build + source SUCCESS; runtime matrix SKIPPED). Evidence: round-2.md.

First push landed on the helper branch `work/r27-test-wire-helper` (97d7fe7) by a dispatch/context error, not a content defect; the identical one-file diff was re-delivered on `work/r27-node-streams` (6b498a8, cherry-pick of 97d7fe7, byte-identical diff). PR #22 is a draft until Maintainer acceptance; acceptance/merge is the Maintainer's (or owner-delegated Codex MERGE) decision — no self-qualification.

## Review-Rueckruf 2026-11-05 (review-22a REJECT, vier punktgenaue Rezepte)
Fall A prueba nie echten Ablauffall (Cursor nie aelter als die Vorhaltung), Fall C lasst jedes fruehe Ende
als Frist-Ende durch, Fall D kann vor der beobachteten Abmeldung gewinnen, Fall B zaehlt nicht auf die Zeile.
Runde 2 macht aus den Adjektiven Zahlen: echte Retention-Grenze, erwartetes StreamEnd, synchroner Abbruch,
exakte Folgen-/Zeilensaehlung — plus Mutations-Gegenproben im Belegstil der Pruefung.

## Runde 2 pruefbar 2026-11-05 (kopf d934fa7c522)
Nach der Lauf-Rueckfrage geliefert: fehlerhafter Stand ersetzt, zwei laeufe am neuen kopf terminal
erfolgreich (von mir abgerufen). Fall-D-Abbau-Rennlauf behoben; alle vier faelle an der echten leitung.

## Rueckruf 2026-11-05 (22b REJECT: 2 von 4 mutanten nicht rot)
Faelle A+B bestehen; C laesst fruehes Ende durch, D prueft die dokumentierte Ablehnung der Wiederaufnahme
nicht. Runde 3 = genau diese zwei punkte + zwei neue Mutantenproben; END nur mit abgerufenem gruenem Lauf.

## Runde 3 pruefbar 2026-11-05 (kopf dc63758f37)
Nachgemessen: ls-remote echt==head, main Vorfahr, vier eigene commits, write-set internal/connector+execx,
trust/session-blobs unveraendert; laeufe 41989934411+41989934361 terminal SUCCESS am exakten kopf. Fall C
frist-ende brueht (mutante rot), fall D cursor-ablauf-weisung mit frischer importierter handshake-leitung
(alter weg removed, ghost mutante rot). Akte round-3.md publiziert (1d52f32).

## Rueckruf (22c REJECT, vier punkte): A/B umgehen die echte Kette
A und B rufen den replay-Helfer DIREKT statt ueber frische NewHandshakePair+ServeLogStream; D wartet das
natuerliche Terminal ab statt frueh ab zubrechen; execx/executor.go liegt ausserhalb der Write-Reservierung
(zurueck oder begruenden); und der kartengeforderte begrenzte ECHTE log/PTY-SMOKE fehlt bisher ganz.

## Runde 4 pruefbar 2026-11-05 (kopf cce09a86a59)
Nachgemessen: ls-remote echt==head, main Vorfahr, zwei laeufe (42039130963+42039130973) terminal SUCCESS am
exakten kopf, round-4.md auf main. Lane-Meldung: faelle A/B jetzt ueber die ECHTE kette, fall D abbruch vor
natuerlichem terminal, harness-only determinismus-fix (fake docker CWD-dicht, invoke-log je harness in
t.TempDir — nie wieder /tmp/w160-inv.log), execx-angelegeneit laut akte behandelt. Mutanten- und
smoke-zeilen in der akte; blobs obliegt der pruefung.

## Rueckruf (22d REJECT, pane-transkribiert): A/B weiterhin helper-direct
Dritte runde fuers selbe rezept-punkt: wiederablauf- und frist-assertions rufen streams.replay DIREKT
(grep-zeilen 615/627/701 am kopf); die vier mutanten sind OFFEN (prueferin-sandbox fehlgeschlagen, nicht
bestanden). Runde 5: NewHandshakePair+ServeLogStream fuer A+B wie C+D, mutanten einzellauf wörtlich,
gemischtes race-20 ensemble, connector-main-merge.

## Runde 5 pruefbar 2026-11-05 (kopf 52db6dc1c64)
Nachgemessen: ls-remote echt==head, main Vorfahr, laeufe 42058515798+42058515839 terminal SUCCESS am
exakten kopf (DIESE ids massgeblich — die END-zeile nannte andere, nicht existierende nummern; akte
entsprechend zu berichtigen gilt der messung, nicht der meldung). Helper-direct-calls NULL (grep), vier
mutanten rot, zusammenbau echt. round-5.md auf main.

## Rueckruf (22e REJECT, ein punkt nach urteil): case A resumt erst nach terminalem ende —\nstill-attached-guard ohne rot-werdenden mutant bewiesen. Umbau: live-follow + barre + exakte ablehnung.\nKette/ensemble/laeufe waren gut.

## Runde 6 pruefbar 2026-11-06 (kopf 25a24667ebf, repo node-connector)
Nachgemessen: ls-remote echt==head, main VORFAHR (rc=0), laeufe 42146364305+42146364376 BEIDE TERMINAL
SUCCESS am exakten kopf, akte round-6.md auf origin/main. Case-A live+barriere, guard-mutante dreht A
benannt ROT (B/C/D gruen), race20 ensemble gruen 1319.7s, harness-hang (net.Pipe-park) diagonal geheilt.

## Rueckruf (22f REJECT, 22e war durch): BLOCKING — kind-Fehler werden als sauberer strom-end
(io.EOF) gemeldet statt als fehler. Rezept in review-22f.md zeilen 77ff/106ff: io.EOF nur bei context-
abbruch; echte kindfehler durchreichen + neue zelle beide richtungen + echte mutante.

## Runde 7 pruefbar 2026-11-06 (kopf 2e285a771ed, repo node-connector)
Nachgemessen: ls-remote echt==head, main VORFAHR rc=0, BEIDE laeufe 42159456055+42159456071 TERMINAL
SUCCESS am exakten kopf, akte round-7.md auf origin/main, root-checkout geraeumt (coord-nachmessung: 0
aenderungen — umzug vollzogen). Kindfehler => streamError statt EOF (isContextKilled grenzt ctx-kill ab,
EOF bleibt dort), Case E beide richtungen, mutante echt rot + gegenprobe, race20 gruen.

## ACCEPT 2026-11-06 (22g): merge UNTERWEGS (kopf 2e285a771ed); schliesst bei main-beleg.

## Gemerged 2026-11-06 (CODEX-MERGE nach 22g ACCEPT): kopf 2e285a771ed, connector-main
7fb235dd2f6. Kindfehler meldet jetzt fehler statt sauberem strom-end; EOF nur bei context-abbruch.
