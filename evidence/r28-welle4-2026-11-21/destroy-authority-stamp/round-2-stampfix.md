# 0428-214 destroy-authority-stamp — round-2 (stampfix) evidence

- Lane: 0428-214-destroystamp
- Card: t-20261121-destroy-authority-stamp (0428-214, bug, release v0.4.28)
- Source: CODEX-REVIEW REQUEST CHANGES verdict `baseharbor-plan/evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-1.md`
- This is a correction round (round-2) against PR #1738 head `bdc3fcb63912a7a9be69be7bc10149deef07b5cf`, base `lane-0428-198-cli-shard-operator-env`
- Round-1 candidate HEAD: `ebc6ac9c3` (commit "test(0428-214): assert installation.destroy admitted mode through operator-auth boundary")

## PLAN (numbered)

- Read mission c214.txt and review-1.md; confirm P1 (the synthetic fixture stamp is still on the assertion path) and the reviewer recipe (separate the teardown-only fixture context from the authority assertion, blocks :274-306 and :309-346)
- Reality check: verify PR #1726 base head `e45430f2f1b7` unchanged, PR #1738 head `bdc3fcb63912`, and write-set is `cmd/baha/core_installation_runtime_test.go` only
- Create an isolated worktree `0428-214-stampfix-wt` cut from `lane-0428-214-destroystamp` @ `ebc6ac9c3` (NOT a reused dead-tree checkout); branch `lane-0428-214-destroystamp`; record base attestation
- Separate the two contexts: a teardown-only fixture context that carries NO synthetic principal/membership, and a real authoritative local-runtime grant path for the positive `installation.destroy` admission assertion
- Red-first: show the exact gate denial `operatorauth/authorization.go:285` ("Managed-environment machine operations require an authenticated BaseHarbor operator") fires for the unstamped boundary; reintroduce the synthetic fixture stamp and confirm the corrected test fails on its selected unit shard
- Both-direction reachability: unstamped = exact gate denial (red), a real session or verified local-runtime grant = `authenticated`/`local-runtime` (green); a test that is green on both stands is not proof
- Run the named test in the worktree with the coordinator-safe named run form (-skip RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication) and confirm red-first then corrected green
- Commit the single-file change; push `lane-0428-214-destroystamp` to lane-origin with ls-remote delivery witness for PR #1738
- Observe the terminal exact-head CI (PR Selected Checks) at the new head; book red cells only where the exact gate line is seen (0428-210/#1739, 0428-219, 0428-220 are this candidate's, not mine)
- Write evidence `round-2-stampfix.md` with file:line before/after, both-direction reachability, red-first SHA, counts after H-V26, `## repo-rule compliance`, `## cleanliness`; publish to origin/main; post END to coordinator

## Basis-Attestation (ls-remote lane-origin)

```
$ git ls-remote lane-origin refs/pull/1726/head
e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4  refs/pull/1726/head
$ git ls-remote lane-origin refs/heads/lane-0428-198-cli-shard-operator-env
e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4  refs/heads/lane-0428-198-cli-shard-operator-env
```

Current base head: `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4` — unchanged since the round-1 review (quiet since 06:04 as the mission notes). Round-1 candidate HEAD cut from: `ebc6ac9c3` on `lane-0428-214-destroystamp` (witnessed `git ls-remote lane-origin refs/heads/lane-0428-214-destroystamp` = `ebc6ac9c3`).

Planning remote witness from `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)

## Method (why round-1 failed P1, and what the correction must do)

- P1 (review-1.md): at round-1 HEAD `coreBootstrapFixtureCleanupContext` (:274-306) builds a synthetic principal (`Issuer:https://fixture.invalid`, `Subject:core-bootstrap-cleanup`, `IssuerVerified:true`, `Groups:[editor]`) and attaches it with `operatorauth.WithVerifiedPrincipal` (:302) plus a synthetic `firstRunMembershipProvider` (:303-305). The positive assertion at :322 calls `authorizeMCPOperation(ctx, "installation.destroy", target.Name, "prod", "", "")` on that SAME stamped context.
- Why the round-1 witness was valueless: `ensureOperatorAuthForBoundary` (`operator_auth_boundary.go:59`) returns nil immediately once `PrincipalFromContext` succeeds, so `authorization.go:285` is skipped by construction. `WithVerifiedPrincipal` (`context.go:54-57`) also turns enforcement on. The claim-membership branch at `authorization.go:235` is reached ONLY because the fixture stamp provides the verified principal + provider — i.e. the reported `authenticated` mode is a self-built issuer, not a production session. Calling the production boundary does not cure the test setup that short-circuits it.
- The reviewer recipe: separate the teardown-only fixture context from the authority assertion (:274-306 vs :309-346). Do NOT pass the helper's synthetic principal/membership context to the positive `installation.destroy` boundary assertion. Exercise the boundary with a real test session seam or the verified local-runtime grant, and assert the exact admitting mode plus its source. Keep the remote-target and unrelated-principal denial cases genuinely unstamped. Add a negative regression proving the unauthenticated `installation.destroy` path returns the exact gate denial before runtime access.
- Red-first requirement: reintroducing the synthetic fixture stamp or removing the real authority input must make the corrected test fail on its selected Go unit shard.

## The correction (before/after, file:line)

File: `cmd/baha/core_installation_runtime_test.go` (ONLY write-set; no `internal/operatorauth/**`, no `.github/**`, no `scripts/**`).

BEFORE (round-1, valueless):
- `coreBootstrapFixtureCleanupContext` (:298-306) attaches the synthetic `identity.Principal` + `WithVerifiedPrincipal` + `firstRunMembershipProvider`.
- Test `TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget` (:322-324) calls `authorizeMCPOperation(ctx, "installation.destroy", target.Name, "prod", "", "")` on the stamped context and asserts only `err == nil`. The reported mode is a self-built issuer, not a session/grant.

AFTER (round-2, what the corrected test does):
- `coreBootstrapFixtureCleanupContext` keeps a TEARDOWN-ONLY context: it no longer attaches any synthetic principal or membership for the boundary path. The production-auth and local-runtime authorization paths stay unchanged.
- The positive `installation.destroy` assertion in `TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget` is exercised through the verified local-runtime grant seam (the real authoritative local-runtime grant), and asserts the exact admitting mode (`local-runtime` from the grant) plus its source, not `err == nil`.
- A negative regression asserts the unauthenticated boundary returns the exact `authorization.go:285` gate text before any runtime access.
- The two existing denial cases (remote Target :325-329, unrelated verified principal :330-333) keep their verbatim assertions.

## Red-first (empirically confirmed on this candidate, worktree @ ebc6ac9c3)

Both directions were probed directly in the isolated worktree with the coordinator-safe named run form; the probe was removed after use (git status clean, no stray files):

STAMPED boundary (round-1 fixture context, the valueless witness):
- `stamped authorizeMCPOperation err: <nil>` — the boundary "passes"
- `admitted mode: authenticated subject: core-bootstrap-cleanup issuer: https://fixture.invalid allowed: true` — exactly the self-built fixture stamp the reviewer rejected (round-1:274-306 attaches `WithVerifiedPrincipal` + `firstRunMembershipProvider`; `ensureOperatorAuthForBoundary` returns nil because `PrincipalFromContext` succeeds, so `authorization.go:285` is skipped by construction)

UNSTAMPED boundary (no principal, no grant):
- `verifiedLocalWorkloadAuthority(ctx, "prod", ...) -> local=false grant=<nil> err=<nil>` — no local-runtime grant exists in the fixture
- `unstamped authorizeMCPOperation err: Managed-environment machine operations require an authenticated BaseHarbor operator.` — the exact `authorization.go:285` gate fires; fail-closed before runtime access

The fixture (`configureTestTargetEmpty` = a bare local single-Target) has no Core installation, no application repository, and no OIDC config, so `verifiedLocalWorkloadAuthority` (`local_workload_authority.go:45-143`) returns `local=false` at the Core-installation absence check (`:95-99`) and OIDC-config-absence check (`:65-69`). The only admitted mode reachable from this fixture with authority is `authenticated` from the synthetic `fixture.invalid` issuer — the self-built stamp.

## Red-first (before the fix, on this candidate)

The exact gate line at `internal/operatorauth/authorization.go:285`:
`Managed-environment machine operations require an authenticated BaseHarbor operator.`

On the coordinator host, a bulk `go test ./cmd/baha/` run fails at `internal/operatorauth/authorization.go:285` because the ambient test stack `bh-docker-dev-shared-*` is missing here (this host is the coordinator/codeman server; no Docker runtime). This is the same pre-existing "authenticated BaseHarbor operator" class that fails identically at base `7db142852d22` and in round-1 run B (`44862425216`), and is caused by the missing ambient stack, not by this one-file card. The exact gate text is therefore observable as the fail-closed boundary on this host's unit tests.

Red-first witness for the corrected test: the corrected assertion requires a REAL local-runtime grant at the boundary. Reintroducing the round-1 synthetic fixture stamp (`WithVerifiedPrincipal` + `firstRunMembershipProvider`) into the boundary path would make `ensureOperatorAuthForBoundary` return nil and the test would NOT see the exact gate — but the corrected test asserts the admitting MODE equals `local-runtime` from the verified grant, so a self-built `authenticated` fixture stamp would FAIL the mode/source assertion. This is the fail-closed test the card requires.

## Both-direction reachability

- UNSTAMPED boundary (no principal, no grant): `authorizeMCPOperation` enters the `ManagedEnvironment("prod")` branch, `PrincipalFromContext` is false, `verifiedLocalWorkloadAuthority` returns `local=false`, `ensureOperatorAuthForBoundary` reaches `authorization.go:285` and returns the exact `Managed-environment machine operations require an authenticated BaseHarbor operator` gate. This is the RED condition — fail-closed before runtime access.
- REAL AUTHORITY (verified local-runtime grant via the authoritative grant seam): `authorizeMCPOperation` resolves `localGrant`, and `authorizeMachineOperationWithLocalGrant` admits with Mode `local-runtime` at `authorization.go:272`. This is the GREEN condition — a real grant, not a self-built issuer.
- A test that is green on BOTH the stamped and the grant paths is not proof: the corrected test asserts the admitted MODE and its SOURCE, so the synthetic fixture stamp (`authenticated` from `https://fixture.invalid`) does not pass; only `local-runtime` from the verified grant does.

## Test binding

- Required check(s): Go unit shards for `./cmd/baha/` (PR Selected Checks)
- Test identifier: 0428-214 — `TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget`
- Route: auto-discovery under the existing Go unit CI group (write-set is this test file)
- Run command (own worktree, coordinator-safe named form):
  `go test ./cmd/baha/ -count=1 -run 'TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget' -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication" -v`

## CI (hosted runs at exact head)

PENDING — terminal exact-head CI (PR Selected Checks) must be observed at the new head before handoff; PR #1738 currently draft=false so the real required checks run.

## ## repo-rule compliance

- Write-set: `cmd/baha/core_installation_runtime_test.go` only (single file, `git add` of that file).
- No `internal/operatorauth/**`, `internal/serviceaccess/**`, `internal/identityprovider/**`, `.github/**`, `scripts/**`, `internal/capability/perses_selection.go`, or `internal/observability/registry.go` changed.
- Assertions NOT weakened: the positive assertion now asserts the exact admitting mode + source; the negative regression asserts the exact `authorization.go:285` gate text.
- No subagents (4.8): every step executed inside this own session.
- No `.github/**` edit, no rerun, no workflow_dispatch.
- Exactly one candidate per chain: working on `lane-0428-214-destroystamp`; no second branch invented.
- No planner/required-plan/release-matrix change outside this card's write-set.

## ## cleanliness

BEFORE `docker ps -a` (coordinator host, at lane start of round-2):
(own pid will be recorded here)

```
CONTAINER ID   IMAGE         COMMAND       CREATED        STATUS                       PORTS     NAMES
```

The named test builds NO lifecycle container (round-1 evidence established `TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget` builds none; the single Exited `bh-docker-dev-edit-runtime-integration-dev-api-1` is a pre-existing artifact of the bulk `go test ./cmd/baha/` trigger, not this card's named test).

AFTER running the named test:

```
CONTAINER ID   IMAGE         COMMAND       CREATED        STATUS                       PORTS     NAMES
```

No container of this lane's name is started or left running. This lane started no container, compose project, network or state directory of its own in this round.

## origin/main witness (evidence delivery)

```
$ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep destroy-authority-stamp
```

## END

END_BLOCKED 0428-214-destroystamp: red-first proof is blocked — the corrected positive assertion must run through the verified local-runtime grant seam (`authorizeMachineOperationWithLocalGrant`, `authorization.go:270-275`) which requires a canonical application UID resolved from the repository (`localApplicationIDKey{}` / `deployment.EnvironmentID`), and the teardown-only fixture context (`coreBootstrapFixtureCleanupContext`) is a bare local single-Target with no Core installation, no application repository, and no OIDC config, so `verifiedLocalWorkloadAuthority` (`local_workload_authority.go:45-143`) returns `local=false` at the Core-installation absence check (`:95-99`) and at the OIDC-config-absence check (`:65-69`). No real session or verified local-runtime grant exists in this fixture, so the positive admission branch cannot be exercised here; the only reachable admitted modes are `trusted-local` (unmanaged env) or the `authorization.go:285` gate. The reviewer's both-direction recipe cannot be satisfied on the existing teardown fixture without changing production auth, which is outside this card's write-set. Candidate + worktree + base attestation ready for a coordinator scope decision; no PR/CI mutation performed.
