---
id: t-20261105-r27-connection-authority-boundary
card_number: "0427-111"
card_short_title: "target-scoped live-Conn"
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: ""
owner: coord-welle4 (Lane w172, freigegeben)
kanban_status: closed
kanban_lane: closed
kanban_summary: "Expose, inside the already accepted boundary internal/coreinstallation (authority), a resolution call that takes the VERIFIED…"
kanban_title: "0427-111 · target-scoped live-Conn"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1386]
sources: []
blocker: ""
resolution: accepted
evidence: [https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/connection-client/blocker-1.md]
---

- [x] t-20261105-r27-connection-authority-boundary · Authority: target-scoped live-connection resolution without an application context #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w172, freigegeben) · **Priority:** high  
    **PR:** [baseharbor#1386](https://github.com/mcpdev80/baseharbor/pull/1386)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/connection-client/blocker-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md)  
**Owner:** coord-welle4 (Lane w172, freigegeben)  
**Priority:** high  
**PRs:** [baseharbor#1386](https://github.com/mcpdev80/baseharbor/pull/1386)  
**Source:** 
<!-- /generated:links -->

## Goal

Expose, inside the already accepted boundary `internal/coreinstallation` (authority), a resolution call
that takes the VERIFIED INSTALLATION plus the TARGET (identity/state facts it already owns) and yields the
live management-connection issuer material that `ConnectionSelection.Resolve` must check. This unblocks the
explicit-selection verification on the real `use`/`target activate` production paths
(`t-20261018-r27-connection-client`).

## Scope

- In scope: one new exported resolver in `internal/coreinstallation` + its tests; wiring evidence for the
  consuming card.
- Out of scope (hard, measured by lane w164 2026-11-05): any change to `resolveApplication`,
  `resolveApplicationCoreRuntime`, `resolveManagementConnectionIssuer` call shape, or app-command paths
  (apply/plan/destroy). Measured fact driving this card: `use` (use_target.go:19) → `target activate.Run`
  (target.go:241) / guided activation (target_activate_wizard.go:15) never build a `resolvedApplication{}`,
  and the live issuer exists only behind `application_service_issuer.go:89→:20` which requires
  `resolvedApplication` + `bhruntime.RuntimeProvider`.

## Acceptance

- The new resolver returns the issuer material from installation+target facts alone (test on the boundary,
  no fabricated app context).
- Existing app-path resolver behavior is untouched (blob-identical files listed in evidence).
- Fail-closed: unverifiable installation or foreign target yields a named error, never a permissive empty.
- Red-first is the blocker transcript itself (w164 END_BLOCKED chain above).

## Required checks

- go test ./internal/coreinstallation ./cmd/baha -count=1, build, vet, gofmt; hosted runs to terminal.

## Handoff

Coordinator decision 2026-11-05 after lane w164 honored the STOP clause with a full call-chain witness.
Consuming candidate: PR #1380 (connection-client), which resumes on a free seat once this lands.

w168 IMPLEMENTATION DONE 2026-11-05: ResolverForTargetSelection in internal/coreinstallation/authority.go (a14bac06, branch work/r27-connection-authority cut from connection-client head). Derives live CA issuer from verified install+target state via serviceaccess.Issuer, no app-context; fail-closed ErrUnverifiableInstallation/ErrForeignTarget. coreinstall green; cmd/baha green (1 pre-existing Docker-socket flaky on pristine HEAD). name-only=2 files; log=own commit only; lsremote a14bac06. Ready for integration into consumer PR #1380 (w164) — no second PR/rerun/.github edits per scope split.

## Kandidat pruefbar 2026-11-05 (kopf b730243cbe1, zweiter Schnitt)
Nach der Basis-Korrektur gemessen: develop ist Vorfahr, EIN eigener Commit, Querschnitt nur Autoritaet +
Sondendatei (die #1380-eigenen Dateien sind korrekt draußen), Lauf 41981375241 terminal erfolgreich.
Fail-closed-Zellen + Grundlinien-Umschaltbeleg in der Akte.

## Rueckruf (1386a REJECT): lesend statt erzeugend
Der Resolver zieht bei fehlender Autorität eine neue CA hoch (EnsureLocalIssuer) — das macht die Pruefung
zur Implikation. Runde 2: rein lesende Beobachtung + zwei neue Sonden-Zellen (fehlendes Verzeichnis, leere
Issuer-Datei); Stopkriterium: je erzeugtes Material.

## Runde 2 pruefbar 2026-11-05 (kopf aa62518c6a6)
Nachgemessen: ls-remote echt==head, develop Vorfahr, zwei eigene commits, write-set genau die zwei
Dateien der Akte; code-gelesen: observeLocalIssuer strictly read-only, kein EnsureLocalIssuer-Aufruf im
Resolver; lauf 41988118382 terminal SUCCESS am exakten Kopf (Selected Checks nicht skipped). Akte
round-2.md publiziert (b998131).

## ACCEPT 2026-11-05 (r1386b): merge-reif fuer die Owner-Runde
Kopf aa62518c6a6; alle vier Sonden selbstonde bestaetigt, Fehlgeburts-Mutante rot, Resolver bleibt lesend —
fehlende/unvollstaendige Autoritaet schlaegt fail-closed fehl. Verbindungs-Karte (#1380) wird nach Merge frei.


## Owner-Abschluss 2026-11-05

- PR [#1386](https://github.com/mcpdev80/baseharbor/pull/1386) nach `develop` gemerged, Squash-Commit `b4f649500b4bea6774b7a8d36842ea6897e39a54`.
- Pflicht-CI [Run 41988118382](https://github.com/mcpdev80/baseharbor/actions/runs/41988118382) auf dem vor Merge verifizierten PR-Head abgeschlossen: `success`, einschließlich `PR Selected Checks`.
- Historische Review-Rückrufe und Korrekturen bleiben als Nachweis erhalten. Fachliche Abnahme gemäß letzter ACCEPT-Bewertung; separate Release-/Cross-Repo-Qualifizierung dadurch nicht vorweggenommen.
