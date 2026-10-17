---
id: core-754
areas: [mcp]
type: bug
release: v0.4.x
version: ""
parent: v0.4.x
owner: "mcpdev80 (core-754 MCP preconditions)"
depends_on: [core-893, core-895, core-896]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#754"]
source_updated: "2026-10-15T16:51:15Z"
labels: [kind/bug, area/mcp, area/dx, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-754 · MCP: classify expected preconditions correctly #task #release/v0-4-x #status/active #view/active #area/mcp #kind/bug
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-754 MCP preconditions)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md)  
**Owner:** mcpdev80 (core-754 MCP preconditions)  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#754](https://github.com/mcpdev80/baseharbor/issues/754)
<!-- /generated:links -->

## Goal

Expected machine/MCP preconditions get stable typed codes instead of being flattened to `internal_error`.

## Scope

- Bug: `machine.Classify` only preserves already-typed `*machine.Error` values, so expected preconditions become `internal_error`: organization configuration not configured; unsupported organization source kind; application without registered deployment; repository manifest not found for workspace operations. CLI output stays actionable but automation cannot distinguish expected state from internal failure.
- Required mapping: missing registered application/deployment → `not_found`; repository manifest/workspace source absent → `source_missing`; organization configuration absent → `validation_failed`; unsupported organization source kind → `unsupported_operation`; real internal/unclassified failures stay `internal_error`.
- Triage (2026-10-15): some classification is now implemented in `cmd/baha/main.go` at `1b1ae323` (workspace/manifest absence, organization configuration errors). Source inspection alone does not prove every case: verify the listed outcomes, cancellation and unexpected-error behavior with bounded CLI/MCP checks and record the actual remaining failures.

## Acceptance

- `baseharbor.organization.inspect` without org config is not `internal_error`.
- Unsupported organization source kind is not `internal_error`.
- `baseharbor.status` / `policy.explain` for an unknown app return `not_found`.
- `baseharbor.workspace.status` outside an app repository returns `source_missing`.
- CLI and MCP use the same underlying typed error semantics.
- Context timeout/cancellation behavior remains unchanged.
- Unknown unexpected errors still classify as `internal_error`.
- The source's "lands directly in active v0.4.21" item is historical.

## Required checks

- Focused machine/MCP tests and `go vet`.

## Dependencies and file ownership

- Product implementation requires the qualified v0.4.26 PR/review/runner foundation (core-893, core-895, core-896; binding 2026-10-15 correction in [core-888](../epics/core-888-development-and-ci.md)).
- No open task dependencies. Related: core-750, core-751, core-752.

## Handoff

- 2026-10-17 Maintainer coordination: core-754 CI session is explicitly granted temporary exclusive write ownership of `scripts/pr-gate-plan.py` and directly related planner regressions. Parallel planner edits for [#983](https://github.com/mcpdev80/baseharbor/pull/983) are paused; its branch/content must remain unchanged and is not accepted. Implement minimal separate CI PR from current develop to execute both exact #985 MCP tests while retaining `coverage-unresolved` and strict required check failure. Later integrate independently reviewed #983 changes normally with conflict analysis; do not overwrite or implicitly approve them.

- 2026-10-17 CI route ownership check (no edit to CI): exact [#985](https://github.com/mcpdev80/baseharbor/pull/985) `5a3813385af5392a9be3095bd038424a4f9950b7`, [Actions 39034547657](https://github.com/mcpdev80/baseharbor/actions/runs/39034547657) selected no Go tests because `scripts/pr-gate-plan.py` classifies new `cmd/baha/mcp_preconditions_test.go` as `registration-mixed-unresolved` without mandatory checks. Existing planner/executor/verifier route can execute selected checks, but a bounded separate selection rule requires modifying **`scripts/pr-gate-plan.py`**. That same CI policy file is still owned in review by [t-20261017-inspect-import-ci-coverage](t-20261017-inspect-import-ci-coverage.md) / [PR #983](https://github.com/mcpdev80/baseharbor/pull/983) at `25e5f8e1d71340afff415648374f4dcfa2407aee`. **Concrete competing path claim: `scripts/pr-gate-plan.py`.** Per Maintainer instruction, do not overwrite the other task; no CI branch/PR, source edits or policy exception were published. Separation required for a future coordinated change: select exact `TestExpectedPreconditionsShareTypedCLIMCPErrors` and `TestMCPReadEntryExpectedPreconditions`, require actual named results, and leave content qualification `coverage_status: unresolved`/finalcheck fail-closed until independent approval. No generated metadata modified; task remains active pending conflict resolution. No merge or acceptance.

- 2026-10-17 **implementation/test candidate — independent review and executable Go test evidence still required**. [Draft product PR #985](https://github.com/mcpdev80/baseharbor/pull/985), exact HEAD `5a3813385af5392a9be3095bd038424a4f9950b7`, from develop `d54ac358fb6a6b256164ac2689a33e981c013baa`. **Actual file scope:** only `cmd/baha/mcp_preconditions_test.go` (new). No product behavior rewritten: `classifyMachineCLIError` already maps the organization and workspace sentinels, `resolveApplicationEnvironment` already returns typed `not_found` for unregistered deployment, and `machineMCPFailure` applies the same typed translation to MCP; verify those pre-existing paths rather than adding a string-based classifier. Candidate test fixtures cover `organization.inspect`, `status`, `policy.explain`, `workspace.status` through an in-memory MCP session, typed CLI/MCP parity including unsupported organization source, missing source/config/deployment, cancellation, timeout and unknown errors. [Product CI 39034547657](https://github.com/mcpdev80/baseharbor/actions/runs/39034547657): Trusted Plan, workflow policy and focused Python SUCCESS; Go MCP tests **NOT EXECUTED** because trusted planner selected `not-required`. Required `PR Selected Checks` FAILURE: `coverage-unresolved: mixed registration/execution source needs independent diff review: cmd/baha/mcp_preconditions_test.go; no required gates or validations`. This is a qualification/verification blocker, not evidence tests passed. No extra CI policy layer or self-exemption. Local source checkout unavailable in connector-only environment (GitHub DNS unavailable), so no local Go test/vet/gofmt execution is claimed. Must independently qualify and execute the exact focused Go checks before review acceptance. No merge or release-scope change.

- 2026-10-17 claim: assigned core-754 on current develop; first audit existing typed semantics and four real CLI/MCP entries, then only demonstrated gaps. Planned scope bounded to cmd/baha MCP entry/error translation and directly relevant focused tests (exact files pending source inspection); exclude App Edit/Lifecycle, import detector, tool registration and workflow/policy. Candidate permitted even if source coverage qualification unresolved; no self-exemption/acceptance/merge. No v0.4.26 release scope change.

- Assigned to mcpdev80; no recent claim. Partial implementation exists (see scope).
