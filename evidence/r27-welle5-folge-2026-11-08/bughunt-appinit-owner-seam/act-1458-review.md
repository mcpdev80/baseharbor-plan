# CODEX-REVIEW 0427-136 — PR #1458

## PLAN

1. Verify the live candidate head, develop base, ancestry, and exact file diff.
2. Check that the test-only bootstrap follows route B and leaves #1347 enforcement and `core_required` semantics unchanged.
3. Evaluate whether the seam-level unit witness is sufficient for the card's native documented-bootstrap acceptance.
4. Verify the exact hosted PR run and the Owner routing blocker for the native acceptance cell.
5. Publish the SHA-specific verdict, owner-action recipe, tests, and stop criterion in the Planning Vault.

## Verdict

**ROLE: REVIEW**  
**URTEIL: KORREKTUR (REQUEST-CHANGES)**  
**PR #1458 head:** `7536878d4b9358446730861766a6e76be7e7e494`  
**develop base:** `07ae6c3e91b081a189266ca4b162ba705d4aa78f`  
**Hosted PR run:** `42461172453`, terminal success on the exact candidate

The source change follows the Owner's route B: it changes only the native acceptance test, boots a genuine Core before the owner seam, and does not alter production enforcement. However, the acceptance clause requires the documented bootstrap path to pass in the native acceptance cell. That test was not executed on this candidate; the PR run skipped `validate`, and the existing impact selector excludes this test-only diff. The seam unit witness is useful but does not substitute for that native acceptance result.

### 1. SHA-exact diff and enforcement boundary: PASS

Remote refs identify `develop` `07ae6c3e91b081a189266ca4b162ba705d4aa78f` and PR #1458 head `7536878d4b9358446730861766a6e76be7e7e494`. `git merge-base --is-ancestor 07ae6c3e91b081a189266ca4b162ba705d4aa78f 7536878d4b9358446730861766a6e76be7e7e494` returned exit 0; GitHub reports the PR open and mergeable.

The full diff against develop is one file only: `cmd/baha/installation_destroy_native_test.go`, with 11 added lines. It invokes `runWithIO(ctx, []string{"up", "--control-plane-only", "--yes"}, ...)` after creating the fresh `--reference local` target and before application initialization. No production file, `internal/deployment` owner check, consent implementation, or workflow is changed. Thus the #1347 owner enforcement and the `core_required`/explicit-consent semantics remain untouched in this candidate.

### 2. The seam unit witness does not satisfy the native acceptance clause

The round-1 evidence says a seam unit test observes `VerifyDeploymentOwner` succeed once a real `installation.json` exists, including a mid-bootstrap state. That confirms the owner predicate accepts an established Core installation. It does not execute the changed acceptance sequence (`target create --reference local` → real `baha up --control-plane-only` → `baha app init --quick`) or prove the destroy/retry lifecycle that follows. The full native acceptance could not be completed on the shared host, so no local full-path witness is available.

The exact PR run `42461172453` is successful overall, but its `validate` job was skipped. The native Docker/Podman `single_default_native` acceptance workflow is not present in the run; the PR's `PR · Native Keycloak/Core` check is also skipped and is not this lifecycle test. The only relevant hosted pass is `PR · Validation · cli-package-tests`, which runs the package without `BASEHARBOR_INSTALLATION_DESTROY_ACCEPTANCE=1`; it does not run the changed native acceptance body. Therefore there is no hosted native-bootstrap result on this exact SHA.

**Fix recipe:** Keep route B and the one-file production/test boundary. The Owner must route `cmd/baha/installation_destroy_native_test.go` to the existing `single_default_native` gate (or an equivalent required native gate) so this test-only change selects the gate. `scripts/ci-single-default-impact.sh:7` currently selects runtime and production paths but not this test file; the required Owner change is to add an explicit impact rule for this acceptance test or an equivalent narrowly scoped marker. The workflow owner must ensure the test runs with `BASEHARBOR_INSTALLATION_DESTROY_ACCEPTANCE=1` on the intended hosted Docker/Podman runner. Then observe the changed test pass on the exact candidate SHA. No workflow or selector file was edited or dispatched by this review.

### 3. Owner routing blocker and hosted result

The evidence accurately identifies the gap: `scripts/ci-single-default-impact.sh:7` has no match for `cmd/baha/installation_destroy_native_test.go`, so the test-only candidate leaves `required=false`; the native acceptance workflow's `single_default_native` job is therefore not selected on the relevant develop push. This is an Owner-side CI-selection blocker, not a reason to infer a pass from unit coverage. The pull-request run's `validate` job and native acceptance gate were skipped, so it does not close that blocker.

`gh run view 42461172453` returned `headSha=7536878d4b9358446730861766a6e76be7e7e494`, `event=pull_request`, `status=completed`, `conclusion=success`. `PR · Validation · cli-package-tests`, CLI build/gofmt/vet/source-contracts, `PR Selected Checks`, source format, focused Python, workflow policy, and trusted plan passed. `validate`, Targeted HA Docker/Podman, and `PR · Native Keycloak/Core` were skipped. The hosted run is green for the checks it selected, but it contains no result for the acceptance test modified by this PR.

## Evidence and candidate witnesses

- `git ls-remote origin refs/heads/develop refs/pull/1458/head` returned `07ae6c3e91b081a189266ca4b162ba705d4aa78f refs/heads/develop` and `7536878d4b9358446730861766a6e76be7e7e494 refs/pull/1458/head`.
- `gh pr view 1458` reports OPEN, base `develop`, `mergeable=MERGEABLE`, `mergeStateStatus=CLEAN`.
- `git merge-base --is-ancestor 07ae6c3e91b081a189266ca4b162ba705d4aa78f 7536878d4b9358446730861766a6e76be7e7e494` returned exit 0.
- `git diff --name-status origin/develop...refs/remotes/origin/pr-1458` lists only `M cmd/baha/installation_destroy_native_test.go`; `git log --oneline origin/develop..refs/remotes/origin/pr-1458` lists only commit `7536878d`.
- Hosted run `42461172453` was terminal success on the exact head. The CLI package test passed, but the acceptance test and native acceptance gate were skipped as detailed above.
- Review-only: no product files changed, no local tests or runtime operations were run, no workflow/selector was edited, and no CI rerun or dispatch was triggered.

## Stop criterion

Do not approve until the documented Core bootstrap plus application-init/destroy-retry acceptance executes and passes in the native hosted acceptance gate on the exact candidate SHA, with the Owner routing change making the test-only diff select that gate. Preserve #1347 owner enforcement and `core_required` semantics. A seam unit test and green package checks with the native test skipped are insufficient.

## END

END_BLOCKED 0427-136-review — KORREKTUR required; PR #1458 head `7536878d4b9358446730861766a6e76be7e7e494`, native acceptance not selected.
