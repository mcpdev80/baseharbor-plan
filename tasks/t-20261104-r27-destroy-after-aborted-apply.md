---
id: t-20261104-r27-destroy-after-aborted-apply
card_number: "0427-105"
card_short_title: "destroy must succeed when a"
type: task
areas: [deployment]
release: v0.4.27
version: ""
parent: ""
owner: coord-welle4 (Lane w158, freigegeben)
kanban_status: closed
kanban_lane: closed
kanban_summary: app destroy --yes ends with success and leaves no running instance and no project ownership when a provider-change apply aborted…
kanban_title: "0427-105 · destroy must succeed when a"
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261104-r27-consent-abort-leaves-undestroyable-state]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1382]
sources: []
blocker: ""
resolution: accepted
evidence: [https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/vm-integration/rebuild-1.md, https://github.com/mcpdev80/baseharbor/pull/1382, https://github.com/mcpdev80/baseharbor/commit/3b5974ca111bb73947ce51ecd3edf588301644ad, https://github.com/mcpdev80/baseharbor/actions/runs/41951027459, https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/destroy-aborted-apply/review-1382c.md]
---

- [x] t-20261104-r27-destroy-after-aborted-apply · Deployment: destroy must succeed when a provider-change apply aborted before runtime materialization #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/deployment #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w158, freigegeben) · **Priority:** high  
    **PR:** [baseharbor#1382](https://github.com/mcpdev80/baseharbor/pull/1382)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/vm-integration/rebuild-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1382), [proof 3](https://github.com/mcpdev80/baseharbor/commit/3b5974ca111bb73947ce51ecd3edf588301644ad), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/41951027459), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/destroy-aborted-apply/review-1382c.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261104-r27-consent-abort-leaves-undestroyable-state](t-20261104-r27-consent-abort-leaves-undestroyable-state.md)  
**Owner:** coord-welle4 (Lane w158, freigegeben)  
**Priority:** high  
**PRs:** [baseharbor#1382](https://github.com/mcpdev80/baseharbor/pull/1382)  
**Source:** 
<!-- /generated:links -->

## Goal

`app destroy --yes` ends with success and leaves no running instance and no project ownership when a
provider-change apply aborted midway — i.e. `deployment.json` exists with an applied record
(`last_applied_ref` set) but the stage runtime environment (`state/<stage>/runtime/runtime.env`) was never
materialized. Today destroy fails there with an unhelpful missing-file error, so the deployment becomes
undestroyable through the normal path.

## Scope

- In scope: the destroy path's handling of a partially-applied provider change (intent applied, runtime
  materialization missing); a regression proving red-on-develop, green-on-candidate.
- Out of scope: the impact-confirmation UX itself (two confirmations for a provider change is intended);
  the consent gate (blob-identical, fail-closed, unchanged); the never-delivered case already fixed by
  `t-20261104-r27-consent-abort-leaves-undestroyable-state` (that cell lacked deployment.json entirely).

## Measured reproduction (2026-11-04, VM lane w150, host baha-docker rebuilt from develop ea3fb38e;
full transcript: [rebuild-1.md](../evidence/r27-welle4-2026-11-04/vm-integration/rebuild-1.md))

- `baha target create` → `app init --yes` rc=0 → `app apply --no-input` rc=1 with
  "provider change: impact-confirmation-required (2 confirmations, --yes gives 1)".
- Afterwards `deployment.json` present with applied intent/runtime provider/delivery/generated state and
  `last_applied_ref` recorded; `state/r27-w150-demo/runtime/runtime.env` absent.
- `baha app destroy --yes` rc=1: "read application runtime environment: open .../runtime/runtime.env: no
  such file or directory". Phase: DESTROY, after passing all preflight checks.

## Acceptance

- Destroy in the state shape above returns success without manual cleanup between steps.
- After destroy: no running instance and no ownership of the project remain (list, not assertion).
- A never-delivered application (no last_applied_ref) and the normal apply+destroy path behave exactly as
  before (regression or untouched-path test each).
- The consent gate remains fail-closed and unmodified (blob comparison).
- Red-first is measured: the new regression fails on develop ea3fb38e (name the commit and show output)
  and passes on the candidate.

## Required checks

- Targeted: `go test ./cmd/baha ./internal/deployment -count=1` with the shared database script pairing;
  build, vet, gofmt.
- Hosted runs of the exact head to terminal state.

## Kandidat pruefbar 2026-11-05 (kopf 942e3cc562b)
- Gemessen von mir: Vorfahr ja, eigener commit, Querschnitt nur Zerstörungs-/Telemetrie-Pfad + zwei neue
  Tests, Lauf 41937967623 terminal erfolgreich.
- Der halbfertige Anbieterwechsel-Zustand endet jetzt mit sauberer Entfernung (Erfolg, kein Rest); die
  geschlossene Zelle (Zustandsdatei fehlt ganz) und der Glueckpfad unveraendert, Schranke blob-identisch.
- Offene Prueffrage an den Kanal: warum die Telemetrie-Autorisierungsdatei mit im Schnitt liegt.

## Review-Rueckruf 2026-11-05 (review-1382a REJECT, ein Rezept-Punkt)
Der Zerstörungs-Fix selbst ist anerkannt und bleibt. Aber die zusätzliche Telemetrie-Datei macht einen
GEMEINSAM gelesenen Datei-Leser nachsichtig (fehlende Datei => leere Liste fuer alle Aufrufer) — das
unterdrueckt echte Bindeungs-Fehler im normalen Betrieb. Runde 2 setzt die Datei auf deinen Stand zurueck
und haelt die Nachsicht strikt im Zerstoerungspfad mit Eigentumsnachweis.

## Runde 2 pruefbar 2026-11-05 (kopf 3691173821)
Rezept ausgefuehrt: Telemetrie-Rücksetzung blob-identisch zu develop (abbb5bb6, von mir gemessen),
Nachsicht jetzt im Zerstoerungspfad mit neuer Eigentumsdatei; Zelle rc=0, #1375-Zelle und Glueckpfad
gruen. Prueffrage an den Kanal: wer ruft runtime_owner_write.go auf (nur Zerstoerungspfad?).

## Rueckruf auf EIGENE messung 2026-11-05 (nicht auf ein Urteil)
Der Lauf am Runde-2-Kopf ist in Source-Format, cli-gofmt und den Unit-Jobs rot (gofmt-Absage an cmd/baha,
Wortlaut aus dem Runner-Job). Runde 3 stellt Form und Unit-Ernst her; Compose-Vorbestand bleibt separiert
(Hebelkarte). Der Inhaltliche Rezeptpunkt (Telemetrie rueckgesetzt, blob gemessen) gilt weiterhin.

## Runde 3 pruefbar 2026-11-05 (kopf d1f4eada327)
- Rezept 1382b in Verhalten gefasst (kein Refactoring um des Refactorings willen): gemeinsamer Stopp-Pfad
  endet bei degeneratem Zustand FEHLERHAFT (fail-closed, Vorher/Nachher gemessen); der Erfolg rc=0 lebt in
  zerstoerungs-eigenen Helfer-Dateien; drei Mutations-Zellen (sichern/TLS/ordinärer Stopp) beweisen die
  Abgrenzung. Erledigt ausserdem: mein Format-Befund aus dem Runner (gofmt-Liste leer), vier formerly-red
  Jobs gruen in lauf 41951027459 terminal.
