---
id: t-20261114-r28-perses-dashboard-identity
card_number: "0428-078"
card_short_title: "Perses identity dashboard"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w078-pr0428-078-appstatus-r3
kanban_status: review
kanban_lane: review
kanban_summary: Deliver identity-provider panels only for verified current Keycloak metrics; do not rely on obsolete SPI assumptions.
kanban_title: 0428-078 · Perses identity dashboard
priority: normal
depends_on: [t-20261114-r28-perses-dashboard-selection]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1606, mcpdev80/baseharbor#1650]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/perses-dashboard-identity/rebase-window-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r2.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/appstatus-integration/round-4.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r3.md"]
---

- [ ] t-20261114-r28-perses-dashboard-identity · Perses identity dashboard #task #release/v0-4-28 #status/review #view/review #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** w078-pr0428-078-appstatus-r3 · **Priority:** normal  
    **PR:** [baseharbor#1606](https://github.com/mcpdev80/baseharbor/pull/1606), [baseharbor#1650](https://github.com/mcpdev80/baseharbor/pull/1650)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/perses-dashboard-identity/rebase-window-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r2.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/appstatus-integration/round-4.md), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-dashboard-selection](t-20261114-r28-perses-dashboard-selection.md)  
**Required by:** [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** w078-pr0428-078-appstatus-r3  
**Priority:** normal  
**PRs:** [baseharbor#1606](https://github.com/mcpdev80/baseharbor/pull/1606), [baseharbor#1650](https://github.com/mcpdev80/baseharbor/pull/1650)  
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
