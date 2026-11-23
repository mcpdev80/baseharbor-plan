# REVIEW and MERGE — PR #1753

## PLAN

1. Read mission and applicable authority/repository rules; establish the evidence path and review contract.
2. Verify current task ownership and exact remote PR head, base, diff scope, and ancestry.
3. Inspect the exact candidate and hosted native-gate logs for actual footprint-show test execution.
4. Record pass or blocked verdict with evidence and publish only if compliant.
5. Verify origin/main evidence path, update board, and post the required final handoff.

## Roles and context

ROLE: REVIEW, then MERGE after all mission gates passed.
Mission file: `/tmp/opencode/m_rev_1753e8.md.g`.
Planning task ID: `t-20261122-footprint-show-not-admitted-in-data-capabilities-gate`.
Session/model/backend: Codex review session; GPT-6.2; backend identity is not exposed by this interface.
Review and merge date: 2026-11-23 UTC.
Evidence path: `evidence/r28-welle5-2026-11-22/footprint-0428-234/review-merge-1753-6a8fbf5a.md`.

The mission labels the card `0428-234`; the authoritative Planning task frontmatter and PR title identify it as `0428-227`. I followed the exact task ID and PR named by the mission. This numbering discrepancy is recorded for coordinator reconciliation.

## Candidate identity, ancestry, and scope

Immediately before merge, the live PR was open, ready, and mergeable. Base was `develop` at `e8acf740553f7218b259f4855f5b79f83f21ab6b`; head was `6a8fbf5aa9cfe483151af16b3def3702fc96456e`. GitHub compare reported `ahead_by=15`, `behind_by=0`, and merge base exactly `e8acf740553f7218b259f4855f5b79f83f21ab6b`.

Pre-merge remote witness from the verified GitHub remote `lane-origin`:

```text
e8acf740553f7218b259f4855f5b79f83f21ab6b refs/heads/develop
6a8fbf5aa9cfe483151af16b3def3702fc96456e refs/heads/lane-0428-227-footprint-gate-admission
6a8fbf5aa9cfe483151af16b3def3702fc96456e refs/pull/1753/head
```

Exact compare file statistics:

```text
cmd/baha/app_broker.go                         +24 / -2
cmd/baha/ci_integration_operator_enabled.go    +17 / -0
cmd/baha/ci_integration_operator_enabled_test.go +69 / -95
internal/operatorauth/local_runtime.go         +1 / -1
internal/operatorauth/local_runtime_test.go    +30 / -0
```

The PR changes exactly these five paths; no `.github/**` or `go.mod` path is changed. Catalog `scripts/pr-gate-coverage.json` has the same blob SHA at base and candidate: `4b69ec21aae2e24a36013bb655788fda508f4d23`. The base catalog has 219 component rows, 219 unique IDs, and 219 unique paths. PR #1790 is merged at `c6a7138ce2bf7de88f45f2a68e5168c835601a16`; comparing that merge to the exact PR base shows it is an ancestor (`ahead_by=3`, `behind_by=0`).

## Content review

The product change adds `app.footprint.show` to the registered read-only local-runtime allowlist and adds a test verifying the operation is registered, read-only, and accepted by `CheckLocalRuntimeGrant`. The command-boundary regression admits only canonical `app footprint show -o json` on data-capabilities, rejects noncanonical and unrelated commands, and retains guided admission while rejecting lifecycle admission.

The runtime broker readiness change treats transient starting state as retryable. The expected/actual version message now reports the actual runtime version. No migration or unrelated state rewrite is added.

Nonblocking cleanup note: `cmd/baha/ci_integration_operator_enabled.go:151-164` contains a second data-capabilities footprint-show admission after the pre-existing condition at lines 151-153 already admits the same canonical form for data-capabilities and core-capability. Its helper delegates directly to the same predicate. This is redundant and the added branch is unreachable for the data-capabilities case; it does not invalidate the behavior proven below. A follow-up can remove the duplicate branch/helper and retain the focused regression.

## Hosted checks and test-to-gate evidence

Exact workflow run `45098577557` completed with conclusion `success`, event `pull_request`, and exact head `6a8fbf5aa9cfe483151af16b3def3702fc96456e`.

The required `PR Selected Checks` check-run `137450946656` completed successfully from GitHub Actions integration `15368`. Its terminal log lines include `NATIVE_REQUIRED: true`, `UNIT_RESULT: success`, and `PR Selected Checks: PASS`. The live required-check ruleset `25223521` is active on `develop` and requires context `PR Selected Checks` from integration `15368`. No check was bypassed. The `develop - integration branch` ruleset was observed disabled; no protection state is claimed for it.

Both native gate jobs completed successfully on GitHub-hosted runners:

- Docker selected data-capabilities runtime job `137444362837`: log reports `demo-data-capabilities PASS` and `RESULT PASS`.
- Podman selected data-capabilities runtime job `137444362898`: log reports `demo-data-capabilities PASS` and `RESULT PASS`.
- Native Docker job `137443933687` and native Podman job `137443933751` both executed `TestApplicationCapabilityLifecycleExistingCore`; each emitted an `Action":"pass"` record and completed successfully.
- The footprint-specific command test `TestCIIntegrationOperatorAdmitsFootprintShowOnlyOnDataCapabilitiesGate` is in the changed `cmd/baha` test file and was covered by successful `PR · Go unit · cli-3` job `137443951052` (433 passed, 16 intentionally skipped, 449 discovered). `TestCheckLocalRuntimeGrantAdmitsFootprintShowReadOperation` is covered by the successful package unit job `137443951055`.

The two selected native data-capabilities runtime cells were actually executed, not skipped. The selected runtime logs show the data-capabilities acceptance group completed successfully. No local product tests were run, no workflow was edited or rerun, and no VM was used.

PR review submissions and unresolved review threads were both empty at final refresh. This session performed the independent review of the complete current diff before the merge.

## Merge result and remote witness

The expected-head guarded squash merge succeeded. GitHub returned merge SHA `1b7598aef8c4cae33b77c8523872637090d0f2bf`.

Post-merge `git ls-remote lane-origin refs/heads/develop refs/pull/1753/head` output:

```text
1b7598aef8c4cae33b77c8523872637090d0f2bf refs/heads/develop
6a8fbf5aa9cfe483151af16b3def3702fc96456e refs/pull/1753/head
```

The PR is merged. The remote branch `lane-0428-227-footprint-gate-admission` is no longer present. The Planning task still shows `blocked` under Coordinator ownership; its owner should reconcile that status and the `0428-234`/`0428-227` number discrepancy based on this merge witness.

## repo-rule compliance

This session reviewed and merged only the mission-named PR. Product files and workflows were not edited locally. No tests were run locally. No force push, protection bypass, or extra product branch was created. No containers or compose projects were started on this host.

Planning remote was verified before evidence publication:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## cleanliness

Before review, shell PID `3347110` ran `docker ps -a`; output contained only the header and no containers. After review, shell PID `3385467` ran `docker ps -a`; output contained only the header and no containers. No compose project was created.

END_DONE codex-rev2-1736: PR #1753 merged at `1b7598aef8c4cae33b77c8523872637090d0f2bf`; exact head `6a8fbf5aa9cfe483151af16b3def3702fc96456e` passed required selected checks and both native data-capabilities runtimes.
