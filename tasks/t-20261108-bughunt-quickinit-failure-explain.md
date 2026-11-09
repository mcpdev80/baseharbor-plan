---
id: t-20261108-bughunt-quickinit-failure-explain
card_number: "0427-141"
card_short_title: "Quick init no reason"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: The error names candidates and the missing distinction; docs/help line points to app plan as the dry run; regression for the…
kanban_title: 0427-141 · Quick init no reason
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1466]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md", "https://github.com/mcpdev80/baseharbor/actions/runs/42480521183", "https://github.com/mcpdev80/baseharbor/commit/ad49d2d2129657e2e09c40b534c6a8030413a083"]
---
- [x] t-20261108-bughunt-quickinit-failure-explain · Bug Hunt v0.4.27: Quick init names no reason #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1466](https://github.com/mcpdev80/baseharbor/pull/1466)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42480521183), [proof 3](https://github.com/mcpdev80/baseharbor/commit/ad49d2d2129657e2e09c40b534c6a8030413a083)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1466](https://github.com/mcpdev80/baseharbor/pull/1466)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
The error names candidates and the missing distinction; docs/help line points to app plan as the dry run; regression for the message text.

## Problem (source evidence in the dossier)
app init --quick only says no unambiguous requirements without context on which decision failed; docs: up has no dry-run, app plan is the substitute. Source: hunt H-D3 BF-10/BF-11.

## Acceptance
The error names candidates and the missing distinction; docs/help line points to app plan as the dry run; regression for the message text.

## Dependencies and file ownership
None. Write-set: cmd/baha init message + docs.

## Audit note (Karten-Audit 2026-11-08)
Audit 2026-11-08 (zuerklaeren): open owner PR #1466 carries the actionable quick-init diagnosis; card stays claimed by chatgpt-r27-cli-diagnostics until that exact head is green. [Dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/karten-audit-2026-11-08.md)


## Acceptance — 2026-11-08

- [PR #1466](https://github.com/mcpdev80/baseharbor/pull/1466) merged into `develop`: `ad49d2d2129657e2e09c40b534c6a8030413a083`; exact PR head `daacddbbe9d011c3fd48ae7cc798e560dd591258`.
- [CI #42480521183](https://github.com/mcpdev80/baseharbor/actions/runs/42480521183): terminal SUCCESS (Go-unit, build, vet, source/docs checks, native Docker/Podman destroy-retry). No standalone end-to-end deployment result is claimed.
- Quick-init error now reports detected SQL/cache/object-storage/workload/metrics/telemetry/secret candidate counts; guidance specifies interactive init and app plan as the dry-run. Targeted regression TestQuickInitFailureExplainsObservedRequirementsAndDryRun PASS.
- `resolution: accepted`; no active worker claim remains.

## Review status
CODEX-REVIEW 2026-11-08 on #1466 head daacddbbe: URTEIL korrektur - recipe in [act-1466-review.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/act-1466-review.md) (candidate ids in quick-init error, Next-text assertions, exact-head green required before approve).
