---
id: t-20261114-r28-cli2-app-lifecycle
card_number: "0428-060"
card_short_title: "Unify up and down semantics"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: f0f6c8b4 (#1738 hop in flight, inherits develop catalog) / Coordinator
kanban_status: wait
kanban_lane: wait
kanban_summary: "Unify up and down semantics. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-060 · Unify up and down semantics
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-env-policy]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1747, mcpdev80/baseharbor#1738]
sources: []
blocker: ""
wait_reason: "#1738 hop auf 78f75c90 laeuft erneut (false-positive catalog-STOP berichtigt: #1738 aendert katalog selbst nicht, erbt nur develops #1786 rows); exakter PR-head gruen ausstehend"
evidence: ["https://github.com/mcpdev80/baseharbor/commit/e6c199e7b7dd7d076a776d11c3ba16f25e59c254"]
---

- [ ] t-20261114-r28-cli2-app-lifecycle · CLI redesign: Unify up and down semantics #task #release/v0-4-28 #status/wait #view/wait #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** f0f6c8b4 (\#1738 hop in flight, inherits develop catalog) / Coordinator · **Priority:** high  
    **PR:** [baseharbor#1747](https://github.com/mcpdev80/baseharbor/pull/1747), [baseharbor#1738](https://github.com/mcpdev80/baseharbor/pull/1738)  
    **Waiting:** \#1738 hop auf 78f75c90 laeuft erneut (false-positive catalog-STOP berichtigt: \#1738 aendert katalog selbst nicht, erbt nur develops \#1786 rows); exakter PR-head gruen ausstehend  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/e6c199e7b7dd7d076a776d11c3ba16f25e59c254)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md)  
**Required by:** [t-20261114-r28-cli2-source-pull](t-20261114-r28-cli2-source-pull.md)  
**Owner:** f0f6c8b4 (#1738 hop in flight, inherits develop catalog) / Coordinator  
**Priority:** high  
**PRs:** [baseharbor#1747](https://github.com/mcpdev80/baseharbor/pull/1747), [baseharbor#1738](https://github.com/mcpdev80/baseharbor/pull/1738)  
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

CODEX-REVIEW 'evidence/cli-redesign-20261114/0428-060/review-2.md' = REQUEST CHANGES am kandidaten 2d848f4469cfc. Der inhalt ist laut abnahme RICHTIG ('the new command-route tests materially address' den alten befund), der BLOCKER ist ein roter gehosteter check: 'PR · Go unit · cli-3' = FAIL (job 136858546552, schritt 'Execute selected Go tests with isolated runtime state', annotation 'exit code 1'), und 'PR Selected Checks' faellt an 'Require complete selected Go shard coverage' — von mir gegen gemessen: selected=fail, cli-3=fail, mergeable=MERGEABLE, head 2d848f4469cf, ancestry FRISCH. Zweiter offener punkt: die reviewerin fand ihre MUTATION-akte nicht ('rg --files evidence' ohne treffer fuer round-2/downroute) — die akte muss unter dem vereinbarten namen '0428-060-round-2-downroute.md' auf origin/main stehen. Lane erhaelt den job-id + die anweisung, den fehlertest aus dem per-job-protokoll zu holen und NUR das zu fixen.

korrektur IST GEKOMMEN, von MIR gemessen: PR #1747 head fb841c2c27c, 'rev-list --count head..develop' = 0 (FRISCH auf dea88c8f2caa), 'PR Selected Checks' PASS — der cli-3-fehler aus review-2.md (job 136858546552, schritt 'Execute selected Go tests with isolated runtime state') ist damit behoben, und der Re-Hop nach dem 46-commits-sprung ist drin. Die karte war 'active' mit owner 0428-060-downroute; ich stelle sie auf 'review', weil ein pruefbarer kandidat mit veroeffentlichter evidence vorliegt. Offener punkt fuer die abnahme: die mutations-akte unter dem vereinbarten pfad 'evidence/cli-redesign-20261114/0428-060-round-2-downroute.md' — die abnahme-sitzung fand sie vorher nicht.

CODEX-REVIEW 'evidence/cli-redesign-20261114/0428-060/review-3.md' = APPROVE CONTENT am exakten head fb841c2c27c90c6aa2c7b9ee9559da912ac64c2a, mit dem vermerk 'identity leak, no content deficiency' (die zwei obersten commits tragen den author '0428-076-nativeshape' — tooling-issue #24, von mir dort dokumentiert). MERGEN KANN ICH NOCH NICHT: develop ist seit 15:24 22fc68ebc065 (Ihr merge von #1748), fuer den kandidaten gilt 'rev-list head..develop' = 4 und ancestry NEIN. Ein hop-auftrag liegt fertig an (mission '0428-060-r3-hop22fc.md', gate exit 0) und geht auf den sitz der isolations-jagd, die ich mit meldefrist stoppe. Im hop-auftrag steht ausdruecklich: push auf 'lane-0428-060-updown' (KEIN neuer branch — das war der fehler der 076-lane heute), und 'git log --format=%an develop..head' muss genau eine identitaet zeigen.

statuskorrektur: NICHT blocked. #1738 editiert pr-gate-coverage.json selbst nicht; der additive hop ERBT develops #1784/#1785/#1786 rows (release bleibt v0.4.27) = korrekt, KEIN owner-decision. f0f fuehrt hop mit korrigierter pruefung aus (git diff develop HEAD -- katalog muss leer sein -> OK). Wartet nur auf gruenen exact-head. develop 78f75c90.
