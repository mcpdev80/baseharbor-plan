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
**Owner:** mcpdev80 (registration-ci-readiness)  
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

- 2026-10-16 initial authority inventory (not yet qualification): claim owner `mcpdev80 (registration-ci-readiness)` published on Planning main at `5ab9a234e775ce00968ae2dd7d76c61bd086f7dd`. Product develop `scripts/pr-gate-plan.py` has a finite `WIZARD_COMPONENTS` map only for individual app components and falls back to unresolved `cli-unresolved-runtime-impact` for shared `cmd/baha/*.go` registrations. `scripts/pr-check-runner.py` already declares `wizard-registration-tests` with independent `TestAppRegistration`, `TestCommandTree`, `TestMachineCoverage`, `TestMCP` families, but the existing trusted planner does not yet select that lane for core-921 shared files. Present develop includes actual shared `cmd/baha/commands.go`, `app_commands.go`, `human_new.go`, `machine_coverage.go`, `mcp.go`, `mcp_tools.go` and additional tool registries plus docs/reference EN/DE generated references. Existing `mcp_stdio_test.go` includes subprocess-oriented tests, so a blanket `^TestMCP` family alone is not proof of an in-process MCP registration check; no test family or hosted workflow qualification has been claimed PASS. No policy exception, production registration, workflow or runtime test was introduced in this inventory. Precise reviewed file inventory, true in-process MCP test(s), positive/negative hosted route, trusted-base helper/version qualification and final authenticated PR check remain to be implemented and independently reviewed. Keep core-921 blocked; no acceptance.

- Scheduled from the independent review of PR #957. This is a **future concrete
  prerequisite for core-921 only**, not a replacement for completing the
  trusted-policy bootstrap within t-20261016-wizard-task-ci-readiness.
