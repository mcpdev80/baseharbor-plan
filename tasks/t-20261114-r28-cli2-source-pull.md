---
id: t-20261114-r28-cli2-source-pull
card_number: "0428-061"
card_short_title: "Implement guided source pull"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w27-pr1627-0428-061-pull
kanban_status: blocked
kanban_lane: blocked
kanban_summary: "Implement guided source pull. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-061 · Implement guided source pull
priority: high
depends_on: [t-20261114-r28-cli2-app-lifecycle, t-20261114-r28-cli2-source-model]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1752]
sources: []
blocker: "Owner-Entscheidung noetig: die zwei neuesten commits b010dabcb und e7df5ab4a6c sind als 'BaseHarbor Worker <worker@example.invalid>' geschrieben (unsigniert, keine karten-identitaet), die fuenf frueheren als '0428-061-sourcepull <0428-061@baseharbor.local>'. das FRUEHERE verdict (a4adc29a584, akte 37ef97e67c) traegt nicht auf die neuen commits ueber, und die review verlangt eine zuordnung (akte identity-followup-e7df5ab4.md, plan c11fcb80ad). optionen: (a) dokumentierte ausnahme wie bei #1596, verdict gilt mit vermerk; (b) branch zuruecksetzen auf den letzten karten-identitaet-kopf und die beiden fixes als neue commits mit 0428-061-sourcepull-identitaet - das braucht einen force-push, also ihre hand. keine lane darf force-pushen."
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-cli2-source-pull · CLI redesign: Implement guided source pull #task #release/v0-4-28 #status/blocked #view/blocked #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** w27-pr1627-0428-061-pull · **Priority:** high  
    **PR:** [baseharbor#1752](https://github.com/mcpdev80/baseharbor/pull/1752)  
    **Blocker:** Owner-Entscheidung noetig: die zwei neuesten commits b010dabcb und e7df5ab4a6c sind als 'BaseHarbor Worker \<worker@example.invalid\>' geschrieben (unsigniert, keine karten-identitaet), die fuenf frueheren als '0428-061-sourcepull \<0428-061@…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-app-lifecycle](t-20261114-r28-cli2-app-lifecycle.md), [t-20261114-r28-cli2-source-model](t-20261114-r28-cli2-source-model.md)  
**Required by:** [t-20261114-r28-cli2-cli-integration](t-20261114-r28-cli2-cli-integration.md)  
**Owner:** w27-pr1627-0428-061-pull  
**Priority:** high  
**PRs:** [baseharbor#1752](https://github.com/mcpdev80/baseharbor/pull/1752)  
**Source:** 
<!-- /generated:links -->

## Goal

Implement guided source pull. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Implement app pull with -c selecting sources, actual entire-repository pull and optional --up same domain operation; preview target/env and shared impacts.

## Entry points and ownership

- Starting points: `cmd/baha/app_update.go; app_workspace_git.go; new dedicated pull coordinator`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Dirty/diverged refs, same repo across components/apps, no-git, partial failures and noninteractive safe consent, --up only after successful pull; preview/metadata side effects truthful.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.

beide basis-karten geschlossen (0428-059 gemergt, 0428-060 als PR #1747 mergeCommit e6c199e7b7dd). Lane arbeitet auf develop-exakter base, ein PR 'lane-0428-061-sourcepull'; akzeptanz-kriterien einzeln belegt (dirty/diverged/no-git/partial/consent/--up erst nach erfolg/unverified explizit).

active again: previous lane (0428-216-sourcepull) was a documented lane loss; fresh laptop lane dispatched with the card mission (base corrected to develop d1acf3f31a36). Dependencies 0428-059 and 0428-060 are closed/merged, so the card is dep-free.

RUECKGANG MEINER STAND-DOWN: der owner hat ausdrtuecklich klargestellt, dass er #1752 NICHT uebernimmt ('I have made no edits', 'I will not write reserved files without your assignment') und dass die karte w27-pr1627-0428-061-pull als inhaber traegt, waehrend commands.go, die machine registry, .github und die generierten indexes bei den jeweiligen integration-/CI-inhabern bleiben - gemeinsame writes laufen ueber mich. ALSO: w27 arbeitet weiter, in zwei schritten. (1) AGENTS.md wiederherstellen: der +0 -125-fall ist real gegen merge-base d1acf3f31a36 (von mir gemessen, 'git diff --numstat develop..refs/pull/1752/head -- AGENTS.md'), die datein gehoert der lane. (2) die BEIDEN restlichen punkte sind reservierte dateien und werden von mir separat vergeben: die machine_coverage-klassifikation fuer 'baha app pull' (exakter hosted run 44955232402 = completed/failure, required 'PR Draft Go · cli-0', cmd/baha TestMachineCoverageCIRealTreeAndJSONClassification, registration_ci_readiness_test.go:82, 'unclassified command: baha app pull') und die generierten EN/DE-indexzeilen. PR bleibt draft, back=4 gegen develop 513488eeb6d, hop folgt.

lane hat geliefert: AGENTS.md wiederhergestellt (commit 16c120f1) und hop auf develop 42da7128e72 -> head d9124a9154d (beide refs gemessen, feature commit 4bae3194fa7 bleibt ancestor, eine kandidaten-kette). der CI-defekt bleibt bestehen und war NICHT von der lane zu beheben: 'unclassified command: baha app pull', registration_ci_readiness_test.go:82, roter beleg run 44955232402; der run 44959026535 auf d9124a9154d ist in progress, ohne klassifikation wird er wieder rot. ENTSCHEIDUNG DES COORDINATORS (04:1xZ): ausnahme von der write-set-reservation erteilt, weil der inhaber der reservierten dateien seit zwei tagen nicht benannt ist und der owner die PR-liste abtragen will (mission sha256 im ledger, owner um veto bis naechster tick gebeten). scope: cliMachineOperations in cmd/baha/machine_coverage.go:95, ein semantisches Operation-objekt in internal/machine/contract.go Operations() mit MCPTool, cliSemanticModes-begruendung, und GENERIERUNG BEIDER docs/reference/cli-machine-coverage.md + docs/de/reference/cli-machine-coverage.md per BASEHARBOR_UPDATE_MACHINE_DOCS. .github/** und scripts/** bleiben gesperrt. der mutationstest muss rot (44955232402) -> gruen am selben test zeigen; danach draft=false, unabhaengiges verdict, ordinary merge.

fortschritt gemessen: die write-set-ausnahme wirkt - head ist 5cb139a6e4e, und die klassifikations-stelle 'unclassified command: baha app pull' (registration_ci_readiness_test.go:82) ist im neuen exakten run 44962445337 nicht mehr der fehler. zwei vertragstests ziehen jetzt nach, beide in cmd/baha: (a) job 137024002111 'PR · Draft Go · cli-0' FAIL TestMCPGenericClientDiscoversCompleteSemanticSurfaceAndExercisesReadOnlyTools (0.14 s) - das neue app-pull operation muss im semantic surface vollstaendig erscheinen (Operations(), MCPTool-name, cliSemanticModes zusammen), (b) job 137024002085 'PR · Draft Go · cli-3' FAIL TestEndToEndInstalledZshAndFishWrappers (0.00 s) - die installierten zsh/fish-wrapper kennen den unterbefehl noch nicht. ZUSAETZLICH ist develop auf 7d4351c6d645 gezogen (#1749 gemergt), also back=8 und ein NEUER hop ist Pflicht, bevor ein verdict oder merge in frage kommt (mission sha256 b65071f7cc3f + detail b0 …). PR bleibt draft=true bis der exakte run gruen ist. meine ausnahme gilt weiter NUR fuer die genannten dateien plus ggf. die completion-tabellen; .github/scripts bleiben gesperrt, und ein veto des owners gegen die ausnahme ist noch moeglich.

exakter head 9140e0c8224, run 44968867153 SUCCESS (21 skipped = HA/release/draft-routing per PR-event), akte 8ce6104ec; unabhaengiges verdict bestellt

independent review REQUEST CHANGES at exact head 9140e0c8224 (evidence 5406131d02, akte review-1752-head9140e0c8.md): F1 app_pull.go:156-167 JSON returns before result.Successful and opts.Up, F2 mcp_lifecycle_extra.go advertises up/component that machineApplicationInput (mcp.go:89-93) cannot carry, F3 source_pull_test.go:146-200 comment overstates partial-failure coverage; correction mission f6e8294fecda dispatched to w27, reviewer session kept for the fresh exact-head review

correction missions to w27: F1/F2/F3 (f6e8294fecda), draft rule (33b8d6833a5b), F2b buffer split (931e8b531eec), F2c/F4 approval enforcement (5caf75836375); reviewer confirmed F4 at evidence d1f4a357ed and holds until the new exact head

corrections F1/F2/F2b/F2c(F4)/F3 pushed as exact head 719242df476 (back=0 against develop 6209874428f, additive on 9140e0c8224); PR stays Draft by Owner decision; exact hosted run 44971297170 queued; codex-rev-1747 reads the head now, verdict only after terminal green

review returned REQUEST CHANGES at 719242df476 (akte aada967193); exact run 44971782040 at head a4adc29a584 is terminal failure in two jobs: Draft Go packages 137052952860 (candidate: partial-failure test asserts wrong state) and Draft Go cli-3 137052952179 (environment: card 0428-229 missing zsh in the draft cell). correction missions 858bf3f62d9d + 5246d5ac2d5e ordered, PR stays draft

lane END reported 'ci-fast-check 295 tests OK'; I asked on which host that ran (mission 42e37d95c429). until it answers, that number is not accepted as evidence; only hosted run 44974701796 counts
