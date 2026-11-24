# w68-0428-277-revealallow

## PLAN

- Read mission + task contract (t-20261124-0428-277-reveal-fail-authorizationresult-allow); verify planning repo remote + baseharbor remote + base SHA
- Cut worktree off develop (05ef485369), claim task, write evidence file under evidence/
- Implement fail-closed AuthorizationResult in recordRevealFailed: on failed reveal, set AuthorizationResult=deny (fail-closed), never spurious allow for a failed release. Write-set: cmd/baha/secret_operations.go + app_context.go (added AuthorizationResultOverride) + their tests.
- Add regression test asserting a failed reveal records deny/discrepancy and never a spurious allow
- go build, go vet, targeted reveal tests to terminal pass
- push candidate (5f23a7d1), open ONE PR #1823 against develop (05ef48536)
- monitor Hosted GitHub CI PR Selected Checks to terminal exact-head pass
- push evidence to origin/main before END post

## repo-rule compliance

- Write-set respected: only cmd/baha/secret_operations.go, cmd/baha/app_context.go, cmd/baha/secret_audit_test.go. No environment_operations.go change needed (bug is at the recordRevealFailed seam in secret_operations.go), no scripts/**, no .github/**, no operatorauth package files.
- No subagents (§4.8): every step run in own session.
- Hosted-only CI: no local go test / unit suite on coordinator host. Verification via exact-head Hosted GitHub CI run.
- One candidate per chain: single branch lane-0428-277-revealallow off 05ef48536.
- Merge done by CODEX, not this lane.
