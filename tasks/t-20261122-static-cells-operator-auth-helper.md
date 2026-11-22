---
id: t-20261122-static-cells-operator-auth-helper
card_number: "0428-231"
card_short_title: "operator auth in static cells"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: b90e4ba1 (lane) / Owner (draft -> ready)
kanban_status: review
kanban_lane: review
kanban_summary: ""
kanban_title: 0428-231 · operator auth in static cells
priority: ""
depends_on: [t-20261121-develop-full-suite-red]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1761]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1761", "https://github.com/mcpdev80/baseharbor/actions/runs/44994765677", "https://github.com/mcpdev80/baseharbor/actions/runs/44998552411"]
---

- [ ] t-20261122-static-cells-operator-auth-helper · operator auth in static cells #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** b90e4ba1 (lane) / Owner (draft -\> ready)  
    **PR:** [baseharbor#1761](https://github.com/mcpdev80/baseharbor/pull/1761)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1761), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44994765677), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44998552411)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261121-develop-full-suite-red](t-20261121-develop-full-suite-red.md)  
**Owner:** b90e4ba1 (lane) / Owner (draft -> ready)  
**Priority:** not set  
**PRs:** [baseharbor#1761](https://github.com/mcpdev80/baseharbor/pull/1761)  
**Source:** 
<!-- /generated:links -->


## Why

Measured by lane `b90e4ba1` (akte
evidence/r28-welle5-2026-11-22/develop-full-suite-red/diagnose-1.md): the helper
`testIsolatedSelectionContext` exists in 7 files at head f16cef27 of PR #1750 and in 0 files at develop 8b9a8f50645 -
so most of these cells clear when #1750 merges. This card stays open only for the parts that survive that merge.


At head `fec44963` of PR #1746 the full Pre-Release run `44980411417` fails in several cells with the same guard:
`Static · init` job 137080600559, `Static · shell-ux` job 137080600541, `Static · config-matrix` job 137080600642,
plus `Integration · integration/docker/core-bootstrap` job 137080600131 and
`Integration · integration/podman/core-bootstrap` job 137080600055 all print
`Managed-environment machine operations require an authenticated BaseHarbor operator.`

That message comes from `cmd/baha/mcp.go:317`. The helper that satisfies it inside a test process already exists
(`runWithIOAsTestOperator`, used by `cmd/baha/env_destroy_integration_test.go:127`), but these cells still drive the
machine paths through the interactive operator path, so they fail regardless of which product PR runs them.

## Acceptance

- The failing init / shell-ux / config-matrix / core-bootstrap paths use the same non-interactive operator helper that
  #1750 delivers for env destroy, so the guard is satisfied without a terminal.
- Hosted CI shows the five jobs above green at one exact head; no local run counts.

PR 1761 ist drafted (kein fertiger kandidat): branch lane-0428-231-static-auth-helper, head 5794874302f1, base 52a3c544 (back=0), gehosteter run 44994765677 SUCCESS/0 failed. Inhalt: ein exportierter helper in internal/operatorauth/test_operator.py -> test_operator.go plus die fan-out ueber die fnf gemessenen dateien (test_operator_context_test.go, app_env_test.go, app_export_command_test.go, installation_destroy_native_test.go, target_definition_change_test.go). Die Lane-Schreibsperre auf internal/operatorauth/** war fuer GENAU diese datei durch die owner-direktive zur helper-route gehoben. Naechster schritt: CODEX-REVIEW am exakten head, dann ready-schalten (entscheidung liegt beim owner, weil der PR draft ist) und fan-in von PR 1746 auf den helper.

helper ist fertig und gruener gelaufen (run 44998552411 SUCCESS am head d275e50c5ba, branch lane-0428-231-static-auth-helper). PR bleibt DRAFT: das ready-schalten ist des owners hand. Rueckstand: base-pointer 52a3c5446f4, develop ist acc34323968, mergeable_state BEHIND - der dritte hop ist der lane befohlen. Diese karte ist die vorgegebene sequenz-stufe vor PR 1746 (0428-208): erst 1761 rein, dann dessen statische zellen-beweise, dann 1746 hop und static suite.
