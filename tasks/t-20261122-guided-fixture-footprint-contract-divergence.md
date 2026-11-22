---
id: t-20261122-guided-fixture-footprint-contract-divergence
card_number: "0428-241"
card_short_title: "guided fixture drift"
type: bug
areas: [testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: b90e4ba1 (#1783 STACKED auf #1770: head 62f4ab0d = merge #1770-tip 0da4a571 + fixture, base=codex/0428-237-exact-native-runtime, PR CLEAN; combined run 45068985009 pending) / Owner (wait green -> merge) / Coordinator
kanban_status: review
kanban_lane: review
kanban_summary: ""
kanban_title: 0428-241 · guided fixture drift
priority: high
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: [mcpdev80/baseharbor#1753, mcpdev80/baseharbor#1770, mcpdev80/baseharbor#1773, mcpdev80/baseharbor#1763, mcpdev80/baseharbor#1780, mcpdev80/baseharbor#1783, mcpdev80/baseharbor#1771, mcpdev80/baseharbor#1787, mcpdev80/baseharbor#1788]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-guided-fixture-footprint-contract-divergence · Selected data-capabilities: native CLI JSON/MCP footprint contracts differ from demo tests/guided/new_edit.py:63 #task #release/v0-4-28 #status/review #view/review #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** b90e4ba1 (\#1783 STACKED auf \#1770: head 62f4ab0d = merge \#1770-tip 0da4a571 + fixture, base=codex/0428-237-exact-native-runtime, PR CLEAN; combined run 45068985009 pending) / Owner (wait green -\> merge) / Coordinator · **Priority:** high  
    **PR:** [baseharbor#1753](https://github.com/mcpdev80/baseharbor/pull/1753), [baseharbor#1770](https://github.com/mcpdev80/baseharbor/pull/1770), [baseharbor#1773](https://github.com/mcpdev80/baseharbor/pull/1773), [baseharbor#1763](https://github.com/mcpdev80/baseharbor/pull/1763), [baseharbor#1780](https://github.com/mcpdev80/baseharbor/pull/1780), [baseharbor#1783](https://github.com/mcpdev80/baseharbor/pull/1783), [baseharbor#1771](https://github.com/mcpdev80/baseharbor/pull/1771), [baseharbor#1787](https://github.com/mcpdev80/baseharbor/pull/1787), [baseharbor#1788](https://github.com/mcpdev80/baseharbor/pull/1788)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** b90e4ba1 (#1783 STACKED auf #1770: head 62f4ab0d = merge #1770-tip 0da4a571 + fixture, base=codex/0428-237-exact-native-runtime, PR CLEAN; combined run 45068985009 pending) / Owner (wait green -> merge) / Coordinator  
**Priority:** high  
**PRs:** [baseharbor#1753](https://github.com/mcpdev80/baseharbor/pull/1753), [baseharbor#1770](https://github.com/mcpdev80/baseharbor/pull/1770), [baseharbor#1773](https://github.com/mcpdev80/baseharbor/pull/1773), [baseharbor#1763](https://github.com/mcpdev80/baseharbor/pull/1763), [baseharbor#1780](https://github.com/mcpdev80/baseharbor/pull/1780), [baseharbor#1783](https://github.com/mcpdev80/baseharbor/pull/1783), [baseharbor#1771](https://github.com/mcpdev80/baseharbor/pull/1771), [baseharbor#1787](https://github.com/mcpdev80/baseharbor/pull/1787), [baseharbor#1788](https://github.com/mcpdev80/baseharbor/pull/1788)  
**Source:** 
<!-- /generated:links -->

## Found by the exact-head CI of PR 1753 (card 0428-227), 2026-11-22

Measured in the selected Docker data-capabilities job 137165839346 of run 45008538769 (terminal FAILURE, head b86440c389b
on develop 8629450ef3c): `app footprint show -o json` IS admitted (the ci-operator log shows the admitted command), yet the
gate still fails with eight `--confirm-candidate` refusals and a contract note that the actual native CLI JSON/MCP footprint
output differs from `tests/guided/new_edit.py:63` in the demo repository.

## Acceptance

1. One canonical footprint contract: the guided demo fixture and the native CLI JSON/MCP output agree on the same fields, or
   the fixture asserts the native output through the shared contract helper (no duplicated expectations).
2. The selected data-capabilities gate for this path runs green with the consent digest supplied by the test harness, and
   the refusal text is proven to be harness behavior, not product behavior.
3. If the fix must touch `cmd/baha/**` product code, that belongs to card 0428-227; this card covers the fixture/contract
   side only.

## Boundaries

baseharbor-demo `tests/guided/new_edit.py` plus the footprint contract assertions in baseharbor `cmd/baha/app_footprint*`
test files. Reserved paths (`.github/**`, `scripts/**`) are excluded.

SITZ BESETZT (03c7350a). Die selected-seite der #1753-rotung hat jetzt eine EIGENE lane: der fixture-/contract-vergleich zwischen 'app footprint show -o json' und baseharbor-demo tests/guided/new_edit.py:63 (job 137165839346: confirm-candidate=8, not_ready=0, unhealthy=0 = reine consent-/fixture-ursache). Auftrag an 03c7350a: abweichung Feld fuer Feld benennen, fix auf der FIXTURE-seite (geteilter contract-helper statt doppelter erwartungen); falls cmd/baha/** produktcode noetig, an 0428-227 rueckmelden statt selbst zu aendern.

SITZ-VORBEHALT, KEIN DOPDEL-VERSAND: dieser auftrag wurde ZWEI mal an 03c7350a zugestellt (rc 0, 'sent'), aber die session liefert nicht (bleibt idle ohne todos) - es ist der dokumentierte NULL-LIEFER-SITZ, dessen rotation an einen owner-directive-wert des eigentuemers gebunden ist, den ich nicht habe. Ich stelle NICHT nochmal ins Leere zu. Die abweichung bleibt gut belegt (selected docker 137165839346: confirm-candidate=8, not_ready=0, unhealthy=0 vs new_edit.py:63) und wartet auf den ERSTEN echt freien arbeitssitz (frei werdend aus den read-only hunts von f0f6c8b4/ffe7611b oder nach #1753-fix auf 0847d100). Kein inhaltlicher blockierer, nur ein kaputter sitz.

SITZ FUNKTIONIERT: 03c7350a lieferte zuvor 0428-225/#1751, die 'null-liefer'-einstufung war falsch. Auftrag gestellt: abweichung 'app footprint show -o json' vs tests/guided/new_edit.py:63 Feld fuer Feld (job 137165839346: confirm-candidate=8 + contract-mismatch=4), fix auf fixture-/contract-seite; produktpfad cmd/baha/** nur an 0428-227 rueckmelden.

UMGEZOGEN von 03c7350a (flaky) auf den funktionierenden sitz f0f6c8b4. Auftrag gestellt (round-3). Ziel: die selected-contract-abweichung 'app footprint show -o json' vs tests/guided/new_edit.py:63 auf der fixture-/contract-seite beenden (job 137165839346: confirm-candidate=8 + contract-mismatch=4).

#1770 native data-caps docker+podman BEIDE SUCCESS (develop 713aadd). Der einzige #1770-blocker ist jetzt selected footprint-show -o json + record-deployment confirm-candidate digest = GENAU diese karte. f0f6c8b4 entblockt damit #1770 + #1753. Option A test-only digest-

FEHL-SCOPE KORRIGIERT: frueher 'runner-bootstrap gate issue END_BLOCKED' war falsch. EXAKTE route (datei:zeile): selected capability lifecycle ruft footprint show/record-deployment ohne --confirm-candidate digest -> deployment_record.go:365-374 fail-closed -> interactive auth. Harness MUSTER existiert: app_candidate_consent_test.go:171-176 withCandidateConsentDigest + coreBootstrapFixtureConsent (app_capability_runtime_test.go:133/190/224/282/332). Test-only fix in app_capability_runtime_test.go selected lifecycle = liefert digest. Entblockt #1770 + #1753 + #1773 selected. f0f6c8b4 re-dispatched.

#1773 exact run 45036009904 selected docker+podman bestaetigen DENSSELBEN defect: 'record deployment before mutation requires --confirm-candidate' = diese karte. 241 digest-consent harness (app_capability_runtime_test.go selected lifecycle, muster app_candidate_consent_test.go:171-176) heilt selected fuer #1770 + #1753 + #1773. native podman 503 separat = 237 (andere session).

241 GELIEFERT (f0f6c8b4): test TestApplicationCapabilityLifecycleFootprintShowDigestConsent + scripts/ci-native-pr-gate.sh:83-84 wired (codeman scope). branch lane-0428-241-footprint-consent-harness head 68b26bd -> PR wird geoeffnet + additiv auf 3939aa5 gehoppt. unit gruen, vet clean. Bei gruen: entblockt selected fuer #1763 #1770 #1771 #1773 #1753. ffe7611b hat 241 korrekt abgegeben (#1723 hop laeuft).

#1780 (241, branch lane-0428-241-footprint-consent head 78171ae9) run 45041991956 CANCELLED: ci-executor-tests 137268311074 failt 2 partition-tests weil FootprintShowDigestConsent in scripts/pre-release-integration.py NICHT registriert. ffe7611b fuegt die registration hinzu + rerun. Nicht merge-ready bis gruen. EIN 241-pr (#1780), f0f6c8b4s -harness-delivery NICHT als zweiter PR. Bei gruen: entblockt selected #1763/#1770/#1771/#1773/#1753. develop 6930872c.

#1780 head c95c2377 run 45042733884 aktiv, base stale 3939aa5. Nach terminal: ffe7611b hoppt additiv auf 6930872c + exact CI NEU, DANN erst merge-ready (current-base proof). Registration-Fix (pre-release-integration.py) muss im neuen run die 2 partition-tests gruen bringen. Bei gruen: selected entblockt #1763/#1770/#1771/#1773/#1753. develop 6930872c.

#1780 run 45042733884: registration-Fix OK (beide selected cells docker 137271327474 + podman 137271327467 identisch), NEUER rest=test-only CI-operator fixture (ci_integration_operator_enabled.go:115-140) laesst read 'app footprint show -o json' nicht durch managed-workload set (ciIntegrationGuidedFootprintShow :232-233 arg-form passt nicht fuer selected-pfad). BESCHLUSS OPTION A: read-only footprint-show in der TEST-ONLY fixture allowlist zulassen, record-deployment(write) braucht weiter digest (241-harness). Produkt fail-closed unveraendert (kein 247/owner). Danach hop 6930872 + rerun. native/coreless jobs noch aktiv, kein merge.

#1780 hat DREI unabhaengige fehlerklassen: (1) selected consent digest=GEFIXT (2) selected test-only allowlist footprint-show=Option A (ffe7611b, ci_integration_operator_enabled.go:115-140) (3) native Docker broker EDGE unhealthy ~2m = 0428-237 image-resolution (ANDERE session/#1770, NICHT 241). #1780 ist NICHT merge-ready bis alle drei geloest. Class-3 ist ausserhalb des 241-write-sets.

#1780 VIERTE, praezise klasse (owner read-only): neue footprint-digest-consent test @ app_capability_runtime_test.go:376 failt podman selected core-capability (137270924827) 'docker.sock rootful vs rootless' weil der BASEHARBOR_TEST_RUNTIME==podman provider-override (muster :32-39 aus ExistingCore) fehlt. FIX-1=override spiegeln/configureIsolatedEmptyRuntimeTarget. FIX-2=Option A footprint-show read allowlist (ci_integration_operator_enabled.go). Beide test-only. Dann hop b27b2ebe + rerun. native docker edge-broker = 237 separat. #1770 = SELBE policy-luecke (andere session) -> nach #1780 fix + hop b27b2ebe.

#1780 run 45042733884 terminally RED (11 jobs): (a) selected read-only footprint fixture = SHARED, wird als eigener optionA-PR von b90e gelandet (nicht in #1780 vergraben), (b) selected podman coreless provider mismatch @:376 = ffe7611b own fix (BASEHARBOR_TEST_RUNTIME podman override), (c) native docker edge-broker unhealthy = 0428-237 andere session. ffe7611b NICHT re-hopen bis (a) gemerged + (c) geloest; nur (b) vorbereiten. Kein stale-green merge.

INFRA-BLOCK: run 45044744796 pending zero-jobs weil self-hosted runner OFFLINE (service inactive) + root 99% voll. Code-fix (provider override :376 + optionA shared) LOBAL weiter, push/rerun erst nach runner-back. Kein stale-green merge moeglich (CI down).

SHARED UNLOCK = PR #1783 (branch lane-0428-241-optionA-operator-allowlist head 8f84fcbb, nur ci_integration_operator_enabled.go+test, non-draft) bringt selected footprint-show policy-freiheit fuer #1780/#1770/#1738. ABER statusCheckRollup LEER + BLOCKED = hosted CI lief am exact head nie an -> b90e triggert per close/reopen (head bleibt). #1780 vorgerueckt auf ef6de850 (run 45045737874 pending, stale 45044680383 cancelt noch). #1738 e09ceb9a: cli-2(137277583015)+native docker(137277586142) FAILED, logs erst am terminal, native podman+selected laufen. Kein merge vor exact run+current base.

#1783 (optionA shared fixture, head 8f84fcbb) hosted CHECKS = 67, 0 FAIL, 4 PENDING. Die 4 pending SIND die self-hosted native data-caps/selected-runtime zellen = runner-blocked (service inactive, root 2.4G). GitHub-hosted teil IST gruen. #1783 ist der SHARED unlock fuer selected footprint-show von #1780/#1770/#1773/#1738(A) -> merge-reif sobald die 4 native zellen dispatchen (runner-back) ODER als N/A fuer ein test-only tagged file bestaetigt. #1780 run 45045737874 noch queued (concurrency hinter stale 45044680383). develop b27b2ebe.

#1783 exact run 45045885547 SELECTED data-caps FAILED (docker 137280787736/podman 137280787743), native laeuft. (1) optionA block matcht FALSCHEN gate: gate=BASEHARBOR_DEMO_OPERATOR_GATE (:100) vs GATE guard (:102); der neue 'data-capabilities'==gate block feuert nie (zelle nutzt anderen string, vermutlich 'guided'). FIX: echten gate-string aus trace (:106) lesen + read-only footprint-show unter DEM admit, ODER ciIntegrationGuidedFootprintShow (:135) um '-o json' canonical argv erweitern (read-only, write bleibt digest). (2) footprint_parity 'CLI JSON vs MCP contracts differ' RuntimeError = PRODUKT-defect (mcp.go:248 vs presenter) -> #1773/0428-246 traegt ihn, NICHT fixture. #1780/#1770/#1773/#1738A erben erst den GEKOPIGTEN #1783. develop b27b2ebe.

KORRIGIERT (owner exact test-source-read): das 'missing --confirm-candidate' = BEABSICHTIGTER negative-control (footprint-show digest consent test), KEIN fixture-fehler. #1783 diff ist korrekt. #1783 run 45045885547 terminal rot wegen 2 SHARED PRODUKT-blockern AUSSERHALB des PRs: (X) new_edit.py:63 footprint_parity native CLI JSON != MCP JSON (selected docker+podman; product mcp.go:248 vs app_footprint_presenter) und (Y) runtime:edge broker unhealthy (native docker 137280389091/podman 137280389052) = 0428-237 ghcr edge image. Beide blocken auch #1780/#1770/#1773/#1738. #1783 haelt OPEN, alle zellen bis terminal, kein push der head aendert, kein merge bis X/Y geloest. develop b27b2ebe.

#1780 ffe END_BLOCKED: NATIVE set -e bricht bei ExistingCore broker :91 (=0428-237, ausserhalb write-set) -> harness laeuft dort nie, HALTEN. SELECTED core-cap fails SIND feins write-set app_capability_runtime_test.go: :376 (podman provider override fehlt), :430 (digest nur aus err.Error(), hash im captured 'out'), :409 (cleanup nach fail). ffe fixt die 3 + hop b27b2ebe + rerun. #1783 (b90e) erweitert MCP-serve+restricted-toolset auf selected gates (parity). develop b27b2ebe.

#1783 selected parity fix (MCP-serve admission+restricted-toolset auf data-caps/core-caps, one-tool baseharbor.app.footprint.show) geloest selected footprint cells fuer #1780/#1770/#1773/#1738. ABER #1783 EIGENE native cells :edge-red (pre-existing, braucht #1770 pin) -> #1783 kann native NICHT selbst gruen zeigen. MERGE-ORDER: NACH #1770 (pin in develop -> #1783 native gruen + selected gruen). b90e haelt #1783 ready, kein merge bis #1770 + own selected gruen.

CRITICAL PATH: #1783 head haengt noch 8f84fcbb (run 45045885547 old fails: native :edge 137280389091/052 + selected docker 137280787736). b90e round-2 MCP-serve admission+restricted-toolset fix noch NICHT pushed -> gekitzelt, neuen head+run melden. native :edge red bis #1770 pin in develop. select data-caps werden mit fix gruen.

#1783 round-2 2da7f565 TERMINAL rot (run 45051057741), NEUE selected signatur: NICHT mehr parity -> Demo new-edit-new-sql haengt (106-107s no-output) 'candidate submission requires --confirm-candidate'. footprint-READ admitted aber 0428-241 sequence unter data-caps NICHT zu Ende enabled (candidate-SUBMISSION write consent haengt). round-3 = tagged fixture selected-gate candidate-submission consent (synthetischer test-only stamp ODER test reicht --confirm-candidate digest durch; STOP-Fall=247 product write-auth). native docker 137296082318/podman 137296082310 = pre-existing :edge 503 (0428-237/#1770, NICHT 1783 code). KEIN merge bis selected sequence terminiert+gruen. develop b27b2ebe.

#1783 round-2 2da7f565 = PARITY FIX GELUNGEN (selected docker 137296517250/podman 137296517242: contracts differ=0, MCP-serve admitted data-caps/core-caps, one-tool baseharbor.app.footprint.show only, other MCP tools DENIED ListTools=1; product unangetastet). ABER selected NICHT gruen: NEUER blocker ANDERE klasse = demo new-edit-new-sql (drive.py:415) no-output timeout an record-deployment WRITE-consent ('requires --confirm-candidate'). Das ist KEIN 247/produkt-thema (consent mechanismus intakt, baseharbor refuses korrekt) SONDERN test-wiring in baseharbor-DEMO (flag-setzer dort, anderes repo). b90e HOLD (kein baseharbor-demo/product edit, #1783 READY, kein merge). BENOETIGT: OWNER autorisation einer baseharbor-demo lane (demo reicht captured confirm-DIGEST + --confirm-candidate durch) + #1770 native pin. native docker 137296082318/podman 137296082310 = :edge 503 = 237. develop b27b2ebe.

#1780 ffe own fixes LANDED head 87ba9bac (run 45051176104): aber run = completed FAILURE selected data-caps (docker+podman runtime + coreless) weil shared #1783 (demo-consent parity noch nicht geloest) + native #1770 pin NICHT in develop (develop=b27b2ebe). :376/:430/:409 selbst fixed. #1780 = downstream von #1783(demo-consent owner auth)+#1770(pin), NICHT merge-ready, kein defect von ffe mehr. develop b27b2ebe.

#1783 selected REAL root (owner exact-log @demo pin 98e4d549): NICHT candidate-consent (apply --confirm-candidate digest-pfad existiert schon, gruen 17:47). Echter Timeout 17:50: new_application(create-only) -> app newfordert interaktive DEV operator auth ('Configure now?'), weil app new im tagged fixture nur gate==guided admitted ist (ci_integration_operator_enabled.go :129 ciIntegrationGuidedAppNew), NICHT unter data-caps/core-caps. FIX = analog footprint-show: app-new/create-only operator admission auf {data-capabilities, core-capability} gates, candidate consent unveraendert, product fail-closed intact. KEIN baseharbor-demo edit, KEIN 247. (A)-owner-blocker FAELLT WEG. b90e routed, neuer head noetig (nicht 2da7f565). native=#1770. develop 1253e8d0a.

ENTSCHEID shared (owner+coordinator): #1783 selected timeout = getagtes TEST-FIXTURE muss app new/create-only operator stempeln unter data-caps/core-caps (analog footprint-show :129 nur-guided). NICHT baseharbor-demo digest-edit (no-op, apply --confirm-captured-digest bereits gruen), NICHT Core/produkt-boundary (fail-closed intact), NICHT 247. Fix im bestehenden #1783 write-set (b90e), KEIN neuer owner. STOP-Fall nur falls echte product session-binding. neuer head noetig (nicht 2da7f565) + exact hosted. native=#1770. develop 1253e8d0a.

#1783 NARROW fix (owner-diagnose, scope berichtigt): ciIntegrationGuidedAppNew admitted nur gate==guided (:129); data-capabilities `app new` create-only faellt durch -> interaktive OIDC -> PTY timeout. FIX = getagtes test-fixture app-new admission auf gate==data-capabilities, exakt kanonische args + Regression (noncanonical + ANDERE gates DENIED/unchanged), kein blanket-allow. Produkt --confirm-candidate boundary UNVERAENDERT; Demo digest NICHT angefasst (existiert, gruen). Footprint-show :135 nur falls rerun-log selected consent-fail zeigt. b90e laeuft, neuer head (nicht 2da7f565). develop 978a0f90b. native=#1770.

#1783 HARNESS FIX gelandet (head 8b99bdc3): ciIntegrationGuidedAppNew admitted fuer gate==data-capabilities (:138, exakt kanonische args) + 135 test lines; Produkt --confirm-candidate boundary UNVERAENDERT. Trusted Plan PASS, selected docker/podman + exact candidate + CLI guided laufen (run 45061359667). Owner redundantes stacked #1787 VOR CI geschlossen (nicht merged) -> b90e = einziger fixture-writer. Regression (noncanonical + andere gates DENIED) bestaetigt am branch. native data-caps = waiting-#1770. develop 978a0f90b. KEIN merge bis reviewed + selected gruen.

#1783 app-new fixture fix ERWIESEN (head 8b99bdc3): run 45061359667 `Validation  ci-integration-operator-seam-tests` = SUCCESS = QUALIFYING EVIDENCE (data-capabilities app-new admitted unter selected gates, Produkt consent intact). SPAETER `native/docker/data-capabilities` FAIL = TestApplicationCapabilityLifecycleExistingCore/secrets broker >2m auf ghcr.io/...:edge = EXAKT der :edge drift, SCHARF geroutet zu #1770 (exact-runtime-image pin; #1770 eigener branch macht native docker+podman GREEN 45060014055). KEIN #1783 defect/chasing am runtime (waere consent/boundary risk). native/podman + selected = waiting-#1770. Merge-Ordnung: #1770->develop ZUERST, dann #1783 re-hop zeigt native gruen. develop 978a0f90b. KEIN merge bis reviewed.

#1783 app-new admission WIRKT (:138 data-capabilities, run 45061359667 seam-tests SUCCESS). NAechster uncovered seam (owner): `app edit` faellt durch -> Trace 'command-not-in-managed-workload-set: app edit' -> new-edit-new-sql-cancel no-output timeout. FIX analog app-new: EINE admission-zeile `gate=="data-capabilities" && ciIntegrationGuidedAppEdit(args)` (canonical len==2 app edit) + Regression (noncanonical/andere gates DENIED, kein blanket), PRODUKT managed-workload boundary UNVERAENDERT. b90e routed, neuer head (nicht 8b99bdc3) + exact selected rerun. native :edge = waiting-#1770. develop 978a0f90b.

#1783 TERMINAL run 45061359667: SELECTED data-caps (docker+podman) app-new admitted + digest-bound app apply + lifecycle = GRUEN (Qualifying-Evidence erbracht). #1783 content KOMPLETT fuer app-new (head bleibt 8b99bdc3). NAechster gate gap = exact `app edit` -> no-output timeout (new-edit-new-sql-cancel): wird vom OWNER als gestapelter test-only fixture follow-up PR behoben (NICHT b90e, um #1787-artige Doppel-writer-kollision zu vermeiden). native docker+podman = pre-existing existing-core/secrets :edge broker readiness = SEPARAT #1770 (pin, nachhop 978a0f90b laeuft). b90e steht auf #1771 hop 978a0f90b (dep-frei via #1786). develop 978a0f90b.

#1783 app-new seam TERMINAL selected GRUEN (8b99bdc3, run 45061359667). #1788 = OWNER gestapelter app-edit follow-up (base = #1783 branch lane-0428-241-optionA, head 6c12225e): exact data-gate app edit admission + Regression (docker/podman, noncanonical, other-gates DENIED), Produkt boundary intact. run 45062680796: Trusted Plan + Focused Python + Demo Pin PASS; native docker+podman pending = :edge = #1770 (NICHT #1788 defect) -> app-edit content nachweislich ok. SUPERSEDE: #1787 closed weil app-new concurrent in #1783 landete. SEQUENZ: #1788 CI terminal -> MERGE #1788 in PARENT #1783 (owner/Codex) -> FRISCHER #1783 exact selected run auf combined head (b90e) -> #1783 merge-ready develop. b90e #1771 hop laeuft. develop 978a0f90b. KEIN zweiter writer am fixture.

#1788 app-edit fixture remote besttigt: run 45062680796 SELECTED docker+podman data-caps PASS (Docker 20m21s/Podman 25m11s) = Qualifying-Evidenz (app-new + app-edit admitted unter data-caps, consent intact). native docker fail/podman pending = :edge broker readiness deadline = SHARED #1770 (NICHT #1788 defect). #1783 8b99bdc3 selected noch fail (app-edit fehlt, lebt in #1788). GUIDANCE: (1) merge #1788 in parent #1783 jetzt (selected-green qualifying, native-red=#1770 kein blocker); (2) #1770 -> develop ZUERST (native-green qualifying) = Hebel der native fuer 1783/1761/1762/1763/1771 gruen macht; (3) dann b90e FRISCHER #1783 rerun auf develop+1770 -> vollstaendig gruen -> #1783 merge. develop 978a0f90b.

#1788 final (owner failed-only rerun): SELECTED docker+podman data-caps PASS + focused seam + all static PASS = app-edit fixture QUALIFIZIERT gruen. native docker+podman FAIL = ExistingCore/secrets broker /health HTTP 503 not_ready FailingStreak 49 / Docker readiness context-deadline = DER geteilte :edge runtime-broker drift = AUSSCHLIESSLICH #1770 (exact-image pin), NICHT #1788/#1783 fixture. CODEX-MERGE dispatcht (fecbada9): #1788 -> base branch lane-0428-241-optionA (=#1783 head) gestapelt gemergt, KEIN develop-touch, STOP-fall falls required-native-check blockiert. Danach #1783 = app-new + app-edit selected vollstaendig gruen; native bleibt 503 bis #1770 in develop. develop 978a0f90b.

#1788 GEMERGT in parent #1783 branch (head 66838807, owner-executed, stacked konsolidierung; fecbada9 CODEX-MERGE hielt korrekt an statt native-503 zu umgehen). #1783 = app-new + app-edit fixture vollstaendig; CI auf 66838807 laeuft (BEHIND develop c928a627 durch #1597). Nach #1770 merge -> #1783 re-hop auf develop+1770 -> native green (pin) + selected green (fixture) = vollstaendig gruen -> #1783 merge develop. native-503 = #1770 shared, NICHT 1783. develop c928a627.

OWNER-SEQUENZ APPROVIERT (policy-konform, 3.3(8) stack retarget): #1783 enthlt ALLE drei selected admissions (app-new :137, app-edit :140, footprint-show :151 data-caps||core-caps) -> heilt genau den footprint-show 'command-not-in-managed-workload-set' fail der #1770 auf develop. Schritt 1 (b90e jetzt): #1783 branch additiv mit #1770-tip (disjunkt: fixture vs scripts pin) + PR base develop->#1770 branch. Schritt 2: exact hosted MUSS native green (pin) + selected green (fixture) + TP green (#1786). Schritt 3: CODEX-MERGE #1783 -> #1770 branch (feature-branch, protection intakt). Schritt 4: #1770 rerun = vollstaendig gruen -> MERGE -> develop. Schritt 5: fan-out re-hops. develop c928a627.

STACK APPLIED (approved sequence): #1783 base via REST PATCH -> #1770 branch codex/0428-237-exact-native-runtime; head 62f4ab0d = merge-commit von #1770 tip 0da4a571 (pin) + #1783 fixture (app-new :137, app-edit :140, footprint-show :151) -> PR exakt CLEAN mit integriertem pin+fixture. Kombinerter run 45068985009 queued. Erwartung: native docker+podman GREEN (pin), selected docker+podman GREEN (fixture incl footprint-show), TP GREEN (#1786). Wenn alle gruen -> Schritt3 CODEX-MERGE #1783 -> #1770 branch -> #1770 rerun vollstaendig gruen -> #1770 MERGE develop -> fan-out. develop c928a627. Kein force/bypass.
