# CODEX-REVIEW 0427-132 — PR #1453 destroy retry

Date: 2026-11-08

## PLAN

1. Verify the exact PR head, develop base, ancestry, and changed-file set from fresh remote state.
2. Review the destroy-discovery delta against the #1448 fail-closed local-runtime contract and the retry fixture.
3. Verify whether the named native retry test actually ran in hosted CI on this candidate.
4. Record the verdict, precise correction, test requirements, and stop criteria in the planning vault.
5. Validate and publish this review act to baseharbor-plan origin/main.

## Candidate and remote witnesses

- Repository: `mcpdev80/baseharbor`, PR #1453, open and mergeable.
- Candidate head: `fd3dd0c2c2d747a21545e518e7c8f965f0f7f2ea` (`gh pr view` and `git ls-remote` `refs/pull/1453/head`).
- Base: `develop` at `e39b0004346cdfd082e34ba55d94d24757bbbd27` (`git ls-remote`). `git merge-base --is-ancestor e39b0004346cdfd082e34ba55d94d24757bbbd27 fd3dd0c2c2d747a21545e518e7c8f965f0f7f2ea` exited 0.
- Exact diff: one file, `cmd/baha/runtime_destroy_all.go`; 6 insertions and 8 deletions. No test or workflow files changed.
- Planning repository identity: `/tmp/opencode/0427-013-r6-plan-publish`; remote `origin` is `https://github.com/mcpdev80/baseharbor-plan.git`.

## Verdict

**REQUEST-CHANGES.** The distinction introduced by this patch is directionally correct and preserves #1448's no-guessed-provider behavior, but the new `os.Stat` check fails open on every error other than success. In addition, the reported hosted run does not execute the named native retry test.

## Findings

### 1. Runtime-owner lookup treats lookup failures as proof of absence

At `cmd/baha/runtime_destroy_all.go:343-346`, a `local` runtime owner is treated as present only when `os.Stat(.../targets/local/runtime)` returns nil. Every other error falls through to the nonblocking recovery result. This conflates `ENOENT` (the expected deployment-only orphan case) with permission errors, I/O errors, and other failures that do not prove the runtime directory is absent. Since the destroy blocker count uses the `preserved because` detail as a safety boundary, an unreadable owner path can be treated like an absent owner and allow later cleanup to proceed.

The positive part is correct: the code does not infer or restore the legacy `compose` provider. A present `targets/local/runtime` directory still produces the blocking `preserved because` result, retaining #1448's fail-closed local-runtime scoping. A deployment-only orphan should remain a nonblocking recovery `SKIPPED` so a retry is not wedged.

### 2. The named test is not demonstrated green on this PR head

Run `42442084950` is terminal success on the exact candidate SHA. `PR · Validation · go-unit-tests` and `PR Selected Checks` passed, but both `Targeted HA · docker` and `Targeted HA · podman` were skipped. The test `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` at `cmd/baha/installation_destroy_native_test.go:20-22` immediately skips unless `BASEHARBOR_INSTALLATION_DESTROY_ACCEPTANCE=1` is set. The PR `go-unit-tests` path is `scripts/pr-unit-database.sh` (`.github/workflows/ci.yml:816`), which runs package tests without that acceptance variable. Therefore its green result does not establish a pass for the named test.

The actual acceptance wrapper is `scripts/ci-native-installation-destroy.sh`, called by the Docker and Podman runtime acceptance workflows. Those workflows require the acceptance environment and assert exactly one test `pass`, but their normal push trigger is `develop` / runtime-validation branches; the candidate's PR run did not include those jobs. No rerun or workflow dispatch was requested or performed. If pre-merge proof on this candidate is mandatory, the CI owner must provide an authorized candidate-SHA native gate selection; `.github/**` remains owner-owned.

### 3. Destroy-path scope and readability

The source diff is confined to `discoverFullDestroyTargets()` and does not alter runtime destruction, cleanup order, or deletion routines. It changes whether an unknown local target's `runtime-provider` discovery result counts as a blocker. The patch does not modify the test suite, so the implementation's two branch cases are not newly protected by a durable regression test in this diff. The readability audit passed on run `42442084950`; the file is 797 lines, below the 800-line limit, and no new helper or dead code was introduced. The long explanatory comment at line 344 can be split for readability but is not the acceptance blocker.

## Correction recipe

- File: `cmd/baha/runtime_destroy_all.go`, `discoverFullDestroyTargets()` around lines 343-349. Treat only `errors.Is(statErr, os.ErrNotExist)` as evidence that the runtime owner directory is absent. For any other stat error, append a blocking `FAILED` or `SKIPPED` result whose detail contains `preserved because` and retain the unknown provider; do not infer a provider.
- Tests: add durable unit coverage for three outcomes: deployment-only `local` state with missing `runtime/` remains a nonblocking recovery result; an existing `runtime/` remains blocking; and an injected non-ENOENT stat failure remains blocking. Keep the #1448 regression `TestMissingLocalTargetRegistrationNeverInventsComposeDestroyAuthority` passing. Put the injected lookup behind a small testable helper rather than relying on filesystem permissions that behave differently under privileged runners.
- CI requirement: the new unit cases must pass in the selected `go-unit-tests` job on the corrected candidate. Separately, show the named native retry test as PASS in the Docker and Podman acceptance job(s) for the exact candidate SHA if pre-merge native evidence is required. A skipped job or a package-level green status is not that proof. The workflow owner must make any needed `.github/**` selection change.
- Stop criterion: do not approve while non-ENOENT lookup errors can be interpreted as absence, while any #1448 runtime-owner regression test fails, or while the required exact-SHA native acceptance remains skipped/unobserved.

## Repo-rule compliance

- Review-only: the product candidate and its files were not modified; the remote head remained `fd3dd0c2c2d747a21545e518e7c8f965f0f7f2ea` at final verification.
- No `.github/**` changes, workflow reruns, or workflow dispatches were made.
- This evidence is stored only in the `baseharbor-plan` vault and contains no Markdown checkbox task lines.

END_DONE 0427-132: REQUEST-CHANGES for PR #1453; candidate `fd3dd0c2c2d747a21545e518e7c8f965f0f7f2ea`.
