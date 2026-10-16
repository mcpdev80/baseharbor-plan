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
prs: ["mcpdev80/baseharbor#974"]
sources: []
blocker: "Independent trusted policy and actual hosted registration matrix not qualified"
resolution: ""
evidence: []
---

- [ ] t-20261016-registration-ci-readiness · CI: qualify shared command and MCP registration checks #task #release/v0-4-26 #status/blocked #view/blocked #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (registration-ci-readiness) · **Priority:** not set  
    **PR:** [baseharbor#974](https://github.com/mcpdev80/baseharbor/pull/974)  
    **Blocker:** Independent trusted policy and actual hosted registration matrix not qualified  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md)  
**Required by:** [core-921](core-921-cli-mcp-register-new-interfaces.md)  
**Owner:** mcpdev80 (registration-ci-readiness)  
**Priority:** not set  
**PRs:** [baseharbor#974](https://github.com/mcpdev80/baseharbor/pull/974)  
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

- 2026-10-16 hosted evidence update: exact product PR #974 HEAD `5259e3415471ac05ca6b701530f9d79946c52bfa`, develop/trusted base `e514a8b6d47b28f268b779376b1e95cd20674611`. [GitHub Actions 38924147524](https://github.com/mcpdev80/baseharbor/actions/runs/38924147524): Focused Python SUCCESS including *six actual* Go registration family tests and real temporary-Git execution of workflow shell branch, CLI guided/build/vet, source/contracts, trusted plan and policy SUCCESS. Final PR Selected Checks FAILURE on independently trusted policy; **no authenticated hosted `wizard-registration-tests` job was scheduled and core-921 remains blocked**. Negatives: unknown/nested source, rename/delete/type changes, absent/SKIP tests and absent in-process MCP. PR #974 description updated. Planning generator must pass before reviewer handoff; [planning run 38925676511](https://github.com/mcpdev80/baseharbor-plan/actions/runs/38925676511) reports stale `views/overview.md`, not yet green. Do not treat successful candidate smoke as trusted-policy promotion.

- 2026-10-16 implementation/review handoff (NOT acceptance): [product PR #974](https://github.com/mcpdev80/baseharbor/pull/974), exact current head `5259e3415471ac05ca6b701530f9d79946c52bfa`, clean integrated develop target `e514a8b6d47b28f268b779376b1e95cd20674611`. Claim on Planning main `5ab9a234e775ce00968ae2dd7d76c61bd086f7dd`. Product paths: `scripts/pr-gate-plan.py`, `scripts/pr-check-runner.py`, `scripts/test_pr_gate_plan.py`, `scripts/test_pr_check_runner.py`, `scripts/test_pr_registration_ci.py`, `cmd/baha/registration_ci_readiness_test.go`. No registration, common workflow, registry, generated reference or runtime change. Exact reviewed shared CLI/JSON/MCP paths, including command tree, help, human_new, coverage and MCP source files, and generated English/German command index/MCP/coverage references, map to independently executed mandatory registration families; unknown nested/new/unreviewed files and delete/rename/type changes remain unresolved. Six separate requirements: `TestAppRegistrationCI`, `TestCommandTreeCI`, `TestMachineCoverageCI`, `TestMachineDocumentationTracksRegistryAndCommandTree`, `TestHumanCommandIndexTracksExactCommandMetadata`, `TestMCPRegistrationCI`. Real MCP family uses the SDK's in-process session and tools/list + app.list invocation. Planner and runner fixtures cover exact-path positive selection, unknown/rename/delete negative, missing/SKIP rejection. The shell route extracted from the production `wizard-*-tests` workflow case has a real local Git trusted-base fixture for future positive and missing-MCP negative. **Do not conflate that fixture with an actual hosted wizard-registration-tests matrix job.** Hosted [run 38923696925](https://github.com/mcpdev80/baseharbor/actions/runs/38923696925) passed Focused Python (including Git fixture) but real final PR Selected Checks FAILED because the current trusted base does not recognize newly authored registration policy (correct fail-closed behavior). Current exact-head [run 38924147524](https://github.com/mcpdev80/baseharbor/actions/runs/38924147524) adds candidate Go family execution within hosted focused tests; check final outcome before acceptance. **Blocked evidence:** independently reviewed/published trusted-policy bootstrap must permit the exact registration source and actual production workflow matrix, then real hosted positive and missing-family negative routes and authenticated final must be proven. No PR-self-authored exemption, blanket cmd/baha waiver, full runtime/release matrix, merge or task acceptance. core-921 must remain unassigned on this dependency until evidence is accepted.

- 2026-10-16 initial authority inventory (not yet qualification): claim owner `mcpdev80 (registration-ci-readiness)` published on Planning main at `5ab9a234e775ce00968ae2dd7d76c61bd086f7dd`. Product develop `scripts/pr-gate-plan.py` has a finite `WIZARD_COMPONENTS` map only for individual app components and falls back to unresolved `cli-unresolved-runtime-impact` for shared `cmd/baha/*.go` registrations. `scripts/pr-check-runner.py` already declares `wizard-registration-tests` with independent `TestAppRegistration`, `TestCommandTree`, `TestMachineCoverage`, `TestMCP` families, but the existing trusted planner does not yet select that lane for core-921 shared files. Present develop includes actual shared `cmd/baha/commands.go`, `app_commands.go`, `human_new.go`, `machine_coverage.go`, `mcp.go`, `mcp_tools.go` and additional tool registries plus docs/reference EN/DE generated references. Existing `mcp_stdio_test.go` includes subprocess-oriented tests, so a blanket `^TestMCP` family alone is not proof of an in-process MCP registration check; no test family or hosted workflow qualification has been claimed PASS. No policy exception, production registration, workflow or runtime test was introduced in this inventory. Precise reviewed file inventory, true in-process MCP test(s), positive/negative hosted route, trusted-base helper/version qualification and final authenticated PR check remain to be implemented and independently reviewed. Keep core-921 blocked; no acceptance.

- Scheduled from the independent review of PR #957. This is a **future concrete
  prerequisite for core-921 only**, not a replacement for completing the
  trusted-policy bootstrap within t-20261016-wizard-task-ci-readiness.
