---
id: t-20261114-r28-cli2-app-interact
card_number: "0428-063"
card_short_title: "Guide app logs exec and urls"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: sweep maintainer (claim 2ae9fd00d) / coord (integrations-regel)
kanban_status: wait
kanban_lane: wait
kanban_summary: "Guide app logs exec and urls. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-063 · Guide app logs exec and urls
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-identity-secrets, t-20261114-r28-cli2-source-model]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1623]
sources: []
blocker: ""
wait_reason: "die vier vollen Pre-Release-gates (mcp, init, shell-ux, config-matrix) sind am head 3617a2a5 ROT wegin ANDEREN karten, nicht wegen 1746 (PR-CI 45007709072 SUCCESS): mcp 137170967605 = 4 unerwartete Perses-methoden (0428-231), init/shell-ux = managed operator authentication (0428-063), config-matrix = workload-only authentication_failed (0428-199); plus die fisch->zsh einschraenkung ist .github-owner-scope"
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1623"]
---

- [ ] t-20261114-r28-cli2-app-interact · CLI redesign: Guide app logs exec and urls #task #release/v0-4-28 #status/wait #view/wait #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** sweep maintainer (claim 2ae9fd00d) / coord (integrations-regel) · **Priority:** high  
    **PR:** [baseharbor#1623](https://github.com/mcpdev80/baseharbor/pull/1623)  
    **Waiting:** die vier vollen Pre-Release-gates (mcp, init, shell-ux, config-matrix) sind am head 3617a2a5 ROT wegin ANDEREN karten, nicht wegen 1746 (PR-CI 45007709072 SUCCESS): mcp 137170967605 = 4 unerwartete Perses-methoden (0428-231), init/shell-ux…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1623)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md), [t-20261114-r28-cli2-source-model](t-20261114-r28-cli2-source-model.md)  
**Required by:** [t-20261114-r28-cli2-cli-integration](t-20261114-r28-cli2-cli-integration.md)  
**Owner:** sweep maintainer (claim 2ae9fd00d) / coord (integrations-regel)  
**Priority:** high  
**PRs:** [baseharbor#1623](https://github.com/mcpdev80/baseharbor/pull/1623)  
**Source:** 
<!-- /generated:links -->

## Goal

Guide app logs exec and urls. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Make app logs/exec/urls guide missing choices, support -c; exec defaults shell and --cmd one command, preserve exit status. Include app-bound service GUI URLs only.

## Entry points and ownership

- Starting points: `cmd/baha/app_logs.go; app_access.go; app_access_urls.go; human_open.go`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Component filtering, ambiguous/non-interactive behavior, safe quoting, no unrelated URL, verified/unknown accessibility and current remote support.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Independent review

Read-only findings: [PR evidence](../evidence/r28-welle4-2026-11-19/codex-review-wave/1623-0428-063-independent-review.md). Draft #1623 `8014d71e` has no exact-head checks and three behavior gaps: `app logs -c` does not filter, `app exec --cmd` does not shell-parse, and child exit status collapses to 1.

## Handoff

Round-1 delivered by w063 (flash): candidate lane-0428-063-cli2-app-interact @ beb2ee5859a8a2ffa07fd5725370275411e27011, draft PR baseharbor#1623 (base cli2-identity-secrets-head). Guided logs/exec/urls over the delivered read view, fail-closed app.logs/app.exec/app.urls authorization; no merge, no ready_for_review. Evidence: evidence/r28-welle1-2026-11-15/cli2-app-interact/round-1.md. CI dispatch belongs to the coordinator.

BOARD-KORREKTUR nach unabhaengiger GEGENLESE (akte evidence/r28-welle4-2026-11-19/codex-review-wave/board-sweep-gegenlese-1.md, haupt e86d817d): der PR dieses fachers ist draft=true. Ein draft ist KEIN kanditat (§5.2), also war der zustand 'review' zu gut — er versprach einen pruefbaren kanditaten, den es nicht gibt. FEHLENDE STUFE, klar benannt: draft auf non-draft, EIN monotoner hopf auf den aktuellen develop, EIN exact-head-lauf bis terminal; die arbeit im zweig ist vorhanden. Rueckstandiger zustand, kein inhaltlicher rueckstand

## Independent review 2026-11-19

- Befunde (independent review 1623): (1) 'app logs -c NAME' parst den component-selector, der ausfuehrungspfad nutzt aber nur options.service — die auswahl filtert NICHT; (2) 'app exec --cmd "echo hi > /tmp/x"' geht als EIN argument an Compose, kein shell-parse, die beworbene syntax funktioniert nicht; (3) preserveWorkloadExitStatus wickelt den kind-exit als presented error ein, cli.ExitCode mappt das falsch — der bewahrte exit-code ist nicht belegt.
- Nachweis-Voraussetzung: ein exaktkopf-lauf mit dem geforderten gate; ueber den gestapelten base-ref ist der derzeit nicht ausloesbar (owner-draht ci.yml:14-18, derselbe grund wie #1615).

PR #1623 draft = kein kandidat (§5.2). rebasen auf die basis, sobald #1615 gruen ist.

## Coordination note (coordinator, gemessen) - UEBERNAHME-BESTAETIGUNG
- claim der maintainer-sitzung ist anerkannt (plan 2ae9fd00d), karte steht auf active; keine meiner lanen schreibt an diesem branch.
- PR 1623: state OPEN, DRAFT (draft hat keine required checks), head 4cbf92960cb, rueckstand 586 commits gegen develop 8629450ef3c5198bb675331c12f56b2c9377aa1c, kein workflow-haengt an diesem head.
- ancestry in ordnung, gemessen: die beiden spitzen aus 0428-057 (8963efd8a, bb5bb3676) liegen IN develop, die verknotungen 4463ac617/e9c313c5a sind eigene branch-verknotungen des kandidaten - kein fremder inhalt verwischt die pruefung.
- die drei alten befund-punkte sind auf diesem branch inhaltlich behoben (selectedComponents durch validateWorkloadLogComponents/workloadLogsCommandArgs, '--cmd' -> sh -c in workloadExecCommandArgs, preserveWorkloadExitStatus ueber cli.WithExitCode) - bestaetigt durch ihre messe, von mir nicht erneut gegengeprueft.
- RESERVIERTE DATEIEN, ihre frage: docs/cli/command-index.md, docs/de/cli/command-index.md und docs/reference/cli-machine-coverage.md sind ERZEUGTE dateien. Regel: niemand loest ihre konflikte von hand - sie werden AUS DEM COMMAND-BAUM NEU ERZEUGT. Integration-owner ist der Coordinator, AUSFUEHRUNG laeuft auf einer benannten worker-lane (der Coordinator schreibt selbst keinen produkt-code): die lane erzeugt die drei dateien aus dem command-baum neu und loest den konflikt dadurch, ohne von hand zu editieren. Die karte bleibt mit ihrem claim bei ihnen - nur diese drei dateien laufen ueber die integrations-linie, damit dort ein einziger schreiber sitzt. Bis zur fertigstellung ihrer seite: KEIN hop, KEIN run auf diesen drei dateien von beiden seiten gleichzeitig.
- SORGFALT fuer die reihenfolge: nach einem hop auf develop werden die nativen data-capabilities-reihen ausgefuehrt und treffen den broker-defekt 0428-237 (zeuge PR 1762, durchgang 45001383922: native docker 137144598339 FAIL nach 2m03s, podman 137144598342 FAIL 503 not_ready nach 4m57s). Revalidierung und read-only-befunde bleiben richtig; terminal gruen erst nach 237.

TRAEGER-GEDANKE IST ERLEDIGT, GRUND GEMESSEN (akte der lane 0847d100): die generator-ausgabe (BASEHARBOR_UPDATE_MACHINE_DOCS=1 go test ./cmd/baha -run TestHumanCommandIndexTracksExactCommandMetadata und TestMachineDocumentationTracksRegistryAndCommandTree) ist BYTE-FOR-BYTE wie develop 8629450ef3c - der carrier-PR 1764 war darum LEER und fiel zu recht durch 'PR . Trusted Plan' 137156455112 und 'PR . Selected Checks' 137156547886 (24 skipped). ENTSCHEID: weder leerer carrier akzeptieren, noch die command-tree-aenderung in eine andere karte ziehen - die neu-erzeugung ist ein SCHRITT IM hop dieses PRs (generator-durchgang, kein hand-edit) und PR 1764 bleibt geschlossen. Damit entfaellt ihre blockade 'wartet auf index-traeger': der hop auf develop 8629450ef3c erzeugt die doc-deltas aus IHREM eigenen command-baum. Rueckstand 586 commits, 20 dateien, davon 8 in cmd/baha; KANTE zu #1620 ueber cmd/baha/app_access.go bitte vor dem hop pruefen (board/integration-order.md).

test: traeger-entscheid gemessen, PR 1764 bleibt geschlossen

TRAEGER-GEDANKE ERLEDIGT, GRUND GEMESSEN: die generator-ausgabe (BASEHARBOR_UPDATE_MACHINE_DOCS=1 go test ./cmd/baha -run TestHumanCommandIndexTracksExactCommandMetadata und TestMachineDocumentationTracksRegistryAndCommandTree) ist BYTE-FOR-BYTE wie develop 8629450ef3c - der carrier-PR 1764 war darum LEER und fiel zu recht durch 'PR . Trusted Plan' 137156455112 und 'PR . Selected Checks' 137156547886 (24 skipped). ENTSCHEID: weder einen leeren carrier akzeptieren, noch die command-tree-aenderung in eine andere karte ziehen - die neu-erzeugung ist ein SCHRITT IM hop dieses PRs (generator-durchgang, kein hand-edit); PR 1764 bleibt geschlossen. Damit entfaellt die blockade 'wartet auf index-traeger': der hop auf develop 8629450ef3c erzeugt die doc-deltas aus dem EIGENEN command-baum. Rueckstand 586 commits, 20 dateien, davon 8 in cmd/baha; KANTE zu #1620 ueber cmd/baha/app_access.go vor dem hop pruefen (coordinator/board/integration-order.md).

#1746: ihr teil ist GELUNGEN (PR-CI 45007709072 SUCCESS/CLEAN am 3617a2a5a8b). Der REST der akzeptanz haengt NICHT an 1746: der volle Pre-Release-durchgang 45009827491 ist rot in mcp/init/shell-ux/config-matrix, aber die kopfe dieser fehl- schlaege sind ANDERE karten - Perses (0428-231), managed-operator-auth (0428-063), workload-auth (0428-199). Und die eine fisch->zsh-zeile (pre-release.yml 343) ist .github-OWNER-scope, die lane darf sie nicht pushen. Karte auf wait; der fisch-einschub liegt beim eigentimer, die gate-kopfe bei ihren eigenen karten.
