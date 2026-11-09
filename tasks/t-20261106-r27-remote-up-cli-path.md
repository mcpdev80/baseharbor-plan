---
id: t-20261106-r27-remote-up-cli-path
card_number: "0427-116"
card_short_title: "CLI start path for Prov-bound"
title: "Remote app up: CLI start path for provider-bound remote apps"
release: v0.4.27
priority: normal
type: task
areas: [cli, remote]
owner: ""
kanban_status: closed
kanban_title: "0427-116 · CLI start path for Prov-bound"
kanban_lane: closed
depends_on: [t-20261017-release-0-4-27-updates, t-20261104-r27-vm-smoke-docker-podman]
prs: [mcpdev80/baseharbor#1407, mcpdev80/baseharbor#1437, mcpdev80/baseharbor#1438]
sources: ["mcpdev80/baseharbor#777"]
repos: [mcpdev80/baseharbor]
blocker: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-3-docker.md", "https://github.com/mcpdev80/baseharbor/commit/0fe53052d00a8d440b499c66a6a65c0d54bae5a0"]
wait_reason: ""
resolution: accepted

---

- [x] t-20261106-r27-remote-up-cli-path · Remote app up: CLI start path for provider-bound remote apps #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/cli #area/remote #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1407](https://github.com/mcpdev80/baseharbor/pull/1407), [baseharbor#1437](https://github.com/mcpdev80/baseharbor/pull/1437), [baseharbor#1438](https://github.com/mcpdev80/baseharbor/pull/1438)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-3-docker.md), [proof 2](https://github.com/mcpdev80/baseharbor/commit/0fe53052d00a8d440b499c66a6a65c0d54bae5a0)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261104-r27-vm-smoke-docker-podman](t-20261104-r27-vm-smoke-docker-podman.md)  
**Required by:** [t-20261106-r27-remote-up-podman-owner-missing](t-20261106-r27-remote-up-podman-owner-missing.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1407](https://github.com/mcpdev80/baseharbor/pull/1407), [baseharbor#1437](https://github.com/mcpdev80/baseharbor/pull/1437), [baseharbor#1438](https://github.com/mcpdev80/baseharbor/pull/1438)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Purpose

Ferngesteuerte Apps lassen sich anlegen/planen/prüfen (plan/status/doctor belegt), aber der
Start-Pfad (`baha app up`) ist über die Remote-Schiene nicht vollständig bedient: Befund-
dateien app_remote_lifecycle.go:34 (Gate) und runtime_explorer_machine.go:55; dev-seitig
fehlt der CLI-Startpfad für bindings-ferne Apps (round-3-Akte, w243/w262 Zeugnisse
evidence/r27-welle5-2026-11-06/remote-control-smoke/round-3.md).

## Acceptance

- `baha app up` (und --confirm-candidate-Pfad) funktioniert gegen eine per Connector gebundene
  App auf Docker UND Podman; doctor meldet danach health OK ohne Befundzeile für den Up-Gap.
- Tests: rote-first-Zelle gegen aktuellen Stand; echte VM-Transkripte (vm-lock, einer-nach-anderer).

kandidat c87c8b644cc auf develop dddf0d7823f; alle gehosteten checks success (skipped nach pfadregel), lauf 42320398007 terminal; docker-zelle meldet echten defekt ErrDeploymentOwnerMissing -> folgt auf karte t-20261106-r27-remote-up-podman-owner-missing

kandidat c87c8b644cc auf develop dddf0d7823f; alle gehosteten checks success (skipped nach pfadregel), lauf 42320398007 terminal; docker-zelle meldet echten defekt ErrDeploymentOwnerMissing -> folgt auf karte t-20261106-r27-remote-up-podman-owner-missing

bahn nach system-reboot frisch beauftragt (takeover der toten lane), konfliktfreie produkt-/testarbeit unter aufgehobenem basis-HOLD (develop 934be499b), .github weiterhin owner-tabu

bahn hat basis konfliktfrei auf develop 934be499b aufgefrischt (head 86f990a6) und die beiden zellen ausgefuehrt — ergebnis ist der owner-seam-fehler, nicht ein neuer defekt dieser karte.

blocker '#117 landing' ERFUELLT (1419 merged develop beb923fe6 11:33Z); deps release-updates+vm-smoke closed. owner-direktive war conditional auf 117 -> jetzt bereit, seat-refill.

r3 request-changes: KEIN Erfolg-fall (err==nil) ueber echtes CLI baha app up auf Docker UND Podman; nur podman-negativ + interne direkt-aufrufe. ask-3 verweis auf #117 falsch (#117 = fail-closed owner-negativ, kein erfolg-transkript). r4 in FRISCHER lane = echter konfliktfreier einsatz auf dem freien sitz.
## Owner-PR-Pruefung — 2026-11-07

- **PR #1407** head `5900dc6b71a2adfec1842164066475061a44d616` ist offen, mergeable und hat PR-CI [42374201283](https://github.com/mcpdev80/baseharbor/actions/runs/42374201283) SUCCESS.
- Der vorhandene Review-Befund verlangt zusaetzlich, dass `app up` nachweislich erfolgreich endet (nicht nur kein lokaler Core-Bootstrap), und einen echten Connector-gebundenen Docker- **und** Podman-Up+Doctor-Gesundheitsnachweis; Podman-Installation-Owner-Befund ist separat zu klaeren. PR-Gruen allein schliesst das nicht. Bis zur echten Abnahme in **review** belassen; kein Merge durch diesen Board-Abgleich.

head c4d528645 drift-frei (develop 812c99c88 Vorfahr), delta nur 116-dateien, CI run 4238139371 terminal PASS. CODEX-REVIEW ausgelöst.

CODEX-REVIEW r4 = REQUEST-CHANGES an head c4d528645: belegt nur fail-closed (upErr!=nil ohne live connector), KEIN echter successfull baha app up + healthy doctor auf Docker UND Podman, native HA/Runtime jobs skipped. run 42381393714 nur go-unit PASS. Review veroeffentlicht act-1407-r4.md (plan 4d00f0ee9). Korrektur r5 an c977fe82.

## Fortsetzung OIDC-/Connector-Abnahme (ChatGPT, 2026-11-07)

- Owner-Anweisung: `active`; bestehender Lane-Owner und PR #1407 bleiben unangetastet. ChatGPT beginnt read-only OIDC-Vorprüfung; keine VM-/Codeman-Dateizugriffe.
- #117 / PR #1419 akzeptiert: Podman-Deployment-Owner-Befund behoben. Offen bleibt echter `baha node add` -> `node connect` -> `baha app up` (`err == nil`) -> `baha doctor` (healthy) auf Docker UND Podman.
- Code-Nachweis: `cmd/baha/node.go` ruft `requestNodeAuthorization` auf; `internal/operatorauth/login.go` verwendet interaktiven Authorization Code mit PKCE und verifiziertem ID-Token. `internal/httpsecurity/middleware.go` verlangt einen gültigen *** Tenant-Rollen. `internal/database/identity_tenant_resolver.go` löst Tenant und Mitgliedschaft unter RLS aus `external_identities` und `memberships` auf.
- Nächster Schritt: vorhandenen sicheren Test-Operator-/Tenant-Provisioning-Pfad verifizieren. Keine manuellen DB-Seeds, Tokens oder Auth-Bypässe. Danach unter VM-Lock echte Docker-/Podman-Nachweise. Der PR-CI-Runtime-Trigger-Befund gehört an den Owner von `.github/**`; kein paralleler Workflow-Eingriff.
- Die bisherigen OIDC-/CI-Schwierigkeiten sind weiterhin offene technische Teilaufgaben, aber mit begonnener Bearbeitung kein stillgelegter Alarmstatus. `Active` ist weder PASS noch Mergefreigabe.

- **2026-11-07 Ownership:** ChatGPT uebernimmt den Produkt-Bootstrap-Teil und die Abnahmevorbereitung als Karten-Owner. Die bisherige Codeman-Lane `lane-0427-116 (geraet blockiert)` sowie deren Core-PR #1407 bleiben als separate, nicht zu ueberschreibende Zuständigkeit erhalten; keine Dateireservierung durch den Karten-Owner-Wechsel aufgehoben.

- 2026-11-07: ChatGPT hat den isolierten produktiven Initial-Tenant-/Operator-Bootstrap als Core-PR [#1437](https://github.com/mcpdev80/baseharbor/pull/1437) auf eigenem Branch implementiert. Neue Dateien `internal/database/operator_bootstrap.go` und `operator_bootstrap_test.go`, nicht im Codeman-PR #1407 reserviert. Implementiert: atomare initiale Tenant-Erstellung und OIDC-verifizierte `editor`-Membership mit serialisiertem, idempotentem Retry, Ablehnung fremder/abgelaufener Principal und zweiter Initialisierung. **Teilimplementierung:** Anbindung an den autorisierten lokalen Core-Setup-/OIDC-Login-Pfad und reale VM-Tests stehen noch aus; Status bleibt `active`, kein Claim zur fertigen End-to-End-Funktion. Eine CI des exakten PR-Heads ist beauftragt; kein weiteres PR-Push bis zum Ergebnis.

- 2026-11-07 Enrollment-UX / Owner-Abnahme: **Ein einziges geschuetztes Datei-Bundle statt manueller Remote-Verbindungsparameter.** Der vorhandene `nodeEnrollmentBundle`-Vertrag enthaelt bereits Tenant-ID, Core-URL, Connector-Adresse, Servername, public CA und One-Time-Authorization. Die fehlende Produktarbeit ist Core-seitige automatische Herleitung und Validierung dieser Werte aus verifizierter Operator-Mitgliedschaft, eigenem Core-Endpoint und gepinntem Trust. Ziel-UX: `baha node add node-docker-1 --runtime docker --output enrollment.json` auf dem Core, dann `baha node connect enrollment.json` auf dem Remote-Host. Keine Tenant-ID, Core-Adresse, CA-Dateipfade oder Admin-Secrets als manuelle Eingaben/Token im CLI. Fehlender oder mehrdeutiger Owner/Issuer/Endpoint ist fail-closed. Neue Datei-Formate vermeiden; bestehendes 0600/One-Time/Expiry erhalten. Docker + Podman echte Native-Tests (positiv und Negativ-Faelle) erforderlich. Produktdatei `cmd/baha/node.go` gehoert derzeit auch zu Core-PR #1436: [Koordinationsauftrag #1436](https://github.com/mcpdev80/baseharbor/pull/1436#issuecomment-6711497609) hinterlegt; keine parallele Aenderung derselben Datei, bis Owner-Konflikt aufgeloest ist. **Status bleibt active; nicht fertig implementiert.**

- 2026-11-07 Wizard-Integration (owner chatgpt-0427-116): `promptNodeAdd` in `cmd/baha/node.go` ist bereits ein interaktiver Wizard, fragt aber Tenant UUID, Core-API, Connector-Adresse, CA-Datei und Environment manuell ab. Das ist unzureichend. CORE-seitige `baha node add` CLI **und** Wizard muessen denselben verifizierten Operator-Tenant-/Core-Endpoint-/Trust-Resolver nutzen und ein einziges geschuetztes Enrollment-JSON erzeugen. Keine frei eingegebene Tenant-UUID, keine loopback-Defaults fuer Remote, keine duplizierte Datei/Token-Logik. Integration/Konflikt mit Node-PR #1436: [Auftrag](https://github.com/mcpdev80/baseharbor/pull/1436#issuecomment-6711528738). Der neue Workstation-Onboarding-Wizard #1435 ist separat und muss den initialen Core-Operator-Tenant vorbereiten, [Schnittstellenauftrag](https://github.com/mcpdev80/baseharbor/pull/1435#issuecomment-6711528355). Der Test auf echte Docker- und Podman-Enrollment-/Remote-App-Erfolge bleibt verpflichtend; nicht als erledigt behaupten.

- **2026-11-07 Produktentscheid: DEFAULT FIRST, ADVANCED OPTIONAL.** Ziel: `baha node add NODE --runtime docker|podman --output enrollment.json` verwendet automatisch die **verifizierte** Operator-Tenant-Membership, den vorhandenen eigenen Core, gesicherte externe erreichbare Endpunkte und die gepruefte CA; fertiges One-Time-JSON fuer `baha node connect FILE` auf Remote-Host. Ein Default-Tenant einer frischen Installation heisst beispielsweise `baseharbor` mit generierter UUID; alternativ komplett benutzerdefiniert nach Wizard-Eingaben, solange Validierung/Owner-Vertrag passt. Im normalen Dialog keine Tenant-UUID, API-Adresse oder CA manuell abfragen, aber der Entwickler **darf alle unterstuetzten Werte im Advanced-Zweig gezielt anpassen**; keine unberechtigte Fremd-Tenant-Wahl oder unsicherer CA-/Issuer-Override. Kein unnoetiges Nachfragen, Cancel ohne Teilmutation, Defaults nie durch `dev` als Tenant-Scope verwechseln. Tests fuer Standard-/Advanced-Pfade, bereits existierende Core-/Tenant-Werte, ungultige Konfigurationen sowie Docker/Podman. PR-Auftraege [#1436](https://github.com/mcpdev80/baseharbor/pull/1436#issuecomment-6711559336) und [#1437](https://github.com/mcpdev80/baseharbor/pull/1437#issuecomment-6711559698); Wizard #1435 abstimmen. Noch offen, `active`.

- **2026-11-07 Uebernahme und Integration:** Codeman hat die Worker-Lanes gestoppt und den finalen SHA-/Evidence-Stand in den bestehenden PRs dokumentiert. ChatGPT hat die unveraenderten R3-/R4-Worker-Artefakte, den Operator-/Tenant-Bootstrap und den Remote-App-Start im [Integrations-PR #1438](https://github.com/mcpdev80/baseharbor/pull/1438) zusammengefuehrt. Aktueller Integrations-Head `7f8fee2f6091a9eb5d3d0d4686ad51eb9ddc8951` mit erfolgreichem hosted CI-Lauf [42404964550](https://github.com/mcpdev80/baseharbor/actions/runs/42404964550). **Status bleibt active**: Default-/Advanced-Wizard, aus verifizierten Core-Daten automatisch befuelltes Enrollment-Bundle sowie echter Docker-/Podman-E2E-Nachweis muessen noch funktional endabgenommen werden. Keine Freigabe fuer Merge/Release allein aufgrund der CI-Matrix. Dieses Integration-PR ist die gemeinsame Arbeitsquelle; Ursprungs-PRs bleiben unveraendert zur Rueckverfolgbarkeit.

- **2026-11-07 Integrations-CI (ChatGPT):** Die Integration auf [Core-PR #1438](https://github.com/mcpdev80/baseharbor/pull/1438) umfasst nun `baha onboard` Default/Advanced samt verifiziertem Keycloak-PKCE/Initial-Tenant (`baseharbor` oder custom), API-Bindung an den Operator-Issuer/Client, Tenant-Aufloesung aus Core-authentifizierter Membership, Core-seitiges public-Endpoint/CA-Profil und ein dateibasiertes One-Time-Node-Enrollment. Ein eigener PR-CI-Pruefblock verlangt exakt PASS fuer neun relevante Tests inklusive echter PostgreSQL-Transaktion (nicht nur go test Exitcode), und der vorhandene CI-Workflow wurde um gezielte native Docker-/Podman-Keycloak+Core-Jobs fuer betroffene PR-Dateien erweitert. Integrations-Head `fbc0d9d153482be27979fd6b31897eb6ad2f53ab`, nativer [PR-CI-Lauf #42407311186](https://github.com/mcpdev80/baseharbor/actions/runs/42407311186) **noch nicht abgenommen**. Echte durchgehende Remote-Connector-/App-E2E-Ergebnisse (Docker und Podman) bleiben verpflichtend; keine Release-/Merge-Freigabe ohne belastbare PASS-Ergebnisse. Karte `active`, nicht `done`.

- **2026-11-07 First-install Korrektur (ChatGPT):** Der bisherige `ModeBootstrap`-Wizard war beim `AppNew`-Pfad ein No-op. Im [Integrations-PR #1438](https://github.com/mcpdev80/baseharbor/pull/1438) startet er jetzt nach dem bestaetigten Review die bestehende `baha up --control-plane-only`-Authority und anschliessend die verifizierte Keycloak-OIDC-PKCE-/Initial-Tenant-Erstellung; fehlgeschlagener Core-Start verhindert jegliche Owner-Mutation. Default-Tenant `baseharbor`, optional eigene Namen. Native Docker/Podman-PR-CI sowie PostgreSQL-Regressionen werden am finalen Head ausgefuehrt; noch **keine echte Node-connect/App-up-End-to-End-Abnahme**, daher Karte `active` und kein Merge. Letzter Integrations-Head `58bbaed713576adfc60943e9b621818d63e6e4f1`.

- **2026-11-07 Letzte E2E-Luecke:** Der geschuetzte Core-Operator-HTTP-Server hat einen separaten `baha serve`-Lebenszyklus; die bisherige `baha onboard`-Ersteinrichtung konvergiert zwar Core (`baha up --control-plane-only`) und verifiziertes Keycloak-/Tenant-Onboarding, aber die sichere automatische Aktivierung des Operator-/Connector-Servers, sein erreichbarer TLS-Endpunkt und die echte `baha node connect FILE`-bis-`baha app up`-Kette sind noch NICHT in beiden Runtime-Varianten als durchgaengig PASS nachgewiesen. HTTP-Route `GET /api/v1/connectors/owner-context` ist in Core-PR #1438 jetzt explizit hinter OIDC im Operator-Mux registriert (Head `be266a7afa1549549ed6d5e58076df960aeacce5`). Status `active`, keine falsche Fertigmeldung/kein Merge; native Job-Ergebnisse unter [CI #42408115747](https://github.com/mcpdev80/baseharbor/actions/runs/42408115747).

- **2026-11-07 native CI failure (ChatGPT):** Native Docker/Podman-PR-CI #42408115747 scheiterte nach erfolgreichem Keycloak-Lauf identisch bei `TestControlPlaneSingleDefaultNativeRuntimeInCI`: Test las absichtlich nicht konfigurierten `w169-isolation-required-*`-Guard-Target statt eines echten eigenen Core-Targets. In [Integrations-PR #1438](https://github.com/mcpdev80/baseharbor/pull/1438) wurde der Test korrigiert: `isolateRuntimeForTest` erzeugt jetzt einen separaten Target; `baha up --control-plane-only --yes` startet dort den realen Core, dessen Runtime danach erst geprueft wird. Exakter Code-Head `8eeb620001e1533ecc1f37a497a7e48122a5c7bb`, neuer [CI-Lauf #42418160655](https://github.com/mcpdev80/baseharbor/actions/runs/42418160655) zum Zeitpunkt der Bearbeitung noch aktiv. Keycloak-/Core-PR-Test darf nicht skippen; volle Remote-Node-Enrollment- und `app up`-Akzeptanz auf Docker/Podman fehlt weiterhin. Karte active, kein Merge.

- **2026-11-07 native CI-Nachpruefung (chatgpt-0427-116):** Auf Core-PR #1438 mit Head `8eeb620001e1533ecc1f37a497a7e48122a5c7bb` ist der zuvor fehlgeschlagene Test `TestControlPlaneSingleDefaultNativeRuntimeInCI` korrigiert: Er erzeugt jetzt einen eigenen isolierten Target, startet dort `baha up --control-plane-only --yes` und prueft erst dann die laufenden Core-Ressourcen. Im [CI-Lauf #42418160655](https://github.com/mcpdev80/baseharbor/actions/runs/42418160655) sind **native Keycloak+Core Docker und Podman beide PASS**. `go-unit-tests` lief beim letzten Abruf noch; die E2E-Kette Core API -> `baha node add` -> Bundle -> `baha node connect` -> Remote-`app up` braucht weiterhin separate echte native Abnahme. Die develop-Impact-Klassifikation fuer Identity/Node ist als noch nicht gepushter Folge-Commit `c3e7a557df3243078499e803f24fc7b7f0b33b1d` vorbereitet (wird erst nach exaktem CI-Head-Lauf vorgerueckt); keine Behauptung einer Freigabe oder eines Merges. Status `active`.

- **2026-11-07 native selector follow-up (ChatGPT):** Core-PR [#1438](https://github.com/mcpdev80/baseharbor/pull/1438) erweitert auf Head `4b656481e20f5f3c223d30cbdf511ae7d2158d7c` die develop-Impact-Selektoren fuer OIDC/Keycloak, Operator-Tenant, Onboarding, Core-API, Node und Remote-App; `scripts/test-ci-impact-selectors.sh` wurde als Regression hinzugefuegt und in die verpflichtende native Docker/Podman-CI eingebunden. [Neuer CI-Lauf #42419767443](https://github.com/mcpdev80/baseharbor/actions/runs/42419767443) gestartet, noch **nicht** endgueltig abgenommen. Der alte Head `8eeb6200` hatte einen vollstaendigen erfolgreichen Go-/Docker-/Podman-PR-Lauf #42418160655, jedoch ohne Remote E2E. Geschuetzter Core-API-Autostart/Health sowie die reale Node-Enrollment-bis-Remote-app-up-Kette fehlen als PASS-Nachweis; Karte bleibt `active`, kein Merge/Release.

- **2026-11-07 Node-CI-Ausbau (ChatGPT):** Core-Integrations-PR [#1438](https://github.com/mcpdev80/baseharbor/pull/1438), zuletzt Head `0eb59ac9b056e0eb298a23e1af9edec57327b4a9`: verpflichtende, gegen Skip abgesicherte CLI-/HTTPS-Node-Regressionen (Owner-Target/Tenant-Bindung, echte HTTP-CSR-Ausgabe, Einmal-Grant-Replay 403, fehlende Auth 401, foreign Tenant 403, remote `app up` ohne lokalen Fallback) in PR-Docker+Podman sowie auch in den bestehenden develop-Native-Jobs. Develop-Selektoren erkennen zudem Aenderungen an den Gate-Skripten und beiden Runtime-Workflows. [Exakter CI-Lauf #42422263152](https://github.com/mcpdev80/baseharbor/actions/runs/42422263152) gestartet, noch nicht vollstaendig bestaetigt. **Kein Remote-E2E-Erfolg behauptet:** produktiver geschuetzter Core-API-Lifecycle, echter separater Connector-Daemon, outbound mTLS und erfolgreicher Docker-/Podman-Remote-Deploy samt status/doctor bleiben technische Abnahmebedingungen. Karte `active`, kein Merge.

## 2026-11-08 – Core-Integration nach develop gemergt (ChatGPT)

- **PR:** [mcpdev80/baseharbor#1438](https://github.com/mcpdev80/baseharbor/pull/1438), gepruefter Head `7c9abb622acd431e450ca2252b58aa8fdd0f3702`, **Merge nach develop erfolgreich:** `0fe53052d00a8d440b499c66a6a65c0d54bae5a0`.
- **CI:** [Lauf #42423252917](https://github.com/mcpdev80/baseharbor/actions/runs/42423252917) auf exakt diesem Head terminal `success`, 20 erfolgreiche Jobs, 0 Fehler; native Docker/Podman Core-, OIDC-/Enrollment-, CLI-Vertragstests und Go-Pruefungen erfolgreich.
- **Abgrenzung:** Dies ist die integrierte Core-Grundlage, **nicht** der Beleg fuer automatisch verwalteten geschuetzten Operator-API-Dienst und realen `baha node connect` -> separaten Connector -> remote `baha app up/status/doctor` ueber Docker und Podman. Diese Release-Abnahme bleibt offen, insbesondere auf [0427-004](nc-3-core-enrollment-remote-runtime-acceptance.md). v0.4.27 ist **nicht** freigegeben.

integration gemergt (0fe53052/#1438); E2E-ABNAHME laeuft real auf docker-2+podman-2 (lanes e2e-*). urteil folgt je karte.

## 2026-11-08 Owner-Freigabe und Uebergabe

- Bearbeitungs-Owner gewechselt von `chatgpt-0427-116` auf `unassigned`. Bereits akzeptierte Karte bleibt `closed`.
- Existing accepted card; ownership released.
- Alle bestehenden PR-, Commit- und CI-Belege bleiben unveraendert. Kein neuer PASS behauptet.

## CI-/PR-Nachtrag — 2026-11-08 (ChatGPT)

- PR [#1407](https://github.com/mcpdev80/baseharbor/pull/1407), Head `345b0352bc4577e2fcd540729d9c1adf94e68810`, am 2026-11-08 erneut auf aktuellen Checks geprueft: [Run 42476049436](https://github.com/mcpdev80/baseharbor/actions/runs/42476049436). Native Destroy-Retry Docker und Podman, Build, Vet, Format und Trusted Plan PASS; Go-Unit-Test zuletzt IN_PROGRESS. PR noch offen/mergeable, **kein Merge** vor terminalem Gesamtergebnis und Head-Abgleich.
- **Plan-Wahrheit:** Vorhandenes `closed/accepted` dieser Karte wurde nicht rueckwirkend geaendert; es ist kein Nachweis, dass PR #1407 bereits gemergt wurde. PR-Abschluss wird separat nachgetragen. CI-Uebernahme durch ChatGPT, keine weitere Produktdatei-Bearbeitung.

## PR-Abschluss — 2026-11-08

- [#1407](https://github.com/mcpdev80/baseharbor/pull/1407) ist nach `develop` gemergt, Merge-SHA `223042bc0372f41a6f0a7c2d1a2e01b095bb7a0b`. Der vorher dokumentierte CI-/Merge-Zwischenstand ist damit historisch.
- Bereits bestehende `closed/accepted`-Kartenannahme wird nicht verändert; kein neuer Worker, keine erneute Produktimplementierung dieser geschlossenen Karte.

## PR #1437 lifecycle reconciliation — 2026-11-08

- PR https://github.com/mcpdev80/baseharbor/pull/1437 closed **without merge** after source audit: 14 of 15 files byte-identical with develop; remaining `cmd/baha/operator_auth.go` differs only by newer, more complete `baha login` usage on develop.
- First-owner bootstrap implementation and regression sources already exist on develop; historical PR would regress the CLI usage string.
- This is **not** an acceptance of full remote-up onboarding/Keycloak E2E: keep the card's existing status and outstanding independent checks.
