---
id: t-20261108-bughunt-0427-core-destroy-keycloak-orphan
card_number: "0427-122"
card_short_title: "destroy leaves keycloak up"
type: bug
areas: [lifecycle, identity]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "coordinator"
kanban_status: wait
kanban_lane: wait
kanban_summary: A consented baha destroy (and baha destroy --all) of the local control plane removes or explicitly reports every Core-owned…
kanban_title: "0427-122 · destroy leaves keycloak up"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1444, mcpdev80/baseharbor#1448, mcpdev80/baseharbor#1449]
sources: []
blocker: ""
wait_reason: "PRs #1444/#1448/#1449 merged; native Docker/Podman Keycloak start/destroy/retry with exact integration SHA and resource count remains to be evidenced."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/commit/ab8c16158"]
---

- [ ] t-20261108-bughunt-0427-core-destroy-keycloak-orphan · Bug Hunt v0.4.27: Core destroy lässt Keycloak-Container laufen #task #release/v0-4-27 #status/wait #view/wait #area/identity #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    **PR:** [baseharbor#1444](https://github.com/mcpdev80/baseharbor/pull/1444), [baseharbor#1448](https://github.com/mcpdev80/baseharbor/pull/1448), [baseharbor#1449](https://github.com/mcpdev80/baseharbor/pull/1449)  
    **Waiting:** PRs \#1444/\#1448/\#1449 merged; native Docker/Podman Keycloak start/destroy/retry with exact integration SHA and resource count remains to be evidenced.  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/ab8c16158)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coordinator  
**Priority:** high  
**PRs:** [baseharbor#1444](https://github.com/mcpdev80/baseharbor/pull/1444), [baseharbor#1448](https://github.com/mcpdev80/baseharbor/pull/1448), [baseharbor#1449](https://github.com/mcpdev80/baseharbor/pull/1449)  
**Source:** 
<!-- /generated:links -->

## Goal

A consented `baha destroy` (and `baha destroy --all`) of the local control plane removes or explicitly reports every Core-owned container, including the Identity reference realization in compose project `bh-local-core-shared` (keycloak + keycloak-access). After destroy, `docker ps -a` shows no `bh-*` containers for the target, and `baha status` never reports a STOPPED control plane while Core containers run.

## Scope

- In scope:
  - Core destroy inventory (`cmd/baha/runtime_destroy_inventory.go`, `runtime_destroy_all.go`, Core retirement paths): enumerate all compose projects owned by the installation, not only `bh-local-shared`; include `bh-local-core-shared` (Keycloak identity realization).
  - Control-plane `status` stop detection: observed runtime must include identity-project containers so STOPPED/running agree.
- Out of scope: changing the two-project Core layout itself; HA/topology work.

## Acceptance

- Repro journey (fresh local rootless Docker target): `baha up --control-plane-only --yes` → READY; consented `baha down`; consented `baha destroy --yes`; then no `bh-local-core-shared-keycloak-*` container exists; destroy output lists them as removed or preserved with reason, never silently omits them.
- `baha destroy --all` picks up a leftover identity container on an otherwise clean target.
- `baha status` after partial stop reflects running identity containers instead of STOPPED.

## Required checks

- New/changed: `cmd/baha` destroy inventory tests covering a second compose project label (`com.docker.compose.project=bh-local-core-shared`) with zero deployment state; native rootless-Docker develop acceptance journey for the up→down→destroy sequence.
- Gate: existing package check selects on touched destroy files; Docker native gate executes the live journey; no PR-blocking cross-repo addition.
- Identify exact test names at implementation time in the handoff.

## Dependencies and file ownership

- Owned files or areas: `cmd/baha/runtime_destroy_*.go`, core status collection.
- Shared files: provider identity realization docs — coordinate.

## Handoff

- Source: bug-hunt session 2026-11-07, 0.4.23-develop (8a3f58da9), Docker 29.6.0 rootless, Ubuntu 26.04.1.
- Report: `~/dev/Tests/Baha-Bug-04-destroy-laesst-keycloak-container.md` (destroy plan JSON without keycloak entries, container labels, status output; observed consistently in 3 destroy + 1 destroy --all runs).
- Leftovers were removed manually (`docker rm -f`) to finish the binary before/after control; documented in the report.

## 2026-11-08 Takeover (ChatGPT)

- Owner `owner:chatgpt`; `active`. Next targeted fix: explicit capture of the protected Core-Keycloak compose project even without running containers, followed by negative/ownership regressions. Do not delete foreign containers. Native Docker reproduction remains required for final acceptance.

## 2026-11-08 Produktfix-PR (ChatGPT)

- [Core PR #1444](https://github.com/mcpdev80/baseharbor/pull/1444), head `ddb311ea6682cd72337423d7e04f68098803285e`: destroy inventory captures `bh-<target>-core-shared` even without running containers, not just via observed runtime containers. Verification continues to use unchanged runtime-owner boundaries.
- Regression tests the identity project without running containers, preview, cleanup, `sharedOnly`, and protection of foreign target projects. Exact-head CI open.
- Final acceptance additionally needs a real native Docker `baha up/down/destroy` sequence and status measurement; not closed prematurely.

## 2026-11-08 Merge-Nachweis PR #1444 (ChatGPT)

- **Inventory-Fix fuer Core-eigenes Keycloak-Projekt:** [PR #1444](https://github.com/mcpdev80/baseharbor/pull/1444) nach `develop` gemergt, Merge-SHA `ab8c16158372bc927f67bb4ee64b6ab98e7626ad`; [exact-head CI #42430589361](https://github.com/mcpdev80/baseharbor/actions/runs/42430589361) terminal `success`, keine fehlgeschlagenen Jobs.
- **Karte bleibt `active`**: echte native Docker-/Podman-End-to-End-Abnahme des urspruenglichen Bugs steht noch aus. Der gemergte Teilfix ersetzt diese nicht.

### 2026-11-08 Docker2 Live-Evidence (ChatGPT)

- [E2E Docker2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/e2e-abnahme/docker2.md) auf aelterem Core-Head `0fe53052`: `baha destroy --yes` entfernte SQL/OpenBao, Keycloak-Container blieben und mussten manuell beseitigt werden; `destroy --all` scheiterte nach Teilabbau wegen fehlender Compose-Provider-Registrierung. Dieser Nachweis ist ein **RED vor #1444**, kein PASS fuer den neuen Merge `ab8c1615`. Bestehender Restfehler `destroy --all` nach Teilabbau braucht separaten Recovery-Test. Keine manuelle Cleanup-Prozedur als Produkt-PASS werten.

## 2026-11-08 Retry nach verlorenem Runtime-Owner (ChatGPT)

- [PR #1448](https://github.com/mcpdev80/baseharbor/pull/1448), Head `70d40bb35d8df865c6db51c8fa19866fdb389b71`: entfernt den nachgewiesenen falschen `compose`-Fallback aus `discoverFullDestroyTargets` fuer unregistrierte Local-Targets. Existieren noch lokale Target-State-Dateien ohne verifizierte Providerbindung, ist das ein **blockierender Eigentums-Fehler** statt ein erfundener Runtime-Adapter. Ownership-/Recovery-Zustand bleibt erhalten; kein fremder Runtime-Fallback.
- Regression prueft explizit fehlende Target-Konfiguration, erhaltenen lokalen Zustand, keinen geratenen Provider und blockierendes `unregistered-target-runtime`. PR-CI offen. Danach noch nativer Docker/Podman-Up/Down/Destroy-Retry notwendig; **Karte active**.

## 2026-11-08 Native-Develop-CI angeschlossen (ChatGPT)

- [PR #1449](https://github.com/mcpdev80/baseharbor/pull/1449), Head `6343c82b48989bf3389907c638396c522ed176b3`: fuehrt vorhandenen echten `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` in den **bestehenden** GitHub-hosted Develop-Nativjobs Docker und Podman verbindlich aus. `BASEHARBOR_INSTALLATION_DESTROY_ACCEPTANCE=1`, einmaliger Test-PASS, kein SKIP/FAIL; gemeinsames CI-Skript, Impact-Selector plus Regression angepasst. Kein Self-hosted Runner und keine zusaetzliche parallele Pipeline.
- **Nachweis noch offen:** PR-CI qualifiziert die Scriptsyntax; erst ein echter Develop-Push-Lauf mit nativen Docker+Podman-PASS auf genauem integriertem SHA zaehlt zur Abnahme. Kartenstatus `active`.

### 2026-11-08 Keycloak-E2E-Schaerfung (ChatGPT)

- PR #1449 nun Head `1e3af6441c886897bb1e1c8a185c9b53e005a758`: bestehender nativer Installations-Destroy-Test erzeugt **echte SQL + Identity/Keycloak**-Ressourcen, weist vor der Destruktion vorhandene Core-eigene Keycloak-Container nach und verifiziert nach dem bestaetigten Retry **0 verbliebene eigene Keycloak-Ressourcen**. Docker/Podman-Gate weiterhin im bestehenden develop-Nativjob. Vorherige Head-CI reicht **nicht** mehr; neue exakte PR-CI sowie spaetere echte develop-Nativ-Gates erforderlich. Karte `active`.

## 2026-11-08 Acceptance correction (ChatGPT)

- **Prior `closed/accepted` was premature**: code/PR merge links are not native end-to-end proof. Native Keycloak-up -> consented destroy -> partial retry -> zero owned resources on BOTH Docker and Podman on integrated SHA missing.
- Reopened to `active` with existing code evidence retained. Do not close until exact integration SHA, native runtime output, verified resource preservation/removal, no SKIP, and VM cleanup are recorded.

### 2026-11-08 CI-Fehler #1448 korrigiert (ChatGPT)

- Die erste exact-head [CI #42432440793](https://github.com/mcpdev80/baseharbor/actions/runs/42432440793) war rot, weil die neue Unknown-Runtime-Blockade unbeabsichtigt vier bestehende Tests fuer **andere** unregistrierte Orphan-Targets mit betraf. Das war ein echter Scope-Regressionseffekt, nicht nur eine CI-Flake.
- Korrigiert in Head `b96b1f83af457f4df926992cdecbd9c7e88ea4d1`: **nur** beim legacy `local`-Target ohne Runtime-Owner fail-closed und State-Erhalt, andere unbekannte Targets behalten ihre bisherige gesonderte Behandlung. Exakte neue CI offen. **Nicht mergen, bevor gruen.**

## 2026-11-08 Owner-Freigabe und Uebergabe

- Bearbeitungs-Owner gewechselt von `"owner:chatgpt"` auf `coordinator`. Board-Spalte `wait` (Abhaengigkeit / ausstehende native Abnahme; **kein** technischer `blocked`-Alarm).
- PRs #1444/#1448/#1449 merged; native Docker/Podman Keycloak start/destroy/retry with exact integration SHA and resource count remains to be evidenced.
- Alle bestehenden PR-, Commit- und CI-Belege bleiben unveraendert. Kein neuer PASS behauptet.

### 2026-11-08 Develop-Merge #1449

- [PR #1449](https://github.com/mcpdev80/baseharbor/pull/1449) nach `develop` gemergt, **SHA `ebf56a092de55c5b2e1d3129b32ab50db6b92790`**, exact-head [PR-CI #42432965054](https://github.com/mcpdev80/baseharbor/actions/runs/42432965054) terminal `success` (15 PASS). Der echte Keycloak-/Installation-Destroy-Nativtest ist damit als Gate in den vorhandenen Docker-/Podman-Develop-Jobs eingebaut.
- **Nativer PASS noch offen:** native Develop-Runs auf dem Merge-SHA wurden durch den folgenden Merge abgebrochen; auf dem folgenden SHA war der native Job wegen Impact-Auswahl geskippt. Nicht als native Abnahme interpretieren. PR #1448 bleibt bis exact-head CI/Integration offen. Coordinator übernimmt die notwendigen nativen Gates.

### 2026-11-08 Letzter Fix gemergt

- [PR #1448](https://github.com/mcpdev80/baseharbor/pull/1448) nach `develop` gemergt, Merge-SHA `1fe57f25007413c710e049094c62bf71656b2aa2`; exact-head [CI #42433268819](https://github.com/mcpdev80/baseharbor/actions/runs/42433268819) terminal `success`, nach Korrektur der vier zuvor fehlgeschlagenen fremden Orphan-Fälle.
- Sämtliche Teilfix-PRs #1444, #1448, #1449 integriert. **Nur native Docker+Podman-Ausführung auf dem finalen integrierten SHA mit Keycloak-Resource-Zählung fehlt noch**; Coordinator hat die Karte, `wait` bleibt bis Nachweis bestehen.
