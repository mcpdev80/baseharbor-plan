# PR #1614 final review and merge decision

## PLAN

1. Read the mission and bind review to the stated PR, head, base, and acceptance evidence.
2. Refresh remote state and verify the candidate head, base head, task contract, and provenance.
3. Inspect the candidate diff, security-sensitive paths, and exact-head required CI receipts.
4. Merge only if each acceptance criterion is evidenced; otherwise record a precise fix recipe.
5. Publish this evidence in baseharbor-plan, update the live board, and report the decision.

## Decision

BLOCKED. PR #1614 was not merged. Two required acceptance claims are not proven by the terminal run: the named app-edit lifecycle test is absent from the wizard job's executed-test list, and no Podman coreless cell ran. The status/version review also found that the partial workspace-resolution fallback can emit an unresolved local source identity without an explicit unresolved observation or warning. These are concrete review blockers for the stated acceptance. No code, workflow, branch, PR, or protection setting was changed, and no rerun or workflow dispatch was requested.

## Candidate and task

- Mission: `/tmp/opencode/m_rev_1614.md.g`.
- Task card: `baseharbor-plan/tasks/t-20261114-r28-cli2-app-status.md` (0428-062, state `wait`, PR #1614). The card depends on accepted 0428-059 source-model and 0428-060 contract work. Its scope is the unified app status/version read model, preserving declared component identity and making unresolved provenance explicit; it does not authorize a release or tag.
- Product remote: `https://github.com/mcpdev80/baseharbor.git`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1614/head` returned:
  `b3df96348a9c56de00d67a060c9a5f0ddf6593d5 refs/heads/develop`
  `0f9747e315b4ac78fea841c666254273544eba73 refs/pull/1614/head`
- PR #1614 was open, based on `develop`, and reported mergeable/clean. The base head was the exact current develop head above. Candidate head: `0f9747e315b4ac78fea841c666254273544eba73`.
- The candidate diff from current develop comprised the 24 paths recorded by the remote PR diff: app status/version collectors, result/view/command code and tests under `cmd/baha`, machine read-model schema and implementation, and English/German CLI documentation. `.github/**` was unchanged. `scripts/pr-gate-coverage.json` was byte-identical to develop. No workflow file was modified.
- The review used the previously published lineage and ingress records: `evidence/r28-welle5-2026-11-23/sweep-1614/hop-wave.md`, `evidence/r28-welle5-2026-11-23/sweep-1614/final-hop-f50b.md`, and `evidence/r28-welle5-2026-11-23/sweep-1614/ingress-forward-rows.md`. Those preserve the final-hop and ingress-forward references named in the mission. The final-hop record itself says the wizard app-edit test was not selected on that head, which conflicts with the mission's claimed test receipt.

## CI and acceptance evidence

- Exact-head run `45131868957` completed with conclusion `success` for head `0f9747e315b4ac78fea841c666254273544eba73`. The terminal `PR Selected Checks` aggregate (job `137556374206`, integration app 15368) succeeded at `2026-11-23T07:51:58Z`.
- The trusted plan job `137548977869` used base SHA `b3df96348a9c56de00d67a060c9a5f0ddf6593d5`, selected Go scope `full`, and logged `No narrow mapping: conservative checks selected.` This is the broad fallback for the unknown/old path mapping; it does not cure a required named test that the executed job did not run.
- The wizard-registration job `137549066105` succeeded. Its `matched_tests` list contains `TestAppRegistrationCICommandHelpAndJSONDiscovery`, `TestCommandTreeCIRouterPathsUnique`, `TestMachineCoverageCIRealTreeAndJSONClassification`, `TestMachineDocumentationTracksRegistryAndCommandTree`, `TestHumanCommandIndexTracksExactCommandMetadata`, and `TestMCPRegistrationCIInProcessDiscoverAndInvoke`. It does not contain `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`. Searching the exact run's relevant job logs did not find an execution or PASS line for that test. Therefore the mission's wizard-test criterion is not met by this run.
- Docker coreless jobs did execute and pass, including core-capability job `137549122051`; that job's reported lifecycle tests were `TestApplicationCapabilityLifecycleExistingCore` and `TestApplicationCapabilityLifecycleFootprintShowDigestConsent`. Neither is the named app-edit lifecycle test.
- The exact run has no Podman coreless job. Podman observability job `137549621114` succeeded, but it is not a Podman coreless lifecycle cell. Podman coreless jobs were skipped or unselected. A skipped/unselected cell is not green execution evidence, so the mission's Docker/Podman coreless acceptance is incomplete.
- The run summary showed 74 check-runs: 31 successful, 43 skipped, zero failed, and zero active. The terminal aggregate's success is recorded as an aggregate only; it is not treated as proof of skipped job execution. Candidate-added advisory validation was skipped and is not presented as required evidence.
- The repository review rules prohibit editing `.github/**` or dispatching/rerunning workflows in this mission. I did neither. The exact route for the named test and Podman coreless cell must be established in the authorized CI selection/gate path, and a new exact-head terminal run must show both tests actually executed and passed. If this requires a workflow-file change, that is outside this reviewer write-set and must be carried by the Owner; no workflow edits are made here.

## Code and security review

- `cmd/baha/app_versions_view.go` at candidate lines 165–186: when `development.ResolveWorkspace` fails, `partialWorkspaceResolution` returns a fallback and an `unresolved` component list. The caller uses only the fallback and drops the unresolved list. For a failed local checkout, lines 172–186 then project the configured source identity (fallback `Identity` when the resolved `Root` is empty) and return no warning. This contradicts the function's contract at lines 79–83 that an unresolved local mapping carries an explicit unmapped state and warning; it can present a configured local path as if it were resolved. Fix by retaining per-component resolution state in the projection and rendering explicit unmapped/unclear observation plus warning for unresolved local components; add a regression covering a mixed model with one resolvable source and one unresolved local source. Ensure the regression is selected by the same durable CI path.
- `cmd/baha/app_versions_view.go` lines 220 onward and the shared selector helpers parse repeatable/comma-separated `-c`/`--component` selectors and reject empty values; the versions view validates the selection against known component rows before filtering. This appears fail-closed for unknown component identities.
- `cmd/baha/app_workspace_source_model.go` lines 46–61 authorizes `workspace.show` before loading the source model. Mutating paths separately authorize their operation, e.g. source add lines 165–180 authorizes `workspace.init` before writing, and uses validated upsert/write paths. This does not show a consent/authorization weakening in the inspected path; the observed direction is stricter read authorization plus operation-specific mutation authorization.
- Version source rows distinguish declared image metadata claims from verified provenance, and the collector does not invent undeclared components. No security-sensitive consent relaxation was found in the inspected diff. The explicit unresolved-local-source state issue above remains a correctness and provenance blocker.
- The complete prior final-hop and ingress rows are linked above. The card's required lineage evidence is present as path references; no additional product changes are in scope for this review.

## Review protocol and repository scope

- The integration rule `PR Selected Checks` was active for develop and the terminal aggregate succeeded. Ruleset state read during review showed the develop integration-branch ruleset disabled and the required-check ruleset active; no protection bypass was used or claimed.
- No PR review approvals or review comments were present at review time. This decision is a blocking review finding, not an acceptance or merge authorization.
- Evidence repository remote was verified before the evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git`.
- No product files, workflow files, branches, PR state, rulesets, or release artifacts were changed.

## Cleanliness

- Host shell PID `462620`, before review finish: `docker ps -a` returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`); no containers were listed.
- No container or compose project was started by this review.
- After review, host shell PID `470857`: `docker ps -a` again returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`); no containers were listed.

## Fix recipe and handoff

1. Correct the partial workspace-resolution projection so unresolved local components cannot be surfaced as resolved identities; preserve explicit unmapped/unclear state and warning.
2. Ensure `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` is reached by the trusted selected CI job on this card's candidate, and prove its PASS line in the job log.
3. Ensure the Podman coreless lifecycle cell required by acceptance is selected and executed on the exact candidate; an observability-only Podman job is insufficient.
4. Run the authorized CI path on the exact candidate and current base, then provide the terminal `PR Selected Checks` aggregate and per-job logs proving execution. Keep PR #1614 unmerged until these findings are resolved and reviewed.

END_BLOCKED codex-rev2-1736: PR #1614 not merged; required app-edit lifecycle execution and Podman coreless evidence are absent; candidate 0f9747e315b4ac78fea841c666254273544eba73.

## Planning evidence validation

- `python3 scripts/plan.py check`: 694 tasks, 7 epics, 13 releases, 24 decisions; 0 errors and 10 pre-existing dependency warnings.

## Origin publication witness

- `git ls-remote origin refs/heads/main` after the first evidence push returned exactly: `0ff4850d92f1c37f5f2d833c035f07ecfb5d2157\trefs/heads/main`.
- Required `git fetch origin main && git ls-tree -r --name-only origin/main | grep '^evidence/r28-welle5-2026-11-23/sweep-1614/review-merge-final.md$'` output, copied exactly:
  `evidence/r28-welle5-2026-11-23/sweep-1614/review-merge-final.md`

## Final freshness read before handoff

- A final `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1614/head` read returned:
  `826d498fc1ae9524112d07477a8809798d8272a7 refs/heads/develop`
  `0f9747e315b4ac78fea841c666254273544eba73 refs/pull/1614/head`
- A final read-only GitHub API check still reported PR #1614 open and non-draft, head `0f9747e315b4ac78fea841c666254273544eba73`, base SHA `b3df96348a9c56de00d67a060c9a5f0ddf6593d5`, `mergeable: true`, and `mergeable_state: behind`. The remote `develop` tip is now `826d498fc1ae9524112d07477a8809798d8272a7`; this base/head freshness mismatch is recorded as observed state. No rerun, dispatch, or PR update was initiated.
- The latest check-runs read remained for the same PR head. `PR Selected Checks` and Docker coreless succeeded; Podman observability succeeded; the Podman coreless and named wizard app-edit test are still absent. A successful aggregate does not resolve those missing acceptance receipts or the behind state.

- Final required `git fetch origin main && git ls-tree -r --name-only origin/main | grep '^evidence/r28-welle5-2026-11-23/sweep-1614/review-merge-final.md$'` output before the final evidence push:
  `evidence/r28-welle5-2026-11-23/sweep-1614/review-merge-final.md`

## PLAN — refreshed review

1. Re-read the m_rev_1614 mission and confirm candidate, write-set, and acceptance criteria.
2. Refresh product and Planning remote state and check whether the candidate or PR state changed.
3. Reinspect exact-head diff, security paths, CI receipts, and required lineage evidence.
4. Complete only the authorized review/merge action if all gates pass; otherwise record a repair recipe.
5. Publish refreshed evidence on baseharbor-plan origin/main, update the board, and post status.


## Fresh review update — current remote state

This update supersedes older candidate, base, and run identifiers in the historical review sections above. The current PR head and receipts were re-read from GitHub on 2026-11-23 after the mission's claimed SHA was found not to exist on the PR remote. This session did not modify product files, the PR, workflows, branches, or protection settings, and did not dispatch or rerun CI.

- Mission candidate `7a155768719316f119dc42531cf02615771244e0` was not found by GitHub's commit check lookup. The current remote PR #1614 head is `fbc501b64851121a9080eae4bdca0278d28561ef` on `lane-0428-062-cli2-app-status`.
- Fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1614/head` returned `304b3ad1d88647377ea647d0d94174bfc9298e14 refs/heads/develop` and `fbc501b64851121a9080eae4bdca0278d28561ef refs/pull/1614/head`.
- GitHub PR API reports state `open`, `draft=false`, base ref `develop`, base SHA `a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d`, head SHA `fbc501b64851121a9080eae4bdca0278d28561ef`, `mergeable=true`, `mergeable_state=behind`. Compare `c3e49f3cc1959db68d57e52db0408bd48a043292...a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d` reports `status=behind`, `ahead_by=0`, `behind_by=1`. The later develop tip is `304b3ad1d88647377ea647d0d94174bfc9298e14`; the PR has not been updated to it.
- The current PR files API reports 23 changed paths, zero `.github/**` paths, and zero catalog paths. No CI/workflow ownership conflict was introduced by this current diff.

## Exact-head CI review

- Existing run `45149713215` is terminal `completed/success` on exact head `fbc501b64851121a9080eae4bdca0278d28561ef`. Its `PR Selected Checks` aggregate is terminal success. I observed the existing run; I did not initiate it.
- The trusted-plan job `137607751558` completed success and its log explicitly says `No narrow mapping: conservative checks selected.` It identifies `VERIFIED_BASE=c3e49f3cc1959db68d57e52db0408bd48a043292`, the run's current develop target at dispatch. The PR API still names older base `a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d`, so a green check against the newer trusted target does not make the PR base current or remove GitHub's `behind` state.
- Wizard validation job `137607847719` completed success. Its log executes the existing validation owner dispatcher and contains no execution output or PASS line for `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`. The grep for that exact test name in the complete job log returned no match. The job's successful status is not proof that the mission's named test ran.
- Docker selected coreless lifecycle jobs for `foundation`, `application`, `identity-backend`, and `core-capability` all completed success. The `core-capability` job was terminal success. This records those cells only; it does not satisfy the missing named app-edit test.
- The current run has a successful Podman observability runtime job, but no Podman coreless lifecycle cell. The Podman coreless application-backup selected cell was skipped. A Podman observability result cannot substitute for the mission's required Podman coreless result.
- The run is green as an aggregate but the required named wizard test and Podman coreless cell are not evidenced as executed. Skipped jobs do not count as passing evidence.

## Current code finding

At exact head `fbc501b64851121a9080eae4bdca0278d28561ef`, GitHub source for `cmd/baha/app_versions_view.go` lines 164–186 still shows this behavior: on `ResolveWorkspace` failure, the code calls `partialWorkspaceResolution`, discards the returned unresolved-component list, uses the fallback resolution, projects `component.Identity` when no resolved root exists, and returns projections without an unresolved warning/state. This can display a configured local source identity as if it were a resolved source. It remains a provenance correctness blocker. Preserve each component's resolution state, render an explicit unresolved/unclear observation and warning, and add a mixed-model regression with one resolvable and one unresolved local source. The new regression must be selected by a durable CI path in the same PR.

## Current decision and repair recipe

END_BLOCKED codex-rev2-1736: PR #1614 not merged; current candidate fbc501b64851121a9080eae4bdca0278d28561ef lacks the named lifecycle test receipt and Podman coreless execution, retains unresolved local provenance fallback, and its PR base is behind.

1. Fix the unresolved local-source projection and add the mixed-model regression. Keep the displayed source from implying a successful resolution when resolution failed.
2. Establish a real CI route for `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` and the required Podman coreless cell, then obtain exact-head logs showing both actually executed and passing. Do not count the broad aggregate alone or skipped jobs as a pass.
3. Bring the PR base to the required current develop base through the authorized candidate workflow and wait for the terminal exact-head aggregate. Do not merge while GitHub reports `behind` or the required receipts are missing.
4. Review the corrected exact head and its remote evidence before any merge decision.

## Cleanliness — current review

- Shell PID `1785625`, after CI observation and source review: `docker ps -a` returned only `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`; no containers were listed.
- This review started no containers and no compose projects.

## Evidence repository verification

- Verified planning remote before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Current product remote witnesses above were obtained only from the GitHub URL `https://github.com/mcpdev80/baseharbor.git`.

## Final origin/main path witness

The required `git fetch origin main && git ls-tree -r --name-only origin/main | grep '^evidence/r28-welle5-2026-11-23/sweep-1614/review-merge-final.md$'` was run immediately before this evidence update. Exact grep output:

`evidence/r28-welle5-2026-11-23/sweep-1614/review-merge-final.md`

## Role and verdict

CODEX-REVIEW: BLOCKED. No merge performed. The current exact-head terminal run does not prove the named app-edit lifecycle test or Podman coreless cell; the unresolved local provenance finding remains; PR #1614 base is behind.
