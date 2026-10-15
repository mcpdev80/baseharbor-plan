---
id: core-893-interface
type: task
release: v0.4.26
version: ""
parent: core-888
owner: mcpdev80 (session 1)
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#930"]
sources: ["mcpdev80/baseharbor#893"]
source_updated: "2026-10-15T20:35:28Z"
labels: [area/evidence]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-893-interface · CI: agree the planning/execution interface for runner isolation #task #release/v0-4-26 #status/active

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** none  
**Required by:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md)  
**Owner:** mcpdev80 (session 1)  
**PRs:** [baseharbor#930](https://github.com/mcpdev80/baseharbor/pull/930)  
**Source:** [baseharbor#893](https://github.com/mcpdev80/baseharbor/issues/893)
<!-- /generated:links -->

## Goal

Agree the concrete planning/execution interface that core-896 (runner isolation) builds on, before #893's final integration. This is phase 1 of [baseharbor#893](https://github.com/mcpdev80/baseharbor/issues/893); phase 2 is core-893.

## Scope

- In scope: the interface between #893 orchestration (`.github/workflows/ci.yml`, PR planning/execution, `PR Selected Checks`) and #896's isolation helpers, using PR #930 as the reference.
- Out of scope: activating anything in production; final runtime/evidence acceptance (core-893).

## Acceptance

- The interface is agreed at an exact commit of PR #930 and recorded in the handoff below with that SHA.
- PR #930 is treated as a reference, not as a qualified or merged dependency. Inspecting a commit does not authorize unreviewed production activation.
- Any later interface change is agreed first and sequenced through the #893 owner.

## Required checks

- Workflow policy/syntax checks of the referenced head.

## Dependencies and file ownership

- Satisfied prerequisite: #892 (closed as completed 2026-10-15).
- #893 owns `.github/workflows/ci.yml`; #896 must not edit it in parallel. Order fixed by the [2026-10-15 dependency correction](../epics/core-888-development-and-ci.md#binding-dependency-correction--2026-10-15).

## Handoff

- 2026-10-15 (baseharbor#896 comment): session 1 states #896 consumes the exact #930 interface commit `ca2653cbf5d86216d87d4cdddb4e21eb5d6d2e06`. The correction text names `d56737bd147e54733c280383fa86ad2abccc7b33` as the reference. **Open:** no Maintainer record that the interface at `ca2653cb` is agreed; record it here (or the agreed SHA) to accept this entry.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
