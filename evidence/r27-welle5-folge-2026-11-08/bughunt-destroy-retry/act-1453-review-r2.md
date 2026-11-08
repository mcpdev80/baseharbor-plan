# CODEX-REVIEW 0427-132 r2 — PR #1453

## PLAN

1. Compare the published round-2 correction with the r1 findings and stop criterion.
2. Verify the exact PR head, current develop head, merge base, and changed-file set from GitHub.
3. Inspect the production branch logic, regression cases, and the hosted run records for the exact candidate.
4. Record the verdict and a concrete correction/evidence recipe in this Planning evidence file.
5. Commit and publish this review to baseharbor-plan origin/main, then verify the remote evidence path.

## Candidate and provenance

- Repository: `mcpdev80/baseharbor`, PR #1453.
- Candidate head: `7557a0b1d088ee8bcb0df2a82a230b5c17f51530`, verified with `gh pr view`, `git ls-remote refs/pull/1453/head`, and `git rev-parse origin/pr/1453` in a fresh clone under `/tmp/opencode/0427-132-r2-review-wt`.
- PR base branch: `develop`. Current `develop` head is `07ae6c3e91b081a189266ca4b162ba705d4aa78f`; PR merge base is `e39b0004346cdfd082e34ba55d94d24757bbbd27`. Candidate ancestry from the current `develop` head is false because #1430 advanced the base after this candidate was cut. GitHub currently reports `MERGEABLE` and `CLEAN`; #1430 does not touch this change's `cmd/baha` files.
- Diff against the merge base: exactly `cmd/baha/runtime_destroy_all.go`, `cmd/baha/runtime_destroy_local_owner_stat.go`, and `cmd/baha/installation_destroy_local_orphan_scope_test.go`. No `.github/**` changes.
- The Planning repository used for this evidence is `/tmp/opencode/0427-132-r2-plan-wt`; `git remote -v` reports `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push. Base before this review commit: `0f6ebdd83ef98bdbe3e4b623800934e66c2ae4ad`.

## Review of the r1 correction

The code delta closes the r1 fail-open branch. In `discoverFullDestroyTargets()` at `cmd/baha/runtime_destroy_all.go`, a present runtime-owner path remains blocking; `errors.Is(statErr, os.ErrNotExist)` is the only path treated as a missing owner and remains nonblocking; every other lookup error now remains blocking and records that ownership could not be verified. The code does not guess a provider or restore the legacy `compose` inference.

The new tests cover deployment-only state, a present local runtime owner, injected non-ENOENT failure, and injected ENOENT. The pre-existing `TestMissingLocalTargetRegistrationNeverInventsComposeDestroyAuthority` remains in the selected package suite. The exact-head hosted `go-unit-tests` job passed in run `42448230775`; `PR Selected Checks`, build, vet, source-format, and CLI gofmt also passed. The run's head SHA is the reviewed candidate.

Static inspection confirms the native acceptance test is explicitly gated at `cmd/baha/installation_destroy_native_test.go:20-22` by `BASEHARBOR_INSTALLATION_DESTROY_ACCEPTANCE=1`. The recorded PR run did not set up the required runtime acceptance: `Targeted HA · docker` and `Targeted HA · podman` are both `skipped`. `gh run list --commit 7557a0b1d088ee8bcb0df2a82a230b5c17f51530` returns only run `42448230775`; no exact-head Docker/Podman dispatch or native acceptance job is present.

This conflicts with the round-2 note's description of a native PASS witness. Its own `### Named native retry test in hosted CI` section says no hosted pass exists for this exact head and that the native jobs are skipped on PR pushes. A pass on the older develop baseline or a local run does not satisfy the prior r1 stop criterion for exact-candidate native acceptance.

## Verdict: REQUEST-CHANGES

The production fix and unit coverage satisfy the code portion of the r1 review. The acceptance evidence remains incomplete because the named native retry test has no verified exact-head Docker/Podman PASS. I therefore do not approve this candidate yet.

## Correction and evidence recipe

- Owner action: provide the exact-head native acceptance for `7557a0b1d088ee8bcb0df2a82a230b5c17f51530` through the existing authorized Docker and Podman acceptance paths. The workflow guards are in `.github/workflows/docker-runtime-acceptance.yml:108` and `.github/workflows/podman-acceptance.yml:110`; workflow files remain Owner-owned and were not changed or dispatched by this review.
- Evidence update: add the workflow run IDs, exact head SHA, selected job names, and test event showing `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` passed for the required runtime(s) to `round-2.md`. The exact-head `go-unit-tests` pass from run `42448230775` remains valid.
- Test requirement: the named native retry test must execute under `BASEHARBOR_INSTALLATION_DESTROY_ACCEPTANCE=1` with the explicit Docker or Podman runtime and report PASS; skipped jobs and package-level success do not satisfy this criterion.
- Stop criterion: keep this review at REQUEST-CHANGES until the exact-head native acceptance is observed and durably recorded. Recheck PR head, current develop, mergeability, and required checks before any later approval.

## Repo-rule compliance

- Review-only. The product candidate was not modified, no test was launched, and no workflow was edited or dispatched.
- The review evidence is stored only in `baseharbor-plan/evidence/r27-welle5-folge-2026-11-08/bughunt-destroy-retry/act-1453-review-r2.md`.
- No Markdown checkbox task lines are present in this evidence file.

END_DONE 0427-132-review-r2: REQUEST-CHANGES for PR #1453 head 7557a0b1d088ee8bcb0df2a82a230b5c17f51530; native exact-head acceptance remains unobserved.
