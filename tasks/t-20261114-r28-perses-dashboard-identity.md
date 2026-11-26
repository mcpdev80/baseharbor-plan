---
id: t-20261114-r28-perses-dashboard-identity
card_number: "0428-078"
card_short_title: "Perses identity dashboard"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w338-0428-078-1855fix2 (e1f6c79e-8ce1-4d2d-b55f-7e3a2658c23d) — re-laned from w327 per NO-RESPONSE rotation
kanban_status: active
kanban_lane: active
kanban_summary: Deliver identity-provider panels only for verified current Keycloak metrics; do not rely on obsolete SPI assumptions.
kanban_title: 0428-078 · Perses identity dashboard
priority: normal
depends_on: [t-20261114-r28-perses-dashboard-selection]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1650, mcpdev80/baseharbor#1855]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/perses-dashboard-identity/rebase-window-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r2.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/appstatus-integration/round-4.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r3.md"]
---

- [ ] t-20261114-r28-perses-dashboard-identity · Perses identity dashboard #task #release/v0-4-28 #status/active #view/active #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** w338-0428-078-1855fix2 (e1f6c79e-8ce1-4d2d-b55f-7e3a2658c23d) — re-laned from w327 per NO-RESPONSE rotation · **Priority:** normal  
    **PR:** [baseharbor#1650](https://github.com/mcpdev80/baseharbor/pull/1650), [baseharbor#1855](https://github.com/mcpdev80/baseharbor/pull/1855)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/perses-dashboard-identity/rebase-window-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r2.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/appstatus-integration/round-4.md), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-dashboard-selection](t-20261114-r28-perses-dashboard-selection.md)  
**Required by:** [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md), [t-20261120-r28-prune-key-too-coarse](t-20261120-r28-prune-key-too-coarse.md), [t-20261120-r28-registerprovider-signal-failclosed](t-20261120-r28-registerprovider-signal-failclosed.md), [t-20261120-r28-restart-persist-signal-dump](t-20261120-r28-restart-persist-signal-dump.md), [t-20261120-r28-runtimetarget-failclosed](t-20261120-r28-runtimetarget-failclosed.md), [t-20261120-r28-signal-one-active-write-path](t-20261120-r28-signal-one-active-write-path.md), [t-20261120-r28-signalregistry-race](t-20261120-r28-signalregistry-race.md)  
**Owner:** w338-0428-078-1855fix2 (e1f6c79e-8ce1-4d2d-b55f-7e3a2658c23d) — re-laned from w327 per NO-RESPONSE rotation  
**Priority:** normal  
**PRs:** [baseharbor#1650](https://github.com/mcpdev80/baseharbor/pull/1650), [baseharbor#1855](https://github.com/mcpdev80/baseharbor/pull/1855)  
**Source:** 
<!-- /generated:links -->

## Goal

Deliver identity-provider panels only for verified current Keycloak metrics; do not rely on obsolete SPI assumptions.

## Scope and file ownership

Own identity dashboard assets and focused tests. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/capability/reference.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/capability/reference.go)
- [internal/identityprovider/keycloak_driver.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/identityprovider/keycloak_driver.go)
- [internal/metrics/prometheus_files.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_files.go)

Create first Keycloak identity dashboard only for validated current version metrics and allowed scope. Do not assume legacy Keycloak SPI. Test no-data and real queried fixture.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Deliver identity-provider panels only for verified current Keycloak metrics; do not rely on obsolete SPI assumptions.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-dashboard-identity](t-20261113-r28-grafana-dashboard-identity.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

## Owner decision — 2026-11-18 (takeover)
No Trusted-Plan allowlist bypass for #1650. Prerequisite 0428-080/#1590 is merged (develop since 409444854) — therefore: retarget #1650 onto develop, re-verify the FULL diff and a fresh exact-head CI; merge only after all gates.

## Retarget status — 2026-11-18 (mission-078)
#1650 retargeted to base `develop` (was lane-0428-080). Head branch `lane-0428-078-perses-identity-on-resolver` advanced non-force `325ab0d4f -> 4f07c807 -> 022c454c` by a regular merge of `origin/develop` (first parent chain lists only the card's commits; `325ab0d4f` is an ancestor of the merge). Base attestation: base `907f16713cbf38693d30c9dadaad7fe299759219`, head `325ab0d4fc0aa80afd7f8e0ba41c86027c8b324d`. Full diff re-verified locally: `go build ./...`, `go vet`, gofmt on all touched files, and identity/perses tests pass (capability, metrics, application, cmd/baha Status/Perses/Identity/Dashboard). CI run 44400488202 @ 022c454c is terminal; all Go gates pass. Two Python CI-structure jobs (`ci-executor-tests`, `Focused Python`) fail identically on develop — pre-existing Owner-scope `.github/**` failures (14 `max-parallel:`, 2 `inputs.gate`/`inputs.runtime` assertions). No `.github/**` edit, no `workflow_dispatch`, no bypass. Evidence: evidence/r28-welle4-2026-11-18/perses-dashboard-identity/rebase-window-1.md.

END_BLOCKED akzeptiert, retarget+merge-zeug am band

Independent read-only review of PR #1650 / 0428-078 (2026-11-19): exact run 44400488202 failed ci-executor-tests and Focused Python; PR changes five reserved `.github/workflows` files despite body saying no such changes. Also `IdentityDashboardEligible` is calculated without requiring the Perses manifest selection/current status. See [review evidence](../evidence/r28-welle4-2026-11-19/codex-review-wave/1650-0428-078-independent-review.md).

## Maintainer review — 2026-11-20 (exact head b6dab95a)
The previous two-PR integration blocker is resolved: #1606 is closed unmerged and #1650 is the sole surviving PR, open, Ready, based on current `develop` `f61ef0f4991cae88727c02b731d862bf395d8984`, exact head `b6dab95a8d73e870841bbe96cbff28cafc216d81`. Exact run [44665488793](https://github.com/mcpdev80/baseharbor/actions/runs/44665488793) completed successfully (34/34 terminal checks, including PR Selected Checks); this is CI evidence only and does not establish the missing dashboard or runtime proof.

Maintainer review remains **REQUEST CHANGES / blocked**. The independent review record is [1650-0428-078-r1.md](../evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r1.md). It verifies that the candidate lacks the card-owned Perses identity dashboard realization/panels and focused schema/panel tests that were present in the closed #1606 tree. It also confirms that `IdentityDashboardEligible` is calculated without gating on Perses selection/current status. A separate agent audit confirms two further authorization defects: `IdentitySelectionWitnessAt` ignores its target data directory/namespace inputs while querying the global registry, so another target's signal may satisfy this target; and any matching provider/ID registry source is accepted without checking native mode or verification (the positive test uses a legacy source with empty mode).

Posted these blockers on [PR #1650](https://github.com/mcpdev80/baseharbor/pull/1650#issuecomment-7029379566), including requested panel assets, Perses status gating, target-scoped native/current source validation, and negative regressions. No approval or merge. Resume only when the surviving PR carries the missing dashboard implementation/tests and fixes the selection, target-authorization and signal-verification gaps, with exact-head required checks executed.

uebergabe dokumentiert (§3.6): die bisherige session w078-…-r2 ist entlassen, ihr zustand war drei commits, die durch einen dateisystem-remote ('origin' = lokaler pfad) NIE bei github ankamen (gh api: No commit found fuer 23a9f656b, 7820a9325, 16d343023). neue lane uebernimmt: push ueber lane-origin, rebase auf develop, EIN run am neuen head

uebernahme erfolgreich gemessen: PR-head ac2a54503794, base = develop 36d075fad77f (merge-base Ahn JA), run 44680875974 completed/success, 34/34 checks fertig, 0 failure, mergeState CLEAN. gate-plan korrekt selectiert: PR Selected Checks success, PR Native gate plan success, native runtime-jobs skipped (der diff selectiert sie nicht). karte bleibt active, weil round-3-akte noch nicht auf main liegt — review kommt erst mit geschriebener evidence (§5.3)

kandidat zugestellt und abnahme bereit: head ac2a54503794 (draft=false, mergeable=clean, base = develop 36d075fad77f, merge-base Ahn JA), run 44680875974 completed/success, 34/34 checks fertig, 0 failure, skipped sind die nativen runtime-jobs, weil der diff sie nicht selectiert (PR Native gate plan = success). evidence round-3.md auf plan main @ 973945a3 mit ls-remote-beweisen. CODEX-REVIEW am exakten head ist bestellt (session 95971e0a, dieselbe reviewer-session wie r1, rolle REVIEW, akte 1650-0428-078-r2.md)

## CODEX review round 2 — 2026-11-20

Review r2 returned **REQUEST CHANGES** on exact head `ac2a5450379492d410a379469e9845b2ce21190d`; see [review evidence](../evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r2.md). The maintainer's exact-head note also requires `IdentityDashboardEligible` to remain false for `ConfiguredUnverified` and a regression through the real local and remote status outputs for selected/unselected Perses. Run `44680875974` is CI success, but 20 of 34 jobs were skipped, including runtime-related gates; no formal GitHub review or approval exists. Returned the card from Review to Wait while the worker pool is full (5/5, no open seats at the 06:28 UTC observation). Resume the owner-assigned card when capacity is available; do not treat the internal review as acceptance or merge approval.

CODEX-REVIEW am exakten head ac2a54503794 = REQUEST CHANGES (akte codex-review-wave/1650-0428-078-r2.md). rezept 1 (karten-assets) und rezept 3 (CI-aufnahme der metrics-tests ueber pr-go-unit-shard.py:118-135) ERFUELLT; rezept 2 offen: der neue TestIdentityAvailabilityRequiresVerifiedPerses (internal/metrics/perses_identity_witness_test.go:164-191) prueft nur capability.PersesStatusNow-rueckgaben, nie den echten applicationStatusResult-pfad und nie IdentityDashboardEligible in lokaler (269-287) noch ferner (173-181) JSON-ausgabe. korrektur = EIN CLI-regressionstest in cmd/baha/ plus mutationsbeweis (gate in app_status_result.go:167-168 raus -> test MUSS rot). befehl hinaus, karte zurueck auf active

## Exact-head re-audit — 2026-11-20 07:05 UTC

The active owner advanced #1650 to `7705a33660736a3ab21b441bebe9057bcccc60fe`; exact run [44692217649](https://github.com/mcpdev80/baseharbor/actions/runs/44692217649) is still in progress (current selection skips native/Core/runtime). Independent diff review confirms both blockers from maintainer comment [7031412203](https://github.com/mcpdev80/baseharbor/pull/1650#issuecomment-7031412203) remain: the eligibility predicate accepts `ConfiguredUnverified`, and the test explicitly expects true for that state; local status tests still do not exercise remote target/output. Prior run 44691504805 failed on superseded head `cd6de5eb0def34d4a190130e6458466c6102a9eb` and is not evidence about this current head. Keep this card Active while the assigned owner continues correction; no Review/acceptance transition is supported. See [sweep evidence](../evidence/r28-welle4-2026-11-20/pr-sweep/continuation-2026-11-20.md).

## Round-4 evidence disposition — 2026-11-20 ~07:15 UTC

The new [round-4 artifact](../evidence/r28-welle4-2026-11-20/appstatus-integration/round-4.md), published on plan main `c84f98fe`, closes the previous local-status coverage gap: its new `cmd/baha` test drives real local `baha status --json` selected/unselected cases, and the mutation proof shows the test fails if the gate is disabled. It does not satisfy the full maintainer acceptance in [comment 7031412203](https://github.com/mcpdev80/baseharbor/pull/1650#issuecomment-7031412203): no remote target/output regression is present, and the predicate still admits `ConfiguredUnverified` while the selected test expects eligibility true for that status. Exact run [44692217649](https://github.com/mcpdev80/baseharbor/actions/runs/44692217649) is green for selected checks but skips Native Keycloak/Core and targeted runtime gates. At the time of this observation, the card remained Active; the later Review transition is reconciled below.

## Review-lane transition re-audit — 2026-11-20 ~07:16 UTC

Plan main `b3f547285541fb45b20b62b5ff3dd4018d269e22` moved 0428-078 from Active to Review after recording that CODEX-REVIEW r3 was requested against head `7705a33660736a3ab21b441bebe9057bcccc60fe` (session ID `95971e0a`). The transition is structurally valid for a review handoff: owner and PR are present. I could not independently verify that the reviewer started or completed; no r3 artifact is in the current plan tree, the reviewer session was not accessible, and GitHub has no formal review. Keep the card in Review as the recorded handoff, with `resolution` empty; this is not acceptance or merge approval.

The substantive requirements remain unresolved. The current PR diff still accepts `ConfiguredUnverified` and the new test explicitly expects eligibility true in that state, contrary to the verified-only contract. The added regression covers local status JSON but not remote target/output. Exact run 44692217649 completed successfully for selected jobs, but Native Keycloak/Core and targeted runtime checks were skipped. GitHub still reports #1650 OPEN+Ready, mergeable, with no formal reviews or later comment resolving maintainer finding 7031412203. Do not accept or merge until the review result and remaining correctness/runtime requirements are addressed.


## Review r3 disposition and wait transition — 2026-11-20 ~07:20 UTC

The exact-head CODEX-REVIEW r3 artifact [1650-0428-078-r3.md](../evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r3.md) returned **REQUEST CHANGES** on `7705a33660736a3ab21b441bebe9057bcccc60fe`. It confirms the new local production status test and mutation proof, but finds no regression through a non-local target / remote status return. This completes the Review handoff without accepting the PR. The review's suggested remote-positive `configured_unverified` expectation conflicts with maintainer comment [7031412203](https://github.com/mcpdev80/baseharbor/pull/1650#issuecomment-7031412203), which explicitly requires verified-only eligibility; resolve that contract conflict by keeping `ConfiguredUnverified` ineligible before merge. Native Keycloak/Core and targeted runtime acceptance also remain skipped/unproven.

I moved 0428-078 from Review to **Wait** because the started correction is paused after REQUEST CHANGES and the fresh read-only Codeman pool snapshot reports workers 5/5, no open seats, reviewer/merger 1/1. Wait reason records the concrete next work: remote status regression, verified-only predicate/test, applicable runtime acceptance and exact-head checks when capacity is available. PR #1650 stays OPEN+Ready; no formal GitHub review or approval exists, and `resolution` remains empty.

CODEX-REVIEW r3 am exakten head 7705a3366073 = REQUEST CHANGES (akte codex-review-wave/1650-0428-078-r3.md, reviewer-session 01a1f4dc, read: PR head vor/nach review gleich). erfuellt und bestaetigt: dashboard-realisierung, mutationsbeweis aus round-4.md stimmt mit dem kandidaten-stand, CI run 44692217649 terminal, mergeable=clean, base develop 36d075fad77f. EIN offener punkt: der neue test (cmd/baha/app_status_perses_gate_test.go:111-140) faehrt nur ein LOKALES target (configureTestTarget, cmd/baha/target_test_helpers_test.go:44-56); die serialisierte FERNE statusantwort (:173-181) ist nicht abgedeckt. korrektur = ein remote-target-fixture mit nicht-lokalem access provider im selben test, assertions auf die serialisierten felder, mutationsbeweis fuer den fernen fall. korrekturauftrag hinaus, akte round-5.md

RUECKNAHME EINES COORDINATOR-SPRUCHS, belegt durch ihre eigene mutation: ich hatte (A) WAHR geantwortet, weil hasRemoteApplicationTarget (cmd/baha/app_remote_status.go:14-16) eine reine datenbedingung ist. WIDERLEGT: collectApplicationStatusResult ruft zuerst collectApplicationStatus (cmd/baha/app_status_result.go:130 -> cmd/baha/app_observe.go:32-41, newApplicationStatusCollection :36), und der scheitert an einem fernen target mit ErrUnavailable VOR der gate-Berechnung (app_status_result.go:144-146) und VOR dem remote-branch (zeile 147-153). ihr mutationsbeweis (akte round-5.md: 'gate entfernt -> ferner fall FEHLGESCHLAGEN, weil die gate nie getroffen wird') ist die probe, die ich von jeder lane verlange. PRODUKTBEFUND: der kommentar app_status_result.go:138-143 behauptet 'Computed before the remote-target early return below so remote-status --json also carries it', die ausfuehrung widerspricht dem - die dreizustand-vertragsseite (not_configured | configured_unverified | verified) erscheint auf der fernen JSON-oberflaeche NIE. variante (2)/serialisierter collector bleibt verboten (app_remote_status.go traegt 0 referenzen auf Perses/DashboardEligible, gemessen). BEFEHL r6, write-set von MIR ERWEITERT, grund ist diese notiz: zusaetzlich cmd/baha/app_status_result.go (nur die REIHENFOLGE der berechnung) und ggf. cmd/baha/app_observe.go (ferner zweig ueber collectResolvedApplicationStatus, app_observe.go:43-47, behandelt isRemoteApplication bereits korrekt); gate selbst (internal/capability/perses_selection.go:439, wert :153-155) und .github/** NICHT ZU AENDERN; ihr lokaler test bleibt unangetastet; neue ferne testfaelle an der echten oberflaeche, praedenz aus cmd/baha/app_maintenance_client_test.go:165/:543/:719, OHNE live-mTLS, OHNE Core-stub; mutationsbeweis (i) felderweitergabe im remote-branch entfernen -> NEUER test ROT, (ii) gate verbiegen -> ROT, (iii) ihr bisheriger gruen-befund muss verschwunden sein. ihr dreistuendiger stillstand auf head 7705a3366073 geht auf meine fehldeutung zurueck, nicht auf sie

abnahme bestellt, alle drei bedingungen der einfrier-regel von mir gemessen: (1) head cb985bdeb50e eingefroren, branch lane-0428-078-perses-identity-on-resolver = refs/pull/1650/head, upd 09:14:51Z; (2) run 44709089717 completed/success am exakten head, base.sha = develop-spitze 681700ca66f3, draft=false, mergeable=clean; (3) akte appstatus-integration/round-6.md (124 zeilen) auf origin/main @ c115b4ae mit 'FREEZE PROOF (at exact head cb985bdeb5)' und 'MUTATIONSPROOF (three lines, verbatim)'. inhalt: reihenfolge-anderung, damit die perses-dreizustandsseite im REMOTHEN pfad mitgetragen wird, gate-logik unveraendert. CODEX-REVIEW r4 unterwegs (session 95971e0a, rolle REVIEW, akte 1650-0428-078-r4.md), mit mutationspflichten und der bitte, die mehreren branches mit 0428-078 im namen gegen §3.8 zu beurteilen

test nur: verdict am eingefrorenen head cb985bdeb50e, ein punkt app_status_result.go:163-167

verdict am eingefrorenen head liegt vor (akte codex-review-wave/1650-0428-078-r4.md, PR head before/after review = cb985bdeb50e/cb985bdeb50e - dritte gueltige abnahme in folge). resultat REQUEST CHANGES, EIN punkt: die eignungsformel in cmd/baha/app_status_result.go:163-167 laesst PersesStatusConfiguredUnverified weiterhin durch; erwartet wird verified plus echter Keycloak-nachweis, fail-closed fuer not_configured UND configured_unverified, auf BEIDEN oberflaechen, gegen den fortgeltenden maintainer-akzeptanzkommentar 7031412203. ERLEDTIGT bestaetigt: reihenfolge-loesung (remote-branch vor collectApplicationStatus, :179-199), der r5-fehler ist weg, mutation ueber IdentitySelectionWitness.NonForgeableAvailable() an internal/capability/perses_selection.go:109-110 faellt den fernen test; P6/P7 sauber (ein branch = PR-head, kein .github/, kein scripts/, keine capability-beruehrung). GRENZERWEITERUNG VON MIR, begruendet: der write-set in app_status_result.go war auf die REIHENFOLGE beschraenkt; fuer :163-167 erweitere ich ausdruecklich auf die eignungsformel, weil der reviewer dort das wartende akzeptanzkriterium sieht. verboten bleiben internal/capability/perses_selection.go (:109-110 und :436-442), .github/, scripts/ - muessten sie die capability-datei antasten, ist das QUESTION an mich. BELEGTE KORREKTUR AN MIR: meine referenz perses_selection.go:439 war an diesem head falsch (dort sitzt DashboardEligibility.Status, :436-442; nachweisstelle ist :109-110). develop ist auf dbe7fbc3905b weiter (0428-174 gemergt), daher rebase als letzter freeze-schritt

abnahme bestellt, alle drei einfrier-bedingungen gemessen: (1) head 0baeaf555010 eingefroren, branch lane-0428-078-perses-identity-on-resolver = refs/pull/1650/head = derselbe SHA, draft=false, mergeable=clean, updated_at 10:37:26Z (kein push nach dem einfrieren); (2) base = develop-spitze dbe7fbc3905b, merge-base --is-ancestor = JA; (3) run 44720819476 completed/success am exakten head; (4) akte appstatus-integration/round-7.md auf main @ 81370cda, 145 zeilen, nennt den head sieben mal, 0 checkboxen, mutationsbeweis ueber perses_selection.go:109-110. inhalt nach owner-anweisung: EIGNUNGSFORMEL in cmd/baha/app_status_result.go:163-167 auf 'verified only' - beide nicht-verifizierten zustaende duerfen nicht mehr durchgehen; perses_selection.go bleibt verschlossen. ihre END-meldung fehlte (vierte lane dieser schicht, die korrekt liefert und dann schweigt); zustellung war vollstaendig, die karte steht trotzdem erst jetzt auf review, weil ich vorher nichts behaupten will

abnahme abgeschlossen mit verdict REQUEST CHANGES, gueltig weil der head vor/nach dem lesen unveraendert war
(0baeaf555010). akte codex-review-wave/1650-0428-078-r7.md @ main, 105 zeilen, lesendes review, kein merge. BESTAETIGT:
internal/capability/perses_selection.go ist im SHA-genauen diff unberuehrt (pruefpunkt null, ihre grenze haelt), und das
verified-only predicate ist fail-closed richtig in cmd/baha/app_status_result.go:165-177 mit demselben wert auf beiden
statusflaechen (:188-206 remote, :299-317 lokal). ZWEI BLOCKIERENDE befunde: P3 target-isolation - ihr
internal/metrics/perses_identity_witness.go nimmt dataDir/namespace an und dokumentiert sie als scope (:37-40), gibt sie
weiter (:64), verwendet sie aber NICHT zur einschraenkung, und der test seedet nur eine source
(perses_identity_witness_test.go:28-65), also kein gegenbeweis target A/B: signal-lookup muss durch das konkrete target
und den uebergebenen state-root/namespace eingeschraenkt werden, fail-closed bei nicht aufloesbarer zuordnung. P4
produktiver abnehmer - 'git grep' im kandidaten findet KEINEN produktionsaufrufer von
PersesIdentityDashboardAvailability/identityDashboardCatalog, alle verwendungen liegen in den neuen tests: ein test-only
golden ist kein release-nachweis, der katalog muss an den tatsaechlich verwendeten Perses provision-/export-pfad, und die
byte-treue gegen das gepinnte perses-schema oder einen echten export belegt werden. wenn P4 in
internal/application/perses_runtime.go oder internal/capability/** reichen musste: STOPP + MELDUNG an mich statt
write-set-erweiterung (§4.2). dazu P1 (positiver fall laeuft nie durch das produktive predicate bis
identity_dashboard_eligible=true, cmd/baha/app_status_perses_gate_test.go:142-157), P2 (remote-fixture endet vor dem
serializer), P5 (ihre witness-sonde haengt an nur einem test - die unabhaengigkeitsfrage, die mir heute schon die
068-korrektur eingetragen hat), P6 ('PR · Native · ...' und 'PR · Selected Runtime' waren skipped, nicht passiert). NEU
FUER ALLE BAHNEN: develop ist f1c2c34236f4, weil der owner #1710 (0428-068) um 11:04:29Z gemergt hat - bei ihrem letzten
commit auf diese spitze rebasen.

abnahme bestellt, alle drei einfrier-bedingungen von mir gemessen: (1) head 9add5e8a2122 = branch = refs/pull/1650/head,
ein commit auf develop 96f2ae11a25a, draft=false; (2) merge-base --is-ancestor = JA nach fetch; (3) check-runs am exakten
head completed/success (source format, go unit packages, go-vet, go-build, trusted plan, native gate plan) - der
runs-endpoint lieferte bei mir leer, deshalb zeugen die check-runs am head und nicht ich. INHALTLICH: sie haben den
owner-r7-auftrag ausgefuehrt und den null-abnehmer-katalog aus dem PR ENTFERNT (4 dateien uebrig, die drei katalog-pfade
tauchen im diff nirgends mehr auf), der witness bleibt mit der von mir verlangten consumer-zeile
(perses_identity_witness.go -> cmd/baha/app_status_result.go:343) und P3 target-isolation in beide richtungen. der katalog
lebt auf karte 0428-181 weiter, sequenziert nach #1684. WARUM ICH ZWEIMAL NICHT BESTELLT HABE: ihre END-meldung
fehlte zum vierten und dann auch beim shrink, und die akte round-8.md war im ersten augenblick noch nicht auf main -Resume-
trigger war bei mir 'terminaler run ODER akte', jetzt beides da. HALTEN SIE STILL: kein push, kein rebase, kein dritter
commit, solange die abnahme laeuft (§3.3 regel 8, ein bewegter head macht das verdict wertlos). wenn ein befall kommt, hole
ich sie zurueck.

UEBERGABE AN DEN OWNER / CODEX, von mir angeordnet nach seiner anweisung dieses augenblicks: 'ich uebernehme ab jetzt
karte 0428-078 / PR 1650 zur fertigstellung ... bitte die bestehende w078-lane sauber freigeben und 0428-078 an mich/Codex
uebergeben'. sein uva review am eingefrorenen head 9add5e8a2122 lautet REQUEST CHANGES (akte
evidence/r28-welle4-2026-11-20/pr-sweep/review-1650-2026-11-20.md), drei punkte: kein dashboard-delivery/produktintegration
im diff, witness-isolation nach echtem target/tenant/state-root nicht belegt, positiver verified-weg nicht ueber die
oeffentliche status-JSON-ausgabe nachgewiesen; run 44737589479 ist gruen, aber kein abnahmenachweis dafuer.
LANE: angehalten (kein edit, kein commit, kein push, head bleibt liegen), liefert eine handoff-akte
appstatus-integration/handoff-078.md und dann END; sitz wird danach freigegeben. MEIN LAUFENDER REVIEW: darf zu ende
gehen und sein verdict dokumentieren, danach KEINE dritte runde von mir - der owner aktualisiert exakt-head CI und merged
selbst, wenn alle erforderlichen checks und der verdict gruen sind. SCHREIBGRENZEN, die ich ihm ausdruecklich mitgebe:
internal/capability/perses_selection.go bleibt verschlossen (owner-anweisung von heute vormittag), und
internal/application/perses_runtime.go wird von #1684 (0428-083) geschrieben - die karte 0428-181 haengt an derselben
sequenz. ihr eigener abnehmer-katalog liegt auf 0428-181, damit aus dieser uebergabe kein zweiter toter baum wird.

ZWEI UNABHAENGIGE VERDICTS AM SELBEN eingefrorenen head 9add5e8a2122, und sie DECKEN SICH - dokumentiert, damit der
uebernehmer nicht zwei mal suchen muss: (1) sein uva review, akte pr-sweep/review-1650-2026-11-20.md: REQUEST CHANGES, punkte
'kein dashboard-delivery/produktintegration im diff', 'witness-isolation nach echtem target/tenant/state-root nicht belegt',
'positiver verified-weg nicht ueber die oeffentliche status-JSON-ausgabe nachgewiesen'; run 44737589479 gruen, aber kein
abnahmenachweis. (2) MEIN CODEX-REVIEW, akte codex-review-wave/1650-0428-078-r8.md (66 zeilen, ROLLE-Label, 'PR head
before/after review = 9add5e8a…/9add5e8a…', also gueltig): REQUEST CHANGES mit derselben richtung - P1 predicate korrekt,
aber serialisiertes positives resultat fehlt; P2 der oeffentliche remote-serializer wird nicht durchfahren (rezept:
remote-fixture durch das produktive status-command + writeJSON, felder decodieren); P3 BLOCKER 'actual Target/tenant binding
and unresolved mapping'; P5 mutations noch nicht vollstaendig isoliert ('same test identity'). STRUKTURELL BESTAETIGT von
beiden seiten: P4 'catalog removed; witness has a production call site' = PASS, P6 geschuetzte dateien = PASS
(perses_selection.go unbewegt), P7 exact-head CI + skipped cells = PASS.
LANE: haelt weiter an (handoff-akte + END angefordert, kein push, head bleibt liegen). SITZ: bleibt belegt bis ihre
uebergabe-akte auf main ist; danach freigabe und der sitz geht an 0428-182 (die naechste datei-disjunkte karte).
HERRIN DER KARTE ist jetzt ihr sweep - ich bestelle keine dritte runde und schreibe keinen fremden claim um.

## Board reconciliation — 2026-11-20

The latest exact-head review recorded REQUEST CHANGES on PR #1650. The Codeman live inventory has no busy Codex reviewer assigned to this card, so implementation is paused. This is started work waiting for correction, not an Owner-decision or technical-impossibility blocker.

## Codex follow-up — 2026-11-20

- Reopened for the explicitly assigned Codex correction after the exact-head r8 REQUEST CHANGES review. PR #1650 candidate `7e185c80d1b66cd86e1a1e7daf0bdfbb21b2a109` binds the Keycloak signal to the canonical Target state root and namespace via the registration ID derived by the Keycloak runtime; endpoint values are not treated as tenant IDs. Mismatched roots, missing target identity, legacy signal IDs, wrong owner, wrong mode, wrong verification, and a path that differs from the current Keycloak descriptor fail closed.
- The public status result now shares one setter for local and remote faces. The remote regression drives `appStatusCommand(...).Run(..., []string{name, "--json"}, ...)`, which reaches the production `writeJSON` encoder. `PersesStatusNow` remains fail-closed and does not synthesize `verified`; its positive serialized result test supplies `verified` at the result boundary plus a real target-bound witness.
- Local focused checks pass: `go test ./internal/metrics -run '^TestIdentityWitness' -count=1` and `go test ./cmd/baha -run '^TestIdentityDashboard' -count=1`. Target-binding mutation fails `TestIdentityWitnessIsolatedToConcreteTarget`; discarded-witness mutation fails `TestIdentityDashboardVerifiedStatusResultSerializesPositive`; unverified-accepted mutation fails `TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses`.
- The earlier run [44833030423](https://github.com/mcpdev80/baseharbor/actions/runs/44833030423) on `3aff73c48e25cd230b72fef86199c68492c858da` was cancelled after the stricter descriptor-path check was added. Exact hosted PR run [44833386349](https://github.com/mcpdev80/baseharbor/actions/runs/44833386349) completed FAILURE on `7e185c80d1b66cd86e1a1e7daf0bdfbb21b2a109`: CLI shards fail on missing authenticated operator context, `internal/logs` package tests fail because Loki mTLS fixture files are absent, and the selected Docker identity runtime job cannot configure `atomic-docker-identity`. Focused identity witness/dashboard tests do not appear among the failing tests. The shared CLI-entrypoint, Loki-fixture, and runtime-target gates overlap active/waiting cards 0428-198/#1726, 0428-204, and 0428-202/#1732. The card is paused in `wait` until those exact shared gates are resolved, then #1650 must refresh against current `develop`, rerun exact CI, and receive a fresh review.
- The current `.github/workflows/ci.yml` admits PR bases `develop`, `main`, and `lane-*`. A feasible cycle break after 0428-204 completes is to base #1726 (`lane-0428-198-cli-shard-operator-env`) on #1732 (`lane-0428-202-lokifix`), run exact combined checks, integrate #1726 into #1732 if green, then rerun and integrate #1732 to `develop`. This is a candidate sequence only; no foreign PR base was changed.
- Demo #167 fixed target bootstrap ordering and passed exact hosted run `44839113085`; it merged as `0130070e2bf1b8694cc2dcc1b2df3f539b161508`. The BaseHarbor Demo source variable now points to that SHA. #1650 was rebased onto current `develop` `40cb28c758b02960356434b630086a341ebe1738` and updated to head `20a35cd7420d7fd71ace5999e6550f5ae761f6e9`; exact run `44839989647` has since completed FAILURE (details below). Its local Perses status test now authenticates through a signed, in-process OIDC provider and persists a real session rather than bypassing enforcement. `go test ./cmd/baha -run '^TestIdentityDashboard' -count=1` and `go test ./internal/metrics -run '^TestIdentityWitness' -count=1` pass; independent review approves the fixture change.
- Exact run `44839989647` is now terminal FAILURE on unchanged head `20a35cd7420d7fd71ace5999e6550f5ae761f6e9`. Direct `gh run view ... --json jobs` confirms failures in `cli-0..3`, `packages`, `PR · Selected Runtime (atomic/docker/identity, docker, identity) / Executed docker · identity` (job `136646249769`), and aggregate `PR Selected Checks`. CLI failures are the shared missing operator-context seam owned by active 0428-204 / #1726; package failures are three missing Loki mTLS fixtures owned by 0428-202 / #1732. The selected runtime log uses the merged Demo pin `0130070e` and shows the first target creation now gets past selector ordering but fails because the standalone acceptance invocation has no authenticated operator. This remains a separate bootstrap/auth-contract question; do not bypass auth or edit active foreign-owned files. Keep #1650 open until the shared gates and this exact runtime gate pass, then refresh against current `develop`, rerun exact CI, and obtain fresh review.
- Independent exact-head review of `20a35cd7` found that the new remote JSON path replaced `collectRemoteApplicationStatus` with synthetic `unverified` data, dropping the retained-publication, live readiness and degraded/error behavior. Fixed in commit `97aa1a8607f5474f15d8d7a0e2cacaf095492504`: remote status now comes from the existing authenticated collector, its errors pass through, and Perses/identity metadata is added to that real status. Regression tests preserve ready/degraded JSON status fields and assert missing Connector session fails closed. Local checks pass: `go test ./cmd/baha -run 'TestIdentityDashboard|TestRemoteApplicationStatusNeverInfersAbsenceFromLocalFiles' -count=1`, `go test ./internal/metrics -run '^TestIdentityWitness' -count=1`, `go build -o /tmp/baseharbor-baha-0428-078 ./cmd/baha`, and `git diff --check`; independent delta review APPROVED. New exact run [44841930757](https://github.com/mcpdev80/baseharbor/actions/runs/44841930757) has since completed FAILURE on this head. It failed CLI shard jobs `136652290195`, `136652290140`, `136652290268`, `136652290501`, package job `136652290169`, and selected Docker identity runtime job `136652788008`, plus aggregate `136653596963`. CLI shards still show the missing authenticated operator context (0428-204/#1726); packages still show the same three missing Loki client-certificate fixture failures (0428-202/#1732); runtime fails at first `baha target create` with the operator-auth message even after the Demo selector-order fix. This confirms a distinct first-target test-bootstrap/auth contract gap. No merge; keep #1650 open until these exact mandatory gates pass and fresh full review is clean.

- Producer-to-witness integration proof added in `28c18f02039f0957544146cf5d0db2a1561a4220`: `Apply()` now routes through the same `RegisterKeycloakMetricsSignalsAt` producer seam exercised by `TestIdentityWitnessFromKeycloakProducer`, which creates canonical Target Keycloak files, registers the real signal, and asks `IdentitySelectionWitnessAt` to consume it without hand-seeding a `SignalSource`. Local checks pass: `go test ./internal/identityprovider -run '^TestKeycloakSignalRegistration' -count=1`, `go test ./internal/metrics -run '^TestIdentityWitness' -count=1`, `go test ./cmd/baha -run 'TestIdentityDashboard|TestRemoteApplicationStatusNeverInfersAbsenceFromLocalFiles' -count=1`, `go build ./cmd/baha`, and `git diff --check`. Exact PR run [44846209015](https://github.com/mcpdev80/baseharbor/actions/runs/44846209015) is running on this SHA; the native gate plan passed and mandatory Go shards, focused validation, Trusted Plan, source format and candidate checks are pending/in progress. Keep the PR open until exact required checks and fresh review are green; the previous head's shared operator-auth/Loki/runtime failures remain unresolved.

- Exact run [44846209015](https://github.com/mcpdev80/baseharbor/actions/runs/44846209015) completed FAILURE on `28c18f02039f0957544146cf5d0db2a1561a4220`. It proves the new producer-to-witness test executed successfully in `internal/metrics`; selected `identity-provider-package-tests`, `go-build`, `go-vet`, source format, `PR · Exact Candidate`, `PR · Trusted Plan`, and `Workflow policy` also pass. Remaining failures are CLI shards `136666535981`, `136666535996`, `136666536022`, and `136666536069` (missing authenticated operator context, shared with 0428-198/#1726 and 0428-204), `packages` job `136666535997` (three Loki datasource tests missing `providers/loki/shared/service-access/pki/client-cert.pem`, 0428-202/#1732), and selected Docker identity runtime `136666960147` (first `baha target create ... --access local-podman` denied because no authenticated operator). No merge. The implementation/test work is complete locally and exact targeted checks pass; task moves to wait until those shared authorization/runtime and Loki gates are resolved, then rebase and rerun exact required CI and obtain fresh review.

dispatched post-recovery 2026-11-23

H-V39 finding: #1650 Trusted Plan FAILS on the 0428-242 catalog guardian for NEW file internal/metrics/perses_dashboards_keycloak.go (split from perses_dashboards.go; #1650 ingress commit 0c1b8ca2 registered 2 rows but missed this new file). So #1650 gate-red = card 0428-260 (1 catalog row / package row), INDEPENDENT of the Owner double-writer question. Lane frozen pending Owner ownership decision; gate clears via 0428-260 regardless.

Owner routed the additive hop to the existing owner (w078): develop d4fa8c589 (#1813) registers internal/metrics/perses_dashboards_keycloak.go (the file that aborted #1650 Trusted Plan). w078 re-engaged for ONE safe additive merge of develop + exact Headed rerun (no force-push, no double-writer conflict resolution -> STOP+QUESTION on conflict). Gate clears via catalog; ownership concern superseded by this additive routing.

RESTART (71ff001a) of dead bbf9d49f. ONE safe additive hop of develop d4fa8c589 (registers perses_dashboards_keycloak.go) into lane-0428-078-perses-identity-on-resolver; abort+QUESTION on conflict with owner commits.

DO-NOT-MERGE guard (Owner): #1650 IdentityDashboardEligible=true depends on #1810 providing a reachable 'verified' path. #1810 currently makes verified unreachable; until 0428-186 lands a real probe (or Owner decides the eligibility instrument), #1650's positive case is unreachable -> hold merge even when its own hop/consent CI is green. #1810 is the active functional dependency for #1650 shipping.

Reconciled: #1650 head now 884d2818, exact-hosted run 45283500012 active. 11-file diff adds test-only app-exec gate admission + identity metrics realization but does NOT change PersesStatusNow nor add the real per-target probe. 0428-186 positive-path OPEN -> #1650 merge HELD on probe (0428-186) + target-isolated query acceptance. DO NOT MERGE (frost + dependency).

END (884d2818, run 45283500012 terminal success, clean hop d4fa8c589, docker/identity+all gates+Trusted Plan green) ACCEPTED as CI-green, but functional ACCEPTANCE GAP found (Owner, independent): dashboard queries use job=keycloak + application/environment labels; production provider-class payload (prometheus_files.go:175) is job=baseharbor-providers + baseharbor_provider/source (no app/env). Queries can't match real series. Correction: align to job=baseharbor-providers,baseharbor_provider=keycloak, add Hosted real-output regression. DO NOT MERGE — held on this label fix AND #1810 probe dependency. No Codex.

Merge HELD on THREE independent grounds (verified): (1) #1810 real per-target probe not landed (02c9b960 fail-closed) -> identity_dashboard_eligible unreachable; (2) label-contract mismatch: dashboard queries job=keycloak+app/env vs production provider payload job=baseharbor-providers+provider/source (fix routed to w078); (3) DELIVERY GAP: #1650 diff touches internal/metrics/** only; internal/application/perses_runtime.go has NO PersesDashboardCatalog/IdentitySelectionWitness integration, so the new keycloak dashboard is DEFINED but NOT wired into the production provision/export path. That consumer is card 0428-181 (planned, depends #1684). => OWNER SCOPE/RELEASE DECISION: either 0428-181/#1684 land the export path, or Owner records a deliberate decision that #1650 ships dashboard-definition-only. Green CI + mergeable metadata do NOT deliver the dashboard. No merge; no Codex.

OWNER DECISION Option A: #1650 stays aimed at a FULLY FUNCTIONAL production Perses delivery/export consumer; do NOT merge a dashboard-definition-only artifact. Merge HELD on: (1) #1810 real probe (verified/eligibility); (2) label-contract fix (provider payload job=baseharbor-providers); (3) delivery/export consumer = card 0428-181 (NOT this PR). #1684 reconciled: it is superseded, its content (0428-083 datasource seam) IS on develop via merge #1745 (57d2f2751) — dependency satisfied, no reopen; 0428-181 prerequisite landed and can proceed. Green CI/mergeable != delivery. No Codex.

Head 84943695: .ci_touch_1 removed -> Trusted Plan + Source Format GREEN (no catalog PR needed). REAL acceptance dependency (Option A): cmd/baha/app_status_result.go still derives persesStatus via static capability.PersesStatusNow(selection) BEFORE identityDashboardBackendEligible. #1810 supplies the real per-target probe metricsprovider.PersesBackendAnswersStatusNow. #1650 MUST (a) stack/rebase on #1810 (merged first) and (b) consume #1810's probe result in the eligibility derivation — do NOT let dashboard JSON/export alone be eligible on static status. Plus full 0428-181 production export consumer. DO NOT MERGE until #1810 merged + probe consumed + 0428-181 delivered. No Codex.

Head 84943695 CONFLICTING/DIRTY vs develop 951014e9 (#1810 merged after my base 6df6807). Routed w078 (existing lane, no overlap): rebase onto 951014e9 + resolve + integrate #1810 probe in app_status_result.go:313 (consume PersesBackendAnswersStatusNow, not static PersesStatusNow) + keep keycloak provider-label fix. exact-head Hosted rerun (old 45297432220 predates integration). Full 0428-181 delivery still required. No merge; no Codex.

Rotated from stalled w078 (reclaimed; branch head 84943695 + PR #1656 preserved). Fresh laptop lane w55 dispatched with concrete rebase+probe-integrate mission: rebase onto develop 840c4a6b, resolve conflicts, replace static capability.PersesStatusNow at app_status_result.go:313 with merged metricsprovider.PersesBackendAnswersStatusNow so eligibility requires the real probe, keep keycloak label fix, exact-head Hosted. Full Option-A also needs 0428-181 (w54). no merge; no Codex.

Parked by owner stop; w55 confirmed no-push. New dep edge: #1650 -> #1815 (fixture ownership).

Vehicle moved to PR #1818 (branch lane-0428-078-cf-fix, base cd2fcda) which carries the rebased 0428-078 (real-probe eligibility consumed, keycloak label fix, dup fixture commit 378ff1afa dropped per #1815 ownership). Old #1650 stays parked DIRTY per owner. w55 owns 0428-1818: fix the failed Go-packages job (run 45307918949, logs at terminal), rerun exact-head. If the failure is the shared operator-fixture, it depends on #1815 merge — no re-add here. Full Option-A still needs 0428-181 export consumer.

Scope ruling (owner): persesDashboardCatalog is observability-only by design (Prometheus/Loki/Tempo) and excludes identity dashboards -> keycloak-identity must NOT be added there. #1818 Go test TestPersesKeycloakDashboardQueriesSelectRealProviderLabels must target the SEPARATE identity-panel producer (0428-181 export consumer path) OR 0428-078 needs a target-bound IdentitySelectionWitness on the identity producer, never gated through backendForKey/PersesDashboardAvailability. w55 resolving package ownership, no catalog-availability edits until decided. Docker consent exit-41 = OWNER authorization (held). #1818 still has #181 (w54) dependency for the identity producer.

w55 kept as same-candidate correction seat (idle, no push). Not a stall to rotate — genuine dep+auth block.

GREEN exact-head candidate: head 306a2b1ea (base develop), PR checks 23 pass / 0 fail incl Podman data-capabilities. keycloak-identity test retargeted to the 0428-181 identity producer (#1819), NOT added to observability catalog (per owner scope ruling); consent gate satisfied without weakening Consent validation. Depends on #1819 (0428-181) being accepted — identity producer is the seam. Ready for Owner exact-diff acceptance; merge held (frost + Owner-direct channel).

EXACT head advanced to 20fc1cb7 (owner rebased the same 4 commits onto develop 3ebfb90d; 8-file/959-line, conflict-free, diff-check clean). Prior head 306a2b1e passed all selected Docker/Podman runtime gates + PR Selected Checks (run 45304374778/45313048505). Hosted PR checks on 20fc1cb7 NOT yet appeared -> NOT yet green on this SHA; watching. keycloak test retargeted to #1819 producer (not observability catalog); consent satisfied without weakening. Acceptance = Owner exact-diff on final SHA 20fc1cb7 once CI lands. #1819 dependency.

CI GREEN on exact head 20fc1cb7 (base develop 3ebfb90d, run 45316544436): PR checks 0 fail, MERGEABLE. keycloak-identity test retargeted to #1819 identity producer (not observability catalog); consent satisfied without weakening Consent validation. Candidate complete -> awaiting OWNER exact-diff acceptance + #1819 dependency resolution. Owner keeps PR open; no merge (frost). Do NOT close until owner accept + #1819 accepted.

VERIFIED GREEN final head 20fc1cb7d496 (develop 3ebfb90d) run 45316544436 completed/success: go unit/packages, build/vet, all 5 selected Docker/Podman gates, PR Selected Checks -> 23 pass / 0 fail, MERGEABLE. keycloak-identity test targets the #1819 identity producer (not observability catalog); consent satisfied without weakening. GATED behind dependency #1819 (still DRAFT, owner target-bound ruling pending). Dependency order (AGENTS 3.3.8): accept+merge #1819 (0428-181 producer) FIRST, then Owner exact-diff accept #1818. Keep #1818 OPEN until both; no merge (frost + owner-direct channel).

REOPENED review->active: #1818 green CI (run 45316544436) is achieved by a SCOPE VIOLATION — diff adds keycloak-identity to persesDashboardCatalog() (perses_dashboards.go), forbidden by owner ruling (identity excluded from observability catalog). Not a valid candidate. Correction required: remove the catalog addition + retarget TestPersesKeycloakDashboardQueriesSelectRealProviderLabels to the real identity producer. Fork A (local metrics assembler) vs C (consume #1819/0428-181 producer seam, no dup) routed to OWNER; coordinator recommends C (single producer; aligns with #1818->#1819 dependency). w55 holds; do not touch observability catalog. Depends on #1819 merge for C.

BRANCH CONTAMINATION confirmed by file evidence: #1818 PR head on lane-0428-078-cf-fix = 20fc1cb7 which has 2 keycloak-identity catalog hits (FORBIDDEN edit) — re-introduced when w53-0428-152 (a DIFFERENT card's session) FORCE-PUSHED 0f20a3b9->20fc1cb7. Clean head is 0f20a3b9 (0 catalog hits, real-probe consumption, no violation). 20fc1cb7 is INVALID for #1818; correct from 0f20a3b9. Blockers: (1) owner A-vs-C (owner leans C: test -> #1819 seam) + #1819 merge (0428-273), (2) Docker consent --confirm-candidate exit-41 (owner authz). w55 holds on clean 0f20a3b9, will NOT build on 20fc1cb7. §4.3: cross-lane force-push on this branch must stop — w55 owns lane-0428-078-cf-fix.

## PR lineage disposition — W16

PR #1650 remains listed as the contaminated-lineage audit. Clean successor PR #1855 is the current candidate for this card. PR #1818 remains an old, stale head and is not qualifying evidence for this card.
