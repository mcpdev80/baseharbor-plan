---
id: t-20261018-r27-device-lifecycle
areas: [access]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle5 (Lane w193)
kanban_lane: active
kanban_summary: "Revoke A without affecting B, apps or platform; bound stale sessions and active connections. Reconnect/renew require valid…"
kanban_status: active
kanban_title: "Devices: renew and revoke one workstation independently"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-device-enrollment, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-device-lifecycle · Devices: renew and revoke one workstation independently #task #release/v0-4-27 #status/active #view/active #area/access #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (Lane w193) · **Priority:** normal  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-access-wizard](t-20261018-r27-access-wizard.md), [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-management-host](t-20261018-r27-management-host.md), [t-20261018-r27-onboarding-wizard](t-20261018-r27-onboarding-wizard.md), [t-20261018-r27-state-recovery](t-20261018-r27-state-recovery.md)  
**Owner:** coord-welle5 (Lane w193)  
**Priority:** normal  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Revoke A without affecting B, apps or platform; bound stale sessions and active connections. Reconnect/renew require valid current authority; explicit local profile removal is not remote revocation. State revalidation and cancel do not partially delete resources.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

bounded workstation identity renewal/revocation owner/tests; same files serialized after enrollment owner. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Two-device stateful tests incl active-session revocation, restart, expiry and preserved foreign identities. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Runde 2026-11-05 (Lane w193, gerundete Entscheidung 2026-11-05)

Begründete Entscheidung (Owner-Antwort 2026-11-05, Koordinationsauftrag w193):

- Write-Set bleibt auf die NEUEN lifecycle-Einträge beschränkt, die Enrollment-Interna werden nicht angefasst.
- (a) `internal/workstationenrollment/Authority.go`: drei neue Owner-Methoden auf dem bestehenden
  `Authority` (own nur `ws.State` + den bestehenden `serviceaccess.CSRIssuer`):
  - `Renew(ctx, scope, request) (Result, error)` — renewt NUR den Umfang A; B, Apps und Plattform
    bleiben unangetastet (Matrixzelle). Nutzt `issuer.Renew`; verifiziert das neue Blatt gegen das
    Vertrauen und den tri-state `RevokedStatus`.
  - `Revoke(ctx, scope) error` — fügt den Serial des aktuellen Blatts von A in die CRL des Issuers
    (`issuer.Revoke(serial)`) ein, so NUR A ungültig wird; B bleibt gültig. Post-Revokation scheitert
    jede Handlung gegen A deterministisch.
  - `RenewAfterRevoked(ctx, scope) (state, error)` — expliziter Fehlerzustand, kein Schweigen: ein
    Umfang, dessen aktuelle Revokationsstatus true ist, schlägt fehl, statt still neu auszustellen.
- (b) begrenzter neuer `contracts/workstationlifecycle/v1`-Eingang parallel zu `EnrollDevice`: ein
  Lifecycle-Schema (`RecordKindWorkstationLifecycle`) + `RenewDevice`/`RevokeDevice`, die den
  Lifecycle-Zustand gegen `Authority` prüfen (fais closed auf unbekannt/revoked).
- Revokation läuft über den bestehenden `issuer.Revoke(serial)`/`RevokedStatus` (LocalIssuer CRL);
  Renew über `issuer.Renew`. Kein eigener PKI-Handler, kein standalone Adapter außerhalb des
  Namespaces (Dauerklausel: nur der echte Lebenszyklus-Pfad).
- Docker/compose: NIET lokal auf dem Session-Host (codeman-server baha-runner-docker-2). Reine
  Docker-/Podman-Tests nur per SSH auf baha-docker bzw. baha-podman, nie hier.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.
