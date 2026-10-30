---
id: t-20261030-postrun-nonpr-producer-skip
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: ""
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261030-postrun-nonpr-producer-skip · Receipt Post-Run fails on non-PR producer runs (runtime-validation pushes) instead of clean skip #task #release/v0-4-27 #status/planned #view/waiting #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
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

- receipt-post-run.yml skips cleanly (exit0, neutral) when producer run event != pull_request (e.g. runtime-validation push runs); no failure, no receipt attempted
- negative regression: fake non-PR producer payload yields skipped outcome in the focused suite
- witness runs: 41111017354 and 41111798732 (Extract Trusted Plan failure on push producer, main e92e2058)

## Required checks

- Targeted checks for the changed area; broaden when impact is unknown.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
