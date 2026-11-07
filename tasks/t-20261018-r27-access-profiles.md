---
id: t-20261018-r27-access-profiles
card_number: "0427-011"
card_short_title: "manage scoped team profiles"
areas: [access]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle4 (Lane w174, freigegeben)
kanban_lane: closed
kanban_summary: Create/update/revoke named profiles for selected Targets/operations/scopes/environments with existing policy authority. Profiles…
kanban_status: closed
kanban_title: "0427-011 · manage scoped team profiles"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-team-auth, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1384]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/evidence/r27-welle4-2026-11-05/access-profiles/round-1.md"]
---

- [x] t-20261018-r27-access-profiles · Access: manage scoped team profiles and owned assignments #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/access #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w174, freigegeben) · **Priority:** normal  
    **PR:** [baseharbor#1384](https://github.com/mcpdev80/baseharbor/pull/1384)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/evidence/r27-welle4-2026-11-05/access-profiles/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-team-auth](t-20261018-r27-team-auth.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-access-wizard](t-20261018-r27-access-wizard.md), [t-20261018-r27-managed-users](t-20261018-r27-managed-users.md)  
**Owner:** coord-welle4 (Lane w174, freigegeben)  
**Priority:** normal  
**PRs:** [baseharbor#1384](https://github.com/mcpdev80/baseharbor/pull/1384)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Create/update/revoke named profiles for selected Targets/operations/scopes/environments with existing policy authority. Profiles are recommendations/assignments, not imported grants. Server rechecks actor and selected targets at commit; idempotent assignment and foreign-grant preservation. No JIT/break-glass or business-user RBAC.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

internal/orgconfig/ bounded access-profile owner; internal/policy/ assignment adapter and tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Domain tests for grants/revoke/ambiguous names/stale selections/foreign installation and no escalation. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Kandidat pruefbar 2026-11-05 (kopf 06479fe0, zwei eigene commits, draft)
Von mir gemessen: Vorfahr ja, Pflege-dateien frei, lauf 41970216583 terminal erfolgreich am exakten kopf.
Karte meldet rote Grundlinie auf develop belegt + fall-satz (zuweisung, widerruf, mehrdeutig, veraltet,
fremd, eskalation).

## Review-Rueckruf 2026-11-05 (r1384a REJECT: 3/6 faelle, adapter war zweite wahrheit)
Profil-aenderungen konnten rechte aufsteigend erweitern; erwartete revision und tenant-binung fehlen;
produktionspfad nicht verbunden. Runde 2: adapter duemm (vermittelt nur), revision + akteur-binung in der
BESTEHENDEN autoritaet, widerruf durch denselben pfad, vier mutantenproben als gegenbeweis.

## Runde 2 pruefbar 2026-11-05 (kopf 3bb95cc794)
Alle sechs faelle mit mutanten a-d rot belegt; autoritaet liegt bei policy.Aggregate + orgconfig.Manager.Owner,
adapter nur ResolveFinding (duemm). Gate: lauf 41981861515 terminal SUCCESS am EXAKTEN kopf; der spaetere
ausfall 41983173186 ist ein fremder Timing-flake (t-20261105-r27-snapshot-change-guard-deterministic) mit
beiden laufen in der akte. Von mir nachgemessen.

## Rueckruf (1384b REJECT, zwei punkte trotz gruerner faelle)
Der adapter haengt nicht am echten produktionspfad (beitrag fliesst nirgends — dieselbe klasse wie 1380a),
und die fassungspruefung laesst ZUKUNFTSrevisionen durch. Runde 3: zusammenstellungs-test + drei
vergleichs-zellen (kleiner/gleich/groesser) mit gleichheit statt groesser-als.

## Runde 3 pruefbar 2026-11-05 (kopf 50b99c4625e = 3e672a24 + develop 42bfcb1cb4, ancestor JA)
Nachgemessen: ls-remote echt==head, name-only (eigene kette + merge ohne inhalt-anderung, dreipunkt-querschnitt
= genau die 8 profil-dateien), lauf 41999836846 terminal SUCCESS am exakten kopf; rezept 1384b beide punkte
gemeldet: echter zusammenbau faltet owned profil in policy.Aggregate, revisions-gleichheit (!=) mit
drei zellen + mutante rot. Akte round-3.md auf main bestaetigt. (Zwischenfall: lane meldete zuvor RC=0 an
veralteter tracking-ref — nach widerlegter erstmeldung sauber nachgeliefert.)

## ACCEPT 2026-11-05 (r1384c): merge-reif fuer die Owner-Runde
Kopf 50b99c4625e (entwicklungs-pfad + develop 42bfcb1cb4, ancestor JA). Produktionspfad gefaltet (echte
zuweisung -> policy.Aggregate), revisions-gleichheit mit 3-zellen-matrix + mutante rot, sechs r2-falle
behalten, blobs identisch — nach der widerlegten erstmeldung (ghost-RC=0) sauber nachgeliefert.


## Owner-Abschluss 2026-11-05

- PR [#1384](https://github.com/mcpdev80/baseharbor/pull/1384) nach `develop` gemerged, Squash-Commit `a7253eca61b18c660cecd0fa597f02f0a350557e`.
- Pflicht-CI [Run 41999836846](https://github.com/mcpdev80/baseharbor/actions/runs/41999836846) auf dem vor Merge verifizierten PR-Head abgeschlossen: `success`, einschließlich `PR Selected Checks`.
- Historische Review-Rückrufe und Korrekturen bleiben als Nachweis erhalten. Fachliche Abnahme gemäß letzter ACCEPT-Bewertung; separate Release-/Cross-Repo-Qualifizierung dadurch nicht vorweggenommen.
