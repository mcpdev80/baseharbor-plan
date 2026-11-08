---
id: t-20261108-bughunt-0427-debug-dump-app-init-flags
card_number: "0427-120"
card_short_title: "CLI debug dump and app-init"
type: bug
areas: [dx, lifecycle]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: "Two related CLI defects found in the 2026-11-07 bug hunt on develop 8a3f58da9 are fixed: (1) baha up without --confirm-candidate…"
kanban_title: "0427-120 · CLI debug dump and app-init"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1439, mcpdev80/baseharbor#1442]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/commit/32ce55dd5"]
---

- [x] t-20261108-bughunt-0427-debug-dump-app-init-flags · Bug Hunt v0.4.27: CLI Debug-Dump und app-init Usage-Regression #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/dx #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1439](https://github.com/mcpdev80/baseharbor/pull/1439), [baseharbor#1442](https://github.com/mcpdev80/baseharbor/pull/1442)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/32ce55dd5)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1439](https://github.com/mcpdev80/baseharbor/pull/1439), [baseharbor#1442](https://github.com/mcpdev80/baseharbor/pull/1442)  
**Source:** 
<!-- /generated:links -->

## Goal

Two related CLI defects found in the 2026-11-07 bug hunt on develop 8a3f58da9 are fixed: (1) `baha up` without `--confirm-candidate` no longer prints a raw goroutine stack to stderr before its clean fail-closed error; (2) the deterministic `baha app init [NAME] [-e ENV|--environment ENV] [--sql] [--workload-component …]` path documented in `baha app init --help` parses and runs again.

## Scope

- In scope:
  - Remove the debug `runtime.Stack` dump fallback in `cmd/baha/deployment_record.go` (~line 523-526, `recordDeploymentBeforeMutation` candidate-consent choke point); keep the existing `errConsentRequiredForCandidateSubmission` error and the confirm-hash prompt.
  - Register the positional NAME and `-e/--environment` options in the `app init` flag parser so the published usage line executes (`unknown option dungeonchurch` / `unknown option --environment` today; misleading `-y` suggestion for `-e`).
  - In scope files: `cmd/baha/deployment_record.go`, `cmd/baha/app_init_*` / init command registration, `cmd/baha/app_commands.go`.
- Out of scope: consent semantics, provider-impact flows, the SQL reference-key defect (0427-121) and destroy discovery (0427-122).

## Acceptance

- Running `baha up --yes --plain` in a git repository with a fresh manifest and no `--confirm-candidate` prints only the candidate block and the consent error; stderr contains no `goroutine` line, in TTY (`script -qec`) and pipe mode.
- `baha app init NAME -e dev --sql --workload-component web --plain` creates the manifest on develop exactly as on v0.4.23; same for `--environment` long form; no `unknown option`.
- Existing init contract tests extended with the documented positional/`-e` invocation; consent path covered by a test asserting no stack output.

## Required checks

- New/changed: `cmd/baha` package — extend `app_init_selection_test.go`/init contract tests with `init NAME -e dev --sql --workload-component` invocation; add a consent-refusal test asserting stderr has no `goroutine`/`runtime.Stack` frames (candidate: `app_up_noop_test.go` or `app_candidate_consent_test.go`).
- Gate: existing package-wide `go test ./cmd/baha/...` PR check selects these on touched files; develop acceptance covers the live rootless-Docker repro (up without consent in a real repo).
- No new CI framework; prove negative (dump removed) and positive (flags parse) selection via file paths above.

## Dependencies and file ownership

- Owned files or areas: `cmd/baha/deployment_record.go` consent branch, init parser/usage.
- Shared files: `docs` reference CLI page for app init usage — coordinate if touched.

## Handoff

- Source: bug-hunt session 2026-11-07, binary 0.4.23-develop (8a3f58da9, own build), Docker 29.6.0 rootless, Ubuntu 26.04.1.
- Reports: `~/dev/Tests/Baha-Bug-01-debug-dump-in-produktion-pfad.md` (repro 4x, source anchor `deployment_record.go:523-526` with verbatim dump) and `~/dev/Tests/Baha-Bug-02-app-init-flags-usage.md` (repro 3x, v0.4.23-vs-develop regression countercheck).
- Repro trigger for the dump requires NO manifest on disk (first candidate submission); with a manifest the refusal happens later in the impact stage without a dump (documented in the report).

## 2026-11-08 Takeover (ChatGPT)

- Owner: `owner:chatgpt`; Lane: `active`.
- Work order: a small, targeted product fix including regression and a mandatory PR CI. No simultaneous changes to other cards.
- No product commit and no PASS/completion claimed yet; evidence/PR added after actual implementation.

## 2026-11-08 Product Work (ChatGPT)

- [PR #1439](https://github.com/mcpdev80/baseharbor/pull/1439) auf `develop`, Head `7a01f888404e195288fc51f83c37c6c453c6a56c`: `runtime.Stack` aus fehlender Candidate-Consent-Fehlerbehandlung entfernt; Fail-Closed bleibt unveraendert.
- Die dokumentierten `app init NAME -e/--environment dev --sql --workload-component` Optionen sind auf dem aktuellen Basiscode bereits implementiert; neuer CLI-Regressionstest beweist beide Aliase und die Workload-Auswahl.
- Noch nicht als abgeschlossen markiert: exakte PR-CI ausstehend; danach Review/Merge und Karte aktualisieren.

## 2026-11-08 Merge Evidence (ChatGPT)

- **PR #1439 erfolgreich nach `develop` gemergt:** Merge-SHA `32ce55dd5c0d623e7dd32ffcf1434a0baa9909dd`; exact-head [CI #42429340000](https://github.com/mcpdev80/baseharbor/actions/runs/42429340000) terminal `success` (alle 11 Jobs erfolgreich).
- Produktiv-Code entfernt den ungewollten `runtime.Stack`-Debug-Dump aus der Consent-Fehlerbehandlung, ohne den Fail-Closed-Fehler zu veraendern. Regression der dokumentierten `app init`-Flags vorhanden.
- **Abnahme nachpruefen:** Ein expliziter Negativtest fuer stderr ohne `goroutine`/Stack in beiden CLI-Modi steht noch aus; Karte bis dahin nicht `closed`.

- **Negativtest-Nachtrag:** [PR #1442](https://github.com/mcpdev80/baseharbor/pull/1442) prueft die echte Candidate-Consent-Ablehnung und stderr auf unerlaubte `goroutine`/`runtime.Stack`-Ausgabe; die initiale Produktkorrektur #1439 ist bereits gemergt. PR-CI fuer #1442 steht noch aus; Karte bleibt bis zur Abnahme `active`.

## 2026-11-08 Final Acceptance (ChatGPT)

- [PR #1442](https://github.com/mcpdev80/baseharbor/pull/1442) **nach develop gemergt**: Merge-SHA `853c2608afcd41f78dea1bb41df0e8e8f09e1110`, exact-head [CI #42430071237](https://github.com/mcpdev80/baseharbor/actions/runs/42430071237) terminal `success`.
- Der Negativtest ruft die echte Candidate-Consent-Ablehnung auf, bestaetigt unveraendertes Fail-Closed und prueft stderr auf `goroutine` und `runtime.Stack`. Zusammen mit gemergtem Produktfix [#1439](https://github.com/mcpdev80/baseharbor/pull/1439) sind die fokussierten Abnahmebedingungen erfuellt.
- Status **closed / accepted**. Keine gesonderte vollstaendige VM-Matrix fuer diesen fokussierten CLI-Fix behauptet.

## Handoff 2026-11-08 (regression)

- Regression confirmed: debug dump survives in develop 0fe53052d (build 0.4.11).
- Karte t-20261108-bughunt-0427-regression-debug-dump-consent (0427-129) dokumentiert die Korrektur.

## 2026-11-08 Owner Release and Handover

- Bearbeitungs-Owner gewechselt von `"owner:chatgpt"` auf `unassigned`. Bereits akzeptierte Karte bleibt `closed`.
- Fixed/accepted #1439 + #1442.
- Alle bestehenden PR-, Commit- und CI-Belege bleiben unveraendert. Kein neuer PASS behauptet.
