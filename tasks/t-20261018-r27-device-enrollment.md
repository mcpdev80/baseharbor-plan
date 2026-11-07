---
id: t-20261018-r27-device-enrollment
card_number: "0427-026"
card_short_title: "issue and validate scoped"
areas: [access]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle4 (Lane w146, freigegeben)
kanban_lane: closed
kanban_summary: "Explicit installation policy may issue recipient-bound, short-lived one-use workstation enrollment and separate device identity.…"
kanban_status: closed
kanban_title: "0427-026 · issue and validate scoped"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261018-r27-profile-contract, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1371]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/commit/24c7d0492f34e58c2a6be505ba80b8bdfb151cb7", "https://github.com/mcpdev80/baseharbor/actions/runs/41964458878"]
---

- [x] t-20261018-r27-device-enrollment · Devices: issue and validate scoped workstation enrollment #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/access #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w146, freigegeben) · **Priority:** normal  
    **PR:** [baseharbor#1371](https://github.com/mcpdev80/baseharbor/pull/1371)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/24c7d0492f34e58c2a6be505ba80b8bdfb151cb7), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/41964458878)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261018-r27-profile-contract](t-20261018-r27-profile-contract.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-device-lifecycle](t-20261018-r27-device-lifecycle.md), [t-20261104-r27-vm-integration-runs](t-20261104-r27-vm-integration-runs.md), [t-20261104-r27-vm-smoke-docker-podman](t-20261104-r27-vm-smoke-docker-podman.md)  
**Owner:** coord-welle4 (Lane w146, freigegeben)  
**Priority:** normal  
**PRs:** [baseharbor#1371](https://github.com/mcpdev80/baseharbor/pull/1371)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Explicit installation policy may issue recipient-bound, short-lived one-use workstation enrollment and separate device identity. Pin destination/scope; each device individually renewable/revocable. Never reuse Node credentials or infer trusted remote access from dev label; no remote app/admin/recovery secrets in bundle.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

bounded workstation enrollment owner/HTTP adapter under existing management boundary; no node enrollment file edits. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Issue/consume/replay/expiry/wrong-recipient/wrong-installation/certificate negative tests; approved crypto/auth owner reuse. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

### Delivery — 2026-11-04 (worker w90, lane w90)
Option A (Owner scope decision 2026-11-04): delivered a NEW bounded workstation-enrollment slice in
its own namespace, distinct from node/connector enrollment (internal/targetenrollment untouched).

- Branch `work/r27-workstation-enrollment` @ `2a4df949` (feat `299f8143` + evidence `53f17b93`),
  PR **#1364** (draft), base develop `3d08ef72`.
- `contracts/workstationenrollment/v1/` — portable wire contract: `Record` + fail-closed
  `ValidateKindEnforcement` + `EnrollDevice` + draft-2020-12 schema.
- `internal/workstationenrollment/` — installation-scoped `Scope` (SPIFFE
  `spiffe://baseharbor/workstations/<tenant>/<station>`, not Core connector), one-use `Store`,
  `Authority.Enroll` validate-then-consume (SignCSR → TrustBundle → ValidateSignedCSR → RevokedStatus,
  all fail-closed), reusing accepted `internal/serviceaccess` issuer boundary.
- `internal/workstationenrollment/http/` — one-use bootstrap/enroll adapter at the management boundary;
  registry-fakt records scope+time; no private key returned.
- Rote-first (RED) cases pass: second-use, elapsed window, foreign recipient/scope, malformed leaf;
  plus positive (single use issues a leaf with scope+time in the registry-fakt) and HTTP end-to-end.
- Local: go build / go test / go vet green; gofmt clean; source-readability-audit PASS.
  Draft CI 41800237126 terminal SUCCESS (Workflow policy + Source format).
- Write-set: ONLY new files (1417 insertions, 0 deletions vs develop); no shared register/registration
  files touched (Owner scope decision — reported as none needed).
- Awaiting Maintainer acceptance + CODEX-REVIEW against evidence; CODEX-MERGE only if it passes. No
  release/tag/deploy authorized by this delivery.


## Koordinator-Erweiterung 2026-11-04 (write-set, produktionspfad-runde, w96)
- Zusaetzlich erlaubt: MINIMALE additive注册-zeilen in internal/controlplaneruntime/server_run.go und
  cmd/baha (provider-/route- hookup am bestehenden authentisierten management-einstieg) — ausschliesslich
  ergaenzend, keine umordnung, keine fachfremde zeile. targetenrollment + fremde register bleiben gesperrt.
- KonFLICTabstimmung: state-owner-linie (cmd/baha fixtures) laeuft parallel auf ANDEREM zweig; merges
  hintereinander ( zuerst was_aelter_reift ), koordiniert coord.

## Produktionspfad-Runde 2026-11-04 (worker w96, lane w96)
Erlaubnis (Coord f49a3303, 2026-11-04): full production wiring — dauerhafter Store im database-Paket
(eigene workstation-enrollment-Tabellen, connector_* unangetastet), scope-aus-Policy-Resolver +
enrollment-provider in cmd/baha (ConnectorEnrollmentHTTP-Muster), plus minimale ADDITIVE provider-/route-
hookup-zeilen in internal/controlplaneruntime/server_run.go und cmd/baha am bestehenden authentisierten
management-einstieg. Ausschliesslich ergaenzend, keine umordnung, keine fachfremde zeile;
targetenrollment + fremde register bleiben HEILIG. Wenn ein teil dieser drei komponenten groesser wird als
die erlaubnis traegt: HALT + END_BLOCKED mit datei:stelle. Basis-Vorfahr develop f8ef4255; gates terminal;
ls-remote==head.


## Coordinator-Umleitungs-Vermerk 2026-11-04 (w96 production round)
- #1364 geschlossen (superseded, begruendung + diff-beleg im close-comment): rebase auf develop f8ef4255.
- Neuer Kandidat: PR #1371 (draft) branch work/w96-production-wiring-f8ef4255 head fb701991;
  prototyp + produktionspfad-verdrahtung, 14 eigene dateien im namespace + store dauernd + policy-quelle.

- Round 2 (lane w104) delivered head af05b198 on branch work/w96-production-wiring-f8ef4255 / PR #1371: all
  four review-1371a recipes addressed (route suffix, policy-sourced station scope, fail-closed registry fact,
  PostgreSQL integration executed against a real database). Base refresh onto develop bb9bc0ef is in flight
  (lane w108); Codex final review follows on the refreshed head only.

- 2026-11-04 (CI): develop advanced to 2a43984a (self-contained PostgreSQL for selected PR Go unit tests).
  PR #1371 is red on go-unit-tests because its base predates that fix (station policy resolver integration
  test dials 127.0.0.1:5433). Task to bring #1371 onto 2a43984a and re-verify real PR CI is commissioned as
  lane w115 (mission queued behind pool capacity: 4 lanes busy).
- Umgebungsbefund 2026-11-04 (Koordinator, ursprüngliche Meldung aus der Klassifikation): Der
  Migrationsrückbau-Test blieb rot und wurde als eigenständiger Produktbefund dieser Karte eingeordnet.
- Berichtigung 2026-11-04 (unabhängige Nachmessung, class-a-verification.md Zeile 1): In frischen isolierten
  Läufen ist der Fehlschlag auf Deiner Hauptlinie UND auf dem Anmelungszweig NICHT reproduzierbar; die
  Klassenentscheidung A war damit überhöht. Der Befund bleibt als offene Sequenz-/Zustandsfrage stehen,
  Produktänderungen gibt es erst mit reproduziertem Fehler. Lane w132 trägt diese Klärung auf.

## Runde 2026-11-04 (Produktbefund Migrationsrückbau)
- Die Umgebungsursache (fest kodierte Datenbankadresse) wird auf der Hebelkarte t-20261022-r27-ci-delivery
  behoben; hier wird nur der echte Produktbefund bearbeitet: Der Rückbautest nimmt mehr zurück als die
  letzte Änderung (internal/database/migration_rollback_integration_test.go) und bleibt auch mit richtiger
  Verbindung rot.
- Kandidatenkette bleibt PR #1371 auf work/w96-production-wiring-f8ef4255 (develop ist Vorfahr), kein zweiter Antrag.

## Handoff 2026-11-04 (Runde nach Basis-Bereinigung, plattenfest nachgemessen)
- Kandidat: PR #1371, Zweig work/w96-production-wiring-f8ef4255, Kopf 8d3531f03ec (ls-remote == Kopf),
  develop 2ea2c6f1 ist Vorfahr; Prüfprotokoll des Kopfes: zwölf grün, null rot, zehn übersprungen.
- Der Rückbau-Fehlschlag ist aufgeklärt und behoben: Die Prüfung las ihren Festwert für die letzte Stufe,
  jetzt folgt sie der Stufenliste (mit Namensprüfung der höchsten Stufe); damit ist die drei Wochen alte
  Frage, warum sie auf der Hauptlinie grün und auf dem Zweig rot war, beantwortet.
- Beweissammlung auf der Platte (rollback-1.md).

## Review-Rueckruf 2026-11-04 (Codex review-1371b, verdict REJECT trotz zwölf grüner Prüfpunkte)
- Die Prüfung ist qualitätsseitig richtig, aber drei Datenbankprüfungen überspringen ohne gesetzte Verbindung
  noch statt zu fehl schlagen, und die Rückbaustufe wird namentlich festgeschrieben.
- BERICHTIGUNG AN MIR SELBST: die Namensfestschreibung war mein eigener Auftragstext (höchste Stufe aus der
  Liste UND zusätzlich der Name). Die Namensprüfung ist genau die Schwäche, die das Urteil beanstandet; sie
  fliegt raus, die Regel ableitung bleibt.
- Korrekturrunde = Lane w143 auf demselben Ast; die Überspringung in den drei Dateien gehört zu diesem Feld,
  alle anderen Überspringstellen bleiben bei der eigenen Karte (PR #1378), damit keine Doppelung entsteht.

## Handoff 2026-11-04 (Runde 4, plattenfest nachgemessen)
- Kandidat: PR #1371, Zweig work/w96-production-wiring-f8ef4255, Kopf f4ec625f801 (ls-remote == Kopf),
  develop e444ae11 ist Vorfahr; Prüfprotokoll 16 grün, null rot, zehn nach Auswahlregel übersprungen.
- Die Namensfestschreibung ist raus (von mir im Zweig gesucht: kein Treffer), die höchste Stufe wird aus der
  geordneten Liste abgeleitet; die Gegenprobe mit vertauschten Stufen folgt weiter der Liste und lässt die
  früheren Stufen unangetastet.
- Die drei Datenbankprüfungen schlagen ohne gesetzte Verbindung fehl (je eine Fehlstelle in der Datei, kein
  Überspringen mehr) und sind mit der Skriptverbindung ausgeführt grün; der Vergleich auf Deiner alten und
  neuen Grundlage sowie auf dem Kandidaten ist dokumentiert.
- Beweissammlung auf der Platte (rollback-2.md).

## Review-Rueckruf 2026-11-04 (Codex review-1371c, verdict REJECT)
- R1 Kaeltestart: eine erste Geratestation kann sich auf einer leeren安装 nicht anmelden — der Zulasser
  verlangt eine Registerzeile, die der Produktionspfad erst nach erfolgreicher Anmeldung schreibt. Die
  Prüferin hat das mit frischer Datenbank gemessen (vierhundertdrei, null Anlagevorgänge); der bestehende
  Test setzt die Zeile manuell und deckt den Fall deshalb nicht.
- R2 Rueckbau: die Stufe wird jetzt aus der Liste gewaehlt, die zugehoerigen Artefakte aber immer noch
  fest behauptet — nach einem Zahlentausch von 0008/0009 scheitert die Prüfung an der Annahme, nicht am
  Produkt. Vorgegeben: die Artefaktmenge aus der Ruücknamedatei der Stufe lesen.
- R3 Betriebsfehler MIT: Die Lane hat ihre Kennung und meine Basisanweisung in AGENTS.md des Produktrepo
  geschrieben. Das fliegt raus, die Regel kommt in meinen Auftragstext.

## Runde 5 pruefbar 2026-11-04 (kopf 1b3a2767ff5)
- Der Zulasser akzeptiert zusätzlich eine gültige, noch unverbrauchte Zuweisung aus der bestehenden
  Zuweisungstabelle — der Zirkel der Erstanmeldung ist damit aufgelöst, ohne neues Schema. Fünf Nachweisfälle
  stehen in der Eidesstatt (coldstart-1.md).
- Die Rückbau-Prüfung liest ihre Artefaktmenge jetzt aus der Rücknamedatei der gewählten Stufe; der
  Zahlentausch von 0008/0009 ist als Gegenprobe gemessen.
- Betriebsfehler bereinigt: AGENTS.md ist aus dem Antrag raus, der Querschnitt zeigt nur Anmeldungs-,
  Datenbank- und Verdrahtungsfeld. Lauf 41921792984 auf dem neuen Kopf: erfolgreich (von mir gemessen).

## Merge-Abschluss 2026-11-05

- [PR #1371](https://github.com/mcpdev80/baseharbor/pull/1371) wurde bei konfliktfreiem GitHub-Head `8badcbd24f9a1be3d59f75233c39294d8876d38a` nach develop gemergt.
- Squash-Commit: [24c7d0492f34e58c2a6be505ba80b8bdfb151cb7](https://github.com/mcpdev80/baseharbor/commit/24c7d0492f34e58c2a6be505ba80b8bdfb151cb7).
- [CI-Lauf #41964458878](https://github.com/mcpdev80/baseharbor/actions/runs/41964458878) erfolgreich; nur tatsächlich ausgeführte Jobs zählen als Testnachweis.
