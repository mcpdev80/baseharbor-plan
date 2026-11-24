---
id: t-20261124-0428-278-perses-provision-ghost-coverage-rows
card_number: "0428-278"
card_short_title: "gate-plan accepts ghost source rows"
type: bug
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "scripts/pr-gate-plan.py silently absorbs a declared source row whose file is absent on develop, mapping it to the parent internal/metrics gate (effectively no owner). Post-merge desk found #1822's two perses_dashboard_provision rows are ghosts until #1819 lands."
kanban_title: 0428-278 · gate-plan accepts ghost source rows
priority: low
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: "Owner-scope: fix would edit scripts/pr-gate-plan.py (validation) — confirm whether the current behaviour is intended forward-registration for the stacked #1819 producer or needs a fail-loud missing-file guard."
wait_reason: ""
resolution: ""
evidence:
  - baseharbor-plan evidence/r28-welle6-2026-11-24/postmerge-verify-2b9a2c6d.md (commit 6bd78abf)
---

## Problem (read-only post-merge desk finding, §3.3.5 Fund→Karte)

- Where: `scripts/pr-gate-plan.py` — when a `scripts/pr-gate-coverage.json` row declares `source.internal_metrics_perses_dashboard_provision_go` → `internal/metrics/perses_dashboard_provision.go` (and the `_test.go` twin) but that file is ABSENT on the current develop tree, the tool matches the changed file via `changed.startswith(row["path"])` longest-prefix absorption and silently maps it to the parent `internal/metrics` data-capabilities gate, WITHOUT flagging the missing declared file.
- Consequence: #1822 (6-row baseline) currently carries TWO ghost rows (perses_dashboard_provision.go + _test.go) that own no gate until #1819 (which adds those files) merges. A typo'd or stale path would likewise be tolerated instead of failing loud.
- Severity: Low. The rows are intended forward-registration for the stacked #1819 producer; they become live on #1819 merge. Risk is the silent-tolerance of a wrong/missing path.

## Acceptance (owner-scope; no worker may edit scripts/**)

- Decide: either (a) confirm forward-registration is intended and add a one-line comment tying the two rows to card 0428-181/#1819, or (b) add a fail-loud guard in scripts/pr-gate-plan.py that errors when a declared row's source file is absent from the candidate tree.
- This card resolves when #1819 merges (rows go live) IF option (a) is chosen; option (b) needs a scripts/** PR by the owner.
