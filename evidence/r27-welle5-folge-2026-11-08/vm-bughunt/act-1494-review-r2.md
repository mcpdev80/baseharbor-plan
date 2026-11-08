# CODEX-REVIEW — 0427-164 r2 — PR #1494

## ROLLE: REVIEW

## PLAN

1. Refresh the PR head, current develop ref, predecessor head, and terminal hosted run.
2. Compare the r2 delta against the previous review and inspect the parser, execution path, consent guard, and regression coverage.
3. Verify the relevant CI group executed on the exact candidate and distinguish successful jobs from skipped jobs.
4. Record verdict, findings, and any merge-time caveat in this Planning evidence file.
5. Publish the act to baseharbor-plan main and post END.

## Verdict: APPROVE

The r2 candidate fixes the parser-stage defect identified in act-1494-review.md. The real CLI entry test proves the documented non-TTY invocation reaches the detach operation; the no-yes case remains fail-closed. The existing consent path still requires both current acknowledgements, and the change does not authorize data deletion.

## Candidate and ancestry

- Repository: mcpdev80/baseharbor.
- PR #1494 is open and mergeable. Exact head: 95afe20411d6949335cb902f621c1cca5a7f8ec5, branch work/w164-target-delete-nontty-consent.
- Previous reviewed head 468027889093cfa776f2851cd9ea765cb4365d6c is the parent of the r2 head; ancestry check succeeds. The r2 delta commit changes only cmd/baha/target.go and cmd/baha/bugs_858_860_regression_test.go. The full PR write-set is five files, all under cmd/baha; no .github files or runtime-destroy path changed.
- Live product ls-remote witness:
  20902f0a6ab016fd8fe6a501751e1becc5f334dd	refs/heads/develop
  95afe20411d6949335cb902f621c1cca5a7f8ec5	refs/heads/work/w164-target-delete-nontty-consent
  95afe20411d6949335cb902f621c1cca5a7f8ec5	refs/pull/1494/head
- PR metadata reported base SHA 171e9569d4bdea0b03faca663dc88a41e185f75f, while the fresh develop ls-remote is 20902f0a6ab016fd8fe6a501751e1becc5f334dd. The code review is approved on the exact head; before any merge, confirm the required selected-check result still applies to the current develop base.

## Review findings

### 1. Argument parsing

In cmd/baha/target.go:548-575, deleteTarget parses output options, recognizes --yes and -y, and appends only remaining positional arguments to kept. It assigns args = kept before requiring exactly one NAME. This works whether the flag occurs before or after the name. Unknown options still return a usage error. The fix resolves the prior failure where NAME plus --yes incorrectly produced “requires NAME”.

### 2. CLI entry and fail-closed behavior

TestTargetDeleteNonTTYYesReachesArgParser in cmd/baha/bugs_858_860_regression_test.go:396-438 uses runWithIO through the real dispatcher with --no-input:

- target delete NAME --yes succeeds and removes the target config entry.
- target delete NAME without --yes returns impact-confirmation-required and preserves the config entry.
- -y also succeeds.

The earlier lower-level target-definition regression at cmd/baha/target_definition_change_test.go:52-80 confirms config-only detach writes a recovery file and preserves protected runtime-owner bytes.

The interactive branch in cmd/baha/target_definition_change.go:38-45 remains unchanged and calls readProviderImpactAcknowledgements with the current plan's confirmation count. That reader loops through each required stage at cmd/baha/provider_change_confirmation.go:58-81. The target-definition plan test asserts two confirmations and rejects missing, single-stage, or stale consent at cmd/baha/target_definition_change_test.go:102-123. The original hx3 dossier also records both prompts in the real interactive path. The r2 CLI regression pins the non-TTY cases; it does not add a new end-to-end TTY invocation.

### 3. Destructive consent remains separate

At cmd/baha/target_definition_change.go:46-63, assumed yes synthesizes only First and Second consent and only when plan.Scope.Destructive is false. It does not set DeleteData. A destructive scope therefore still reaches ValidateProviderImpactScopeConsent without fabricated consent. The shared destructive confirmation tests in cmd/baha/provider_change_confirmation_test.go:16-38 require the separate deletion acknowledgement. This PR path is config-only, retains runtime/data owners, and does not touch baha destroy or its zeroing path.

### 4. Hosted CI

GitHub run 42520608394 for exact head 95afe20411d6949335cb902f621c1cca5a7f8ec5 completed with conclusion success. PR Selected Checks succeeded. The PR · Validation · go-unit-tests job succeeded; it ran scripts/pr-unit-database.sh on the pull_request event and logged the cmd/baha package passing. This package contains TestTargetDeleteNonTTYYesReachesArgParser.

There were 12 successful jobs, 12 conditional jobs skipped, and no failed or pending jobs. Skipped jobs are not counted as executed passes. The target-delete change is limited to config consent and does not require the skipped native runtime families for this regression.

## repo-rule compliance

- Product candidate was reviewed read-only; no product refs were changed.
- No tests were run locally, no workflows were edited or rerun, and no VM/container work was started.
- Evidence is stored only in baseharbor-plan.
- Planning pre-push witness: 57c8d9f520a3bb95df473d2319f208ebd290f459	refs/heads/main
- No merge, tag, or release action was performed.

## END

END 0427-164-review-r2: APPROVE — exact head 95afe20411d6949335cb902f621c1cca5a7f8ec5; CI run 42520608394 terminal success, PR Selected Checks pass.
