# Befund 1 — Live verify chain1 (r28-welle4-2026-11-19)

Lane: mission-verify-chain1 (mission tag: verify-chain1). Revision labels are in each section.
Scope: read-only verification of Accepted claims against live develop. No product change, no PR.

## Reality witnesses

- Planning repo toplevel (wrong-zone check): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` → `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (correct zone; the workers/ copy was not used).
- Product develop head (ls-remote): `deeeb64778b3f6109d3a8e49fd652d490901e89c refs/heads/develop`
- The mission's chain1 stage names `ec592fd385`; that commit is an ancestor of `deeeb6477` (`git merge-base --is-ancestor ec592fd38 deeeb6477` → yes; it is PR #1687's merge commit, see `git log --oneline deeeb6477`). All chain1 inspection ran in a fresh detached worktree at `deeeb6477` (`/var/tmp/chain1-wt`, `git worktree add` on the fetched SHA).
- Tests are unit-only on this host (R1 respected): `GOCACHE=/var/tmp/chain1-gocache GOPATH=/var/tmp/chain1-gopath`, run inside the worktree. No containers were started (cleanliness line at the end).

## These 1 — #116 fail-closed guard (outcomeMatchesImpact / unexpected continuation-edge at A=false → actual-disposition-differs)

**CONFIRMED** (revision label: develop deeeb6477; guard commits 8349eaced / 96ac1b2e7 merged via 40b990139, ancestor of deeeb6477).

- Code: `internal/application/provider_change_result.go:53-62` — the parenthesized guard `(len(imp.ContinuationDependencies) == 0 || !continuationDependencyOutcomesMatch(...))` plus the third branch `else if !unexpectedEdgeAllowed(out, imp)` → `out.Status="failed"; out.ErrorCode="actual-disposition-differs"` (lines 59-61). `unexpectedEdgeAllowed` at `provider_change_result.go:242-247`: for a NON-continuation operation (`continuationRequiresDependencyEvidence == false`, the A=false case) an applied receipt carrying any continuation edge is rejected — fail closed.
- Helper: `internal/application/provider_change_dependency_result.go:56` (`continuationRequiresDependencyEvidence`).
- Test witness (targeted run, green): `go test ./internal/application/ -run 'TestProviderResultNonContinuationBehaviourPin|TestProviderResultRequiresFreshEntireContinuationGraph' -v` →
  - `non_continuation`: log line `non-continuation receipt with unexpected edge failed closed: status=failed code=actual-disposition-differs` — exactly the claimed disposition.
  - `non_continuation_clean`: `status=applied` (fail-closed does not over-tighten).
  - `continuation_without_evidence`: `status=failed code=continuation-dependency-unverified`.
  - `--- PASS: TestProviderResultNonContinuationBehaviourPin (0.00s)` plus 20/20 graph subtests PASS, `ok github.com/mcpdev80/baseharbor/internal/application 0.052s`.
- Why the witness carries: the pin test drives the real `RecordProviderChangeResult` entry point with a stop impact (A=false) whose applied receipt carries an unplanned continuation edge, and asserts status+exact ErrorCode; the observed outcome equals the card's claim.

## These 2 — #120 MCP fail-loud (partial → error, not success)

**CONFIRMED** (revision label: develop deeeb6477; fix 7d3438364 = PR #1688 merge, ancestor of deeeb6477).

- Code: `cmd/baha/app_registration_921.go:201-212` — the apply handler mirrors the CLI Edit contract: it classifies the private `partial` `appMachineError` via `machine.Classify(classifyMachineCLIError(...))`, attaches the result as `Details` and returns `machineMCPFailure(&partial)` — a partial provider-change can no longer return as success. CLI precedent `appEditApplyConfirmed` rejects `result.Status != "complete"`.
- Test witness (targeted run, green): `go test ./cmd/baha/ -run 'TestCore921MCPEditHandlerLevelNegatives/missing-pending-partial-fails-loud' -v` → `--- PASS: ... missing-pending-partial-fails-loud/missing-pending (0.24s)`; the whole `TestCore921MCPEditHandlerLevelNegatives` suite PASS (`ok github.com/mcpdev80/baseharbor/cmd/baha`).
- Why the witness carries: the regression `core921PendingPartialMCPReportsFailure` (`cmd/baha/registration_921_test.go:535`, wired at :232) drives the MCP/HTTP handler directly with a missing pending impact (Status="partial", nil error pre-fix) and asserts the handler reports failure.
- PR truth: `gh pr view 1689/1688` family — #1688 content present in develop ancestry via 7d3438364 (commit message references #1688).

## These 3 — #121 central env filter on all list paths

**NOT ON DEVELOP — card is in REVIEW, not accepted** (revision label: checked at develop deeeb6477; fix commits 361398afa / d9d70a984 exist only on `origin/lane-0428-efilter`, head `d9d70a9845ea11f6d839b3f5600b67b214002d20`; `git merge-base --is-ancestor 361398afa deeeb6477` → NO).

- Inspected at deeeb6477: `internal/observability/registry.go:488` `func List(kind, placement, applications, ...)` has no environment parameter or environment predicate; `registry.go:551/555/588/615` (`ListLogs`, `ListTraces`, `ListApplicationMetrics`, `ListMetrics`) likewise carry no environment dimension; no `envfilter_regression_test.go` exists in `internal/observability/`.
- Coordinator clarification (2026-11-19, this session): #121 stands in REVIEW as PR #1691 (head d9d70a984); develop ancestry correctly does not contain it. This matches chain1's earlier finding. No contradiction, no new card. The thesis "central filter on all list paths" is therefore **not expected to hold at deeeb6477 and verifiably does not** — nothing further to check per the coordinator's ruling.

## These 4 — #122 writer + ReconcileMatching

**NOT ON DEVELOP — card is in REVIEW, not accepted** (revision label: checked at develop deeeb6477; fix commits 282ef0dfa … 8956bf08e exist only on `origin/lane-0428-appclass-writer`, head `8956bf08e40e52b84a0dae55a9f1cb54db957636`; `git merge-base --is-ancestor 282ef0dfa deeeb6477` → NO).

- Inspected at deeeb6477: `grep -rn "ReconcileMatching" --include="*.go" .` → 0 hits; `ApplicationLogSourceID` / `reconcileApplicationLogSource` → no non-test hits. The writer and reconciliation primitive are absent from develop, as expected for a review-stage card.
- Coordinator clarification (2026-11-19): #122 stands in REVIEW as PR #1692 (head 8956bf08e); no contradiction, no new card, nothing further per the ruling.

## These 5 — #118 DIAG_EXEC stdout leak (no stdout leak)

**CONFIRMED** (revision label: develop deeeb6477; fix de5324658 = PR #1689 merge commit, `gh pr view 1689` → MERGED 2026-11-19T01:02:27Z at de53246585560ddf2c3e6ceae6d0f6eea6b71b68; `git merge-base --is-ancestor de5324658 deeeb6477` → YES).

- Code: the diff removed 3 lines from `cmd/baha/app_edit_apply.go` (the `if true`-guarded `fmt.Printf` DIAG_EXEC dump). At deeeb6477: `grep -n "Printf\|Println\|fmt.Print" cmd/baha/app_edit_apply.go` → no hits; `grep -rn DIAG_EXEC --include="*.go" .` matches only the regression test file `cmd/baha/app_edit_diag_exec_stdout_test.go` (no DIAG_EXEC code remains in production paths).
- Test witness (targeted run, green): `go test ./cmd/baha/ -run 'TestAppEditApplyPartialHasNoDiagnosticStdoutInAnyDiagExecMode' -v` → subtests `unset` and `set` both `--- PASS`; the child harness asserts no `DIAG_EXEC` text reaches process stdout in either mode and that both modes behave identically (`ok github.com/mcpdev80/baseharbor/cmd/baha 0.030s`).
- Why the witness carries: it executes the real app-edit partial path in a subprocess under both `BAHA_118_DIAG_EXEC_MODE` settings and asserts the stdout byte stream stays clean — the exact leak class the card fixed.

## These 1/2/5 summary

All three chain1 theses that were actually merged (116, 120, 118) are confirmed on live develop deeeb6477 with code location + green targeted test runs. Theses 121 and 122 are not accepted content at this head (review-stage, PR #1691/#1692) and the develop absence was verified, closed by the coordinator ruling in-session.

## PLAN

1. Read mission; verify planning repo path — done
2. Fetch live develop heads (baseharbor, baseharbor-demo); base attestation — done
3. Verify #116 fail-closed guard — confirmed
4. Verify #120 MCP fail-loud — confirmed
5. Verify #121 env filter — not on develop (review-stage, coordinator ruling)
6. Verify #122 writer + ReconcileMatching — not on develop (review-stage, coordinator ruling)
7. Verify #118 diag exec leak — confirmed
8. Write befund-1.md, commit, push — this file
9. Chain2 stage (#102/#093/#099/#117) → befund-2.md
10. Cleanliness + END post

## repo-rule compliance

- No product changes: worktree detached at the fetched develop SHA; read + test only; no git mutations in the product repo (only a `git worktree add` under /var/tmp).
- No `.github/**` touched, no reruns, no workflow_dispatch, no PR, no merge, no force.
- Tests unit-only on this host (R1); no containers/networks/volumes created.
- Scratch confined to /var/tmp (worktree + Go caches), per mission.
- No subagents used.
- Host cleanliness: before: no lane processes/containers; after: `docker ps` unchanged (nothing started by this lane); worktree removed; evidence committed and pushed. cleanliness: clean.

## END_BLOCKED/END marker

END mission-verify-chain1.md DONE (befund-1 chain1 stage complete; see befund-2.md for the chain2 stage).
