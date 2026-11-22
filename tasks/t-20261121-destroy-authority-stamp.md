---
id: t-20261121-destroy-authority-stamp
card_number: "0428-214"
card_short_title: "0428-214 destroy stamp"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: f0f6c8b4 (#1738: class-C destroy auth-fixture + re-hop b27b2ebe; class-A erbt #1783; class-B=237)
kanban_status: active
kanban_lane: active
kanban_summary: "TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget shows which authority mode admitted installation.destroy, instead…"
kanban_title: 0428-214 · 0428-214 destroy stamp
priority: high
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1738, mcpdev80/baseharbor#1781, mcpdev80/baseharbor#1783]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1738", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/destroy-authority-stamp/round-5-rebase.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/operator-auth-helper/carrier-census-1737-1738-1740-1741.md"]
---

- [ ] t-20261121-destroy-authority-stamp · installation.destroy authorization assertion runs on a stamped context #task #release/v0-4-28 #status/active #view/active #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** f0f6c8b4 (\#1738: class-C destroy auth-fixture + re-hop b27b2ebe; class-A erbt \#1783; class-B=237) · **Priority:** high  
    **PR:** [baseharbor#1738](https://github.com/mcpdev80/baseharbor/pull/1738), [baseharbor#1781](https://github.com/mcpdev80/baseharbor/pull/1781), [baseharbor#1783](https://github.com/mcpdev80/baseharbor/pull/1783)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1738), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/destroy-authority-stamp/round-5-rebase.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/operator-auth-helper/carrier-census-1737-1738-1740-1741.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** f0f6c8b4 (#1738: class-C destroy auth-fixture + re-hop b27b2ebe; class-A erbt #1783; class-B=237)  
**Priority:** high  
**PRs:** [baseharbor#1738](https://github.com/mcpdev80/baseharbor/pull/1738), [baseharbor#1781](https://github.com/mcpdev80/baseharbor/pull/1781), [baseharbor#1783](https://github.com/mcpdev80/baseharbor/pull/1783)  
**Source:** 
<!-- /generated:links -->

## Goal

`TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget` shows **which authority mode** admitted
`installation.destroy`, instead of printing an authorization green that its own stamp produced.

## Why

H-V23 section 1 (akte `evidence/bug-hunt-2026-11-21/fail-closed-honesty/round-1.md`, Karte A) is the single confirmed
falschlich-authentifiziert case: `cmd/baha/core_installation_runtime_test.go:323` asserts that the fixture cleanup context
is AUTHORIZED for `installation.destroy` in environment `prod`, inside a test whose contract is that cleanup authority is
bound to its local target. The context is stamped at `:298-306`
(`WithEnforcement` -> `WithVerifiedPrincipal` -> `WithMembershipProvider`), and `WithVerifiedPrincipal` implies
`WithEnforcement` (`internal/operatorauth/context.go:54-57`), so `internal/operatorauth/authorization.go:285` is
unreachable by construction. The green demonstrates the fixture, not production authority.

## Scope

Allowed write-set:

- `cmd/baha/core_installation_runtime_test.go`

Forbidden: production code, `internal/operatorauth/**` (Owner rail), every other `cmd/baha/` file — 0428-204 owns those
while it runs, so this card stacks behind it.

## Acceptance criteria

1. Either the authorization is asserted through the boundary the cleanup path really takes
   (`ensureOperatorAuthForBoundary`, `cmd/baha/operator_auth_boundary.go:55`), or the assertion moves to a positive-path
   test and the denial test stays unstamped.
2. The denial subtests (remote AccessProvider, unrelated verified principal) keep passing with the same assertions.
3. The output names the admitting mode (`authenticated` from a session, or `local-runtime` from the grant); an unstamped
   synthetic principal is not acceptable proof.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | Go unit shards for `./cmd/baha/` (PR Selected Checks) |
| Test identifier | `0428-214` |
| Route | `auto-discovery` |

## Dependencies

Needs the seam helper that 0428-204 introduces (content, not a merge wait). Do not commission while 0428-204 writes in
`cmd/baha/`.

## Stop and report

If the mode cannot be observed without touching `internal/operatorauth/**`, stop and report file:line.

## Handoff

Branch: `lane-0428-214-destroystamp` @ `a8079303acaaba860ae444eec684ff9625551f82` (rebased onto current base; round-5 akte)
PR: #1738, base `lane-0428-198-cli-shard-operator-env` (chain rule 3.3.8, content wait on #1726)
Base head: `7546b1806aac9a0055a647e20f2843564eb3c1ce` (base lane #198 was rebased since round-4 old pointer c2f9f2f32fd; DRIFT recorded in round-5)
Terminal hosted run: 44878737065 (PR Selected Checks aggregate FAILURE; PR · Trusted Plan now SUCCESS after rebase; 3 inherited CLI-shard failures cli-0/native — out of this card's write-set, owned by #198; my test in cli-2 435-passing set)
Evidence:
`evidence/r28-welle4-2026-11-21/destroy-authority-stamp/round-5-rebase.md`.

kommissioniert auf dem freien ornith-sitz: branch vom head der basis-lane 0428-204 (7db142852d22), base-ref des PRs auf den lane-branch 'lane-0428-204-cli-operator-entrypoints'. write-set genau eine datei: cmd/baha/core_installation_runtime_test.go. konfliktfrei gegen 213 und 207. lane 5b17f066, modell verifiziert.

214-lane nannte PR #1738 im feld 'PR', aber 'prs:' war leer; prs gefuellt. gemessen: refs/heads/lane-0428-214-destroystamp = ebc6ac9c3a30, merge-base --is-ancestor 7db142852d22 <head> = 0, eine eigene datei, base-ref = lane-0428-198-cli-shard-operator-env.

kandidat vollstaendig und gemessen: head ebc6ac9c3a30, base-ref 'lane-0428-198-cli-shard-operator-env' @ 7db142852d22 (ketten-regel), draft=false. der ECHTE durchgang 44862425216 (von MIR per undraft ausgeloest) ist terminal: policy/Trusted Plan/Native gate plan/Source format/Focused Python/cli-vet/cli-build/cli-gofmt/source-contracts = SUCCESS, 'PR · Go unit · cli-0..3' = failure (geerbte operator-auth-klasse; scheitert ebenso an der basis #1726). mein eigener grep am protokoll: '--- FAIL: TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget' = 0 zeilen, der karten-fall scheitert also in KEINEM ausgefuehrten shard. reichbarkeits-beleg der lane: 'authorization.go:235' (claim-membership-ast) nur mit verified principal + provider. PROTOKOLL-VERSTOSS FESTGEHALTEN: die lane hat ihre END-zeile per 'codeman agent post 9142ab1f-…' an mich gepostet — genau das ist verboten (AGENTS 3.3.4, die meldung laeuft ueber den watch-pfad, nicht ueber post an eine fremde session). folge: sitz wird freigegeben (rotation), arbeit bleibt gutgeschrieben.

kette nachgezogen, von mir gemessen: head bdc3fcb63912, base 'lane-0428-198-cli-shard-operator-env' (basis-head beim rebase c2f9f2f32fd6, seitdem e45430f2f1b7 — fuenfter owner-push), 'merge-base --is-ancestor' = 0, draft=false; eigener durchgang terminal: run 44867291850 / 44867319394 completed/failure, cli-shards geerbt. WICHTIG FUER DIE ABNAHME: PR Selected Checks faehrt einen pr_merge-commit (85ae26150145 = 'Merge <head> into <base>'), 'exact-head' heisst bei gestapelten PRs der merge, nicht der branch allein. Akte round-3-chainrebase.md (plan 38b79bce).

CODEX-REVIEW 'Verdict: REQUEST CHANGES' (destroy-authority-stamp/review-1.md, origin/main b3816e18/b33d3e3f) an head bdc3fcb63912: P1 = die behauptete RUECKNAHME des eigen-stempels ist im kandidat NICHT enthalten — 'cmd/baha/core_installation_runtime_test.go:294-306' reicht den bereits gestempelten kontext weiter, die neue assertion ':332-346' ruft zwar die produktions-grenze, nutzt aber denselben kontext. Rezept des reviewers: teardown-only fixture-kontext und authority-assertion trennen (':274-306', ':309-346'). P2 zaehlt GENAU DREI erste-level-FAIL-zeilen am durchgang 44867319394 (log 903158 bytes, log-failed 16321) und sagt ausdtruecklich: 'not to be booked as a generic inherited gate class — the exact gate text is absent'. Die drei: (1) 'app_list_all_targets_test.go:26' = karte 0428-210/#1739; (2) 'secure_profile_export_command_test.go:125' 'operator authentication needs interactive setup' (textquelle 'cmd/baha/operator_auth_boundary.go:117'); (3) 'target_hotfix_test.go:201' 'target "edge-a" is not configured'. IHR eigenen fall scheint im protokoll NICHT als fail — was der reviewer als P2-notiz festhaelt, und der grund, warum ich sie zurueck auf 'active' setze statt auf 'review'.

korrektur-lane '0428-214-stampfix' (2dfa5466, ornith) dispatcht; ihr auftrag fuehrt das rezept des reviewers wortlich (trennung von fixture-teardown-kontext und authority-assertion, ':274-306' und ':309-346'), dazu der reichweiten-beweis in beide richtungen als vorbild aus #1741 und die rot-zuerst-pflicht mit STOP-kriterium.

meine entscheidung UBER den gemeldeten blocker der lane (END_BLOCKED, und sie hatte recht): das rezept des reviewers zielt auf einen ast, den es am ziel nicht geben kann. gemessen: 'coreBootstrapFixtureCleanupContext' ('cmd/baha/core_installation_runtime_test.go:274-300') ist ausdruecklich test-only teardown MIT synthetischem editor-principal (kommentar ':297-299': 'production auth and local-runtime authorization paths remain unchanged'; ':279-281' verbieten wiederverwendung eines unrelated principal), und 'installation.destroy' fehlt in 'operatorauth.LocalWorkloadOperation' — darum liefert 'verifiedLocalWorkloadAuthority' ('cmd/baha/local_workload_authority.go:41-59') 'local=false'. DIE gesuchte authority lebt und ist getesteT: 'application_destroy_authorization.go:29-38' (operation='installation.destroy' nur mit 'installationApplicationScope'-proof) -> 'installation_application_scopes.go:23-45' (gerufen in 'runtime_destroy_all.go:103', 'management_remote_installation_destroy.go:80'), unit-abgedeckt in 'installation_application_scopes_test.go:23/:27/:58' + 'installation_sibling_scope_test.go:42/:77/:82'. Auftrag an die lane: assertion auf DEN mechanismus verlagern (positive + negative richtung), teardown-stempel bleibt unangetastet. Karte bleibt 'active', ein PR (#1738).

korrektur delivered, abnehmbar, ABER ohne PR-Selected-Checks-Quittung: head a25a74c23c23 (branch == PR-head, gemessen), base e45430f2f1b7 unveraendert, draft=false. inhalt: 'TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope' in 'cmd/baha/core_installation_runtime_test.go' (+50 zeilen, einzige erlaubte datei), positiver ast durch den 'installationApplicationScope'-naht des destruction-planners, negativer ast OHNE consent failt closed mit 'impact-confirmation-required'; der synthetische teardown-stempel ist UNANGETASTET (wie sein eigener kommentar verlangt). GEHOSTET: run 44875783227 — 'Workflow policy'/'Native gate plan'/'Source format' success, 'PR · Trusted Plan' FAILS (schritt 'Resolve exact immutable PR inputs using trusted base policy', 'python3 $RUNNER_TEMP/pr-gate-plan.py --diff …' exit 1 nach 0.2 s), DARAUFHIN sind 'PR · Go unit · shards', 'Selected Core-less', 'Selected Runtime' = skipping und 'PR Selected Checks' failt nach 8 s. Das erklaert auch die 20 skipped checks an #1737: der gate-planner verweigert die basis/head-paarung, nicht den test. DIagnose-lane laeuft (issuefamilie 0428-208/'ci.yml:1301').

inhaltlich von mir abgenommen (round-3), ABER der kandidat kann CI-NICHT bekommen: meine diagnose-lane (600aa109, akte round-4-gateplanner.md, plan c9937f5a) beweist 'ursache = PR #1738 head a25a74c23c23 ist KEIN nachkomme seiner base e45430f2f1b7, abzweigung bei c2f9f2f32fd'. Der trusted-base-guard ('git merge-base' fail-closed) bricht ABOR VOR dem planner: exit 1, ~0.2 s, keine stderr-zeile — deshalb 'PR · Trusted Plan' failure + ALLE fan-out-zellen 'skipping' + 'PR Selected Checks' failure nach 8 s. Meine eigene nachmessung: #1737 und #1738 = keine nachkommen; #1741 und #1740 = nachkommen (deshalb dort cli-1/2/3/owner SUCCESS). H1 (andere planner-version) WAIDERLEGT (sha256 identisch base vs develop), H2 (unmappbarer pfad) WAIDERLEGT (9 neue _test.go dateien -> 'broad_required' fallback, exit 0), H3 (leerer diff) nur als JSONDecodeError-Reproduktion relevant. Der planner selbst braucht KEINE owner-änderung an scripts/**; noetig ist ein REBASE der beiden lane-branchs auf e45430f2f1b7.

inhaltlich abgenommen (round-3, akte round-3-scope-proof.md), aber UNBEWEISBAR am kandidat bis zum rebase: meine diagnose-lane (600aa109, akte round-4-gateplanner.md, plan c9937f5a) beweist URSACHE = 'PR #1738 head a25a74c23c23 ist KEIN nachkomme seiner base e45430f2f1b7; abzweigung bei c2f9f2f32fd'. Der trusted-base-guard bricht VOR dem planner (exit 1, ~0.2 s, keine stderr) -> 'PR · Trusted Plan' failure, alle fan-out-zellen 'skipping', 'PR Selected Checks' failure nach 8 s. Meine nachmessung der nachkomme-frage: #1737 NEIN, #1738 NEIN, #1741 JA, #1740 JA (deshalb dort cli-1/2/3/owner success). H1 (planner-version differs) WAIDERLEGT: sha256 von scripts/pr-gate-plan.py identisch base vs develop. H2 (unmappbarer pfad) WAIDERLEGT: 9 neue _test.go dateien fallen auf 'broad_required' zurueck, exit 0. H3 (leerer diff -> JSONDecodeError) real, aber nicht der abbruchpfad. KEINE aenderung an scripts/** noetig: nur REBASE beider lane-branchs auf e45430f2f1b7.

rebase delivered, und der fenster-blocker ist damit AN DIESER KARTE GELÖST (von mir gemessen, nicht von ihr): head a8079303acaa, 'PR · Trusted Plan' = success, fan-out skippt nicht mehr (19 skipped = pfadfilter statt ALLE), 'PR Selected Checks' weiter failure aus ERBSCHAFT: cli-0 'TestAppListAllTargetsWorksAfterInstallationDestroy' = 0428-210/#1739, packages 'providers/loki/shared/service-access/pki/client-cert.pem' = owner-stapel #1615. IHR fall laeuft und besteht im cli-2-durchsatz (435 PASS). BASIS-KORREKTUR: sie meldet 'current base 7546b1806' — drei unabhaengige lesegaenge (gh api git/refs + zwei ls-remote) geben 'e45430f2f1b7', und 7546b1806 ist AHNE davon (9 commits, 'merge-base --is-ancestor' = 0). Der rebase zielte also auf ein veraltetes SHA: unschaedlich fuer den guard, aber der diff gegen die echte basis zeigt 25 dateien statt der einen ihrer karte — der reviewer muss gegen e45430f2f1b7 bilden. Inhaltlich unveraendert: 'TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope' (positiv durch die 'installationApplicationScope'-naht, negativ ohne consent = 'impact-confirmation-required'), teardown-stempel unangetastet.

CODEX-REVIEW 'review-2.md' (plan ea196e46 + 04ae137d) = 'Verdict: REQUEST CHANGES', drei belege, alle von mir nachvollzogen. BEFUND 1 (inhalt): 'cmd/baha/core_installation_runtime_test.go:378-386' behauptet die ausgewaehlte destruction-operation NICHT — nachtrag: positiver kontext MIT enforcement-stellung OHNE principal, 'operatorauth.AuthorizationDecisionFromContext(ctx)' lesen, 'Allowed' UND 'Operation == "installation.destroy"' verlangen, plus mutation (zuordnung weg = rot); no-consent-assertion und teardown-stempel bleiben. BEFUND 2 (basis) = MEINE EIGENE MESSENSCHAFT von row 874: 'merge-base --is-ancestor e45430f2f1b7 a8079303acaa' = NEIN, merge-base ist 7546b1806aac, 9 commits rueckstaendig; rebase auf das echte ziel, kein zweiter branch. BEFUND 3 (aggregat): cli-0 'TestAppListAllTargetsWorksAfterInstallationDestroy' = 0428-210/#1739 und die nativen docker/podman-zellen = 0428-215/#1745 — fremde baustellen; der reviewer behaelt meine gleich-basis-per-job-rechnung (durchgang 44867737065 gegen 44867737078) und bucht den aggregate TROTZDEM als failure. MISSION liegt fertig im coordinator/missions/ (0428-214-r5-bothdirections.md, payload-gate 0) und geht auf den ersten frei werdenden sitz — in der abnahme-stunde waren alle funf plaetze belegt, daher kein Scheinauftrag.

ROUTE NEU FESTGELEGT NACH CENSUS (akte operator-auth-helper/carrier-census-1737-1738-1740-1741.md, plan commit da2176f7f40, von 1450c201 gemessen): PR 1726 wird NICHT wieder eroeffnet und es entsteht KEIN neuer traeger - #1750 ist gemergt, also wird der JEWEILIGE eigene delta des kandidaten auf develop 8629450ef3c neu geschnitten. Fernzeugnis der kinder: alle back=275, mergeStateStatus UNSTABLE, base zeigt auf die tote basis lane-0428-198-cli-shard-operator-env (spitze e45430f2f1b). Carrier-abhaengigkeit: nein. Ihr PR-head gemessen: 1738 siehe akte 'Child PR state and diff against the named carrier'. Naechster schritt: mission auf dem ersten freien arbeits-sitz (neu schneiden statt hoepfen; bei 'nein' reicht der additive hop), dann exact gehosteter durchgang + unabhaengige pruefung. Kein merge aus der alten basis heraus.

RE-CUT BEAUFTRAGT, weil der census diesen kandidat als EINZIGEN der vier kinder OHNE carrier-abhaengigkeit ausweist (akte carrier-census-1737-1738-1740-1741.md, plan da2176f7f40): base retarget auf develop (eine einzige metadata-aenderung, ausdruecklich autorisiert), dann additiver hop auf 8629450ef3c, danach EIN durchgang mit den vier data-capabilities-job-ids als zeugen. rueckstand 275 commits, 30 dateien. Ausfuehrende lane ist f0f6c8b4 (frei nach der 237-rueckgabe). KONFLIKT-REGEL: wenn die erzeugten index-dateien im merge konfliktieren, gilt der generator-pfad, kein hand-edit; sollte dafuer .github/scripts betroffen sein, STOP mit datei:zeile an mich (reservierte gebiete).

RECONCILED: stale mission '0428-214-r5-bothdirections' (rebase onto retired #1726 + no-merge) ist SUPERSEDED. card sagt develop retarget + re-cut after #1750 merged - #1750 IST GEMERGT (f6d3fc5c) -> precondition erfuellt. PR #1738 dirty auf 7e679293 (275 stale commits) -> NEUER recut-lane auf develop 31aededf, additiv. User verlangt MERGE wenn ready -> no-merge instruction aufgehoben. exact 4 data-caps jobs. 0847d100 drauf.

STALE-MISSION REKONCILIIERT + KOLLISION VERHINDERT: '0428-214-r5-bothdirections' (rebase onto retired #1726 + no-merge) ist SUPERSEDED. Owner fuhr den recut SELBST: head 2ba70a58 = single-file cmd/baha/core_installation_runtime_test.go auf develop 31aededf, force-with-lease (gleicher PR, kein develop-descendant -> erlaubt unter close-all mandat), altes 7e679-stack entfernt. Coordinator-dispatch an 0847d100 auf #1738 zurueckgezogen (kein competing writer). review: exact hosted run auf 2ba70a58 beobachten, merge wenn aggregate gruen + review.

#1781 (coreinst catalog) GEMERGT 6930872c -> core_installation_runtime_test cataloged. #1738 recut (2ba70a5) additiv auf 6930872c gehoppt von f0f6c8b4 + exact hosted. Trusted Plan greift jetzt (catalog da). selected haengt ggf. an #1780(241). develop 6930872c.

run 45043343935 cli-2 137272473729 failt core_installation_runtime_test.go:375 'managed-environment machine ops require authenticated operator' = destroy braucht test-only synthetic-operator stamp (Option A fixture) ODER fail-closed assert. re-hop auf b27b2ebe (#1782) noetig (head f0adb35 stale 3939aa5). STOP-Fall: product-247. f0f6c8b4 geroestet.

#1738 run 45044988050 terminal rot = 3 klassen: (A) selected footprint-show record-deployment-confirm = shared, loest PR #1783 (optionA). (B) native broker readiness 503 = 0428-237 andere session. (C) cli-2 destroy core_installation_runtime_test.go:375 braucht authenticated operator context = f0f own FIX (tagged test-only fixture stempelt destroy-pfad ODER fail-closed assert; STOP-Fall=247). Dazu re-hop e09ceb9a (stale base 3939aa5) -> b27b2ebe + exact hosted docker+podman. Kein merge vor exact run+current base.
