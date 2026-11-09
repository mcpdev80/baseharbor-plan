---
id: t-20261109-0427-180-dangling-app-lock
card_number: "0427-180"
card_short_title: "0427-180 · Killed app"
type: bug
areas: []
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-0427-180-impl
kanban_status: active
kanban_lane: active
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0427-180 · 0427-180 · Killed app
priority: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261109-0427-179-flock-not-enforced]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1517]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261109-0427-180-dangling-app-lock · 0427-180 · Killed app lifecycle holder leaves dangling per-app lock that blocks the target #task #release/v0-4-27 #status/active #view/active #kind/bug
    <!-- generated:card -->
    **Owner:** lane-0427-180-impl  
    **PR:** [baseharbor#1517](https://github.com/mcpdev80/baseharbor/pull/1517)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261109-0427-179-flock-not-enforced](t-20261109-0427-179-flock-not-enforced.md)  
**Owner:** lane-0427-180-impl  
**Priority:** not set  
**PRs:** [baseharbor#1517](https://github.com/mcpdev80/baseharbor/pull/1517)  
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

## Task Note
Hunt H-P5 (evidence: hp5.md FINDING 2, proven): a holder killed with SIGKILL leaves the per-app dotfile `.scope.app_installation.lock` on disk (cleanup only runs on clean release). The target-wide scan `deploymentsHaveAppLocks` then reports held=true forever: all later lifecycle operations on the target fail closed with no self-service recovery. Required: stale-detection (holder pid recorded in dotfile + liveness check) and an automatic reclaim path in the acquire, with a regression proving kill -9 followed by a new lifecycle call succeeds after reclamation.
