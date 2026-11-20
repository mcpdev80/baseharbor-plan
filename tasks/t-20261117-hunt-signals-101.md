---
id: t-20261117-hunt-signals-101
release: v0.4.28
repos: [mcpdev80/baseharbor]
card_number: "0428-101"
title: "ID-Raum-Heterogenitaet und Keycloak-Kollision in Signal-IDs"
kanban_status: closed
kanban_lane: closed
kanban_title: 0428-101 · ID-Raum-Heterogenitaet und
kanban_summary: ""
sources: []
source_note: "hunt hunt-signals befund-1 (akte: evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md)"
depends_on: []
owner: codex-open-pr-sweep-0428-101
blocker: ""
wait_reason: ""
resolution: accepted
superseded_by: ""
prs: [mcpdev80/baseharbor#1707]
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1707", "https://github.com/mcpdev80/baseharbor/actions/runs/44643902576", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/pr-sweep/0428-101-keycloak-project-signal.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md"]
card_short_title: ID-Raum-Heterogenitaet und
---

- [x] t-20261117-hunt-signals-101 · ID-Raum-Heterogenitaet und Keycloak-Kollision in Signal-IDs #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** codex-open-pr-sweep-0428-101  
    **PR:** [baseharbor#1707](https://github.com/mcpdev80/baseharbor/pull/1707)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1707), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44643902576), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/pr-sweep/0428-101-keycloak-project-signal.md), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261117-hunt-signals-103](t-20261117-hunt-signals-103.md), [t-20261117-hunt-signals-104](t-20261117-hunt-signals-104.md)  
**Owner:** codex-open-pr-sweep-0428-101  
**Priority:** not set  
**PRs:** [baseharbor#1707](https://github.com/mcpdev80/baseharbor/pull/1707)  
**Source:** 
<!-- /generated:links -->

Einzelschritte in der referenzierten hunt-akte (befund-1.md); Umsetzung als normale task-kette (claim -> branch -> CI -> evidence -> review).

## Handoff

The earlier file-overlap blocker was stale: at the time of implementation, open #1650's current diff did not touch `internal/identityprovider/keycloak_realization.go`, and no live Codeman worker owned this file. On develop `bbc937c8f1b1f1604bd5b68f4c66259dc3a3e978`, changed the Keycloak observability registry identity from the global `keycloak-metrics` value to `keycloak:<compose-project>`, matching project-scoped Loki/Tempo identities. Added `TestKeycloakSignalRegistrationKeepsProjectsDistinct`; it failed on the base because registration of the second project replaced the first, and passes with the fix. No registry or workflow changes.

Implementation is in draft [PR #1707](https://github.com/mcpdev80/baseharbor/pull/1707), exact head `162ac67022aceb0dbddc4e78a00fdc62391ce25e`. Local verification on that exact commit: `go test ./internal/identityprovider -count=1` PASS; `go vet ./internal/identityprovider` PASS; `git diff --check` PASS. CI route: `internal/identityprovider` is auto-discovered by the existing `PR · Go unit · packages` shard; `scripts/pr-gate-plan.py` maps changed production files in this package to identity-provider package checks, Go build/vet, CLI checks and Docker/Podman lifecycle gates. Exact PR run [44643902576](https://github.com/mcpdev80/baseharbor/actions/runs/44643902576) completed successfully on exact head `162ac67022aceb0dbddc4e78a00fdc62391ce25e`: draft-source/routing and all five Draft Go shards passed. Draft policy skipped ordinary source/selected/native/runtime gates. Keep this card in review and the PR draft until the review step; before merge, make it Ready and require fresh exact-head CI including the selected impact gates.

gemergt, von mir gemessen: PR #1707 merged=true, merge-commit b7cbc00f0adf, und 'git merge-base --is-ancestor b7cbc00f0adf origin/develop' = JA — der inhalt ist also auf der jetzigen develop-spitze 6b8188df26a1 enthalten. Die drei funde dieser jagd (#1707 selbst war befundlos in seiner sach, aber die jagd fand drei Fol defizite in ihm) sind als karten 0428-166/167/168 gegossen, 0428-168 ist bereits aktiv besetzt
