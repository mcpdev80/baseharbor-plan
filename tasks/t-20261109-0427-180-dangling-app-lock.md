---
id: t-20261109-0427-180-dangling-app-lock
card_number: "0427-180"
card_short_title: "0427-180 · Killed app"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: queued
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0427-180 · 0427-180 · Killed app
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261109-0427-180-dangling-app-lock · 0427-180 · Killed app lifecycle holder leaves dangling per-app lock that blocks the target #task #release/v0-4-27 #status/planned #view/queued #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Later release** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** queued  
**Release:** v0.4.27  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

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
