---
id: t-20261114-r28-perses-loki-source
card_number: "0428-086"
card_short_title: "Connect Perses Loki"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w086-0428-086-lokisource (codeman e7dfe31a, laptop) — PR ohne laufende session, von mir neu angesetzt
kanban_status: active
kanban_lane: active
kanban_summary: "Provision selected authorized Loki datasource via supported Perses plugin, scoped and verified."
kanban_title: 0428-086 · Connect Perses Loki
priority: normal
depends_on: [t-20261114-r28-perses-contract-seam, t-20261114-r28-perses-runtime, t-20261114-r28-perses-signal-inventory]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1616]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob//evidence/r28-welle4-2026-11-19/codex-review-wave/1616-0428-086.md"]
---

- [ ] t-20261114-r28-perses-loki-source · Connect Perses Loki #task #release/v0-4-28 #status/active #view/active #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** w086-0428-086-lokisource (codeman e7dfe31a, laptop) — PR ohne laufende session, von mir neu angesetzt · **Priority:** normal  
    **PR:** [baseharbor#1616](https://github.com/mcpdev80/baseharbor/pull/1616)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob//evidence/r28-welle4-2026-11-19/codex-review-wave/1616-0428-086.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-contract-seam](t-20261114-r28-perses-contract-seam.md), [t-20261114-r28-perses-runtime](t-20261114-r28-perses-runtime.md), [t-20261114-r28-perses-signal-inventory](t-20261114-r28-perses-signal-inventory.md)  
**Required by:** [t-20261114-r28-perses-log-trace-dash](t-20261114-r28-perses-log-trace-dash.md), [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** w086-0428-086-lokisource (codeman e7dfe31a, laptop) — PR ohne laufende session, von mir neu angesetzt  
**Priority:** normal  
**PRs:** [baseharbor#1616](https://github.com/mcpdev80/baseharbor/pull/1616)  
**Source:** 
<!-- /generated:links -->

## Goal

Provision selected authorized Loki datasource via supported Perses plugin, scoped and verified.

## Scope and file ownership

Dedicated Loki datasource adapter/tests; retain existing Loki backend. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/logs/driver.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/logs/driver.go)
- [internal/logs/lifecycle.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/logs/lifecycle.go)
- [internal/logs/query.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/logs/query.go)
- [internal/serviceaccess/policy.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/serviceaccess/policy.go)

Use Perses LokiDatasource plugin verified in pinned image. Resolve only authorized existing Loki, establish TLS/auth and execute an actual log query. Test absent/not-ready datasource, denied cross-target and clean removal.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Provision selected authorized Loki datasource via supported Perses plugin, scoped and verified.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-loki-source](t-20261113-r28-grafana-loki-source.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

CODEX-REVIEW welle 4 = ACCEPT (urteilsdatei 1616-0428-086.md): inhalt + running evidence auf exaktem kopf, KEIN merge in dieser welle. kopf: 088 76331c7d83055f821fa1e6ff21c1cc37d9a08ae9 (lauf 44467712113 SUCCESS + host-zeuge 5x), 086 7d6538b45cac40f4e8fa0de8aa97fcede7893e6c (lauf 44052892273 SUCCESS, mergeable 'behind'). karte bleibt review, weil der zustand 'accepted' in diesem schema nicht existiert — die abnahme ist durch die urteilsdatei belegt, der merge folgt im fenster, danach closed

Laptop 2: PR #1616 ist draft=false/state open, aber es lief keine session mehr dazu (karte hing auf review mit owner coord = vorgemerkt, nicht bestaetigt — jetzt berichtigt). write-set disjunkt gemessen: internal/logs/loki_datasource.go, internal/logs/loki_test.go, internal/logs/runtime_log_source_snapshot.go + testdata; merge-tree gegen develop fac01c772 = 0 konflikte. abgrenzung: NICHT internal/metrics/perses_prometheus_datasource* (083 busy), NICHT cmd/baha/** oder docs/cli/** (084/089), NICHT registry.go (123), NICHT cmd/baha/app_status_result.go (reserviert fuer 062/#1614 und 142). inhalt: der loki-adapter muss die echte backend-witness fuer 'perses status' liefern (verfuegbarkeit pro backend, nicht global) — das ist der 077-fund, der bereits auf karte t-20261119-r28-perses-status-backend-witness (0428-142) steht
