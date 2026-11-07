# CODEX-REVIEW PR #1420

## PLAN

1. Read the mission and verify fresh exact PR head/base remote SHAs.
2. Inspect the exact candidate diff against the task contract and requested findings.
3. Check relevant evidence, exact-head CI state, and owner-scoped skips.
4. Record a SHA-specific verdict and actionable findings in planning evidence.
5. Publish evidence on planning origin/main, verify its remote tree entry, and post END.

## Review identity and candidate

Role: CODEX-REVIEW. Card t-20261018-r27-client-commands (0427-022). Product repository: mcpdev80/baseharbor. PR #1420 is OPEN, non-draft, mergeable, base develop. Fresh `git ls-remote` witness from the product clone:

```
eee11d50b7a7b55675a282f03d4a1a78e4511cf0 refs/heads/develop
0c23adc56151b94f05916ffcc0cc13b061961107 refs/pull/1420/head
```

Candidate head is `0c23adc56151b94f05916ffcc0cc13b061961107`; base head is `eee11d50b7a7b55675a282f03d4a1a78e4511cf0`. `git merge-base --is-ancestor <base> <head>` returned 0. `git diff --stat <base> <head>` reports exactly `cmd/baha/client_commands_behaviors_test.go | 235 +...`; name status reports only that added file. No workflow files or product implementation changed. Planning repository identity was verified before this evidence commit:

```
origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Planning checkout top-level: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.

## Contract and verdict

The task requires “Real CLI->TLS API tests with two independent homes/checkouts, same deployment, precedence, denial, server loss, stale consent and error parity.” Verdict: **REJECT_LANE_FIX**. The candidate adds five test functions, but the tests are fixture-level calls into internal seams, not real CLI-to-TLS journeys. They use two temporary directories while not establishing that both address the same deployment identity through a TLS client/server. The new tests therefore do not prove the card's central transport and shared-deployment condition.

The fixture at `cmd/baha/application_core_authority_test.go:22-43` configures a local test target and injects synthetic verified principal and tenant contexts. It has no TLS listener or API client. The new test file itself imports no TLS or HTTP test harness (`cmd/baha/client_commands_behaviors_test.go:3-19`).

Behavior findings:

- Precedence: `TestClientCommandsTwoHomesSameDeploymentPrecedence`, `cmd/baha/client_commands_behaviors_test.go:59-100`, invokes `runWithIO` for `app init` twice, but `configureTestTarget` uses the local test target and the test only asserts that each home receives a nonempty server-shaped ID. It does not assert a common deployment or shared identity. The cited `TestCLIProductionPathAssignsServerIdentityProves`, `cmd/baha/app_binding_production_test.go:30-84`, is one home and local-target-backed. The separate two-home test at `app_binding_production_test.go:86-139` asserts distinct per-home IDs, not one shared deployment, and is also local-target-backed. Coverage for the required same-deployment TLS precedence is missing.
- Denial: `TestClientCommandsDenialOverTwoHomes`, `cmd/baha/client_commands_behaviors_test.go:106-145`, directly calls resolve/record/execute helpers. It correctly checks `ErrorApprovalRequired` and unchanged intent, but explicitly expects denial before transport. The cited `TestRemoteApplyCannotPublishBeforeCurrentProviderAcknowledgement`, `cmd/baha/application_remote_authorization_test.go:17-49`, is likewise a single-home helper test. Neither proves denial through TLS across two homes. No tamper inversion scenario is exercised by this test.
- Server loss: `TestClientCommandsServerLossOverTwoHomes`, `cmd/baha/client_commands_behaviors_test.go:151-168`, loops two working directories while passing the same prebuilt `remoteResolved` value and directly invokes `newResolvedApplicationStatusCollection`. It checks `ErrUnavailable`, which is fail-closed at this seam, but makes no TLS request. The cited `TestRemoteApplicationStatusNeverInfersAbsenceFromLocalFiles`, `cmd/baha/app_remote_status_test.go:12-37`, is one home and directly tests the status helper.
- Stale consent: `TestClientCommandsStaleConsentOverTwoHomes`, `cmd/baha/client_commands_behaviors_test.go:173-212`, calls the internal apply helper from each home and checks a machine error and unchanged intent. It does not cross TLS; it also does not pin the expected error code.
- Error parity: `TestClientCommandsErrorParityOverTwoHomes`, `cmd/baha/client_commands_behaviors_test.go:217-235`, sends a bogus flag to `resolveApplication` directly and compares classified error codes. It is not a command-runner or TLS API parity test.

The assertions that are present generally fail closed at their tested internal seam, but that is not evidence of the required end-to-end fail-closed behavior. The fix should exercise the actual CLI command runner and TLS API client against a TLS test server/shared deployment, use two independent home/store roots bound to the same deployment, and assert each of the five behaviors through that path. Keep the denial and stale-consent cases from mutating protected intent, and include the required tamper inversion proof if that remains part of the acceptance claim.

## CI and existing runtime test

The exact-head GitHub run is `42354903947` (run number 4990, pull_request event, candidate head above), terminal success. `cli-package-tests` job `128350778682` passed, and `PR Selected Checks` job `128352623844` passed. The CLI selected check maps to `go test ./cmd/baha -count=1 -json` in `scripts/pr-check-runner.py` (`cli-package-tests` route); the PR check's matched package is `./cmd/baha`, so this added package test is in its CI group. The group permits opt-in skips (`allow_skips=True`). No workflow edit or rerun was performed.

Targeted Docker, Podman and selected-runtime jobs were skipped by the owner push-ref gate, as specified in the mission. These are owner-scoped runtime gates and are not a reason for this review rejection.

`TestAppEditCommandCompleteProviderEditRunsRealLifecycle` is unchanged by this one-file delta (`cmd/baha/app_edit_apply_test.go:890-970` is outside the diff) and requires a real Docker Core/OpenBao runtime. The previous same-base #1419 comparison recorded the same test failing on both base and candidate with `existing native network lacks a protected Core or shared backend owner` (`evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-5.md:74`). This is a pre-existing runtime-dependent failure, not introduced by #1420. The CLI package job allows opt-in runtime skips; its package pass does not convert that Docker runtime failure into evidence for the new TLS acceptance requirement.

## Repo-rule compliance

This was a read-only review of the exact PR candidate. No product files, workflows, CI runs, or PR state were changed. Evidence is stored only in the genuine planning repository verified above. No subagents were used. No Docker or Podman project was started.

## END CODEX-REVIEW DONE

CODEX-REVIEW 0427-022/#1420-review-a verdict=REJECT_LANE_FIX head=0c23adc56151b94f05916ffcc0cc13b061961107 two_home_tls=simulated coverage=precedence-LUFT/denial-LUFT/server-loss-LUFT/stale-consent-LUFT/error-parity-LUFT fail_closed=internal-seams-only ci=42354903947+128350778682+128352623844 TERMINAL delta=one-file preexisting_red=owner-runtime-gate recipe=add real CLI-to-TLS tests over two independent homes bound to the same deployment and cover all five behaviors, including tamper denial
