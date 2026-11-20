---
id: t-20261114-r28-perses-dashboard-databases
card_number: "0428-076"
card_short_title: "Perses database dashboards"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w202-0428-076-dbpanels
kanban_status: active
kanban_lane: active
kanban_summary: Deliver PostgreSQL/MongoDB panels only when verified compatible metrics and permissions exist.
kanban_title: 0428-076 · Perses database dashboards
priority: normal
depends_on: [t-20261114-r28-perses-dashboard-selection]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1597]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-perses-dashboard-databases · Perses database dashboards #task #release/v0-4-28 #status/active #view/active #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** w202-0428-076-dbpanels · **Priority:** normal  
    **PR:** [baseharbor#1597](https://github.com/mcpdev80/baseharbor/pull/1597)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-dashboard-selection](t-20261114-r28-perses-dashboard-selection.md)  
**Required by:** [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** w202-0428-076-dbpanels  
**Priority:** normal  
**PRs:** [baseharbor#1597](https://github.com/mcpdev80/baseharbor/pull/1597)  
**Source:** 
<!-- /generated:links -->

## Goal

Deliver PostgreSQL/MongoDB panels only when verified compatible metrics and permissions exist.

## Scope and file ownership

Own database dashboard assets and focused tests. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/capability/reference.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/capability/reference.go)
- [internal/application/provider_registry.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/application/provider_registry.go)
- [internal/metrics/prometheus_files.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_files.go)

Create first PostgreSQL/MongoDB panels using only verified actual exporters/labels. Each unsupported database must remain explicitly unavailable; no silent exporter install. Validate real data/no-data per supported fixture.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Deliver PostgreSQL/MongoDB panels only when verified compatible metrics and permissions exist.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-dashboard-databases](t-20261113-r28-grafana-dashboard-databases.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

delivered: head 2e5f8703, ci dispatcht, base-parity-lauf laeuft

Independent read-only review of PR #1597 / 0428-076 (2026-11-19): draft/dirty, stale base, 23 commits/31 files including selection work outside scope; only draft feedback ran and workflow-dispatch validation failed at ORAS setup. Found Tempo service.name mismatch, unresolved Prometheus dashboard variables, Loki query label mismatch and unsorted aggregate JSON map. See [review evidence](../evidence/r28-welle4-2026-11-19/codex-review-wave/1597-0428-076-independent-review.md).

ARBEITET JETZT, kante gegen session gemessen (w202-0428-076-dbpanels, 1f393616, ornith, worktree aus develop 40cb28c758b0). ZWEI TEILE, ein kandidat: (A) PR-hygiene, gemessen: #1597 head 540ed13cec36 (16.11. 06:24) sitzt NICHT auf develop ('git merge-base --is-ancestor 40cb28c758b0 <head>' = NEIN), draft=TRUE, checks 7 success / 1 failure / 48 skipped, die fehlerzelle heisst 'validate'. befohlen: rebase auf develop-spitze, force-with-lease auf den EIGENEN lane-branch perses-dashboard-databases-lane, 'gh api -X PATCH .../pulls/1597 -f draft=false', body/titel mit kartennummer + head-sha + aktenpfad, KEIN zweiter PR (gh pr list --head vorher). (B) DIE PRODUKTFRAGE DER KARTE bleibt: PostgreSQL-/MongoDB-panels NUR bei verifizierten metrics UND berechtigungen am AKTUELLEN develop (der kartentext referenziert cd77e20e - nachmessen, nicht glauben); nicht unterstuetzte datenbanken muessen ausdruecklich abwesend/unknown bleiben, ein panel das daten erfindet ist ein fehler. regression pro fall ueber die echte oberflaeche; hosted run am exakten head selbst beobachten (§4.6); gateway-faelle (cli-0..3/packages) = feld-gate 0428-198/0428-202, nicht ihr diff. schreibfeld: internal/metrics/prometheus_files.go + perses_dashboards*, internal/capability/reference.go, internal/application/provider_registry.go, cmd/baha/app_status_result.go, docs/spec/**. disjunkt gehalten zu w203-0428-143 (prometheus_verify.go + integration_contract.go) und zu den ruhenden lanes #1684/#1724. akte: evidence/r28-welle4-2026-11-20/perses-database-panels/round-1.md, nummerierte zeilen (keine checkboxen - die blockieren die board-publikation).
