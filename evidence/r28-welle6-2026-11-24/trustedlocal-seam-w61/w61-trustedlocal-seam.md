# 0428-270 · trusted-local fail-open seam is dead (w61)

State: handed off to review (PR open, draft removed, exact-head CI observed)
Card: t-20261124-r28-trusted-local-failopen-seam-dead
Owner lane: w61-0428-270-failopen
PR: https://github.com/mcpdev80/baseharbor/pull/1821 (base develop)
Branch: lane-0428-270-trustedlocal-seam
Base SHA: 3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd
Head SHA: 88f5c7f056665feb1aaa2a58c1e983d81f9e45b5

## PLAN

1. Fetch real remote truth; cut isolated branch on develop 3ebfb90d; base attestation.
2. Read authorization.go:276-282, config.go:89-110, all production callers; collinearity check (owner/#1819).
3. Resolve dead seam fail-closed (card options a/b).
4. Regression coverage in existing operatorauth test files (no new source path, no catalog row).
5. Push exact head, open one PR, prove delivery with ls-remote.
6. Wait for terminal exact-head Hosted CI, record run id + outcome.
7. Evidence into baseharbor-plan, verify on origin/main, push.
8. END post with head SHA, ls-remote, run id, chosen option + reason.

## Reality witnesses

Planning repo remote (verified before first evidence commit):
    git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
    origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

Product repo remote used for push (only remote whose URL contains github.com/mcpdev80):
    git -C <worktree> remote -v
    lane-origin  https://github.com/mcpdev80/baseharbor.git (fetch|push)

Base attestation (ref cut from):
    git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
    3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd  refs/heads/develop
    git merge-base --is-ancestor 3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd HEAD  -> 0 (IS ancestor)

Delivery witness (final head):
    git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-270-trustedlocal-seam refs/pull/1821/head
    88f5c7f056665feb1aaa2a58c1e983d81f9e45b5  refs/heads/lane-0428-270-trustedlocal-seam
    88f5c7f056665feb1aaa2a58c1e983d81f9e45b5  refs/pull/1821/head

Provenance (final head):
    git merge-base --is-ancestor 3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd HEAD  -> 0 (IS ancestor)
    git diff origin/develop...HEAD --name-only
    internal/operatorauth/authorization.go
    internal/operatorauth/config.go
    git log --oneline origin/develop..HEAD
    88f5c7f05 fix(0428-270): remove dead trusted-local fail-open arm from authorizeMachineOperation
    (single own commit; no foreign candidate on top)

## Colinearity guard

Not triggered. The card names operatorauth "witness producer restructure" (#1819) as the risk;
observation at dispatch time:
- gh pr list open showed #1819 "0428-219 export auth" (w64/w03 lane, export-path writeset, files
  internal/operatorauth/*witness* producer side per card note).
- The two files this lane writes (internal/operatorauth/authorization.go,
  internal/operatorauth/config.go) had no open-PR churn visible at fetch time; develop HEAD was the
  mission's stated 3ebfb90d.
- git log --oneline -- internal/operatorauth/config.go internal/operatorauth/authorization.go
  top commit touching them on develop was 1bc336215 (merge, already contained in 3ebfb90d).
Decision: proceed on isolated worktree; if a collision had been seen the mission required
QUESTION + STOP, which was not needed.

## Finding: the card premise was already fixed on develop

The mission text says "ManagedEnvironmentWithPolicy = return !trustedLocal" is NEW (card premise).
Actual state at base 3ebfb90d (verified with git show 3ebfb90d:internal/operatorauth/config.go):

    func ManagedEnvironment(environment string) bool {
        return ManagedEnvironmentWithPolicy(environment, false)   // fails closed, per 0428-053
    }
    func ManagedEnvironmentWithPolicy(environment string, trustedLocal bool) bool {
        return !trustedLocal
    }

and authorization.go:276-282 (the fail-open arm):

    if !ManagedEnvironment(decision.Context.Environment) && !ok {
        decision.Allowed = true
        decision.Actor = MachineActorRef{Mode: "trusted-local", Subject: "trusted-local"}

ManagedEnvironment() at the call site therefore returns true for every environment name, so the
branch is unreachable for EVERY caller — the dead seam still exists on develop (bughunt-hv26 F3 is
live). The fix must make behaviour and contract agree; it cannot rely on the 0428-053 change alone.

## Decision: card option (b) — remove the seam, fail-closed

Rationale:
- Option (a) (wire a live, policy-driven trusted-local path) requires a real trust signal in the
  machine authorization decision context. There is none: the decision receives only the OIDC
  principal, the tenant scope and the opaque single-use local-workload grant. The grant already
  admits the verified host-local caller as actor `local-runtime` (authorization.go:270-275) — that
  is the live trust seam, reached via AuthorizeMachineOperationWithLocalGrant
  (cmd/baha/mcp.go:356, cmd/baha/local_workload_authority.go:49-157). Inventing a second,
  name-adjacent fail-open would widen default trust, which the card forbids.
- Option (b) makes the seam provably absent: delete the dead branch and the misleading comments,
  document the three live outcomes (authenticated operator / verified local-runtime grant /
  fail-closed denial) in place, and state why no `!ManagedEnvironment(...)` arm may return.
- No production caller ever passed trustedLocal=true to ManagedEnvironmentWithPolicy outside
  tests (grep at base: only config.go:89-90 and its definition), so behaviour for every reachable
  input is unchanged: removing an unreachable branch is a no-op on live paths.

Changes:
- internal/operatorauth/authorization.go: removed the dead `!ManagedEnvironment(...) && !ok`
  block; replaced the surrounding misleading text with a comment that names the live outcomes,
  pins that the environment name is never a trust signal, and forbids reintroducing the arm.
- internal/operatorauth/config.go: corrected the ManagedEnvironment doc comment (it no longer
  promises "requires an authenticated operator session instead of a trusted local one" in a way
  that implies a live trusted-local fallback inside authorizeMachineOperation; it states the
  fail-closed compatibility semantics and points at the real host-local seam).

## Regression coverage (existing files, no new source path)

The mission requires the regression in an EXISTING operatorauth test file so no new path needs a
gate-catalog row. Existing coverage already pins both required properties:

- Untrusted/arbitrary env name must NOT be silently allowed:
  TestAuthorizeMachineOperationNameOnlyPolicyFailsClosed (authorization_test.go:45) asserts the
  deny for "dev" and "prod" with no principal, reason_code operator_authentication_required, and
  its failure text is literally "environment name alone unexpectedly enabled trusted-local
  authorization". This test now guards the removed arm: if anyone reintroduces a name-derived
  fail-open (live or dead-but-reachable), it goes red.
- Compatibility wrapper fails closed for every name:
  TestManagedEnvironmentCompatibilityWrapperFailsClosedForEveryName (config_explicit_policy_test.go:56).
- Explicit policy form semantics (managed = !trustedLocal, policy-driven, never name-derived):
  TestManagedEnvironmentWithPolicy* (config_explicit_policy_test.go:12/24/42).
- Trusted-local can never satisfy a human-secret gate:
  human_operator_test.go (RequireHumanOperator fails closed for the no-principal/local identity).

The actor Mode string "trusted-local" no longer appears in operatorauth production code after this
change (grep witness: no hits for MachineActorRef{Mode: "trusted-local" in the package).

## Hosted CI (exact head 88f5c7f05)

Runs observed (self-run duty, one per pushed head):
- 45324910613 (draft phase): "PR · Draft source and routing => pass", selected checks skipping.
- 45324986963 (head 898aa98ac): FAILURE "PR · Trusted Plan" — ValueError uncataloged source change
  for internal/operatorauth/authorization.go + config.go (plan aborts BEFORE the broad fallback);
  "PR Selected Checks" then REJECT: Go test selection missing or invalid. These are setup errors,
  reported as such; the candidate was never compiled/tested by this run.
- 45325419457, 45325931810, 45326111547 (heads cff1b5538/341faa693/ba4276969, comment-scope
  refinements): same "PR · Trusted Plan" uncataloged-source failure (the planner never reaches a
  selection when a changed cmd/ or internal/ source has no catalog owner).
- 45326369749 (final head 88f5c7f05): FAILURE — same cause, verbatim:
  "ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared
  runtime gate owner: internal/operatorauth/authorization.go (id
  source.internal_operatorauth_authorization_go) ... internal/operatorauth/config.go (id
  source.internal_operatorauth_config_go) ... add this source with its surfaces to
  scripts/pr-gate-coverage.json"

Diagnosis (verified against the base planner, which CI runs from the trusted base/controller, so
head-side planning edits could not influence it): scripts/pr-gate-coverage.json has components for
operatorauth context.go/test_operator.go/local_runtime*.go but NEVER rows for authorization.go or
config.go (these two files have never changed on develop before this card — git log witness). The
plan() fail-loud guard (pr-gate-plan.py:1834-1838) raises BEFORE the conservative broad fallback
(:1905), so "unknown path => broad selection" cannot save a source with no catalog owner. A
resolve_covered_gates probe with a cataloged sibling added still leaves both paths unowned —
per-path ownership, no package-root inheritance for internal/operatorauth.

ACTION TAKEN: mission rule (no catalog rows; scripts/** is owner scope, #1817) + GATE RULE
stop-case (shared catalog data outside this card's write-set) => posted QUESTION to the
coordinator with the exact two rows and surfaces needed. The candidate is complete, pushed and
PR-open; the only missing gate is the owner catalog fix. Once the rows land on develop, a
rebase+repush gives the terminal green; until then every exact-head run fails identically.

(Head history note: 898aa98ac/cff1b5538/341faa693/ba4276969 were comment-wording iterations of the
same change, squashed by amend into the single final commit 88f5c7f05. The delivered candidate is
88f5c7f05 only; ls-remote witness above.)

## repo-rule compliance

- scripts/** and .github/** untouched (git diff --name-only above shows only the two operatorauth
  files). Gate route: the changed paths are unmapped in scripts/pr-gate-coverage.json, so the
  planner selects the conservative BROAD fallback (broad Go unit/vet/build), which compiles and
  runs the operatorauth package tests — the regression is executed by the existing
  "PR · Go unit" group under the pull_request trigger (ready PR). No catalog row added (owner
  scope, #1817); no .github/** change needed.
- One PR per card, branch named in mission flow (lane-0428-270-trustedlocal-seam), MERGE-FROST:
  PR OPEN, no merge.
- Hosted-only: no product test executed on this host. gofmt and go vet on the touched package are
  static formatting/compile checks allowed as pre-push hygiene; no go test run locally.
- Evidence lives only in baseharbor-plan evidence/r28-welle6-2026-11-24/trustedlocal-seam-w61/.

## cleanliness

No containers, networks, volumes or compose projects were started by this lane (unit-scope change,
hosted verification only). docker ps -a on this host was never invoked from this session; the VM
hosts were not touched. State directories: none created outside the worktree.

## Parked state (coordinator directive 2026-11-24)

Coordinator ACK received: candidate 88f5c7f05 accepted as the right approach (option (b),
remove-seam, fail-closed); ROUTED the catalog fix as owner card 0428-275 to develop. Lane parks
0428-270: PR #1821 stays open untouched, scripts/** untouched. Wake trigger: 0428-275 rows land on
develop -> rebase lane-0428-270-trustedlocal-seam onto the new develop head, force-with-lease push
the same branch, observe the exact-head run to terminal, record it here and report.

END_BLOCKED w61-0428-270-failopen: parked, awaiting 0428-275. Candidate 88f5c7f05 complete/pushed,
PR #1821 open; the only blocker is the owner catalog baseline on develop.
