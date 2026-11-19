---
id: t-20261119-hunt-metrics-registration-visibility-only
card_number: "0428-123"
card_short_title: "registry-Eintrag ohne"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w123-0428-123-pr1693-regvis-r5
kanban_status: review
kanban_lane: review
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-123 · registry-Eintrag ohne
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1693]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44557894265", "https://github.com/mcpdev80/baseharbor/actions/runs/44578337221"]
---

- [ ] t-20261119-hunt-metrics-registration-visibility-only · Application-class metrics registration ist sicht-only: registry-Eintrag ohne effectiven scrape/export #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** w123-0428-123-pr1693-regvis-r5  
    **PR:** [baseharbor#1693](https://github.com/mcpdev80/baseharbor/pull/1693)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44557894265), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44578337221)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w123-0428-123-pr1693-regvis-r5  
**Priority:** not set  
**PRs:** [baseharbor#1693](https://github.com/mcpdev80/baseharbor/pull/1693)  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
## Befund (intake aus hunt-918)
Befund 1 (MEDIUM): Application-class metrics registration ist sicht-only: registry-Eintrag ohne effective scrape/export. Akzeptanz: registriert==exportiert Invariante mit test; oder registrierung schlaegt fehl statt still. Kein Overlap mit dem gefixten List-Pfad (dd62b9d3).
Erlaubtes write-set (vorschlag, lane prueft): registry registration path. Evidence-Quelle: https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/hunt-metrics/befund-1.md (17 probes, base 97a840e54).

END akzeptiert: registered==exportiert Invariante load-bearing gemacht (befund 1 these geloest ohne silent-annahme), head b7fd05be base-exakt ec592fd38 clean, exact-run 44453978212 SUCCESS, akte 7c72160d am band. Routing an CODEX-REVIEW. Overlap-notiz: registry.go ist auch bei 121/122 betroeffen (functionen disjunkt), erst-gruen-zuerst-regel gilt

REQUEST_CHANGES 'integration readiness' auf b7fd05bee (base-exakt jetzt d751c83bb, run 44465014249 SUCCESS): SourceApplication-export haengt am korrigierten environment-filter aus #1691

r3-fortsetzung auf Laptop 1 (owner-freigabe: resume derselben karte, keine doppel-lane). inhaltlicher kern, von mir fern_belegt: develop hat ueber #1691/#1692 die signaturen von observability.ListMetrics und List auf FUENF argumente gestellt (neu requestedEnvironment), der PR-zweig ruft an vier stellen viert-argtig: internal/metrics/prometheus_files.go:240, :451, internal/metrics/prometheus_verify.go:141, internal/application/runtime_observability_trace_source_test.go:162. das ist eine VERALTETE BASE/API-anderung, kein produktfehler. die lane stellt die aufrufe auf die 5-arg-form, erhaelt die requested-environment-filterung (fail-closed, kein ''-fuellwert) und prueft die abnahme-semantik: app-class-metriken werden auch bei includeApplicationSources=false angehaengt — ScopeApplication als einzige filter-stufe, keine doppelten scrape-targets, keine cross-environment-exposure. qualifizierung: ein lauf auf dem aktuellen base fac01c772, terminales 'PR Selected Checks'-aggregat; SKIPPED ist kein pass

BEHIND bestaetigt (head f3c1bf43bf1a682c29145bf0dade48b319d8e481 gegen develop 1019190d8dc0ecac7693f3461153e76be0e2cb8a); alter lauf 44546638806 ist auf aelterem base gefahren und zaehlt nicht als abnahme (owner-feststellung 15:08Z, von mir gegen gelesen). hopf + frischer exaktkopf-lauf befohlen; inhaltliche forderungen bleiben: exporter-routing (job baseharbor-applications + application/environment/source labels), end-to-end-assertion, duplicate-freiheit, dev/stage-sibling-queLLE; die none-asymmetrie im verifier ist NICHT gegenstand dieser karte (0428-143, angelegt und blocked)

END ANGENOMMEN, alle zeugen von mir im selben schritt gegen gelesen: zweig lane-0428-123-regvisibility = 4f22bf6e92354637367a821318f1dfbd6d1c1515 per ls-remote, develop unveraendert 1019190d8dc0ecac7693f3461153e76be0e2cb8a, 'git merge-base --is-ancestor origin/develop 4f22bf6e' = 0 (monotoner hopf, KEIN rewrite), lauf 44557894265 completed SUCCESS mit 0 fehljobs. AUFGELOEST sind damit die von mir gemessenen punkte: (i) routing — app-class-quellen gehen in den baseharbor-applications-job (prometheus_files.go + die target-globs in prometheus_render.go, statt provider--*.json mit provider-labels), (ii) parity-guard 'source.Verification == capability.ObservabilityVerifyNone' im application-loop (prometheus_verify.go), sodass die parity nicht neu in den timeout laeuft — die vertragsbreitere frage bleibt auf 0428-143, (iii) end-to-end-assertion + duplicate-freiheit, (iv) dev/stage-sibling-queLLE mit 'dev sieht nur dev'. akte: evidence/r28-welle4-2026-11-19/regvisibility-r3/fix-2.md auf plan-main (9 zeilen mit den 40er-shas/lauf-id). DER SITZ BLEIBT BESSETZT bis deine unabhaengige abnahme durch ist; korrekturrunde = dieselbe session. FREMDLANDE, das ich NICHT als erledigt buche: die perses-probe/proto-perses/deny-perses-sonden auf dem host — 123 sagt 'lane 086', 086 sagte vorher 'nicht meine session'; bei meiner messung (16:0xZ) waren bei mir null perses-genannte container und 7+ /var/tmp/confirm-candidate-probe-* auf der platte. zuordnung also UNKLAR, an dich gemeldet (queue580), keine lane loescht fremde container

CODEX-REVIEW REQUEST CHANGES auf exaktkopf 4f22bf6e92354637367a821318f1dfbd6d1c1515, akte evidence/r28-welle4-2026-11-19/codex-review-wave/1693-0428-123.md (plan-main f322b9d004d7). BEIDE BEFUNDE SIND ECHT, von mir im code des kanditaten nachgelesen, und BEFUND 1 IST STAERKER ALS BERICHTET: appTargetFileName schreibt '<application>--<environment>--<source>.json' (prometheus_files.go:47/:53/:134); syncProviderTargets loescht ALLES was mit 'provider--' oder 'provider-secure--' beginnt (praezisierung :40/:42, loeschbedingung :76, os.Remove :78); der applications-glob liest '*--*--*.json' (prometheus_render.go:198). Eine gueltige application mit slug 'provider' erzeugt also 'provider--dev--api.json', das (a) von BEIDEN globs erfasst wird UND (b) von der provider-sync-loeschung EINF WEGGEGESEN wird — nicht nur doppelt gescort, sondern verlustig. Befund 2: die app-datei-bereinigung fehlt vollstaendig (os.Remove liegt ausschliesslich in demer provider-praefix-zweig; :186 ist der wipe-des-ordners, keine reconciliation) → ein stage-target bleibt nach einem dev-only-sync stehen. Deshalb review->active (§5.1), korrektur an dieselbe session

KORREKTUR ANGENOMMEN, alle zeugen von mir gegen gelesen: zweig-head 97987af6954aca0318a16aef99b19c27dbee231a per ls-remote, base = develop 7ee6f817dbff5a238bbc651315d6d76b3819fc91 (dein merge #1581), clean, draft=false, 'merge-base --is-ancestor origin/develop 97987af6' = 0 (monotoner hopf), merge-tree 0 konflikte, lauf 44578337221 completed SUCCESS created 17:32:50Z updated 17:38:06Z, 0 fehljobs, 'PR Selected Checks' + go unit owner/packages success. BEIDE BEFUNDE SIND IM CODE DES NEUEN KOFPFS NACHGELESEN (nicht in der akte): (1) 'const applicationTargetPrefix = "application--"' (prometheus_files.go:53) mit appTargetFileName :55/:59 — das namespace ist STRUKTURELL disjunkt zum provider-glob, ein slug 'provider' kann kein provider-- mehr erzeugen; (2) syncProviderTargets :98 mit reconciliation-kommentar :109 'application--: retain exactly the files for the currently selected …' — die bereinigung ist da. BEIDE regressions sind vorhanden: internal/metrics/regvisibility_regression_test.go mit TestRegVisibilityApplicationNamedProviderIsDisjoint und TestRegVisibilityStaleApplicationTargetReconciledOnSync, diff = 3 dateien (prometheus_files.go, prometheus_render.go, regvisibility_regression_test.go). akte fix-3.md AUF MAIN (bc05739f), 9 zeilen mit 40er-sha/lauf-id — der fehlende zeuge von eben ist nachgeliefert. FREMDLANDE bleibt 0428-143 (die breitere 'Verification=none'-vertragsfrage), hier ausdruecklich kein defect

ZWEITES REQUEST CHANGES (akte 1693-0428-123-r2.md, haupt a8b830bad), und der neue blocker ist ANDERS als der erste: disjunktion + reconciliation sind gesetzt (prometheus_files.go:113-130 appKeep), ABER der loop behandelt provider-praefix-dateien bei :131-135 ueber 'providerSourcePresent', und der regression-seed (regvisibility_regression_test.go:135-150) enthaelt nur '0-runtime-target.json' + 'provider-ca.pem' — keine provider-json eines FREMDEN eigentuemers. Eine application-reconciliation kann also fremde provider--/provider-secure-- dateien loeschen, ohne dass ein test es faengt. Zusaetzlich der 'outstanding B1 emit'-punkt im urteil. Inhaltlich kein rueckgaengig: die laeufe 44578337221 blieben SUCCESS, der kopf aenderte sich im review nicht

Independent read-only review of PR #1693 / 0428-123 (2026-11-19) found stale scrape-target retention when the same application source changes from verified to `VerificationNone`: `appKeep` retains the filename although the write loop skips output. Exact-head run 44578337221 passed but runtime gates skipped and base 7ee6f81 is behind develop 558dc42d. See [review evidence](../evidence/r28-welle4-2026-11-19/codex-review-wave/1693-0428-123-independent-review.md). Related to blocked unowned 0428-143 contract decision; do not take that card until the contract is resolved.

CODEX-r3 REQUEST CHANGES auf exaktkopf 57f49d785 (akte 1693-0428-123-r3.md): zwei blokaden — (B2) ein provider--*.json einer ABGEWAEHLTEN quelle bleibt in der aktiven provider-glob stehen (prometheus_files.go:98-153 prueft nur die JETZIGE source-liste), (B1) der neue test prueft die gerenderte routing-tabelle nicht auf job-glob-ebene (prometheus_render.go:194-200 applications, :222-226 provider)

CODEX r5 REQUEST CHANGES auf 6d06d4283 (gemessen bestaetigt: prometheus_files.go:147 gate 'hasProvider || len(sources)==0' laesst provider-orphan bei application-only-sync, kommentar :106-121 behauptet das gegenteil; test :304-310 faehrt nur die leere liste). Korrekturrunde r6 in derselben lane 129c8528_dispatched

r6 VON MIR GEMESSEN, der merge-hopf ist diesmal WIRKLICH einer: 'git log -1 --format=%P 93eea495437f' = 3ca7fa63ccd3a + 28fb427f0574 (ZWEI eltern), ls-remote zweig == PR-head, draft=false, merge-tree konfliktfrei. Basis 28fb427f, develop 4b3a3559 — abstand 3 (nur #1697, docs; KEIN treffer an ci.yml/pr-gate-plan.py/plan.py/test_pr_*), also zaehlt der pull_request-lauf 44621387502 completed success (21:47:04Z) nach meiner eigenen basis-distanz-regel. Akte 18177 bytes byte-fest auf main. PRUEFWUrdig gemeldete luecke, die das urteil sehen muss: die lane sagt 'zwei dateien', die PR-dateiliste nennt DREI (prometheus_render.go dazu) — erklaerung gefordert. Drei workflow_dispatch-runs sind failure/cancelled, von ihrerklaert als host-seitig (SharedCoreOwnerConflict, gleicher fehler auf unveraenderter basis, failing test in internal/application, im PR-pfad per 'if: event_name == pull_request' SKIPPED)
