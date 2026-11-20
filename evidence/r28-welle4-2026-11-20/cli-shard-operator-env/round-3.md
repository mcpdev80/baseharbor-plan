# 0428-198 · cli shards need operator env — round 3 (handoff for rotation)

- Lane: w198-0428-198-cligate (laptop)
- Candidate branch: lane-0428-198-cli-shard-operator-env
- Delivered head (ls-remote lane-origin): 7546b1806aac9a0055a647e20f2843564eb3c1ce
- Base attest: develop 40cb28c758b02960356434b630086a341ebe1738 is ancestor of 7546b1806 (git merge-base --is-ancestor = YES); git log 40cb28c75..7546b1806 lists ONLY my commit on top of 8b2cb2a97.
- Branch provenance (git diff ... HEAD against base): 7 test files + the blessed test seam in main.go.
- CI gate for 0428-198 = cli-0..3 ONLY now (packages half resolved by PR #1732 per owner 2026-11-20).

## The three required lines (owner 3.3.6 rotation)

### (1) What changed at each of the four dock points — or why not

Dock point 1 — runWithIO seam (cmd/baha/main.go:157, `if testOperatorContext != nil`):
made PERMANENT via an init() in cmd/baha/operator_test_fixture_test.go that sets
testOperatorContext to operatorAuthFixtureContext(ctx). This stamps a verified
operator principal (Groups [editor] + tenant editor membership) onto the runWithIO
context AFTER WithEnforcement. Reaches the production CLI run path
rootCommand().Execute(ctx) for every command dispatched through runWithIO.

Dock point 2 — perses_lifecycle_transport_test.go:54 persesMatrixContext: rewired
from `operatorauth.WithEnforcement(ctx)` to `operatorAuthFixtureContext(operatorauth.WithEnforcement(ctx))`,
so the perses transport cells get the principal. TEST: TestPersesLifecycleTransportActionMatrix
now ok.

Dock point 3 — application_restore_external_identity_test.go:83: rewired
`machineNoninteractiveContext(t.Context())` to
`machineNoninteractiveContext(operatorAuthFixtureContext(t.Context()))`. TEST:
TestRestoreBindsOriginalExternalIdentityAndProtectedDestination now ok.

Dock point 4 — repository_runtime_fixture_test.go:78 runRepositoryFixtureApplyCall:
rewired `machineNoninteractiveContext(ctx)` to
`machineNoninteractiveContext(operatorAuthFixtureContext(ctx))`, the single choke
point every repository-apply fixture call threads through.

### (2) Output of the four-cell gate command

Command: `go test ./cmd/baha/ -run 'TestMCPGenericClient|TestPersesLifecycleTransport|TestRestoreBinds|TestGuidedRepository' -count=1`
Result: FAIL (exit 1), 18.4s. Per-cell (isolated runs):
- TestPersesLifecycleTransportActionMatrix: ok (2.5s) — dock point 2 works.
- TestRestoreBindsOriginalExternalIdentityAndProtectedDestination: ok (5.8s) — dock point 3 works.
- TestMCPGenericClientDiscoversCompleteSemanticSurfaceAndExercisesReadOnlyTools: FAIL — "Managed-environment machine operations require an authenticated BaseHarbor operator." (0.06s)
- TestGuidedRepositoryRuntimeFixtureRegressionSuite: FAIL — subtests production-retirement-current-scope-and-data-consent and production-retirement-stale-publication-rejection fail with the same operator-auth message.

### (3) The finding I owe the owner — does my seam reach the path these four tests take

Measured with a debug print in the seam (temporary, reverted before commit): the
[w198-seam] print fires for runWithIO-dispatched commands, proving the seam is
ACTIVE in the runWithIO->rootCommand().Execute(ctx) path. BUT it does NOT reach
the MCP tool-handler path: TestMCPGenericClient builds its context from the MCP
request context (CallTool context.Background()), which is reconstructed inside the
handler and carries no WithEnforcement state, so PrincipalFromContext returns
ok=false and the gate fails closed. The runWithIO seam is therefore INCOMPLETE for
any command that resolves through an MCP tool handler or a direct
context.Background()/t.Context() call that never flows through runWithIO. The
whole-package init() seam + the four wired context-builders cover the
runWithIO-dispatched and the three direct-context-builder cells; the MCP-handler
and remaining direct-call cells stay red. Full cmd/baha run: 136 FAIL (down from
140 baseline) — the seam fixed 4, the remaining 136 span every entry point that
does not thread an WithEnforcement context into the command/action/MCP handler.

## Rotation handoff state (for the incoming lane)

- Branch at 7546b1806; working tree clean (only untracked baha binary).
- go vet clean; gofmt clean.
- Uncommitted work at rotation: NONE (all committed and pushed).
- Scope reality: #1594's managed-enforcement enforcement broke the ENTIRE cmd/baha
  test surface (~136 tests), not the 4 ctx-builders the earlier diagnosis named.
  The four named dock points are fixed; the failure is systemic across
  runWithIO->MCP-handler and direct .Run(ctx)/direct-function-call entry points
  that never receive an WithEnforcement context. Covering all 136 needs either a
  per-test context seam at every builder (dozens of sites) or a production-level
  change to how the command/MCP layer establishes the enforcement principal — both
  beyond the four-dock-points hypothesis. Packages half of the field gate is
  resolved (PR #1732); only cli-0..3 remain for 0428-198.
- Prior evidence: round-1.md, round-2.md.

## END

- END_BLOCKED w198-0428-198-cligate — seam lives and is proven active in the
  runWithIO path; systemic ~136-entry-point breakage exceeds the four-dock-points
  scope. Candidate 7546b1806 committed + pushed; branch handed to incoming lane at
  same head. Incoming lane: cli-0..3 only (packages resolved by PR #1732).
