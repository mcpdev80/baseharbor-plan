# CODEX-REVIEW — 0427-130 R4 / PR #1459

## PLAN

1. Verify current GitHub PR head, develop head, exact diff, commit ancestry, and hosted result on the candidate SHA.
2. Compare the R4 regression against the R2 review stop criterion and the card's actual command-entry acceptance.
3. Inspect the Docker and Podman job logs to identify which tests really ran.
4. Record the verdict, actionable correction recipe, and stop condition in planning evidence.
5. Publish this act to the verified baseharbor-plan origin/main and confirm its remote presence.

## Verdict

**ROLLE: REVIEW**
**URTEIL: KORREKTUR (REQUEST-CHANGES)**
**PR #1459 head:** `b3bb20416c69919af02bd854b3966cfe5e3761ca`
**Current develop:** `223042bc0372f41a6f0a7c2d1a2e01b095bb7a0b`

The claimed R4 command-entry test is not present at the exact PR head. The existing `TestUpNameResumesRegisteredDeploymentAcceptsParity` still tests parsing and calls `resolveRegisteredApplication` directly. The hosted run is terminal green, but its native Docker and Podman cells run the unrelated installation-destroy retry test, not the `baha up NAME` command. The R2 stop finding therefore remains.

### 1. The regression still bypasses the top-level command entry

At `cmd/baha/runtime_ports_test.go:342-420`, `TestUpNameResumesRegisteredDeploymentAcceptsParity` creates a registered deployment and confirms parser parity. It then calls `resolveRegisteredApplication` directly at line 386; its fail-closed case calls the same resolver directly at line 417. There is no `runWithIO` call, and no `runWithIO`, `rootCommand`, or `runtimeUpCommand` invocation in this test file. It does not execute `baha up NAME --yes --plain` outside an application repository.

The round-4 claim that the regression enters the CLI through `runWithIO` conflicts with the source at the exact reviewed head. The test proves resolver behavior when explicitly given `NAME`; it does not prove the top-level parser and command route `NAME` into that resolver. Its unknown-name negative also seeds a foreign registration under that name and directly calls the resolver, rather than verifying fail-closed behavior from the top-level command for an unknown/unregistered name.

**Correction recipe:** in `cmd/baha/runtime_ports_test.go`, replace or extend this test to invoke `runWithIO` with the actual top-level command. From a temporary working directory outside a repository, seed the registered deployment and invoke `up NAME --yes --plain`; assert it resumes/selects the exact deployment through the command's production path. Invoke `app up NAME` with the same fixture and assert the same selected deployment. Invoke top-level `up UNKNOWN --yes --plain` through `runWithIO` and assert it fails closed without falling back to another repository or deployment. Retain parser parity as a separate focused assertion.

The existing `PR · Validation · go-unit-tests` job runs the `cmd/baha` Go tests on `pull_request`, so the corrected test belongs in that package and must be exercised by that job on the final exact candidate SHA.

**Stop criterion:** the registered-name, parity, and unknown-name assertions all execute through `runWithIO` and demonstrate the top-level command behavior; the exact-head `go-unit-tests` and `PR Selected Checks` are terminal green. The current source does not meet this condition.

### 2. Candidate scope and drift provenance

`b3bb20416c69919af02bd854b3966cfe5e3761ca` is a merge commit with parents `da68dd48abab8acc48d8e882d39015cef257e710` and `cd494610c9327d122720e90851ce1f818e5d073e`. The candidate branch contains the R2 and R3 task commits plus one drift merge whose second parent is the exact `cd494610` develop head. `git log --oneline cd494610..b3bb2041` lists only those four commits; there are no extra foreign candidate commits on that branch.

The three-dot product diff from that base contains eight files: six `cmd/baha` files and the English/German CLI command indexes. It contains no `.github/**` file. The drift merge carries the develop content present at `cd494610`.

Live develop has since advanced to `223042bc0372f41a6f0a7c2d1a2e01b095bb7a0b` through `201735b0` (#1460) and `223042bc` (#1407). Those later commits change Keycloak/use-target and remote-up paths, not the alias parser/test files, but the PR no longer has a current-base freshness witness at review time. `gh pr view 1459` currently reports `mergeable=UNKNOWN` and `mergeStateStatus=UNKNOWN`; the round-4 report's `MERGEABLE/CLEAN` statement is not the live API result. Resolve current mergeability at landing time and refresh/review any changed candidate SHA.

### 3. Hosted run and native cell scope

Run `42475609941` is terminal success on the exact PR head `b3bb20416c69919af02bd854b3966cfe5e3761ca`. `PR · Validation · go-unit-tests` (job `128716229423`) and `PR Selected Checks` (job `128718353300`) passed.

Both named native jobs actually executed and passed, but their logs identify a different test:

- `PR · Native destroy retry · docker`, job `128716218501`: log records `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` and ends `PASS: native installation destroy current-scope, partial failure, retry and foreign preservation`.
- `PR · Native destroy retry · podman`, job `128716218424`: log records the same `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` and the same native destroy/retry pass result.

These are real hosted Docker and Podman executions, not skips. They prove the destroy-retry test passed; they do not exercise or replace the missing command-entry `baha up NAME` regression. The native Keycloak/Core job is skipped, but the card's required check for this CLI behavior is the unit/CLI regression, not those destroy jobs.

### Stop criterion

Do not approve until the production command-entry regression exists and passes on the exact final head. Preserve the parser parity assertion, prove registered-name resume and unknown-name fail-closed through `runWithIO`, and obtain terminal green `go-unit-tests` and `PR Selected Checks`. Do not count the native destroy-retry cells as evidence for the up-name alias. Confirm current mergeability and base freshness before any merge action.

## Evidence witnesses

- `git ls-remote https://github.com/mcpdev80/baseharbor.git` returned:

```text
223042bc0372f41a6f0a7c2d1a2e01b095bb7a0b	refs/heads/develop
b3bb20416c69919af02bd854b3966cfe5e3761ca	refs/pull/1459/head
```

- `gh pr view 1459` reports OPEN, base `develop`, head `b3bb20416c69919af02bd854b3966cfe5e3761ca`; the live `mergeable` and `mergeStateStatus` fields were both `UNKNOWN`.
- `git show origin/pr-1459:cmd/baha/runtime_ports_test.go` contains the resolver calls at lines 386 and 417 and no `runWithIO` invocation in the test file.
- Run `42475609941` is terminal success on the exact head. The `go-unit-tests` and `PR Selected Checks` jobs passed. Native Docker job `128716218501` and native Podman job `128716218424` both ran `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` and passed.
- Planning repo verified by `git rev-parse --show-toplevel` as `/tmp/opencode/0427-130-r4-review-plan-wt`, with origin `https://github.com/mcpdev80/baseharbor-plan.git`.
- Pre-publication `git ls-remote origin refs/heads/main` returned:

```text
a1e9c7afa4ac013f39d097dbd0404a857b291256	refs/heads/main
```

- This review changed no product files, PR refs, or workflows and started no tests, reruns, dispatches, containers, or VM work.

## END

END_BLOCKED 0427-130-review-r4 — KORREKTUR: exact head `b3bb2041` still has no `runWithIO` command-entry regression; the alleged test directly calls `resolveRegisteredApplication`. Hosted unit and selected checks pass, and native Docker/Podman jobs really ran, but those jobs exercised installation destroy retry, not the up-name alias. No CODEX-MERGE authorization.
