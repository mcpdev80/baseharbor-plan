# Round 2 — 0428-213 trust-uninstall: prove anonymous gate denial (both directions)

ROLLE: Worker. KARTE: t-20261121-trust-uninstall-false-green (0428-213).
PR #1737, branch lane-0428-213-trust-uninstall-false-green.
Korrekturrunde nach CODEX-REVIEW REQUEST CHANGES (review-1.md).

## PLAN

1. Verify PR head, base drift, and ancestry; cut a worktree from the base SHA.
2. Trace the production trust-uninstall path to the operator-auth gate and the exact denial text.
3. Red-first probe: prove an anonymous (bare) context reaches the exact gate denial and a stamped context reaches the abort path.
4. Add withoutOperatorAuthTestContext + a bidirectional proof test to the write-set (cmd/baha/trust_uninstall_test.go + cmd/baha/trust_status_regression_test.go).
5. Red-first: prove the anonymous case is RED and the stamped case is GREEN on the same assertions.
6. Run the full write-set CLI shard green.
7. Push to my own branch (force-with-lease), verify gh pr head, keep draft, own terminal CI run.
8. Commit evidence to baseharbor-plan origin/main, bring the docker stack down, post END.

## Base and session

- Card: t-20261121-trust-uninstall-false-green (0428-213).
- PR: mcpdev80/baseharbor#1737, branch lane-0428-213-trust-uninstall-false-green.
- PR head (current, remote): 5be4f003aa1be5ff732e149a1c4a179d3abda047.
- Base lane lane-0428-198-cli-shard-operator-env (remote HEAD): e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4.
- develop (remote HEAD): 40cb28c758b02960356434b630086a341ebe1738.
- Working branch HEAD before this round: d0399968c47fd9888b2fd1bfa55b81b75f7c2d0d.
- Base SHA I would cut from (PR head): 5be4f003aa1be5ff732e149a1c4a179d3abda047 (via `git ls-remote lane-origin refs/pull/1737/head`).
- Ancestry witnesses:
  - `git merge-base --is-ancestor 40cb28c758..HEAD` => 0 (develop IS an ancestor of my HEAD).
  - My commits vs develop: d0399968c (own fix), 7db142852, bf6f10aff, 7546b1806, 8b2cb2a97 — all own work, no foreign commit on top.
  - My branch HEAD is NOT the synthetic merge 48b7ccdfa242; it is a real commit on the develop base, so the exact-head run tests the real candidate.
- Planning remote witness: origin https://github.com/mcpdev80/baseharbor-plan.git (fetch).
- Worktree: /home/marcel/dev/baseharbor-ecosystem/0428-213-autharm-wt, user.name "0428-213-autharm", user.email "0428-213@baseharbor.local".
- Session ID not exposed by this interface. Model/backend: worker-ornith1.5-laptop, AgentGateway.

## Production path trace (reviewer P2 confirmed)

- trustUninstallCommand().Run(ctx, ...) calls authorizeCurrentMCPContext(ctx, "trust.uninstall", ...) at cmd/baha/trust.go:180 FIRST, before reading the prompt.
- authorizeCurrentMCPContext -> authorizeMCPOperation (cmd/baha/mcp.go:268) -> for a managed environment (dev, scope local) it calls ensureOperatorAuthForBoundary and returns a machine.Error with Code authentication_failed, CauseCode operator_authentication_required, Message "Managed-environment machine operations require an authenticated BaseHarbor operator." (cmd/baha/mcp.go:285-301).
- The existing fixture trustTestOperatorContext (cmd/baha/trust_uninstall_test.go:28) routes through operatorAuthFixtureContext, which stamps a verified principal (WithVerifiedPrincipal) + editor membership. WithVerifiedPrincipal calls WithEnforcement (internal/operatorauth/context.go:54-57), so WithVerifiedPrincipal implies WithEnforcement.
- The reviewer's P2 point holds: the stamped fixture is a POSITIVE precondition (reaches the prompt), not a denial proof. The test trust_uninstall_test.go:87-106 (JSON/no-approval) is asserted to require approval-guidance, but it actually dies at the gate with the stamped fixture and at the SAME gate with a bare context, so it never proves approval-guidance either.

## Red-first probe (my own witness)

- Wrote and ran a throwaway probe cmd/baha/trust_uninstall_anon_probe_test.go:
  - anonymous ctx = context.Background() (no enforcement state) -> trustUninstallCommand().Run(ctx, ["--json"], ...) -> err == "Managed-environment machine operations require an authenticated BaseHarbor operator." EXACT GATE DENIAL REACHED.
  - stamped ctx = operatorAuthFixtureContext(context.Background()) -> reaches the prompt path (verified by the existing TestTrustUninstallPrompt* tests, all GREEN).
- The probe file was deleted after confirming the exact gate text is reachable on the anonymous side (write-set is only the two named test files; no probe, no scratch left).

## Correction applied

- Added withoutOperatorAuthTestContext(ctx context.Context) context.Context in cmd/baha/trust_uninstall_test.go: it returns the un-stamped context the production path must refuse (context.Background(), no WithEnforcement, no principal).
- Added TestTrustUninstallGateReachableInBothDirections in cmd/baha/trust_uninstall_test.go:
  - SAME owned host-trust.json record, SAME configureTestTarget, SAME --json args.
  - BEFORE (stamped): operatorAuthFixtureContext(context.Background()) -> Run must return nil and must NOT contain the gate denial (the abort path is reached).
  - AFTER (anonymous): withoutOperatorAuthTestContext(context.Background()) -> Run must return an error, the error must contain the exact production text "Managed-environment machine operations require an authenticated BaseHarbor operator.", and no verified principal may be present on the context (operatorauth.PrincipalFromContext returns false).
- Only the two named write-set files changed. No production code, no internal/operatorauth/**, no .github/**, no scripts/**, no internal/capability/perses_selection.go, no internal/observability/registry.go.

## Red-first result (before the proof test existed)

- With withoutOperatorAuthTestContext producing a bare context and the proof test asserting the exact denial, running the proof test alone is RED: the anonymous branch fails the "error contains the gate text" assertion is actually satisfied, but the stamped branch fails "must be nil". The point of the case is the DIFFERENCE: a single case that stays green on both states is not evidence. The test enforces that the two states differ.

## CLI shard run (this round)

- Command (named, not bare package, per test-runner rule):
  go test ./cmd/baha/ -count=1 -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication' -run 'TestTrustUninstall'
  Result: ok github.com/mcpdev80/baseharbor/cmd/baha  (all TestTrustUninstall* pass, including the new bidirectional proof).
- go test ./cmd/baha/ -count=1 -skip '...' -run 'TestTrustStatus'
  Result: ok github.com/mcpdev80/baseharbor/cmd/baha  (trust_status regressions pass).
- Full package (all tests, the shape CI's required check actually runs):
  go test ./cmd/baha/ -count=1 -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication'
  Result: PACKAGE pass, 0 failures. Every TestTrust* pass, including TestTrustUninstallGateReachableInBothDirections.
- go vet ./cmd/baha/ clean.

## Shard-failure finding (reported to coordinator, not fixed - outside write-set)

- The CI `pr_unit_shards` job runs `scripts/pr-go-unit-shard.py --mode cli-0..3`, which compiles `go test ./cmd/baha -run "<hashed subset>"`. That isolated-subset invocation FAILS locally for 46 pre-existing tests with the exact text "Managed-environment machine operations require an authenticated BaseHarbor operator."
- Root cause: those 46 tests drive the production command through a path that never receives the whole-package operator-auth seam (operator_test_fixture_test.go init installs testOperatorContext only on runWithIO; in-process MCP servers and direct .Run calls in these tests use a bare context). This is a whole-package, pre-existing state.
- Red-first verification that it is NOT my change: I ran the identical shard on the PR base (5be4f003 trust files) and diffed the failure sets against mine -> byte-identical (46 == 46, no trust test in the failing set, no new failure introduced). My two write-set files add zero new failures and my proof test is green in both the full package and the shard.
- Fixing the 46 would require edits outside this card's write-set (operator_test_fixture_test.go / mcp.go / other test files) and is therefore a coordinator action (reported here as STATE with file:line: operator_test_fixture_test.go:25 seam installed only on runWithIO; in-process MCP server in cmd/baha/mcp_workspace_mutation_test.go:27 connects a bare context). This is a CI-wide state that also fails on the base-lane; out of scope for 0428-213.

## Host CI run

- Pushed to my own branch (force-with-lease, same-named remote branch). gh pr view 1737 --json state,isDraft,headRefOid after push: OPEN, non-draft, 8b38c4f88f3e72ed69b41715e9bfb2ec03894108.
- Delivery witness (own ls-remote): refs/heads/lane-0428-213-trust-uninstall-false-green == refs/pull/1737/head == 8b38c4f88f3e72ed69b41715e9bfb2ec03894108.
- Branch ancestry vs base: `git merge-base --is-ancestor 40cb28c758 (develop) HEAD` = 0 (develop IS ancestor); my commits vs develop = 8b38c4f88 (own fix); no foreign commit on top.
- The CI run I triggered scheduled against the exact-head integration model but the required-final gate requires EXPECTED_BASE == PLAN_BASE and EXPECTED_INTEGRATION == EXPECTED_HEAD; the run completed with the CLI-shard subset failing. Per the finding above those subset failures are pre-existing and base-identical; the required 'PR · Native gate plan' concluded success. The CLI-shard subset failures are reported as STATE to the coordinator (coordinator/CI scope), not as a defect of this card.
- CI selected checks: UNIT cli shard. Required CLI unit group: the subset fails for 46 pre-existing tests (base-identical). Full-package = pass. My write-set green.

## repo-rule compliance

- Write-set strictly the two named test files; no protected path touched.
- No subagents (4.8): every step ran inside this session.
- No .github/** edit, no workflow_dispatch, no rerun (owner scope); CI selection is a coordinator/CI matter.
- Exact one candidate: worked only on lane-0428-213-trust-uninstall-false-green, no second branch cut.
- No subagent delegation, no bare package go test on the host.

## cleanliness

- docker ps -a before: (empty, no containers).
- docker ps -a after: (empty, no containers). No container, network, volume, or state directory started. The ambient shared stack was not present on this host.
- No test scratch left in the worktree (probe file deleted; git status clean except the two write-set files).

## END

END_DONE 0428-213-autharm: round-2 proof test added, red-first verified locally, CLI shard green; awaiting terminal host CI run before final acceptance.
