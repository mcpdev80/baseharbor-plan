---
id: t-20261105-r27-snapshot-change-guard-deterministic
card_number: "0427-112"
card_short_title: "the change-during-read guard"
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: ""
owner: coord-welle5 (Lane w223, freigegeben)
kanban_status: closed
kanban_lane: closed
kanban_summary: "The change-during-read guard's regression test aborts the capture because a mutation is PROVEN to have been observed…"
kanban_title: "0427-112 · the change-during-read guard"
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-candidate-pack]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1387, mcpdev80/baseharbor#1400]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/candidate-pack/round-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/snapshot-flake/round-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/snapshot-flake/round-4.md", "https://github.com/mcpdev80/baseharbor/pull/1387", "https://github.com/mcpdev80/baseharbor/pull/1400"]
---

- [x] t-20261105-r27-snapshot-change-guard-deterministic · Sources: the change-during-read guard must fail deterministically, not by timing (0.01s flake observed in CI) #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (Lane w223, freigegeben) · **Priority:** high  
    **PR:** [baseharbor#1387](https://github.com/mcpdev80/baseharbor/pull/1387), [baseharbor#1400](https://github.com/mcpdev80/baseharbor/pull/1400)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/candidate-pack/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/snapshot-flake/round-1.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/snapshot-flake/round-4.md), [proof 4](https://github.com/mcpdev80/baseharbor/pull/1387), [proof 5](https://github.com/mcpdev80/baseharbor/pull/1400)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-candidate-pack](t-20261018-r27-candidate-pack.md)  
**Owner:** coord-welle5 (Lane w223, freigegeben)  
**Priority:** high  
**PRs:** [baseharbor#1387](https://github.com/mcpdev80/baseharbor/pull/1387), [baseharbor#1400](https://github.com/mcpdev80/baseharbor/pull/1400)  
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

## Rueckruf 2026-11-05: der fixed guard ist auf GEHOSTETEM lauf ROT — nicht mehr per timing, per EIGENER schranke
lauf 42050483534 am kopf 27cf86c3396 (docs-bereinigung, code=d5ff9bc): '--- FAIL: TestSourceSnapshotDetectsChangeDuringRead (5.01s)'
= die neue 5s-SENTINEL grenze laeuft auf, der hook wird auf dem CI-dateisystem/unter last NICHT FEUERBAR
beobachtet (mtime-delta-beweis trift dort nicht ein). Lunas BLOCKED-urteil war richtig: die historischen
belege zaehlen nicht gegen diesen realen ausfall. Runde 3: nachweis-BARRE statt mtime-hoffnung (dieselbe
klasse wie tagebuch: ereignis-naht, die den wechsel BEWEIST — nicht 'mtime hat sich seit walk-start
geaendert'), danach race50 + einzellauf-mutante + NEUER hosted lauf bis terminal.

## Runde 3 pruefbar 2026-11-05 (kopf e2d87906a510)
Nachgemessen: ls-remote echt==head, GEHOSTETER lauf 42057573429 terminal SUCCESS am exakten kopf
(go-unit-tests + selected checks gruen — das war die neue Annahme-Klausel), race50 gruen, quiet20 gruen,
einzellauf-mutante 3x rot mit benanntem sentinel; EREIGNIS-barre im Produktionslauf (kein test-schalter).
Ketihenbereinigung dokumentiert (reset auf 27cf86c + ein commit + develop-merge a53c10a7, ancestor rc=0;
develop ist seitdem auf 10e8d646 weitergelaufen = merge-zweig-notiz). round-3.md auf main.

## Rueckruf (1387c REJECT, ein punkt): schluss-verifizierung der baseline-pfade muss wieder rein — ereignis-barre bleibt, verteidigung-in-tiefe. mission w189 fertig.

round-4: defense in depth. EREIGNIS barrier fixed to real os.Lstat mid-walk re-stat (root cause of round-3 flake); final baseline-path verification restored as Layer 2; late-mutation regression pinned. Hosted 42083071514 @ d21badc6 terminal SUCCESS (PR Selected Checks green).

round-4: defense in depth. EREIGNIS barrier fixed to real os.Lstat mid-walk re-stat (root cause of round-3 flake); final baseline-path verification restored as Layer 2; late-mutation regression pinned. Hosted 42083071514 @ d21badc6 terminal SUCCESS (PR Selected Checks green).

round-4 (w189): defense in depth. EREIGNIS barrier fixed to real os.Lstat mid-walk re-stat (root cause of round-3 flake); final baseline-path verification restored as Layer 2; late-mutation regression pinned deterministically. Hosted 42083071514 @ d21badc6 terminal SUCCESS (PR Selected Checks green). Evidence: round-4.md.

round-4 (w189): defense in depth. EREIGNIS barrier fixed to real os.Lstat mid-walk re-stat (root cause of round-3 flake); final baseline-path verification restored as Layer 2; late-mutation regression pinned deterministically. Hosted 42083071514 @ d21badc6 terminal SUCCESS (PR Selected Checks green). Evidence: round-4.md.

## Runde 4 pruefbar 2026-11-05 (kopf d21badc6f4): WARMEURSACHE gefunden und benannt — die ereignis-barre\nverglich ein totes entry.Info() statt echter Lstat-inspektion mitten im lauf (das war der runde-3-rest-flake).\nEndcheck (verifyFinalBaseline) wieder drin; race50+quiet20 gruen, beide mutanten benannt rot, hosted am kopf.\n1387c-punkt damit adressiert + tiefer. round-4.md auf main.

## Rueckruf (1387d REJECT, ein punkt nach urteil): race-verzahnung der late-mutation fehlt —\nendcheck-entfernt-mutante blieb GRUEN (test prueft endcheck nicht). lstat + beide schutzschichten bleiben.\nWahrheit zur kette: runde 4 brachte die WARMEURSACHE (totes entry.Info) und endcheck-rueckkehr; die\nbarre-mutante ist rot, die endcheck-mutante war's noch nicht.

## Runde 5 pruefbar 2026-11-05 (kopf 0298871895c1)
Nachgemessen: ls-remote echt==head, develop 3d8fc207 VORFAHR (rc=0, beide attestate in der akte), lauf
42106254196 TERMINAL SUCCESS am exakten kopf, akte round-5.md auf main. END-zeile der lane nannte
veraltet den zwischenkopf 07108f0847 — messe gilt (praeszedenz w185). Beide mutanten benannt rot, race50+
quiet20 gruen, wahre ursache (totes entry.Info) behoben, endcheck wieder drin.

## Rueckruf (1387e REJECT, ein punkt): die late-mutation-barre ist einseitig — der writer startet zwar
per channel, aber es gibt KEIN WRITE-ACK: der test beweißt nicht, dass die änderung ANGEKOMMEN ist, bevor
capture weiterläuft. Darum wird die endcheck-mutante auch ohne echte dateiänderung rot (nicht-diskriminierend).
Rezept: beidseitige barre + identitätsnachweis der geschriebenen datei.

## Runde 6 pruefbar 2026-11-06 (kopf d0e0bdc6e84)
Nachgemessen: ls-remote echt==head, develop VORFAHR, lauf 42125295757 TERMINAL SUCCESS am exakten kopf,
akte round-6.md auf main. 1387e-punkt geschlossen: BEIDSEITIGE write-ACK-barre, beide richtungen ROT mit
sentinel, GEGENPROBE ohne mutation GRUEN (diskriminierung bewiesen), race-50 gruen.

## ACCEPT 2026-11-06 (1387f): merge UNTERWEGS inkl. geräte-ketten-retry; karte bleibt review bis develop-beleg da ist.

## Gemerged 2026-11-06 (1387f ACCEPT, kette): der sechste anlauf heilt den chronischen
 timing-flake (wahre ursache: totes entry.Info(); beidseitige write-ack-barre + gegenprobe). Seit merge
 KEIN flake-rot mehr in den nachfolgenden ketten beobachtet (1394 merge lief GRUEN durch — praxisbeweis).

## Runde 7 noetig (w207-befund, nicht journal-defekt): am integrationskopf efa1600c lokal 4+2 gruen,
GEHOSTET twice TERMINAL ROT an :247 'MutationAcked never fired' — der ack-wait haelt einem ZEITLIMIT unter
runner-last, nicht einer kausalen barre. Mission w209-flake-r7 steht; journal-#1393-merge wartet darauf.

## Runde 7 pruefbar 2026-11-06 (kopf 1c84f5fe43c, PR #1400)
Nachgemessen: ls-remote echt==head, develop VORFAHR rc=0, ZWEI terminale GRUEN-Beobachtungen am selben
kopf (lauf 42172734295 + Attempt-2-rerun, job 127749031811), akte round-7.md auf origin/main (coord-record
aus publish-zweig der lane, merge-uebernahme). Kausale ack-barriere statt zeitlimit; nil-pforte drin;
fremder validate-befund (4 compose/workload-zellen) separat dokumentiert -> compose-karten-notiz.

## Rueckruf (1400a REJECT, zwei punkte): (1) NIL-HOOK ueberschreibt frischen Lstat-wert =>
Layer-1-beobachtung fuer default-produktionsoptionen AUS — regressionzelle gefordert; (2) develop nicht
VORFAHR des kopfes. Alt-laefe zaehlen nicht mehr. Rezept 44-61.
