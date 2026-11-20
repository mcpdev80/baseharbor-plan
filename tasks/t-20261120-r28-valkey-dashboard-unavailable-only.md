---
id: t-20261120-r28-valkey-dashboard-unavailable-only
card_number: "0428-183"
card_short_title: "valkey dashboards gate"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w183-0428-183-valkeygate
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-183 · valkey dashboards gate
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1714]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md"]
---

- [ ] t-20261120-r28-valkey-dashboard-unavailable-only · Perses: new DB/Valkey dashboards reachable only as DashboardUnavailable #task #release/v0-4-28 #status/active #view/active #kind/bug
    <!-- generated:card -->
    **Owner:** w183-0428-183-valkeygate  
    **PR:** [baseharbor#1714](https://github.com/mcpdev80/baseharbor/pull/1714)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w183-0428-183-valkeygate  
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
