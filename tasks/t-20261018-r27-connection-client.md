---
id: t-20261018-r27-connection-client
card_number: "0427-023"
card_short_title: "resolve trusted local or"
areas: [remote]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: ChatGPT (remote-client regression)
kanban_lane: active
kanban_summary: Keep management connection separate from placement Target. Explicit selection wins deterministically; bind server installation…
kanban_status: active
kanban_title: "0427-023 · resolve trusted local or"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261018-r27-profile-codec, t-20261022-r27-ci-access, t-20261105-r27-connection-authority-boundary]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1380, mcpdev80/baseharbor#1473]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1380"]
---

- [ ] t-20261018-r27-connection-client · Client: resolve trusted local or remote management connections #task #release/v0-4-27 #status/active #view/active #area/remote #kind/task
    <!-- generated:card -->
    **Owner:** ChatGPT (remote-client regression) · **Priority:** normal  
    **PR:** [baseharbor#1380](https://github.com/mcpdev80/baseharbor/pull/1380), [baseharbor#1473](https://github.com/mcpdev80/baseharbor/pull/1473)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1380)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261018-r27-profile-codec](t-20261018-r27-profile-codec.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md), [t-20261105-r27-connection-authority-boundary](t-20261105-r27-connection-authority-boundary.md)  
**Required by:** [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261108-smoke-0427-operator-api-undocumented](t-20261108-smoke-0427-operator-api-undocumented.md), [t-20261108-smoke-0427-serve-enrollment-authority](t-20261108-smoke-0427-serve-enrollment-authority.md)  
**Owner:** ChatGPT (remote-client regression)  
**Priority:** normal  
**PRs:** [baseharbor#1380](https://github.com/mcpdev80/baseharbor/pull/1380), [baseharbor#1473](https://github.com/mcpdev80/baseharbor/pull/1473)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Keep management connection separate from placement Target. Explicit selection wins deterministically; bind server installation identity, pinned trust and discovery/version negotiation. User-scoped local cache stores no remote authority; unavailable or changed server fails closed without local execution.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

bounded management connection/client package; cmd/baha/use_target.go connection-selection helper (no root registry edits). These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

TLS httptest, wrong peer/equal alias/two-installation/stale-cache/precedence tests; no runtime. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Anspruch 2026-11-04
- Auftrag: Verwaltungsverbindung und Platzierungsziel getrennt halten, ausdrueckliche Auswahl gewinnt
  deterministisch, Bindungen (Installation, Vertrauen, Entdeckung) weisen bei Abweichung vor jeder Wirkung ab.

## Kandidat pruefbar 2026-11-04
- Kopf f1f3551291c, develop ist Vorfahr, log-Zeile traegt nur den eigenen Commit (von mir gemessen).
- Die Wiederverwendung laeuft ueber die bereits abgenommene Kern-Installations-Autoritaet; Verbindung und
  Ziel sind getrennt, ausdrueckliche Auswahl gewinnt, Bindungen schliert fehlgeschluessen.
- Die Lane meldet einen PRE-EXISTING Ausfall der Compose-Lebenszyklus-Pruefung und nennt das keine
  Regression. Der Review muss das auf Deiner Hauptlinie selbst nachmessen (rote Grundlinie, nicht
  behauptet); die PR-eroeffnung uebernahm ich, weil die Lane den Schritt vergessen hatte.

## Review-Rueckruf 2026-11-05 (r1380a REJECT, zwei funde)
(1) Der Baseline-fehler ist VON DER PRUEFUNG SELBST auf develop nachgemessen identisch — Vorbestand der
Compose-Familie, erledigt, keine nachfolge. (2) ECHTER mangel: die neue autoritaetspruefung haengt nicht am
Produktionspfad — die echte Ziel-aktivierung ruft ConnectionSelection.Resolve nicht. Runde 2 schliesst den
pfad, mit STOP-recht falls dafuer ein fake-context noetig waere.

## Runde (basis-erneuert) pruefbar 2026-11-05 (kopf 02b2e65e7c5)
Nachgemessen: ls-remote echt==head, develop a53c10a7 drin (ancestor rc=0), gehosteter lauf 42055518849
TERMINAL SUCCESS am exakten kopf. Mutanten benannt rot, 1386-resolver nur gelesen (authority.go blob
unveraendert), fails-closed belegt. round-1.md (welle5) auf main.

## Gemerged 2026-11-05 (CODEX-MERGE nach 1380b ACCEPT): develop 3d8fc207de, merge-zweig 560945201e
(develop-abgleich a53c10a7+drin), same-head flake-rerun 42093092814 attempt2 SUCCESS, merge ohne bypass.
Drei-Autoritaeten-trennung + fails-closed pfad damit ECHT im zweig.

## Wiedereröffnet 2026-11-08 — echte Remote-Client-Lücke

Abgleich `baseharbor/develop`: `cmd/baha/use_target.go:bindExplicitSelectionToConnection` ruft `coreinstallation.Load(targetRuntimeStateRootByName(target))` aus **lokalem** Dateizustand auf. Bei Entwickler-PC mit `baha` ohne lokalen Core und externem Core fehlt dieser lokale Installationsdatensatz zwangsläufig; `baha use` verlangt stattdessen `baha core install`. Das widerspricht dem Outcome dieser Karte: Remote Management Connection muss über verifizierte Server-Installation/Trust/Discovery möglich sein, ohne lokale Core-Installation und ohne Kopie autoritativen States. Der `connection-profile/v1` Schema-Vertrag ist kein Beweis einer produktiven Remote-Bindung. 

**Akzeptanz offen:** developer-only CLI -> externes Core HTTPS/OIDC (serververifizierte Installations-ID, CA, Session, Scope) -> Target selection -> Docker-/Podman-Connector -> tatsächlich verifizierte Remote-App READY; negatives (fremde/abgelaufene Verbindung, falsches Tenant, nicht verfügbar, kein lokaler Fallback). Nicht mit Credential-Karte `0427-047` verwechseln; deren Draft #1470 behandelt einen separaten Aspekt. Vorheriger Merge #1380 bleibt historisch, aber `closed` ist für die End-to-End-Anforderung nicht mehr gerechtfertigt.


## Plan-validator correction — 2026-11-08

- The previous `resolution: reopened-regression` was invalid on an `active` card. Reopening remains documented in the audit narrative; the resolution field is intentionally empty until a verified final acceptance. Existing owner, PRs and dependencies remain unchanged.

## Draft #1473 2026-11-08 — Remote-Client-Qualifikation

PR [#1473](https://github.com/mcpdev80/baseharbor/pull/1473), Head `22277f8f`, wartet auf echte Remote-Bindung. Initialer Fix: `baha use` gibt für remote AccessProvider keine irreführende lokale Core-Installationsanweisung mehr aus und verweigert weiterhin jede unbestätigte Verbindung; Regression gegen lokalen Bootstrap-Fallback hinzugefügt. `connection-profile/v1` ist bisher nur ein Schema (`implementation deferred`), und der Core Machine HTTP Discovery-Handler liefert zwar Operationen, aber keine überprüfbare Installations-ID. **Produktiver Remote-Management-Client und hostübergreifender E2E-Durchlauf sind weiterhin OPEN.** CI-Lauf [#5228](https://github.com/mcpdev80/baseharbor/actions/runs/42481850017) gestartet; bei Inspektion waren alle gelisteten Jobs skipped, daher keine bestandenen Tests. Vor Freigabe: API-Identitätsnachweis, CA-Pin, OIDC-Tenant, remote Baha-Aufruf, Docker/Podman Connector und App READY, ohne lokale Core-State-Dateien.

## Ready CI qualification 2026-11-08

- PR [#1473](https://github.com/mcpdev80/baseharbor/pull/1473) temporarily converted to Ready for mandatory CI on exact head `092aa88a9a63e1c124420f91d231a07ef5e1934f`.
- [CI run #5303](https://github.com/mcpdev80/baseharbor/actions/runs/42510962220) reported **FAIL** for `PR · Source format` and `PR · Validation · cli-gofmt`, including `cmd/baha/machine_http_executor.go`, `cmd/baha/management_remote_connection.go`, `cmd/baha/management_remote_connection_test.go`, `cmd/baha/use_target.go`, `cmd/baha/use_target_remote_connection_test.go`, `internal/controlplaneruntime/server_run.go`. Other checks were still executing at inspection; do not infer PASS from the draft.
- Architectural gap persists: `verifyRemoteManagementConnection` authenticates a profile and server identity but does not itself route application operations through `machinehttp`; the separate developer workstation -> remote Core -> connector -> application READY and destroy contract remains unproved. Keep Draft / active until both formatting and functional E2E are qualified.

## Formatting remediation 2026-11-08

- Head `2d5ee37ca953cf1fa869121b297e96bd6ae14644` on PR [#1473](https://github.com/mcpdev80/baseharbor/pull/1473): six previously unformatted Go files corrected in bounded commits.
- Current [Ready CI #5319](https://github.com/mcpdev80/baseharbor/actions/runs/42512036786): **PR Source format PASS** and CLI gofmt PASS; other mandatory tests still active at last inspection. No merge authorization while full E2E dispatch remains absent.
- Inspected `cmd/baha/management_remote_connection.go`: `verifyRemoteManagementConnection` checks TLS/CA + issuer + tenant + installation identity but **does not dispatch app apply/status/update/destroy** over `/api/v1/machine/executions`. Server HTTP lifecycle handlers exist in `cmd/baha/machine_http_executor_lifecycle.go`; wire the actual developer CLI to them with authenticated, target/tenant-scoped execution. Validate a separate Dev-PC -> remote Core -> Connector -> Docker app HTTP READY, update, destroy, with no local-runtime fallback. Until proven, remain active and E2E FAIL.
