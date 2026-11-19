---
id: t-20261114-r28-perses-dashboard-hosts
card_number: "0428-077"
card_short_title: "Perses host and container"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: 0428-077 r2 (END akzeptiert, sitz entlassen)
kanban_status: closed
kanban_lane: closed
kanban_summary: "Deliver host/container panels only for actually available matching metrics, without adding privileged exporters."
kanban_title: 0428-077 · Perses host and container
priority: normal
depends_on: [t-20261114-r28-perses-dashboard-selection]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1602]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1602-0428-077.md", "https://github.com/mcpdev80/baseharbor-plan/blob/1731df3a6d1eddcf1541d44435f687b5890c068b/evidence/r28-welle4-2026-11-19/dashboard-hosts-hopf/fix-2.md", "https://github.com/mcpdev80/baseharbor/pull/1602", "https://github.com/mcpdev80/baseharbor/actions/runs/44530337283", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-review-wave/1602-0428-077-r2.md", "https://github.com/mcpdev80/baseharbor-plan/blob/c2a4c6b5960ba343126486ff8cc25e0eecb6bd27/evidence/r28-welle4-2026-11-19/codex-review-wave/1602-0428-077-r2.md"]
---

- [x] t-20261114-r28-perses-dashboard-hosts · Perses host and container dashboards #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** 0428-077 r2 (END akzeptiert, sitz entlassen) · **Priority:** normal  
    **PR:** [baseharbor#1602](https://github.com/mcpdev80/baseharbor/pull/1602)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1602-0428-077.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/1731df3a6d1eddcf1541d44435f687b5890c068b/evidence/r28-welle4-2026-11-19/dashboard-hosts-hopf/fix-2.md), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1602), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44530337283), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-review-wave/1602-0428-077-r2.md), [proof 6](https://github.com/mcpdev80/baseharbor-plan/blob/c2a4c6b5960ba343126486ff8cc25e0eecb6bd27/evidence/r28-welle4-2026-11-19/codex-review-wave/1602-0428-077-r2.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.28  
**Depends on:** [t-20261114-r28-perses-dashboard-selection](t-20261114-r28-perses-dashboard-selection.md)  
**Required by:** [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** 0428-077 r2 (END akzeptiert, sitz entlassen)  
**Priority:** normal  
**PRs:** [baseharbor#1602](https://github.com/mcpdev80/baseharbor/pull/1602)  
**Source:** 
<!-- /generated:links -->

## Goal

Deliver host/container panels only for actually available matching metrics, without adding privileged exporters.

## Scope and file ownership

Own host/container dashboard assets and focused tests. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/metrics/prometheus_render.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_render.go)
- [internal/metrics/prometheus_files.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_files.go)

Create first host/container dashboard only for verified existing host signals; if no authorized source, show actionable no-data, not fabricated healthy CPU/RAM. Include native dashboard fixture/schema and real query when fixture provides signals.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Deliver host/container panels only for actually available matching metrics, without adding privileged exporters.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-dashboard-hosts](t-20261113-r28-grafana-dashboard-hosts.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

akte dff7d9d5

kandidat a4d0c3cb (echter merge-durchlauf, FF-push, run 44049875883 SUCCESS, mergeable unknown=>neu bestimmen)

CODEX-REVIEW welle 4 = REQUEST CHANGES auf dem gepueften kopf (urteil 1602-0428-077.md). korrekture-runde ist vorgemerkt und wartet auf einen freien sitz: die vier perses-karten und 083 teilen sich dateien mit den laufenden lanen, darum kein paralleler start ohne write-set-nachweis. 083: 'runtime provisioning absent' (datasource wird gebaut, aber nicht in Perses bereitgestellt); 073: 'alert rule nicht ausgefuehrt/nicht persistiert' (persesAlertRealEvaluation); 077: 'catalog-availability aus host provider-metrics allein'; 089: 'PersesComposeServices rendert keine config (--config=/etc/perses/config.yaml) + loopback upstream'

REQUEST-CHANGES-runde dispatched. zweig 'behind' -> hopf auf develop e1dc2cf61 ist schritt 1. write-set-klausel: internal/capability/perses.go + internal/metrics/perses_contract_test.go geteilt mit dem 084-zweig (comm -12 gemessen) — fuer beide gilt SCHREIB-VERBOT + stop/meldung, damit kein paralleles schreiben entsteht. gegen die lanen 122 und 088 ist der schreibset disjunkt (077 vs 088: leer)

END akzeptiert, qualifiziert: head 9f5470f97a112a6dae226712d63731676775b405, monoton auf develop 3b634232f (zwei hopfs), b6c9702ba ist ancestor, merge-tree 0 konflikte, PR open/draft=false/clean, exaktkopf-lauf 44530337283 completed SUCCESS (0 fehljobs, 15 ausgefuehrte zellen, 'PR Selected Checks' success). rezept belegt: internal/logs/render.go:145/163/296 ('target_label = "baseharbor_provider"'), internal/telemetry/otlp_payload.go:28 ('baseharbor.provider'), internal/metrics/perses_dashboards_hosts.go:90/216/243-245 (unavailable-kind + begruendung), neue matrix mit 'Prometheus gesund, Loki ohne signal -> Loki unavailable'. CODEX-REVIEW beauftragt (1602-0428-077-r2.md), bei approve merge. FOLGE-KARTE angelegt fuer die von ihr gemeldete grenze (echte backend-witness im CLI-gesicht braucht cmd/baha/app_status_result.go)

CODEX-REVIEW approved candidate 9f5470f97a112a6dae226712d63731676775b405; CODEX-MERGE squash merge 5a68196a1e6bf627fbd8e17f106d58f1e63f6ce6. Exact-head run 44530337283 passed PR Selected Checks; runtime and Core-less jobs were skipped and are not claimed as passes.

GEMERGT: CODEX-REVIEW 'APPROVE — exact head 9f5470f97a112a6dae226712d63731676775b405' (run 44530337283 SUCCESS) + 'END_APPROVE … backend availability is fail-closed per backend', merge-receipt: squash-merged 13:25:17Z, merge-commit = neuer develop 5a68196a1e6bf627fbd8e17f106d58f1e63f6ce6 (linear, 3b634232f ist ancestor). squashed (head kein ancestor), ALSO datei-hash-zeug: alle 14 diff-dateien zwischen kandidat und develop identisch, abweichend: 0
