---
id: t-20261018-r27-onboarding-wizard
card_number: "0427-043"
card_short_title: "attach a workstation with"
areas: [wizard]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: "coordinator"
kanban_lane: closed
kanban_summary: Native success continues silently; import one trusted device bundle or non-secret team profile and authenticate only as policy…
kanban_status: closed
kanban_title: "0427-043 · attach a workstation with"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-client-commands, t-20261018-r27-device-lifecycle, t-20261018-r27-profile-codec, t-20261018-r27-secure-export, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1435, mcpdev80/baseharbor#1438]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/e2e-abnahme/podman2.md"]
wait_reason: ""

---

- [x] t-20261018-r27-onboarding-wizard · Onboarding: attach a workstation with minimal questions #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** normal  
    **PR:** [baseharbor#1435](https://github.com/mcpdev80/baseharbor/pull/1435), [baseharbor#1438](https://github.com/mcpdev80/baseharbor/pull/1438)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/e2e-abnahme/podman2.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-device-lifecycle](t-20261018-r27-device-lifecycle.md), [t-20261018-r27-profile-codec](t-20261018-r27-profile-codec.md), [t-20261018-r27-secure-export](t-20261018-r27-secure-export.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md)  
**Owner:** coordinator  
**Priority:** normal  
**PRs:** [baseharbor#1435](https://github.com/mcpdev80/baseharbor/pull/1435), [baseharbor#1438](https://github.com/mcpdev80/baseharbor/pull/1438)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Native success continues silently; import one trusted device bundle or non-secret team profile and authenticate only as policy requires. Distinguish bootstrap from attach; never install duplicate services when joining. Provide explicit existing-app attach versus new app, path remap and session-only/secure choice. Back/cancel/EOF never mutate.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

bounded connection import/export/onboarding wizard files/tests; existing presentation/controller APIs; no central registry edits. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Actual wizard entry tests for both connection modes, repeated operations/no re-prompt, invalid imports/conflicts/cancel; no runtime. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

END geliefert, ABER NICHT review-ready: DRIFT (develop 8a3f58da9) + KOLLISION mit #119 (application_registry_source.go + internal/orgconfig/source_oci.go + application_registry_pull_error_test.go sind #119 owned, deren lane 27494182 laeuft parallel dort). onboarding besitzt NUR onboarding.go/connection_profile_codec.go/internal/onboardingwizard/*. CI 9-pass (registration ok). korrektur: rebase + #119-dateien raus. karte active.

r2 drift-frei (head 09ec640b2, develop 8a3f58da9 merged, ancestor rc0). delta NUR 5 eigene onboarding-dateien (OCI-kollision als lag-artefakt aufgeloest, bytegleich develop). CI run 42395810316 terminal 9-pass, zaun+registration gruen. CODEX-REVIEW. lane geliefert.

r2 review REQUEST-CHANGES (bundle-import dead end + root registration/classification/command-index fehlt). r3 korrektur auf freiem ornith-sitz. karte active MIT worker.

- 2026-11-07 Ergaenzung aus 0427-116: PR #1435 implementiert den Workstation-Onboarding-Wizard mit Installation, attach/import, App und Persistenz, **aber bisher keine Entdeckung/Initialisierung einer verifizierten Operator-Tenant-Membership**. Fuer einen frischen lokalen Management-Core muss die Erst-Owner-OIDC-PKCE-/Tenant-editor-Zuordnung aus Core-PR #1437 nach expliziter Zustimmung angeboten werden; vorhandene Memberships werden verifiziert und still wiederverwendet. Attach/import duerfen keinen Tenant erzeugen; eine TrustedLocal-Verbindung darf die Operator-/Tenant-Authorization nicht umgehen. Cancel/EOF = keine Mutation. Node-Enrolment bleibt im bestehenden JSON-Vertrag von `baha node add/connect`, kein neues Workstation-Bundle dafuer. [Auftrag an PR #1435](https://github.com/mcpdev80/baseharbor/pull/1435#issuecomment-6711528355); Owner `lane-0427-043-onboarding-r3` bleibt zustaendig. Card `active`, noch keine Umsetzung oder Abnahme behaupten.

- **2026-11-07 Produktentscheid: DEFAULT FIRST, ADVANCED OPTIONAL.** Grundsatz `so wenig wie moeglich, so viel wie noetig`: Wizard bietet einen vollstaendigen sofort verwendbaren empfohlenen Pfad, ohne Fragen zu vorhandenen Core-/Trust-/Tenant-Details. Beispiel-Default bei frischer Installation: Tenant-Name/Slug `baseharbor`, UUID wird generiert; Installation, Operator-OIDC-Realm/Client, Endpunkte und Trust nach echten Fakten und sicherem Vertrag ableiten. **Jeder** konfigurierte Wert darf im erweiterten Pfad individuell gesetzt werden, soweit vom Vertrag unterstuetzt (Tenant-Name/Slug, Identity-Provider/Realm-Client, relevante Endpunkte/Trust, Runtime/Target); der Wizard zeigt Defaults und validiert Eingaben vor Commit. Operator-Tenant ist installationsweit und **nicht** an `dev` gebunden. Der sichere First-Owner PKCE-Proof und bewusste Zustimmung bleiben zwingend; Existing/Attach/Import verwenden vorhandenen Tenant unveraendert, nie heimlicher Owner-Transfer. Abbruch = keine Mutation. Tests fuer Default, Custom, Bestehendes und Negativfaelle. Umsetzung PR #1435 in Abstimmung mit #1437; [PR-Auftrag](https://github.com/mcpdev80/baseharbor/pull/1435#issuecomment-6711558947). Noch offen, `active`.

HANDOVER an Owner+ChatGPT (Owner-Direktive 2026-11-07): r2-PR#1435 head 09ec640b in review-REQUEST (root registration/classification/index offen); r3-wip 0d60f6b5 auf refs/heads/lane/0427-onboarding-r3 (bundle-import durch enrollment-seam, tests lokal gruen). Handover-comment auf PR. Evidenz round-2/round-3 auf origin/main. Worker-lane freigegeben, keine weiteren lane-aenderungen.

- **2026-11-07 Uebernahme und Integration:** Codeman hat die Worker-Lanes gestoppt und den finalen SHA-/Evidence-Stand in den bestehenden PRs dokumentiert. ChatGPT hat die unveraenderten R3-/R4-Worker-Artefakte, den Operator-/Tenant-Bootstrap und den Remote-App-Start im [Integrations-PR #1438](https://github.com/mcpdev80/baseharbor/pull/1438) zusammengefuehrt. Aktueller Integrations-Head `7f8fee2f6091a9eb5d3d0d4686ad51eb9ddc8951` mit erfolgreichem hosted CI-Lauf [42404964550](https://github.com/mcpdev80/baseharbor/actions/runs/42404964550). **Status bleibt active**: Default-/Advanced-Wizard, aus verifizierten Core-Daten automatisch befuelltes Enrollment-Bundle sowie echter Docker-/Podman-E2E-Nachweis muessen noch funktional endabgenommen werden. Keine Freigabe fuer Merge/Release allein aufgrund der CI-Matrix. Dieses Integration-PR ist die gemeinsame Arbeitsquelle; Ursprungs-PRs bleiben unveraendert zur Rueckverfolgbarkeit.

- **2026-11-07 Integrations-CI (ChatGPT):** Die Integration auf [Core-PR #1438](https://github.com/mcpdev80/baseharbor/pull/1438) umfasst nun `baha onboard` Default/Advanced samt verifiziertem Keycloak-PKCE/Initial-Tenant (`baseharbor` oder custom), API-Bindung an den Operator-Issuer/Client, Tenant-Aufloesung aus Core-authentifizierter Membership, Core-seitiges public-Endpoint/CA-Profil und ein dateibasiertes One-Time-Node-Enrollment. Ein eigener PR-CI-Pruefblock verlangt exakt PASS fuer neun relevante Tests inklusive echter PostgreSQL-Transaktion (nicht nur go test Exitcode), und der vorhandene CI-Workflow wurde um gezielte native Docker-/Podman-Keycloak+Core-Jobs fuer betroffene PR-Dateien erweitert. Integrations-Head `fbc0d9d153482be27979fd6b31897eb6ad2f53ab`, nativer [PR-CI-Lauf #42407311186](https://github.com/mcpdev80/baseharbor/actions/runs/42407311186) **noch nicht abgenommen**. Echte durchgehende Remote-Connector-/App-E2E-Ergebnisse (Docker und Podman) bleiben verpflichtend; keine Release-/Merge-Freigabe ohne belastbare PASS-Ergebnisse. Karte `active`, nicht `done`.

- **2026-11-07 First-install Korrektur (ChatGPT):** Der bisherige `ModeBootstrap`-Wizard war beim `AppNew`-Pfad ein No-op. Im [Integrations-PR #1438](https://github.com/mcpdev80/baseharbor/pull/1438) startet er jetzt nach dem bestaetigten Review die bestehende `baha up --control-plane-only`-Authority und anschliessend die verifizierte Keycloak-OIDC-PKCE-/Initial-Tenant-Erstellung; fehlgeschlagener Core-Start verhindert jegliche Owner-Mutation. Default-Tenant `baseharbor`, optional eigene Namen. Native Docker/Podman-PR-CI sowie PostgreSQL-Regressionen werden am finalen Head ausgefuehrt; noch **keine echte Node-connect/App-up-End-to-End-Abnahme**, daher Karte `active` und kein Merge. Letzter Integrations-Head `58bbaed713576adfc60943e9b621818d63e6e4f1`.

- **2026-11-07 Letzte E2E-Luecke:** Der geschuetzte Core-Operator-HTTP-Server hat einen separaten `baha serve`-Lebenszyklus; die bisherige `baha onboard`-Ersteinrichtung konvergiert zwar Core (`baha up --control-plane-only`) und verifiziertes Keycloak-/Tenant-Onboarding, aber die sichere automatische Aktivierung des Operator-/Connector-Servers, sein erreichbarer TLS-Endpunkt und die echte `baha node connect FILE`-bis-`baha app up`-Kette sind noch NICHT in beiden Runtime-Varianten als durchgaengig PASS nachgewiesen. HTTP-Route `GET /api/v1/connectors/owner-context` ist in Core-PR #1438 jetzt explizit hinter OIDC im Operator-Mux registriert (Head `be266a7afa1549549ed6d5e58076df960aeacce5`). Status `active`, keine falsche Fertigmeldung/kein Merge; native Job-Ergebnisse unter [CI #42408115747](https://github.com/mcpdev80/baseharbor/actions/runs/42408115747).

- **2026-11-07 native CI failure (ChatGPT):** Native Docker/Podman-PR-CI #42408115747 scheiterte nach erfolgreichem Keycloak-Lauf identisch bei `TestControlPlaneSingleDefaultNativeRuntimeInCI`: Test las absichtlich nicht konfigurierten `w169-isolation-required-*`-Guard-Target statt eines echten eigenen Core-Targets. In [Integrations-PR #1438](https://github.com/mcpdev80/baseharbor/pull/1438) wurde der Test korrigiert: `isolateRuntimeForTest` erzeugt jetzt einen separaten Target; `baha up --control-plane-only --yes` startet dort den realen Core, dessen Runtime danach erst geprueft wird. Exakter Code-Head `8eeb620001e1533ecc1f37a497a7e48122a5c7bb`, neuer [CI-Lauf #42418160655](https://github.com/mcpdev80/baseharbor/actions/runs/42418160655) zum Zeitpunkt der Bearbeitung noch aktiv. Keycloak-/Core-PR-Test darf nicht skippen; volle Remote-Node-Enrollment- und `app up`-Akzeptanz auf Docker/Podman fehlt weiterhin. Karte active, kein Merge.

- **2026-11-07 native CI-Nachpruefung (chatgpt-0427-116):** Auf Core-PR #1438 mit Head `8eeb620001e1533ecc1f37a497a7e48122a5c7bb` ist der zuvor fehlgeschlagene Test `TestControlPlaneSingleDefaultNativeRuntimeInCI` korrigiert: Er erzeugt jetzt einen eigenen isolierten Target, startet dort `baha up --control-plane-only --yes` und prueft erst dann die laufenden Core-Ressourcen. Im [CI-Lauf #42418160655](https://github.com/mcpdev80/baseharbor/actions/runs/42418160655) sind **native Keycloak+Core Docker und Podman beide PASS**. `go-unit-tests` lief beim letzten Abruf noch; die E2E-Kette Core API -> `baha node add` -> Bundle -> `baha node connect` -> Remote-`app up` braucht weiterhin separate echte native Abnahme. Die develop-Impact-Klassifikation fuer Identity/Node ist als noch nicht gepushter Folge-Commit `c3e7a557df3243078499e803f24fc7b7f0b33b1d` vorbereitet (wird erst nach exaktem CI-Head-Lauf vorgerueckt); keine Behauptung einer Freigabe oder eines Merges. Status `active`.

- **2026-11-07 native selector follow-up (ChatGPT):** Core-PR [#1438](https://github.com/mcpdev80/baseharbor/pull/1438) erweitert auf Head `4b656481e20f5f3c223d30cbdf511ae7d2158d7c` die develop-Impact-Selektoren fuer OIDC/Keycloak, Operator-Tenant, Onboarding, Core-API, Node und Remote-App; `scripts/test-ci-impact-selectors.sh` wurde als Regression hinzugefuegt und in die verpflichtende native Docker/Podman-CI eingebunden. [Neuer CI-Lauf #42419767443](https://github.com/mcpdev80/baseharbor/actions/runs/42419767443) gestartet, noch **nicht** endgueltig abgenommen. Der alte Head `8eeb6200` hatte einen vollstaendigen erfolgreichen Go-/Docker-/Podman-PR-Lauf #42418160655, jedoch ohne Remote E2E. Geschuetzter Core-API-Autostart/Health sowie die reale Node-Enrollment-bis-Remote-app-up-Kette fehlen als PASS-Nachweis; Karte bleibt `active`, kein Merge/Release.

- **2026-11-07 Core API Konfigurationsfix (ChatGPT):** Integrations-PR #1438 Head `5fb2bb2680f3810290a58cf49aa121fac4085596`: `baha serve` reicht den expliziten Workstation-Enrollment-Schalter `BASEHARBOR_WORKSTATION_ENROLLMENT_ENABLED` jetzt an die bestehende geschuetzte Serverkonfiguration (`WorkstationEnrollmentEnabled`) weiter, inkl. true/false-Regressionstest. Neuer exakter CI-Lauf [#42420199089](https://github.com/mcpdev80/baseharbor/actions/runs/42420199089) noch offen. Der automatische geschuetzte API-Lifecycle und die echte Remote-Node-E2E-Abnahme fehlen weiterhin; Karte `active`, kein Merge.

- **2026-11-07 OIDC-Fail-Closed Erweiterung (ChatGPT):** Integrations-PR #1438 Head `bd4b46cea6a4a6a94112f97908c383bc569d2298` bindet jetzt auch `WorkstationEnrollmentEnabled` an den verifizierten Core-Operator-Keycloak-Realm; vorher galt `bindServeToOwnedOperatorOIDC()` nur bei Node-Enrollment. Negative Tests fuer nicht eingerichtete/abweichende Autoritaet hinzugefuegt. CI [#42420267191](https://github.com/mcpdev80/baseharbor/actions/runs/42420267191) noch nicht abgenommen. Nach ADR 0015 wird eine echte Lifecycle-Verwaltung und E2E-Akzeptanz benoetigt; Status bleibt `active`, kein Merge.

- **2026-11-07 Node-CI-Ausbau (ChatGPT):** Core-Integrations-PR [#1438](https://github.com/mcpdev80/baseharbor/pull/1438), zuletzt Head `0eb59ac9b056e0eb298a23e1af9edec57327b4a9`: verpflichtende, gegen Skip abgesicherte CLI-/HTTPS-Node-Regressionen (Owner-Target/Tenant-Bindung, echte HTTP-CSR-Ausgabe, Einmal-Grant-Replay 403, fehlende Auth 401, foreign Tenant 403, remote `app up` ohne lokalen Fallback) in PR-Docker+Podman sowie auch in den bestehenden develop-Native-Jobs. Develop-Selektoren erkennen zudem Aenderungen an den Gate-Skripten und beiden Runtime-Workflows. [Exakter CI-Lauf #42422263152](https://github.com/mcpdev80/baseharbor/actions/runs/42422263152) gestartet, noch nicht vollstaendig bestaetigt. **Kein Remote-E2E-Erfolg behauptet:** produktiver geschuetzter Core-API-Lifecycle, echter separater Connector-Daemon, outbound mTLS und erfolgreicher Docker-/Podman-Remote-Deploy samt status/doctor bleiben technische Abnahmebedingungen. Karte `active`, kein Merge.

- **2026-11-07 Target-Bindung (ChatGPT):** Core-PR [#1438](https://github.com/mcpdev80/baseharbor/pull/1438), Head `7c9abb622acd431e450ca2252b58aa8fdd0f3702`: `baha serve` waehlt den verifizierten Core-Autoritaets-Target jetzt fuer Connector- **und** reines Workstation-Enrollment aus (vorher nur Connector). Gemeinsame Methode `serveEnrollmentAuthorityTarget` + verpflichtender nativer Regressionstest. [CI #42423252917](https://github.com/mcpdev80/baseharbor/actions/runs/42423252917) noch offen. API-Lifecycle und Live-E2E bleiben offen; Karte bleibt `active`.

## 2026-11-08 – Core-Integration nach develop gemergt (ChatGPT)

- **PR:** [mcpdev80/baseharbor#1438](https://github.com/mcpdev80/baseharbor/pull/1438), gepruefter Head `7c9abb622acd431e450ca2252b58aa8fdd0f3702`, **Merge nach develop erfolgreich:** `0fe53052d00a8d440b499c66a6a65c0d54bae5a0`.
- **CI:** [Lauf #42423252917](https://github.com/mcpdev80/baseharbor/actions/runs/42423252917) auf exakt diesem Head terminal `success`, 20 erfolgreiche Jobs, 0 Fehler; native Docker/Podman Core-, OIDC-/Enrollment-, CLI-Vertragstests und Go-Pruefungen erfolgreich.
- **Abgrenzung:** Dies ist die integrierte Core-Grundlage, **nicht** der Beleg fuer automatisch verwalteten geschuetzten Operator-API-Dienst und realen `baha node connect` -> separaten Connector -> remote `baha app up/status/doctor` ueber Docker und Podman. Diese Release-Abnahme bleibt offen, insbesondere auf [0427-004](nc-3-core-enrollment-remote-runtime-acceptance.md). v0.4.27 ist **nicht** freigegeben.

integration gemergt (0fe53052/#1438); E2E-ABNAHME laeuft real auf docker-2+podman-2 (lanes e2e-*). urteil folgt je karte.

## 2026-11-08 Owner-Freigabe und Uebergabe

- Bearbeitungs-Owner gewechselt von `owner:chatgpt` auf `coordinator`. Board-Spalte `wait` (Abhaengigkeit / ausstehende native Abnahme; **kein** technischer `blocked`-Alarm).
- True first-owner OIDC/Keycloak Tenant end-to-end and connected Node onboarding need real Docker/Podman acceptance.
- Alle bestehenden PR-, Commit- und CI-Belege bleiben unveraendert. Kein neuer PASS behauptet.

## PR #1435 reconciliation — 2026-11-08

- Historical [PR #1435](https://github.com/mcpdev80/baseharbor/pull/1435) closed **without merge** as superseded by develop. `cmd/baha/onboarding_command.go` already implements the previously inlined `onboardCommand`, `runOnboardCommand`, and `finishOnboardOutput` plus an explicit first-owner `runOnboardInitialTenant` path.
- All PR-defined production method names and test function names exist on develop (including the split command file); the current tests additionally cover first-owner onboarding, bundle import and real Core bootstrap failures.
- The old branch would reintroduce duplicate command definitions. Keep card status/owner and the remaining real onboarding acceptance obligations unchanged; historical green PR CI is not a fresh E2E proof.
