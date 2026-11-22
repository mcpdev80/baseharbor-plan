---
id: t-20261122-static-cells-operator-auth-helper
card_number: "0428-231"
card_short_title: "operator auth in static cells"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: b90e4ba1 (#1771 hopped 2d578b1d TP GREEN via #1786; #1761 b9b8f059 TP-green inherits #1783/#1788) / Coordinator
kanban_status: review
kanban_lane: review
kanban_summary: ""
kanban_title: 0428-231 · operator auth in static cells
priority: ""
depends_on: [t-20261121-develop-full-suite-red]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1761, mcpdev80/baseharbor#1771, mcpdev80/baseharbor#1746, mcpdev80/baseharbor#1784, mcpdev80/baseharbor#1785, mcpdev80/baseharbor#1783, mcpdev80/baseharbor#1786, mcpdev80/baseharbor#1762]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1761", "https://github.com/mcpdev80/baseharbor/actions/runs/44994765677", "https://github.com/mcpdev80/baseharbor/actions/runs/44998552411", "https://github.com/mcpdev80/baseharbor/actions/runs/44999534797", "https://github.com/mcpdev80/baseharbor/actions/runs/45000121766", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/static-cells-operator-auth-helper/review-1761-head669d76ac447.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/static-gate-registration/hunt-operator-auth-static-cells-round-1.md"]
---

- [ ] t-20261122-static-cells-operator-auth-helper · operator auth in static cells #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** b90e4ba1 (\#1771 hopped 2d578b1d TP GREEN via \#1786; \#1761 b9b8f059 TP-green inherits \#1783/\#1788) / Coordinator  
    **PR:** [baseharbor#1761](https://github.com/mcpdev80/baseharbor/pull/1761), [baseharbor#1771](https://github.com/mcpdev80/baseharbor/pull/1771), [baseharbor#1746](https://github.com/mcpdev80/baseharbor/pull/1746), [baseharbor#1784](https://github.com/mcpdev80/baseharbor/pull/1784), [baseharbor#1785](https://github.com/mcpdev80/baseharbor/pull/1785), [baseharbor#1783](https://github.com/mcpdev80/baseharbor/pull/1783), [baseharbor#1786](https://github.com/mcpdev80/baseharbor/pull/1786), [baseharbor#1762](https://github.com/mcpdev80/baseharbor/pull/1762)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1761), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44994765677), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44998552411), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44999534797), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/45000121766), [proof 6](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/static-cells-operator-auth-helper/review-1761-head669d76ac447.md), [proof 7](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/static-gate-registration/hunt-operator-auth-static-cells-round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261121-develop-full-suite-red](t-20261121-develop-full-suite-red.md)  
**Owner:** b90e4ba1 (#1771 hopped 2d578b1d TP GREEN via #1786; #1761 b9b8f059 TP-green inherits #1783/#1788) / Coordinator  
**Priority:** not set  
**PRs:** [baseharbor#1761](https://github.com/mcpdev80/baseharbor/pull/1761), [baseharbor#1771](https://github.com/mcpdev80/baseharbor/pull/1771), [baseharbor#1746](https://github.com/mcpdev80/baseharbor/pull/1746), [baseharbor#1784](https://github.com/mcpdev80/baseharbor/pull/1784), [baseharbor#1785](https://github.com/mcpdev80/baseharbor/pull/1785), [baseharbor#1783](https://github.com/mcpdev80/baseharbor/pull/1783), [baseharbor#1786](https://github.com/mcpdev80/baseharbor/pull/1786), [baseharbor#1762](https://github.com/mcpdev80/baseharbor/pull/1762)  
**Source:** 
<!-- /generated:links -->


## Why

Measured by lane `b90e4ba1` (akte
evidence/r28-welle5-2026-11-22/develop-full-suite-red/diagnose-1.md): the helper
`testIsolatedSelectionContext` exists in 7 files at head f16cef27 of PR #1750 and in 0 files at develop 8b9a8f50645 -
so most of these cells clear when #1750 merges. This card stays open only for the parts that survive that merge.


At head `fec44963` of PR #1746 the full Pre-Release run `44980411417` fails in several cells with the same guard:
`Static · init` job 137080600559, `Static · shell-ux` job 137080600541, `Static · config-matrix` job 137080600642,
plus `Integration · integration/docker/core-bootstrap` job 137080600131 and
`Integration · integration/podman/core-bootstrap` job 137080600055 all print
`Managed-environment machine operations require an authenticated BaseHarbor operator.`

That message comes from `cmd/baha/mcp.go:317`. The helper that satisfies it inside a test process already exists
(`runWithIOAsTestOperator`, used by `cmd/baha/env_destroy_integration_test.go:127`), but these cells still drive the
machine paths through the interactive operator path, so they fail regardless of which product PR runs them.

## Acceptance

- The failing init / shell-ux / config-matrix / core-bootstrap paths use the same non-interactive operator helper that
  #1750 delivers for env destroy, so the guard is satisfied without a terminal.
- Hosted CI shows the five jobs above green at one exact head; no local run counts.

PR 1761 ist drafted (kein fertiger kandidat): branch lane-0428-231-static-auth-helper, head 5794874302f1, base 52a3c544 (back=0), gehosteter run 44994765677 SUCCESS/0 failed. Inhalt: ein exportierter helper in internal/operatorauth/test_operator.py -> test_operator.go plus die fan-out ueber die fnf gemessenen dateien (test_operator_context_test.go, app_env_test.go, app_export_command_test.go, installation_destroy_native_test.go, target_definition_change_test.go). Die Lane-Schreibsperre auf internal/operatorauth/** war fuer GENAU diese datei durch die owner-direktive zur helper-route gehoben. Naechster schritt: CODEX-REVIEW am exakten head, dann ready-schalten (entscheidung liegt beim owner, weil der PR draft ist) und fan-in von PR 1746 auf den helper.

helper ist fertig und gruener gelaufen (run 44998552411 SUCCESS am head d275e50c5ba, branch lane-0428-231-static-auth-helper). PR bleibt DRAFT: das ready-schalten ist des owners hand. Rueckstand: base-pointer 52a3c5446f4, develop ist acc34323968, mergeable_state BEHIND - der dritte hop ist der lane befohlen. Diese karte ist die vorgegebene sequenz-stufe vor PR 1746 (0428-208): erst 1761 rein, dann dessen statische zellen-beweise, dann 1746 hop und static suite.

korrekturronde ABGESCHLOSSEN, kandidatiegruen: head d275e50c5ba0245b6ab8a42f9655c9bef1bb2bd0 (additive kette 57948743 -> e0d4a0e3 -> d275e50c), base 52a3c5446f4, PR bleibt DRAFT (ready-schalten ist des owners hand). Gehosteter run 44998552411 SUCCESS/0 failed, cli-shards 137134801858 / 137134801765 / 137134801777 / 137134801792 und packages 137134801752. Fan-out ist VOLLSTAENDIG: alle fnf dateien rufen den helper, keine zweite provider-definitie. Offene punkte: ein hop auf develop acc34323968 (befohlen) und danach exact-head review, dann merge - diese karte ist die sequenz-stufe vor PR 1746.

hop von ihrer lane ist belegt: head 669d76ac447, additiv aus develop acc34323968, back=0, run 44999534797 SUCCESS/0 failed, cli-shards 137137806291/137137806376/137137806417/137137806374 und packages 137137806463; die draft-routen-reihen (native-matrix 137137808006, selected-runtime 137137808013, selected checks 137137808235, validation-matrix 137137807405) waren SKIPPED und zaehlen nicht als beleg. Danach hat der owner den PR auf READY geschaltet: draft=false, der VOLLE gehostete run 45000121766 ist aktiv mit 36 jobs, und die beiden nativen data-capabilities-reihen (docker UND podman) werden erstmals AUSGEFUEHRT. Exact-head review ist aktiv bei fecbada9, merge erfolgt nach gruenem CI + verdict.

EXAKT-HEAD REVIEW = APPROVE am head 669d76ac44792a56d2642df05c5211058460b3bb (akte static-cells-operator-auth-helper/review-1761-head669d76ac447.md, plan main 305bf4149c7): fan-out ist VOLLSTAENDIG, die provider-definitie steht GENAU EINMAL. Beleg am draft-stand: run 44999534797 SUCCESS/0 failed; die nativen reihen waren damals skipped, darum gab es KEINEN matrix-beleg - der reviewer hat das ausdruecklich als stand benannt, nicht als freigabe. Nach dem ready-schalten des owners ist aktiv der volle CI 45000121766 mit AUSGEFUEHRTEN nativen data-capabilities-reihen (docker 137139636770, podman 137139636747, selected-runtime 137139969524 und 137139969537).Merge erfolgt erst, wenn dieser run terminal success ist; der merge-befehl liegt bereit.

AM EXAKTEN head 669d76ac447 ist ein Exact-Head-APPROVE vorhanden (akte review-1761-head669d76ac447.md, plan main 305bf4149c7, fan-out voellig, provider genau einmal). ABER der volle CI 45000121766 zeigt einen ECHTEN fehlgeschlagenen nativen job: native/docker/data-capabilities 137139636770 faellt in TestApplicationCapabilityLifecycleExistingCore/secrets, broker-readiness timeout nach 2m03s. Das ist DIESSELBE signatur wie bei PR 1753, 1723 und 1725 - und sie erscheint jetzt an develop acc34323968 selbst. Damit ist die these 'nur base-zeiger-verzug' FUER DIESEN FALL WIDERLEGT: der defekt hat develop-Hoehe. Kein merge, bis der run gruen ist (weigerung des owners). Die karte 0428-240 (diagnostics im CLI-fehlertext, cmd/baha/app_broker.go:206) ist auf einer ausfuehrenden lane; der readiness-fix selbst braucht eine besitzer-entscheidung, weil die abhaengigkeit im fehlertext bisher NICHT benannt wird.

merge ist NICHT erfolgt, preflight hat korrekt abgelehnt: exact run 45000121766 ist TERMINAL FAILURE (native docker 137139636770 und native podman 137139636747, broker-readiness timeout 2m03s in TestApplicationCapabilityLifecycleExistingCore/secrets), alle uebrigen shards und source-format sind SUCCESS. Der Exact-Head-APPROVE am selben head bleibt gueltig fuer den INHALT; was fehlt, ist der native beleg, und der haengt an 0428-237. Karte steht darum auf wait mit dem defekt als grund - nicht auf review.

merge ist NICHT erfolgt: preflight hat korrekt abgelehnt, weil run 45000121766 TERMINAL FAILURE ist (native docker 137139636770 und podman 137139636747, broker-readiness timeout 2m03s), alle anderen shards SUCCESS. Der Exact-Head-APPROVE am selben head gilt fuer den inhalt weiter; der fehlende native beleg haengt an 0428-237. Kein unveraenderter rerun.

MESSE STATT MEINUNG, vier protokolle selbst gezogen (gh api job-logs): selected-docker 137139969524 (PR 1725) zeigt wortlich den fehlgeschlagenen aufruf 'app footprint show -o json' plus 'operator/automation consent (--confirm-candidate); refusing to record deployment state' (achtfach im selben job, digest 9a4da90e4e0d60e54a45a1ccf16b2a147a53eb7c865fc67d87d9b837df509295); selected-podman 137139969537 ebenso (257 KB / 242 KB protokolle). In ALLEN vier gelesenen jobs (dazu 137139636770 und 137139636747 von PR 1761) steht 'readiness timeout' NULL mal und 'not_ready' GENAU EIN mal (podman 137139636747). SHARED BLOCKER DAMIT: die fussnoten-ZULASSUNG, also dieser kandidat und karte 0428-227 - NICHT die broker-chronologie 0428-237. Ich habe 0428-237 umgeschichtet (keine aenderung an internal/controlplaneruntime ohne wiederholbaren not_ready auf develop 8629450ef3c).

MESSE STATT MEINUNG, vier protokolle selbst gezogen (gh api job-logs, 72-257 KB): selected-docker 137139969524 (PR 1725) zeigt wortlich 'app footprint show -o json' plus 'operator/automation consent (--confirm-candidate); refusing to record deployment state' (achtfach, digest 9a4da90e4e0d60e54a45a1ccf16b2a147a53eb7c865fc67d87d9b837df509295); selected-podman 137139969537 ebenso. In ALLEN vier gelesenen jobs (auch 137139636770 und 1371396747 von PR 1761) steht 'readiness timeout' NULL mal, 'not_ready' GENAU EIN mal (podman 137139636747). SHARED BLOCKER = die fussnoten-ZULASSUNG (0428-227), NICHT die broker-chronologie 0428-237; 0428-237 habe ich umgeschichtet (kein eingriff in internal/controlplaneruntime ohne wiederholbaren not_ready auf develop 8629450ef3c).

MESSE STATT MEINUNG: selected-docker 137139969524 (PR 1725) zeigt wortlich 'app footprint show -o json' plus 'operator/automation consent (--confirm-candidate); refusing to record deployment state'; selected-podman 137139969537 ebenso. In allen vier gelesenen jobs (auch 137139636770 und 137139636747 von PR 1761) steht 'readiness timeout' NULL mal, 'not_ready' GENAU EIN mal (podman 137139636747). SHARED BLOCKER = fussnoten-ZULASSUNG (0428-227), NICHT die broker-chronologie 0428-237.

MESSE STATT MEINUNG, vier protokolle selbst gezogen (gh api job-logs, 72-257 KB): selected-docker 137139969524 (PR 1725) zeigt wortlich 'app footprint show -o json' plus 'operator/automation consent (--confirm-candidate); refusing to record deployment state'; selected-podman 137139969537 ebenso. In ALLEN vier gelesenen jobs (auch 137139636770 und 137139636747 von PR 1761) steht 'readiness timeout' NULL mal, 'not_ready' GENAU EIN mal (podman 137139636747). SHARED BLOCKER = die fussnoten-ZULASSUNG (karte 0428-227), NICHT die broker-chronologie 0428-237.

MESSE STATT MEINUNG, vier protokolle selbst gezogen (gh api job-logs, 72-257 KB): selected-docker 137139969524 (PR 1725) zeigt wortlich 'app footprint show -o json' plus 'operator/automation consent (--confirm-candidate); refusing to record deployment state'; selected-podman 137139969537 ebenso. In ALLEN vier gelesenen jobs (auch 137139636770 und 137139636747 von PR 1761) steht 'readiness timeout' NULL mal, 'not_ready' GENAU EIN mal (podman 137139636747). SHARED BLOCKER = die fussnoten-ZULASSUNG (karte 0428-227), NICHT die broker-chronologie 0428-237.

STANDALONE bestehende gate, KEIN #1746-blocker (owner-erklaerung): 'Managed-environment machine operations require an authenticated BaseHarbor operator for shell-ux-static/dev' - die shell-ux-static/dev zelle braucht eine operator-auth BASELINE/fixture. Das ist eine EIGENE bestehende gate, die der PR 1746 nicht verursacht und nicht blockiert (1746 cli-3 ist SUCCESS). Wer die operator-auth baseline in den static cells liefert, loest diese gate. Nicht mit 1746-akzeptanz verwechseln.

HUNT-belegt -> UNABHAENGIG fixbar (nicht an #1753 gekoppelt). PRIMAERDEFEKT cmd/baha/local_workload_authority.go:62: fixture meldet '--access local-docker', check vergleicht gegen 'local' -> grant faellt ab -> 'authenticated operator' fails in shell-ux/init/config-matrix statischen zellen. FIX: local-docker/local-podman als grant akzeptieren, regression in cmd/baha shards, KEIN .github. SEKUNDAR (tag baseharbor_ci_operator_testonly fehlt = no-op helper) NUR melden, ob fix 2 allein genuegt (tag waere .github owner-scope). NEBENBEFUND: static-mcp rot ist NICHT operator-auth sondern die 0428-232 demo-pin/candidate perses-divergenz.

SHARED-PREREQ. b90e4ba1 besitzt cmd/baha/operator_test_fixture_test.go. #1746 mcp-static failed an operator-auth fixture setup (Durchgang 45023477422) -> #1761 muss den static-cell operator-auth fixture-helper auf develop liefern. Achtung: #1769 nutzt fuer anonymen fall das REAL symbol operatorauth.WithEnforcement (kein neuer helper), also KEINE kollision. Guard/denial-logik NICHT aendern, kein auth-bypass.

PR #1771 (draft) head 172fb251 auf develop 8629450ef3c = BEHIND aktuellem develop 64eab13e -> b90e4ba1 hoppt einmalig additiv auf 64eab13e + exact-hosted + draft->ready. Root-cause KORRIGIERT: nicht ein alias; echte drop = root quick-init route OHNE app.adopt scope in cliLocalWorkloadOperation (main.go). Fix additiv isLocalRuntimeAccessProvider (local + local-docker/local-podman) in grant-check + init-scope. operator-auth/boundary INTAKT, KEIN .github/scripts/operatorauth. Runs 45023442557 + 45024197667 success/failed 0 am alten head. STATIC-GATES nicht lane-startbar (Owner workflow_dispatch pre-release.yml) - als ausloeser notiert, nicht als deficit. Dient #1746 mcp-static (geteiltes fixture/grant-issue). Akte plan origin/main.

0428-231 = operator-auth static-cells prereq fuer #1746 full static suite (shell-ux 137302542528/init 137302542587/mcp 137302542606/config-matrix 137302542638 fail 'authenticate operator'/authentication_failed). #1761(static-auth-helper head 669d76ac) + #1771(static-opauth-fix head dc775235) beide stale base, UNASSIGNED -> b90e additive hops b27b2ebe + rerun (helper->fix stacked). mcp target create mcp-static fail = pruefen ob 247 product-semantik (STOP->owner) oder helper deckt es. develop b27b2ebe.

0428-231 hops: #1771 ebd01baa Trusted Plan GRUEN (selected data-caps pending-runner). #1761 fcfe3f09 Trusted Plan FAIL weil cmd/baha/mcp.go unkatalogisiert (fail-loud guardian) -> geloest durch PR #1784 (mcp.go->gate.mcp, CI SUCCESS, review 1450c201). NACH #1784 merge: #1761 re-hop neuer develop -> Trusted Plan gruen. Dann #1746 static operator-auth gates (warten auf 231). develop b27b2ebe.

#1784 (mcp.go->gate.mcp) GEMERGT als develop 484c95fca -> loest #1761 Trusted Plan fail (war mcp uncataloged fail-loud). b90e re-hoppt #1761 auf 484c95fca (additiv). #1771 ebd01baa Trusted Plan gruen, selected data-caps pending-runner. 0428-231 -> #1746 static operator-auth gates. Review der 231 heads durch Owner wenn runs terminal. develop 484c95fca.

#1761 Trusted Plan fail ATTRIBUTION KORRIGIERT (war nicht mcp.go/#1784): #1761 fuegt 6 neue uncataloged sources hinzu = cmd/baha/{app_env_test,app_export_command_test,installation_destroy_native_test,target_definition_change_test,test_operator_context_test}.go + internal/operatorauth/test_operator.go (produkt operatorauth TestPrincipal/WithVerifiedTestOperatorPrincipalForced = legitimer static-auth-helper inhalt 0428-231). FIX = #1761 self-cataloged seine neuen files in pr-gate-coverage.json (lane-owned) + re-hop 484c95fca -> Trusted Plan gruen. native broker=#1770 waiting. #1771 ebd01baa selected docker fail (broker/parity), podman aktiv. Owner review bei terminal. develop 484c95fca.

#1771 ebd01baa run 45054073860 = DOWNSTREAM, own static-opauth-fix code OK. selected docker+podman fail an FIXTURE SETUP (nicht dem local-workload grant): target-create bootstrap lief, dann 'up' rejected (installation.json absent) + 'app footprint show' rejected outside managed workload set = #1783 fixture admission. native docker+podman fail ExistingCore secrets broker health = #1770 exact image. #1771 haelt (keine aenderung von owner/b90e noetig ausser re-hop auf develop-mit-1783+1770). Actions-API listet latest-attempt nur native jobs = job/attempt linkage, logs zeigen selected fails. develop 484c95fca.

b90e hop-both clean. #1761 fcfe3f09 Trusted Plan fail = 4 neue uncataloged sources (app_env_test/app_export_command_test/target_definition_change_test/internal/operatorauth/test_operator.go) - catalog-json AUSSERHALB hop write-set -> SEPARATER catalog-PR surface-e (f0f, muster #1784) noetig, dann #1761 re-hop -> gruen. #1771 ebd01baa Trusted Plan SUCCESS (main.go/local_workload_authority.go cataloged), fail nur native #1770 + selected ExistingCore 'Re-run --confirm-candidate'=SELBE demo-consent grenze #1783. KEIN target-create in beiden -> KEIN 247-stop. develop 484c95fca.

#1771 ECHTER selected-root-cause (independent review + bezeugt target.go:722): detectRuntimeForTarget behandelt access != '' && != 'local' als remote -> local-docker/local-podman GRANT im runtime probe blockiert, VOR engine ownership. FIX IN SCOPE 0428-231 (produkt target.go, b90e): local-docker/local-podman als lokal + shared provider/runtime check (local-docker<->Docker, local-podman<->Podman, unknown/remote/mismatch FAIL-CLOSED) + hosted regression. Erklaert selected fails (nicht nur #1783 demo-consent). native broker=#1770. #1761=catalog surface-e (f0f) dann re-hop. KEIN 247. develop 484c95fca.

STALL behoben: #1771 branch noch ebd01baa (target.go fix NICHT gepusht, b90e war idle). NEU DISCAPACHED an b90e: local-docker/local-podman als lokal + shared provider/runtime check fail-closed + regression + re-hop 484c95fca. #1761 branch fcfe3f09 wartet surface-e catalog-PR (f0f busy, branch noch nicht gepusht). #1597: owner hat obsolete run 45055436080 (1d1bdf) force-cancelled (golden newline mismatch gefixt in 993a57f2), current run 45056348316 queued (jobs unassigned, kein fail), 0847 observes + hop 484c95fca nach terminal. develop 484c95fca, 20 offen.

CATALOG-Order bestaetigt: #1785 (f0f surface-e, diff nur pr-gate-coverage.json, die 4 #1761 sources app_env_test/app_export_command_test/target_definition_change_test/internal-operatorauth-test_operator -> surfaces, checks green) = intended. Nach #1785 merge -> b90e re-hops #1761 (fcfe3f09 bleibt bis dahin) -> Trusted Plan gruen. #1771 target.go fix landed b9dc3c31; seine neue target_runtime_access_provider_test.go catalog-row kommt NACH #1785-merge rebase-basiert (selbe JSON, beide rows) -> kein competing write. #1597 98620890 parallel naechster merge. develop 484c95fca.

#1785 MERGED als 1253e8d0a (develop forward; catalog = mcp + 4 #1761 sources). #1761: b90e hoppt auf 1253e8d0a -> erbt catalog -> Trusted Plan gruen (war fcfe3f09 TP-red). #1771 b9dc3c31 TP-red wegen target_runtime_access_provider_test.go -> b90e setzt die row jetzt auf 1253e8d0a + re-hop, beide catalog-rows behalten (kein competing write mehr, #1785 drin). native data-caps = #1770 waiting. Dann 0428-231 gaetes -> #1746 static auth gates. #1597 re-hop 1253e8d0a (0847). develop 1253e8d0a, 20 offen (1785 raus).

#1771 provider-fix = CORRECT (detectRuntimeForTarget: local-docker<->Docker, local-podman<->Podman, mismatch/remote/unknown fail-closed, 9/9 regression; provider-reject 'no authenticated live runtime binding' NICHT mehr in native cells -> grant laeuft bis candidate-consent (#1783/#1770 familie, separat). #1771 TP failt NUR wegen 2 uncataloged diff-sources (cmd/baha/target.go MODIFIED + target_runtime_access_provider_test.go NEW), catalog ausserhalb #1771 write-set -> f0f surface-f catalog-PR (#1785 muster), dann b90e re-hop #1771. #1761 hop auf 1253e8d0a (erbt #1785) -> TP gruen. develop 1253e8d0a.

#1761 hop b9b8f059 auf 1253e8d0a = Trusted Plan GREEN (erbt #1785 catalog). run 45059388188: SELECTED docker+podman data-caps FAIL = SELBER geteilter #1783 fixture seam (app new/create-only operator auth, admitted nur gate==guided :129) - KEIN unique #1761 defect, KEIN demo digest-edit (no-op). #1761 erbt #1783 fixture-loesung: nach #1783 app-new admission merge + #1761 re-hop -> selected gruen. native docker/podman = :edge broker #1770 (laufen noch). Kein merge bis terminal + nach #1783. #1771 TP-fail wartet surface-f rows (f0f). develop 1253e8d0a.

#1761 hop b9b8f059 (auf 1253e8d0a) Trusted Plan GREEN run 45059388188 terminal; selected data-caps fail = geteilter #1783 app-new seam (kein unique fix, erbt loesung). #1786 GEMERGT (978a0f90b: target.go+provider-test rows) -> #1771 hoppt nach #1783 push auf 978a0f90b -> TP gruen. #1762 f0f additiver hop 978a0f90b (1-file test-only, GitHub-hosted dep-frei, native waiting-#1770). develop JETZT 978a0f90b (#1786 squash).

#1786 GEMERGT (develop 978a0f90b: #1771 target.go+provider-test catalog rows). #1771 b9dc3c31 = BEHIND -> additiver HOP 978a0f90b (b90e next, DEP-FREI von #1783, nur #1786 noetig) -> Trusted Plan gruen + rerun, neuer head. #1761 b9b8f059 TP-green; selected data-caps fail = geteilter #1783 app-new seam -> re-hop ERST NACH #1783 MERGE (erbt admission aus develop). native data-caps = :edge broker waiting-#1770. develop 978a0f90b.

#1771 b9dc3c31 = behind -> Trusted Plan fail (2 sources, jetzt in #1786 develop 978a0f90b katalogisiert). b90e additiver hop 978a0f90b (dep-frei, nur #1786 noetig) laeuft -> TP gruen + rerun, neuer head. Provider content fertig (docker<->Docker/podman<->Podman, mismatch/remote fail-closed + regression). #1761 selected = geteilter #1783 app-new/#1788 app-edit seam -> re-hop erst nach #1783<-#1788 combined merge. native :edge = waiting-#1770. develop 978a0f90b.

#1771 additiver hop 2d578b1d auf develop 978a0f90b (#1786: target.go + provider_test rows) -> TRUSTED PLAN GREEN (run: TP pass; der bisherige '2 unkatalogisierte sources' TP-fail ist damit behoben, catalog geerbt). Provider content fertig + regression (mismatch/remote fail-closed). fail=3 = native :edge waiting-#1770 + selected waiting-#1783/#1788. #1761 b9b8f059 TP-green, selected=#1783 seam erbt. Merge-ready beider nach #1770+#1783 combined + owner review. develop 978a0f90b.
