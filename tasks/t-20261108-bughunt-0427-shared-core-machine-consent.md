---
id: t-20261108-bughunt-0427-shared-core-machine-consent
card_number: "0427-123"
card_short_title: "Shared-Core Consent blockiert"
type: bug
areas: [lifecycle,dx]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "owner:chatgpt"
kanban_status: active
kanban_lane: active
kanban_summary: Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.
kanban_title: "0427-123 · Shared-Core Consent blockiert"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1445]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
---

## Outcome and acceptance

Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.

- [ ] t-20261108-bughunt-0427-shared-core-machine-consent · 0427-123 · App up/down haengt an machine-consent #task #release/v0-4-27 #status/active #view/active #area/dx #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** owner:chatgpt · **Priority:** high  
    **In progress** · owner:chatgpt  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** owner:chatgpt  
**Priority:** high  
**PRs:** none  
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
