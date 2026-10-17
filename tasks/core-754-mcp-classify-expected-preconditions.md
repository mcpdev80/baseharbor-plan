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

- 2026-10-17 **Verified #986 CI candidate:** `7b666773c948fedef0ea337f6212ee982986c88d`; [run 39038225852](https://github.com/mcpdev80/baseharbor/actions/runs/39038225852). Workflow-executed 44 planner tests and 17 runner tests PASS, including real dependency-free Go fixture proving exact `^Testname$` patterns exclude similarly named failing tests; existing missing/skip/fail regressions preserved. Trusted Plan, Focused Python, ci-policy, executor/verifier SUCCESS. Required PR Selected Checks FAILURE solely coverage-unresolved for runner implementation/test files, pending independent review. Actual #985 Go tests not yet executed.

- 2026-10-17 **Regex fixture preparation:** Replace `\\Z` with portable `^Testname$` patterns and run actual Go test discovery/execution with extra similar names; before final hosted results this was pending, superseded by the verified evidence above.

- 2026-10-17 **updated #986 independent CI review handoff**: exact [CI PR #986](https://github.com/mcpdev80/baseharbor/pull/986) HEAD `70ec5d3f864a4f36bc7927e466451dcc226f6c1a`, [Actions 39037450572](https://github.com/mcpdev80/baseharbor/actions/runs/39037450572), attempt 1. Existing workflow invocations `python3 scripts/test_pr_gate_plan.py` and `python3 scripts/test_pr_check_runner.py` now actually run 44 and 16 tests respectively, both **PASS**. New test classes moved before final `unittest.main()`. Tests exercise mandatory discovery and actual output-contract parsing of each of the two core-754 Go tests: both RUN/PASS succeed; either missing, SKIP or FAIL blocks. Actual `.github/workflows/ci.yml` binding test verifies `wizard-*-tests` loads executable `pr-check-runner.py` from trusted `BASE_SHA` (not the untrusted PR head). Real temporary Git fixture creates independently reviewed source, advances trusted develop with CI, normally merges target into source, and confirms exact selection survives the clean merge while `coverage_status` remains **unresolved**; unreviewed post-merge follow-up remains rejected. Hosted CI: Trusted Plan, Focused Python, `pr-planner-tests`, `ci-policy`, `ci-executor-verifier-tests` all **SUCCESS**; `PR Selected Checks` **FAILURE** solely unreviewed CI executor sources `scripts/pr-check-runner.py`, `scripts/test_pr_check_runner.py`. This is correct, not an approval. To execute the *actual #985 Go tests*, #986 must first be independently reviewed and normally integrated into develop; then merge develop normally into #985 (no force), run its regular exact-integration CI, and evaluate each required Go test result. No claim that actual #985 Go tests have run; no self-qualification/merge. #983 paused and unchanged; review and reconcile its `scripts/pr-gate-plan.py` work separately without granting its contents. No release scope change; no generated status/metadata changed. Planning render/check validation remains unproven and must not be represented as green.

- 2026-10-17 #986 continued CI implementation. Corrected regression placement so `python3 scripts/test_pr_gate_plan.py` and `python3 scripts/test_pr_check_runner.py` discover the added classes (previously after `unittest.main()`). The new runner regression drives the existing `execute_validation` with per-family Go `-list` and `-run` protocol fixtures; covers both PASS, each missing, each SKIP, and each FAIL; existing runner's missing/SKIP/non-PASS blockers remain. Added a workflow-source regression requiring `.github/workflows/ci.yml` `wizard-*-tests)` to execute `pr-check-runner.py` loaded via `git show "$BASE_SHA"`, never PR HEAD. Planner permits the exact #985 review commit after normal trusted-develop merge using the existing clean merge-chain proof, but still always emits `coverage_status=unresolved`; no source qualification or final-check relaxation. #985 cannot execute the new profile before #986 is independently accepted and integrated on develop, followed by normal develop integration into #985 and targeted PR CI. Interim CI [39036784285](https://github.com/mcpdev80/baseharbor/actions/runs/39036784285) failed planner test's mock call count; [39036847554](https://github.com/mcpdev80/baseharbor/actions/runs/39036847554) detected the new classes, 43 planner tests but runner fixture required downloading Go 1.25; [39036988980](https://github.com/mcpdev80/baseharbor/actions/runs/39036988980) planner succeeded but isolated Go fixture failed before discovery. Latest candidate `f64bde94459877e8a343c1d4e0755028d9453c49` in [CI 39037172618](https://github.com/mcpdev80/baseharbor/actions/runs/39037172618) awaiting actual jobs at handoff time; **no green final status asserted**. #983 remains paused, untouched; its `scripts/pr-gate-plan.py` additions need later ordinary reviewed reconciliation, not takeover. No merge/self-approval. Planning derived view validation not yet evidenced.

- 2026-10-17 **separate core-754 CI execution PR for independent review**: [Draft #986](https://github.com/mcpdev80/baseharbor/pull/986) candidate `b275469b5c8b9fe8e199e68ab7ca02783d70d424` (runner repaired from current develop; original policy/test changes from `934cb2a04f4e4b61506037986fa9bcbc21498dd5`). Scope exactly `scripts/pr-gate-plan.py`, `scripts/pr-check-runner.py`, `scripts/test_pr_gate_plan.py`, `scripts/test_pr_check_runner.py`. Trusted planner has exact #985 head `5a3813385af5392a9be3095bd038424a4f9950b7` and single-added `cmd/baha/mcp_preconditions_test.go` execution selection, emits `wizard-core754-mcp-tests` and required CLI format/vet/build while **always** retaining source `coverage_status: unresolved`. Existing trusted runner individually discovers/executes `TestExpectedPreconditionsShareTypedCLIMCPErrors` and `TestMCPReadEntryExpectedPreconditions` using anchored patterns, rejects missing/skip/non-PASS; no path-wide MCP allowance or finalcheck bypass. Actual [CI 39036373808](https://github.com/mcpdev80/baseharbor/actions/runs/39036373808): Trusted Plan, focused Python, `pr-planner-tests`, `ci-policy`, `ci-executor-verifier-tests` **SUCCESS**; required `PR Selected Checks` **FAILURE** on independent coverage of `scripts/pr-check-runner.py` and `scripts/test_pr_check_runner.py`. These are *policy/runner verification* jobs on #986, **not yet an authenticated run of the two Go tests on exact #985**. Those tests require independently accepted/integrated runner and planner before #985's actual focused run; do not report them executed or qualified yet. Initial #986 runs 39036064438/39036163610/39036261842 failed on corrupted runner syntax; complete file restored from trusted develop before passing source checks. #983 remains unchanged/paused: it also edits `scripts/pr-gate-plan.py`; after each independent source review, normally integrate/reconcile the two bounded planner modifications, without overwriting #983 or treating its contents as accepted. No merge, no self-qualification or release-scope change. Planning metadata unchanged; generated views require their own validator evidence, do not claim it from source CI.

- 2026-10-17 Maintainer coordination: core-754 CI session is explicitly granted temporary exclusive write ownership of `scripts/pr-gate-plan.py` and directly related planner regressions. Parallel planner edits for [#983](https://github.com/mcpdev80/baseharbor/pull/983) are paused; its branch/content must remain unchanged and is not accepted. Implement minimal separate CI PR from current develop to execute both exact #985 MCP tests while retaining `coverage-unresolved` and strict required check failure. Later integrate independently reviewed #983 changes normally with conflict analysis; do not overwrite or implicitly approve them.

- 2026-10-17 CI route ownership check (no edit to CI): exact [#985](https://github.com/mcpdev80/baseharbor/pull/985) `5a3813385af5392a9be3095bd038424a4f9950b7`, [Actions 39034547657](https://github.com/mcpdev80/baseharbor/actions/runs/39034547657) selected no Go tests because `scripts/pr-gate-plan.py` classifies new `cmd/baha/mcp_preconditions_test.go` as `registration-mixed-unresolved` without mandatory checks. Existing planner/executor/verifier route can execute selected checks, but a bounded separate selection rule requires modifying **`scripts/pr-gate-plan.py`**. That same CI policy file is still owned in review by [t-20261017-inspect-import-ci-coverage](t-20261017-inspect-import-ci-coverage.md) / [PR #983](https://github.com/mcpdev80/baseharbor/pull/983) at `25e5f8e1d71340afff415648374f4dcfa2407aee`. **Concrete competing path claim: `scripts/pr-gate-plan.py`.** Per Maintainer instruction, do not overwrite the other task; no CI branch/PR, source edits or policy exception were published. Separation required for a future coordinated change: select exact `TestExpectedPreconditionsShareTypedCLIMCPErrors` and `TestMCPReadEntryExpectedPreconditions`, require actual named results, and leave content qualification `coverage_status: unresolved`/finalcheck fail-closed until independent approval. No generated metadata modified; task remains active pending conflict resolution. No merge or acceptance.

- 2026-10-17 **implementation/test candidate — independent review and executable Go test evidence still required**. [Draft product PR #985](https://github.com/mcpdev80/baseharbor/pull/985), exact HEAD `5a3813385af5392a9be3095bd038424a4f9950b7`, from develop `d54ac358fb6a6b256164ac2689a33e981c013baa`. **Actual file scope:** only `cmd/baha/mcp_preconditions_test.go` (new). No product behavior rewritten: `classifyMachineCLIError` already maps the organization and workspace sentinels, `resolveApplicationEnvironment` already returns typed `not_found` for unregistered deployment, and `machineMCPFailure` applies the same typed translation to MCP; verify those pre-existing paths rather than adding a string-based classifier. Candidate test fixtures cover `organization.inspect`, `status`, `policy.explain`, `workspace.status` through an in-memory MCP session, typed CLI/MCP parity including unsupported organization source, missing source/config/deployment, cancellation, timeout and unknown errors. [Product CI 39034547657](https://github.com/mcpdev80/baseharbor/actions/runs/39034547657): Trusted Plan, workflow policy and focused Python SUCCESS; Go MCP tests **NOT EXECUTED** because trusted planner selected `not-required`. Required `PR Selected Checks` FAILURE: `coverage-unresolved: mixed registration/execution source needs independent diff review: cmd/baha/mcp_preconditions_test.go; no required gates or validations`. This is a qualification/verification blocker, not evidence tests passed. No extra CI policy layer or self-exemption. Local source checkout unavailable in connector-only environment (GitHub DNS unavailable), so no local Go test/vet/gofmt execution is claimed. Must independently qualify and execute the exact focused Go checks before review acceptance. No merge or release-scope change.

- 2026-10-17 claim: assigned core-754 on current develop; first audit existing typed semantics and four real CLI/MCP entries, then only demonstrated gaps. Planned scope bounded to cmd/baha MCP entry/error translation and directly relevant focused tests (exact files pending source inspection); exclude App Edit/Lifecycle, import detector, tool registration and workflow/policy. Candidate permitted even if source coverage qualification unresolved; no self-exemption/acceptance/merge. No v0.4.26 release scope change.

- Assigned to mcpdev80; no recent claim. Partial implementation exists (see scope).
