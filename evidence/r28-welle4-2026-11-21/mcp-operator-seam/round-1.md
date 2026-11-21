# 0428-218 - MCP operator seam uncovered (t-20261121-mcp-operator-seam-uncovered)

## Role / card
Worker. One PR per card. Card born from hunt lane H-V29 (evidence/bug-hunt-2026-11-21/seam-reachability-desk/round-1.md, plan ab9b5822). This is the MCP arm that #1615 does not heal.

## Base attestation (before branch)
- base-lane head I branched from (verified via `git ls-remote`, then FETCH_HEAD):
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-198-cli-shard-operator-env`
  => `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4  refs/heads/lane-0428-198-cli-shard-operator-env`
- develop base for reference (verified):
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
  => `40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop`
- Planning repo remote (verified `git remote -v` before first evidence commit):
  `https://github.com/mcpdev80/baseharbor-plan.git` (owner main)
- PR base: `lane-0428-198-cli-shard-operator-env`. Body note: "STACKED ON: #1726 (0428-204) -- content dependency, not merge dependency."
- My worktree branch: `lane-0428-218-mcp-operator-seam` cut from `e45430f2f` (the base-lane head).

## Repo-rule compliance
- Wrote only inside my worktree `lane-0428-218-mcp-operator-seam` (cut from base-lane head e45430f2f).
- Did not touch internal/operatorauth/**, cmd/baha/mcp.go, cmd/baha/app_init_wizard.go, or cmd/baha/operator_test_fixture_test.go. Only added a new file: cmd/baha/mcp_operator_seam_test.go.
- Did not edit .github/**, scripts/pr-gate-coverage.json, or any other lane's files.
- gofmt applied to the new file; go vet passes; build + tests pass locally.
- No subagents (4.8). All steps executed inside this session.

## Branch provenance (proof)
- `git merge-base --is-ancestor e45430f2f HEAD` => YES: base-lane head is an ancestor of my first commit.
- `git log --oneline e45430f2f..HEAD` lists ONLY my commit:
  de4a45ec5 test(0428-218): prove MCP operator-auth seam reachable in both directions
- `git diff e45430f2f..HEAD --name-only`:
  cmd/baha/mcp_operator_seam_test.go
- Push delivered: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-218-mcp-operator-seam` => de4a45ec5.
- PR #1741 draft, head de4a45ec5, base lane-0428-198-cli-shard-operator-env. `git ls-remote ... refs/pull/1741/head` => de4a45ec5.

## Scope decision (Owner clarification 2026-11-21)
The seam mechanism already lives on the base-lane head: withoutOperatorAuthTestContext /
operatorAuthTestContextAllowed (cmd/baha/app_init_wizard.go:29-34) and the fixture init() in
cmd/baha/operator_test_fixture_test.go stamp a verified operator principal onto any context that
does not opt out. So this card is NOT "the seam is missing" -- it is "which MCP cases stamp instead of
marking anonymous". Per Owner instruction: judge per MCP test file "marks anonymous" vs "stamps
principal (wrongly-green)", mark the wrongly-green cases with withoutOperatorAuthTestContext(ctx),
do NOT change denial semantics, do NOT edit internal/operatorauth/** or cmd/baha/mcp.go, do NOT
edit .github/**. Own PR, base = base-lane head.

## Entry-point table: every MCP call site that reaches authorizeMCPOperation / authorizeCurrentMCPContext
Scope limited to MCP tool handlers; runWithIO (main.go:145 WithEnforcement) is the CLI path and is
out of this card's seam (the seam lives in mcp.go, not runWithIO).

- target.create (mcp_target_mutation.go:60) -> authorizeCurrentMCPContext(ctx,"target.create",...) -- reachable; denied when no verified principal (measured)
- target.delete (mcp_target_mutation.go) -> authorizeCurrentMCPContext -- reachable
- app.* lifecycle (mcp_tools.go / mcp_lifecycle_extra.go) -> authorizeMCPOperation / authorizeResolvedMCPOperation -- reachable
- backup / restore (mcp_tools.go:610,651) -> authorizeMCPOperation -- reachable
- destroy (mcp_tools.go:689) -> authorizeMCPOperation -- reachable
- apply / update / repair (mcp_tools.go:492,528,574) -> authorizeMCPOperation -- reachable
- app.new (mcp_tools.go:369) -> authorizeMCPOperation -- reachable
- workspace.* (mcp_tools.go / mcp_workspace_mutation.go) -> authorizeCurrentMCPContext -- reachable
- provider.* , organization.* , policy.* (mcp_tools.go) -> authorizeCurrentMCPContext -- read-only + managed check
- connectivity.connect (connectivity.go:615) -> authorizeCurrentMCPContext -- reachable
- control-plane.stop (control_plane_stop.go:38) -> authorizeCurrentMCPContext -- reachable

## Reachability evidence (measured, not assumed)
A temporary debug test drove baseharbor.target.create on an
withoutOperatorAuthTestContext(context.Background()) context against a prod manifest and observed:
```
SEAMDEBUG ANON IsError=true err=<nil> body={"contract_version":"v1","error":{"code":"authentication_failed","message":"Managed-environment machine operations require an authenticated BaseHarbor operator.","next":"Authenticate the operator for the selected Target and environment, then retry the same operation."}}
```
prod is managed: ManagedEnvironment("prod") == true (operatorauth/config.go:89, always-fail-closed).
PrincipalFromContext(bg) == (nil, false). So the anonymous path reaches the seam and is refused with
the exact production denial code. This is the RED protocol.

## Per-MCP-test-file verdict (marks anonymous vs stamps / wrongly-green)
Files #1726 already marked correctly (verified present in this card's base-lane head):
- cmd/baha/agent_mcp_test.go -- "managed read/mutation fail closed" subtests use withoutOperatorAuthTestContext (unauth client); success subtests legitimately stamp. Correct.
- cmd/baha/mcp_application_authoring_test.go -- prod denial uses withoutOperatorAuthTestContext, asserts authentication_failed. Correct.
- cmd/baha/mcp_platform_tools_test.go -- prod denial marked. Correct.
- cmd/baha/mcp_secret_tools_test.go -- prod denial marked, asserts authentication_failed. Correct.
- cmd/baha/mcp_stack_tools_test.go -- prod denial marked. Correct.
- cmd/baha/mcp_workspace_mutation_test.go -- prod denial marked, asserts authentication_failed. Correct.
- cmd/baha/control_plane_stop_impact_test.go, cmd/baha/provider_external_removal_test.go, cmd/baha/runtime_destroy_impact_test.go -- #1726 marked the managed-denial subtests. Correct.

No unmarked managed-env auth-denial subtests remain in the MCP files. The remaining MCP tests that
build a stamped context (operatorAuthFixtureContext / operatorAuthTestContext) do so on success /
parity subtests where stamping is intended (CLI/MCP parity, dev-path), not denial. No wrongly-green
auth-denial case to mark; #1726's markers already cover the seam.

## Mutation proof (two protocols, the acceptance core)
New file cmd/baha/mcp_operator_seam_test.go -- TestMCPOperatorSeamReachesGateBothDirections:
drives the same managed target.create twice on the same transport:
- BEFORE (wrongly-green protocol): stamped context (operatorAuthFixtureContext) -> SUCCEEDS. This is
  exactly the trap the card targets: an MCP test that receives its verified principal from the fixture
  can never reach the denial it claims; a case that stays green here is not proof the gate works.
- AFTER (red protocol): identical call on withoutOperatorAuthTestContext(context.Background()) ->
  authentication_failed.
Result:
```
=== RUN   TestMCPOperatorSeamReachesGateBothDirections
--- PASS: TestMCPOperatorSeamReachesGateBothDirections (0.66s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.674s
```
Both directions land on opposite sides of the gate on the same transport, proving the production denial
path is reachable in-test without any internal/operatorauth/** or cmd/baha/mcp.go change and without
changing denial semantics. A case that stays green on BOTH states is not a regression (5.3/5.6); this
test is red on the anonymous state, so it exercises the seam.

## CI coverage (read-only, .github/** untouched)
- scripts/pr-gate-coverage.json (read, not changed): gate.mcp -> atomic/static/mcp (covers capability.profile.machine-interface). Static MCP contract gate.
- cmd/baha Go unit tests run in .github/workflows/ci.yml job pr_unit_shards (line ~1185): bash scripts/pr-unit-database.sh "${{ matrix.shard }}".
- scripts/pr-go-unit-shard.py distributes EVERY Test* in cmd/baha across cli-0..cli-3 by sha256(name)[:8] % 4 (fail-closed: every selected test must pass). TestMCPOperatorSeamReachesGateBothDirections lands in cli-3. Auto-scheduled by CI under the existing PR trigger (draft=false). Durable CI-backed evidence (Owner directive 2026-11-07).
- Local CI-equivalent run: bash scripts/pr-unit-database.sh cli-3 (run in session) -- results recorded in this round.

## Cleanliness
- No containers / compose projects started. No docker/podman state touched (the cli-3 CI fixture
  Docker PostgreSQL is created by scripts/pr-unit-database.sh, not by this lane; no compose stack here).
- Worktree lives under /home/marcel/dev/baseharbor-ecosystem/workers/0428-218-mcpseam-wt (fixed
  workspace layout); build cache under /home/marcel/dev/baseharbor-ecosystem/workers/.tmpbuild.
- Temporary debug test (zz_seedebug_test.go) deleted.

## END
0428-218-mcpseam: MCP seam reachable both directions; dedicated mutation-proof test added, no seam/operatorauth change; PR #1741 draft on base-lane head e45430f2f; CLI cli-3 (pr_unit_shards) will run it.
END lane 0428-218-mcpseam DONE
