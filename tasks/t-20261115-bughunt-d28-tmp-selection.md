---
id: t-20261115-bughunt-d28-tmp-selection
card_number: "0427-190"
card_short_title: "bf03 private selection store"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: "lane-0427-187-fix-bf03 (ornith)"
kanban_status: review
kanban_lane: review
kanban_summary: "BF-03 (daemon security): persisted target selection lives in a world-writable /tmp/baha-test- path. Found on develop 0e9ccb582…"
kanban_title: 0427-190 · bf03 private selection store
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1582"]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md"]
---

- [ ] t-20261115-bughunt-d28-tmp-selection · BF-03 persisted target selection in world-writable /tmp path #task #release/v0-4-27 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** lane-0427-187-fix-bf03 (ornith)  
    **PR:** [baseharbor#1582](https://github.com/mcpdev80/baseharbor/pull/1582)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-0427-187-fix-bf03 (ornith)  
**Priority:** not set  
**PRs:** [baseharbor#1582](https://github.com/mcpdev80/baseharbor/pull/1582)  
**Source:** 
<!-- /generated:links -->

## Goal

BF-03 (daemon security): persisted target selection lives in a world-writable /tmp/baha-test-* path. Found on develop 0e9ccb582 during H-D28.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
