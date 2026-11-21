---
id: t-20261120-r28-valkey-dashboard-unavailable-only
card_number: "0428-183"
card_short_title: "valkey dashboards gate"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w23-pr1714-0428-183-r3
kanban_status: wait
kanban_lane: wait
kanban_summary: ""
kanban_title: 0428-183 · valkey dashboards gate
priority: ""
depends_on: [t-20261121-loki-verify-probe, t-20261120-r28-cli-shard-operator-env]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1714]
sources: []
blocker: ""
wait_reason: "Independent review returned REQUEST CHANGES at head ecff7e2f575 (akte evidence/r28-welle4-2026-11-21/valkey-dashboard-unavailable/review-1-head1ecff7e2.md, verdict line 76): (1) two author identities 0428-183-realpos and worker in the four-commit range, card 0428-224 requires one identity; (2) the exact-head package job passed but its hosted log names no per-case test/duration receipt. Semantics themselves are fail-closed and the emitted-label query matches the golden, so no functional rework is requested. Content dependency: a writer for branch lane-0428-183-valkey-dashboard-gate (hop was taken by the Owner, lane w23 was released) and one scripts-scope receipt change by the Owner (same class as the #1625 finding, scripts/pr-go-unit-shard.py:60-82)."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md", "https://github.com/mcpdev80/baseharbor/pull/1734", "https://github.com/mcpdev80/baseharbor/actions/runs/44853938826"]
---

- [ ] t-20261120-r28-valkey-dashboard-unavailable-only · Perses: new DB/Valkey dashboards reachable only as DashboardUnavailable #task #release/v0-4-28 #status/wait #view/wait #kind/bug
    <!-- generated:card -->
    **Owner:** w23-pr1714-0428-183-r3  
    **PR:** [baseharbor#1714](https://github.com/mcpdev80/baseharbor/pull/1714)  
    **Waiting:** Independent review returned REQUEST CHANGES at head ecff7e2f575 (akte evidence/r28-welle4-2026-11-21/valkey-dashboard-unavailable/review-1-head1ecff7e2.md, verdict line 76): (1) two author identities 0428-183-realpos and worker in the four…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1734), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44853938826)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261121-loki-verify-probe](t-20261121-loki-verify-probe.md), [t-20261120-r28-cli-shard-operator-env](t-20261120-r28-cli-shard-operator-env.md)  
**Owner:** w23-pr1714-0428-183-r3  
**Priority:** not set  
**PRs:** [baseharbor#1714](https://github.com/mcpdev80/baseharbor/pull/1714)  
**Source:** 
<!-- /generated:links -->

## Found by bug hunt H-103 (funded from card t-20261117-hunt-signals-103, AGENTS 3.3.5 finding-to-card duty)

F2 of hunt round-1, measured at develop 96f2ae11a25a: internal/metrics/valkey.go:187, :195, :226, :265 return DashboardUnavailable on every path the hunt could reach, so availability is never true even when the backend is configured and verified.

## Acceptance

1. An availability path that returns a real dashboard (not DashboardUnavailable) when the backend signal is configured AND verified, mirroring the identity-dashboard predicate that 0428-078 hardened.
2. Tests for all three states (not_configured, configured_unverified, verified) on the Valkey face named by the finding (internal/metrics/valkey.go:187/195/226/265); configured_unverified must be false.
3. Mutation both directions (predicate reverted, availability branch forced) with separate isolated tests, and the CI job name in the evidence.

## Boundaries

internal/metrics/** plus the dashboard catalog. No .github/**, no gate changes. Coordinate with 0428-078 (identity dashboard) so the same availability semantics are not implemented twice differently.

hunt-fund F2 (akte hunt-signals-103/round-1.md) auf freiem sitz besetzt: valkey.go:187/195/226/265 liefert nur DashboardUnavailable, eine gesunde deployment-umgebung erreicht die dashboards nie. akzeptanz: echter verfuegbarkeits-pfad bei konfiguriert UND verifiziert (dieselbe verified-only-semantik wie 0428-078), tests fuer alle drei zustaende auf DB- und Valkey-seite, mutationen als ISOLIERTE tests, CI-jobname in der akte. SCHREIBFELD-ABGRENZUNG: perses_prometheus_datasource.go und perses_datasource_lifecycle.go (#1684) sowie perses_tempo_* / internal/capability/perses.go (#1645) sind ausdruecklich verschlossen, meldung statt doppelter schreiber (§4.3).

## Acceptance wording corrected by the coordinator (2026-11-20)

Item 2 originally said 'the DB and Valkey faces'. That wording came from my hunt summary, not from the finding: the
finding's only root location is internal/metrics/valkey.go. No DB dashboard catalog exists in internal/metrics at
develop 96f2ae11a25a, and the postgresql/mongodb keys live in internal/capability/perses_selection.go, which the owner
ruled closed for this card. Creating a new postgres catalog here would be new scope no contract asks for (§4.2), so the
card is limited to the Valkey face. If a DB dashboard availability path is genuinely wanted, it needs its own finding
and its own card, which the coordinator would found - not this lane as a side effect.

PR #1714 head c5b810c8cb85, 14 success / 20 skipped / 0 failure am exakten head. unabhaengige abnahme: REQUEST CHANGES - die valkey-verfuegbarkeit ist ein vom aufrufer gesetztes bool, es gibt keinen echten producer, das query spec ist leer, und der PR fuehrte titel/body 'x' (titel habe ich per REST PATCH gesetzt, head unbewegt: c5b810c8cb85 vorher = nachher). korrektur zugestellt.

HANDOFF ABGESCHLOSSEN (dritte runde war ein basis-drift, kein rueckfall): rebase auf develop f5ce95af, damit der 182-contract (RequiresAdapter -> Unsupported) drin ist; der stale test in perses_dashboards_valkey_test.go:178 UND der falsche kommentar in perses_dashboards_valkey.go:33-35 sind berichtigt. PR #1714 head 18e84809634e, branch = refs/pull/1714/head (dieselbe sha gemessen), draft=false, 3 dateien, checks 14 success / 20 skipped / 0 failure, run 44755545566, 'PR · Go unit · packages' completed/success (executed, nicht skipped). akte valkey-dashboard-gate/round-3.md auf main: 0 checkboxen, head 4x, run-id 4x, drift-beleg 6x. hintergrund gegen develop 3653369a4d83 = behind_by 1 (#1717/0428-188), hop vor dem merge, nicht vor der abnahme.

KORREKTURRUNDE nach Ihrem REQUEST CHANGES am exakten head 18e84809634e (verdict-akte evidence/r28-welle4-2026-11-20/codex-review-wave/1714-0428-183.md, main ec59061a9492). drei beleg, alle in DIESEM PR #1714: P1 der positive status war INJIZIERT statt aus dem echten producer - 'Supported' aus dem verfuegbaren availability-/authorized-/verified-pfad ableiten (stelle perses_dashboards_valkey.go:246); P2 das positive panel fuehrt keine daten-query - query-plugin-payload + echte expr in :230-248, regression auf die exported bytes; P3 der vertrags-text nach 0428-182 ist noch veraltet - :188-207, test :40-46 und :149-167. der negative fall bleibt, wie sie bestaetigt haben, richtig fail-closed. basis-hop auf develop 40cb28c vor der arbeit (unsere basis war f5ce95af). akte valkey-dashboard-gate/round-4.md, ein hosted run am exakten head mit 'PR · Go unit · packages' executed.

hop NICHT angekommen, von MIR gemessen: 'merge-base develop head' = 7fbb2d2c6c64 (= merge-commit von #1734, 08:25:49Z), 'rev-list --count head..develop' = 73 — der head ist 73 commits HINTER develop, ihr commit-text 'rebase onto 97b2ba554' ist damit falsch. Der gruene run 44905111045 gilt einem ueberholten stich, nicht dem exakten head (klasse 'ererbtes gruen' aus H-V40/H-V46). Dieselbe lane (1613a991) erhaelt einen NEUEN versuch mit zwei zusätzlichen bewiesen, die bisher fehlten: 'rev-list --count head..develop' = 0 UND 'git log -1 --format=%P' muss mit dem gemessenen develop beginnen; fetch des develop ueber 'refs/temp/develop-now', weil ihr vorhandener remote-tracking stand nachweislich alt war.

hop IST angekommen, von MIR erneut gemessen (nach meiner zurueckweisung): PR #1714 head d0ae338d7d4b, 'git log -1 --format=%P' = 97b2ba5543f0 = der gemessene develop, 'merge-base --is-ancestor develop head' = JA, 'rev-list --count develop..head' = 1, 'rev-list --count head..develop' = 0, mergeable=MERGEABLE. Meine vorige meldung '73 commits hinter develop' galt dem vorheren head 52688ef4c958 (merge-base 7fbb2d2c6 = merge-commit #1734); die lane hatte 13:51 bereits round 2 geschoben — mein lese-zugriff lief gegen den alten stand. Beide staende stehen in der akte, damit die folge nachvollziehbar bleibt. Die karte geht ins review; abnahme folgt in der abhaengigkeits-reihenfolge.

hop angekommen: PR #1714 head d0ae338d7d4b, vater = 97b2ba5543f0 = der gemessene develop, ancestry JA, 'rev-list --count develop..head' = 1, 'rev-list --count head..develop' = 0, mergeable MERGEABLE. Meine fruhere meldung '73 commits hinter develop' galt dem alten head 52688ef4c958 (merge-base 7fbb2d2c6 = merge-commit #1734); die lane hatte 13:51 bereits round 2 geschoben. Der hostete run 44906881418 am neuen head ist in_progress; ist er rot, kommt die karte zurueck auf active.

test hop

hop round 2 war korrekt (parent 97b2ba5543f0, 'rev-list head..develop' = 0, run 44906881418 success). develop bewegt sich: 14:09:38Z landed #1742 als merge-commit ddfa80f7202a, also ist head d0ae338d7d4b wieder vier commits rueckstaendig ('merge-base --is-ancestor develop head' = NEIN, 'rev-list develop..head' = 1). Dieselbe lane erhaelt den zweiten re-hop auf den aktuellen develop, fetch ueber refs/temp/develop-now. karte bleibt active bis der run terminal ist. #1742 ist GEMERGT, karte 0428-217 closed/accepted (https://github.com/mcpdev80/baseharbor/pull/1742).

hop round 3 IST ANGEKOMMEN, von MIR gemessen: PR #1714 head 0afcaf374225, 'git log -1 --format=%P' = dea88c8f2caa = der gemessene develop, 'merge-base --is-ancestor develop head' = JA, 'rev-list --count head..develop' = 0, 'rev-list --count develop..head' = 1, autor 0428-183-hopdev. Alle geforderten checks am EXAKTEN head: 'PR Selected Checks' pass, 'Go unit' cli-0/1/2/3 pass, 'Trusted Plan' pass; run 44911551416 completed/success (event=pull_request). Delta = 'internal/metrics/perses_dashboards_valkey.go' + test + testdata, keine tabu-beruehrung. Akte 'valkey-dashboard-unavailable/round-3-hopdevelop.md' auf origin/main. Damit ist die karte abnahme-reif; der abnahme-sitz ist noch mit H-V48 beschaeftigt und bekommt sie als naechstes.

verdict am head 0afcaf374225: positiver fall synthetisch. Korrektur auf 0428-183-realpos.

korrektur abgeliefert: head bf251b2b083d, PR-head = branch-head, head..develop = 0 (exakte base gegen develop e6c199e7b7dd), eigener run 44920689363 completed/success, 14 checks pass / 0 fail. Positiver fall laeuft jetzt ueber die injectierbare verification, der echte producer liefert auf develop 'unavailable'. Befund an die abnahme: zwei der drei commits tragen die generische 'worker'-identitaet (karte 0428-224).

verdict REQUEST CHANGES (2) an bf251b2b083d: (1) positiver pfad bleibt synthetisch (valkey_test.go:308-312), (2) query up{job="baseharbor-providers", backend="valkey"} (valkey.go:269) traegt ein 'backend'-label, das der provider-target-writer nicht emittiert — belegt durch die korrigierten hosts-dashboards (perses_dashboards_hosts.go:234 nutzt 'up{job=...}' ohne backend-label, :249-251/:276-281 erklaeren genau dieses muster als 'could never resolve against emitted data'). akte review-2.md, plan-sha 7814f2e2d. mein fehler: die mission ging versehentlich an die abnahme-sitzung; ruecknahme zugestellt.

Candidate at Owner's hop head ecff7e2f575fb991fbe5c3c1c5f6785569d70228 on develop d1acf3f31a36 (back=0), exact hosted run 44940738791 completed/success. Lane 47ffdde2 obeyed the stop order, pushed nothing (handoff evidence 6408d1301), so the lane is no longer active and the card moves to review. Content: valkey dashboard availability query label + honest unavailable/verified contract.

review -> wait: verdict REQUEST CHANGES measured at ecff7e2f575, no live session can currently write the branch (spawn admission hold, tooling issue #6)
