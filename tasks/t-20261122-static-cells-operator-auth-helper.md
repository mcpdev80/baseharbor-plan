---
id: t-20261122-static-cells-operator-auth-helper
card_number: "0428-231"
card_short_title: "operator auth in static cells"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: b90e4ba1 (lane, #1761)
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-231 · operator auth in static cells
priority: ""
depends_on: [t-20261121-develop-full-suite-red]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1761]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1761", "https://github.com/mcpdev80/baseharbor/actions/runs/44994765677", "https://github.com/mcpdev80/baseharbor/actions/runs/44998552411", "https://github.com/mcpdev80/baseharbor/actions/runs/44999534797", "https://github.com/mcpdev80/baseharbor/actions/runs/45000121766", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/static-cells-operator-auth-helper/review-1761-head669d76ac447.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/static-gate-registration/hunt-operator-auth-static-cells-round-1.md"]
---

- [ ] t-20261122-static-cells-operator-auth-helper · operator auth in static cells #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** b90e4ba1 (lane, \#1761)  
    **PR:** [baseharbor#1761](https://github.com/mcpdev80/baseharbor/pull/1761)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1761), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44994765677), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44998552411), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44999534797), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/45000121766), [proof 6](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/static-cells-operator-auth-helper/review-1761-head669d76ac447.md), [proof 7](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/static-gate-registration/hunt-operator-auth-static-cells-round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261121-develop-full-suite-red](t-20261121-develop-full-suite-red.md)  
**Owner:** b90e4ba1 (lane, #1761)  
**Priority:** not set  
**PRs:** [baseharbor#1761](https://github.com/mcpdev80/baseharbor/pull/1761)  
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
