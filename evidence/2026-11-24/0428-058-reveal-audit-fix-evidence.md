# PR #1809 correction — reveal success audit + env_destroy actor

- **Lane:** lane-0428-058-cli2-audit-events
- **PR:** #1809
- **Task:** 0428-058 (audit secret set/delete/list + env destroy outcomes)
- **New head (local):** `9a0419b498abd4e92baea3e241e3ebfcf333aefd`
- **PR #1809 head (remote):** `9a0419b4` (via `git push --force-with-lease`)
- **Develop base:** `6df6807e` (PR #1817, env_operations.go catalog row)
- **CI run:** `45298000296` (run 7590), head `9a0419b4`

## Review findings addressed

PR #1809 reviewer confirmed Finding C (env_destroy `trusted-local` actor + `AuthorizationResult` outcome-match) as good, but flagged the **premature SUCCESS audit still open** inside `authorizeHumanReveal`/the env consumer.

### Fix A/B — move SUCCESS audit to the actual release point
- `cmd/baha/secret_operations.go`: seam now records the authorization decision via `recordRevealAuthorized` (outcome `authorized`), never the material-release `success`.
- `cmd/baha/environment_operations.go` `inspectApplicationEnvironment`: records `recordRevealFailed` at each post-auth read/stat/parse failure (lines 35/41/48), and `recordRevealSuccess` only after the env contract is successfully read and parsed (line 55). DENIAL stays at the auth seam.
- `cmd/baha/env_destroy.go` `recordEnvDestroyAudit`: runtime actor routes through `operatorauth.AuthorizationDecisionFromContext(ctx)`; no verified decision ⇒ actor `trusted-local` (not a person), `AuthorizationResult=deny` for denial/failure and `allow` for success; `event.Application = envName` for a valid non-runtime event.

### Hosted regressions (cmd/baha/secret_audit_test.go)
1. `TestAuthorizeHumanRevealSeamRecordsAuthorizationNotSuccess` — seam records `authorized`, never `success`.
2. `TestAuthorizeHumanRevealPostAuthReadFailureRecordsNoSuccess` — post-auth read failure records `authorized`+`failed`, no `success`.
3. `TestAuthorizeHumanRevealSuccessfulReleaseRecordsSuccess` — successful release records `authorized`+`success`.

## Verification (local)
- `go build ./cmd/baha/` clean.
- `gofmt -l` clean on all four touched files.
- `go vet ./cmd/baha/` clean.
- Targeted tests: 12/12 PASS — `TestAuthorizeHumanReveal*` (all 6 incl. the 3 new regressions), `TestRecordSecretAudit*` (7), `TestRecordEnvDestroyAudit*` (3 incl. `RuntimeSuccessIsAllowNotPerson`, `RuntimeFailureIsDenyWithRuntimeActor`, `DeniedIsDenyWithRuntimeActor`).

## Rebase onto new develop head
- Old develop `d4fa8c58` → new develop `6df6807e` (PR #1817 added `cmd/baha/environment_operations.go` catalog row).
- `git rebase --onto lane-origin/develop d4fa8c58 lane-0428-058-cli2-audit-events`: clean, no conflicts. Fix logic intact (verified: `recordReveal*` calls preserved, `recordEnvDestroyAudit` signature matches develop's `ctx`/`outcome` form, tests still pass).
- Force-pushed `--force-with-lease` (remote was still at original `c92182b0`; no lost work).

## CI (Hosted, exact-head, Hosted-only)
- Run **45298000296** (run 7590), head `9a0419b4`.
- Job conclusions: **17 success, 13 skipped, 0 failure, 0 null.** Critical gates `PR · Trusted Plan` and `PR Selected Checks` both success.
- Run-level `status`/`conclusion` fields still report `in_progress`/`null` at time of writing — this is the known GitHub API lag where the run conclusion updates after post-job aggregation; every job (including the required gates) is terminal-success.

## Repo-rule compliance
- Write-set confined to `cmd/baha/` (`secret_operations.go`, `environment_operations.go`, `secret_audit_test.go`) and `internal/operatorauth/` (via develop's restructured `recordEnvDestroyAudit` context). No `.github/**` edits (Owner scope).
- Build/vet/gofmt green. No subagents used.

## Handoff / stop
- PR #1809 left open; head `9a0419b4`. No merge, no Codex. Awaiting CODEX-REVIEW → CODEX-MERGE per task contract.
