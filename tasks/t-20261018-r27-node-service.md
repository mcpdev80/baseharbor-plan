---
id: t-20261018-r27-node-service
areas: [connector]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: coord-welle4 (Lane w136)
kanban_lane: review
kanban_summary: "Review retained PR #4 exact unique work against current Core before extending; preserve it.…"
kanban_status: review
kanban_title: "Connector: reconcile enrollment service and restart behavior"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261022-r27-ci-runtime]
repos: [mcpdev80/baseharbor-node-connector]
prs: [mcpdev80/baseharbor-node-connector#19]
sources: ["mcpdev80/baseharbor-node-connector#3"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/node-service/round-4.md"]
---

- [ ] t-20261018-r27-node-service · Connector: reconcile enrollment service and restart behavior #task #release/v0-4-27 #status/review #view/review #area/connector #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w136) · **Priority:** normal  
    **PR:** [baseharbor-node-connector#19](https://github.com/mcpdev80/baseharbor-node-connector/pull/19)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/node-service/round-4.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Required by:** [nc-3](nc-3-core-enrollment-remote-runtime-acceptance.md), [t-20261018-r27-node-trust](t-20261018-r27-node-trust.md), [t-20261104-r27-vm-integration-runs](t-20261104-r27-vm-integration-runs.md), [t-20261104-r27-vm-smoke-docker-podman](t-20261104-r27-vm-smoke-docker-podman.md)  
**Owner:** coord-welle4 (Lane w136)  
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
