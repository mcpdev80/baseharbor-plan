# operator-auth admission SEAM reachability census — read-only bug-hunt desk

Desk: §3.3.5 fill. Befund only. NO edits / PRs / merges / subagents.
Shift: r28-welle6-2026-11-24
Card: 0428-211 (seamreach) — 211 desk
Host: /tmp/opencode/211-seam-wt (fresh read-only `git clone --no-checkout` of the real GitHub repo)

## REALITY WITNESSES

- Planning repo remote (verified before first evidence commit):
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`
  (NOT /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan — that is a directory inside the workers bookkeeping repo)
- Product remote: `https://github.com/mcpdev80/baseharbor.git` (clone origin)
- develop base SHA (origin/develop): `2b9a2c6d1611ea85e11bf81e9650c28165c8293a`
  `git ls-remote origin develop` => `2b9a2c6d1611ea85e11bf81e9650c28165c8293a	refs/heads/develop`
- The baseharbor checkout under /home/marcel/dev/baseharbor-ecosystem/baseharbor is a blob:none partial clone whose local `develop` ref reads `36d075fad77fa61ac8c153e979855546589b32c2` — STALE vs origin. Cited only as a stale reference, never as proof of remote state.

## PLAN

- Verify planning + product remotes via git ls-remote (done).
- Cut a fresh read-only clone of the real GitHub remote (done).
- Item 1: every call site of operatorauth Authorize*/WithEnforcement*/AuthorizationDecision/ActorFromContext in production vs _test.go; flag decisions CONSTRUCTED in test with no production counterpart caller.
- Item 2: the -tags=baseharbor_ci_operator_testonly build-tag seam — what enabling flips, whether any untagged production path flips too.
- Item 3: CLI/audit surfaces that write an AuthorizationResult without a seeded Principal and which fall back to cli/local-operator on a FAILED operation.
- Per-item PASS/FINDING with file:line repro; each FINDING -> a proposed NEW card number + one-line contract; mark findings already covered by 0428-218/270/277.
- Commit + push atomically the single evidence file only; origin/main freshness witness.

## ITEM 1 — call-site reachability of operatorauth authorization/admission helpers

Production (untagged) callers, with file:line:
- `cmd/baha/mcp.go:356` `operatorauth.AuthorizeMachineOperationWithLocalGrant(ctx, request, localGrant)` — MCP operator seam `authorizeMCPOperation`, production.
- `cmd/baha/mcp.go:359` `operatorauth.AuthorizeMachineOperation(ctx, request)` — same seam, non-managed env path.
- `internal/machinehttp/handler.go:217-218` `WithVerifiedPrincipal` + `AuthorizeMachineOperation` (HTTP handler admission).
- `internal/machinehttp/source_transfer.go:31-32` same (source transfer admission).
- `internal/machinehttp/streams.go:192-203` same (stream admission).
- `internal/machinehttp/terminal.go:93-94` same (runtime.exec admission).
- Context decorators `WithEnforcement*`, `PrincipalFromContext`, `AuthorizationDecisionFromContext`, `WithVerifiedPrincipal`, `WithMembershipProvider*`, `WithSkipResolveOperatorBoundary`, `EnforcementEnabled`, `ShouldSkipResolveOperatorBoundary`: called from many production files (`cmd/baha/main.go:142-143`, `operator_auth_boundary.go`, `app_access.go`, `app_exec.go`, `app_client_consent.go`, `app_evidence_helpers.go`, `env_destroy.go`, `management_remote_connection.go`, `node*.go`, etc.).

Test-only construction, with file:line:
- `internal/operatorauth/test_operator.go:31` — package-level `.go` (NOT `_test.go`), so it compiles INTO every production operatorauth build. Its exported symbols are however only ever *called* from `_test.go`:
  - `WithVerifiedTestOperator` (test_operator.go:38), `WithVerifiedTestOperatorPrincipalIfAbsent` (43), `WithVerifiedTestOperatorPrincipalForced` (48), `WithVerifiedTestOperatorPrincipal` (82), `WithVerifiedTestOperatorForce` (98), `TestPrincipal` (109).
  - `git grep -n "WithVerifiedTestOperator" -- '*.go' | grep -v "_test.go"` => EMPTY (confirmed). Production composition never calls them.
- `cmd/baha/test_operator_context_test.go:17` `runWithIOAsTestOperator` -> `testOperatorContext` -> `operatorauth.WithVerifiedTestOperator` (line 38 of the file). This is THE seeded test-operator entry for the CLI test surface.
- `internal/operatorauth/local_runtime_test.go`, `human_operator_test.go`, `authorization_test.go`, `authorization_claims_test.go`, `cmd/baha/mcp_operator_seam_test.go`, and every `internal/machinehttp/*_test.go` construct `AuthorizationDecision` / stamp a verified principal via `WithVerifiedTestOperator` / `WithAuthorizationDecision`.

Finding (FINDING, "content on unreachable AST" class, cf. 0428-218 runWithIO precedent):
- `internal/operatorauth/test_operator.go` is a package-level fixture whose exported helpers are referenced ONLY from test files. It is compiled into the production operatorauth package (no build tag) yet has NO production call path. This is the exact "authorized decision CONSTRUCTED in test but whose production counterpart has no real caller" class — the verified principal / read-granting membership / enforcement composition it wires lives on an AST node reachable only from `runWithIOAsTestOperator`. The production counterpart (`WithVerifiedPrincipal` + real `MembershipProvider`, main.go:142-143, machinehttp handler.go:217) is a DIFFERENT, real path.
- The read-granting `membershipProviderFromContext(ctx)` used by `authorizeMachineOperation` (internal/operatorauth/authorization.go:227) resolves via `ResolveClaimMembership` and FAILS CLOSED (`ErrClaimsNotVerified`/`ErrNoClaimMembership`) on any unverified principal. There is no production caller that omits it.

Already covered: `cmd/baha/mcp_operator_seam_test.go:1` explicitly declares itself "the 0428-218 mutation proof for the MCP operator-auth seam". The test-only-constructed-decision class is the same class 0428-218 already tracks. => **wie 0428-218, andere stelle** (test_operator.go fixture vs mcp.go seam).

## ITEM 2 — the -tags=baseharbor_ci_operator_testonly build-tag seam

Tag-gated file pair (both live in cmd/baha, package main), with file:line:
- `cmd/baha/ci_integration_operator_enabled.go:1` `//go:build baseharbor_ci_operator_testonly` — 573 lines. Provides `func withCIIntegrationOperator(ctx, args) context.Context`, `ciIntegrationOperatorContext` (557), the synthetic verified operator `ciAcceptanceOperator` + `ciAcceptanceMembershipProvider` (uses `operatorauth.WithVerifiedPrincipal`, `WithMembershipProvider`, `PrincipalsHaveVerifiedIdentity`; returns `ErrClaimsNotVerified` on unverified), guarded by `os.Getenv("DEMO_ATOMIC_GATE") != "1"`.
- `cmd/baha/ci_integration_operator_disabled.go:1` `//go:build !baseharbor_ci_operator_testonly` — 10 lines. Provides the no-op `func withCIIntegrationOperator(ctx, _ []string) context.Context { return ctx }`.

What enabling the tag flips (file:line):
- At `cmd/baha/main.go:148` `ctx = withCIIntegrationOperator(ctx, filtered)` — the ONLY production call site. With the tag DISABLED (all normal/release/CI binaries) it is an identity no-op (disabled.go:7-10). With the tag ENABLED (`baseharbor_ci_operator_testonly`, used only by the disposable demo acceptance gate) it installs a synthetic verified operator for the CLI (enabled.go:20-24), but only when `DEMO_ATOMIC_GATE=1` (enabled.go:27) and after `deployment.LoadConfig()` + target resolution (enabled.go:30-79); otherwise still returns `ctx` unchanged.

Is ANY untagged (production) path flipped by enabling the tag? => NO (FINDING, confirm):
- `git grep -n "func withCIIntegrationOperator\b"` production callers => ONLY `cmd/baha/main.go:148`, and that call is identical in both variants.
- The `withCIIntegrationOperator` exported/test symbol is called from `cmd/baha/ci_integration_operator_enabled_test.go` (701 lines of assertions, tag-gated) and from main.go:148. No untagged test or production file calls the enabled variant.
- Conclusion: the test-only operator is STRICTLY tag-gated and FAILS CLOSED for untagged binaries: untagged builds contain `ci_integration_operator_disabled.go` (no-op) and never the synthetic operator. A real unverified principal still hits the production fail-closed seam (authorization.go:227). Enabling `baseharbor_ci_operator_testonly` does NOT open an unauthenticated production path — it only swaps the no-op for the synthetic operator inside one disposable acceptance gate.

## ITEM 3 — CLI/audit surfaces writing an AuthorizationResult WITHOUT a seeded Principal, and cli/local-operator fallback on FAILED ops

`AuthorizationResult` (evidence string field, `internal/evidence/model.go:83`) is written in these production files, with file:line:
- `cmd/baha/app_access.go:387,394` — allow; guarded by `AuthorizationDecisionFromContext(ctx)` then `PrincipalFromContext(ctx)`.
- `cmd/baha/app_evidence_helpers.go:46,53` — allow; same two-tier guard.
- `cmd/baha/env_destroy.go:353,355,358,367,369` — allow/deny; guarded by decision-then-principal.
- `cmd/baha/machine_http_terminal_audit.go:24` — always "allow"; actor seeded via `evidence.WithActor(ctx, "http", descriptor.Actor.Subject)` (line 14) from an admission-decided descriptor (already authenticated at the seam).
- `cmd/baha/secret_operations.go:59,61,69,79,81,194,196,204,208,210` — allow/deny; guarded by decision-then-principal-then-trusted-local (see below).

The #1823 actor-fallback ladder (which surfaces fall back to cli/local-operator on a FAILED operation):
- `internal/evidence/model.go:124-128` `ActorFromContext(ctx)` returns `Actor{Interface: "cli", Identity: "local-operator"}` when no `WithActor` value is present. THIS is the cli/local-operator person fallback.
- The audit write sites above do NOT use `ActorFromContext` blindly: they first consult `AuthorizationDecisionFromContext(ctx)` (decision wins), then `PrincipalFromContext(ctx)` (verified principal wins), and ONLY the no-decision AND no-principal branch reaches a person-less actor:
  - `cmd/baha/secret_operations.go:77` -> `event.Actor.Identity = "trusted-local"` (a runtime actor, NOT the cli/local-operator person default — the comment at line 73 explicitly says so).
  - `cmd/baha/env_destroy.go:365` -> `"trusted-local"` (comment line 362).
- On a FAILED operation with no decision and no principal: `secret_operations.go:81`/`env_destroy.go:369` write `AuthorizationResult = "deny"` (matches the failed outcome) rather than "allow". So the only path that stamps `local-operator` as the actor is a call that never seeded a principal into the enforcement seam at all — which the fail-closed machine-http/mcp seams reject before reaching audit.

Finding (FINDING, audit-actor class):
- The cli/local-operator person default at `internal/evidence/model.go:128` is reachable ONLY when a caller writes audit without seeding a principal/decision. The current production audit writers (`secret_operations.go`, `env_destroy.go`, `app_evidence_helpers.go`, `app_access.go`) each have an explicit no-decision/no-principal branch that stamps `trusted-local` (runtime actor) or `deny` (failed) — so `local-operator` is not silently attributed as an authenticated person on a denied machine mutation.
- `machine_http_terminal_audit.go:24` always writes "allow" using the stream descriptor's already-admitted actor — correct only because admission (`internal/machinehttp/terminal.go`) enforces the seam before the descriptor is built. Worth a guard review if the descriptor can ever carry an anonymous actor.

Already covered: the `operator.identity` audit surfaces (`cmd/baha/operator_auth_status.go:31` Principal "local-operator", `cmd/baha/operator_operations.go:25` Mode "trusted-local") are the operator-auth STATUS/identity command, not a mutation admission seam. => **wie 0428-277, andere stelle** (identity status surface). The fail-closed machine mutation seam and the test-only fixture are **wie 0428-218**.

## FINDINGS -> PROPOSED NEW CARDS (Fund->Karte)

1. FINDING (unreachable-AST fixture): `internal/operatorauth/test_operator.go` is a package-level, no-build-tag fixture compiled into production operatorauth, whose exported helpers are called ONLY from `_test.go`. Propose NEW card: operator-auth seam reachability / test-only fixture dead-code review.
   One-line contract: "Audit every exported symbol in internal/operatorauth/test_operator.go for a production caller; if none exist, mark the fixture as test-only (move to _test.go or tag it) and confirm production composition uses the WithVerifiedPrincipal+real-membership path at main.go:142-143 / machinehttp handler.go:217."
2. FINDING (audit actor on failed op): `internal/evidence/model.go:128` `local-operator` person default + `machine_http_terminal_audit.go:24` unconditional "allow". Propose NEW card: operator-auth audit attribution must never record an unauthenticated actor as a person on a failed/anonymous mutation.
   One-line contract: "Every AuthorizationResult write must seed its actor from a present AuthorizationDecision, a verified Principal, or an admission-decided runtime actor (trusted-local); never from the cli/local-operator person default on a FAILED operation, and machine_http_terminal_audit must assert the descriptor actor is authenticated before stamping 'allow'."
3. NOTE (already-tag-gated, no action): the `baseharbor_ci_operator_testonly` seam is confirmed strict and fail-closed for untagged binaries (disabled.go no-op vs enabled.go synthetic operator, main.go:148 identical). No card needed.

## ALREADY COVERED (mark 'wie 0428-xxx, andere stelle')

- Item 1 fixture-decision class: **wie 0428-218** (mcp_operator_seam_test.go:1 is the declared 0428-218 proof).
- Item 3 identity-status operator surfaces: **wie 0428-277**.
- Item 2 tag seam: confirmed already fail-closed; no new work.

## repo-rule compliance

- Read-only product access only: a fresh `git clone --no-checkout` of the real GitHub remote; `git grep`/`read`/`ls-remote` only. NO edits, NO PR, NO merge, NO subagent, NO workflow change (Owner split 2026-11-04).
- Evidence written only to baseharbor-plan (never a product repo).

## cleanliness

- No containers / compose projects started. No docker/podman activity.
- Clone zone: /tmp/opencode/211-seam-wt (ephemeral, removed at END).

## END

Lane: 211-seamreach | Status: DONE | candidate SHA: 2b9a2c6d1611ea85e11bf81e9650c28165c8293a (origin/develop base; read-only census, no product commits)
