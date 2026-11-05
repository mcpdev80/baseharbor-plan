---
id: t-20261018-r27-protected-credentials
areas: [access]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle4 (Lane w175)
kanban_lane: review
kanban_summary: Explicit secure choice uses existing authoritative protected store when managed secrets exist; never bootstrap OpenBao solely to…
kanban_status: review
kanban_title: "Credentials: retain and recover opted-in local credentials"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-native-auth, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1385]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/evidence/r27-welle4-2026-11-05/protected-credentials/round-1.md", "https://github.com/mcpdev80/baseharbor/evidence/r27-welle4-2026-11-05/protected-credentials/round-2.md", "https://github.com/mcpdev80/baseharbor-plan/evidence/r27-welle4-2026-11-05/protected-credentials/round-3.md"]
---

- [ ] t-20261018-r27-protected-credentials · Credentials: retain and recover opted-in local credentials #task #release/v0-4-27 #status/review #view/review #area/access #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w175) · **Priority:** normal  
    **PR:** [baseharbor#1385](https://github.com/mcpdev80/baseharbor/pull/1385)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/evidence/r27-welle4-2026-11-05/protected-credentials/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/evidence/r27-welle4-2026-11-05/protected-credentials/round-2.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/evidence/r27-welle4-2026-11-05/protected-credentials/round-3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-native-auth](t-20261018-r27-native-auth.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-secure-export](t-20261018-r27-secure-export.md)  
**Owner:** coord-welle4 (Lane w175)  
**Priority:** normal  
**PRs:** [baseharbor#1385](https://github.com/mcpdev80/baseharbor/pull/1385)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Explicit secure choice uses existing authoritative protected store when managed secrets exist; never bootstrap OpenBao solely to reuse working native auth. Keep human/service/machine classes separate; references only in ordinary state. Verify reuse, rotation/revocation and local recoverability; report external non-exportable credentials explicitly. Remote-secret placement never falls back to the workstation.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

internal/credential/broker.go and prepared-material persistence integration; internal/credential/openbao/; focused tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Focused existing broker/OpenBao adapter tests plus bounded integration only for real persistence/rotation behavior not covered cheaply. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

w162: device-rebind recovery for opt-in local developer credentials (commit 74a74e49). opt-in local FilePreparedMaterialStore authority + recover; wires existing OpenBao managed path where present, fail-closed when absent. CI run 41974727140 = PR Selected Checks success. Pending: Codex review + Maintainer merge.

## Kandidat pruefbar 2026-11-05 (kopf 74a74e49fdc)
devaccess-erweiterung (rebind + verdrahtung des bestehenden bao-pfads), vier wiederherstellungszellen,
fail-closed-zelle namentlich rot belegt, selected-checks gruen am kopf. Kein neuer geheimnis-speicher.

## Rueckruf 2026-11-05 (1385a REJECT: zellen 4/4 ok, aber wiederholung kann OpenBao zweimal
beschreiben und kaemt mit konkurrierendem eintrag)
Runde 2: eine Set pro pfad (abgeleitet aus der bestehenden reconcile-naht), rueckgabe des wiedergewonnenen
wertes, zaehlung der Get/Set-paare DURCH den echten produktionspfad; kein neuer speicher.

round-2 fix pushed (e295127e), CI Selected Checks 41985472620 success, card to re-review

## Runde 2 pruefbar 2026-11-05 (kopf e295127e45b)
Gemessen: Vorfahr ja, zwei eigene commits, Querschnitt devaccess+befehlsverdrahtung. Rezeptpunkt erfuellt
meldet die Lane: genau EIN Schreibvorgang pro frischem Geraet, NULL bei vorhandenem Bestand, Wettlauf:
vorhandener Wert gewinnt, alles ueber die bestehende Vergleichs-Naht.

## Rückruf (1385b REJECT): Wettlauf-Sonde der Prüfung erwischt Überschreiben
Der eigene Race-Nachweis der Lane war unvollständig: der Test brach vor dem Wiederherstellungsschritt ab,
dahir blieb das Überschreiben eines konkurrierend erzeugten Werts unentdeckt. Runde 3: create-only/CAS-
Erstseedung über die bestehende Ablage-Autorität, vorhandener Wert gewinnt (ein Get, null Set), der Test-
ablauf heilt nachweislich bis zum Schritt durch, CAS-Mutante macht die Konfliktzelle rot.

Round 3: create-only CAS seed (SetManagedCredentialIfAbsent, -if-not-exists) over existing OpenBao authority; existing managed value wins (1 Get 0 overwrite Set on conflict); race test fixed (initial Get NOT-FOUND, concurrent injected between Exists and seed, seed no-ops winner wins) + mutant RED cell. PR #1385 head b3c3c1c1; hosted CI #4790 success.
