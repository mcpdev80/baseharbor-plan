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
**Required by:** [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261108-smoke-0427-operator-api-undocumented](t-20261108-smoke-0427-operator-api-undocumented.md), [t-20261108-smoke-0427-serve-enrollment-authority](t-20261108-smoke-0427-serve-enrollment-authority.md), [t-20261109-r27-local-delta-delivery](t-20261109-r27-local-delta-delivery.md), [t-20261109-r27-target-policy-presets](t-20261109-r27-target-policy-presets.md)  
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

## Native bootstrap marker diagnosis 2026-11-08

- Exact-head [#5319](https://github.com/mcpdev80/baseharbor/actions/runs/42512036786) FAIL in Docker and Podman native Keycloak/Core: `TestControlPlaneSingleDefaultNativeRuntimeInCI` could not read `baseharbor-bootstrap-cleanup-pending` before bootstrap. This is a shared test marker setup defect, not evidence of a product runtime failure.
- Root cause: the old PR head's `TestMain` did not enable the native acceptance marker cell, and `ensureRuntimeIntegrationTrustPlane` changed `XDG_DATA_HOME` after the package marker boundary. The fix was already on develop; copied that version of `cmd/baha/runtime_integration_test_support_test.go` into #1473 head `b14ed8372315e761d900f14e050afbae9970e462`.
- Fresh [CI #5320](https://github.com/mcpdev80/baseharbor/actions/runs/42512795402) initiated on that head; no PASS asserted until Docker and Podman checks truly execute successfully. Remote app apply/update/destroy E2E remains FAIL independently.

## Native integration proof 2026-11-08

- PR [#1473](https://github.com/mcpdev80/baseharbor/pull/1473), exact head `b14ed8372315e761d900f14e050afbae9970e462`, [CI #5320](https://github.com/mcpdev80/baseharbor/actions/runs/42512795402): native Keycloak/Core **Docker PASS / Podman PASS**; native destroy/retry **Docker PASS / Podman PASS**; source format, gofmt, go-build, go-vet PASS. Unit check was still running at inspection; final PR Selected Checks pending, so do not mark full CI PASS prematurely.
- These green native cells validate Core bootstrap and cleanup, **not** remote app lifecycle from a developer workstation. Keep the card open pending authenticated remote apply/status/update/destroy and real Docker-host proof.

## Go unit regression alignment 2026-11-08

- CI [#5320](https://github.com/mcpdev80/baseharbor/actions/runs/42512795402) completed FAIL only in `TestRemoteTargetSelectionDoesNotRequireOrBootstrapLocalCore`: test expected obsolete text `remote Core management connection`, while production returns actionable `remote management connection profile not configured (BASEHARBOR_CONNECTION_PROFILE)` (under typed authentication failure).
- PR #1473 head `e1b67be0f0f4400c51b6e6819d00e80425e7c0cf` now explicitly clears `BASEHARBOR_CONNECTION_PROFILE` in the test and checks that actionable missing-profile message. Production fail-closed behavior unchanged. [CI #5327](https://github.com/mcpdev80/baseharbor/actions/runs/42516611610) pending qualification.
- The remote developer-to-host application lifecycle is **not** proven by the unit correction; keep this card open until real E2E passes.

## Ready CI and Target tenant authority review 2026-11-08

- PR [#1473](https://github.com/mcpdev80/baseharbor/pull/1473) head `e1b67be0f0f4400c51b6e6819d00e80425e7c0cf`: [CI #5327](https://github.com/mcpdev80/baseharbor/actions/runs/42516611610) **PASS**, including all required checks. This qualifies the scoped Core identity/handshake patch, not the complete remote app lifecycle.
- Security review found `verifyRemoteManagementConnection` previously compared returned tenant to the profile only, not the configured selected Target. New head `d177ed15362ac1677a2afead8a573d9acfb8fff2` binds expected `ResolvedTarget.TenantID` explicitly and adds foreign/empty target-tenant regression tests. [CI #5341](https://github.com/mcpdev80/baseharbor/actions/runs/42529833874) pending on exact head.
- Still missing: dispatch of authenticated developer CLI application operations to Core Machine HTTP API and external developer-workstation E2E proof. **Do not close card or assert remote deployment PASS based on green CI alone.**

## Remote machine HTTP client seam 2026-11-08

- New PR [#1473](https://github.com/mcpdev80/baseharbor/pull/1473) code on head `70756f8175146a153898eeda531c6f34d1d61901`: reuse the authenticated, pinned TLS/OIDC Core connection as `verifiedRemoteCore`; negotiate semantic operations through canonical `GET /api/v1/machine/discovery`, reject discovered foreign execution URLs and unsupported contract versions.
- Introduced `requestMachineExecution` (canonical POST only) with explicit caller-provided stable idempotency key, matching Target/environment/application and strict relative Location validation. A 202 is **admission only**, never represented as operation success. Added negative tests for unverified sessions, forged binding/Location and wrong Target. No CLI application route has been switched over yet.
- [CI #5351](https://github.com/mcpdev80/baseharbor/actions/runs/42530971667) pending at time of update. Do not merge/close this card until this head passes required CI, CLI apply/status/update/destroy actually use the authenticated remote Core path, and the external workstation Docker E2E is verified.

## Machine HTTP transport qualification follow-up 2026-11-08

- Production seam added to #1473: reuse one verified, CA-pinned Core identity; retrieve canonical Machine discovery; submit an explicitly selected operation via authenticated POST with caller-supplied stable idempotency key and strict Target/Environment/Application/Location matching. A 202 is admission, never claimed READY or deployed. Test cases cover forged endpoint and Location, wrong Target and unverified session.
- Initial #5351 checks exposed a Go wrapper compilation error (wrong return arity), fixed at head `e23c32115cc0c7fd0ae405eaf918457fd4a2e804`. New [CI #5352](https://github.com/mcpdev80/baseharbor/actions/runs/42531128980) pending at update. This HEAD is not yet qualified.
- Still required: actual CLI routing of app apply/status/update/destroy, terminal execution status handling and real separate workstation-to-Docker-host E2E. Do not merge until that contract is demonstrated.

## Remote status CLI first slice 2026-11-08

- [CI #5352](https://github.com/mcpdev80/baseharbor/actions/runs/42531128980) completed **PASS**, exact head `e23c32115cc0c7fd0ae405eaf918457fd4a2e804`.
- New #1473 head `fe00f658e1349bd421c79e4ea5421f85822ef5b4`: `readMachineExecution` authenticates GET at pinned Core origin, validates immutable execution ID/operation/context and terminal state; no HTTP-202 acceptance as success, no foreign URLs. Negative/terminal-success tests added.
- The `app status NAME --environment dev` CLI route now explicitly detects a remote Target **before any local Core/runtime inspection**, verifies selected Target tenant/profile/OIDC, submits canonical machine `status` with unique idempotency key, and checks the terminal execution result. Refuses implicit NAME, non-dev sessions and missing Core profile without local fallback; tests added. This is a bounded first CLI slice, **not yet full remote apply/update/destroy or E2E proof**.
- [CI #5358](https://github.com/mcpdev80/baseharbor/actions/runs/42532145952) started on new head; required Go/native checks not yet qualified at update. Do not merge/close the card while remote mutations and physical remote READY/destroy remain unproven.

## CLI entrypoint and pinned execution completion 2026-11-08

- Previous PR [#1473](https://github.com/mcpdev80/baseharbor/pull/1473) head `e23c32115cc0c7fd0ae405eaf918457fd4a2e804`: [CI #5352](https://github.com/mcpdev80/baseharbor/actions/runs/42531128980) **SUCCESS**, including final PR selected checks.
- New head `79d46ea7002a38c4155fb17db289eff973d6da4d`: Remote Core machine execution completion now uses pinned authenticated GET on the canonical execution URL and verifies immutable operation/context/Target. Only terminal `succeeded` yields result; pending/failed/cancelled cannot be called READY. Tests include mismatched scope, failed and pending state, forged execution ID.
- `baha app status NAME --environment dev` explicitly routes via verified remote Core when the selected Target has a non-local AccessProvider; requires explicit NAME, only supports a verified dev session, returns machine status JSON and refuses local runtime fallback. Added simulated TLS Core handshake -> machine discovery -> execute -> read success test and CLI entrypoint negative test. **This is an incremental read-only slice**; no remote apply/update/destroy yet.
- Current [CI #5361](https://github.com/mcpdev80/baseharbor/actions/runs/42532306194) pending on this exact head. Keep the card active and remote-E2E FAIL until full application operations and separate-workstation native Docker E2E have real evidence.

## Status payload authority cross-check 2026-11-08

- PR #1473 current head `4cb549171f372d11f68955119ed2e2e51e255409`: remote `baha app status` now validates the actual application `StatusResult` v1 target/application/environment, in addition to the authenticated execution envelope. Even a successful execution with foreign status payload cannot be rendered as an authorized application's result.
- Remote status command preserves the local CLI's error semantics for failed readiness checks; tests include positive pinned TLS handshake -> discovery -> POST status -> GET terminal result and negative foreign Target status payload, as well as the negative entrypoint test without remote Core profile.
- New [CI #5365](https://github.com/mcpdev80/baseharbor/actions/runs/42532503957) triggered on this head. **Do not assert PASS until the exact-head run completes.** Remote app apply/update/destroy and real Dev-PC -> Connector Docker app E2E are still open.

## Authenticated remote mutation CLI 2026-11-09

- PR [#1473](https://github.com/mcpdev80/baseharbor/pull/1473) head `0e348b3ef16195b7cc9f04fe18d25e014cae7af4`: bound explicit remote `baha app apply NAME`, `baha app update NAME --no-backup`, `baha app destroy NAME --yes`, `baha app up NAME` and named root `baha up NAME` to the existing pinned TLS/OIDC Core Machine HTTP operations. Remote selections are resolved before local runtime paths; no local Docker fallback. Missing explicit application name fails closed. Only `dev` is supported until multi-environment OIDC qualification.
- Enforced request-scoped Target/tenant/application/environment, stable idempotency key and terminal execution result; HTTP 202 is never considered READY. Long-running mutation transport/observation now honors the Core's 30-minute execution budget. A transport timeout must NOT automatically resubmit mutations.
- Forward explicit `--confirm-candidate DIGEST` through `machineApplyInput` and Core candidate consent context. Explicit `--provider-consent-file PATH` is parsed as a strict bounded plan-bound `ProviderChangeConsent` (both stages mandatory), carried to Core for apply/destroy; Core still verifies the live plan and separate deletion approval. Update currently supports only explicit `--no-backup`, never assumes a password file path from the client exists on Core.
- Regression coverage includes fail-closed missing remote profile for all CLI mutation entrypoints, unsafe flag and consent cases, and mocked authenticated TLS Core apply/update/destroy terminal lifecycle roundtrips. **CI for this exact head is not yet confirmed green.**
- **Outstanding real-world acceptance:** No authenticated local-source transfer/registration from a fresh developer workstation to remote Core yet; `app.new` creates a new project on the Core, it does not import a pre-existing developer repository. No physical developer workstation -> remote Docker Connector -> app HTTP READY/update/destroy evidence. Do not merge/close card or declare remote E2E PASS until proven.

## Remote mutation retry safety 2026-11-09

- PR #1473 current candidate head `2e27907ddfefe14b26282678a800638ab4cc5a45`: the remote CLI accepts one explicit `--idempotency-key KEY` for deterministic retry after an uncertain mutation response. A generated request key is included in transport failure diagnostics; invalid/duplicate/empty keys fail closed. No implicit mutation retry. Regression tests added.
- Server `machineApplyInput.confirm_candidate` now passes the operator-confirmed exact candidate hash through BOTH Machine HTTP and MCP to the existing `withCandidateConsentDigest` boundary, rather than silently omitting repository candidate approval.
- The remote HTTP POST timeout is isolated from the short handshake timeout, with 31-minute limit for Core's 30-minute execution budget and a read-only terminal observation path. Two-stage plan-bound consent remains enforced by Core and is only provided from an explicit bounded JSON file.
- Do not close: current head still needs fresh required CI and real external developer-workstation -> Core -> Connector -> app apply/READY/update/destroy proof, including import/registration of a pre-existing developer repository.

## Remote stop parity 2026-11-09

- New #1473 head `708139ada019476bd421779654467d44b267552c`: explicit `baha app down NAME` on remote Target invokes authenticated Machine HTTP `app.stop`, including optional plan-bound provider consent file; validates terminal stop `state=stopped` with `data_preserved=true`. Remote selection never falls back to local runtime.
- Added TLS Core roundtrip and CLI negative regression tests for remote stop. `--yes` does not replace staged provider/consumer impact acknowledgements.
- Current head has no complete exact-head CI proof yet; previous [#5370](https://github.com/mcpdev80/baseharbor/actions/runs/42533302009) succeeded on an earlier SHA. Physical E2E and safe first-source registration remain open; no merge or card closure.

## Merge reconciliation and exact-head qualification 2026-11-09

- #1473 exact current head `708139ada019476bd421779654467d44b267552c`: remote application stop `app.stop` bound to `baha app down NAME` with staged provider consent and retained recovery proof; mocked pinned TLS Core roundtrip and CLI negative tests extended.
- Current PR state **Draft, mergeable=false** against `develop` (compare: 79 commits ahead, 59 behind at inspection). Branch reconciliation is required; do not squash/merge by force or infer compatibility from older SHA.
- [CI #5370](https://github.com/mcpdev80/baseharbor/actions/runs/42533302009) completed SUCCESS on older head `bc0cee720dc9bede904cc7e91d014fa31abfdc60`. The **current** head has no visible exact-head workflow result at inspection; status is not PASS.
- Product remains partial: existing Core-registered applications can use bounded authenticated remote lifecycle; importing a pre-existing workstation repository to Core and real workstation -> Core -> Connector -> Docker HTTP READY/update/destroy are not yet proven. Card stays active, not Done.

## Safe develop reconciliation 2026-11-09

- #1473 reconciled without force with current develop `20902f0a6ab016fd8fe6a501751e1becc5f334dd` through a genuine two-parent merge commit `82fe9120821f442332ed372958e08ba5d16df8c9`. All 23 PR file patches were applied onto develop, existing shared native-test fixture retained unchanged. The one overlapping `app_input_resolver.go` guard was merged to preserve **both** nonlocal app dispatch and the existing fail-closed remote control-plane bootstrap guard.
- Verified compare against develop: **ahead 80 / behind 0**, `mergeable=true` and both safety guards present. PR intentionally remains **Draft** because a fully valid remote source registration and physical E2E acceptance are outstanding.
- Fresh exact-head [CI #5372](https://github.com/mcpdev80/baseharbor/actions/runs/42535190815) started on integrated SHA. No PASS assertion until Go/native/selected checks complete.


## CI-Diagnose 2026-11-09 (PR #1473, Head 82fe9120)

- PR #1473 ist weiterhin Draft und mergebar mit aktuellem develop (GitHub-Compare: 80 ahead, 0 behind); die alte Konfliktmeldung ist damit ueberholt.
- Exakt-Head-Lauf [42535190815](https://github.com/mcpdev80/baseharbor/actions/runs/42535190815) **FAIL** im Job `PR · Draft focused checks` (128897829606), Grund: `gofmt -l` nennt `cmd/baha/management_remote_connection_test.go` und `cmd/baha/management_remote_mutation.go`. Andere Vollmatrix-Jobs sind in diesem Draft-Lauf SKIPPED, nicht PASS.
- Naechste Qualifikation: beide Dateien gofmt, neuer exakter Head, Ready-PR mit vollstaendiger CI; danach echte Remote-Source-Registrierung und separater Dev-PC -> Core -> Docker-Connector -> HTTP READY/update/destroy-Nachweis. Kein Merge und keine E2E-Abnahme auf Basis des Draft-Laufs.


## Remote source admission review 2026-11-09

- PR #1473 advanced concurrently to Ready at `9f29a0066b6a04b31d62b691ffa4224d63aed5a2`; full CI [42535614007](https://github.com/mcpdev80/baseharbor/actions/runs/42535614007) in progress at inspection. Do not edit the concurrently maintained PR branch blindly or claim PASS ahead of completion.
- Reviewed current `cmd/baha/machine_http_executor_platform.go`: `executeHTTPAppNew` invokes `development.CreateApplication` on the **Core host filesystem** using its supplied root; this creates a new generated application and is NOT an import/transfer of a repository from a developer workstation.
- Required source-admission design: explicitly transfer/admit existing portable Application Intent and workload sources through an authenticated, target/tenant-scoped bounded API; validate source digest and canonical application ownership on the Core before mutation, reject path traversal, symlinks, foreign repository and changed digest, and retain idempotency. Reuse existing app.adopt and source inspection contracts where feasible; do not treat arbitrary local `path` as a trusted Core path. Real external host E2E still needed.

## Exact-head CI after merge and terminal guards 2026-11-09

- Merged/reconciled branch with current develop via SHA `82fe9120821f442332ed372958e08ba5d16df8c9`, no forced ref update; comparison verified no commits behind develop and preserved both nonlocal app dispatch and no-local-bootstrap guard.
- Draft [CI #5376](https://github.com/mcpdev80/baseharbor/actions/runs/42535376141) failed due malformed duplicated code in `management_remote_machine.go`; repaired at `0ad30f1b2b87272a5096c3fda65a49b679e18b9e`.
- Latest candidate `9f29a0066b6a04b31d62b691ffa4224d63aed5a2` uses typed pending execution sentinel and rejects an unverified or operation-mismatched lifecycle receipt. Fresh Ready [CI #5379](https://github.com/mcpdev80/baseharbor/actions/runs/42535614007): source-format, gofmt, Go build/vet **PASS** at last inspection; go-unit-tests and native Docker/Podman Keycloak/Core + destroy/retry still running. No final selected-check verdict yet.
- This CI proves code-level contracts only. The existing developer repository transfer/registration and separate physical Docker-host E2E are not evidenced; keep card active and PR unmerged.

## Existing source staging reuse boundary 2026-11-09

- Existing accepted source pieces **already exist**: 0427-019 candidate packer [PR #1381](https://github.com/mcpdev80/baseharbor/pull/1381) and 0427-018 immutable candidate ingress [PR #1398](https://github.com/mcpdev80/baseharbor/pull/1398). Do not reimplement source packing or upload storage.
- Remaining integration gap for 0427-023 is narrower: the freshly connected remote developer CLI must invoke those existing source/candidate boundaries, retain exact source identity, and bind the server-side registered application to the selected Core/tenant/Target before apply. Current explicit `app apply NAME` assumes Core-registered source. Physical Docker-host end-to-end proof remains required.


## CI-Regression corrected 2026-11-09

- [PR #1473](https://github.com/mcpdev80/baseharbor/pull/1473) reached Ready at `9f29a006` but [CI 42535614007](https://github.com/mcpdev80/baseharbor/actions/runs/42535614007) failed `PR · Validation · go-unit-tests`: `TestRemoteMutationArgumentsFailClosed/apply/demo---confirm-candidate-bogus` accepted a malformed digest. Format, build, vet, native Keycloak/Core Docker+Podman and native destroy-retry were green in that run.
- Fixed `remoteMutationArgs` to require exact 64-character lowercase hex SHA-256 candidate confirmation. Test now supplies a canonical digest in the positive path; malformed `bogus` stays rejected. Commits: `10f57886` and `ec80ea74` on #1473.
- These commits require new exact-head CI; prior green jobs are not inherited as acceptance. Remote candidate ingest/source handoff and physical workstation-to-Docker lifecycle E2E remain open. Keep card active, no merge.


## Remote candidate argument hardening 2026-11-09

- On #1473 after digest-shape validation, added fail-closed duplicate `--confirm-candidate` rejection for both separate and equals variants; regressions included. Product commits `f560f1df` and `d20a88cd`.
- [CI 42536471426](https://github.com/mcpdev80/baseharbor/actions/runs/42536471426) is an earlier head and cannot qualify the latest duplicate-guard patch. Fresh exact-head CI required.
- Existing 0427-019 source snapshot captures metadata and bounded source-file identities but is not by itself a wire upload. Existing candidate ingress must be reused, not replaced; physical remote source-registration and lifecycle smoke remain outstanding. Card active, no merge.


## CI format requalification 2026-11-09

- On #1473 exact head `d20a88cd`, [CI 42536593588](https://github.com/mcpdev80/baseharbor/actions/runs/42536593588) showed `PR · Source format` and `PR · Validation · cli-gofmt` **FAIL** solely for `cmd/baha/management_remote_mutation_test.go`. The added `--confirm-candidate=` negative vectors omitted gofmt spaces around string concatenation; go-build/go-vet were PASS, full matrix had not reached terminal qualification at inspection.
- Corrected the Go source to gofmt-compatible string concatenation in new commit `1de087888c4b6c1db468be22535b7bcd21dc97a3`; exact-head CI still required. No release/merge claim.


## Exact-head CI and empty consent guards 2026-11-09

- [CI 42536954065](https://github.com/mcpdev80/baseharbor/actions/runs/42536954065) completed **SUCCESS** for #1473 head `1de087888c4b6c1db468be22535b7bcd21dc97a3`; this proves the prior remote lifecycle/argument regressions, not a live remote source import.
- Additional fail-closed audit found `--confirm-candidate=` and `--provider-consent-file=` with empty values could silently collapse to an omitted optional argument, bypassing an explicitly provided operator choice. New guards explicitly reject empty or duplicate flags, including mixed forms; tests added in commits `8d51ab8f` and `03af9f56`.
- Latest head `03af9f56ba9e91a8e914cc059ed66890aa671649` requires fresh CI. `develop` remains ancestor at review (94 ahead, 0 behind). PR must stay open; source registration and separate workstation-to-Connector E2E still outstanding.


## Remote-Source-Audit 2026-11-09 — actual code vs. prior ingress assumption

- Exact-head [CI 42539059547](https://github.com/mcpdev80/baseharbor/actions/runs/42539059547) was in progress at inspection for `03af9f56`; source format and cli-gofmt PASS, other selected validations still running. No inheritance of previous PASS.
- **Architectural correction (verified in code and prior PR changed-file lists):** merged 0427-019/#1381 adds only `internal/development/source_snapshot.go` and tests. `CaptureSource` produces identities/path/mode/count metadata, not the source bytes as an uploadable archive or authenticated transfer. Merged 0427-018/#1398 changes `cmd/baha/deployment_record.go` and candidate tests; it validates/retains consent for source identity, but does NOT implement a remote byte-ingress HTTP endpoint. Do **not** claim there is already a source-ingress to wire, or that `app.new` and `app.adopt` accept a developer workstation path as a remote file source.
- Existing `app.adopt` in `cmd/baha/mcp_adoption_tools.go` calls `persistRepositoryApplication` over a path on the execution host; `cmd/baha/machine_http_executor_platform.go` `app.new` also creates files on the execution host. Neither transfers local workstation sources. Remote CLI currently deliberately requires a preexisting Core-registered application, hence E2E registration is still not fulfilled.
- Implement *one* authorized source admission using established application/deployment identities, pinned candidate SHA and a bounded source transport. Suggested phases: (1) explicit source identity, max bytes, file and path restrictions, canonical tenant/target/installation authorization; (2) transfer exact content bytes or obtain verified immutable Git/OCI source; (3) atomic Core-side staging with digest and workload inspection and no overwrite of another owner's state; (4) only then authorize remote apply; (5) negative regression for traversal, symlink, stale digest, foreign tenant/target and interrupted upload, plus actual independent developer-PC E2E. Avoid a second independent receipt/protocol or implicit local Core fallback.
- Card remains **active**. No merge/E2E PASS until the actual source bytes (or verifiably resolvable immutable source) and lifecycle are proven.


## Remote managed Intent registration via Machine HTTP 2026-11-09

- #1473 now implements a **bounded first stage** of remote registration: `app.create` is in canonical `httpOperationKinds` and `executeHTTPAppCreate` routes a fully scoped Target/Application/Environment request to the already authorized `createMachineApplication` handler. Product commits `38a12698`, `55ab277e`; tests `3d4314be` cover foreign Target/app/environment, missing selectors, and discovery registration.
- This creates **target-managed Application Intent/identity only** (no local source bytes, filesystem transfer, or implicit Core path); it is deliberately not called `app.adopt`, not a completed repository-source import, and not a verified E2E deployment. Operator authentication/authorization and canonical identity persistence remain owned by existing server authorities. Exact-head CI required before claiming PASS.
- Remaining: developer CLI handoff for local repository source acquisition and authenticated bounded transfer/immutable source resolution, canonical Core workload inspection, physical remote Docker Connector READY/update/destroy smoke. Keep active and PR open.


## Remote CLI target-managed application creation 2026-11-09

- #1473 now routes `baha app create NAME` for a configured remote Target through the verified pinned Core Machine HTTP client rather than `createTargetManagedApplication` on the workstation. The Core HTTP `app.create` implementation reuses the existing authorized `createMachineApplication` identity authority; the CLI checks terminal execution and application/environment/ID/manifest receipt before reporting creation, no automatic mutation retry. Commits `91c95716` (CLI), `024e16ab` (client), `36c8946f` (TLS fixture roundtrip). HTTP handler/discovery and negative selector tests `38a12698`/`55ab277e`/`3d4314be`.
- This is a real, bounded **remote target-managed Intent registration** route, not repository adoption: `baha app init --quick` and a user's local workload bytes still need authenticated source transfer or verified immutable source resolution. These must not be inferred from `app.create` success.
- Full exact-head CI required on `36c8946f` and later changes; real separate developer workstation and Docker Connector E2E must still qualify. Keep card `active` and PR unmerged.


## UX/architecture decision: source, runtime and delivery are independent (2026-11-09)

- Owner requires the interactive first-run source choice `local | git | image`, persisted to avoid repeat prompts, with safe defaults; non-interactive CI must use unambiguous saved/explicit selection and fail closed on ambiguity. This is distinct from runtime choice.
- **Target determines both Runtime Provider and Delivery Provider.** Runtime may be Docker/Podman/Kubernetes/OpenShift; Delivery may be `direct` or `delegated` (e.g. Argo CD). A Git source is NOT synonymous with GitOps delivery, and Kubernetes YAML is NOT the only admissible source or delivery path.
- Reuse accepted [ADR 0011](https://github.com/mcpdev80/baseharbor/blob/develop/docs/decisions/0011-delivery-providers-and-tool-neutrality.md) and `internal/delivery.Selection` (`baseharbor.delivery/v1`): BaseHarbor owns portable intent, policies and semantic observation; a delegated GitOps reconciler exclusively owns the cluster resource mutations. Never run direct Kubernetes apply against delegated/ArgoCD-owned resources; reject conflicting owners fail closed.
- On delegated delivery, render/provide a pinned desired artifact/revision through the selected Delivery Provider, wait for external synchronization and verify the effective Application status; do not equate GitOps 'Synced' alone with BaseHarbor READY. Argo CD/Flux implementation is not automatically present just because Kubernetes manifest inspection is present. If Target advertises unsupported provider/runtime, fail clearly before writes and offer the required setup, not silent fallback to Docker/Podman/direct.
- Current scope for #1473 is target-independent source selection and safe dispatch/contract, plus actual Docker/Podman remote E2E. Do not falsely claim Kubernetes/OpenShift/ArgoCD execution complete; keep future provider realization assigned to separate conformance cards.


## ADR / roadmap reconciliation 2026-11-09

Rechecked product ADR 0007 (Runtime selected by Target, workload source separate), ADR 0011 (Runtime/Capability/Delivery orthogonal; one reconciliation owner), ADR 0017 (stable server-generated app ID, historical authored-ID wording superseded by v0.4.25), `docs/spec/delivery-provider-contract-v1.md` and `internal/delivery/contract.go` against `baseharbor-plan/ROADMAP.md`, `releases/v0.4.27.md`, `releases/v0.5.x.md`, `releases/v0.7.x.md`, core-325/v0.7.8, and core-318/v0.8.5. **No ADR conflict.**

Scope clarification for 0427-023: Source acquisition (`local | git | OCI-image`) is independent of Target-selected Runtime and Delivery; an existing Target selection is authoritative for direct/delegated mode, so the wizard must not demand a new delivery selection. Interactively ask only unresolved/ambiguous source choices and persist a reviewed selection; CI/noninteractive fails closed on ambiguity. Do not silently change target/runtime/delivery, infer Argo CD from a Git source or default a delegated target to direct. Source bytes or pinned native refs must follow authorized Core ownership. Do not create a new universal package format, mandatory registry, build farm, Git publisher, pipeline/controller or GitOps sync loop.

**Release separation:** v0.4.27 requires Docker/Podman direct remote lifecycle and a tested delegated *boundary/handoff* (0427-024 already accepted), not a live Kubernetes/OpenShift/Argo CD rollout. Existing 0427-019 snapshot packer/0427-018 candidate identity ingress are not an authenticated workstation byte-upload endpoint; choose existing native source/acquisition or artifact transfer mechanisms and add only a missing bounded adapter if the real user path requires it. The native delivery/stages planning decision explicitly prohibits automatic Git push/merge for delegated targets. Kubernetes foundations are v0.7.x, delegated/GitOps reference runtime core-325 v0.7.8, complete Kubernetes parity v0.8.x. Unsupported target/runtime/delivery combinations must fail before mutation with actionable diagnostics, never silently fall back. No change in existing card owners or downstream milestone placement.


## Completion audit 2026-11-09: exact-head CI, scope and remaining physical E2E

- Full previous-head [CI 42539410799](https://github.com/mcpdev80/baseharbor/actions/runs/42539410799) completed **SUCCESS** for `36c8946f4b98ccd9d5c5fe7a9f5458693920df83`, including remote `app.create` HTTP routing, guard tests, and selected native validation. That does not establish actual external workstation → Core → Connector app deployment.
- Added a fail-closed CLI entrypoint regression (`cmd/baha/app_create_remote_failclosed_test.go`, commit `456cde20`) to ensure a selected remote target with missing Core connection cannot create authoritative application deployment state locally, and cannot print a fake success. Fresh exact-head CI required.
- Re-verified `ROADMAP.md`, release `v0.4.27`, accepted ADR 0007/0011/0017, delivery contract, existing cards 0427-019 (source snapshot metadata only), 0427-018 (candidate identity/receipt), 0427-015 (native artifact selection), 0427-022 (CLI operations), 0427-024 (delegated handoff). Product source import should reuse native artifact, Git and workspace mechanisms; an authenticated bounded workstation payload admission is still missing. **Do not treat #1473 as completed just because remote managed intent creation and CI are green.**
- Missing acceptance: secure Local/Git/OCI source selection with persisted per-application preference and headless-safe behavior, real source/admission route for existing workstation files or resolvable pinned release, independent two-host remote Docker/Podman app READY/update/destroy proof, and final exact-head review. Existing spec forbids invented custom build service or automatic delegated GitOps push/merge. Card stays active and PR stays open.


## Implicit repository selector for remote CLI, 2026-11-09

- Addressed developer UX request for `baha app apply` without NAME when already in a repository. In `cmd/baha/management_remote_mutation.go` missing NAME now reuses existing `application.FindRepositoryManifest` / `LoadManifestFile`, selects only the local `Name` plus matching requested environment and sends no workstation path/source content/application ID to Core; explicit NAME retains precedence. Fail closed if missing/malformed `baseharbor.yaml` or environment mismatch. Product commit `8c2b132b`; focused new unit test `management_remote_implicit_name_test.go` at `28e7ebc9`.
- This makes **application selection** simpler; **source acquisition/deployment remains separate**, not solved by finding a filename. A remote app must still be registered on the owning Core, and the source bytes or immutable image must be admitted through a supported, authorized delivery path before application READY can be claimed. The source choice wizard for local/Git/OCI is still outstanding.
- Previous complete CI [42539410799](https://github.com/mcpdev80/baseharbor/actions/runs/42539410799) PASS on earlier head; new exact-head [42541121973](https://github.com/mcpdev80/baseharbor/actions/runs/42541121973) queued/pending at update, no PASS inherited. Keep active and open until independent workstation-to-remote Docker/Podman READY/update/destroy and source-admission acceptance.


## Reuse existing workspace source model (2026-11-09)

- Code recheck: `internal/development/source.go` already owns `.baseharbor/sources.yaml` (`SourceModelVersion=baseharbor.sources/v1`) and XDG-local workspace mappings. `SourceDefinition` supports `repository` (stable repository + ref) and `oci` (image ref), with component mappings; `cmd/baha/app_workspace_wizard.go` already offers existing local checkout/worktree or OCI image and prompts Git repository identity/ref for local worktrees. **Do not introduce a second stored Local/Git/OCI selection config or a second workspace wizard.** Refine this existing wizard's presentation to distinguish current checkout from an immutable remote Git source only when its acquisition semantics are implemented. Keep local absolute paths exclusively on developer machine, never part of portable intent or server-authoritative identity.
- The direct `baha app apply` no-NAME improvement on #1473 uses the local portable `baseharbor.yaml` only as a selector, not as a source-transfer or ownership grant. The existing SourceModel and XDG workspace mapping are the correct reuse points for the subsequent source choice; remote admission still needs bounded authenticated source/artifact resolution at the owning Core.


## Owner decision — Git/OCI only for remote deployment (2026-11-09)

**Supersedes all earlier suggestions in this card for a third `local` deployment-source option or authenticated workstation-source byte upload.** The remote deployment source choices are strictly:

1. **Git repository** — canonical source of truth. A selected repository revision is pinned to its exact commit SHA; no mutable branch/tag alone is accepted as deployment identity. Any uncommitted local changes are **not deployed**. Local worktree/checkout is permitted only as a developer-side workspace and for repository identity selection; no source bytes or local filesystem path travel to Core.
2. **OCI container image** — immutable release artifact pinned to its manifest digest (`@sha256:...`); a mutable tag alone is insufficient for an exact remote deployment.

Interactive first-use choice can be Git or OCI; reuse the existing `.baseharbor/sources.yaml` (`development.SourceModel`) and developer-local workspace mapping, with defaults and no repeated prompts. Noninteractive/CI must use an explicitly configured or unambiguous source, never guess or silently upload. A selected Target determines runtime and delivery (direct or delegated), independent of the source choice, per ADR 0007/0011 and the delivery contract. For delegated GitOps, do not push/merge Git or directly mutate externally owned resources.

**Scope removed:** local-worktree snapshot packaging/byte upload as a separate remote deployment path, an upload endpoint, and local dirty-state release publication. Existing local Docker/Podman development and workspace mapping stay supported; this decision affects only remote application deployment source. This explicitly resolves the earlier concern of having to build a workstation-to-Core source byte-ingress for #1473; such an endpoint is **not** an acceptance condition anymore. Replace its acceptance with exact Git revision/OCI digest resolution, authorized Core-side acquisition, immutable candidate binding, and genuine independent workstation → Core → Connector READY/update/destroy E2E. An existing local `baseharbor.yaml` may still supply only the application selector, never the deployment source itself. Existing historical notes above are superseded where they say Local/Git/OCI or require a source byte upload.

Card remains active, PR #1473 unmerged pending actual remote source resolution and physical E2E proof; do not claim those are implemented merely by revising the scope.


## Git/OCI immutable-source guard implemented (2026-11-09)

- #1473 now has a focused validator `internal/development.ValidateImmutableRemoteSources` for the *existing* `.baseharbor/sources.yaml` SourceModel. Remote Git refs must be a complete 40-character lowercase hex commit SHA; OCI refs must pin `@sha256:` with exactly 64 lowercase hex characters. Mutable branches, tags, malformed hex and short digests are refused. This does not add a third/local upload source, a second source model or a registry service. Product `ed556ffd`, tests `358f74db`.
- `remoteApplicationMutation` now calls `validateRemoteSelectedSources` before applying a matching current-repository model, using only local read-only manifest lookup and SourceModel parsing. It does not send file paths or workstation source bytes and it does not allow a local repository to override a separately selected registered remote app. Existing server-managed apps without a corresponding local source model are still supported. Production `37279d4d` + `09454821`, tests `6efba93a`.
- **Do not overclaim**: this is an immutable *local selection preflight*, not yet Core-side Git checkout/OCI pull, not proof of remote candidate digest binding, and not independent two-machine READY/update/destroy. Server authority must verify actual acquired Git/OCI artifact identity and retain its verified revision before mutation. Card remains active and PR #1473 unmerged until the actual end-to-end behavior is proven.


## Machine HTTP immutable-release handoff gap — code verified 2026-11-09

- Git/OCI preflight exact-head `6efba93a` encountered **PR Source format FAIL** (only `internal/development/immutable_remote_sources_test.go` via gofmt). Fixed on `f0d9a58b`; new CI [42541940685](https://github.com/mcpdev80/baseharbor/actions/runs/42541940685) pending/running at inspection. Do not carry forward earlier failed check as green.
- Read `cmd/baha/mcp.go:machineApplyInput` and `cmd/baha/machine_http_executor_lifecycle.go:executeHTTPApply` against `cmd/baha/management_remote_mutation.go`: **the current Machine HTTP `apply` request carries Target, Name, Environment, SkipMemoryPreflight, ConfirmCandidate and ProviderChangeConsent, but no immutable Git repository+commit or OCI image+digest.** The Core resolves an already registered server-side app and executes its existing source; a passing client-side SourceModel pin check cannot establish that Core deployed that selected pin.
- Minimum missing production handoff: add one typed immutable source selection on the existing application/candidate authority (not a new generic source server), validate Git URL and full commit / OCI repo digest on both ends, resolve and verify existence and content on owning Core through existing native Git/OCI/registry credential mechanisms, bind exact revision to canonical app/environment/Target/candidate and consent, perform authorized lifecycle only after verified acquisition. If source is absent or doesn't match selected Core state, fail clearly before mutation. No local source upload or automatic Git push/merge. Tests should include mutable ref, forged/unavailable commit, image tag, OCI digest mismatch, foreign tenant/app/Target, dirty local workspace irrelevance, interrupted acquisition, delegated owner/no direct mutation; plus real two-machine Docker/Podman E2E.
- Previous successful tests only exercised preexisting Core-registered apps; they **do not** exercise remote Git/OCI source admission. Keep card active and PR unmerged until proven.


## Fail-closed correction: pinned local selection cannot imply Core artifact delivery (2026-11-09)

- On #1473, `internal/development.ValidateImmutableRemoteSources` validates Git/OCI digest syntax locally but `machineApplyInput` still has **no source-binding field**, and Core executes its existing server-side desired source. A previously proposed 'validator passes, then apply' path could therefore silently deploy the wrong/stale Core source. This is a real product risk.
- Commit `ec7de000` changes matching local `.baseharbor/sources.yaml` remote apply to **fail closed even for syntactically valid pins**, with a precise unsupported Core-binding message; commit `5039a33a` updates negative regression tests. Existing previously registered Core-managed applications with no local SourceModel remain usable. This prevents a false success claim but is **not** a feature-complete source handoff.
- Previous CI [42541768334](https://github.com/mcpdev80/baseharbor/actions/runs/42541768334) reported gofmt FAIL for `internal/development/immutable_remote_sources_test.go` (corrected commit `f0d9a58b`). Fresh exact-head [42542063736](https://github.com/mcpdev80/baseharbor/actions/runs/42542063736) pending on `5039a33a` at inspection. No merge/close while actual Core-side acquisition/pin binding and physical E2E are missing.


## Typed immutable SourceModel in canonical Machine HTTP apply (2026-11-09)

- Reused the existing `development.SourceModel` as an **optional** `source_model` in the existing `machineApplyInput` contract (no second custom source schema, no local source upload, no new HTTP endpoint). Commits: schema `fedd9931`; single read-only local model extraction `bd317d44`; CLI payload `4d409bf1`; Core owner/immutability checks `ca4c3ae6`; tests `bd382527` and `96eaf1be`. The selected local source model does not grant authorization or application ownership.
- Core's `executeHTTPApply` now binds the canonical operation Target/Application/Environment, rejects foreign `source_model.application` and mutable Git branch/OCI tag before running any runtime operation. **A valid source still returns explicit unsupported** until a Core-side authenticated Git/OCI artifact acquisition and exact revision/candidate binding is implemented. This is intentional fail-closed behavior; do not report a working SourceModel→deployment E2E.
- CI [42542653160](https://github.com/mcpdev80/baseharbor/actions/runs/42542653160) found `gofmt` in `cmd/baha/mcp.go`, fixed at `60851a4f`. Fresh exact-head CI required; earlier run failure is not a product/remote runtime PASS. PR #1473 remains unmerged and 0427-023 active until actual Core artifact admission, real remote Docker/Podman READY/update/destroy, tests, and independent final review are complete.


## Remote source URL guard and schema tests 2026-11-09

- PR #1473 extended the existing immutable Git/OCI selector validation to reject workstation filesystem paths and `file://` URLs, plaintext HTTP/unauthenticated `git://` transport, URL-embedded secrets, query/fragment and whitespace. Only HTTPS/SSH Git repository identities with full pinned 40-hex SHA are acceptable. OCI digest references reject whitespace, query and fragment. Product `f1bacb7a`; new table tests `83943d8c`.
- This validation is applied at the developer CLI **and again by Core** for the new optional `machineApplyInput.source_model`. Its accepted syntax is not evidence that an artifact has been downloaded or matched to an installed runtime. Real Core-side Git/OCI candidate acquisition and runtime READY remain open.
- The previous exact-head CI 42542653160 found formatting issues in `cmd/baha/mcp.go`, fixed in `60851a4f`. Fresh exact-head CI [42542902338](https://github.com/mcpdev80/baseharbor/actions/runs/42542902338) queued at inspection on `83943d8c`. No completion, merge or external E2E claim before results.


## Machine HTTP immutable source payload tested (2026-11-09)

- The existing `machineApplyInput.source_model` now receives an immutable copy of `development.SourceModel` from the CLI via `remoteApplyPayloadWithSource`; there is no local workspace/path upload and no duplicated source schema. SourceModel serialization preserves Git repository+commit SHA or OCI image+digest and component mapping; duplicate `source_model` injection and mutable source refs fail closed. Code: `f2e23b46`, `3536486c`; tests: `e91cf2e1`.
- The Core validates source syntax and selected application scope, then responds explicitly `unsupported` for not-yet-admitted source artifacts before any mutation. Do not equate transport/validation with actual remote Git fetch, OCI pull, verified candidate receipt, or READY. Real Core-side artifact acquisition and candidate binding remain the next implementation milestone, as does independent workstation-to-Connector E2E.
- Fresh exact-head CI [42543000036](https://github.com/mcpdev80/baseharbor/actions/runs/42543000036) queued on `e91cf2e1` at inspection; no PASS claimed. Prior formatting issue `mcp.go` fixed in `60851a4f`. Card remains active, PR #1473 stays open.


## Source transport hardening + CI follow-up (2026-11-09)

- The optional immutable Git/OCI SourceModel now travels in the **existing** machine apply request with a focused payload helper. The test ensures the Git repo+full commit or OCI image+digest survives JSON encode/decode, with no developer-local XDG/worktree mapping. Rejected: mutable refs and duplicate source fields. Product `f2e23b46` + `3536486c`; test `e91cf2e1` (gofmt fixed `31772fd7`).
- Remote Git URL security allows HTTPS, SSH and passwordless enterprise SSH user identities, rejects local paths, insecure Git schemes and embedded credentials. Implementation `f1bacb7a`, refinement `dfaa24c6`, tests `83943d8c` + `5df59e94`. Core re-validates via the shared source validator before mutation. **This is an authenticated transport/validation milestone only; Git fetch/OCI pull and exact Core candidate persistence are NOT yet implemented.**
- Fresh CI [42543128465](https://github.com/mcpdev80/baseharbor/actions/runs/42543128465) queued on exact PR head `31772fd7` at last inspection. No fabricated PASS, merge or source E2E claim. 0427-023 remains active.


## Core-owned Git checkout and bounded pinned staging (2026-11-09)

- Added bounded read-only validation against **Core-registered repository state**, not developer-supplied paths or fetch URLs. `verifyCoreGitCheckout` checks registered source kind, real Git root, `remote.origin.url`, exact commit HEAD and clean tracked/untracked status before considering an apply. Code `7f1dd97d`; fixture tests `e357ab66`; handler preflight `af0b11b0`.
- Identified a TOCTOU risk: a mutable registered worktree might change after verification and before runtime materialization. The Core therefore **still refuses the mutation even for a matching clean checkout** until a transaction-owned immutable snapshot and Candidate Consent binding exist. Handler guard `6d48284a`, no fake READY. This preserves ADR one-writer ownership and Git source-of-truth semantics.
- Added `internal/development.StagePinnedGitTree`: native `git archive` at an exact 40-hex commit, bounded to 128 MiB/10,000 files and a short execution timeout; extracts only regular files and directories into a temporary Core-owned tree and rejects symlinks, hardlinks, special files, traversal and `.git` metadata. Code `02d1408d`; tests `1f187dcf` demonstrate dirty checkout changes do not enter the pinned export and unsafe archive entries fail closed. This staging helper **is not yet transaction-integrated**, and the temporary staging path is not treated as an accepted application Candidate.
- Remaining work: put staged content under the existing Core lifecycle lock, bind its Git revision/content fingerprint to the authoritative application/target/candidate + explicit consent, use that **same staged tree** for native Docker/Podman Connector materialization, verify observed digest/READY, implement OCI registry acquisition with digest verification and run independent external-workstation E2E. No automatic git push/merge, no local source upload, no new build farm or parallel delivery owner.
- Fresh exact-head CI [42543889377](https://github.com/mcpdev80/baseharbor/actions/runs/42543889377) queued on `1f187dcf` at last check. Previous workflow [42543128465](https://github.com/mcpdev80/baseharbor/actions/runs/42543128465) failed the selected-check aggregator because required native jobs were cancelled during successive pushes, not because all tests passed. Keep 0427-023 active and PR #1473 open.

## Git candidate staging and first remote registration gap (2026-11-09)

Owner scope: Git commit or OCI digest only, no workstation upload. Implement full lifecycle before release acceptance.
Added pure Core staging helper prepareStagedCoreGitCandidate (91e9d812, cleanup 727482e1, tests 9edca206). It verifies an already-registered Git checkout, stages exactly the immutable commit, checks the archived baseharbor.yaml against canonical Application ID, Target and Environment, fingerprints staged bytes and prepares the existing delivery.CandidateSubmission identity. Temporary files are caller-owned and failure paths clean up. It does not yet bind consent/persist a deployment or perform a runtime mutation.

Critical first-deploy gap verified in createTargetManagedApplication: first app.create persists DeploymentSource.Kind=managed with only a Core-owned source/baseharbor.yaml, NOT a Git checkout. verifyCoreGitCheckout currently requires Kind=repository and matching origin. Therefore fresh app.create -> app.apply remains unsupported. Do NOT mark complete merely because staging the prior checkout works.

Remaining implementation: authorize Git repository through existing tenant/organization source policy before privileged Core fetch (no arbitrary client URL / SSRF); perform credential-helper-backed native Git clone/fetch at an exact commit; stage and bind immutable tree to consent + canonical deployment record under application lifecycle lock; preserve exact staged artifact for Connector delivery and recovery. OCI needs authenticated digest/manifest verification and native image integration. Respect direct/delegated Target delivery and one reconciliation owner. Require physical independent workstation -> Core -> Docker/Podman Connector READY/update/destroy proof before acceptance.

Latest code head 9edca206, CI https://github.com/mcpdev80/baseharbor/actions/runs/42544549416 pending at inspection. Keep 0427-023 active, PR #1473 open and unmerged.


## CI review 2026-11-09 08:40 CET: git archive PAX header failure

- Exact PR head `9edca206` CI [42544549416](https://github.com/mcpdev80/baseharbor/actions/runs/42544549416) completed FAIL. Real failing jobs: Go unit tests in `cmd/baha` and `internal/development` (`TestPrepareStagedCoreGitCandidatePinsCanonicalApplication` and `TestStagePinnedGitTreeExportsCommitNotDirtyWorktree`), both rejecting the normal global PAX metadata emitted by native `git archive` as an unsupported TAR entry. This is a product bug, not a waived test.
- The same CI passed Source format, go-build, go-vet, cli-gofmt, focused Python, native Docker/Podman destroy retries, and native Keycloak/Core Docker+Podman. PR Selected Checks failed as a consequence of failed Go unit tests.
- Fix in `c9fa6127`: allow only global PAX `comment` metadata (commit identifier) and refuse unknown global metadata/path/link overrides; `9e1a8e26` adds positive Git PAX and negative path/link metadata tests. New exact-head CI [42580961985](https://github.com/mcpdev80/baseharbor/actions/runs/42580961985) pending at last observation. No claim of success before result.
- Keep card active and PR unmerged: the fix addresses native git archive parsing only, not remote source onboarding, immutable Core candidate consent/Connector binding, OCI source acquisition, or physical remote READY/update/destroy E2E.


## Follow-up code/CI review 2026-11-09

- CI 42580961985 on 9e1a8e26 failed `PR Source format` because pinned_git_archive_test.go contained an extra blank line (`gofmt -l`), and its `PR Selected Checks` aggregate therefore did not pass. Fixed gofmt in commit d86f703e.
- Reviewed `fingerprintStagedCandidate`: previously hashed file paths and bytes, but omitted the Git-tracked executable permission bit. Two different release trees (same bytes, different executable mode) could receive identical candidate fingerprints. Fixed in 7c5dcffa to hash the executable mode, while rejecting files replaced with symlinks/non-regular entries at hash time. Test added in 831bae43, test formatting fixed f3483c4a.
- New exact-head CI [42581333500](https://github.com/mcpdev80/baseharbor/actions/runs/42581333500) pending at observation. This is a hardening/fix iteration, **not** a validated remote end-to-end apply. Remaining first Git source authorization, transaction-bound staging/consent, OCI resolution and real remote Docker/Podman E2E remain open. Keep #1473 unmerged and 0427-023 active.


## Review 2026-11-09: exact-head Go unit failure

- PR #1473 head `f3483c4a` CI [42581333500](https://github.com/mcpdev80/baseharbor/actions/runs/42581333500) completed **failure**. All format, policy, build, vet, focused Python, native Docker/Podman destroy retry, and native Keycloak/Core jobs were green. The sole real failing test was `cmd/baha/TestRemoteAppCreateWithoutVerifiedCoreLeavesNoLocalDeployment`; Selected Checks failed transitively.
- Failure observed: missing `deployment` owner for Target in isolated fixture. Test previously asserted only the missing remote connection-profile diagnostic; actual owner guard can fire first. No successful local fallback occurred. Commit `11407ad3` adjusts test to accept either documented fail-closed owner refusal or missing Core connection, while preserving the assertions of no added local deployment records and no fake success output.
- New exact-head CI [42582726511](https://github.com/mcpdev80/baseharbor/actions/runs/42582726511) queued at inspection. No green claimed before it finishes. Card stays active and PR remains open pending actual Git/OCI source admission, candidate binding, Connector E2E and explicit release acceptance.


## Batched source-authority/format correction — 2026-11-09

- Owner requested **batch changes into one push**, no CI rerun for each file. The previous PR head `81e6d6ef` CI [42585958514](https://github.com/mcpdev80/baseharbor/actions/runs/42585958514) reported failed `PR Source format` and `cli-gofmt` for `management_core_git_candidate_test.go` and `management_core_source_binding_test.go`. The remaining native/unit jobs were still in progress at investigation; do not claim total pass/failure until complete.
- **One branch update** (`6fc29219`) corrects both formatting differences and closes a source-authority escape hatch: for an already Core-managed application with no registered `.baseharbor/sources.yaml`, a new workstation-only `source_model` is explicitly refused. A matching pinned registered source still resolves; existing legacy managed applications without a selected source preserve their existing path. The associated regression test ensures the foreign/unregistered selection fails closed.
- New exact-head CI [42586760494](https://github.com/mcpdev80/baseharbor/actions/runs/42586760494) pending at last check. PR #1473 remains **unmerged**, card 0427-023 **active**. This fixes admission-guard test/format issues, **not** the remaining authorized Git repository acquisition, persistent candidate/consent handoff, OCI registry admission, connector READY/update/destroy E2E.


## 2026-11-09 follow-up: protect update/repair against unbound source selection

- CI [42587978089](https://github.com/mcpdev80/baseharbor/actions/runs/42587978089) on `e0a6a6ba` passed Source format, cli-gofmt, Build, Vet, Trusted Plan, native Podman/Core and Docker/Core; Go unit was still running at inspection. Avoid claiming a full PASS before the workflow completes.
- One consolidated PR push `6e9a052f` adds `rejectUnboundRegisteredSourceMutation` in the existing Core source registration layer and applies it at the real HTTP `update` and `repair` boundaries. When a Core-managed app has an immutable `.baseharbor/sources.yaml`, neither operation can silently use the old managed runtime bypassing the yet-unbound Candidate+Consent. Existing managed apps without a pinned source remain unaffected; the regression covers both cases. Destroy/cleanup is not covered by this prohibition.
- Important: this remains a deliberate fail-closed safety step. Authenticated Git/OCI artifact acquisition, persistent consent tied to the staged byte tree, physical Connector delivery and real READY/update/destroy E2E are **still outstanding**. Keep PR #1473 open and this card active. One batch push, not per-file pushes.


## Produktentscheidung 2026-11-09 – lokale Dirty-Deltas statt Core-Git-Clone

Verbindliche Richtung: [Decision](../decisions/2026-11-09-r27-local-delta-delivery-and-target-presets.md), [Issue #1513](https://github.com/mcpdev80/baseharbor/issues/1513). Default `baha app apply` nimmt den tatsächlichen lokalen Arbeitsstand (inklusive nicht commiteter Dateien) und nutzt bestehenden autorisierten Candidate-Ingress, Content-Fingerprint und inkrementellen Transport. Core-seitiger Remote-Git-Clone und SHA-only-Candidate sind **keine** notwendige Entwicklungsquelle. Ziel-Policies kommen als editierbare Best-Practice-Wizard-Presets und Core-seitige Autorisierung, nicht als harte Namens-/Umgebungsverbote. Vorhandene OCI-Transferfunktionen reuse; kein eigener Delta-/Registry-Standard. Git SHA/Branch sind Metadaten. V0.4.27 nur Docker/Podman, Kubernetes/OpenShift später. **Akzeptanz weiterhin offen**: reale unabhängige Dev-PC -> Core -> Connector -> READY/update/destroy und 2. Apply nur geänderte Bytes, negative Policy/Auth-/Tamper-Tests, CI exact head. Unveränderten Status `active` beibehalten; kein Merge-PASS ohne Nachweis.


## 2026-11-09 – Direct Core-owned Docker client route

- Product-owner clarified that independent developer workstation -> authenticated Core -> Docker on the **same Core VM** needs no separate Node Connector. Node Connector remains for remote runtime hosts, not as an artificial extra dependency for Core-local execution.
- Remote Core client Target provider `baseharbor-core` implemented in PR #1473 (`d174ae0a`), with explicit `--tenant-id UUID` in `baha target create`. This is a **client-only access route**: `baha use` verifies existing pinned HTTPS/OIDC profile + tenant and cannot bootstrap a second Core or run workstation Docker. The Core-side Machine HTTP executor stays bound to its existing `local` installation Target.
- Regression covers client tenant mapping, missing-profile rejection and no local Docker fallback. EN/DE target documentation added `78e45485`. Source-format gofmt correction `95a3976e`. Exact-head CI pending after new validation branch ref.
- Prior temporary `37c3d680` Git/OCI-only change was fully reverted in `c2ac5b2b` after verifying the newer accepted product decision #1513: **developer dirty/untracked delta source delivery is the intended dev default**, with user-editable target policies (test clean by default). Do not remove working-tree source transfer based on stale Git-only handover.
- Actual Core-local remote apply and second delta/destroy are NOT YET proven. Preserve working VM Core, tenant, OpenBao, Keycloak and TLS; avoid installing unrelated Connector for same-host smoke. PR #1473 remains active/unmerged; no release acceptance claim.

## 2026-11-09 – Remote HTTP app.create source binding regression fix

- PR #1473: `executeHTTPAppCreate` decoded `machineApplicationCreateInput.SourceModel` but called `createMachineApplication`, silently dropping the source model. Fixed at `5e631181` to pass the model to the existing `createMachineApplicationWithSource` authoritative validation/persistence path.
- Regression test added at `aa7bbac8`: mutable Git ref `main` must fail with `ErrorValidationFailed` at the real HTTP create boundary before registration; the test does not imply a runtime deployment proof.
- Follow the latest approved dev delta and Target preset decision (#1513); the earlier Git/OCI-only PR prose was corrected. Do not remove the existing authorized developer delta source-transfer path.
- Still OPEN: branch reconciliation with develop (10 overlapping changed files at inspection), exact-head CI, and physical independent Dev-PC -> Core-local Docker -> application READY, second delta apply, update and destroy. Do not merge or mark the smoke PASS. No live VM changes were made.

## 2026-11-09 – Rebase qualification and CI corrections

- Owner's true rebase finished at `03c12b93db5e5bbabeae72460b33b058a51fc7cd` on `develop` `d2e225f2000b88ee255559b0cc3f9ac51c225e7e`; GitHub confirmed mergeable before follow-up commits. Four conflict resolutions; local build/vet/test compilation PASS per handoff, full Go tests delegated to CI.
- Exact-head Ready CI `42687471705` revealed two concrete failures: `PR · Source format` because `cmd/baha/app_context.go` had 807 lines (800 limit), and `PR · Validation · pr-planner-tests` because the generated EN CLI index was missing `--tenant-id UUID` in `baha target create`.
- Fixed by moving `resolvedApplication.ResourceLabel()` to `cmd/baha/app_context_resource_label.go` (`29ac9d44`, `bc0e6d42`), and aligning both EN/DE command indices with actual CLI Usage (`e480f05e`, `d1965fa4`). No application behavior changed. Fresh CI is required on the new exact head; earlier in-progress jobs do not qualify the new commits.
- Remains active/unmerged: full exact-head CI, physical independent developer workstation -> authenticated Core -> Core-local Docker -> application READY, second delta apply, update and destroy. Preserve VM and security/tenant state.

## 2026-11-09 – CI native second-Core regression after rebase

- CI #42688295995 at HEAD `89520362` had one failed native Docker destroy-retry job: `TestSecondSameHostCoreNativeConflictInCI` asserted two different selected Target identities but called `isolateRuntimeForTest`, which by design always selects the **same** package-owned bootstrap Core Target after the newer isolation changes on `develop`.
- Fixed in PR #1473 commit `2bc0de6c`: negative test now registers a distinct second local Target on the same runtime engine without `--default`, selects that Target explicitly, and verifies selection before the same-host Core conflict check. Production Core implementation was not changed. Existing first Core remains test-owned; no VM smoke run.
- CI must qualify the **new exact head**, including Docker and Podman negative native checks; no merge claim from the old failed run.

## Integration status 2026-11-09

- PR [#1473](https://github.com/mcpdev80/baseharbor/pull/1473) merged into `develop` at `6b1838ee38bed120f4af0770a84ac2d1880094ff` after exact-head green CI. This is code integration, **not** a successful independent workstation smoke test; no physical VM changes or E2E READY proof have been reported.
- Other completed integration steps: #1512 (`bc839f05`), #1518 (`cb30f7a6`) and #1491 (`14c5922c`) merged on fresh green CI. #1514 policy presets, #1470 credential recovery and #1503 native Greenfield proof remain separate Draft PRs pending acceptance. Smoke must be performed on an intentionally selected develop build and its result recorded before treating this card as accepted.

## PR #1521 continuation — 2026-11-10

- Product PR #1521 is open at exact head `1f23746686b70e7e2825b4adf3a70c86c21c6290`. The developer workstation CLI has the same build installed. Remote `app create`, `app plan`, `app status`, `app doctor`, and `app preflight` had passed against the Core before the apply attempt. Apply was sent with current explicit provider-impact consent; no runtime containers were created and Core still reports the application as created.
- The live workstation certificate is now listed in the Core OpenBao CRL as revoked. Subsequent Core requests correctly fail closed with HTTP 401, so status/doctor/destroy cannot be completed from this identity. The revocation check itself was verified against the signed CRL. The path that caused the revocation during the apply attempt is still under investigation; do not report the live deployment or cleanup acceptance as passed.
- Exact local checks on `1f237466`: `go test ./internal/onboardingbundle ./internal/sourcetransfer ./internal/openbao -count=1`, focused CLI routing/onboarding/docs tests, `go vet` on touched packages, Go build, and `TestExtractDroppedTablesRequiresDropTableClause` passed. The broad `go test ./cmd/baha -count=1` failed in host-native tests because this workstation's existing Docker network has no protected Core/shared-backend owner; it is not a clean isolated runtime fixture.
- CI evidence: workflow dispatch `42856283862` is still running but skips PR-selected Go/native jobs because it is not a pull-request event. Manual Docker acceptance `42856724053` is still running. Manual Podman acceptance `42856722970` fails at its pre-bootstrap Doctor probe because `unix:///var/run/docker.sock` is unavailable even with the Podman runtime selected. These are not full exact-head PR-CI evidence. The preceding PR run at `f613f398` also failed the generated command-index and migration rollback assertions; both false-positive sources are corrected on `1f237466`, pending an exact-head PR-event CI run.
- Decision: retain `kanban_status: active`. Acceptance remains open for a new valid workstation identity, apply-to-READY, status/doctor after apply, and remote destroy/ownership verification, plus exact-head PR CI and native Docker/Podman confirmation. PR #1521 is not merged.
