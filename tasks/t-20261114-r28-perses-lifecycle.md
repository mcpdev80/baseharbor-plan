---
id: t-20261114-r28-perses-lifecycle
card_number: "0428-084"
card_short_title: "Perses lifecycle commands"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: 0428-084 korrektur (codeman 3ae5c022, ornith) — monoton auf develop, aggregate gruen
kanban_status: closed
kanban_lane: closed
kanban_summary: Guide enable/status/disable and ownership-safe removal of optional Perses using the accepted CLI contract; preserve monitoring…
kanban_title: 0428-084 · Perses lifecycle commands
priority: normal
depends_on: [t-20261114-r28-perses-contract-seam, t-20261114-r28-perses-runtime]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1598]
sources: []
blocker: ""
wait_reason: ""
resolution: "accepted"
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/2fd8d98dc8066b74bc2b7c121412cef3089e7ca3/evidence/r28-welle4-2026-11-19/codex-review-wave/1598-0428-084.md", "https://github.com/mcpdev80/baseharbor-plan/blob/c7376f916380d9d95d70e05204a10da2ef42d9b6/evidence/r28-welle4-2026-11-19/codex-review-wave/1598-0428-084-r2.md", "https://github.com/mcpdev80/baseharbor-plan/blob/6f05b59ccf3f13065093f7848de098063548d84f/evidence/r28-welle4-2026-11-19/perses-lifecycle-hopf/fix-3.md", "https://github.com/mcpdev80/baseharbor-plan/blob/c23cf7586911b623cde384d8769001626a686dd8/evidence/r28-welle4-2026-11-19/perses-lifecycle-hopf/fix-4.md", "https://github.com/mcpdev80/baseharbor/pull/1598", "https://github.com/mcpdev80/baseharbor-plan/blob/c5927a9bb48b75ccd592c091fa7c0d49dfa1c547/evidence/r28-welle4-2026-11-19/codex-review-wave/1598-0428-084-r3.md"]
---

- [x] t-20261114-r28-perses-lifecycle · Perses lifecycle commands #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** 0428-084 korrektur (codeman 3ae5c022, ornith) — monoton auf develop, aggregate gruen · **Priority:** normal  
    **PR:** [baseharbor#1598](https://github.com/mcpdev80/baseharbor/pull/1598)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/2fd8d98dc8066b74bc2b7c121412cef3089e7ca3/evidence/r28-welle4-2026-11-19/codex-review-wave/1598-0428-084.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/c7376f916380d9d95d70e05204a10da2ef42d9b6/evidence/r28-welle4-2026-11-19/codex-review-wave/1598-0428-084-r2.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/6f05b59ccf3f13065093f7848de098063548d84f/evidence/r28-welle4-2026-11-19/perses-lifecycle-hopf/fix-3.md), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/c23cf7586911b623cde384d8769001626a686dd8/evidence/r28-welle4-2026-11-19/perses-lifecycle-hopf/fix-4.md), [proof 5](https://github.com/mcpdev80/baseharbor/pull/1598), [proof 6](https://github.com/mcpdev80/baseharbor-plan/blob/c5927a9bb48b75ccd592c091fa7c0d49dfa1c547/evidence/r28-welle4-2026-11-19/codex-review-wave/1598-0428-084-r3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.28  
**Depends on:** [t-20261114-r28-perses-contract-seam](t-20261114-r28-perses-contract-seam.md), [t-20261114-r28-perses-runtime](t-20261114-r28-perses-runtime.md)  
**Required by:** [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** 0428-084 korrektur (codeman 3ae5c022, ornith) — monoton auf develop, aggregate gruen  
**Priority:** normal  
**PRs:** [baseharbor#1598](https://github.com/mcpdev80/baseharbor/pull/1598)  
**Source:** 
<!-- /generated:links -->

## Goal

Guide enable/status/disable and ownership-safe removal of optional Perses using the accepted CLI contract; preserve monitoring backend data.

## Scope and file ownership

Dedicated lifecycle adapter; no shared command registry write without CLI coordinator. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/application/provider_registry.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/application/provider_registry.go)
- [internal/providerui/application.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/providerui/application.go)
- [cmd/baha/app_dev_routing.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/cmd/baha/app_dev_routing.go)
- [cmd/baha/commands.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/cmd/baha/commands.go)

Add guided enable/status/disable via the accepted CLI/domain operation, proving inventory and ownership; false readiness is forbidden. Runtime stop/remove must not delete Prometheus, Loki, Tempo or foreign data. Shared CLI registry owned by coordinator.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Guide enable/status/disable and ownership-safe removal of optional Perses using the accepted CLI contract; preserve monitoring backend data.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-lifecycle](t-20261113-r28-grafana-lifecycle.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

delivered option-1 slice: head bcd13ddcb62, 14 tests, ci dispatcht; runtime-e2e deferred (frost)

hopf-runde angesetzt: #1598 war 'dirty' (merge-konflikt) UND draft; lane fuehrt monotonen merge-hopf auf develop aus, loest perses-konflikte inhaltserhaltend, haelt die 800-zeilen-grenze (source-readability-audit) und promoted den PR, bevor sie den exact-head-lauf beobachtet (akte perses-lifecycle-hopf/fix-1.md). SERIELLL mit 0428-076/#1597: dieselbe perses-dateimenge, daher noch nicht parallel angesetzt

hopf delivered und von mir geprueft: head 831c2bea8bd9b87aac71588353318e66d582c901, monoton (develop da76c5cf9 ancestor UND alter head e86672374 Vorfahr), merge-tree gegen develop 0 konflikte (ware 4), PR promoted draft=false. ABER exact-head lauf 44499778660 FAILURE: 'PR · Go unit · cli-0' und 'cli-3' -> 'machine_documentation_test.go:48: unclassified product command: baha app perses disable' + 'human_documentation_test.go:107: machine documentation drift in docs/cli/command-index.md'. ursache ist echte fehlende klassifikation der neuen lifecycle-kommandos (entscheidung in cmd/baha/machine_coverage.go:21 currentCommandCoverage(); 'gap' = fatal, 'semantic' verlangt machine.OperationByID-eintrag in internal/machine/contract.go), keine flaezigkeit. befehl r2: typed operations fuer alle neuen perses-kommandos wie bei 'app delete'/'app stop', die zwei generierten referenzen (docs/reference/cli-machine-coverage.md, docs/cli/command-index.md) neu erzeugen, lokal 'go test ./cmd/baha -run TestMachineDocumentation|TestHumanDocumentation' gruen, dann hopf-push + exact-head CI mit ausdrucklich gruenen cli-0/cli-3; akte fix-1.md mit fehlzeile + entscheidung je kommando + beiden laeufen

END angenommen, von mir ferngeprueft: head 3852472aa5281e6f69d38cba07cfb2cd7b9db018 monoton auf da76c5cf9, merge-tree 0 konflikte, PR open/draft=false/clean, exaktkopf-lauf 44510690944 completed SUCCESS mit NULL fehljobs und 'PR Selected Checks' = success (die 'PR · Selected Runtime'/'Core-less'-zellen skipped, wie vorgesehen). kopf-folge war: 831c2bea8 documentation-classification (44499778660 FAIL, machine_documentation_test.go:48), 6e371c99b golden-record (44509535053 FAIL, contracts/machine_control_test.go:41), 3852472aa gruen. abnahme fehlt noch — CODEX-REVIEW dafuer beauftragt

URTEIL REQUEST CHANGES auf dem CI-gruenen kopf 3852472aa (lauf 44510690944 SUCCESS, 'PR Selected Checks' success — CI sagt ueber diese stelle nichts: das lifecycle-convergence-gate ist invertiert, machine transports skippen den runtime-apply, direkter CLI fuehrt ihn sofort aus). rezept: cmd/baha/perses_lifecycle.go + geteilte CLI/MCP-lifecycle-tests, transport/aktions-matrix ueber enable/disable/remove, stop-kriterium 'machine transport meldet erfolg ohne apply'. MISSION vorbereitet (/var/tmp/missions/mission-084-convergence-gate.md), startet auf dem naechsten freien sitz. GRUND, warum ich sie NICHT schon jetzt dispatche: ihr schreibset teilt internal/machine/contract.go + contracts/machine/v1/control.golden.json + docs/reference/mcp.md mit der LAUFENDEN 057-lane (comm -12 gemessen) — paralleles schreiben in dieselben dateien ist ohne integrationsplan verboten (§4.3)

REQUEST-CHANGES-runde laeuft, gestartet auf dem frei gewordenen 057-sitz: das parallel-schreiben an internal/machine/contract.go + contracts/machine/v1/control.golden.json + docs/reference/mcp.md ist aufgehoben, weil 057 END_BLOCKED gemeldet und die lane entlassen ist (§4.3). kopf 3852472aa ist CI-gruen, aber das convergence-gate ist invertiert (machine transports skippen apply, direkter CLI fuehrt aus)

END akzeptiert, von mir qualifiziert auf dem NEUEN develop: head ea6cddd204fbc408b8e1b3b587f1f054ea1f43ce, monoton auf e1dc2cf61 (3852472aa ist ancestor), merge-tree 0 konflikte, PR open/draft=false/clean, exaktkopf-lauf 44523123388 completed SUCCESS mit 0 fehljobs und 'PR Selected Checks' = success. inhalt: gate jetzt richtig herum (cmd/baha/perses_lifecycle.go:19-25 'machine transports (MCP stdio, HTTP/remote) run the shared apply lifecycle immediately; the direct human CLI defers … prints the actionable deferred-apply notice'). CODEX-REVIEW fuer DIESEN kopf beauftragt (1598-0428-084-r2.md), bei approve merge ich ins fenster

URTEIL: 'APPROVE CONTENT — exact head ea6cddd204fbc408b8e1b3b587f1f054ea1f43ce', 'END_APPROVE_CONTENT #1598 / run 44523123388 SUCCESS / merge held for monotonic base hop and fresh exact-head'. von mir gegen das JETZIGE develop geprueft: PR open/draft=false/mergeable_state 'behind' (NICHT dirty), 'git merge-tree --write-tree origin/develop <kopf>' = 0 konflikte gegen f518e859d, aggregate 'PR Selected Checks' auf diesem sha = completed success, combined status 'pending' (0 contexts, weil der develop bewegt ist). mission-084-hopf-onto-f518e859.md ist GESCHRIEBEN (reiner hopf, keine produkt-aenderung, konfliktannahme an environment.go/registry.go + config_mutation.go-beruehr-verbot) und startet auf dem ersten freien sitz; danach meldet die lane den neuen kopf + den frischen exact-head-lauf, und die abnahme mergt

hopf-lane gestartet (mission-084-hopf-onto-f518e859.md, reiner hopf auf f518e859d, keine produkt-aenderung): die abnahme hat APPROVE CONTENT auf ea6cddd20 erteilt, den merge aber an 'monotonic base hop + fresh exact-head' gekoppelt. sitz kam frei, weil 088s lane abgeliefert hat (088 selbst ist jetzt im fenster). nach deren lauf-meldung geht der kopf sofort zur abnahme mit dem einzigen zusatz-beleg 'git diff --name-only ea6cddd20 <kopf>' = leer

END_BLOCKED PRUEFE ich als FALSE zurueck, weil alle drei gruenden widerlegt sind: (1) 'git show <rev>:internal/machine/contract.go | grep -c app.perses' = 0 in develop 3b634232f, im 088-kopf 78c002ff5, in f518e859d UND im alten develop da76c5cf9 — die vier app.perses-ops waren nie in develop, sie sind 084s eigener zusatz (zeilen 205-208 ihres astes); (2) 'git merge-tree --write-tree 3b634232f ea6cddd20' = 0 CONFLICT-zeilen (merge-tree c82b5b4882776d3e7d9bdf21c2d184f35631a271), PR 'behind' statt 'dirty'; (3) der einzige kommentar-unterschied in internal/metrics/perses_contract_test.go zwischen develop und 084 ist 084s EIGENER block, von #1592 kommt dort nichts. BEFEHL: hopf als MERGE-commit ('git merge origin/develop', macht develop zum ancestor ohne die zeilen anzufassen) + die vier nachweise in der akte (ancestor rc=0, merge-tree 0, ea6cddd20 als ancestor, grep app.perses = 4) und der abschnitt 'was ich falsch gemeldet habe', weil die akte 12163463 einen falschen fernzeug enthaelt. dann fokus-tests, push, exact-head lauf bis terminal

END_DONE inspiziert, disposition: INHALT angenommen (APPROVE CONTENT auf ea6cddd20, app.perses = 4 typed ops erhalten, merge-commit 3316714c mit develop 859654861 + ea6cddd20 als ancestors, merge-tree 0), QUALIFIKATION fehlt — urSAche = VERALTETE BASE, kein produktfehler: develop = fac01c772 (695ad5494 + 86858f129 + bcd0e29ca + fac01c772), der unterschied zu ihrem base beruehrt .github/workflows/ci.yml und scripts/test_ci_check_routes.py, also genau EIN weiterer lauf. ihr lauf 44536437699: unit/docs/format/readability PASS; der 'runtime-integration'-schritt fiel wegen ORAS/trust-plane runner-precondition aus — das ist eine ÄUSSERE BLOCKADE (punkt (a) des 114-drahts), von ihr korrekt gemeldet und von mir NICHT als ihr defect gebucht. IHRE FINDING, von mir an der datei geprueft statt geraten: 'scripts/pr-candidate-advisory.py' existiert auf develop (142 zeilen); .github/workflows/ci.yml:1111 ist die base_ref-bedingung, :1133 ruft das advisory-skript, :731/:795/:805 fuehren den output 'candidate_advisory_required'. ANTWORT an sie: ihre lane-validations sind in IHREM eigenem PR advisory (policy, owner-direktive 15:3xZ), das erklaert auch ihr 'integration_sha_mismatch' — kein STOP-grund. akte auf plan-main 981b0e85

REVIEW-KANDIDAT: head 4ce0ca0…, base = develop fac01c77276ca2bf1e20cd0b7334bda5dd43e353 (aktuell), draft=false, 'merge-base --is-ancestor origin/develop <kopf>' = 0 (monoton, ein hopf), 'PR Selected Checks' = success auf exakt diesem kopf, 'PR · Source format' success, 0 fehljobs. INHALT von der abnahme schon APPROVE CONTENT (ea6cddd20), app.perses = 4 typed ops erhalten. REIHENFOLIE-PFLICHT, von mir GEMESSEN: sie teilt 12 dateien mit #1599 (0428-089), davon drei GLEICH (internal/application/perses_lifecycle.go blob 9a8ee71, cmd/baha/commands.go 05ec558, cmd/baha/completion.go a692437) und zwei inhaltlich VERSCHIEDEN: cmd/baha/perses_lifecycle.go (084 = 295 zeilen gegen 089 = 190 zeilen) und internal/capability/perses.go. Das ist gestapelte/funktionell ueberlappende arbeit, kein zufallsgleichnam. DARUM GEHT #1598 VOR #1599 (land/reconcile, dann 089 rebase + review ihres sicherheits-/serviceaccess-rests gegen das genaue ergebnis). akte: evidence/r28-welle4-2026-11-19/perses-lifecycle-hopf/ auf plan-main
