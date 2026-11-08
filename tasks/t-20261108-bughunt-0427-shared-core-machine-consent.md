---
id: t-20261108-bughunt-0427-shared-core-machine-consent
card_number: "0427-123"
card_short_title: "shared-core consent blocks"
type: bug
areas: [lifecycle,dx]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "coordinator"
kanban_status: wait
kanban_lane: wait
kanban_summary: Merged unit/contract fixes are not native Docker/Podman PTY acceptance; see open test requirements below.
kanban_title: "0427-123 · shared-core consent blocks"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1445, mcpdev80/baseharbor#1446]
sources: []
blocker: ""
wait_reason: "PRs #1445 and #1446 merged. Native PTY Docker/Podman two-stage app down and denial proof still needed."
resolution: ""
evidence: ["https://github.com/marcel/dev/baseharbor/commit/db06f01e9", "https://github.com/mcpdev80/baseharbor/commit/db06f01e9"]

---

## Outcome and acceptance

Merged unit/contract fixes are not native Docker/Podman PTY acceptance; see open test requirements below.

- [ ] t-20261108-bughunt-0427-shared-core-machine-consent · 0427-123 · App up/down haengt an machine-consent #task #release/v0-4-27 #status/wait #view/wait #area/dx #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    **PR:** [baseharbor#1445](https://github.com/mcpdev80/baseharbor/pull/1445), [baseharbor#1446](https://github.com/mcpdev80/baseharbor/pull/1446)  
    **Waiting:** PRs \#1445 and \#1446 merged. Native PTY Docker/Podman two-stage app down and denial proof still needed.  
    **Evidence:** [proof 1](https://github.com/marcel/dev/baseharbor/commit/db06f01e9), [proof 2](https://github.com/mcpdev80/baseharbor/commit/db06f01e9)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coordinator  
**Priority:** high  
**PRs:** [baseharbor#1445](https://github.com/mcpdev80/baseharbor/pull/1445), [baseharbor#1446](https://github.com/mcpdev80/baseharbor/pull/1446)  
**Source:** 
<!-- /generated:links -->

## Problem (bug-hunt intake 2026-11-08, verified before carding)

BF-2 docker2 hunt: up/down on shared-core is not completable without machine-consent digest; down hangs after consent prompt. Related to (not identical with) 0427-120's --confirm-candidate flag.

## Acceptance

up/down complete through documented interactive flow without hanging; any required confirmation is explicit, single, and recoverable; stuck-state cleanup exists.

## Dependencies and file ownership

Depends only on the release umbrella. Write-set per repo rules; intake evidence carries the exact repro.

## 2026-11-08 Übernahme (ChatGPT)

- Owner `owner:chatgpt`; `active`. Sicherheitsrelevanter Consent-Fluss: interaktiven App-Up/Down-Weg und die bestehende `ProviderChangeConsent`-Pruefung gegen die VM-Reproduktion untersuchen. Keine Abschwaechung der Freigabe- oder Datenloeschungs-Gates. Zuerst echter Negativ-/Positivtest, dann enger Produktfix.

## 2026-11-08 Consent-Pfadpruefung (ChatGPT)

- Der aktuelle lokale CLI-Stop-Pfad `authorizeApplicationStop` unter `cmd/baha/application_stop_impact.go` bietet auf einem erkannten Terminal `readProviderImpactAcknowledgements` an, prueft erst danach per `ValidateProviderImpactScopeConsent` und verifiziert vor Mutation den unveraenderten Plan. Der maschinenlesbare Consent bleibt per `BASEHARBOR_PROVIDER_CHANGE_CONSENT` an den aktuellen `plan_id` gebunden; generisches `--yes` reicht **absichtlich nicht**.
- Der Bug-Hunt beschreibt bei `baha app down` einen blockierenden Prompt auf echtem Rootless-Docker, aber noch keinen exakten aktuellen `develop`-PTY-Trace, der zwischen fehlendem Terminal-Input, abweichendem Plan-ID und fehlender Scope-Confirmation unterscheidet. Bestehender `readProviderImpactAcknowledgements`-Test validiert die Sicherheits-Logik, aber nicht den realen PTY-Weg.
- Kein Sicherheits-Bypass und keine behauptete Behebung. Naechster konkreter Nachweis: PTY-E2E mit 2× `y`, Plan-SHA-Vergleich und timeout-gesteuertem Abbruch; danach ggf. lokaler CLI-Input-Fix. Karte bleibt `active`.

### 2026-11-08 DIAG_EXEC-Teilfehler (ChatGPT)

- In `cmd/baha/app_machine_adapters.go` hat der aktuelle `develop` zwei **unbedingte** `fmt.Printf("DIAG_EXEC ...")` bei fehlgeschlagenem Machine-Provider-Change. Diese Debug-Ausgaben umgehen die stabilen maschinenlesbaren Fehlergrenzen, stoeren stdout und koennen Outcome-Details exponieren. Als sicherer, eng abgegrenzter **Teilfix** von 0427-123 werden sie ohne Aenderung der Consent-/Result-Logik entfernt und gegen Rueckfall getestet. Dieser Teilfix ist **nicht** die Loesung des PTY-Down-Haengers; Karte bleibt danach aktiv.

- **Teilfehler-Fix-PR:** [#1445](https://github.com/mcpdev80/baseharbor/pull/1445), Head `f80dc0b9eefc0b4f757ec4ba4d05a500e569f450` entfernt beide ungefilterten `DIAG_EXEC`-Stdout-Prints und fuegt eine Source-Regression hinzu. Kein Consent-Sicherheits-Bypass. Exact-head CI offen, PTY-Haenger weiterhin separat zu beheben.

## 2026-11-08 Merge-Nachweis PR #1445 (ChatGPT)

- **Teilfehler-Fix: ungefilterte DIAG_EXEC-Stdout-Ausgaben entfernt:** [PR #1445](https://github.com/mcpdev80/baseharbor/pull/1445) nach `develop` gemergt, Merge-SHA `db06f01e9fd793706da5072769922a0c64afecf0`; [exact-head CI #42430983626](https://github.com/mcpdev80/baseharbor/actions/runs/42430983626) terminal `success`, keine fehlgeschlagenen Jobs.
- **Karte bleibt `active`**: echte native Docker-/Podman-End-to-End-Abnahme des urspruenglichen Bugs steht noch aus. Der gemergte Teilfix ersetzt diese nicht.

## 2026-11-08 Interaktiver Consent-Regressionstest (ChatGPT)

- [PR #1446](https://github.com/mcpdev80/baseharbor/pull/1446) Head `90e9aae7f5c07729a309f97672f60247885c4845`: reproduziert `authorizeApplicationStop` auf dem echten CLI-Autorisierungspfad mit einer endlichen interaktiven Eingabe (2x `yes`, Ablehnung Stufe 1, Ablehnung Stufe 2). Prueft Erfolg nur bei aktueller Plan-ID und fail-closed bei Ablehnung. Noch kein echter PTY auf Docker/Podman; CI offen, Karte weiterhin `active`.

## 2026-11-08 PR #1446 erfolgreich gemergt (ChatGPT)

- [PR #1446](https://github.com/mcpdev80/baseharbor/pull/1446) erfolgreich nach `develop` gemergt: `f9e207ac0d0b4c983fbb01d4357a8784c41c92de`. Exact-head [CI #42431899984](https://github.com/mcpdev80/baseharbor/actions/runs/42431899984) terminal `success`, **10 PASS, 0 FAIL, 0 ausstehend**.
- Echter `authorizeApplicationStop`-Codepfad mit zwei Ja-Bestaetigungen, Ablehnung in Stufe 1/2, aktueller Planbindung regressionsgetestet. **Karte bleibt active:** echter PTY- und nativer Docker-/Podman-Lifecycle-Nachweis weiterhin ausstehend, keinerlei Sicherheits-Bypass.

## 2026-11-08 Acceptance correction (ChatGPT)

- **Prior `closed/accepted` was premature**: code/PR merge links are not native end-to-end proof. Real PTY two-stage app down on BOTH Docker and Podman still lacks exact SHA and PASS-not-SKIP evidence.
- Reopened to `active` with existing code evidence retained. Do not close until exact integration SHA, native runtime output, verified resource preservation/removal, no SKIP, and VM cleanup are recorded.

## 2026-11-08 Owner-Freigabe und Uebergabe

- Bearbeitungs-Owner gewechselt von `"owner:chatgpt"` auf `coordinator`. Board-Spalte `wait` (Abhaengigkeit / ausstehende native Abnahme; **kein** technischer `blocked`-Alarm).
- PRs #1445 and #1446 merged. Native PTY Docker/Podman two-stage app down and denial proof still needed.
- Alle bestehenden PR-, Commit- und CI-Belege bleiben unveraendert. Kein neuer PASS behauptet.
