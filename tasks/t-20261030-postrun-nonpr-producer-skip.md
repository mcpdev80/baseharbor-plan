---
id: t-20261030-postrun-nonpr-producer-skip
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: q260
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1230]
sources: []
blocker: ""
resolution: pending maintainer acceptance
evidence: [board-2026-10-30/q260.md]
---

- [x] t-20261030-postrun-nonpr-producer-skip · Receipt Post-Run fails on non-PR producer runs (runtime-validation pushes) instead of clean skip #task #release/v0-4-27 #status/review #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** q260  
    **PR:** [baseharbor#1230](https://github.com/mcpdev80/baseharbor/pull/1230)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    **Evidence:** [proof 1](board-2026-10-30/q260.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** pending maintainer acceptance  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** q260  
**Priority:** not set  
**PRs:** [baseharbor#1230](https://github.com/mcpdev80/baseharbor/pull/1230)  
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

- q260: PR #1230 created, CI terminal (Workflow policy pass, PR checks skipping as expected for non-PR trigger branch). Evidence: q260.md. Branch work/postrun-nonpr-skip, commit 9a5abda0.
