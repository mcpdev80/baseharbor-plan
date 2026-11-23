# PR 1623 review and merge evidence

## PLAN

1. Read the m_rev_1623 mission and capture the task contract, candidate, scope, and acceptance requirements.
2. Refresh authoritative Planning and product remote state, ownership, PR, base, and hosted CI evidence.
3. Review the exact candidate and verify acceptance criteria without exceeding the authorized review/merge scope.
4. Complete the authorized merge if every required gate passes, or document the blocker and actionable recipe.
5. Publish evidence to baseharbor-plan origin/main, synchronize the board, and post final lane status.

## Mission and authoritative task contract

- Mission `/tmp/opencode/m_rev_1623.md.g` assigns ROLE: REVIEW only and expressly says “kein merge durch sie.” It names candidate head `521d76812aa6d87a4f3b48a58347ec21b48c27b0`, exact base/develop `ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb`, and requests scope, hosted test receipts, coreless application-shard state, and source/remote review.
- Planning task `t-20261114-r28-cli2-app-interact` / 0428-063 currently reports `state: wait`; its three declared dependencies are accepted. The recorded blocker still requires positive full pre-release acceptance; task evidence names run `45015912507` as cancelled after 25 failures in cross-card gates. The card’s explicit scope is guided app logs/exec/urls and dedicated tests. It reserves `cmd/baha/commands.go`, shared parser/machine registry, generated indexes, release notes, and `.github/**` for their designated owners. Release `v0.4.28` is active. Read the task note, release note, Owner CLI brief, command map, and code-entry index.
- The mission’s statement that the target candidate has 20 terminal green checks is not true of the live remote state observed below. No workflow was rerun or dispatched, and no local tests were run.

## Remote and candidate witnesses

- Product remotes in the existing `/tmp/opencode/1623-fix-wt` worktree were inspected first. `lane-origin`, `origin`, and `upstream` resolve to `https://github.com/mcpdev80/baseharbor.git`; only the GitHub URL was used for remote truth. The worktree was detached at an older local commit and had no local modifications; it was not used as remote-state evidence.
- Initial and final `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1623/head` snapshots both reported `ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb refs/heads/develop` and `213ca519527b3bfa295c618d0364b221013a6796 refs/pull/1623/head`.
- PR API reports #1623 OPEN, non-draft, branch `lane-0428-063-cli2-app-interact`, base `develop`, current head `213ca519527b3bfa295c618d0364b221013a6796`, mergeable `MERGEABLE`, `mergeStateStatus=BLOCKED`, and no submitted review records. The mission head `521d76812aa6d87a4f3b48a58347ec21b48c27b0` is the parent of a later commit; the requested exact candidate is no longer the PR head.
- GitHub compare from base `ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb` to requested head `521d76812aa6d87a4f3b48a58347ec21b48c27b0` reports merge base equal to that base, 18 ahead, zero behind. The ancestry check `git merge-base --is-ancestor ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb 521d76812aa6d87a4f3b48a58347ec21b48c27b0` succeeded.
- `git diff --name-only ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb...521d76812aa6d87a4f3b48a58347ec21b48c27b0` returned:

```text
cmd/baha/app_access.go
cmd/baha/app_access_urls.go
cmd/baha/app_exec.go
cmd/baha/app_interact.go
cmd/baha/app_interact_test.go
cmd/baha/app_logs.go
cmd/baha/commands.go
cmd/baha/human_open.go
cmd/baha/machine_coverage.go
cmd/baha/operator_auth_boundary.go
contracts/machine/v1/control.golden.json
docs/cli/applications.md
docs/cli/command-index.md
docs/de/cli/applications.md
docs/de/cli/command-index.md
docs/de/reference/cli-machine-coverage.md
docs/reference/cli-machine-coverage.md
internal/cli/cli.go
internal/cli/cli_test.go
internal/machine/contract.go
internal/operatorauth/context.go
internal/operatorauth/interaction_operations_test.go
```

- GitHub PR files API reports the same 22 paths, and no `.github/**` or catalog path. The file set includes several paths the task note calls reserved, including `cmd/baha/commands.go`, `cmd/baha/machine_coverage.go`, and `internal/machine/contract.go`; this needs an explicit task-scope/coordination basis before accepting the card.
- Current head adds commit `213ca519527b3bfa295c618d0364b221013a6796`, parent `521d76812aa6d87a4f3b48a58347ec21b48c27b0`, subject `docs: match guided exec command syntax`. The exact delta from 521d is `cmd/baha/app_exec.go`, `docs/cli/command-index.md`, and `docs/de/cli/command-index.md`. The latter two are generated indexes reserved by the task note; this review cannot treat direct one-line edits as generator-verified output. Revalidate scope and generation on the actual current head.
- Provenance log requested for the named base and candidate (`git log --oneline ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb..521d76812aa6d87a4f3b48a58347ec21b48c27b0`) is:

```text
521d76812 fix: preserve exec argv after component selector
d44dad4dd fix: pass guided exec command flags through
47c138c4a hop(0428-1623): additive merge --no-ff onto develop b41103867 for coreless-lifecycle repro probe
a3a2a552e Merge remote-tracking branch 'origin/develop' into lane-0428-063-cli2-app-interact
f174513c4 scripts: catalog runtime-gate ownership for changed CLI sources
ea8cddf87 cmd/baha: extract guided app shell/exec path into app_exec.go
d3f56709c Merge remote-tracking branch 'origin/develop' into HEAD
804199430 fix(0428-063): usage validation before operator-auth gate for guided logs/exec
900be2612 Merge remote-tracking branch 'origin/develop' into HEAD
4cbf92960 Reject component filters without a workload contract
accd46da1 Fix CLI application interaction behavior
8014d71ea ci: trigger qualifying pull_request run — card t-20261114-r28-cli2-app-interact
e9c313c5 Merge remote-tracking branch 'origin/cli2-identity-secrets-head' into lane-0428-063-cli2-app-interact
4463ac617 Merge branch 'cli2-identity-secrets-head' into lane-0428-063-cli2-app-interact (base-heal r2)
7ee9c8808 Merge remote-tracking branch 'origin/cli2-identity-secrets-head' into heal-063
1004ecd5f Merge remote-tracking branch 'origin/develop' into lane-0428-063-cli2-app-interact
beb2ee585 cmd/baha: exit-status preservation keeps a plain runtime error identity (0428-063 refinement)
78e8257eb cmd/baha: guided app logs/exec/urls over the status read view (0428-063)
```

- The log contains commits authored by other lanes (`w21-pr1702-0428-246-footprint`, `w091-0428-091`, `w073-perses-alerts`, `w206`, and `lv4-verify`) as well as Marcel. The task has accepted dependencies and a prior stacked history, but this log is not “only own commits”; the review cannot attest that the strict provenance condition is satisfied. Reconcile the chain provenance rather than assuming every imported commit is in-scope.

## Hosted test and environment-gate receipts

- Run `45178269349` is the pull-request run for the mission’s exact head `521d76812aa6d87a4f3b48a58347ec21b48c27b0`; GitHub reports terminal `completed / cancelled` and zero jobs. It supplies no named access-CLI test receipt and no coreless-application-shard result.
- Run `45178624184` is the current pull-request run for current head `213ca519527b3bfa295c618d0364b221013a6796`; at the last observation it was `pending` with no jobs listed. It has no terminal `PR Selected Checks` aggregate and no log receipt yet. `gh pr checks 1623` reported no checks on the branch at that observation.
- Run `45177957547` is for older head `d44dad4dd2fbf9a5e2314c04b39f3936840b1471` and was still in progress; it cannot prove the requested or current head.
- Candidate source contains named access CLI tests including `TestGuidedLogsParsesTailComponentsAndFollowJSONSplit`, `TestGuidedLogsJSONNeverFollowsAndFailsClosedNoninteractive`, `TestGuidedExecParsesComponentCmdAndExitStatus`, `TestGuidedExecExitStatusIsPreserved`, `TestGuidedExecNonInteractiveAmbiguityFailsClosed`, `TestGuidedURLsListOnlyVerifiedAppAndBoundServiceURLs`, and `TestAppURLsJSONShapeStaysSecretSafe`. These are source names, not execution receipts. No exact hosted PASS line or valid package receipt was available for head 521 or current head 213 at review time.
- The required coreless-lifecycle application shard is neither proven green nor proven cleanly skipped on the exact candidate. The only observed exact-head run for 521 was cancelled before jobs; the current-head run was pending. Do not infer green from the mission statement or from another head.

## Source review and repo-rule compliance

- Read-only source inspection at 521 confirms the guided exec path validates component selection before explicitly enforcing `app.exec` authorization, routes `--cmd` through workload `sh -c` without invoking a host shell, and returns child exit status through `cli.WithExitCode`. URL listing derives app endpoints and bound service GUI entries from the status view and exposes verified status rather than guessing accessibility. These observations do not replace the missing exact-head tests.
- Product tests were not run locally, consistent with COST_CONTROL. No source, PR, workflow, or branch was changed by this review; no CI rerun or workflow dispatch was initiated. No subagents were used. Planning remote was verified before committing this evidence: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Session identity: Codex, model family GPT-6 as disclosed to this session; exact backend build metadata is not exposed. Review task/lane identifier: `codex-rev2-1736`; owner-directed Codeman session identifier: `9142ab1f-c464-4f2f-abc8-d6997d8655ae`.

## Findings and decision — pre-reactivation snapshot (superseded below)

ROLE: REVIEW
VERDICT AT PRE-REACTIVATION SNAPSHOT: BLOCKED

The mission’s exact head 521d is no longer the remote PR head. Its run 45178269349 was cancelled before any jobs, while current head 213ca has only a pending run and no receipts. The full-pre-release blocker remains on the authoritative Planning task. The current candidate also contains a later generated-index edit, and the requested base-to-head log contains other-lane commits whose provenance cannot be certified under the strict rule. No merge was attempted, as explicitly directed by the mission.

Repair recipe: keep the existing PR chain, resolve whether the 213ca docs/index commit is authorized and regenerate the reserved command indexes through the supported generator; reconcile the foreign-author history against the task dependency/stack policy and exact base; then obtain a terminal `pull_request` run for the resulting exact current head with `PR Selected Checks` from integration 15368, named access CLI test or valid package receipt, and the coreless application shard green or demonstrably clean-skipped. Recheck the authoritative task’s full-pre-release blocker and all required source/Planning evidence before any acceptance or merge.

## Cleanliness

- Before review source inspection, shell PID `2362373`: `docker ps -a` printed only `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`; no containers were listed.
- No containers or compose projects were started by this session. A second docker listing is recorded after review in the final addendum.

Historical END_BLOCKED snapshot, superseded by the terminal post-merge review below: the PR had not yet produced the requested terminal run when this snapshot was recorded.

## Final live snapshot and after-cleanliness witness

- Final product `git ls-remote` again returned `ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb refs/heads/develop` and `213ca519527b3bfa295c618d0364b221013a6796 refs/pull/1623/head`.
- Final PR API remained `OPEN`, current head `213ca519527b3bfa295c618d0364b221013a6796`, base `develop`, `mergeStateStatus=BLOCKED`.
- Final poll of run `45178624184` remained `pull_request / pending` on exact current head `213ca519527b3bfa295c618d0364b221013a6796`; no terminal conclusion or job receipts were present.
- After review, shell PID `2381588`: `docker ps -a` printed only `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`; no containers were listed.

## Validation STATE

`python3 scripts/plan.py check` reported `error: tasks/t-20261123-wizard-org-default-usageerror.md: resolution is only valid on a checked card` (698 tasks, 1 error, 10 warnings). This is an unrelated Planning task; it was not edited as part of this review. `git diff --check` passed, and the review evidence contains no markdown checkbox lines.

## Required origin/main path witness before this publication

Immediately before this evidence update, `git fetch origin main && git ls-tree -r --name-only origin/main | grep '^evidence/r28-welle5-2026-11-23/sweep-1623/review-merge.md$'` emitted this exact output:

evidence/r28-welle5-2026-11-23/sweep-1623/review-merge.md

## PLAN — re-dispatch at 2eb6f40bd

1. Record this re-dispatch plan and read the prior blocked review plus current task contract.
2. Refresh GitHub remote refs, PR head/base, exact-head run, and all requested receipts.
3. Review the exact candidate diff for card scope, gate routing, and source/security behavior.
4. Document the exact-head verdict and cleanliness; do not merge under this mission.
5. Publish the updated evidence to baseharbor-plan origin/main, synchronize the board, and post final status.

## Re-dispatch observation hold — awaiting lane 0847

- Current PR #1623 remote refs at this re-dispatch: `develop` is `ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb`; PR/branch head is `2eb6f40bd3a5724f11c655621c8b5bc99c48b022` (the mission short SHA `2eb6f40bd`).
- Run `45182759775` is for exact head `2eb6f40bd3a5724f11c655621c8b5bc99c48b022`, pull_request event, and remains `pending` with zero registered checks. The older run `45178624184` is for head `213ca519527b3bfa295c618d0364b221013a6796` and remains `in_progress`; it is not evidence for the new head.
- Coordinator correction: the earlier 0/0 interpretation was not terminal success; it reflected no registered checks on the new head. Lane 0847 owns observation. This review is paused until that lane delivers an END with terminal status; only then resume against its final SHA.
- No review verdict is issued in this interim note. No product tests, CI reruns, workflow dispatch, product edits, or merge actions were performed during this pause.

Planning remote verification before this evidence update: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.

## Required origin/main path witness before this interim publication

Immediately before this evidence update, `git fetch origin main && git ls-tree -r --name-only origin/main | grep '^evidence/r28-welle5-2026-11-23/sweep-1623/review-merge.md$'` emitted this exact output:

evidence/r28-welle5-2026-11-23/sweep-1623/review-merge.md

## PLAN — m_rev_1623pm follow-up

1. Record this mission plan, then read m_rev_1623pm and determine its scope against the current hold.
2. Check available lane 0847 state, then refresh exact remote refs, final SHA, and terminal run status.
3. Review the specified final candidate and verify test, gate, scope, and provenance evidence.
4. Publish the verdict and actionable findings without merging unless explicitly authorized.
5. Publish updated evidence to baseharbor-plan origin/main, synchronize the board, and post the required lane status.


## Superseding post-merge review — m_rev_1623pm

ROLE: REVIEW

The user supplied `/tmp/opencode/m_rev_1623pm.md.g` as the active post-merge review mission. This section supersedes the earlier paused/blocked snapshot and records only observed remote state. Planning task `t-20261114-r28-cli2-app-interact` / card 0428-063 now reports `state: accepted`; its three dependencies also report accepted. This review did not alter the task status.

### Remote and merge facts

- Product remote checked before this review closeout: `https://github.com/mcpdev80/baseharbor.git`.
- Product `git ls-remote` before closeout returned:

```text
f3d84787462f324a6311e2e95928441c64a09296 refs/heads/develop
2eb6f40bd3a5724f11c655621c8b5bc99c48b022 refs/pull/1623/head
```

- Codeman `agent ls --json` showed no live session named with `0847` or `1623`; the current mission supplied the final head, and the terminal GitHub run was independently re-read directly. PR API reports #1623 `MERGED`, merge commit `f3d84787462f324a6311e2e95928441c64a09296`, merged at `2026-11-23T14:03:35Z` by `mcpdev80`; source head was `2eb6f40bd3a5724f11c655621c8b5bc99c48b022`, base `develop` at `ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb`.
- The merge commit has the exact base as its parent. GitHub compare from that base to the merge commit reports ahead by 1, behind by 0, merge base `ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb`.
- The source candidate compare reports that same merge base, 20 commits ahead, and zero behind. Its history includes task/hop merges and the accepted identity-secrets dependency; the final effective merge diff is bounded to the 22 paths below. No unrelated `0428-258` wizard path is in the diff; that change is already in the base. This post-merge review records the candidate ancestry rather than claiming the range is composed solely of commits authored in this lane.
- Merged diff paths:

```text
cmd/baha/app_access.go
cmd/baha/app_access_urls.go
cmd/baha/app_exec.go
cmd/baha/app_interact.go
cmd/baha/app_interact_test.go
cmd/baha/app_logs.go
cmd/baha/commands.go
cmd/baha/human_open.go
cmd/baha/machine_coverage.go
cmd/baha/operator_auth_boundary.go
contracts/machine/v1/control.golden.json
docs/cli/applications.md
docs/cli/command-index.md
docs/de/cli/applications.md
docs/de/cli/command-index.md
docs/de/reference/cli-machine-coverage.md
docs/reference/cli-machine-coverage.md
internal/cli/cli.go
internal/cli/cli_test.go
internal/machine/contract.go
internal/operatorauth/context.go
internal/operatorauth/interaction_operations_test.go
```

These paths implement the card’s guided `app logs`, `app exec`/`app shell`, and `app urls` behavior, authorization/operation registration and tests. The EN/DE command indexes are the authorized syntax synchronization documented in `env-gate-fix.md` § Scope reconciliation and the `d65029d97` / `604c79b65` evidence lineage. The effective diff has no `.github/**`, runtime-gate catalog, or integration-harness change.

### Exact-head CI receipts

- PR run `45182759775`: event `pull_request`, exact head `2eb6f40bd3a5724f11c655621c8b5bc99c48b022`, terminal `completed / success` at `2026-11-23T14:03:14Z`.
- The terminal aggregate `PR Selected Checks`, check-run `137745621894`, app `github-actions` (`15368`), has the same exact head and terminal `completed / success`. The aggregate executed its selected native-acceptance, complete selected Go-shard coverage, and normal selected-job result requirements. Unselected unrelated matrix jobs are skipped by selection; that is not reported as a pass for those jobs.
- `PR · Go unit · cli-3`, job `137732225005`, exact head `2eb6f40bd3a5724f11c655621c8b5bc99c48b022`, terminal success. Its executed receipt is `PASS cli-3: 449 passed / 17 intentionally skipped / 466 discovered; CLI inventory total=1916`. This is the package/shard receipt allowed by the 1606 acceptance rule. The 17 skips are reported as intentional; no failing or missing `cli-3` receipt was observed.
- The selected coreless application shard job `PR · Selected Core-less · docker / PR selected · integration/docker/coreless-lifecycle · application`, job `137732302937`, exact head `2eb6f40bd3a5724f11c655621c8b5bc99c48b022`, terminal success at `2026-11-23T13:51:25Z`. The job executed `Run exact selected Core-less lifecycle gate` successfully and then `Clean owned runtime and local registry` successfully. Its log shows passing executions for `TestSelectiveApplicationBackendRuntimeAddRemoveReAdd`, `TestSelectiveHTTPSRuntimeAddRemoveReAdd`, `TestManagedRegisteredOTLPNativeConsumerHandoff`, and `TestEnvironmentDestroyNativeLifecycle`. The selected-group aggregate `137739801441` is also terminal success. This is an executed gate, not a skipped receipt.
- The prior env-gate classification (b) concerned catalog/harness routing and acceptance-only fixtures. Neither catalog nor harness was changed in the merged diff; the exact selected application shard ran and passed, with explicit cleanup. No gate-drop or skip-hiding change is present in the merged source diff.

### Source review and compliance

- The reviewed behavior remains bounded to the card: logs use the status read view and bounded tail/follow semantics; exec treats `--cmd` as one command unit, preserves the child exit status, and does not invoke a host shell; URLs are derived from the secret-safe status model and report verified/unverified accessibility. Authorization is enforced for the `app.logs`, `app.exec`, and `app.urls` operation categories before execution or guidance.
- No product source was edited by this review. No PR update, workflow dispatch/rerun, local product test, container start, or merge action was performed by this session. No subagents were used.
- Planning remote was verified before evidence publication: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- `python3 scripts/plan.py check` still reports one unrelated error at `tasks/t-20261123-wizard-org-default-usageerror.md` (“resolution is only valid on a checked card”) and ten warnings; the 0428-063 task itself is accepted. `git diff --check` passed. This evidence contains no markdown checkbox lines.
- Session identity: Codex, GPT-6 model family; exact backend build metadata is not exposed. Lane identifier `codex-rev2-1736`; requested owner-directed Codeman session `9142ab1f-c464-4f2f-abc8-d6997d8655ae`.

### Verdict and cleanliness

VERDICT: ACCEPTED for the requested post-merge diff and exact-head CI review. No review correction is required; no recipe is pending. The repository merge was performed by the owner before this review, not by this session.

- Before closeout, shell PID `3505374`: `docker ps -a` printed only the header; no containers were listed.
- After source review, shell PID `3648406`: `docker ps -a` printed only the header; no containers were listed. No local container or compose project was started by this session.

Final product `git ls-remote` after review and before evidence publication:

```text
f3d84787462f324a6311e2e95928441c64a09296 refs/heads/develop
2eb6f40bd3a5724f11c655621c8b5bc99c48b022 refs/pull/1623/head
```

Final PR #1623 head remains `2eb6f40bd3a5724f11c655621c8b5bc99c48b022`; merged develop remains `f3d84787462f324a6311e2e95928441c64a09296`.

END_DONE codex-rev2-1736: PR #1623 post-merge diff matches card 0428-063 plus authorized syntax sync; exact-head cli-3, selected coreless application gate, and PR Selected Checks are terminal-success at 2eb6f40bd3a5724f11c655621c8b5bc99c48b022; merged as f3d84787462f324a6311e2e95928441c64a09296.


Required origin/main path witness for this post-merge publication. Immediately before the evidence commit, `git fetch origin main && git ls-tree -r --name-only origin/main | grep '^evidence/r28-welle5-2026-11-23/sweep-1623/review-merge.md$'` emitted this exact matching path:

evidence/r28-welle5-2026-11-23/sweep-1623/review-merge.md
