---
id: t-20261114-r28-perses-dashboards
card_number: "0428-082"
card_short_title: "Perses Infra dashboards"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w208-0428-082-dashboards
kanban_status: closed
kanban_lane: closed
kanban_summary: Create native Perses infrastructure dashboards with verified metrics and explicit missing-signal behavior.
kanban_title: 0428-082 · Perses Infra dashboards
priority: normal
depends_on: [t-20261114-r28-perses-dashboard-selection, t-20261114-r28-perses-datasources]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1665]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44895755773", "https://github.com/mcpdev80/baseharbor/pull/1665"]
---

- [x] t-20261114-r28-perses-dashboards · Perses infrastructure dashboards #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** w208-0428-082-dashboards · **Priority:** normal  
    **PR:** [baseharbor#1665](https://github.com/mcpdev80/baseharbor/pull/1665)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44895755773), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1665)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-dashboard-selection](t-20261114-r28-perses-dashboard-selection.md), [t-20261114-r28-perses-datasources](t-20261114-r28-perses-datasources.md)  
**Required by:** [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** w208-0428-082-dashboards  
**Priority:** normal  
**PRs:** [baseharbor#1665](https://github.com/mcpdev80/baseharbor/pull/1665)  
**Source:** 
<!-- /generated:links -->

## Goal

Create native Perses infrastructure dashboards with verified metrics and explicit missing-signal behavior.

## Scope and file ownership

Own infrastructure dashboard assets only, preserve separate data sources. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/metrics/prometheus.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus.go)
- [internal/metrics/prometheus_render.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_render.go)
- [internal/metrics/prometheus_verify.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_verify.go)

Deliver a real first infrastructure dashboard, not merely a framework. Based on verified fixture, include application/provider scrape readiness such as existing `up` series with proper labels, visible time range and explicit no-data. Execute at least one real Prometheus query and validate the versioned Perses dashboard spec.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Create native Perses infrastructure dashboards with verified metrics and explicit missing-signal behavior.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-dashboards](t-20261113-r28-grafana-dashboards.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

## Owner decision — 2026-11-18 (takeover)
Proceed directly after the 083-ready decision: once 083+080 are in develop, rebase #1665 onto active develop, prove Security/Authorization and exact-head checks, independent review; continue only on green + acceptance evidence. No release-gate shortening.

Independent read-only review of PR #1665 / 0428-082 (2026-11-19): draft, no exact-head CI, stacked on old #1684 branch and includes shared datasource files. Dashboard labels host resource panels while queries return scrape statistics; probe calls discard context. See [review evidence](../evidence/r28-welle4-2026-11-19/codex-review-wave/1665-0428-082-independent-review.md).

SITZ W208 AUF IHRER KARTE - ZWEI PFLICHTSCHRITTE, BEIDE VON MIR VORGEBEREITET: (1) #1665 ist draft=true (gemessen), und ein draft hat KEINE required-zellen; undraft geht NUR mit 'gh api -X POST repos/mcpdev80/baseharbor/pulls/1665/mark_ready' (mein altes PATCH -f draft=false-rezept war unwirksam, tooling-issue #12 offen). (2) ihre basis-lane ist weitergelaufen: refs/pull/1684/head = b71c6da27e8b, und #1684 sitzt auf #1724 (408b18d2dc7b) - sie stapeln damit auf der kette 177 -> 083 -> 082, genau wie §3.3.8 (warten auf INHALTE, nie auf merges). branch auf refs/pull/1684/head rebasieren, ancestry-beweis in die akte; PR-base bleibt refs/heads/w083-perses-datasources. write-set bleibt internal/metrics/prometheus*.go; die 076-da-teien (internal/metrics/perses_dashboards*.go + testdata/perses-dashboards/) sind fertig in #1597 und dort nur lesbar; internal/logs/** ist gerade 0428-202 (sitz w207). cli-zellen rot = 0428-198, packages-zelle rot = 0428-202 (neu: fehlendes client-cert.pem im fixture, KEINE owner-entscheidung) - beide nur benennen, nicht nachstellen.

BASIS-ARTEFAKT GEMESSEN, NICHT SCOPE-FEHLER DER LANE: #1665 zeigt 333 dateien inkl. gesperrter rails (internal/capability/perses_selection.go, internal/identityprovider/**, 5 dateien unter .github/workflows/), WEIL die PR-base auf refs/heads/w083-perses-datasources = ed55d893374b zeigt, die 083-lane aber auf refs/heads/lane-0428-083-datasources-r2 = b71c6da27e8b veroeffentlicht. Ihr head db27880c108a sitzt sauber auf 408b18d2 (177) -> b71c6da2 (083). w208 hat den retarget-befehl ('gh api -X PATCH .../pulls/1665 -f base=lane-0428-083-datasources-r2') + die auflage, rail-freiheit der dateiliste VOR dem undraft selbst zu belegen; die draft-sweep-aussage 'undraft-faehig NEIN wegen rail-beruehrung' ist damit fuer #1665 ueberholt.

handoff abgeschlossen, ABER DIE PLATTFORM SAGT NEIN ZU NICHT-entwick-basen: #1665 hat jetzt base refs/heads/lane-0428-083-datasources-r2 und 14 dateien (der 333-dateien-zustand ist WEG, mein retarget hat also gewirkt), 13 tests bestehen lokal. die required-zellen koennen auf dieser base NICHT laufen: gemessen am head db27880c108a = 3 success / 7 failure / 48 skipped / 2 cancelled, und die fehlgeschlagenen namen sind 'PR · Draft Go · cli-0/1/3', 'Workflow policy', 'PR Trusted Plan', 'PR Selected Checks' - das workflow-triggerschluesselwort haengt am base-ref, nicht am draft-flag (der PR ist draft=false, gemessen). DARUM wait statt review: die karte wartet auf den MERGE ihrer basis-lane (#1724 -> #1684), nicht auf inhaltlichen vorgaengern. TRIGGER FUER DIE NAechSTE KANTE: #1684 ist auf develop, dann base zurueck auf develop, ein exact-head-CI, dann abnahme. KEIN rerun von der lane aus (§3.8). ZWISCHENZEIT wird eine neue regeskarte daraus, ob gestapelte PRs im fenster ueberhaupt required-zellen bekommen duerfen - das ist ein .github/**-thema beim owner.


## Completion — 2026-11-21

Implemented via #1665 at e84e434bc1b49ce43a1c48041312242c8a56a981; exact PR run 44895755773 passed, merge commit 77c1e60f51b91003ac3ddc391008c15e4a713a5c. Full test-to-gate evidence: [closeout record](../evidence/closeouts/0428-082-176-2026-11-21.md).
