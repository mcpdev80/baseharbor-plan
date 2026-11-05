---
id: t-20261105-r27-compose-host-isolation
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: ""
owner: coord-welle4 (Lane w169, freigegeben)
kanban_status: review
kanban_lane: review
kanban_summary: "TestRepositoryWorkflowRealLifecycle, TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI,…"
kanban_title: "CI: composed InCI tests must run against an isolated runtime state, never a shared live daemon"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1383]
sources: []
blocker: ""
resolution: ""
evidence: [https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/execution-journal/baseline-1.md]
---

- [ ] t-20261105-r27-compose-host-isolation · CI: composed InCI tests must run against an isolated runtime state, never a shared live daemon #task #release/v0-4-27 #status/review #view/review #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w169, freigegeben) · **Priority:** high  
    **PR:** [baseharbor#1383](https://github.com/mcpdev80/baseharbor/pull/1383)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/execution-journal/baseline-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coord-welle4 (Lane w169, freigegeben)  
**Priority:** high  
**PRs:** [baseharbor#1383](https://github.com/mcpdev80/baseharbor/pull/1383)  
**Source:** 
<!-- /generated:links -->

## Goal

`TestRepositoryWorkflowRealLifecycle`, `TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI`,
`TestRepositoryComposeWorkloadOnlyLifecycleInCI`, `TestRepositoryBuildWorkloadRebuildsSourceChangesInCI`
yield deterministic pass/fail on any host: each test's runtime view comes from state it created itself,
never from a shared or pre-existing daemon/core (measured: a live local-core on a shared rootless daemon
flips the runtime gate red for unrelated candidates).

## Scope

- In scope: the four named tests and their shared harness (per-test isolated daemon/socket/state dir or
  equivalent native isolation); honest fail-closed semantics preserved (no skips — that rule is closed
  under `t-20261104-r27-db-skip-sites`).
- Out of scope: workflow files and runner configuration (owner field); product runtime behavior; the
  fail-closed apply panic path in `cmd/baha/deployment_record.go:140` (documented pre-existing state,
  separate concern with its own reproduction).

## Measured provenance (2026-11-05)

- Baseline matrix (lane w157): develop 512dcd72 and PR #1373 head 52e972fd behave byte-identically
  (SKIP when env unset, FAIL at the runtime gate under shared live state) — cross-branch, not candidate-bound.
- Corroborations: lane w145 hosted failure with identical signature on coreinstallation paths; lane w147
  reported the same runner family twice (runs 41938947818, 41940701025).

## Acceptance

- On a host WITH a foreign live core/daemon: the four tests still pass when the product is correct
  (isolation proven) — measured, not claimed.
- Without container capability: fail-closed with a named error (no skip), consistent with the skip-sites rule.
- Red-first: harness change shown green-on-candidate for a scenario that is red on the previous develop state
  with shared live state present.
- Existing lifecycle semantics asserted by these tests remain asserted (no weakened expectations).

## Required checks

- `go test ./cmd/baha -run 'TestRepository(WorkflowRealLifecycle|Compose|BuildWorkload)' -count=2` under
  (a) clean state, (b) deliberately polluted shared state — transcripts in evidence.
- go build, vet, gofmt; hosted runs of the exact head to terminal.

## Kandidat pruefbar 2026-11-05 (kopf 9bf29c89846, basis-auffrischung drin)
Zellenstand nach dem nachtrag: zustimmungs-ursache fixiert, verseuchter develop JETZT rot gemessen (war
zuerst gruen — grund war die aeltere basis), head gruen; isolierungs-frage wird im urteil als eigener
abschnitt gefuehrt.

## Rueckruf 2026-11-05 (1383a REJECT: zustimmung belegt, isolierung OFFEN)
Der fixture-harness nutzt den Umgebungs-Daemon; am verseuchten kandidaten bleibt die schranke rot. Runde 2:
pro lebenszyklus-test eigener daemon/socket- oder gleichwertiger namespace OHNE shared state zu loeschen;
beweis: vier tests zweimal, sauber + absichtlich verseucht, am exakten kopf.

## Runde 2 pruefbar 2026-11-05 (kopf 789ae14655b)
Nachgemessen: ls-remote echt==head, eigener test-commit auf der kette, lauf 42002171842 terminal SUCCESS
am exakten kopf (frische shared runner = neutraler beweis der wiederhergestellten isolation), akte
round-2.md publiziert. Basis noch develop 24c7d0492f3 (ancestor gegen 42bfcb1cb4 NEIN) — develop-merge
obliegt dem merge-zweig, wie in der akte vermerkt.
