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
