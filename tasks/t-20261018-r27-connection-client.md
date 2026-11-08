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
