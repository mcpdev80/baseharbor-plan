# CODEX-REVIEW 0427-172 r3 — PR #1502

ROLLE: REVIEW  
URTEIL: APPROVE  
Kandidat: `4362f4a16f821214774ff4a524efe6a35799d3a3`  
PR: https://github.com/mcpdev80/baseharbor/pull/1502  
PR base: `20902f0a6ab016fd8fe6a501751e1becc5f334dd`  
Live develop at review: `b3a8042d18ea60f162a32a51df34a499cad6a237`  
Hosted run: `42546833737` (`pull_request`, exact candidate head, completed/success)

## PLAN

1. Re-read the prior review recipe and round-3 evidence, then verify live PR, head, base, develop, and changed paths.
2. Trace the TestMain marker claim through trust-plane setup and package teardown; inspect the owner-preservation regression and native logs.
3. Trace injected ExistingFilesForProject failure through orphan adoption and marker-retention assertions.
4. Confirm the exact-head hosted jobs and distinguish passed native tests from skipped jobs.
5. Publish the verdict and a post-merge landing-check recipe to Planning.

## Review against act-1502-review-r2

### Marker root and ownership

The candidate addresses the r2 root mismatch. `runRuntimeIntegrationTestMain` claims the marker using the current process PID before `m.Run()` (`cmd/baha/runtime_integration_test_support_test.go:107-126`). The helper does create a fresh per-run data home rather than literally reusing TestMain's physical directory. It now captures TestMain's marker path, carries the marker bytes to the per-run root, removes the old copy, switches `XDG_DATA_HOME`, records `runtimeIntegrationTrustPlaneDataRoot`, and verifies the marker through `ensureBootstrapLeftoverMarker` (`runtime_integration_test_support_test.go:622-677`, `:605-617`). When no state/XDG root exists, `bootstrapLeftoverMarkerPath` falls back to `deployment.DataRoot()` (`:153-169`). TestMain teardown removes the marker from the tracked root (`:117-135`).

`TestBootstrapMarkerSurvivesDataRootSwitch` checks that the original PID is preserved, the initial marker is gone, and the marker is readable under the new root (`cmd/baha/runtime_integration_cleanup_coverage_test.go:1246-1304`). The actual trust-plane setup path was also exercised in the exact-head native Docker and Podman jobs: `TestSecondSameHostCoreNativeConflictInCI` passed in Docker job `128933577055` and Podman job `128933577080`. Their logs show the bootstrap setup completing and the second target being refused without a second Core. The marker-root issue from r2 is resolved.

### Deterministic runtime-file permission failure and adoption denial

`runtimeBootstrapOrphanFileReadErr` provides the deterministic injected failure (`runtime_integration_test_support_test.go:288-296`). The production orphan-footprint check calls `bootstrapOrphanReadRuntimeFiles` (`:466-500`), whose normal path calls `bhruntime.ExistingFilesForProject` and whose test seam can inject `os.ErrPermission` (`:519-528`). Only `os.ErrNotExist` is treated as proof that runtime files are absent; other read errors propagate as unverifiable (`:478-516`). The adoption path turns that error into a failure and does not consume the marker (`:424-437` and the adoption error handling immediately following).

`TestBootstrapAdoptionFailsClosedOnRuntimeFilePermissionError` sets the seam to `os.ErrPermission`, uses a target with no owned projects so engine inventory cannot mask the read failure, asserts adoption returns an error, and asserts the marker remains (`runtime_integration_cleanup_coverage_test.go:1306-1357`). This closes the r2 test gap with a deterministic denial assertion.

### Exact-head CI and native coverage

Live PR API identifies head `4362f4a16f821214774ff4a524efe6a35799d3a3`, base `20902f0a6ab016fd8fe6a501751e1becc5f334dd`, open and mergeable. Fetching `refs/pull/1502/head` produced that same commit. The diff from the PR base contains only:

- `cmd/baha/runtime_integration_cleanup_coverage_test.go`
- `cmd/baha/runtime_integration_test_support_test.go`

No `.github/**` changes. The exact-head run `42546833737` completed successfully. `PR · Validation · cli-package-tests` job `128933579320` passed on the `pull_request` trigger and covers the `cmd/baha` package, including the marker-transfer and injected-permission regressions. Native destroy-retry Docker job `128933577055` and Podman job `128933577080` both passed; each log explicitly records `TestSecondSameHostCoreNativeConflictInCI` PASS.

The distinct `PR · Native Keycloak/Core` job `128933581031` was skipped. I do not count that job as a pass. This does not invalidate the requested r3 marker-root review: the applicable native Docker/Podman destroy-retry jobs executed and passed. The card's F3 healing proof is a separate post-merge develop-push obligation below.

The PR base remains `20902f0a6ab016fd8fe6a501751e1becc5f334dd`, while current develop is `b3a8042d18ea60f162a32a51df34a499cad6a237`; current develop is not an ancestor of this candidate. Keep the exact reviewed SHA and ordinary merge/base integration gates in view at landing; any new candidate SHA requires its own applicable checks.

## F3 post-merge healing proof and landing recipe

The post-merge develop run was not available at review time because PR #1502 is still open. Per the task instruction, that is an owner-dependent landing check, not a reason to withhold this source review's approval.

After the owner lands the approved candidate through the normal merge path:

1. Record the exact merge commit and fresh `git ls-remote` develop head.
2. Observe the normal develop-push run through terminal completion; do not dispatch or rerun it from this review.
3. In both native Docker and Podman jobs, verify that `TestUpNameResumesThroughCommandEntrypoint` and `TestControlPlaneSingleDefaultNativeRuntimeInCI` actually executed and passed. A skipped test is not healing evidence.
4. Record run/job IDs and the relevant test log lines in the card evidence. If either test is skipped, absent, or fails, keep F3 open and do not mark the card's healing proof complete.

## Verdict

**APPROVE** for candidate `4362f4a16f821214774ff4a524efe6a35799d3a3`. The marker is carried with the original process owner into the tracked trust-plane data root, the teardown reads/removes that tracked claim, the permission injection reaches the actual ExistingFilesForProject seam and adoption refuses while preserving the marker, and the applicable exact-head Docker/Podman native checks passed. The post-merge develop run remains an explicit landing check owned by the landing sequence, as requested; it is not represented as already complete.

This was a read-only product review. No product files, PR state, branches, or workflows were changed; no local tests or containers were started.

Planning validation: after refreshing Planning `origin/main`, `python3 scripts/plan.py check` passed with 435 tasks, 0 errors, and 4 dependency warnings. An earlier run before that refresh failed in existing task-link metadata (`ValueError: not enough values to unpack (expected 2, got 1)` at `scripts/plan.py:650`); no task metadata was changed for this review. `git diff --check` passes, and this evidence file contains no checkbox syntax.

END_DONE 0427-172-review-r3: APPROVE — candidate `4362f4a16f821214774ff4a524efe6a35799d3a3`; plan evidence to publish on origin/main.
