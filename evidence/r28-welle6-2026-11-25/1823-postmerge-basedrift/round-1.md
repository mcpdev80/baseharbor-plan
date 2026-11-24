# 1823 post-merge verification + new-develop base-drift — READ-ONLY Befund

Shift: r28-welle6-2026-11-25 · Lane: w96-0428-277-postmerge-drift · Type: READ-ONLY Befund (no edits/PR/merge/CI-trigger)

## PLAN

- Confirm #1823 landed correctly on develop tip (file:line witness)
- BASE-DRIFT analysis for the serial chain (#1819, #1820, #1812): file-overlap with #1823 + rebase cleanliness
- State new exact develop SHA each serial lane must rebase onto + whether #1823 touched any gate-plan/coverage

## Baseline attestation

- develop exact SHA (git ls-remote, ssh origin ssh://git@github.com/mcpdev80/baseharbor.git):
  `f14fb87c8f5afd91168e4f174d620c9f00e6341e` (refs/heads/develop)
- #1823 commit on develop tip: `f14fb87c fix(0428-277): fail-closed AuthorizationResult for failed reveal (#1823)` (2026-11-24 15:44:37 +0100)
- This SHA is the develop HEAD (verified via fresh fetch, not the quarantined workers/baseharbor checkout)
- develop ancestry at f14fb87c: ... #1821 (05ef4853) → #1824 (2b9a2c6d) → #1825 (46d3dccc) → #1823 (f14fb87c)

## 1. #1823 confirmed present on develop tip (Y)

File:line witnesses on origin/develop @ f14fb87c:

- `cmd/baha/secret_operations.go`
  - `recordRevealFailed` (func at line 154) routes through shared `recordRevealForTarget` with the deny override: `}, "failed", reason, "deny")` at line 171.
  - `recordRevealForTarget` signature now takes `authorizationResultOverride string` (line 189).
  - Override applied at lines 221-222: `if authorizationResultOverride != "" { event.AuthorizationResult = authorizationResultOverride }`.
  - Attribution block (lines 205-217) runs BEFORE the override, so the authenticated actor (Subject/Assurance/Methods) is preserved on failed reveal.
- `cmd/baha/secret_audit_test.go`
  - `TestAuthorizeHumanRevealFailedRecordsRevealAudit` seeds an ALLOWED `operatorauth.AuthorizationDecision` (lines ~332-346): `Allowed: true`, `Actor.Assurance: "loa2"`, `Actor.Methods: []string{"password", "webauthn"}`, `Subject: "trusted-local"`.
  - Asserts `event.AuthorizationResult == "deny"` even under the upstream allow (fail-closed) — lines ~362-367.
  - Asserts spurious-allow is rejected (line ~369-371), `event.Actor.Subject == "trusted-local"` (RC2, line ~383), `event.Actor.Assurance == "loa2"` (line ~388), `event.Actor.Methods == [password webauthn]` exact (line ~390).
- Behavior is additive to the audit path; no other behavior regressed. No other files touched (write-set = exactly the two files above).

Conclusion: **#1823 confirmed Y** — fail-closed deny routing, loa2/webauthn actor preservation, expanded assertions all present at the exact lines quoted.

## 2. Base-drift table for the serial chain

| Lane | Card | HEAD (origin) | Merge-base w/ develop | Write-set (vs develop) | Overlaps #1823 files? | Rebase-onto (new develop) | Clean (git merge-tree)? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| #1819 | w54-0428-181-export | 17381017 (fix 0428-181 RC1/RC2) | 05ef4853 (#1821, 2026-11-24 11:21) | `.github/workflows/pre-release.yml`, `cmd/baha/env_destroy_integration_test.go`, `cmd/baha/secret_audit_test.go`, `cmd/baha/secret_operations.go`, `internal/application/runtime_postgres.go`, `internal/deployment/environment_destroy_scope.go`, `internal/deployment/environment_destroy_scope_test.go`, `internal/metrics/perses_dashboard_provision.go`, `internal/metrics/perses_dashboard_provision_test.go` | YES — both `cmd/baha/secret_operations.go` AND `cmd/baha/secret_audit_test.go` | f14fb87c8f5afd91168e4f174d620c9f00e6341e (post #1823) | merge-tree clean (0 conflict lines) BUT content is REVERSE of #1823 |
| #1820 | fresh-from-develop cut (pending) | n/a | n/a | to-be-cut | depends on cut base | f14fb87c8f5afd91168e4f174d620c9f00e6341e (or later) | N/A until cut |
| #1812 | lane-0428-249-runtime-image-fix (blocked on consent) | 47590207 (ci: reload candidate image before runtime publish) | 46d3dccc (#1825, 2026-11-24 13:43) | `.github/workflows/pre-release-runtime-suite.yml` (Owner scope), `cmd/baha/secret_audit_test.go`, `cmd/baha/secret_operations.go` | YES — both `cmd/baha/secret_operations.go` AND `cmd/baha/secret_audit_test.go` (the runtime-suite yaml is Owner-scope, separate) | f14fb87c8f5afd91168e4f174d620c9f00e6341e (post #1823) | merge-tree clean (0 conflict lines) BUT content is REVERSE of #1823 |

Key drift facts:

- Both #1819 and #1812 are based on **pre-#1823** develop (`f14fb87c` is NOT an ancestor of either lane head — verified via `git merge-base --is-ancestor`). Their merge-bases are #1821 (05ef4853) and #1825 (46d3dccc) respectively, both BEFORE #1823 landed.
- The shared-file changes on #1819 and #1812 are the **reverse** of the #1823 fix: they revert `recordRevealForTarget` from the 6-arg form (`outcome, detail, "deny"`) back to the old 3-arg form (`outcome, reason`), and strip the fail-closed override + the expanded test assertions.
- `git merge-tree --write-tree develop <lane>` reports 0 conflict lines for both lanes — i.e. the hunks happen to be disjoint enough to apply cleanly. BUT the merge is semantically wrong: it would DROP #1823's fail-closed behavior and its regression assertions, leaving the audit regression reintroduced. A clean merge-tree is NOT acceptance here — the lane must rebase/merge onto post-#1823 develop and RE-APPLY its own changes on top of the fix, not silently drop it.
- No #1823 file overlaps with any `perses_dashboard_provision*` (#1819) file or with `internal/deployment/environment_destroy_scope*` (#1819) — the only #1823 overlap is the two secret files.

## 3. New exact develop SHA each serial lane must rebase onto + gate-plan impact

- Exact develop SHA to rebase onto (post #1823): **f14fb87c8f5afd91168e4f174d620c9f00e6341e** (report; expect f14fb87c8 as the mission predicted — confirmed).
- #1820: cut from this exact SHA (or later), do NOT cut from a pre-#1823 base.
- #1819, #1812: rebase onto f14fb87c8 (or later) when their turn comes; the pre-#1823 base reintroduces the #1823 revert and must be rebased to re-apply cleanly on top of the fix.
- #1823 is a **product test + narrow source fix only** — it touches NO gate-plan file (`.github/**` untouched) and NO coverage-configuration file. It introduces no gate-plan or coverage change affecting #1819/#1820/#1812. (Caveat: #1819/#1812 carry their own widened test assertions in the same secret files; their CI coverage depends on their own PR's CI-group, not on #1823.)

## Evidence witnesses (read-only, created nothing)

- `git ls-remote ssh://git@github.com/mcpdev80/baseharbor.git refs/heads/develop` → `f14fb87c8f5afd91168e4f174d620c9f00e6341e`
- `git show f14fb87c --stat` → only `cmd/baha/secret_audit_test.go` + `cmd/baha/secret_operations.go`
- `git merge-tree --write-tree develop <lane>` → clean for both #1819 and #1812
- `git merge-base --is-ancestor f14fb87c <lane>` → NO for both (both pre-#1823)
- No product files edited, no branch cut, no PR, no CI triggered. No subagents (§4.8). Contacted no other session.

## cleanliness

- Created nothing in the product repo. Read-only verification in a throwaway fetch zone `/tmp/baha-verify` (not a product checkout, not the quarantined workers/baseharbor). No containers/compose projects started. No docker/podman state.

## END

END lane w96-0428-277-postmerge-drift DONE — read-only Befund delivered, no edits.
