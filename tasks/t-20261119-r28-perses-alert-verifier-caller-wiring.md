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
owner: w53-0428-152-alertfix
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
    **Owner:** w53-0428-152-alertfix  
    **PR:** [baseharbor#1816](https://github.com/mcpdev80/baseharbor/pull/1816)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-review-wave/1704-0428-073.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261119-r28-perses-status-backend-witness](t-20261119-r28-perses-status-backend-witness.md)  
**Owner:** w53-0428-152-alertfix  
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

run 45286659035: surfaces now correct; 3 catalog id fields must change dot-separated to underscore source.cmd_baha_app_status_collect_go / source.cmd_baha_app_status_perses_alert_evaluator_0428_152_test_go / source.cmd_baha_perses_lifecycle_go (id-only change). Head 836469a3; exact-head Hosted rerun. scripts/** exact only; PR open; no merge; no Codex.

Trusted Plan base-policy blocker (run 45287020021): resolves vs trusted develop catalog 0d29c2a9, which lacks the 3 rows, so in-PR self-catalog cannot authorize. Lane told to strip scripts/pr-gate-coverage.json from #1816 (product-code-only). OWNER/CI-catalog must land baseline rows on develop FIRST, then #1816 rebases+green. No local tests; no merge; no Codex.

Blocked on develop catalog baseline (run at 70ab77ad: Trusted Plan + selected checks FAIL, correct-by-design — lane removed in-PR self-catalog per base-policy rule). #1816 is now product-code-only. OWNER/CI-catalog must add 3 rows to develop scripts/pr-gate-coverage.json (all surfaces docker.data.capabilities+podman.data.capabilities): source.cmd_baha_app_status_collect_go/_app_status_perses_alert_evaluator_0428_152_test_go/_perses_lifecycle_go; then #1816 rebases to green develop. #1809/#1650 new paths already have develop rows (verified) — not catalog-blocked.

#1816 70ab77ad product-code-only (consumer+3-state+tests delivered, scripts/** out of diff); run 45287538708 red ONLY on the missing develop baseline. No lane defect; no merge; no Codex.

UNBLOCKED: Owner merged #1817 -> develop 6df6807e carries the 3 baseline rows. Fresh lane w52 rebases lane-0428-152 (from 70ab77ad, product-code-only) onto develop + exact-head Hosted; Trusted Plan should pass now. Deliverable unchanged: reportPersesSurfaceStatus alert-evaluator observation + command-face assertion. No scripts/** in PR; no merge; no Codex.

Rebase onto develop 6df6807 WORKED — Trusted Plan PASSES at b21d144e. NEW functional fail: cli-0 TestPersesAlertEvaluatorObservationUnappliedReportsNotConfigured (test :300) — unapplied surface returns configured_unverified but must be "not configured". Routed w52: fix alert-evaluator 3-state mapping (unapplied->not configured; applied-unprobed->configured_unverified; owner-gated->unavailable; OK false), don't weaken test. exact-head Hosted; #1816 open until green; no merge; no Codex.

Two Go shards failing at b21d144e (Trusted Plan green post-rebase): cli-0 unapplied->not configured (was configured_unverified, :300); cli-2 PersesStatusSurface :204 reportPersesSurfaceStatus needs authenticated BaseHarbor operator/session the TEST context lacks -> both selected+unselected auth short-circuit. Routed w52: fix 3-state mapping + seed proper auth in test (do NOT assert the auth error), fresh exact-head Hosted. #1816 OPEN; no merge; no Codex.

Head still b21d144e (fix not pushed). run 45294765410 two Go failures (cli-0 unapplied state mismatch -> not configured; cli-2 test lacks authenticated BaseHarbor operator for reportPersesSurfaceStatus at :204). Firm re-routed to w52: push both fixes to a NEW head off b21d144e + fresh exact-head Hosted. Only old runtime job left. No merge; no Codex.

Rotated from stalled w52 (reclaimed; branch b21d144e + PR #1816 preserved, Trusted Plan green). Fresh flash lane w53 dispatched with both fixes baked-in: cli-0 unapplied->not configured 3-state mapping; cli-2 test must seed authenticated BaseHarbor operator (runWithIOAsTestOperator) so reportPersesSurfaceStatus evaluates selected+unselected (not assert auth-error). exact-head Hosted; PR open; no merge; no Codex.

New head 916dccc8 (w53 pushed after rotation). run 45298447080 cli-1: FIX1 over-corrected — (A) unselected Detail must carry verifier reason "Perses is not selected" (not generic wording); (B) selected+contract+silent must be configured_unverified, NOT not_configured (gate not_configured strictly on real non-selection). Routed w53 precise. exact-head rerun; #1816 UNMERGED until green; no Codex; owner keeps running gates.
