---
id: nc-3
card_number: "0428-041"
card_short_title: "Core Connector runtime"
areas: [connector]
type: task
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_lane: closed
kanban_summary: "The Node Connector integrates with real Core enrollment and sessions, and real remote Docker Compose and rootless Podman Quadlet…"
kanban_status: closed
kanban_title: 0428-041 · Core Connector runtime
depends_on: [t-20261017-release-0-4-28-updates, t-20261018-r27-node-cli, t-20261018-r27-node-service, t-20261018-r27-node-streams, t-20261018-r27-node-trust, t-20261106-r27-remote-up-cli-path]
repos: [mcpdev80/baseharbor-node-connector]
prs: []
sources: ["mcpdev80/baseharbor-node-connector#3"]
source_updated: "2026-10-08T13:52:57Z"
labels: []
blocker: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-public-console-connector-scope.md"]
---

- [x] nc-3 · Node Connector: Core-compatible enrollment and real remote Docker/Podman acceptance #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/connector #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261018-r27-node-cli](t-20261018-r27-node-cli.md), [t-20261106-r27-remote-up-cli-path](t-20261106-r27-remote-up-cli-path.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-public-console-connector-scope.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261018-r27-node-cli](t-20261018-r27-node-cli.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md), [t-20261018-r27-node-streams](t-20261018-r27-node-streams.md), [t-20261018-r27-node-trust](t-20261018-r27-node-trust.md), [t-20261106-r27-remote-up-cli-path](t-20261106-r27-remote-up-cli-path.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor-node-connector#3](https://github.com/mcpdev80/baseharbor-node-connector/issues/3)
<!-- /generated:links -->

## Execution boundary (2026-10-18)

This existing card is the final Connector acceptance/handoff owner, not a parallel implementation umbrella. The retained scope below remains acceptance authority. Implementation is split in the [v0.4.27 plan](../releases/v0.4.27.md). Own only the final acceptance receipt/matrix and connector documentation corrections after the named predecessors are accepted; no competing service/session/CLI edits. Reuse verifier-valid native proofs from those tasks, run only missing/affected compatibility coverage. Keep historical PR #4/source branches intact; historical source evidence does not qualify the current candidate.

## Goal

The Node Connector integrates with real Core enrollment and sessions, and real remote Docker Compose and rootless Podman Quadlet operations pass through Core. Remaining scope is assigned to v0.4.27; published historical slices are not automatically requalified for current source.

## Scope

- Baseline at the cut: Core `1aa1a503facc1f4cbbd58fab21619fda53ed6d47`, Console `0d7c8522ef91f0fc5af47cf6123868f73f543ed4`, Connector `572b81dab1e48ef7df18c4e40b038ba33e196827`; re-fetch heads. Pre-freeze: no legacy compatibility/migration/aliases; native standards first; preserve Core authorization, policy, ownership and secret safety. Follow-up to closed nc#1 and merged nc#2, not a second connector/control plane.
- Align targetaccess wire/session/bootstrap/stream definitions with the canonical versioned Core package/fixtures; keep descriptor vs transport explicit; detect drift automatically.
- Complete integration with real Core enrollment/CA authority and outbound session admission: identity, Target/runtime binding, version/capability negotiation, nonce/one-time token, trusted destination checks.
- Validate remote Docker Compose and rootless Podman Quadlet staging/apply/status/logs/metrics/exec/PTY/destroy through Core; the Connector never authorizes/selects placement or owns desired state.
- Request freshness/replay/idempotency for mutations, audit correlation, timeout/cancel, bounded concurrent streams.
- Renewal/rotation/CA overlap/revocation on new and active sessions with documented revalidation bounds, fail-closed.
- At-least-once log reconnect/replay with expired-cursor errors; a PTY disconnect cannot silently resume another process.
- Negatives: wrong peer/Target/runtime, rejected enrollment, unavailable Core, interrupted transfer, path/symlink escape, foreign-resource preservation, cleanup.
- Docs (README/TARGET-ACCESS/DEPLOYMENT) separate connector-side features from end-to-end supported operation; Windows cross-build is not runtime support.
- Out of scope: a mandatory connector for native Kubernetes/OpenShift, inbound management endpoints, generic shell, private-source publication.
- **Additional acceptance (comment 2026-10-08, planning only):** guided lifecycle `baha node add` on Core (name, runtime, one-time short-lived token) then `baha node connect` on the remote host (Core URL + secure token prompt): detect runtime, install/configure/launch the rootless connector service, enroll a locally generated key via pinned Core identity, verify mTLS, establish an outbound-only persistent connection, report READY. Core/CLI owns the user-facing commands and authorization; the connector repo owns packaging, service lifecycle, bootstrap and renewal/reconnect. Safe install/update/uninstall (no Go on the node), systemd user/lingering for rootless Podman, idempotent re-enrollment with explicit re-enroll/revocation policy, actionable diagnostics, no insecure TLS default, no token in argv/history/logs. `baha node list/status` shows liveness, trust/cert expiry, capabilities and disconnect reason. E2E between a Core Docker VM and a remote Podman VM (lab hosts named in the source), independent remote Target `podman-node-test`, preserving the existing `podman-test` Core. Cover first enroll, restart, renew, Core unavailable/reconnect, invalid/expired/used token, revoked cert, tenant mismatch, unsupported runtime, remote resource list/inspect and no silent local fallback. Coordinate with baseharbor#769, baseharbor#807 and console-2.

## Acceptance

- Shared golden fixtures + package tests/vet/build pass locally first.
- Real pinned Core → Connector → Docker and Podman gates pass with ownership/cleanup proof.
- Enrollment/reconnect/rotation/revocation/stream negative cases are executable and retained as evidence.
- Effective capabilities derive from the authenticated runtime, not static promises.
- Documentation and evidence correctly separate unit/fixture, cross-build and live runtime support.
- Not marked shipped without pinned cross-repo runtime evidence.

## Required checks

- `go test -race ./...`, `go vet ./...`, connector build; pinned live Core → Connector runtime gates.

## Dependencies and file ownership

- Connector repository; Core commands/authorization in baseharbor. Coordinate with v0.4.27 work area 1.

## Handoff

- 2026-10-06: draft PR [baseharbor-node-connector#4](https://github.com/mcpdev80/baseharbor-node-connector/pull/4) includes `46e9d269a59716c99a0379d553a399864f479c61` (strict enrollment identity installation and negative tests); source checks only, no remote runtime evidence. 2026-10-07: public-repo hygiene (LICENSE, SECURITY.md, public CI) done. Current README documents manual startup; the seamless guided lifecycle is not proven. The draft PR was last updated 2026-10-08; Maintainer to decide continue/close.
> Pre-research evidence retained (o64/o66/o68, console-2 PR #8, nc-3 PR pending): v0.4.26 ist noch nicht geschlossen (D2/W1/verify pending) => Release-27-Arbeit formal zurueck auf waiting, Outcome-Referenzen bleiben verlinkt.
> 27-PAUSE (Owner 2026-10-23): Arbeit ruht bis 26 geschlossen; laufende Research-Ergebnisse/PRs bleiben als Artefakte dokumentiert, keine weiteren Runden.

## 2026-11-07 Core-Connector E2E dependency (ChatGPT)

Core PR [#1438](https://github.com/mcpdev80/baseharbor/pull/1438), exact source head `7c9abb622acd431e450ca2252b58aa8fdd0f3702`, implements the Core-side enrollment, owner/tenant binding, remote CLI route and Docker/Podman CI contract tests. The updated Core native PR checks are **not** a full cross-repo native E2E claim. This card remains the existing **sole owner of final live Core -> separate Connector -> Docker/Podman acceptance** after the Core prerequisite is integrated, not a new parallel implementation lane. Reuse `internal/openbao/service_csr_native_connector_test.go` and `service_csr_native_connector_application_test.go` as the existing true live outbound-Connector/native-project proof; they explicitly do not qualify the actual `baha app up` CLI or the full protected API service lifecycle. Final acceptance must add those missing assertions with exact Core+Connector SHA, real native runtime, PASS-not-SKIP, authoritative status/doctor, negative OIDC, replay, resource preservation and cleanup. Current Core run [42423252917](https://github.com/mcpdev80/baseharbor/actions/runs/42423252917) still pending at time of note. Do not mark this card accepted from PR-only Core checks.

## 2026-11-08 – Core-Integration nach develop gemergt (ChatGPT)

- **PR:** [mcpdev80/baseharbor#1438](https://github.com/mcpdev80/baseharbor/pull/1438), gepruefter Head `7c9abb622acd431e450ca2252b58aa8fdd0f3702`, **Merge nach develop erfolgreich:** `0fe53052d00a8d440b499c66a6a65c0d54bae5a0`.
- **CI:** [Lauf #42423252917](https://github.com/mcpdev80/baseharbor/actions/runs/42423252917) auf exakt diesem Head terminal `success`, 20 erfolgreiche Jobs, 0 Fehler; native Docker/Podman Core-, OIDC-/Enrollment-, CLI-Vertragstests und Go-Pruefungen erfolgreich.
- **Abgrenzung:** Dies ist die integrierte Core-Grundlage, **nicht** der Beleg fuer automatisch verwalteten geschuetzten Operator-API-Dienst und realen `baha node connect` -> separaten Connector -> remote `baha app up/status/doctor` ueber Docker und Podman. Diese Release-Abnahme bleibt offen, insbesondere auf [0427-004](nc-3-core-enrollment-remote-runtime-acceptance.md). v0.4.27 ist **nicht** freigegeben.

### 2026-11-08 Docker2 E2E fehlender First-Owner-Pfad (ChatGPT)

- [Native Docker2 Evidence](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/e2e-abnahme/docker2.md) auf Core `0fe53052`: Bootstrap `baha up --control-plane-only` READY, aber erstes Operator-OIDC-Login `baha login -e dev --init-tenant` wurde nicht ausgefuehrt; folglich fehlten verifizierter Operator-User, Authority-Profil, echtes Node-Enrollment und erfolgreicher Remote-Up. `node add` und Wizard scheiterten korrekt fail-closed. Report-Labels `CELL 1 PASS`/`CELL 3 PASS` pruefen nur Teilgrenzen, **nicht** den E2E-Erfolg. Die bestehende Karte bleibt die Freigabe-Abnahme fuer echten First-Owner-OIDC (vorher Managed-Realm/Client, danach verifizierter First Owner), Connector und Remote-Deployment. Keine privilegierte Testidentitaet ohne Login im Produkt seeden.


## Release scope correction — 2026-11-13

Separate Core-to-Connector enrollment and remote runtime-host acceptance is v0.4.28 work. It is not needed when the selected Core itself runs Docker or Podman on the target VM.
