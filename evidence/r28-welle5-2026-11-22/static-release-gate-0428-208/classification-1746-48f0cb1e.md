# PR #1746 failure classification

## PLAN

1. Verify PR #1746 exact head, base, run, current repository remotes, and review scope.
2. Collect exact failed-job logs and terminal state for CI fast-check from run 44976686495.
3. Inspect candidate/base source at cited lines for the release gate catalog, managed operator authentication, and Perses method contract.
4. Classify each finding as PR defect, existing develop/infra defect, or owner exception with file:line or job evidence.
5. Write the read-only classification evidence, including required witnesses and VERDICT: HELD (classification only).

## Candidate and run witnesses

- PR: https://github.com/mcpdev80/baseharbor/pull/1746; state open. Exact head `48f0cb1e44d5014ea1fc65015fe1c1b312aed47f`; PR base SHA `6209874428f08dc3e90d6e29a42b30683ce9932a`.
- Run: https://github.com/mcpdev80/baseharbor/actions/runs/44976686495; event `workflow_dispatch`; head `48f0cb1e44d5014ea1fc65015fe1c1b312aed47f`; terminal `completed/failure`. The run selected six static gates: init, mcp, config-matrix, agent, shell-ux, ci-fast-check.
- Results: init job 137069323512 failure; mcp 137069323541 failure; config-matrix 137069323606 failure; agent 137069323626 success; shell-ux 137069323632 failure; ci-fast-check 137069370445 success. The initially reported in-progress ci-fast-check is now terminal success; its `Run static gate` step and evidence upload passed.
- At review time, `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1746/head` returned `8b9a8f50645db1dbaad4a5e1f2140930436d3ea7 refs/heads/develop` and `48f0cb1e44d5014ea1fc65015fe1c1b312aed47f refs/pull/1746/head`. PR/run metadata still records base `6209874428f08dc3e90d6e29a42b30683ce9932a`; develop has since advanced. Classification below is bound to the assigned exact head and run, not a new-base qualification.
- `gh api user` returned `mcpdev80`. Product remote witness: `lane-origin https://github.com/mcpdev80/baseharbor.git` (fetch and push); the planning repo remote verified before evidence publication is `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- PR #1746 changed `.github/workflows/pre-release-runtime-suite.yml`, `.github/workflows/pre-release.yml`, `CHANGELOG.md`, `docs/releases/v0.4.28.demo-ref`, `scripts/ci-fast-check.sh`, `scripts/pr-gate-plan.py`, `scripts/pre-release-check-plan.py`, `scripts/pre-release-runtime-impact.json`, `scripts/release-requirements.json`, `scripts/test_ci_v0427_gate_catalog.py`, `scripts/test_pre_release_check_plan.py`, and `scripts/test_pre_release_runtime_reuse.py`. No BaseHarbor product authentication or Perses source file is in that diff.

## Finding 1 — alleged missing `gate_id`

Classification: the alleged `gate_id` catalog defect is not present; the failure attribution is incorrect. The catalog deliberately uses `id` keys. `scripts/pre-release-check-plan.py:26` reads `row['id']`; it does not read a `gate_id` property. The candidate catalog has 66 gate rows, and the selected `atomic/static/{init,mcp,config-matrix,agent,shell-ux,ci-fast-check}` IDs are present with `jobs: [static_gates]` and the v0.4.28 requirement.

The shell runner’s `.github/workflows/pre-release-runtime-suite.yml:235-239` assigns the variable `gate_id="atomic/$RUNTIME/$GATE"`, then tests catalog `.id == $gate` at line 237. It only prints the `Missing release-gate catalog entry` error if that jq predicate fails. In all six static jobs, the `Validate gate resource declaration` step succeeded. The `gate_id` text in the log is the echoed shell source, not an emitted failure. The actual init failure follows in job 137069323512, log lines 612-623: `Managed-environment machine operations require an authenticated BaseHarbor operator.` No PR #1746 defect and no Owner exception are indicated by this claim.

## Finding 2 — managed operator authentication in init/config-matrix/shell-ux

Classification: existing static-test context/fixture prerequisite, outside the #1746 diff; it blocks the full-suite positive proof but is not evidence of a product authorization defect. The product fails closed as specified by `internal/operatorauth/authorization.go:283-290` when there is no authenticated operator.

Exact hosted witnesses:

- Job 137069323512, Static init, log lines 612-623: `Managed-environment machine operations require an authenticated BaseHarbor operator`; affected `init-source-fixture/dev`; resolution text says authenticate the operator.
- Job 137069323606, Static config-matrix, log lines 575-579: `authentication_failed` / `Managed-environment machine operations require an authenticated BaseHarbor operator`.
- Job 137069323632, Static shell-ux, log lines 574-585: the same authenticated-operator error; affected `shell-ux-static/dev`.

This is not the failure fixed by PR #1750/card 0428-223. PR #1750 remains open and draft; its body addresses test-process target-selection leakage (`target "company-dev" is not configured`) via `testIsolatedSelectionContext`, not managed-operator authentication. The auth failure belongs to the static gate’s test context/fixture or its explicitly supplied operator identity. Treat it as an existing develop/infra/test-fixture prerequisite requiring its own follow-up, not as a regression caused by #1746. If a repair requires changing `.github/**` operator identity setup, that change is Owner-owned; no such change was attempted here.

## Finding 3 — Perses MCP tool mismatch

Classification: existing MCP test-contract drift in the pinned Demo fixture, not a BaseHarbor product regression from #1746. Static mcp job 137069323541, log line 578, says `missing=[]` and `unexpected=[baseharbor.app.perses.disable, baseharbor.app.perses.enable, baseharbor.app.perses.remove, baseharbor.app.perses.status]`.

The expected test list is `mcpdev80/baseharbor-demo` at the exact pinned Demo SHA `5d1cf312e18d06915db35c340bebe4e3d4f39d45`, file `tests/mcp/run.sh:31-128`. Its `expected` set omits all four tools and line 127 compares the entire live `names` set against it. The intended product MCP contract is explicit in `internal/machine/contract.go:205-208` and `docs/reference/mcp.md:68-71`; `cmd/baha/mcp_lifecycle_extra.go:61-77` registers the same four live tools. `internal/capability/perses_selection.go` is a Perses dashboard-selection model, not the MCP tool registry or the source of these method names.

PR #1751/card 0428-225 is merged, but its diff changes only `cmd/baha/agent_mcp_test.go`; it adds a product-side regression test and does not update the pinned Demo checker. The live failure at #1746’s exact run proves the release gate mismatch remains. Do not remove declared product tools: that would contradict the machine contract and docs. A separate Demo fixture/card should add the four intended tools (and correct read-only/destructive classification) to `tests/mcp/run.sh`, then update the v0.4.28 Demo pin to that tested commit. This is not repairable within #1746’s current scope and no Owner exception for the Perses selection file is needed.

## Disposition

No local tests were run. No PR comment, rerun, workflow dispatch, merge, or product edit was made. The full static-suite success criterion remains unmet: the catalog claim is disproven, the operator-auth context is a separate inherited prerequisite, and the MCP fixture mismatch needs a follow-up outside this candidate. The existing six-gate run is terminal; ci-fast-check passed but does not override the four failures.

VERDICT: HELD (classification only)
END codex-rev2-1736 DONE — classification complete; evidence publication pending.
