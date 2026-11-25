---
id: t-20261124-0428-278-perses-provision-ghost-coverage-rows
card_number: "0428-278"
card_short_title: "gate-plan ghost source rows"
type: bug
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: ""
kanban_title: 0428-278 · gate-plan ghost source rows
priority: low
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-24/postmerge-verify-2b9a2c6d.md
---

- [ ] t-20261124-0428-278-perses-provision-ghost-coverage-rows · gate-plan ghost source rows #task #release/v0-4-28 #status/planned #view/ready #area/ci #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** low  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-24/postmerge-verify-2b9a2c6d.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** low  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Problem (read-only post-merge desk finding, §3.3.5 Fund→Karte)

- Where: `scripts/pr-gate-plan.py` — when a `scripts/pr-gate-coverage.json` row declares `source.internal_metrics_perses_dashboard_provision_go` → `internal/metrics/perses_dashboard_provision.go` (and the `_test.go` twin) but that file is ABSENT on the current develop tree, the tool matches the changed file via `changed.startswith(row["path"])` longest-prefix absorption and silently maps it to the parent `internal/metrics` data-capabilities gate, WITHOUT flagging the missing declared file.
- Consequence: #1822 (6-row baseline) currently carries TWO ghost rows (perses_dashboard_provision.go + _test.go) that own no gate until #1819 (which adds those files) merges. A typo'd or stale path would likewise be tolerated instead of failing loud.
- Severity: Low. The rows are intended forward-registration for the stacked #1819 producer; they become live on #1819 merge. Risk is the silent-tolerance of a wrong/missing path.

## Owner decision — 2026-11-25

Choose the fail-loud behavior. The planner must report a clear error when a coverage row points to a source absent from the candidate tree; it must not silently absorb a missing/typoed path into a parent gate. Forward registration is valid only when the declared source is present in the same candidate and its intended gate is selected.

## Acceptance

- Add the candidate-tree presence guard in `scripts/pr-gate-plan.py` and cover missing and present source rows.
- The missing source case fails with the path and source ID; the present source case selects its declared gate.
- Use the existing Trusted Plan and selected-check workflows; no new pipeline or self-hosted runner.
- Prove positive selection for a relevant source change and that unrelated changes do not select unnecessary native gates.
- Record exact candidate SHA, test, selected gate, trigger, and actual run.

## Handoff

- **Handoff (Codex-Lane w118):** No product change was made; the earlier separate CI-owner prerequisite is superseded by the owner decision above. Add the candidate-tree presence guard and its regression in the same implementation PR. Coordinate edits to the shared CI planner with its owner, while preserving the existing Trusted Plan and selected-check workflows; no parallel pipeline is authorized. 0428-265's source/path mapping belongs to its own implementation PR.
