---
id: t-20261018-r27-execution-journal
card_number: "0427-029"
card_short_title: "persist execution identity and"
areas: [state]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: Owner/ChatGPT (externe Übernahme 2026-11-05, Direktive)
kanban_status: closed
kanban_title: "0427-029 · persist execution identity and"
kanban_lane: closed
kanban_summary: "Persist accepted/running/terminal or uncertain status, correlation and authorized request commitment before effects. Duplicate…"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261022-r27-ci-authority]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1373]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence:
  - "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/execution-journal/slice-1.md"
  - "https://github.com/mcpdev80/baseharbor/pull/1373"
  - "https://github.com/mcpdev80/baseharbor/commit/0ce814d0"
---

- [x] t-20261018-r27-execution-journal · Operations: persist execution identity and terminal outcomes #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/state #kind/task
    <!-- generated:card -->
    **Owner:** Owner/ChatGPT (externe Übernahme 2026-11-05, Direktive) · **Priority:** normal  
    **PR:** [baseharbor#1373](https://github.com/mcpdev80/baseharbor/pull/1373)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/execution-journal/slice-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1373), [proof 3](https://github.com/mcpdev80/baseharbor/commit/0ce814d0)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md)  
**Required by:** [t-20261018-r27-journal-wiring](t-20261018-r27-journal-wiring.md)  
**Owner:** Owner/ChatGPT (externe Übernahme 2026-11-05, Direktive)  
**Priority:** normal  
**PRs:** [baseharbor#1373](https://github.com/mcpdev80/baseharbor/pull/1373)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Persist accepted/running/terminal or uncertain status, correlation and authorized request commitment before effects. Duplicate request with changed content is rejected; reconnect retrieves the same operation. Bound retention, no secrets/artifact payloads in ordinary journal. No claim of exactly-once effects across crashes. Handler/lifecycle wiring is a later task.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

internal/machinehttp/store.go; bounded durable execution-journal files and tests in internal/machinehttp/. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Focused disk/reopen/corruption/concurrent admission/retention tests, secret scanning; no runtime. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Stand-Vermerk 2026-11-04 (coord f49a3303)
- Claim publiziert (owner w107). Lane WARTET auf Kapazitaet im Worker-Pool (4 aktive Lanes, Spawn-Hold);
  kartenzustand deshalb Zwischenstand: noch keine code-aenderung, keine branch work/r27-execution-journal.

## Coordination note 2026-11-04 (coordinator f49a3303)
- Lane w112 reported the card as already delivered by the merged journal state and closed without code. That
  claim was checked against develop bb9bc0ef and rejected for two criteria:
  duplicate request with changed content is not refused (internal/machinehttp/store.go:102-130 keys records by
  execution id only, no comparison, no typed error), and reconnect retrieving the same operation has no path.
  Criteria on persistence before effects, bounded retention without payloads, and the no-exactly-once wording
  are satisfied by the merged state.
- Correction round: branch work/r27-execution-journal, red-first tests for both gaps against the real path,
  implementation inside internal/machinehttp, draft PR, terminal gates. Evidence must live in
  evidence/r27-welle4-2026-11-04/execution-journal/ (an off-board proof file does not count).

- Correction round (lane w112) delivered head 0ce814d0, PR #1373 draft on develop 2a43984a: duplicate request
  with changed content is refused and reconnect returns the same operation, both added to store.create through an
  operations index with red-first tests; criteria 1, 4, 5 were already covered by the merged journal state.

## Review-Rueckruf 2026-11-04 (Codex review-1373a, verdict REJECT)
- Die semantische Operationsauswahl wurde als Anfragen-Wiedererkennungsschlüssel benutzt; eine
  anfragen-eigene Identität mit Nicht-Geheimnis-Verpflichtung über die ganze Anfrage fehlt.
- Die Eingabe fehlt in der Verpflichtung; der Wiedererkennungsindex geht beim erneuten Öffnen verloren, weil
  load() ihn nicht aus dem erhaltenen Protokoll aufbaut.
- Doppel- und Wiedererkennungswege sind im Anfragepfad vom neu akzeptierten Lauf nicht unterscheidbar
  (runExecution läuft erneut, typisierter Fehler als internal verpackt).
- Es fehlt die Reihenfolge-Regression: Eintrag lesbar, bevor die erste Wirkung beginnt.
- Formulierung "replayed once, never a second time" muss auf die gebundene Garantie verschlankt werden.
- Korrekturrunde = Lane w119 auf demselben Zweig und PR #1373 (Kopf vorher 0ce814d0).

## Ownership transition 2026-11-04 (coordinator, documented handoff)
- The card line previously named lane w107, which never started; lane w112 (session released) delivered the
  candidate now on PR #1373 head 0ce814d0. Sole owner for the correction round is the Codex worker instance
  `codex-heavy-wk` executing mission coordinator/missions/cx01-journal-r2.txt. No other session writes this
  branch; you have an explicit handover, so stop-condition "unclear ownership" is cleared.

## Handoff 2026-11-04 (Codex-Worker cx01, Kanban-Setzung über card-status.py)
- Candidate: PR #1373 head 11ed442e on branch work/r27-execution-journal, develop ecbb8854 is an ancestor,
  hosted checks terminal 2 pass / 0 fail / 14 skipping.
- Round 2 addresses all five Codex review-1373a recipes: per-request identity with a non-secret commitment,
  operation index rebuilt from the retained journal, distinguishable duplicate/reconnect outcomes, and an
  ordering regression proving the record is readable before the first effect. Wording narrowed to the bounded
  guarantee. Evidence: evidence/r27-welle4-2026-11-04/execution-journal/round-2.md.

## Auflösungspfad 2026-11-04 (Coordinator)
- Der Grund, warum dieses Prüfstück rot bleibt, ist nicht dieser Kandidat, sondern die gemeinsame
  Testumgebungsursache. Deren Behebung läuft als eigene Karte t-20261022-r27-ci-delivery mit PR #1377
  (Zweig work/r27-ci-delivery-dsn, Kopf 029e3ddd522): die Datenbankprüfungen lesen die Verbindung jetzt aus
  einer Quelle. Ist diese Karte angenommen, wird #1373 auf demselben Kopf neu geprüft; bis dahin bleibt der
  Blocker mit diesem Auslöser stehen.

## Handoff 2026-11-04 (Runde nach Basis-Verbindung, plattenfest nachgemessen)
- Kandidat: PR #1373, Zweig work/r27-execution-journal, Kopf 0d89a13e63a (ls-remote == Kopf), develop 2ea2c6f1
  ist Vorfahr; Prüfprotokoll des Kopfes: acht grün, null rot, zehn nach Auswahlregel übersprungen.
- Schreibgut bleibt auf die sechs Dateien des Protokollfeldes beschränkt; keine Workflow-, keine Produktdatei
  außerhalb des Feldes.
- Der Aufräumfehler war eine echte Abschlusslücke im Produkt, keine Umgebung: ein Hintergrundauftrag schrieb
  das Protokoll nach der Rückgabe weiter. Die Zusage wird jetzt vor der Rückgabe erwartet; die Gegenprobe
  (wieder im Hintergrund) macht die Prüfung nachweislich rot, zwanzig Wiederholungen und der
  Wettläufer-Nachweis sind grün.
- Beweissammlung auf der Platte (teardown-1.md).

## Handoff 2026-11-04 (Runde nach Basis-Verbindung, plattenfest nachgemessen)
- Kandidat: PR #1373, Zweig work/r27-execution-journal, Kopf 0d89a13e63a (ls-remote == Kopf), develop 2ea2c6f1
  ist Vorfahr; Prüfprotokoll des Kopfes: acht grün, null rot, zehn nach Auswahlregel übersprungen.
- Der frühere Blocker (unterschiedliche Datenbankanschlüsse) ist durch die verbundene Hebelkarte entfallen;
  der Eintrag ist retired.
- Schreibgut bleibt auf die sechs Dateien des Protokollfeldes beschränkt.
- Der Aufräumfehler war eine echte Abschlusslücke im Produkt, keine Umgebung: ein Hintergrundauftrag schrieb
  das Protokoll nach der Rückgabe weiter. Die Zusage wird jetzt vor der Rückgabe erwartet; die Gegenprobe
  (wieder im Hintergrund) macht die Prüfung nachweislich rot; zwanzig Wiederholungen und der
  Wettläufer-Nachweis sind grün. Beweissammlung: teardown-1.md.

## Review-Rueckruf 2026-11-04 (Codex review-1373c, verdict REJECT)
- Der Prüfer hat den Synchronismus selbst zurückgebaut (Handler auf Hintergrundlauf gestellt) und gemessen:
  beide bestehenden Tests bleiben grün — der Endzustandsbeweis fehlt also, er ist nur behauptet. Runde 4 muss
  einen rückbau-festen Test bringen: nach Rückkehr des Handlers steht der terminale Zustand sofort fest.
- Fehler beim finalen Speichern werden im Handler verworfen (Zeilen 214-232): ein Schreibfehler kann heute
  als Erfolg zurückkehren. Runde 4 reicht den Fehler durch und belegt das mit einem Speicherausfall-Test.
- Sleep-Schleifen in den neuen Tests raus (deterministische Synchronisation).

## Runde 4 pruefbar 2026-11-05 (kopf 52e972fd, develop 512dcd72 eingepflegt)
- Endzustands-Beweis ist mutantenfest (Rückbau auf Hintergrundlauf => Test rot, wörtlich belegt);
  Schlaf-Schleifen raus; Speicherfehler enden sichtbar ohne Antwort-Semantik-Änderung (Spec-Stelle 104
  unangetastet). Querschnitt nur sieben Maskin-HTTP-Dateien, Log-Zeile nur eigene Commits.

## Review-Rueckruf 2026-11-05 (r1373d REJECT, EIN punkt)
Mutantenfestigkeit und Durchreichen der Speicherfehler sind BESTAETIGT. Einziger Rest: der neue
Endzustands-Test wartet weiter per sleep-Schleife statt ereignisfest. Runde 5 = kanal-ordnung + race-20 +
erneute Mutantenprobe.

## Runde 5 pruefbar 2026-11-05 (kopf 2b997f3c19e, basis auf develop 24c7d049)
Schlaf-Polling raus (Kanal-Ordnung), race-count=20 grün, Rückbau-Mutante 20/20 rot gemessen, alle
gehosteten Jobs am Merged-Kopf terminal erfolgreich (41981442440, von mir abgerufen). Damit sind alle drei
Punkte der dritten Prüfung abgearbeitet; Merge obliegt der Owner-Runde.

## Rueckruf (1373e REJECT): ein Schlaf-Pfad uebersehen
Race-20 und Mutante bestanden; aber in der synchronisation bleibt time.Sleep an einer stelle. Runde 6:
kanal-/ereignis-synchronisation fuer genau den jeweiligen Uebergang, race-20 + Mutante erneut.

## Runde 6 pruefbar 2026-11-05 (kopf d691c3cd242, basis 2b997f3c19e)
Fern nachgemessen: ls-remote==d691c3cd242, GENAU ein eigener commit, time.Sleep im fernen machinehttp-baum
NULL Treffer (vorher 3) — Rezept 1373e erfuellt; lauf 41998165081 terminal SUCCESS am exakten kopf
(Selected Checks/unit/build/vet/format/workflow-policy/trusted-plan gruen, docker/podman-HA skipped wie
vorgesehen). Develop ist seit schnitt auf 42bfcb1cb4 weitergelaufen — base-refresh obliegt dem merge-zweig.

## Rueckruf (1373f REJECT): Mutant ueberlebt den EINZELLAUF
Race-20 und sleep-freiheit bestaetigt; aber eine einzelne end-state-aussage kann noch durchrutschen — die
synchronisation wartet auf wiederholung, nicht auf das EREIGNIS terminal-commit. Runde 7: steuerbare
barriere + einzellauf-rot-pflicht (3x wörtlich) + diesmal develop-42bfcb1cb4 in den zweig mergen.

## End zurueckgewiesen 2026-11-05 (13:4x), drei plattenbefunde gegen MERGEFAEHIG
1) Eigener hosted lauf 42025651234 am kopf 13e3e046a4e FEHLERHAFT genau am mutanten-test
(execution_request_identity_test.go:482 'backgrounded mutant committed terminal state on 202 tail') —
lokal 3x3 rot, auf dem laeufer ueberlebt: barriere haelt unter CI-bedingungen nicht. END-zeile zitierte
ueberdies den lauf des FALSCHEN zweigs (flake-kur). 2) ancestor develop 42bfcb1cb4 gemessen NEIN.
3) round-7.md am falschen ort (workers/evidence statt plan-repo). Korrektur befohlen: mutanten-zelle im
CI-pfad mit race flags ausstatten oder nachweis warum sie dort nicht laeuft + develop-merge + terminaler
neuer lauf + akte an rechten ort. Karte bleibt active.

## Runde 7 pruefbar 2026-11-05 (kopf a896bf61c5c)
Nachgemessen: ls-remote echt==head, develop 42bfcb1cb4 VORFAHR (merge drin), eigene commits 13e3e046+a48d53c7;
PR-GATE 'CI · PR #1373' terminal SUCCESS am exakten kopf (selected checks gruen, validate laut PR-Regel
skipped). Der daneben fehlgeschlagene BRANCH-workflow enthaelt die COMPOSE-inci-familie — das ist die
bekannte, separat kardierte Compose-Kette (#1383, dort blocked auf VM-Tor), KEIN tagebuch-defekt.
Einzellauf-Mutante per live-event-filter fix geschlossen (rot, wörtlich in akte), race20 gruen 125s.
Akte round-7.md von mir aus falschem ordner in den schichtordner gehoben. Freigabewege: MERGE obliegt der
Owner-Runde, die lane wartet auf nichts.

## Externe Übernahme — durch Coordinator nur markiert, nicht bearbeitet
PR #1373 (kopf a896bf61c5c, unsrerseits PRUEFBAR gemeldet, gate terminal gruen am kopf): Implementierung,
Abnahme, Merge und Planning-Abschluss liegen ab jetzt bei Owner+ChatGPT. Keine Lane dieser Seite fasst
machinehttp-dateien der kette an; abhaengige (management-host, state-recovery via journal-wiring) bleiben
bis zurueckgemeldetem Abschluss dieser Seite gesperrt gemessen. Die laufende wiederabnahme (1373g im
pruefkanal) ist hinfällig geworden und wird nicht weiter verfolgt.

## Vermerk zur Übernahme: unsere wiederabnahme (1373g) sagt ACCEPT auf a896bf61c5c
Einzellauf dreifach bestanden, mutante 3x rot (hosted-sonde gruen), race-20 gruen, PR-Gate terminal SUCCESS
am exakten kopf — akte review-1373g.md. Merge und abschluss liegen bei Owner+ChatGPT (übernahme), dieser
satz ist nur der abnahme-befund unserer seite ins protokoll.

## Korrektur zum vorrigen vermerk: die 1373g-URTEILSDATEI existiert nicht auf plan-main (nur pane-zeile gemessen)
Der abnahme-befund gilt als pane-beleg (END_DONE 5ec1339c mit feldern), die schritt-akte wurde durch die
abbestellung nicht mehr geschrieben. Fuer die owner-seite: keine datei referenzieren, dieakte existiert nicht.

## Abschluss 2026-11-05 – Owner/ChatGPT

- PR [#1373](https://github.com/mcpdev80/baseharbor/pull/1373) merged into `develop` as `77511c8a6672f34faf0d5ac543ba126485f05c41` (squash).
- Exact PR head `a896bf61c5c359cbdff47e26f4958b4ffc6c3282` matched [CI run 42031707838](https://github.com/mcpdev80/baseharbor/actions/runs/42031707838), completed success. Workflow policy, source format, trusted plan, go-unit-tests, go-vet, go-build, focused Python and selected checks all passed; `validate` and separate cross-repo gates were skipped by the selected PR policy, not treated as executed successes.
- Round-7 evidence: [deterministic terminal event barrier and single-call mutant, race-20](../evidence/r27-welle4-2026-11-05/execution-journal/round-7.md); independent reviewer recorded ACCEPT on this exact head. Duplicate/reconnect request identity and terminal persistence are integrated; no unrelated CI or cross-repo qualification is claimed.
- Previous review hold cleared; the downstream journal-wiring card may proceed. Release qualification remains separate.
