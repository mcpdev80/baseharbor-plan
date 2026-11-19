---
id: t-20261114-r28-perses-datasources
card_number: "0428-083"
card_short_title: "Connect Perses Prometheus"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: 0428-083 lane (codeman 5447f0df, flash) — END angenommen, basis-hopf ausstehend
kanban_status: active
kanban_lane: active
kanban_summary: Provision authorized existing Prometheus datasource in Perses using supported pinned native plugin and proxy/TLS contract.
kanban_title: 0428-083 · Connect Perses Prometheus
priority: normal
depends_on: [t-20261114-r28-perses-contract-seam, t-20261114-r28-perses-runtime, t-20261114-r28-perses-signal-inventory]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1608, mcpdev80/baseharbor#1684]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1684-0428-083.md", "https://github.com/mcpdev80/baseharbor-plan/blob/5010af27b84c1542be14022823cfaa3a645ac4d3/evidence/r28-welle4-2026-11-19/codex-review-wave/1684-0428-083-r2.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44573407736"]
---

## Owner decision — 2026-11-17

Owner decision (2026-11-17): Unblock. Reopen PR #1608 if it remains suitable, otherwise create a superseding PR on develop. Restore the Prometheus datasource integration and rebase PR #1665 onto an actively CI-covered base. Run the applicable exact-head CI and security/authorization checks before review and merge. No merge is authorized solely by this decision.

- [ ] t-20261114-r28-perses-datasources · Connect Perses Prometheus #task #release/v0-4-28 #status/active #view/active #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** 0428-083 lane (codeman 5447f0df, flash) — END angenommen, basis-hopf ausstehend · **Priority:** normal  
    **PR:** [baseharbor#1608](https://github.com/mcpdev80/baseharbor/pull/1608), [baseharbor#1684](https://github.com/mcpdev80/baseharbor/pull/1684)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1684-0428-083.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/5010af27b84c1542be14022823cfaa3a645ac4d3/evidence/r28-welle4-2026-11-19/codex-review-wave/1684-0428-083-r2.md), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44573407736)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-contract-seam](t-20261114-r28-perses-contract-seam.md), [t-20261114-r28-perses-runtime](t-20261114-r28-perses-runtime.md), [t-20261114-r28-perses-signal-inventory](t-20261114-r28-perses-signal-inventory.md)  
**Required by:** [t-20261114-r28-perses-alerts](t-20261114-r28-perses-alerts.md), [t-20261114-r28-perses-dashboards](t-20261114-r28-perses-dashboards.md)  
**Owner:** 0428-083 lane (codeman 5447f0df, flash) — END angenommen, basis-hopf ausstehend  
**Priority:** normal  
**PRs:** [baseharbor#1608](https://github.com/mcpdev80/baseharbor/pull/1608), [baseharbor#1684](https://github.com/mcpdev80/baseharbor/pull/1684)  
**Source:** 
<!-- /generated:links -->

## Goal

Provision authorized existing Prometheus datasource in Perses using supported pinned native plugin and proxy/TLS contract.

## Scope and file ownership

Dedicated Prometheus datasource adapter/tests; no new Prometheus instance or invented metrics. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/metrics/prometheus.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus.go)
- [internal/metrics/prometheus_files.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_files.go)
- [internal/metrics/prometheus_verify.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_verify.go)
- [internal/serviceaccess/policy.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/serviceaccess/policy.go)

Use Perses PrometheusDatasource native versioned spec with existing authorized metrics endpoint, CA and credentials via proxy as supported; test actual query plus unauthorized/cross-target denial and no secret in descriptors.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Provision authorized existing Prometheus datasource in Perses using supported pinned native plugin and proxy/TLS contract.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-datasources](t-20261113-r28-grafana-datasources.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

## Owner decision — 2026-11-18 (takeover)
Card is ready to work after the 2026-11-17 unblock. Precondition per owner: 083 AND 080 must land on develop before #1665 continues (080 already merged via #1590). Deliver 083 on a fresh branch + one PR per card rule (#1608 stays closed).

kandidat auf branch lane-0428-083-datasources-r2 von develop 907f16713; 19 test cells PASS; CI run 44398435160 SUCCESS exact-head; fail-closed golden test

hopf-runde angesetzt (PR #1684 war 'behind', draft=false). schreibset ist DISJUNKT zu 0428-084 (von mir gemessen: keine gemeinsame datei zwischen refs/pull/1684 und refs/pull/1598 gegen develop) — daher parallel erlaubt. mission traegt die fenster-lerneffekte: merge-hopf statt rebase, doc-classifier-pflicht VOR push (praezedenz 084: unclassified product command), readability-audit, jobliste + skipped-gruende, frischer isolierter clone

hopf delivered und verifiziert: branch lane-0428-083-datasources-r2 = ab6932296, MONOTON auf develop da76c5cf9, merge-tree 0 konflikte, PR #1684 open/draft=false/clean, exact-head lauf 445… completed SUCCESS (von mir per gh api auf den exakten kopf gelesen). schreibset war disjunkt zu 0428-084 (comm -12 der dateimengen = leer), parallel war damit erlaubt

END akzeptiert, sitz entlassen: head ab6932296f1f24c2024810f10b155633d931f7d4, monoton auf develop da76c5cf9, merge-tree 0 konflikte, exact-head run 44505333646 completed SUCCESS mit NULL fehljobs (von mir per gh api auf jobs geprueft, nicht nur der lauf-status), PR #1684 open/draft=false/clean. akte perses-datasources-hopf/fix-1.md von mir aus der gemeinsamen kopie gesichert und gepusht (board 79cc02a1)

CODEX-REVIEW welle 4 = REQUEST CHANGES auf dem gepueften kopf (urteil 1684-0428-083.md). korrekture-runde ist vorgemerkt und wartet auf einen freien sitz: die vier perses-karten und 083 teilen sich dateien mit den laufenden lanen, darum kein paralleler start ohne write-set-nachweis. 083: 'runtime provisioning absent' (datasource wird gebaut, aber nicht in Perses bereitgestellt); 073: 'alert rule nicht ausgefuehrt/nicht persistiert' (persesAlertRealEvaluation); 077: 'catalog-availability aus host provider-metrics allein'; 089: 'PersesComposeServices rendert keine config (--config=/etc/perses/config.yaml) + loopback upstream'

REQUEST CHANGES abgeholt: datasource muss im laufenden Perses erscheinen (runtime provisioning), nicht nur als builder/golden-artefakt; branch lane-0428-083-datasources-r2 @ ab6932296, write-set gegen 121/057/110 gemessen disjunkt

korrektur-runde abgeliefert, von mir qualifiziert: branch lane-0428-083-datasources-r2 = f0adef107, monoton auf dem NEUEN develop e1dc2cf61, merge-tree 0 konflikte, PR open/draft=false/clean, exaktkopf-lauf 44520439061 completed SUCCESS (0 fehljobs, 33 ausgefuehrte zellen, 'PR Selected Checks' success). akte perses-datasources-hopf/fix-2.md auf origin/main. CODEX-REVIEW fuer diesen kopf beauftragt (urteil 1684-0428-083-r2.md); merge erst in meinem fenster

URTEIL AUF f0adef107 = REQUEST CHANGES ('runtime consumer and mounts absent / no merge'), von mir gegen deinen neuen kopf nachgerechnet: a9befb3127b26a8a0f622bcf686fb6bcbb9b9e6e unterscheidet sich von f0adef107 um GENAU EINE datei (internal/metrics/perses_prometheus_datasource_runtime.go), und 'MaterializePersesPrometheusDatasourceAt' taucht dort nur in internal/metrics/*_runtime.go + seiner eigenen test-datei auf, in internal/application/ nirgends — die aufruf-stelle fehlt also weiter. monotoner stack ist OK (e1dc2cf61 ancestor, f0adef107 ancestor), PR draft=false/blocked, lauf 44522363321 in_progress, aber der ist nicht die qualifying stelle. befehl an dieselbe lane: (1) aufruf an der echten apply-grenze in internal/application/perses_runtime.go VOR dem Perses-start, (2) read-only compose-mounts aus dem materializer-ergebnis (config-/datenpfade, kein zweite konstante), (3) isolierter Docker-runtime-test mit gepinntem image, der das LADEN der GlobalDatasource zeigt + query/proxy/TLS, zelle muss AUSGEFUEHRT statt skipped sein (sonst befuind an den owner mit datei:zeile der skip-bedingung, nicht selbst aendern), (4) grep-beleg vor push, (5) akte fix-3.md mit matrix

ENTBLOCKT durch den #1592-merge (develop 3b634232f): internal/application/perses_runtime.go ist jetzt in develop, also ist die aufruf-stelle folge-arbeit und kein fork von 088s kandidat. mission verlangt: aufruf an der apply-grenze vor dem Perses-start, read-only compose-mounts aus dem materializer-ergebnis, isolierter Docker-runtime-test (zelle muss laufen, sonst skip-bedingung als befuind + host-zeugen-praezedenz)

END ANGENOMMEN, alle zeugen von mir gegen gelesen: zweig-head 24cd5f4538fa8f9bc814fcd481143484742c3a14, base = develop c296086ca (der #1616-merge), PR non-draft, merge-tree gegen develop 0 konflikte, lauf 44573407736 completed SUCCESS created 17:05:46Z auf GENAU DIESEM kopf; akte evidence/r28-welle4-2026-11-19/perses-datasources-hopf/fix-4.md (main b01fb21d, blob c0113b26). DER EINE GRUND, WARUM SIE NICHT AUF REVIEW GEHT: der owner hat um 18:19:51+01:00 #1581 gemergt, develop ist 7ee6f817dbff5a238bbc651315d6d76b3819fc91, und der unterschied c296086ca -> 7ee6f817d betrifft scripts/test_pr_gate_plan.py + scripts/ci-workflow-policy.sh — scripts/test_pr_* ist ein treffer meiner base-abstands-regel, also schuldet die lane EINEN monotonen hopf auf 7ee6f817d plus EINEN exact-head-lauf. Kein inhalt zweifelt daran: die drei teile (apply-grenze runtime_postgres.go:140 -> ensurePersesDatasourceRuntime, read-only compose-mounts resolver-abgeleitet perses_runtime.go:99 fail-closed, container-akzeptanz-test lokal 3x gruen) sind geliefert. IHR BEFUND ist notiert und geht in die owner-draht-liste: 'PR Selected Runtime' skipped, skip-kette ci.yml:973 runtime_required=false <- pr-selected-runtime-matrix.py <- pr-gate-plan.py ohne mapping fuer perses/apply-pfade (owner-scope, von der lane NICHT geaendert) — nach dem hopf prueft sie, ob #1581 ihren fall schon abbildet
