ROLLE: REVIEW

Session ID: not exposed by this interface. Model: GPT-6 (Codex). Backend: Codex API. Review time: 2026-11-21 08:02 UTC.

**Verdict: REQUEST CHANGES**

## PLAN

1. Read /var/tmp/rev1738b.txt; record the numbered plan in this evidence file and the live board.
2. Resolve GitHub remotes, then verify PR #1738 head a8079303, base e45430f2, refs, ancestry, and before/after freeze.
3. Read card 0428-214 and the cited lane evidence; inspect the SHA-exact one-file diff and destruction authorization path.
4. Assess the positive installationApplicationScope path, negative impact-confirmation-required path, and unchanged teardown stamp.
5. Inspect exact-head per-job CI logs and same-base comparison; classify red cells without calling the failed aggregate green.
6. Check prohibited paths and cleanliness; write verdict and recipes, publish only this evidence file, and verify remote publication.

## Candidate and base

- Card: t-20261121-destroy-authority-stamp (0428-214), release v0.4.28.
- Candidate: mcpdev80/baseharbor PR #1738, branch lane-0428-214-destroystamp, open and draft=false.
- PR head before review: a8079303acaaba860ae444eec684ff9625551f82.
- PR base branch and base SHA: lane-0428-198-cli-shard-operator-env at e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4.
- PR head after review: a8079303acaaba860ae444eec684ff9625551f82.
- Product remote from the first Git action, `git -C workers/baseharbor remote -v`: origin git@github.com:mcpdev80/baseharbor.git (fetch/push).
- Planning remote, verified before writing evidence: origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push).
- Remote refs before review: e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4 refs/heads/lane-0428-198-cli-shard-operator-env; a8079303acaaba860ae444eec684ff9625551f82 refs/heads/lane-0428-214-destroystamp; a8079303acaaba860ae444eec684ff9625551f82 refs/pull/1738/head. The PR API reports the same head and base.
- SHA-exact comparison against the current base e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4 reports one changed path: cmd/baha/core_installation_runtime_test.go (72 additions, 0 deletions). No other card or protected paths are in this diff.
- Important ancestry detail: GitHub compare e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4...a8079303acaaba860ae444eec684ff9625551f82 reports common ancestor 7546b1806aac9a0055a647e20f2843564eb3c1ce, ahead_by=2, behind_by=9, status=diverged. Thus the candidate content is only the one owned file, but its branch is still based on the older 7546 SHA rather than descending from current base e454. The current PR merge ref is 8b0ab6f29c6df9ffd14cad359f9c6e135cf50372 with parents e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4 and a8079303acaaba860ae444eec684ff9625551f82. The run's Trusted Plan succeeded, but that does not change the branch ancestry result.
- No candidate files, refs, workflows, or PR metadata were changed during review.

## Contract review

The current owner instruction for this review defines the acceptance: `TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope` must show a positive path through the destruction planner's installationApplicationScope seam, a negative no-consent result with `impact-confirmation-required`, and must leave the synthetic teardown stamp unchanged. The owner clarified that installation.destroy is not a LocalWorkloadOperation and this card does not need a local-runtime-grant branch. I applied that current scope ruling while noting that the planning card's older text still describes the earlier operator-auth objective.

1. Positive scope path: PARTIALLY MET. The new test at cmd/baha/core_installation_runtime_test.go:368-386 builds an aggregate destruction plan, checks its destructive application-deployment child, creates consent, obtains an installationApplicationScope proof, and calls authorizeApplicationDestruction. The current production path at cmd/baha/installation_application_scopes.go:20-41 validates the installation.destroy parent consent and records matching child plan IDs; cmd/baha/application_destroy_authorization.go:28-38 selects operation `installation.destroy` for a matching proof. The test traverses these functions. However, its positive assertion only checks `authorizeApplicationDestruction` returned no error; it discards the returned plan and does not inspect the authorization decision. Since the fixture manifest is `dev` and the operator-auth library allows a trusted-local dev operation, the test does not pin that the selected operation was specifically `installation.destroy`. A future regression that falls back to ordinary `destroy` could stay green.
2. Negative no-consent path: PASS. A fresh fixture is used; `withInstallationApplicationScopes` is called without consent; the test requires a machine.Error with CauseCode `impact-confirmation-required` at lines 391-405. This guard returns before the child destruction authorization or runtime cleanup call.
3. Teardown stamp: PASS as scoped by the owner. The existing synthetic principal and membership construction in `coreBootstrapFixtureCleanupContext` at lines 294-306 are unchanged by the SHA-exact diff. The added scope-proof test uses `retainedNativeBackendFixture` and does not consume that synthetic stamp. The older test still has its existing fixture-auth assertions; the owner explicitly ruled that this card should preserve the stamp and prove the destruction-planner scope instead.
4. Write-set: PASS. The diff changes only cmd/baha/core_installation_runtime_test.go. It does not touch .github/**, scripts/**, internal/operatorauth/**, internal/identityprovider/**, internal/serviceaccess/**, internal/capability/perses_selection.go, internal/observability/registry.go, or the named owner-stack paths.

## Hosted CI

Exact-head hosted run 44878737065 (`CI · PR #1738`) completed at 2026-11-21T07:12:20Z with failure. `PR · Trusted Plan` (136769129076), `PR · Native gate plan` (136769128922), source format, cli-gofmt, cli-build, cli-vet, source-contracts, Focused Python, and Go unit cli-1/cli-2/cli-3 succeeded. `PR Selected Checks` job 136770316121 failed. The new test name hashes to cli-2 in scripts/pr-go-unit-shard.py's SHA-256 four-way selector; that exact job 136769169443 reports `PASS cli-2: 435 passed / 19 intentionally skipped / 454 discovered`. The shard runner validates that every selected discovered test was executed and passed before printing this receipt.

There are 19 skipped check runs in the exact-head check-run inventory. These are path-filtered or release-only cells (including Draft/release source, consumer pins, runner interface, Public Contracts, Targeted HA, and main release); the relevant cli-2 shard and Native Keycloak/Core docker/podman jobs were executed. `PR · Selected Runtime` was skipped by its selection gate. The planner and Trusted Plan did not fail or suppress the relevant fan-out.

Per-job failure classification, using the same-base hosted run 44867737078 on exact base SHA e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4:

- Candidate cli-0 job 136769169547 failed `TestAppListAllTargetsWorksAfterInstallationDestroy`: `app_list_all_targets_test.go:26: all-targets inventory depended on deleted Target config "docker-dev": BaseHarbor config root is configured but the config.yaml is missing`. Baseline cli-0 job 136735244280 contains the same test and same failure. This is inherited, card 0428-210 / PR #1739; it is not introduced by this one-file diff.
- Candidate Native Keycloak/Core docker job 136769169438 and podman job 136769169441 both failed `TestControlPlaneSingleDefaultNativeRuntimeInCI`: `control_plane_single_native_ci_test.go:30: prepare BaseHarbor integration trust plane: target "..." is not configured`. The same test and same file:line fail in the same-base baseline docker job 136735244241 and podman job 136735244263. These are inherited base failures, not evidence of a defect in the new test.
- The candidate run did not schedule `PR · Go unit · packages`. The same-base baseline packages job 136735244287 did fail the three `TestPersesLokiDatasourceMultiSource*` tests, including missing `providers/loki/shared/service-access/pki/client-cert.pem` at loki_test.go:522 and :586, and `loki_test.go:633: expected 2 per-source queries even on full miss, got 0`. Those are the owner-stack #1615 failures described in the mission; they are not candidate failures because no packages job ran for this candidate.
- Thus the three executed red jobs on the candidate have corresponding same-base failures. This justifies classifying their test failures as inherited, but `PR Selected Checks` remains failure and is not a pass.

Log protocol byte counts:

- Candidate run 44878737065: `gh run view --log` returned 903,295 bytes; `gh run view --log-failed` returned 8,855 bytes. Per-job `gh run view --job 136769169547 --log` returned 46,015 bytes for cli-0; `--job 136769169443 --log` returned 44,208 bytes for cli-2; native docker and podman `gh run view --job ... --log` returned 0 bytes each. Their GitHub Actions per-job log API bodies were 49,614 bytes (docker) and 37,759 bytes (podman), and exposed the target-not-configured lines above.
- Same-base run 44867737078: `gh run view --log` and `--log-failed` each returned 0 bytes. Per-job `gh run view --job ... --log` returned 0 bytes for the queried cli-0, packages, docker, podman, and cli-2 jobs. Per-job GitHub Actions log API bodies were 23,040 bytes for cli-0, 34,610 bytes for packages, 49,123 bytes for docker, and 37,809 bytes for podman. All failure counts above came from those individual per-job logs, not the incomplete aggregate output.

## Findings and recipes

Finding 1 — the positive test does not assert the selected destruction operation.

- File: cmd/baha/core_installation_runtime_test.go:378-386.
- Change: in the new scope-proof test, run the positive context with operatorauth enforcement state enabled without adding a principal or changing the synthetic teardown fixture; retain the returned destruction plan and inspect `operatorauth.AuthorizationDecisionFromContext(ctx)`. Require `Allowed` and `Operation == "installation.destroy"`.
- Test requirement: the positive case must pass only when the installation scope selects `installation.destroy`; a mutation that removes or changes the planner's operation assignment must make the test fail. Keep the existing no-consent assertion on `impact-confirmation-required` and the old teardown stamp unchanged.
- Stop criterion: the positive test observes the exact operation and allowed decision through the production planner, the negative test remains fail-closed, and cli-2 executes the regression successfully.

Finding 2 — PR head is not based on the current base head.

- State: the owner-confirmed base is e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4. The current head's merge-base is 7546b1806aac9a0055a647e20f2843564eb3c1ce; compare reports 9 commits behind the current base. The card diff is one file, but the candidate branch still carries the stale base ancestry.
- Change: rebase the existing lane-0428-214-destroystamp candidate onto current base e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4; do not create a second branch. Preserve the one-file card diff and the unchanged synthetic teardown stamp.
- Test requirement: after rebase, verify base ancestry and the exact name-only diff, then observe a new terminal hosted `PR Selected Checks` result for the new head.
- Stop criterion: stop when e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4 is an ancestor of the candidate, the diff remains only cmd/baha/core_installation_runtime_test.go, and the required aggregate is successful.

Finding 3 — the exact-head required aggregate is red for inherited failures.

- State: run 44878737065 `PR Selected Checks` failed because cli-0 and Native Keycloak/Core docker/podman are red. The failure test names and relevant file:line evidence are the same on run 44867737078 at the exact base. The candidate did not execute the packages job; its baseline packages failure is separately recorded as owner-stack evidence.
- Change: do not modify unrelated tests in this card. Resolve the cli-0 and native-core base failures through their owning work, and retain the same-base per-job log comparison.
- Test requirement: the updated candidate must run required cli-2 and selected native/CLI jobs; inspect each per-job log and require terminal `PR Selected Checks` success on the final rebased head.
- Stop criterion: do not accept while the required aggregate is failure, skipped, or queued. Inherited classification explains ownership only; it does not turn the failed aggregate green.

## Cleanliness

- Before review: PID 3890629; `docker ps -a` returned only the header and no containers.
- After review: PID 3934972; `docker ps -a` returned only the header and no containers.
- No Docker or Podman state was created or modified.

## Review limits

Read-only review. No local tests were run; no workflow was changed or dispatched; no PR comment, merge, force-push, close, or candidate mutation was performed. The current task file retains older operator-auth acceptance wording; this review applies the current owner clarification in the mission as its controlling scope.

END codex-rev-cli2b DONE — candidate SHA a8079303acaaba860ae444eec684ff9625551f82.

## origin/main publication witness

After fetching origin main, `git ls-tree -r --name-only origin/main | grep '^evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-2.md$'` returned exactly:

```text
evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-2.md
```
