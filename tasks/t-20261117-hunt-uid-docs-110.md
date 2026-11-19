---
id: t-20261117-hunt-uid-docs-110
release: v0.4.28
repos: [mcpdev80/baseharbor]
card_number: "0428-110"
title: "Corrupt-config and mutation paths stay silent despite fail-loud guarantee"
kanban_status: active
kanban_lane: active
kanban_title: 0428-110 · Corrupt-config and mutation
kanban_summary: ""
sources: []
source_note: "hunt hunt-uid-docs (akte: evidence/r28-welle3-2026-11-16/hunt-uid-docs/befund-1.md)"
depends_on: []
owner: 0428-110 korrektur (codeman 14c1d53d-c346-4785-b0e3-f2673d5f9b77, ornith)
blocker: ""
wait_reason: ""
resolution: ""
superseded_by: ""
prs: [mcpdev80/baseharbor#1682]
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-uid-docs/befund-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-uid-docs-110/fix-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1682-0428-110.md"]
card_short_title: Corrupt-config and mutation
---

- [ ] t-20261117-hunt-uid-docs-110 · Corrupt-config and mutation paths stay silent despite fail-l #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** 0428-110 korrektur (codeman 14c1d53d-c346-4785-b0e3-f2673d5f9b77, ornith)  
    **PR:** [baseharbor#1682](https://github.com/mcpdev80/baseharbor/pull/1682)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-uid-docs/befund-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-uid-docs-110/fix-1.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1682-0428-110.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** 0428-110 korrektur (codeman 14c1d53d-c346-4785-b0e3-f2673d5f9b77, ornith)  
**Priority:** not set  
**PRs:** [baseharbor#1682](https://github.com/mcpdev80/baseharbor/pull/1682)  
**Source:** 
<!-- /generated:links -->

CODEX-REVIEW welle 4 = REQUEST CHANGES auf dem gepueften kopf (urteil 1682-0428-110.md). korrekture-runde ist vorgemerkt und wartet auf einen freien sitz: die vier perses-karten und 083 teilen sich dateien mit den laufenden lanen, darum kein paralleler start ohne write-set-nachweis. 083: 'runtime provisioning absent' (datasource wird gebaut, aber nicht in Perses bereitgestellt); 073: 'alert rule nicht ausgefuehrt/nicht persistiert' (persesAlertRealEvaluation); 077: 'catalog-availability aus host provider-metrics allein'; 089: 'PersesComposeServices rendert keine config (--config=/etc/perses/config.yaml) + loopback upstream'

REQUEST CHANGES abgeholt: XDG-ghost-guard auf den XDG-pfad beschraenken + state-dir-regression; branch lane-0428-110-mutation-loud @ fb6f36936 NICHT monoton -> hopf zuerst; target.go ist fuer diese lane gesperrt (057 schreibt dort)
