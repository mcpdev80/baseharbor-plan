---
id: t-20261119-r28-perses-alert-verifier-caller-wiring
kanban_title: 0428-152 · alert-verifier caller wiring
card_number: "0428-152"
card_short_title: "alert-verifier caller wiring"
type: task
areas: [metrics, observability, cli]
release: v0.4.28
version: ""
parent: ""
owner: w41-0428-152-alertverifier
kanban_status: active
kanban_lane: active
blocker: ""
wait_reason: ""
depends_on: [t-20261119-r28-perses-status-backend-witness]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1816]
sources: []
source_note: "befund aus der unabhaengigen review und der korrekturrunde von karte 0428-073 (PR #1704), fundstelle von MIR am develop 28fb427f nachgemessen; akte evidence/r28-welle4-2026-11-19/codex-review-wave/1704-0428-073.md P6"
evidence:
  - "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-review-wave/1704-0428-073.md"
resolution: ""
created: 2026-11-19
---

- [ ] t-20261119-r28-perses-alert-verifier-caller-wiring · alert-verifier haengt in der luft #task #release/v0-4-28 #status/active #view/active #area/cli #area/metrics #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** w41-0428-152-alertverifier  
    **PR:** [baseharbor#1816](https://github.com/mcpdev80/baseharbor/pull/1816)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-review-wave/1704-0428-073.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261119-r28-perses-status-backend-witness](t-20261119-r28-perses-status-backend-witness.md)  
**Owner:** w41-0428-152-alertverifier  
**Priority:** not set  
**PRs:** [baseharbor#1816](https://github.com/mcpdev80/baseharbor/pull/1816)  
**Source:** 
<!-- /generated:links -->

## Goal

Der Perses-alert-evaluator-verifier (internal/metrics/perses_prometheus_alerts.go) ist eine vertragsoberflaeche OHNE abnehmer: kein produktionspfad ruft ihn. Ziel ist ein einziger, ehrlicher abnehmer — die 'baha app perses status'-observation — der das ergebnis des verifikators zeigt, ohne einen zustand zu erfinden, den der verifikator nicht liefern darf. Eine korrektur des zustands-textes (karte 0428-073, laeuft) ist ohne abnehmer eine sicherung ohne geraet: der text kann beim naechsten refactoring verschwinden, ohne dass ein test es merkt.

## Scope

- In scope: der abnehmer-pfad in cmd/baha/app_status_collect.go (gemessen: zeile ~401 setzt eine 'management-ui/perses'-observation ueber AddObservation) und die zugehoerigen tests in cmd/baha/. VON MIR NACHGEMESSEN am develop 28fb427f mit 'git grep -n "VerifyPersesAlertEvaluatorHealth|BuildPersesAlertEvaluator|PersesAlertReachability|persesAlertRealEvaluatorContractPresent" -- cmd internal': null treffer ausserhalb von internal/metrics/**.
- Out of scope: jede aenderung an internal/metrics/perses_prometheus_alerts.go (karte 0428-073, laeuft), internal/metrics/prometheus_files.go (0428-123), internal/capability/registry.go (0428-151), internal/application/provider_consent_authority.go (0428-119).
- ABHANGIGKEIT (gemessen): karte 0428-142 (PR #1702) aendert GENAU DIESE datei (cmd/baha/app_status_collect.go in ihrer aenderungsliste). Diese karte DARF NICHT parallel zu 0428-142 arbeiten; sie hopft auf deren gemergten inhalt.

## Acceptance

- 'baha app perses status' zeigt fuer den alert-evaluator genau einen von drei zustaenden: 'not configured' (im manifest nicht ausgewaehlt), 'unavailable (owner-gated evaluator contract)' (ausgewaehlt, contract fehlt) — und NIE 'healthy'/'verified', solange persesAlertRealEvaluatorContractPresent() false ist.
- Die entscheidung kommt AUS DEM VERIFIKATOR (ein aufruf, ein ergebnis), nicht aus einer zweiten, parallel gelernten logik im cli.
- Ein negativer test beweist: wenn der verifikator einen fehler liefert, darf die observation nicht auf 'healthy' fallen (fail-closed am abnehmer, nicht nur im verifikator).
- Kein neuer zustaeds-behaälter, kein neues manifest-feld: die entscheidung muss aus den bestehenden bindings/feldern ableitbar sein (owner-regel: kein state ohne vertrag).
- Ein positiver test haelt den EXAKTEN wortlaut der zustands-texte fest (das ist der punkt, an dem 0428-073 bisher gescheitert ist).

## Required checks

- **Modified features:** go test ./cmd/baha -count=1 -run '^Test(Perses|AppStatus|Observability)' und go test ./internal/metrics -count=1 -run '^TestPersesAlert'; neue tests muessen vom 'PR · Go unit'-shard ausgefuehrt werden (CI-aufnahmepflicht §5.3), job + workflow-zeile in der akte nennen.
- **CI integration:** ein pull_request-lauf am exakten kopf bis terminal; die runtime-zellen duerfen wegen der fehlenden ORAS-installation im PR-job (owner-draht 114(a)) skipped bleiben, dann die skip-zeile wORTLICH in die akte — SKIPPED ist nicht pass (§5.4).

## Scheduling

Unstarted and unassigned; scheduled behind 0428-142/#1702 because both need
`cmd/baha/app_status_collect.go`. This is ordinary prerequisite sequencing, so
the card remains planned and renders as waiting until 0428-142 is accepted.

Dep backend-witness closed/accepted; blocking dep #1702 (0428-142) MERGED -> cmd/baha/app_status_collect.go consolidated on develop d4fa8c589. Dispatched flash lane w41 (7d4c6d78) on new branch lane-0428-152-alertverifier-caller. Write-set cmd/baha/app_status_collect.go + cmd/baha tests only; Hosted-only verify; no collision with active lanes (secret_*/ci_integration_* different files). One honest consumer for the alert-evaluator verifier.

Correction (maintainer review on 3f8e6fa): alert-evaluator observation added only to app-status; acceptance requires it on the Perses STATUS command face too (cmd/baha/perses_lifecycle.go persesStatusResult returns without it; command-face test checks unrelated top-level state). Routed w41: add observation to perses_lifecycle.go status path + fix that test; no internal/metrics edits; exact-head Hosted rerun; PR open until green.

Precise gap (Owner): 'baha app perses status' = cmd/baha/perses_lifecycle.go reportPersesSurfaceStatus returns persesStatusResult without the alert-evaluator observation (only added to app-status collectManagedServiceChecks). w41 instructed to add the observation to reportPersesSurfaceStatus + fix that command-face test; no internal/metrics; exact-head Hosted rerun; PR open.

Still open: lane edited only app_status_collect.go through f0fe88e; cmd/baha/perses_lifecycle.go reportPersesSurfaceStatus still omits the alert-evaluator observation from persesStatusResult, so 'baha app perses status' cannot show it. Directive pinned to that exact function + its command-output test. No Codex; Hosted-only.

Correction after run 45286007687: head 7fa61146 catalog rows use docker/podman.observability, but Trusted Plan authoritatively requires docker/podman.data.capabilities for app_status_collect.go, app_status_perses_alert_evaluator_0428_152_test.go, cmd/baha/perses_lifecycle.go. Lane instructed to change only those three rows' surfaces; no broad package rows; no .github/** changes; keep reportPersesSurfaceStatus alert-evaluator fix; exact-head Hosted rerun; PR open; no merge; no Codex.
