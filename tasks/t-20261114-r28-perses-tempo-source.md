---
id: t-20261114-r28-perses-tempo-source
card_number: "0428-091"
card_short_title: "Connect Perses Tempo"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w091-pr0428-091-tempo-source
kanban_status: active
kanban_lane: active
kanban_summary: "Provision selected authorized Tempo datasource via supported Perses plugin, scoped and verified."
kanban_title: 0428-091 · Connect Perses Tempo
priority: normal
depends_on: [t-20261114-r28-perses-contract-seam, t-20261114-r28-perses-runtime, t-20261114-r28-perses-signal-inventory]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1610, mcpdev80/baseharbor#1645]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44688554297", "https://github.com/mcpdev80/baseharbor/actions/runs/44689126814"]
---

- [ ] t-20261114-r28-perses-tempo-source · Connect Perses Tempo #task #release/v0-4-28 #status/active #view/active #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** w091-pr0428-091-tempo-source · **Priority:** normal  
    **PR:** [baseharbor#1610](https://github.com/mcpdev80/baseharbor/pull/1610), [baseharbor#1645](https://github.com/mcpdev80/baseharbor/pull/1645)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44688554297), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44689126814)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-contract-seam](t-20261114-r28-perses-contract-seam.md), [t-20261114-r28-perses-runtime](t-20261114-r28-perses-runtime.md), [t-20261114-r28-perses-signal-inventory](t-20261114-r28-perses-signal-inventory.md)  
**Required by:** [t-20261114-r28-perses-log-trace-dash](t-20261114-r28-perses-log-trace-dash.md), [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** w091-pr0428-091-tempo-source  
**Priority:** normal  
**PRs:** [baseharbor#1610](https://github.com/mcpdev80/baseharbor/pull/1610), [baseharbor#1645](https://github.com/mcpdev80/baseharbor/pull/1645)  
**Source:** 
<!-- /generated:links -->

## Goal

Provision selected authorized Tempo datasource via supported Perses plugin, scoped and verified.

## Scope and file ownership

Dedicated Tempo datasource adapter/tests; retain existing Tempo backend. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/traces/tempo.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/traces/tempo.go)
- [internal/traces/realization.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/traces/realization.go)
- [internal/serviceaccess/policy.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/serviceaccess/policy.go)

Use Perses TempoDatasource/trace query plugin verified in pinned image. Resolve only authorized existing Tempo with TLS/auth; test actual trace query plus unsupported, denied and absent-source behavior.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Provision selected authorized Tempo datasource via supported Perses plugin, scoped and verified.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-tempo-source](t-20261113-r28-grafana-tempo-source.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

luna-r1 REQUEST_CHANGES (bdafd838) — korrekturrunde laeuft

BOARD-KORREKTUR: der eingetragene #1610 ist closed-ohne-merge (d57ab5275, 2026-11-16T12:58Z), der einzige offene traeger ist #1645 — und der ist DRAFT. Ein draft ist kein kandidat (§5.2, meine eigene regel den lanen), deshalb darf die karte nicht auf review stehen. Zustand planned; der weg zur abnahme: draft #1645 auf non-draft + hopf + exaktkopf-lauf

dep-frei nach plan.py show (contract-seam, runtime, signal-inventory accepted). basis develop, NICHT der lane-branch von 0428-083, weil 083 auf 0428-174 haelt. write-set: perses-datasource-pfade; anweisung enthaelt die Konfliktfelder zu 168 (registry/migration) und 078 (app_status_result, perses_identity)

entscheidung auf ihre frage: KEIN owner-scope noetig. ihr gruen-beleg run 44665488793/43874313785 ist vom 16.11. an head c781eb86 und damit nach der gate-logik-aenderung durch #1708 wertlos (§5.4); develop ist nicht ahne des heads (merge-base 14d8f17d, 20 commits voraus), also ist der hop pflicht. befehl: rebase auf develop, push --force-with-lease auf den unprotected lane-branch w091-tempo-r5-fix, 'gh pr ready 1645' (mechanisch, lane-seitig), EIN run am neuen head bis terminal. grenze: cmd/baha/app_status_result.go = develop-stand ubernehmen, sonst STOP mit datei:zeile, weil dort 078 schreibt


## 2026-11-20 exact-head CI recheck

PR #1645 is now Ready (not Draft) at `253883eb96fd4d1765397028f67b4409fa9c7371`, based on `develop@36d075fad77fa61ac8c153e979855546589b32c2`. Exact PR run [44688554297](https://github.com/mcpdev80/baseharbor/actions/runs/44688554297) completed with overall conclusion `cancelled`; `go-vet` and the `packages` shard fail to compile because `internal/metrics/perses_tempo_fixture_test.go:95` calls missing `serviceissuer.Issuer.CertificateFor`. The PR Selected Checks job fails because selected Go shard coverage is incomplete. Runtime/native and release gates were skipped. Earlier exact-head run 44688531802 was also cancelled. Keep this task Active for its owner to repair the candidate and obtain a terminal passing exact-head run; do not move to Review based on Ready metadata alone.


## 2026-11-20 latest candidate refresh

The owner advanced #1645 to `6a7e462cc0bc10fb8fe55e2746efb6a3e03e73a2` (Ready, based on develop `36d075fad77fa61ac8c153e979855546589b32c2`). Exact PR run [44689126814](https://github.com/mcpdev80/baseharbor/actions/runs/44689126814) completed with failure. `go-vet` reports undefined `PersesConfiguredStatusNow` in `internal/capability/perses_security_test.go:292` and `cmd/baha/app_perses_access_cli_test.go:136`; the packages shard reports Perses fixture tests failing because the persisted gateway plan file is absent, plus capability build failures. Selected Go shards and `PR Selected Checks` fail; native/runtime and release gates are skipped. No formal GitHub review exists. Keep Active; require the owner to repair the current head and produce passing exact-head required checks plus Tempo runtime acceptance before Review.
