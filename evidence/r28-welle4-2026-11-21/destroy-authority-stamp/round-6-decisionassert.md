# round-6-decisionassert — 0428-214 / PR #1738 / lane-0428-214-destroystamp

ROLLE: WORKER · KARTE: t-20261121-destroy-authority-stamp (0428-214) · RELEASE: v0.4.28
MISSION: coordinator/missions/0428-214-r5-bothdirections.md
REVIEW: evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-2.md (Verdict: REQUEST CHANGES)

## PLAN

1. Read mission, review-2, card; resolve github remote; cut worktree lane-0428-214-destroystamp, set identity 0428-214-scopeop.
2. Rebase candidate onto TRUE base e45430f2 (merge-base was 7546b1806, 9 commits behind); squash to 1 own commit; verify 4 base witnesses.
3. Inspect production destroy path (application_destroy_authorization.go:29-37, secret_operations.go, mcp.go authorizeMCPOperation, internal/operatorauth/authorization.go) to scope Finding 1 against AuthorizationDecisionFromContext.
4. Mutation (Finding 1): in TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope positive path, drive the production operator-auth boundary for the managed scope and assert decision.Allowed AND decision.Operation == "installation.destroy"; proven fail-closed (mutation to "destroy" turns the test red).
5. Symptom test BEFORE push (both directions pass); fail-closed mutation proven red; production file restored, git diff clean.
6. Push branch force-with-lease; gh pr view 1738 draft=false; prove delivery via GitHub API; ci-fast-check PASS; wait for terminal PR Selected Checks.
7. Write this akte, publish to baseharbor-plan origin/main, post END_DONE with plan-sha.

## Candidate and base

- Card: t-20261121-destroy-authority-stamp (0428-214), release v0.4.28.
- Candidate: mcpdev80/baseharbor PR #1738, branch lane-0428-214-destroystamp, open and draft=false.
- Head after this round: 7e6792939c552f89c66a53958c8eb7bcd255a1b3.
- Base branch and exact base SHA (attested before cut): lane-0428-198-cli-shard-operator-env @ e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4.
- Product remote from the first Git action, `git -C baseharbor remote -v`: lane-origin https://github.com/mcpdev80/baseharbor.git (fetch/push); origin and upstream resolve to the same github.com/mcpdev80 URL. Only lane-origin was pushed/fetched.
- Planning remote verified before first evidence commit: origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push).

## Base witnesses (Finding 2 of review-2 resolved)

- Remote head of base (git ls-remote lane-origin refs/heads/lane-0428-198-cli-shard-operator-env): e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4.
- Remote head of candidate (git ls-remote lane-origin refs/heads/lane-0428-214-destroystamp): 7e6792939c552f89c66a53958c8eb7bcd255a1b3.
- Pre-rebase ancestry (git merge-base --is-ancestor e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4 a8079303acaaba860ae444eec684ff9625551f82): NO. merge-base was 7546b1806aac9a0055a647e20f2843564eb3c1ce, 9 commits behind the true base — exactly the drift review-2 row 874 recorded.
- Rebase command run from the worktree: `git rebase --onto e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4 7546b1806aac9a0055a647e20f2843564eb3c1ce` (9 commits of true base carried, no foreign branch cut).
- Post-rebase witnesses:
  - `git merge-base --is-ancestor e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4 HEAD` = 0 (PASS, e454 is an ancestor of head 7e6792939).
  - `git rev-list --count e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4..HEAD` = 1 (exactly one own commit, squashed from the two prior round-5 commits).
  - `git diff --name-only e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4..HEAD` = `cmd/baha/core_installation_runtime_test.go` (only the allowed file).
  - `git log -1 --format=%an` = `0428-214-scopeop` (identity corrected from the prior `devtest` push).
  - `git log --oneline e45430f2..HEAD` lists only the single own commit 7e6792939.

## Contract review (Finding 1 resolved)

1. Positive scope path now asserts the selected destruction operation. The new test TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope (cmd/baha/core_installation_runtime_test.go:368-401) builds the aggregate destruction plan, keeps the destructive application-deployment child scope, confirms the scope, and now calls authorizeApplicationDestruction while carrying a verified operator principal and editor membership on the context. It then drives the same production operator-auth boundary the real destroy path runs (ensureOperatorAuthForBoundary(ctx, r.Target.Name, "prod")) and reads operatorauth.AuthorizationDecisionFromContext(ctx), requiring Allowed == true AND Operation == "installation.destroy". This pins the exact operation through the production planner seam.
   - Rationale for the boundary + managed scope: in a direct fixture unit test a dev/local target without a verified principal never reaches a populated operator-auth decision (probe-verified: ensureOperatorAuthForBoundary returns nil for dev/local and leaves the decision empty). The line-332 cleanup-context test in the same file uses the identical mechanism (WithVerifiedPrincipal + WithMembershipProvider + ensureOperatorAuthForBoundary for "prod"), so this is the established, in-repo pattern for populating the decision.
   - The planner selects operation "installation.destroy" ONLY when the confirmed installationApplicationScope proof is present (cmd/baha/application_destroy_authorization.go:29-37 falls back to ordinary "destroy" otherwise); the assertion therefore fails closed if that assignment is removed.
2. Negative no-consent path unchanged: a fresh fixture is used; withInstallationApplicationScopes is called without consent; the test requires a machine.Error with CauseCode impact-confirmation-required at core_installation_runtime_test.go:416-430. This guard returns before the child destruction authorization or runtime cleanup call.
3. Teardown stamp unchanged: the synthetic teardown principal and membership construction in coreBootstrapFixtureCleanupContext (core_installation_runtime_test.go:294-306) is untouched by this round's diff; the added scope-proof test uses retainedNativeBackendFixture and does not consume that synthetic stamp.
4. Write-set: PASS. The diff changes only cmd/baha/core_installation_runtime_test.go. It does not touch .github/**, scripts/**, internal/operatorauth/**, internal/identityprovider/**, internal/serviceaccess/**, internal/capability/perses_selection.go, internal/observability/registry.go, or the named owner-stack paths.

## Fail-closed mutation (Finding 1 proof)

- Mutation applied: `cmd/baha/application_destroy_authorization.go:36` changed `operation = "installation.destroy"` to `operation = "destroy"`.
- Result with the mutation: `go test ./cmd/baha/ -run 'TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope'` → FAIL, `core_installation_runtime_test.go:412: installation.destroy was not admitted as operation installation.destroy through the destruction-planner seam: allowed=true operation="destroy"`. The test turns red exactly when the planner's operation assignment is removed, as required.
- Production file restored to its original content (`operation = "installation.destroy"` at :36); `git diff --name-only` after restore lists only the test file. No production file was changed in the delivered candidate.

## Symptom test BEFORE push (both directions)

- Command (safe skip form, per TEST RUNNER RULE): `go test ./cmd/baha/ -count=1 -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication' -run 'TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope'`
- Result: PASS, positive log `confirmed installation.destroy scope selected and admitted as operation installation.destroy through the destruction-planner seam`; negative log `missing consent rejected with impact-confirmation-required`.
- Full relevant suite (both directions plus shared cleanup boundary): `go test ./cmd/baha/ -run 'TestCoreBootstrap|TestInstallationApplicationScope|TestApplicationDestroy'` → ok (6.09s). `go vet ./cmd/baha/` → clean; `go build ./...` → clean.

## Hosted CI (Finding 3 of review-2, same-base per-job comparison)

- Candidate run for head 7e6792939c552f89c66a53958c8eb7bcd255a1b3: run 44886762103 (`CI · PR #1738`), terminal conclusion failure.
- Per-job terminal results for run 44886762103:
  - `PR · Go unit · cli-2` (job 136793740203): SUCCESS, receipt `PASS cli-2: 435 passed / 19 intentionally skipped / 454 discovered; CLI inventory total=1784`. The card test TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope executes in this shard and passes (discovered count 453 -> 454 vs the base, exactly the one new test).
  - `PR Selected Checks` aggregate 136794984777: failure.
  - `PR · Go unit · cli-0` (job 136793740193): failure, per-job log 23033 bytes, failing line `app_list_all_targets_test.go:26: all-targets inventory depended on deleted Target config "docker-dev": BaseHarbor config root is configured but the config.yaml is missing: /tmp/TestAppListAllTargetsWorksAfterInstallationDestroy3763447568/001/config/config.yaml`.
- Same-base baseline run 44867737078 at exact base SHA e45430f2f1b7 (the same-base comparison review-2 relied on):
  - `PR · Go unit · cli-0` (job 136735244280) FAILS with the identical line `app_list_all_targets_test.go:26: all-targets inventory depended on deleted Target config "docker-dev": ...config/config.yaml` (baseline job log 23040 bytes).
  - `PR · Go unit · cli-2` (job 136735244295) PASS, receipt `PASS cli-2: 434 passed / 19 intentionally skipped / 453 discovered`.
- Inheritance classification: the candidate cli-0 failure is byte-identical to the same-base baseline cli-0 failure (same file:line, same message). This is inherited from 0428-210 / PR #1739 (target-config removal), not introduced by the one-file card diff. The native Keycloak/Core docker and podman cells are 0428-215 / PR #1745 (foreign write-set). Neither the candidate's native cells nor the candidate packages job ran; the inherited classification stands on the identical cli-0 line.
- Aggregate verdict: `PR Selected Checks` remains FAILURE and is NOT booked as a pass. Success is required only for the exact tested head with actually executed required jobs; the candidate head 7e6792939 is a verified descendant of the exact base e45430f2, so no new run on a newer base is required. The red aggregate is owned outside this card's write-set and resolves through #1739 and #1745.

## repo-rule compliance

- Write-set: only cmd/baha/core_installation_runtime_test.go changed in the candidate. No production code, no internal/operatorauth/** (Owner rail), no .github/**, no scripts/**, none of the named owner-stack paths (#1615/#1625/#1623, #1650/#1606, #1614, #1731, #1704). Fail-closed mutation to application_destroy_authorization.go was reverted before the push; git diff --name-only after restore lists only the test file.
- One integration candidate per chain: working only on lane-0428-214-destroystamp; no second branch invented. A stale 0428-214-stampfix-wt worktree from a prior lane was removed before cutting this round's worktree.
- Branch provenance: base head e45430f2f1b7 attested via git ls-remote before the rebase; git merge-base --is-ancestor e45430f2 7e6792939 = 0; git diff origin base..HEAD --name-only lists only the test file; git log --oneline base..HEAD lists only the single own commit 7e6792939 authored 0428-214-scopeop. No foreign commit carried on top.
- CI policy: ci-fast-check.sh ran clean (Source readability, workflow policy 20 approved files, Go unit). Required checks come from the base plan; candidate-added checks (advisory) ran and reported. Required aggregate (PR Selected Checks) is failure and reported as such, not green.
- No subagents, no workflow edits, no workflow_dispatch, no reruns, no merge, no close, no PR comment. END delivered over idle + watcher, not by posting to the coordinator session.

## cleanliness

- No Docker or Podman containers or compose projects were started on this host (the coordinator/codeman server host). The card runs pure Go unit tests only.
- `docker ps -a` before: PID 4011207; returned header only, no containers.
- `docker ps -a` after: PID 4011207; returned header only, no containers.
- `docker volume ls`: no candidate-owned volumes created by this round.
- Worktree cleanup: the lane worktree /home/marcel/dev/baseharbor-ecosystem/0428-214-scopeop-wt holds only the one-file test change; it will be removed at END along with any stray worktree.

## todo §4.4

- Live board file: workers/todos/0428-214-scopeop.json (id 0428-214-scopeop, steps ticked as worked).

END 0428-214-scopeop DONE — candidate SHA 7e6792939c552f89c66a53958c8eb7bcd255a1b3.

## origin/main publication witness

Before committing any evidence, planning remote verified: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v` shows lane-origin https://github.com/mcpdev80/baseharbor.git and planning origin https://github.com/mcpdev80/baseharbor-plan.git.
After fetching origin main, `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep '^evidence/r28-welle4-2026-11-21/destroy-authority-stamp/round-6-decisionassert.md$'` returned exactly:

```text
evidence/r28-welle4-2026-11-21/destroy-authority-stamp/round-6-decisionassert.md
```
