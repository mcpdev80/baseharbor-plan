---
id: t-20261120-r28-valkey-dashboard-unavailable-only
card_number: "0428-183"
card_short_title: "valkey dashboards gate"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: 0428-183-hopdev
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-183 · valkey dashboards gate
priority: ""
depends_on: [t-20261121-loki-verify-probe, t-20261120-r28-cli-shard-operator-env]
repos: [mcpdev80/baseharbor]
prs: ['mcpdev80/baseharbor#1714']
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md", "https://github.com/mcpdev80/baseharbor/pull/1734", "https://github.com/mcpdev80/baseharbor/actions/runs/44853938826"]
---

- [ ] t-20261120-r28-valkey-dashboard-unavailable-only · Perses: new DB/Valkey dashboards reachable only as DashboardUnavailable #task #release/v0-4-28 #status/active #view/active #kind/bug
    <!-- generated:card -->
    **Owner:** 0428-183-hopdev  
    **PR:** [baseharbor#1714](https://github.com/mcpdev80/baseharbor/pull/1714)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1734), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44853938826)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261121-loki-verify-probe](t-20261121-loki-verify-probe.md), [t-20261120-r28-cli-shard-operator-env](t-20261120-r28-cli-shard-operator-env.md)  
**Owner:** 0428-183-hopdev  
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
