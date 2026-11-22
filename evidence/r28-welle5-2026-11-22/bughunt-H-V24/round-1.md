# Bug-hunt H-V24: MCP / guided-contract desk on develop (0428-218/241 area)

- bug-hunt H-V24, sitz f0f6c8b4. REINE BEFUNDUNG, develop-stand, KEINE Produkt-/Datei-Aenderung.
- READ-ONLY: no edit/commit/push/merge/comment, no subagent, no product change, no PR.
- develop HEAD: 64eab13e23fba8bca07a1d68c687fa36afedb64e (via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`).
- remote guard: all remotes -> https://github.com/mcpdev80/baseharbor.git; used github.com/mcpdev80 remote.
- Method: read-only `git show`/`grep`/`rg`/`gh api` on develop (ref fb5a5dead for #1741 head, develop for product). One targeted `go build ./cmd/baha/` (build only, NO test execution) -> exit 0.

## PLAN

1. Establish reality (remote guard, develop HEAD). No git write.
2. Desk 1 (MCP tool-flaeche): read cmd/baha/mcp.go + internal/machine/contract.go. Check MCP tool names/annotations match product contract; compare against the 0428-232 perses-drift precedent.
3. Desk 2 (guided demo new_edit.py contract): read baseharbor-demo tests/guided/new_edit.py + drive.py + new_edit_helpers_test.py on develop. Check candidate-consent / --confirm-candidate contract alignment.
4. Desk 3 (recut mcp_operator_seam_test completeness from #1741): verify the seam test's helpers/contract exist on develop; positive + negative directions reachable in-test.
5. Classify each finding: ECHTER DEFECT / doku-luecke / kein-befund. File:line + rezept.
6. Write akte + Fundbilanz + cleanliness. No product change, no PR, no comment.

## Befunde

### Desk 1 — MCP tool-name / annotation contract (0428-218/241 area)

**FUND 1: ECHTER DEFECT — recut MCP operator-auth seam test references a helper that does not exist on develop or on the #1741 head.**

- file:line `cmd/baha/mcp_operator_seam_test.go:55` (on #1741 head fb5a5deaf36, NOT on develop) calls `withoutOperatorAuthTestContext(context.Background())` to build the anonymous ("AFTER marking / red") direction of `TestMCPOperatorSeamReachesGateBothDirections`.
- `withoutOperatorAuthTestContext` is NOT defined anywhere:
  - develop: grep across cmd/baha/*.go -> no match. Only `operatorAuthFixtureContext` exists (in #1741's `cmd/baha/operator_test_fixture_test.go:61`, and it is the "stamped / green" direction).
  - #1741 head fb5a5dead: `withoutOperatorAuthTestContext` not in `mcp_operator_seam_test.go`, not in `operator_test_fixture_test.go`, not in `mcp_workspace_mutation_test.go`.
- The seam test comment (lines 28-33) requires the identical managed `target.create` call to land on OPPOSITE sides of the gate: stamped -> authorized, anonymous -> denied `authentication_failed`. The anonymous half (line 55-62, 94-102) CANNOT compile/run without `withoutOperatorAuthTestContext`.
- Positive direction is reachable: `operatorAuthFixtureContext` stamps `WithVerifiedPrincipal` + `WithMembershipProvider` (operatorauth/context.go:64,76 via #1741 operator_test_fixture_test.go:61-73) -> `authorizeMCPOperation` (cmd/baha/mcp.go:284) reaches `operatorauth.PrincipalFromContext(ctx)` at mcp.go:303 and passes the gate.
- Negative direction is NOT yet wired on develop/#1741: the "anonymous / opt-out" context helper is missing, so the test as written does not compile. This is the "wrongly-green trap" the card targets (lines 24-27): without the opt-out helper the case stays green and is not evidence the gate works.
- Produkt-side the negative path is intact: mcp.go:303 `if _, authenticated := operatorauth.PrincipalFromContext(ctx); !authenticated` -> mcp.go:310 `ensureManagedEnvironmentOperatorBoundary` -> mcp.go:314-323 returns `machine.ErrorAuthenticationFailed` ("Managed-environment machine operations require an authenticated BaseHarbor operator."), which the test pins at line 94/87-88 (`"code":"authentication_failed"`).
- Re-producible: the seam test will fail to COMPILE on develop until `withoutOperatorAuthTestContext` is added (read-only desk cannot add it — that is a test write).
- Minimum rezept (test-only, kartenwuerdig): add `withoutOperatorAuthTestContext(ctx)` to `operator_test_fixture_test.go` (the single collection point for the 0428-198/218 gate map, #1741) as the inverse of `operatorAuthFixtureContext`: start from `context.Background()` (no verified principal), apply `operatorauth.WithMembershipProviderIfAbsent` if needed, and return a context with NO verified principal so `PrincipalFromContext` at mcp.go:303 reports unauthenticated -> the managed mutation is denied. Do NOT change `internal/operatorauth/**` denial semantics (test comment line 32-33). This is a TEST write, not a product fix; the guard is already correct.

### Desk 2 — guided demo new_edit.py contract (baseharbor-demo, develop)

**FUND 2: kein-befund — candidate-consent contract in new_edit.py aligns with the product refusal.**

- file:line `tests/guided/new_edit.py:213-256` (`edit_candidate_confirmation`, `resume_confirmed_edit_apply`), `tests/guided/drive.py:80-92` (`capture_confirm_hash`), `tests/guided/drive.py:139-145` (`EXPECTED_CANDIDATE_CONSENT_REFUSAL`).
- The product prints (cmd/baha/app_candidate_consent.go:155) `...: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state` and `Re-run with --confirm-candidate <digest> ...`.
- `EXPECTED_CANDIDATE_CONSENT_REFUSAL` (drive.py:139-145) reproduces the exact wrapped refusal text the product emits; `capture_confirm_hash` (drive.py:80-92) extracts the 64-hex digest after `Re-run with --confirm-candidate`; `find_foreign_error_signature` (drive.py:147+) keeps any other error fatal. The guided apply re-invokes `baha app apply --confirm-candidate <digest>` (new_edit.py:256).
- One observation (NOT a defect, no product change): `capture_confirm_hash` normalizes with `re.sub(r"\s+","", ...)` and searches `Re-runwith--confirm-candidate<digest>`; verified by python repro that the digest group still captures correctly (the whitespace collapse is intentional for hard-wrapped PTY output). No mismatch.

### Desk 3 — recut mcp_operator_seam_test completeness (#1741)

- Covered by FUND 1. The recut test is INCOMPLETE relative to develop: it is absent on develop entirely and, on #1741, references the undefined `withoutOperatorAuthTestContext` (the anonymous/red direction). Positive (stamped) direction is fully supported by the existing `operatorAuthFixtureContext` seam.
- go build ./cmd/baha/ on develop -> exit 0 (build only, no test exec). The seam test would NOT compile on develop until the opt-out helper is added.

## Fundbilanz

- echte defekte: 1 (FUND 1 — recut seam test references undefined `withoutOperatorAuthTestContext`; the negative/red direction of the MCP operator-auth gate is not yet reachable in-test on develop or #1741).
- doku-luecke: 0.
- kein-befund: 1 (FUND 2 — guided demo candidate-consent contract aligns).

## cleanliness

- READ-ONLY. No product code, no test code, no .github, no scripts changed.
- No git write beyond reading refs (checkout to a throwaway `dev-verify` branch HEAD 64eab13e2 for local `go build` — no commits; no push).
- `go build ./cmd/baha/` build only, NO test execution (no bare `go test ./cmd/baha/`).
- No container/network/volume/state created. No docker/podman compose project started (coordinator/codeman host; tests run only on named SSH hosts).
- ambient-core / fremder-lane images untouched.
- cleanliness: nothing changed.

## END

w27-pr1627-0428-061-pull DONE — findings only. FUND 1 (recut seam test references undefined `withoutOperatorAuthTestContext`) is kartenwuerdig; minimal rezept = add the opt-out helper to the #1741 operator-auth seam collection point as a test-only write (no operatorauth/** denial change). Awaiting Owner card decision.
