---
id: t-20261018-r27-node-service
card_number: "0427-040"
card_short_title: "reconcile enrollment service"
areas: [connector]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: coord-welle4 (Codex-Worker cx09)
kanban_lane: closed
kanban_summary: "Review retained PR #4 exact unique work against current Core before extending; preserve it.…"
kanban_status: closed
kanban_title: "0427-040 · reconcile enrollment service"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261022-r27-ci-runtime]
repos: [mcpdev80/baseharbor-node-connector]
prs: [mcpdev80/baseharbor-node-connector#19]
sources: ["mcpdev80/baseharbor-node-connector#3"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/node-service/round-5.md", "https://github.com/mcpdev80/baseharbor-node-connector/commit/816720c4480d2ded55b9029fa711b843ef5bfdac", "https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41920428445", "https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41920428585"]
---

- [x] t-20261018-r27-node-service · Connector: reconcile enrollment service and restart behavior #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/connector #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Codex-Worker cx09) · **Priority:** normal  
    **PR:** [baseharbor-node-connector#19](https://github.com/mcpdev80/baseharbor-node-connector/pull/19)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/node-service/round-5.md), [proof 2](https://github.com/mcpdev80/baseharbor-node-connector/commit/816720c4480d2ded55b9029fa711b843ef5bfdac), [proof 3](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41920428445), [proof 4](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41920428585)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Required by:** [nc-3](nc-3-core-enrollment-remote-runtime-acceptance.md), [t-20261018-r27-node-trust](t-20261018-r27-node-trust.md), [t-20261104-r27-vm-integration-runs](t-20261104-r27-vm-integration-runs.md), [t-20261104-r27-vm-smoke-docker-podman](t-20261104-r27-vm-smoke-docker-podman.md)  
**Owner:** coord-welle4 (Codex-Worker cx09)  
**Priority:** normal  
**PRs:** [baseharbor-node-connector#19](https://github.com/mcpdev80/baseharbor-node-connector/pull/19)  
**Source:** [baseharbor-node-connector#3](https://github.com/mcpdev80/baseharbor-node-connector/issues/3)
<!-- /generated:links -->

## Outcome and acceptance

Review retained PR #4 exact unique work against current Core before extending; preserve it. Package/install/start/restart/uninstall rootless service without Go on node; native XDG/systemd user/lingering; explicit re-enrollment rules and protected local key generation. No desired-state or placement authority on node.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

Connector internal/targetaccess/install.go and bootstrap/enrollment service files; cmd/baseharbor-node-connector/; matching tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Focused Connector service/bootstrap tests/vet/build; bounded native service smoke for actual systemd behavior. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.


## Handoff 2026-11-04 (lane w105, coord f49a3303)
- Candidate: connector PR #19 (draft -> ready by coordinator), branch work/r27-node-service, head 764a2a4.
- Delivered: thin internal/nodeservice lifecycle (install/start/restart/uninstall, rootless systemd-user,
  lingering), re-enrollment determinism, protected local key generation; targetaccess reused; no desired-state
  or placement authority on the node. Nine red-first cases in evidence (slice-2).
- Path reservation: coordinator decision (b) — no contract-reserved connector service path existed; proposed
  path documented for public-surfaces/authority-contract review.
- Codex review r19a dispatched on this exact head; merge only after verdict.

## Review-Rueckruf 2026-11-04 (Luna review-19a, verdict REJECT)
- Kein aufrufbarer Produktionspfad: Install schrieb keine echte systemd-user-Unit; Remove stoppte/disabled die
  eigene Unit nicht nachweislich; lingering-Policy fehlt.
- Autorisierung erfolgt nicht vor Wirkungen (Lebensdauer-/Metadataseiteneffekte vor dem Autorisierungsschritt).
- Restart-Verhalten nicht beobachtet (Tests verglichen keine tatsaechlichen Aufrufe); fehlende Autorisierung
  nicht als Mutation mit NIL-Wirkungen belegt; zwei nativ uebersprungene Hosted-Jobs wurden nicht ausgefuehrt.
- Korrekturrunde = Lane w110 auf demselben Zweig/PR #19 (draft bis Umleitung durch coord). PR-Kopf vorher
  764a2a4.

## Round 2 2026-11-04 (lane w110, coord f49a3303)
- Head 78b3c4f on work/r27-node-service / PR #19: real rootless systemd-user unit install/remove/restart/enable
  plus lingering, authorization checked before every lifecycle or metadata effect, restart behaviour compared
  against start from recorded calls, native smoke run executed on a real user host.
- Hosted connector CI on this head: 1 pass, 2 skipping, 1 FAIL = job "source", step "Verify exact candidate
  source formatting". Formatting round is commissioned (lane w118, queued behind pool capacity); no review on a
  red head.

## Review-Rueckruf 2026-11-04 (Codex review-19a, verdict REJECT)
- Der Quellformat-Prüfer ist berechtigt rot: zwei Dateien des Antrags sind nicht formatiert (gofmt -l nennt
  cmd/baseharbor-node-connector/main.go und internal/nodeservice/nodeservice.go).
- Inhaltlich fehlt die echte wurzellose Benutzer-Einheit: Installation meldete Erfolg nach bloßer Manager-Probe,
  Entfernen nutzte keine unterstützten Vorgänge, der Produktionspfad konnte den Lebenszyklus nicht aufrufen,
  die Prüfung vor der Wirkung war nicht erzwungen.
- Korrekturrunde = Lane w130 auf demselben Zweig (Kein zweiter Antrag), mit nativem Rauchtest Nachweispflicht.

## Handoff 2026-11-04 (Runde 3, plattenfest nachgemessen)
- Kandidat: PR #19, Zweig work/r27-node-service, Kopf fcca9c4a295 (ls-remote == Kopf), Hauptlinie ist Vorfahr;
  Schreibgut bleibt auf die sechs Dateien des Verbindungspakets beschränkt.
- Die wahre Ursache des Naturlaufs war ein Produktfehler, keine Umgebung: der ausgelieferte Einheitsabschnitt
  schrieb eine Blöße Befehlszeile ohne das erforderliche Ausführungsschlüsselwort, therefore der Benutzerdienst
  die Einheit nicht lud. Meine Gegenprobe hatte die Host-Ausrede widerlegt; die Lane hat mit reiner
  Null-Code-Gegenprobe gegengemessen.
- Behoben: gültige Ausführungslinie mit absolutem Pfad, echter Installieren/Starten/Neustarten/Entfernen-
  Durchlauf auf lebendigem Benutzerdienstverwalter mit Erfolgs-Rückgabewerten, Überspringen und
  Entfernen über unterstützte Vorgänge, Prüfung vor jeder Wirkung.
- Gehostete Läufe des Kopfes: zwei grün, zwei übersprungen nach Auswahlregel; Formatierung leer.
- Beweissammlung liegt auf der Platte (round-3.md, 8131 Byte).

Round 4 (lane w136): --self-owned-unit ExecStart now executable + unit enabled after install; both review-19b gaps closed with own-command proof; both hosted gates green on 2fe4aef375. Reviewer acceptance pending.

## Handoff 2026-11-04 (Runde 4, plattenfest nachgemessen)
- Kandidat: PR #19, Zweig work/r27-node-service, Kopf 2fe4aef3757 (ls-remote == Kopf), Hauptlinie ist Vorfahr,
  Schreibgut bleibt auf sechs Dateien des Verbindungspakets beschränkt; gehostete Läufe: zwei grün, zwei nach
  Auswahlregel übersprungen.
- Lücke 1 (nicht ausführbare Befehlszeile) ist im Code geschlossen: Der Anmelder kennt das eigene
  Eigentumsmerkmal jetzt wirklich (Eingabelesung in cmd/baseharbor-node-connector/main.go:282, Ausgabestelle
  Zeile 146), und das Protokoll zeigt den echten Vorgang unter dem Dienstverwalter (Prozessnummer im
  Protokollauszug), nicht eine künstliche Probeeinheit.
- Lücke 2 (deaktivierte Einheit) ist geschlossen: Nach dem Einrichten wird der einschaltende Vorgang
  aufgerufen (internal/nodeservice/systemd.go:284), gemeldeter Zustand ist aktiviert.
- Beweissammlung auf der Platte (round-4.md).

## Review-Rueckruf 2026-11-04 (Codex review-19c, verdict REJECT)
- Der Eigentumsnachweis prüft nur Teilzeichenfolgen: ein artfremder Wert mit passendem Teilstück wird
  akzeptiert (Gegenbeispiele der Prüfung: Fremdpräfix/Fremdsuffix und Marker-Kollisionen wie
  foreign-baseharbor-node-connector.evil.container).
- Ein Fehler beim Aktivieren wird im Einrichtungsaufruf verschluckt: ein nicht aktivierter Zustand kann als
  erfolgreiche Einrichtung erscheinen. Beides sind echte Produktlücken, keine Umwelt.
- Korrekturrunde = Lane w141 auf demselben Zweig: Bindung an den kanonischen Namensraum bzw. die erwartete
  Einheitsidentität mit geschlossener Abweisung, Aktivierungsfehler muss als Einrichtungsfehler zurückkommen,
  und die Rot-auf-dem-kranken-Stand-Pflicht wird auf fcca9c4a nachgerechnet.

## Handoff 2026-11-04 (Round 5, Lane w141)
- Candidate: PR #19, branch `work/r27-node-service`, head `9913ce4770363cead7cc95726816acd4269c0358`; `ls-remote` matches and `origin/main` is an ancestor. PR remains OPEN/READY; no merge or PR status change.
- Replaced substring ownership matching with exact canonical identity; five counterexamples cover foreign prefix, suffix, marker collision, and conflicting identity. Enable failure now returns as a typed setup error; the test checks the remaining unit file and disabled state.
- New tests failed on `fcca9c4a295625062827343263de5b2ddaff4d62` and passed on this candidate. `go test ./... -count=1`, `go vet ./...`, `go build ./...`, `gofmt -l cmd internal` (empty), and `git diff --check` passed.
- Hosted runs reached terminal: Quality `41900064640` SUCCESS / job `126819771900` PASS; Source Conformance `41900064793` SUCCESS / job `126819771878` PASS. Native enrollment and encrypted transport were terminal SKIPPED, not counted as green.
- Full red-on-old output, run evidence, diff, and repo-rule compliance: `evidence/r27-welle4-2026-11-04/node-service/round-5.md`.

## Handoff 2026-11-04 (Runde 5, plattenfest nachgemessen)
- Kandidat: PR #19, Zweig work/r27-node-service, Kopf 9913ce4770363 (ls-remote == Kopf), Hauptlinie ist
  Vorfahr; sechs Dateien im Feld, Läufe zwei grün / zwei nach Auswahlregel übersprungen.
- Die Eigentumsprüfung vergleicht jetzt EXAKT gegen die drei zulässigen Eigennamen
  (internal/nodeservice/nodeservice.go:85-89, Gleichheit statt Teilzeichenfolge); die verbliebenen
  Textvergleiche in der Datei sind Prüfungen von Fehlermeldungen in Tests.
- Ein Fehler beim Aktivieren kommt als typisierter Einrichtungsfehler zurück; die Rot-auf-dem-kranken-Stand-
  Pflicht ist auf fcca9c4 nachgerechnet (fünf Kollisionsfälle plus der Aktivierungsfall, wörtlich in der
  Beweissammlung) statt behauptet.
- Die Meldung kam über die Ablagespur an, weil das Senden einer Freigabegrenze begegnete; beide Wege sind
  protokolliert.

## ChatGPT owner acceptance 2026-11-04

- Connector PR [#19](https://github.com/mcpdev80/baseharbor-node-connector/pull/19) merged into main at [816720c4480d](https://github.com/mcpdev80/baseharbor-node-connector/commit/816720c4480d2ded55b9029fa711b843ef5bfdac).
- Final head 807d92d3eb0128f25e4610f90f076c0b5b3c5882 passed quality [41920428445](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41920428445) and source conformance [41920428585](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41920428585).
- Reenrollment preserves installed unit; Start/Restart propagate persistence failures. Regression tests added. Native enrollment and encrypted transport jobs were selected SKIPPED; earlier native smoke proof remains in round-5.
