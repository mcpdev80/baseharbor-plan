---
id: t-20261114-r28-perses-runtime
card_number: "0428-088"
card_short_title: "Launch optional Perses"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: 0428-088 fenster-hopf (codeman a9212508-20e3-43f8-8234-b40426e56dab, ornith)
kanban_status: active
kanban_lane: active
prs: [mcpdev80/baseharbor#1592]
kanban_summary: "Implement explicitly enabled optional Perses runtime, pinned reviewed image/plugin versions, lifecycle and safe storage using…"
kanban_title: 0428-088 · Launch optional Perses
priority: normal
depends_on: [t-20261114-r28-perses-contract-seam]
repos: [mcpdev80/baseharbor]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1592-r3-runtime.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/perses-runtime/r4-1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44467712113", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1592-host-witness-review.md", "https://github.com/mcpdev80/baseharbor-plan/blob//evidence/r28-welle4-2026-11-19/codex-review-wave/1592-0428-088.md"]
---

- [ ] t-20261114-r28-perses-runtime · Launch optional Perses #task #release/v0-4-28 #status/active #view/active #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** 0428-088 fenster-hopf (codeman a9212508-20e3-43f8-8234-b40426e56dab, ornith) · **Priority:** normal  
    **PR:** [baseharbor#1592](https://github.com/mcpdev80/baseharbor/pull/1592)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1592-r3-runtime.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/perses-runtime/r4-1.md), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44467712113), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1592-host-witness-review.md), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob//evidence/r28-welle4-2026-11-19/codex-review-wave/1592-0428-088.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-contract-seam](t-20261114-r28-perses-contract-seam.md)  
**Required by:** [t-20261114-r28-perses-datasources](t-20261114-r28-perses-datasources.md), [t-20261114-r28-perses-lifecycle](t-20261114-r28-perses-lifecycle.md), [t-20261114-r28-perses-loki-source](t-20261114-r28-perses-loki-source.md), [t-20261114-r28-perses-secure-access](t-20261114-r28-perses-secure-access.md), [t-20261114-r28-perses-tempo-source](t-20261114-r28-perses-tempo-source.md)  
**Owner:** 0428-088 fenster-hopf (codeman a9212508-20e3-43f8-8234-b40426e56dab, ornith)  
**Priority:** normal  
**PRs:** [baseharbor#1592](https://github.com/mcpdev80/baseharbor/pull/1592)  
**Source:** 
<!-- /generated:links -->

## Goal

Implement explicitly enabled optional Perses runtime, pinned reviewed image/plugin versions, lifecycle and safe storage using the existing runtime/provider seam.

## Scope and file ownership

Own dedicated Perses runtime assets and tests; do not provision unrelated telemetry backends. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/providerui/application.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/providerui/application.go)
- [internal/metrics/prometheus_render.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_render.go)
- [internal/metrics/prometheus_files.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_files.go)
- [internal/deployment/runtime_provider.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/deployment/runtime_provider.go)

Use the accepted seam to implement an opt-in owned Perses runtime with verified immutable image and required plugin availability, protected persistent/config state and real readiness. Normal applications must not create Perses. Missing image/security policy must fail closed. Add removal/restart/foreign-owner tests.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Implement explicitly enabled optional Perses runtime, pinned reviewed image/plugin versions, lifecycle and safe storage using the existing runtime/provider seam.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-runtime](t-20261113-r28-grafana-runtime.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

kandidat e264ca4b7, exact-head run 44403933672 SUCCESS, TLS material generiert+projiziert via command override, regression TestPersesTLSFilesProjectedAndConsumed; BEHIND gegen 8dccd4fe1 => hopf in der merge-welle

r2 plugin-extract: kandidat 54fbe4771, exact-head run 44420115459 SUCCESS, /etc/perses/plugins writable tmpfs unter read_only:true, TestPersesRuntimeSmokeDockerIsolated verschaerft -> GET /api/v1/plugins meldet shipped UI plugin

board-wahrheit: Codex haelt REQUEST CHANGES auf 54fbe4771 aufrecht (letzter recheck 00:01Z, comment am PR) — die 088-lane hat danach keinen neuen head gestellt und ist released. r3-mission wird beim naechsten END-freiraum aus dem PR-kommentar-rezept geschnitten und dispatched. review-status war damit nicht mehr zutreffend -> active

r3 END akzeptiert: runtime-zeug PASS (32/32 module via /api/v1/plugins, tmpfs+read_only beide koepfe), monotoner hopf c452f705c normal gepusht, exact-head run 44456253144 SUCCESS selbst beobachtet, akte 4b271bf9. OWNER-FIND: scripts/pr-gate-coverage.json:60-63 ohne perses-gate, kein workflow setzt BASEHARBOR_PERSES_RUNTIME_SMOKE — dauerloesung beim owner. Routing an CODEX (rezept-punkt 'nicht falsifiziert zur laufzeit' damit erfuellebt)

hopf-route berichtigt: rebase unbrauchbar, weil der branch develop-merge-commits traegt und der 075-seam-ahn (4bab986dc) schon auf develop liegt — rebase spielt integrierte history neu ab. merge-hopf angewiesen, PR-head bleibt bis zum neuen head c452f705c, karte bleibt review (basisarbeit, kein inhaltsschritt)

base-exakt: merge-hopf auf develop 21161b101, head 76331c7d8, PR #1592 clean, inhalt byte-identisch (diff-vs-diff-belege in r4-1.md), CI-CP #5653 SUCCESS — abnahme kann auf diesem head urteilen

CODEX-REVIEW current-head recheck: #1592 head 76331c7d8, base develop 21161b101; exact-head Source & Quality 44467712113 SUCCESS. r4-1 proves Perses content byte-identical across hopfs. Hold remains: no exact-current-head Docker witness and TestPersesRuntimeSmokeDockerIsolated has no mapped/selected CI/native gate (BASEHARBOR_PERSES_RUNTIME_SMOKE unset). 32/32 plugin witness was on c452f705c, so cannot stand in for current-head execution. No merge pending exact-head runtime witness and owner-approved gate mapping/disposition. GitHub review API rejected REQUEST_CHANGES because connected identity authored PR; equivalent finding posted as PR issue comment 7001328277.

hopf-arbeit abgeschlossen (merge auf develop 21161b101, head 76331c7d8), abnahme hebt stale review — kein merge bis zelle gemapped ist

hopf-stand: 76331c7d8 = merge auf develop da76c5cf9 (inhalt byte-identisch, r4-1.md), PR #1592 open behind (entwickelt sich mit naechstem merge)

host witness beigebracht (exact head 76331c7d83055f821fa1e6ff21c1cc37d9a08ae9, branch-ref gezeugt): BASEHARBOR_PERSES_RUNTIME_SMOKE=1 go test ./internal/application -run '^TestPersesRuntimeSmokeDockerIsolated$' -> PASS, multiple runs 19.32/25.99/14.50/22.24/8.39s plus cross-check worktree 11.80s; develop da76c5cf9 meldet 'no tests to run' (der test existiert nur auf dem kandidaten, bestaetigt audit 0428-133 fund 2). akte perses-runtime/witness-1.md commit ebf15c9f (ancestor von origin/main). PR #1592 open behind (basis hat sich bewegt, inhalt unchanged, hopf r4-1.md). hosted smoke-zelle bleibt owner-scope 0428-114 — nach praezedenz 088-r3 gilt der host witness als zeuge, wenn genau dieser fehlende draht als owner-befund dokumentiert ist; das ist er. daher: review statt blocked

CODEX-REVIEW welle 4 = ACCEPT (urteilsdatei 1592-0428-088.md): inhalt + running evidence auf exaktem kopf, KEIN merge in dieser welle. kopf: 088 76331c7d83055f821fa1e6ff21c1cc37d9a08ae9 (lauf 44467712113 SUCCESS + host-zeuge 5x), 086 7d6538b45cac40f4e8fa0de8aa97fcede7893e6c (lauf 44052892273 SUCCESS, mergeable 'behind'). karte bleibt review, weil der zustand 'accepted' in diesem schema nicht existiert — die abnahme ist durch die urteilsdatei belegt, der merge folgt im fenster, danach closed

urteil ACCEPT galt 76331c7d83055f821fa1e6ff21c1cc37d9a08ae9; develop ist jetzt e1dc2cf61 (#1691 squash-merged), der ast ist 'behind' und 'merge-base --is-ancestor e1dc2cf61 <kopf>' fehlt — darum hopf + frischer exact-head-lauf + NEUES urteil auf dem neuen kopf (§5.2, urteil uebertraegt nicht). ZUSAMMENHANG, den ich dokumentiere: 0428-083 haengt an dieser karte, weil internal/application/perses_runtime.go NUR auf dem 088-ast existiert (cat-file -e fehlt fuer develop, e1dc2cf61, a9befb312, f0adef107) — 083 hat recht mit seiner scope-warnung und ich habe (b) befohlen: nicht forken, nach meinem 088-merge rebasen und dann aufruf-stelle + mounts + docker-runtime-test liefern
