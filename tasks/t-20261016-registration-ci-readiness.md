---
id: t-20261016-registration-ci-readiness
type: task
areas: [ci]
release: v0.4.26
version: ""
parent: core-888
owner: "mcpdev80 (registration-ci-readiness)"
priority: ""
depends_on: [t-20261016-wizard-task-ci-readiness]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261016-registration-ci-readiness · CI: qualify shared command and MCP registration checks #task #release/v0-4-26 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (registration-ci-readiness) · **Priority:** not set  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md)  
**Required by:** [core-921](core-921-cli-mcp-register-new-interfaces.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Qualify the exact shared command/CLI/JSON/MCP registration paths of core-921
on the real trusted PR planner, executor and authenticated final verifier before assignment.

## Scope

- Review current develop registration paths and exact core-921 file boundaries.
- Ensure command tree, help/discovery goldens, machine coverage, generated reference
  drift and real in-process MCP registration tests are selected and actually run.
- Require a bounded hosted positive/negative workflow-route qualification; no
  broad cmd/baha exemption or runtime matrix.
- Preserve other sessions and integrate independently approved trusted policy.

## Acceptance

- Every mandatory registration family has matching executed tests and authenticated results.
- Any shared command/registry source outside reviewed bounds fails closed.
- Real PR Selected Checks green for exact accepted integration; independent review.
- No registration implementation in this CI prerequisite.

## Handoff

- Scheduled from the independent review of PR #957. This is a **future concrete
  prerequisite for core-921 only**, not a replacement for completing the
  trusted-policy bootstrap within t-20261016-wizard-task-ci-readiness.
