---
id: t-20261114-r28-perses-tempo-source
card_number: "0428-091"
card_short_title: "Connect Perses Tempo"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: 0428-091-
kanban_status: wait
kanban_lane: wait
kanban_summary: "Provision selected authorized Tempo datasource via supported Perses plugin, scoped and verified."
kanban_title: 0428-091 · Connect Perses Tempo
priority: normal
depends_on: [t-20261114-r28-perses-contract-seam, t-20261114-r28-perses-runtime, t-20261114-r28-perses-signal-inventory]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1610, mcpdev80/baseharbor#1645]
sources: []
blocker: ""
wait_reason: "hop and rerun are deliberately withheld: run 44814746593 failed in cli-0..3 and packages on the interactive-setup operator context, which card 0428-221 (PR 1750) fixes; rerun only after that merge and an additive hop to current develop"
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44688554297", "https://github.com/mcpdev80/baseharbor/actions/runs/44689126814", "https://github.com/mcpdev80/baseharbor/actions/runs/44695439903", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1645-0428-091.md"]
---

- [ ] t-20261114-r28-perses-tempo-source · Connect Perses Tempo #task #release/v0-4-28 #status/wait #view/wait #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** 0428-091- · **Priority:** normal  
    **PR:** [baseharbor#1610](https://github.com/mcpdev80/baseharbor/pull/1610), [baseharbor#1645](https://github.com/mcpdev80/baseharbor/pull/1645)  
    **Waiting:** hop and rerun are deliberately withheld: run 44814746593 failed in cli-0..3 and packages on the interactive-setup operator context, which card 0428-221 (PR 1750) fixes; rerun only after that merge and an additive hop to current develop  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44688554297), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44689126814), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44695439903), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1645-0428-091.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-contract-seam](t-20261114-r28-perses-contract-seam.md), [t-20261114-r28-perses-runtime](t-20261114-r28-perses-runtime.md), [t-20261114-r28-perses-signal-inventory](t-20261114-r28-perses-signal-inventory.md)  
**Required by:** [t-20261114-r28-perses-log-trace-dash](t-20261114-r28-perses-log-trace-dash.md), [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** 0428-091-  
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

hop geliefert und gleichzeitig widerlegt, dass der alte 16.11.-lauf galt: head 6a7e462cc0bc, draft=false, develop 36d075fad77f ist ahne (merge-base --is-ancestor JA). ABER der exakte head ist ROT: 37/37 checks fertig, 8 failure = PR Selected Checks, PR · Validation · go-vet, PR · Go unit · owner/packages/cli-0/cli-1/cli-2/cli-3. alle unit-shards + vet gleichzeitig = kompilierfehler im gefuehrten stand, nicht Verhalten. auftrag: log-failed WÖRTLICH, go build/go vet im worktree, konfliktloesung-pruefung gegen develop-stand, dann EIN run. vergleichsregel dazu: develop-push ist auf 36d075fad77f success (run 44669117744/44669117784, 0 failure)

## 2026-11-20 latest candidate refresh

The owner advanced #1645 to `6a7e462cc0bc10fb8fe55e2746efb6a3e03e73a2` (Ready, based on develop `36d075fad77fa61ac8c153e979855546589b32c2`). Exact PR run [44689126814](https://github.com/mcpdev80/baseharbor/actions/runs/44689126814) completed with failure. `go-vet` reports undefined `PersesConfiguredStatusNow` in `internal/capability/perses_security_test.go:292` and `cmd/baha/app_perses_access_cli_test.go:136`; the packages shard reports Perses fixture tests failing because the persisted gateway plan file is absent, plus capability build failures. Selected Go shards and `PR Selected Checks` fail; native/runtime and release gates are skipped. No formal GitHub review exists. Keep Active; require the owner to repair the current head and produce passing exact-head required checks plus Tempo runtime acceptance before Review.

hop geliefert: head 6a7e462cc0bc, draft=false, develop 36d075fad77f ist ahne des heads (merge-base --is-ancestor JA). der exakte head ist ROT: 37/37 checks fertig, 8 failure = PR Selected Checks, PR Validation go-vet, PR Go unit owner/packages/cli-0/cli-1/cli-2/cli-3. alle unit-shards plus vet gleichzeitig zeigt einen kompilierfehler im gefuehrten stand, nicht das produktverhalten. auftrag: log-failed woertlich, go build und go vet im worktree, konfliktloesung gegen develop-stand pruefen, dann EIN run. vergleich: develop-push ist auf 36d075fad77f success (run 44669117744 und 44669117784, 0 failure)

ihre sandbox-these GEMESSEN WIDERLEGT, ursache ist ihr hop. CI-run 44689126814 log-failed: 5x 'undefined: capability.PersesConfiguredStatusNow', 4x 'cannot use files.ResourceProject', 12x 'no such file or directory', FAIL in cmd/baha (4x) + internal/capability + internal/application. diese symptome sind kompilierfehler, und die symbole EXISTIEREN auf develop: internal/capability/perses.go:268 definiert PersesConfiguredStatusNow, ResourceProject ist auf develop vorhanden; ihr head BENUTZT beide (cmd/baha/app_perses_access_cli_test.go:136, internal/capability/perses_security_test.go:292/297/302) => die konfliktloesung des rebase hat develop's perses.go zurueckgesetzt. baseline gegen 'die shards laufen nie': run 44669117744/44669117784 sind develop-push-runs, und 44667933981 zeigt 'Go unit owner/packages/cli-0..3' + go-vet/go-build ALLE success. ihr lokaler vergleichs-run lief auf dem coordinator-host (/home/marcel/.config existiert dort, nicht auf einem runner) und beweist nichts ueber CI. befehl: git diff lane-origin/develop...HEAD -- internal/capability/perses.go, dann 'git checkout lane-origin/develop -- <die datei>', dann 'go build ./…' + 'go vet ./…' VOR jedem push, dann EIN run


## 2026-11-20 candidate refresh after owner push

PR #1645 advanced to exact head `0449f06587c849f598447094428d2f7296ed1f5b`, still OPEN, Ready/non-draft, based on `develop`, mergeStateStatus `BLOCKED`, and without formal reviews. Exact run [44695439903](https://github.com/mcpdev80/baseharbor/actions/runs/44695439903) is still in progress: 35 jobs, 10 success, 20 skipped and 5 Go unit shards in progress at the latest poll. Build, vet, authority-package tests, OpenBao-package tests, source format, workflow policy, Trusted Plan and focused Python have passed so far. Native Keycloak/Core, selected runtime, public contracts, and release gates are skipped. Keep this card Active; do not treat the partial green set as Review or merge acceptance.

kandidat ist nach meiner messung currency-faehig und gruen: head 0449f06587c849f598447094428d2f7296ed1f5b, base.sha = develop-spitze 36d075fad77f, draft=false, mergeable=clean, run 44695439903 completed/success, 36/36 checks fertig, 0 failure. ahnen-pruefung erst FALSE dann KORRIGIERT gemessen: mein erster 'merge-base --is-ancestor' lief gegen ein in meinem objektbaum FEHLENDES objekt (leerer merge-base = technical nein, kein historisches). nach 'git fetch lane-origin refs/pull/1645/head' ist develop 36d075fad77f der merge-base = JA. diff gegen develop: 25 dateien, ohne app_status_result.go, perses_datasources*, observability/* = write-sets der laufenden karten frei. CODEX-REVIEW ist bestellt (session 95971e0a, rolle REVIEW, akte 1645-0428-091.md); der Auftrag enthaelt meine eigene widerlegung ihrer sandbox-these und den nachweis, dass der erste hop-head 6a7e462cc0bc durch verlorene develop-symbole rot war


## Sweep correction — 2026-11-20 ~07:50 UTC

A concurrent plan update moved this card to Review after run `44695439903` succeeded. Reverted it to Active after rechecking task acceptance: that run passed selected checks but skipped the Selected Runtime / Tempo runtime gate, and the existing acceptance note explicitly requires passing exact-head checks plus Tempo runtime acceptance before Review. The PR remains OPEN+Ready at `0449f06587c849f598447094428d2f7296ed1f5b`, with `mergeStateStatus=CLEAN`, no formal GitHub review, and no runtime acceptance evidence. Independent Wait/Review audit agrees there is no justified Review handoff.


## Independent CODEX-REVIEW result — 2026-11-20 07:51 UTC

The exact-head review in [1645-0428-091.md](../evidence/r28-welle4-2026-11-20/codex-review-wave/1645-0428-091.md) returned **REQUEST CHANGES** on head `0449f06587c849f598447094428d2f7296ed1f5b`. It identifies: (P1) no pinned Perses runtime proof that the Tempo datasource plugin can reach the managed Tempo service-access endpoint from the Perses network namespace; current `localhost` rewrite does not prove routability; (P2) `tempoProviderHTTPClient` disables `AuthenticationRequired`, allowing required mTLS identity to be omitted; (P3) the candidate removed two fail-closed host-dashboard regression tests without replacements. The exact Actions run `44695439903` succeeded but skipped native/runtime jobs, so it cannot discharge P1. Direct GitHub PR reviews API remains empty; this is an internal Codex review artifact, not a submitted GitHub review. Card stays Active pending corrections and exact acceptance.


## Wait-reason correction — 2026-11-20 08:09 UTC

The current Wait status is supported by the owner pause and the latest Codeman pool snapshot (5/5 seats, no open seat), but the prior `wait_reason` incorrectly emphasized the earlier green run and did not reflect the later CODEX-REVIEW r2 REQUEST CHANGES. The reason now records the outstanding Perses runtime endpoint, mTLS policy, and host-dashboard regression findings and sets the concrete resume trigger: first open worker seat, followed by corrections and exact-head acceptance. PR #1645 remains OPEN+Ready at `0449f065`; no closure transition is supported.

SITZ FREI GEWORDEN DURCH DEN MERGE VON #1709 (develop 681700ca66f3) -> diese karte nimmt ihn, die warteschlange ist damit geloest. neue frische lane 0428-091- (sid 0ee3dfb3, flash-kanal, model worker-flash ueber agentgateway, readiness von spawn-lane.sh verifiziert). gemessener ausgang: #1645 head 0449f06587c8, base 36d075fad77f, draft=false, mergeable=clean, 25 dateien, develop-ahn JA, run 44695439903 completed/success 36/36 - der gruene stand ersetzt NICHT das verdict (§5.4), das verdict ist REQUEST CHANGES (akte codex-review-wave/1645-0428-091.md, vier punkte P1-P4). auftrag: endpoint-routbarkeit aus dem echten netzwerk-namespace von Perses ohne verlust der AuthenticationRequired-policy (perses_tempo_datasource.go:482-496, :467-470, internal/traces/tempo.go:511-523), rueckgabe der ZWEI geloeschten fail-closed host-dashboard regressionstests in internal/capability/perses_test.go, und die drei 'partially present, not accepted'-punkte auf accepted fuehren. Coordinator/lane tooling observations have been moved to the separate Codeman Coordinator Tooling repository.
