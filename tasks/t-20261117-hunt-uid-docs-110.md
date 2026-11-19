---
id: t-20261117-hunt-uid-docs-110
release: v0.4.28
repos: [mcpdev80/baseharbor]
card_number: "0428-110"
title: "Corrupt-config and mutation paths stay silent despite fail-loud guarantee"
kanban_status: closed
kanban_lane: closed
kanban_title: 0428-110 · Corrupt-config and mutation
kanban_summary: ""
sources: []
source_note: "hunt hunt-uid-docs (akte: evidence/r28-welle3-2026-11-16/hunt-uid-docs/befund-1.md)"
depends_on: []
owner: 0428-110 r2 (codeman 14c1d53d, END akzeptiert)
blocker: ""
wait_reason: ""
resolution: accepted
superseded_by: ""
prs: [mcpdev80/baseharbor#1682]
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-uid-docs/befund-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-uid-docs-110/fix-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1682-0428-110.md", "https://github.com/mcpdev80/baseharbor/pull/1682", "https://github.com/mcpdev80/baseharbor-plan/blob/0a65a9ad503c9ad81c86ede4692a61093484a600/evidence/r28-welle4-2026-11-19/codex-review-wave/1682-0428-110-r2.md"]
card_short_title: Corrupt-config and mutation
---

- [x] t-20261117-hunt-uid-docs-110 · Corrupt-config and mutation paths stay silent despite fail-l #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** 0428-110 r2 (codeman 14c1d53d, END akzeptiert)  
    **PR:** [baseharbor#1682](https://github.com/mcpdev80/baseharbor/pull/1682)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-uid-docs/befund-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-uid-docs-110/fix-1.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1682-0428-110.md), [proof 4](https://github.com/mcpdev80/baseharbor/pull/1682), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob/0a65a9ad503c9ad81c86ede4692a61093484a600/evidence/r28-welle4-2026-11-19/codex-review-wave/1682-0428-110-r2.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.28  
**Depends on:** none  
**Owner:** 0428-110 r2 (codeman 14c1d53d, END akzeptiert)  
**Priority:** not set  
**PRs:** [baseharbor#1682](https://github.com/mcpdev80/baseharbor/pull/1682)  
**Source:** 
<!-- /generated:links -->

CODEX-REVIEW welle 4 = REQUEST CHANGES auf dem gepueften kopf (urteil 1682-0428-110.md). korrekture-runde ist vorgemerkt und wartet auf einen freien sitz: die vier perses-karten und 083 teilen sich dateien mit den laufenden lanen, darum kein paralleler start ohne write-set-nachweis. 083: 'runtime provisioning absent' (datasource wird gebaut, aber nicht in Perses bereitgestellt); 073: 'alert rule nicht ausgefuehrt/nicht persistiert' (persesAlertRealEvaluation); 077: 'catalog-availability aus host provider-metrics allein'; 089: 'PersesComposeServices rendert keine config (--config=/etc/perses/config.yaml) + loopback upstream'

REQUEST CHANGES abgeholt: XDG-ghost-guard auf den XDG-pfad beschraenken + state-dir-regression; branch lane-0428-110-mutation-loud @ fb6f36936 NICHT monoton -> hopf zuerst; target.go ist fuer diese lane gesperrt (057 schreibt dort)

END akzeptiert, von mir qualifiziert: head 7cc41858b771bb0e2cc4e1d8ffac0f4feadbf4e1, monoton auf dem neuen develop e1dc2cf61, merge-tree 0 konflikte, PR draft=false/clean, exaktkopf-lauf 44520608459 SUCCESS (0 fehljobs, 'PR Selected Checks' success, 'PR · Selected Runtime (atomic)' success). rezept-punkte belegt: internal/deployment/config_mutation.go:72-78 (route-spezifisches predicate, aufruf in zeile 78) und der neue state-dir-test TestSaveStateRouteFirstWriteNotRejectedAsGhost in internal/deployment/config_mutation_test.go:223. target.go NICHT beruehrt (meine sperre gehalten). CODEX-REVIEW auf diesem kopf beauftragt (1682-0428-110-r2.md); sitzfreigabe nach der urteils-rueckmeldung

URTEIL GEKOMMEN: END_APPROVE_CONTENT #1682 / 7cc41858b771bb0e2cc4e1d8ffac0f4feadbf4e1 / run 44520608459 SUCCESS / 'merge deferred to owner window'. window ist offen (#1691 ist seit 11:56:52Z in develop) — CODEX-MERGE fuer GENAU diesen kopf angeordnet, receipt kommt in die urteilsdatei, neuen develop-sha melde ich an alle lanen

GEMERGT: CODEX-REVIEW END_APPROVE_CONTENT auf 7cc41858b771bb0e2cc4e1d8ffac0f4feadbf4e1 (run 44520608459 SUCCESS, aggregate success + Selected-Runtime success), CODEX-MERGE per squash mit expected-head 12:36:33Z, merge-commit = neuer develop f518e859df7adabed6e891ae30c010f0a075bdcc. SQUASH-PRAEZEDENZ angewandt (ancestor schlaegt fehl): internal/deployment/config_mutation.go UND config_mutation_test.go sind zwischen PR-kopf und develop DATEI-HASH-IDENTISCH, also inhalt in develop ohne verlust. reviewerin-vermerk 'resolve the outdated owner review thread' ist erfuellt (zustimmender thread behoben), karte closes
