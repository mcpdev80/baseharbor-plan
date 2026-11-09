---
id: core-750
card_number: "0427-001"
card_short_title: "present complete"
areas: [inspect]
type: bug
release: v0.4.27
version: ""
parent: v0.4.27
owner: "t1236-ha-native (Ornith; owner-directive 2026-10-31, prior=marcel)"
kanban_lane: closed
kanban_summary: "baha app inspect projects ports, health, workload/infrastructure classes and capability findings from normalized evidence for…"
kanban_status: closed
kanban_title: "0427-001 · present complete"
depends_on: [core-893, core-895, core-896, t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1222"]
sources: ["mcpdev80/baseharbor#750"]
source_updated: "2026-10-15T16:51:33Z"
labels: [kind/bug, area/dx, area/compatibility]
blocker: "Zwei Teil-Ursachen (t-runner2 Ground-Truth, evidence/board-2026-10-31/t-runner2/): Q1 DOCKER=Owner-Entscheidung (baha-runner-docker-2 faehrt ROOTFUL docker; rootless setuptool verweigert; Linger已从 coordinator enabled, aber Service-Modell rootful-vs-rootless --force = Host-Sicherheitsentscheidung, RUNBOOK 6.2). Q2 PODMAN=worker product fix (openbao-postgres scram/mTLS 28P01, Lane t-openbao-pgauth). sudo/env Codefix gelandet (8155a1dc). sudo-Fix + prep laufen; HA-Jobs failen an Q1/Q2."
resolution: "accepted"
evidence: ["https://github.com/mcpdev80/baseharbor/commit/8bc490ea"]
---

- [x] core-750 · Inspect: present complete source-neutral findings #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/inspect #kind/bug
    <!-- generated:card -->
    **Owner:** t1236-ha-native (Ornith; owner-directive 2026-10-31, prior=marcel)  
    **PR:** [baseharbor#1222](https://github.com/mcpdev80/baseharbor/pull/1222)  
    **Blocker:** Zwei Teil-Ursachen (t-runner2 Ground-Truth, evidence/board-2026-10-31/t-runner2/): Q1 DOCKER=Owner-Entscheidung (baha-runner-docker-2 faehrt ROOTFUL docker; rootless setuptool verweigert; Linger已从 coordinator enabled, aber Service-Modell r…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/8bc490ea)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md), [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** t1236-ha-native (Ornith; owner-directive 2026-10-31, prior=marcel)  
**Priority:** not set  
**PRs:** [baseharbor#1222](https://github.com/mcpdev80/baseharbor/pull/1222)  
**Source:** [baseharbor#750](https://github.com/mcpdev80/baseharbor/issues/750)
<!-- /generated:links -->

## Goal

`baha app inspect` projects ports, health, workload/infrastructure classes and capability findings from normalized evidence for every supported source family, not only Compose.

## Scope

- Bug: inspect normalizes Compose, repository-authored Quadlet and raw Kubernetes into `workload_evidence`, but shared summary projections are gated by `SelectedCompose != ""`, so equivalent Quadlet/Kubernetes repositories under-report (`ports`, `health_checks`, `workload_services`, `infrastructure_services`, capability `findings` stay empty; human output omits Published ports / Health checks / Capabilities). Confirmed at v0.4.20 `12ebe1a87afdf82923a0c341bcc90578005d79ab`; parity fixtures `testdata/adoption-parity/{compose,quadlet,kubernetes}`.
- Root cause: `internal/repositoryinspect/inspect.go` — `NormalizeWorkloadSource(...)` fills `result.WorkloadEvidence`; `result.SelectedCompose` is set only for Compose; the summary projection sits inside `if result.SelectedCompose != ""`. Violates the source-neutral inspect/init contract (#519). Still visible at `1b1ae323` (shared service/port/health projection and workload log suggestion depend on `SelectedCompose`).
- Fix: use normalized `WorkloadEvidence.Components` as the canonical source for shared summary fields for all adapters. Compose-specific parsing may remain only for details not yet in normalized evidence (e.g. database bootstrap details), never as the gate for shared summaries.

## Acceptance

- Compose, Quadlet and Kubernetes parity fixtures produce equivalent shared summary semantics.
- Ports are projected from normalized component evidence for all source families.
- Health/readiness is projected for all source families.
- Workload vs infrastructure component classification is projected for all source families.
- Capability findings implied by normalized infrastructure classes are source-neutral.
- The workload log suggestion is not Compose-only.
- Human / JSON / MCP consume the same Result semantics.
- No repository mutation is introduced.
- Existing Compose behavior remains green.

## Required checks

- Focused repositoryinspect tests and full Go tests/vet.

## Dependencies and file ownership

- Product implementation requires the qualified v0.4.26 PR/review/runner foundation (core-893, core-895, core-896; binding 2026-10-15 correction in [core-888](../epics/core-888-development-and-ci.md)).
- No open task dependencies. Related: core-751, core-752. Earlier release parent #569 (closed).

## Handoff

- Logic still present at develop `33b7ca94b42cc45e908c0d964cfbe0cc8349f231` (2026-10-15). Earlier fix branches: `fix/750-source-neutral-inspect-summary` `4c810c9f749eaaba9f755c628df22770826c3e05`, `…-v0421-r2` `e73bc60595a9426242ec1cd1e0883377cf91ab91`, `…-v0421` `7ffe2417587d0cab80f04808e64187d72b3b0668`. Branch hygiene (2026-10-15): divergent earlier fix branches were inventoried; neither full integration nor safe deletion was proven by ancestry. Compare useful changes against the current contract; no blanket merge/rebase. The remote branches were later removed in the [maintenance cleanup](core-909-maintenance-remove-superseded-branches.md); their original commits are preserved in the Maintainer's local mirror backup.
- No release target: core-901 explicitly gives this bug no new release assignment.


## Resolution (2026-11-02)
- Merged via PR #1222 (merge commit 8bc490ea) after rebase onto develop tip; PRSC success on e1b42d64. Source-neutral inspect findings delivered.
