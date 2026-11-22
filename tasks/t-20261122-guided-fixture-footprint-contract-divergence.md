---
id: t-20261122-guided-fixture-footprint-contract-divergence
card_number: "0428-241"
card_short_title: "guided fixture drift"
type: bug
areas: [testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: b90e4ba1 (#1783 round-3: selected demo candidate-submission consent hang) / 237(native :edge) / Owner
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-241 · guided fixture drift
priority: high
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: [mcpdev80/baseharbor#1753, mcpdev80/baseharbor#1770, mcpdev80/baseharbor#1773, mcpdev80/baseharbor#1763, mcpdev80/baseharbor#1780, mcpdev80/baseharbor#1783]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-guided-fixture-footprint-contract-divergence · Selected data-capabilities: native CLI JSON/MCP footprint contracts differ from demo tests/guided/new_edit.py:63 #task #release/v0-4-28 #status/active #view/active #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** b90e4ba1 (\#1783 round-3: selected demo candidate-submission consent hang) / 237(native :edge) / Owner · **Priority:** high  
    **PR:** [baseharbor#1753](https://github.com/mcpdev80/baseharbor/pull/1753), [baseharbor#1770](https://github.com/mcpdev80/baseharbor/pull/1770), [baseharbor#1773](https://github.com/mcpdev80/baseharbor/pull/1773), [baseharbor#1763](https://github.com/mcpdev80/baseharbor/pull/1763), [baseharbor#1780](https://github.com/mcpdev80/baseharbor/pull/1780), [baseharbor#1783](https://github.com/mcpdev80/baseharbor/pull/1783)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** b90e4ba1 (#1783 round-3: selected demo candidate-submission consent hang) / 237(native :edge) / Owner  
**Priority:** high  
**PRs:** [baseharbor#1753](https://github.com/mcpdev80/baseharbor/pull/1753), [baseharbor#1770](https://github.com/mcpdev80/baseharbor/pull/1770), [baseharbor#1773](https://github.com/mcpdev80/baseharbor/pull/1773), [baseharbor#1763](https://github.com/mcpdev80/baseharbor/pull/1763), [baseharbor#1780](https://github.com/mcpdev80/baseharbor/pull/1780), [baseharbor#1783](https://github.com/mcpdev80/baseharbor/pull/1783)  
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
