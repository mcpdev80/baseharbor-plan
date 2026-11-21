---
id: t-20261114-r28-cli2-app-lifecycle
card_number: "0428-060"
card_short_title: "Unify up and down semantics"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: 0428-060-downroute
kanban_status: active
kanban_lane: active
kanban_summary: "Unify up and down semantics. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-060 · Unify up and down semantics
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-env-policy]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1747]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-cli2-app-lifecycle · CLI redesign: Unify up and down semantics #task #release/v0-4-28 #status/active #view/active #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** 0428-060-downroute · **Priority:** high  
    **PR:** [baseharbor#1747](https://github.com/mcpdev80/baseharbor/pull/1747)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md)  
**Required by:** [t-20261114-r28-cli2-source-pull](t-20261114-r28-cli2-source-pull.md)  
**Owner:** 0428-060-downroute  
**Priority:** high  
**PRs:** [baseharbor#1747](https://github.com/mcpdev80/baseharbor/pull/1747)  
**Source:** 
<!-- /generated:links -->

## Goal

Unify up and down semantics. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Converge app apply and up through one authorized plan/preflight/apply/verify lifecycle; down preserves state and accepts applicable component selection.

## Entry points and ownership

- Starting points: `cmd/baha/app_apply.go; app_up_lifecycle.go; app_lifecycle.go; internal/application/runtime_lifecycle.go`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

No success without verified readiness; component subset and shared effects, partial failures, auth/consent, existing CLI/JSON/MCP and local/remote behavior; runtime proof as required.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.

END_BLOCKED war eine scope-frage, keine blockade. Arbeit: down-consent-gate in executeApplicationStop implementiert, baut gruen am develop 77c1e60f5, write-set sauber (app_update.go NICHT im diff, von mir nachgemessen). Frage: die echte down-autorisierung authorizeApplicationStop liegt in cmd/baha/application_stop_impact.go:177, die nicht in meinem mission-schreib-set stand. Gemessen und ERLAUBT, begrenzt: datei existiert auf develop, und kein anderer offener PR fasst sie an (#1739 delta 0 treffer, #1742 delta 0 treffer). Grenze 1: app_runtime_retirement.go:112 (nutzt dieselbe funktion) bleibt STOP-pflichtig, weil consent/retirement in 0428-209/0428-214 verhandelt wird. Grenze 2: keine autorisierung weicher fuer gruen, beide richtungen mit mutation belegt. Noch kein PR am remote (kein lane-0428-060* branch gemessen)

ERSTER EIGENER PR DER KARTE: #1747 (head 8103f0065098, base develop, draft=false, mergeable MERGEABLE). Von mir gemessen: ancestry gegen develop 77c1e60f51b9 = JA, rev-list --count develop..head = 1, delta gegen develop = GENAU zwei dateien (cmd/baha/app_lifecycle.go + cmd/baha/app_lifecycle_down_convergence_test.go), 'PR Selected Checks' pass, 0 fehlgeschlagene check-zeilen. Ihr seam downRequiresConfirmedConsent: 5 treffer am head, eine definition von TestDownConsentGoesBothWays. Sie meldet ausserdem: der erreichbare down-pfad (app down/stop -> retireRuntimePreservingData) sei ueber e.confirmed + authorizeApplicationStop bereits autorisiert, und die owner-grenze app_runtime_retirement.go:112 sei unangetastet. GENAU DAS muss die abnahme pruefen: ob der neue seam im produktionspfad greift und nicht nur im test.

CODEX-REVIEW 0428-060-review-1.md = REQUEST CHANGES am exakten head 8103f0065098, von MIR nachgemessen: die ROUTE ist richtig verdrahtet ('appDownCommand' 'cmd/baha/app_lifecycle.go:21-31' delegiert an 'appStopCommand' und der consent-seam wird in ':127' befragt), ABER der test 'app_lifecycle_down_convergence_test.go:15' ruft die boolean hilfsfunktion DIREKT — die mutation 'seam-aufruf entfernen' laesst ihn GRUEN, also ist kriterium 2/3 unbewiesen. Lane 0428-060-downroute arbeitet die route-echen faelle (ohne/mit --yes, beide richtungen, fuer down UND stop) plus mutationen und hop auf develop 97b2ba5543f0.
