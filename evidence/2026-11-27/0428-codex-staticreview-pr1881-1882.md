# Static review of BaseHarbor PRs #1881, #1882, and #1884

## PLAN

1. Read both task contracts and existing evidence; record acceptance criteria and scope.
2. Verify GitHub remotes, exact PR heads, and develop base; record provenance before review.
3. Inspect SHA-exact diffs for #1881 and #1882 against develop `6944e8761`; check scope and test coverage.
4. Compare each diff to its card contract, consent/auth gates, CI surface, and existing test scaffold.
5. Write separate PASS or CHANGES verdicts with file:line evidence in this akte.
6. Publish only the review evidence through an isolated Plan PR; no product edits, merge, or rerun.

## PLAN extension for PR #1884

7. Extend the comparison to PR #1884 (0428-292): verify exact head and develop base `6944e8761`, record ancestry, changed paths, consent-gate integrity, and terminal run `46032316692`.
8. Correct the comparative trusted-catalog lift analysis against the exact base planner and all eight candidate PR records; distinguish repeated paths and the separate #1876-family hold.
9. Publish this same akte through a fresh isolated Plan PR and verify its exact-head Plan validation.

## Review status

Mission read: `coordinator/missions/codex-staticreview-1881-1882.txt`. No native `todowrite` tool is exposed in this session; board plan is recorded in the live JSON todo file.

## Visible commit identity block

- Exact task frontmatter owners verbatim fetched from Plan `origin/main` `41972b641f9b97f29dbf1aec320309d21568645b`: `owner: w399-0428-289-providers` (0428-310), `owner: w397-0428-307-idfallback` (0428-315), and `owner: w399-0428-289-providers` (0428-292).
- Git user.name: `w267-0428-284-pridentity`.
- Git user.email: `w267-0428-284-pridentity@baseharbor.local`.
- Literal commit invocation: `git -c user.name=w267-0428-284-pridentity -c user.email=w267-0428-284-pridentity@baseharbor.local commit ...`.
- Pre-push author gate: `git show -s --format=%an HEAD` must equal `w267-0428-284-pridentity`.

## Provenance and exact candidates

- The evidence worktree was initially cut from Plan `origin/main` `e06de0fc45479a59272daea0f662e9bb6b058012`. Before creating the evidence branch/first commit, the verified Plan remote advanced to `dd9561905a66d95445f6139bfff37820efe19f7c`; this current main is merged into the evidence branch below. The initial base SHA remains the ancestor of the first commit.

- Plan repository remotes verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Plan evidence worktree was cut from exact `origin/main` SHA `e06de0fc45479a59272daea0f662e9bb6b058012`.
- Product remote is `https://github.com/mcpdev80/baseharbor.git`. Fresh `git ls-remote` returned `6944e8761af6f07b801f55e39bb9a5409226c10b refs/heads/develop`, `fc510d73d52ab86a51a3948e9e3e8bdf1c116e95 refs/pull/1881/head`, and `be410aea1ceee44163a26f7ad7eecc94b808e275 refs/pull/1882/head`.
- PR #1881 is OPEN, non-draft, branch `lane-0428-310-migration-marker`, mergeState BEHIND. GitHub compare against develop `6944e8761` reports status `diverged`, ahead 1 / behind 1, merge base `ea5218d72e263f21e79853b679af50074dab8c25`. Its content diff is based on that merge base; the current develop head is one commit newer.
- PR #1882 is OPEN, non-draft, branch `lane-0428-315-timeouts`, mergeState BLOCKED. GitHub compare against develop `6944e8761` reports status `ahead`, ahead 2 / behind 0, merge base `6944e8761af6f07b801f55e39bb9a5409226c10b`.
- #1881 files: `internal/orgconfig/migration_marker_test.go`, `internal/orgconfig/store.go`, `scripts/pr-gate-coverage.json`. #1882 files: `cmd/baha/app_observe.go`, `internal/application/timeouts.go`, `internal/application/timeouts_test.go`, `scripts/pr-gate-coverage.json`. Neither diff contains `.github/**`, consent, or operator-auth changes.
- Card owners fetched verbatim from this Plan `origin/main`: 0428-310 has `owner: w399-0428-289-providers`; 0428-315 has `owner: w397-0428-307-idfallback`.

## Test and CI routing review

- Existing non-draft pull-request CI has `pr_unit_shards` in `.github/workflows/ci.yml:1290-1320`; it depends on the trusted PR plan, selects its matrix from `unit_matrix`, and runs `scripts/pr-unit-database.sh`. The source-to-package selector at `.github/workflows/ci.yml:1762-1806` uses changed Go files with `scripts/pr-draft-go-packages.py` and runs selected non-CLI package tests. Both new Go test files are therefore reachable through the existing package shard on pull-request events; no workflow trigger or `.github/**` change is needed.
- The selected package shard did not execute for the observed terminal runs because the trusted base-catalog plan failed first. Do not treat skipped unit jobs as test receipts. After the catalog owner lifts the base hold, the owner/lane must produce the required fresh exact-head hosted evidence.
- #1881 adds `TestWorldWritableMigrationMarkerWriteFailureFailsClosed` and `TestMigrateToCanonicalKeepsDataBeforeMarkerOrder`. Candidate catalog rows map the changed orgconfig files to Docker and Podman data-capability surfaces. The observed run `46020925858` failed `PR · Trusted Plan` with `uncataloged source change` for both files; `PR Selected Checks` then rejected empty `UNIT_SCOPE` with `REJECT: Go test selection missing or invalid`. Earlier same-head run `46020800719` was cancelled; its Go shards were cancelled and are not test receipts.
- #1882 adds `TestStatusTimeoutMatrixValues`, `TestStatusTimeoutMatrixDistinctGroups`, and `TestManagementServicesShareManagementGroup`. Candidate catalog rows map these files to `source.gate.integration.static.public.contracts`; independently, changed Go paths are selected by the package shard described above. Run `46024898195` failed `PR · Trusted Plan` with `uncataloged source change` for `internal/application/timeouts.go` and `internal/application/timeouts_test.go`; the aggregate also rejected the missing unit selection. No test result is available from this run.
- No local test command, rerun, workflow_dispatch, product edit, or merge was performed in this static review.

## Verdict: PR #1881 — CHANGES

- Blocking finding at `internal/orgconfig/store.go:340-361`: `writeFrozenMarker` discards the read-back bytes and only checks that `os.ReadFile` succeeds; `frozenMarkerComplete` likewise treats every readable non-directory file as complete. An empty or wrong-content marker therefore makes `migrateToCanonical` return success at lines 417-420, despite the canonical content constant at line 294. Make both checks compare exact bytes to `canonicalMarkerContent`, return failure for mismatch, and add empty/truncated/wrong-content regression coverage.
- Blocking finding at `internal/orgconfig/store.go:214-225` and `:447-475`: after marker-write failure, `adoptLegacySelection` returns `adopted=true` plus an error; `LoadActiveOptional` immediately returns that error. On a subsequent call the direct canonical read succeeds and bypasses `adoptLegacySelection`, so the marker is never retried. If the canonical file is later absent, no marker exists to prevent legacy re-adoption. Make the production load path repair/complete the marker safely before it accepts the migrated state or otherwise ensure the once-only marker cannot be lost; add a two-call `LoadActiveOptional` regression that does not manually call `writeFrozenMarker`.
- Blocking durability finding at `internal/orgconfig/store.go:390-423`: syncing the temporary data file before rename does not make the renamed directory entry durable. No parent-directory sync occurs after the canonical rename and before marker creation. A crash can therefore lose the canonical name while a later marker claims migration completion. Sync the containing directory after the data rename before writing the marker, then persist marker creation in the same directory; preserve data-before-marker ordering and test the ordered filesystem operations through the existing seam.
- The observed trusted-base-catalog failure is a separate owner lift dependency, not evidence that the candidate's new unit tests passed. No rerun is authorized in this mission.

## Verdict: PR #1882 — CHANGES

- Blocking scope finding at `internal/application/timeouts.go:5-31` and `cmd/baha/app_observe.go:19-32`: this PR consolidates `cmd/baha` application-status probe timeouts, but card 0428-315's Task section cites the Perses Tempo query timeout and the object-storage reconcile/readiness values. The PR changes none of those cited files. On the exact base, `internal/metrics/perses_tempo_datasource.go:65-66` defines `tempoTraceQueryTimeout = 10s` and `internal/metrics/perses_tempo_verify.go:98-100` uses that same constant, so the alleged Tempo mismatch is not present. `internal/objectstorage/seaweedfs.go:32-34` gives 120s reconcile, 90s readiness, and 3s existing-provider probe budgets for distinct operations. Either the authorized task owner must narrow the contract to the CLI status-probe matrix and document why it satisfies H-V42, or the implementation must address the actual cited scope while keeping distinct operation budgets separate; do not silently retarget the card.
- The matrix values preserve the old `app_observe.go` literals, and the aliases at lines 24-32 are behavior-neutral for those CLI probes. The new tests check constants and unique group values but do not test the cited Tempo/Object-storage sites. The existing Go package shard is a real CI route for these tests once the trusted base-catalog dependency is lifted; the current run has no test receipt.
- The observed trusted-base-catalog failure is a separate owner lift dependency. No card edit, rerun, workflow dispatch, or product change is authorized in this review.

## cleanliness

No containers, compose projects, or test VMs were started. This was a read-only product review; only this akte in the isolated Plan worktree and the requested live todo JSON were written.

## Comparative verdict: PR #1884 — CHANGES; Trusted Plan STATE

- Fresh GitHub witnesses: `refs/heads/develop` is `6944e8761af6f07b801f55e39bb9a5409226c10b`; `refs/pull/1884/head` is `e6425f9bf79d57dceddaedee1a07117da3d8a3b1`. `gh pr view 1884` reports OPEN, non-draft, base `develop`, branch `lane-0428-292-consent-ux`, merge state BLOCKED. The base is an ancestor of the exact head.
- Exact diff against develop: 8 files, 543 insertions / 41 deletions. Write-set: `cmd/baha/app_apply.go`, `app_candidate_consent.go`, new `app_candidate_consent_interactive.go`, `app_candidate_consent_test.go`, `app_edit_apply_result.go`, `app_remote_lifecycle.go`, `deployment_record.go`, and `scripts/pr-gate-coverage.json`. No `.github/**` or workflow file is changed. `git diff --check` is clean.
- The acceptance-critical fail-closed checks remain in the path: `app_candidate_consent.go:215-237` requires non-empty consent and constant-time exact digest equality; `deployment_record.go:400-419` resolves explicit/context/one-shot consent before writing and still runs deployment admission; ownership and source availability checks follow before the pending record is assembled (`deployment_record.go:423-449`). The new test file adds positive, refusal, noninteractive, and changed-source cases (`app_candidate_consent_test.go:346-468,493-579`).
- Blocking static finding at `app_candidate_consent.go:240-258`: `interactiveCandidatePromptAllowed` receives the concrete reader `in` but decides interactivity solely from `os.Stdin` being a TTY. The prompt then consumes `in` at lines 116-120. An internal `applicationInput` context reader can differ from `os.Stdin` while process stdin remains a terminal; a queued `y` on that non-terminal reader could then be accepted as operator consent. The test controls `interactiveCandidateStdin` as a boolean (`app_candidate_consent_test.go:355-394,582-599`) and therefore does not prove the supplied reader is the actual terminal stream. Require the consent prompt to consume only a verified terminal reader or to carry an explicit trusted interactive-input capability from the CLI boundary; add a regression with TTY stdin but a different buffered context reader containing `y`, asserting no bind and fail-closed write.
- Additional contract mismatch at `app_remote_lifecycle.go:160-167`: the comment says the prompt is display-only and its answer is not part of remote behavior, but the prompt calls `bindCandidateConsentForSubmission` on `y` (`app_candidate_consent.go:116-120,138-151`), and `recordDeploymentBeforeMutation` consumes that process-global binding (`deployment_record.go:400-411`). There is no remote lifecycle regression in the new test file. Clarify whether this remote `app up` route intentionally accepts inline operator consent; if yes, remove the display-only claim and test the actual remote route end-to-end without weakening the Core-side gate; if no, prevent the global binding from authorizing this route. This is not evidence of a failed remote security check; it is an unresolved behavior/code-contract edge in the card's shared apply path.
- Hosted state is not qualification: run [46032316692](https://github.com/mcpdev80/baseharbor/actions/runs/46032316692) is completed FAILURE on the exact head `e6425f9bf79d57dceddaedee1a07117da3d8a3b1`, event `pull_request`, branch correct. `PR · Trusted Plan` fails at “Resolve exact immutable PR inputs using trusted base policy” with `invalid trusted PR gate coverage catalog: uncataloged source change` for `cmd/baha/app_candidate_consent_interactive.go`, `cmd/baha/app_candidate_consent_test.go`, and `cmd/baha/app_remote_lifecycle.go`. `PR Selected Checks` then fails “Require complete selected Go shard coverage”: `UNIT_SCOPE` is empty, `UNIT_RESULT` is `skipped`, with `REJECT: Go test selection missing or invalid`. Thus the new tests did not execute; this run is not a receipt. Source format, workflow policy, and native gate plan succeeded, but those do not replace required test receipts. No dispatch/rerun was triggered.

## Trusted-Plan lift mechanism — corrected across the eight A candidates

The trusted catalog object already exists on develop: `scripts/pr-gate-coverage.json` is blob `792a767aaceb600f5f0da228264413333014d1a8`, 4,389 lines / 137,751 bytes (SHA-256 `4f69f085ab096c97fcdf9cd0e6726ee1fd5c61414edc11d00af139f2f0a72363`). At the exact base, `scripts/pr-gate-plan.py:1890` reads `<base>:scripts/pr-gate-coverage.json`; `:1902` loads the controller catalog; `:1944-1954` raises fail-loud for every changed `cmd/` or `internal/` source path lacking an exact catalog owner. The live failure on #1884 proves this is the same gate, not a consent test failure.

The eight A candidates in this chain are #1874, #1875, #1877, #1879, #1880, #1881, #1882, and #1884. Their changed source paths are the ones listed in the published H-V34 catalog-desk akte for #1874/#1877/#1879/#1880/#1881/#1882, plus #1884's three paths shown by run `46032316692`. A correction to H-V34: #1875 and #1877 are two open PRs touching the SAME two source paths (`cmd/baha/app_workload.go` and `cmd/baha/app_workload_runtime_identity_fallback_test.go`); they need one shared base-catalog row per exact path, not duplicate entries. Their PR-local copies of the same rows do not make either PR's Trusted Plan see the row in its base. The #1876 PR/family has a separate content defect (`runtime_specific`/test registration per the owner queue) and is not one of these eight A-catalog victims; do not count its green check rollup as a Trusted Plan lift or include it in this row batch.

Therefore “add each PR's own row and merge in arbitrary sequence” is insufficient for the first qualifying run: the controller always reads the base checkout, so a row present only in the candidate is invisible to that candidate's own Trusted Plan. A single base-side lift must first make all unique new paths in this A cohort visible to the trusted planner (or an owner-authorized planner change must explicitly validate a safe candidate catalog overlay against the trusted base). The planner/workflow are shared policy surfaces outside these card write-sets; this review does not edit them. The minimal non-code lift is one deduplicated registry update on develop containing the exact rows/surfaces for the cohort paths, followed by fresh exact-head pull_request qualification for each candidate; after that, candidates can be merged in dependency order and their same-PR catalog rows remain idempotent. Do not merge candidates before confirming each relevant path resolves in the trusted base and its required tests actually execute. Distinct component IDs are derived from unique paths; #1875/#1877 are the known duplicate-path pair and must share one canonical row per path.

For the eight A victims, the current owner-queue sequence is #1874, #1875, #1877, #1879, #1880, #1881, #1882, and #1884. The detailed H-V34 inventory names #1874, #1877, #1879, #1880, #1881, #1882, and an ungrounded #1876-family entry; card 0428-307 evidence separately confirms open #1875 with the same two source paths as #1877. Thus the evidence supports eight PR candidates, but not eight unique source-path sets; #1875/#1877 share two paths. The #1876 family has a separate content defect and is not an A-catalog victim. The trusted gate does not permit bypass: the exact needed owner/coordinator action is the trusted-base catalog/planner lift, then the normal hosted checks.

## Current evidence publication provenance

- Old local evidence attempt: the shared checkout branch at `43cf2a8ba5e8dfdea07a8d909edf839c515306d7` was not used or repaired; its tree included unrelated 0428-342 files. It remains untouched.
- Fresh isolated Plan clone remote verified before branch creation: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Fresh `origin/main` cut point: `41972b641f9b97f29dbf1aec320309d21568645b`; this is the base of the clean evidence branch and is the required base attestation for the first evidence commit.
- Isolated-clone render/check: `784 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings` (the warnings are pre-existing accepted tasks with unaccepted dependencies). The isolated clone remained limited to this akte.
- A mistaken earlier invocation called `python3 /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/scripts/plan.py render/check` against the shared checkout; `render` stopped with `ValueError: not enough values to unpack (expected 2, got 1)` in `short_ref`. The subsequent shared-checkout status showed modifications to `tasks/t-20261116-r28-bug-apply-consent-ux.md`, `tasks/t-20261125-hunt43-env-leak-disk.md`, `views/kanban-dashboard.md`, `views/overview.md`, and `views/releases/v0.4.28.md`. I did not inspect, restore, stage, or commit those paths further; their prior status is unknown, so they are left untouched for coordinator reconciliation.
- No local tests, workflow dispatch, rerun, product write, or product merge was performed in this review. The evidence branch contains only this akte.

## Cleanliness

No containers, compose projects, or test VMs were started. Product review remained read-only; Plan work is isolated from shared Plan and product worktrees.

END_BLOCKED w267-0428-284-pridentity: #1884 CHANGES; exact-head Trusted Plan 46032316692 fails on base catalog and the interactive input/remote-route review findings remain open.

## Current-base reconciliation

- Plan main advanced after the initial evidence commit from `41972b641f9b97f29dbf1aec320309d21568645b` to `cb8bf89521e891650ee8712395514b1836253f30`. The evidence branch merged that exact current `origin/main` with merge commit `b863facd7573db8a036599a70c05e8f20bc86781`, authored and committed as `w267-0428-284-pridentity`.
- Current-base proof: `git merge-base --is-ancestor origin/main HEAD` succeeded. Exact `git diff origin/main...HEAD --name-only` output: `evidence/2026-11-27/0428-codex-staticreview-pr1881-1882.md`. `git log --oneline origin/main..HEAD` lists only my evidence commit `187c239d5` and current-main merge commit `b863facd7`.
- Re-rendered and checked in the isolated clone after this merge: 784 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings.

## Follow-up disposition: 0428-315 / PR #1882

Role: REVIEW/DISPOSITION only. No product edit and no merge.

- Clarification: the live `refs/pull/1882/head` and GitHub PR API both identify `78ab390579afeb483fb1c181ad9eb11e0e317ea3` as the current head; `be410aea1ceee44163a26f7ad7eecc94b808e275` is its merge-base/earlier head, with nine descendant commits (including w400's implementation and later catalog-only updates) between them.
- Refreshed Plan `origin/main` is `66eb5f0b52958349b3e6b1667cd02026470b1d31`. The current product PR #1882 is OPEN at exact head `78ab390579afeb483fb1c181ad9eb11e0e317ea3`, based on develop `6944e8761af6f07b801f55e39bb9a5409226c10b`.
- Disposition: route (b), implementation of the cited Tempo/ObjectStorage sites, is the correct route for this card; do not narrow or retarget the Task contract. The alleged Tempo timeout divergence is not present on the reviewed base: `internal/metrics/perses_tempo_datasource.go:65-66` defines the 10s trace-query timeout and `internal/metrics/perses_tempo_verify.go:98-100` uses the same constant. Keep that value and make the shared matrix the single source of truth; do not change timeout behavior.
- ObjectStorage values have separate operation semantics and must remain distinct: `internal/objectstorage/seaweedfs.go:32-34` defines 120s reconcile, 90s readiness, and 3s existing-provider probe budgets. Only consolidate the matching reconcile budget with the matrix `OverallTimeout`; preserve readiness and probe budgets as independent values. No timeout tuning or consent/auth-gate change is authorized by this disposition.
- This route is already implemented in #1882's final content. The published `evidence/2026-11-27/0428-315/akte.md` records w400's changes at `internal/metrics/perses_tempo_datasource.go` and `internal/objectstorage/seaweedfs.go`, with the behavior-preserving matrix tests and unchanged values. The R5 exact-head review `evidence/2026-11-27/0428-315/verdict-r5-w267.md` reviewed final head `78ab390579afeb483fb1c181ad9eb11e0e317ea3` and found the content PASS after reviewing its catalog-only delta from `b61e3ab7e17f5e780d4ad37de92de4c4ece53d49`.
- Handoff to the dispatched worker: do not duplicate or extend the implementation on #1882. Preserve the current content and wait for the base-side trusted-catalog/Freeze #136 lift and required exact-head hosted qualification. The observed pair `46055456117` and `46055569861` is terminal FAILURE, with Trusted Plan/catalog and empty `UNIT_SCOPE` failures; neither run supplies test receipts. Content PASS is not CI qualification or merge approval.
- If the Owner instead elects route (a), the exact proposed Task edit is: replace the final Task sentence with “Centralize the existing CLI application-status probe timeout values in a documented matrix, and have each probe consume its matching matrix value; preserve all current durations and operation-specific budgets.” That would remove the Tempo/ObjectStorage acceptance target and is a scope change requiring the Owner's explicit approval. This review does not apply that edit.

## Follow-up publication plan

1. Fetch current Plan `main` at `66eb5f0b52958349b3e6b1667cd02026470b1d31` in a fresh isolated clone.
2. Append only this 0428-315 disposition to this existing akte; do not edit product files or task metadata.
3. Run Plan render and check; require zero errors.
4. Commit under `w267-0428-284-pridentity`, push a fresh evidence branch, open one Plan PR, and wait for terminal green Plan validation on its exact head.
5. Do not merge; report the unchanged Plan-main SHA and the PR/head/validation witness for the Coordinator.

## Follow-up commit identity and base attestation

- Plan `origin/main` before branch creation: `66eb5f0b52958349b3e6b1667cd02026470b1d31`.
- Git remote verified in the isolated clone: `origin https://github.com/mcpdev80/baseharbor-plan.git`.
- Commit author and committer identity: `w267-0428-284-pridentity` / `w267-0428-284-pridentity@baseharbor.local`.
- Commit invocation: `git -c user.name=w267-0428-284-pridentity -c user.email=w267-0428-284-pridentity@baseharbor.local commit ...`.
- Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w267-0428-284-pridentity`.
- First branch push delivery witness (`git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/w267-staticreview-followup`):

```text
4863dbd814199cf644b09437a2a60bc325a0c8df	refs/heads/w267-staticreview-followup
```

## Follow-up END

END_DONE w267-0428-284-pridentity: 0428-315 disposition is route (b), already implemented in #1882; content PASS, hosted qualification still blocked by class-A trusted-plan gate; no merge.

## Follow-up cross-validation: #1884 and #1881

Role: read-only content cross-validation; no product edits or product merges.

- #1884 live `refs/pull/1884/head` and PR API agree on `b25c192159f78b2e3ed4d49f0ea587e216f04ace`, base `6944e8761af6f07b801f55e39bb9a5409226c10b`; compare shows the prior reviewed `e6425f9bf79d57dceddaedee1a07117da3d8a3b1` is its ancestor and there are three correction commits. The consent-reader finding is superseded for the reported queued foreign-reader case: `interactiveCandidatePromptAllowed` rejects generic readers (`app_candidate_consent.go:279-305`), while the CLI wrapper is created from the terminal file (`core_installation.go:313-325`); the negative queued-reader and wrapper-preservation regressions are at `app_candidate_consent_test.go:636-710`.
- #1884 finding 2 is only partially resolved. The contradictory “display-only” assertion is removed and the remote lifecycle now explicitly calls the consent prompt before recording the deployment (`app_remote_lifecycle.go:166-176`). However, `TestRemoteApplyRouteInlineBindContractIsTruthful` at `app_candidate_consent_test.go:724-749` exercises only the non-terminal refusal path and never calls `executeRemoteApplicationApply`; its comment claims both directions, but no remote-route affirmative/success case exists. Correction recipe for w405: extend this test (or add a focused sibling) to execute the remote lifecycle with a terminal affirmative response and assert the exact candidate consent reaches the persisted deployment, while retaining the non-terminal fail-closed case and the existing admission/digest checks; do not test only the prompt/write leaves. The pair `46051642251` / `46051804829` is terminal FAILURE on exact head `b25c192159f78b2e3ed4d49f0ea587e216f04ace`; Trusted Plan fails and the unit/runtime jobs are skipped, so this remains content-test coverage CHANGES and is not CI qualification.
- #1881 live `refs/pull/1881/head` is now `2e81d55fd019c54fecc79875f21b1ba5c6fdfc33`, not the supplied board SHA `1cd5029f7149f3bc72bfce7f7ff28e662f6bddf5` or the earlier akte witness `fc510d73d…`. The current head has `1cd5029f…` as its parent and adds one commit whose only changed path is `internal/orgconfig/migration.go`; the delta routes the existing parent-directory sync through `orgconfigSyncDir` (`migration.go:148-151`), whose default remains the production `syncDir` (`:54-65`). The injected error still traverses `syncDir` and becomes `*syncDurabilityError` (`:244-260`), and the regression asserts `errors.As`, no completion marker, and retained data (`migration_marker_test.go:439-490, 494-558`). R6's content PASS therefore carries to current head `2e81d55f…`; no new content finding. The current Hosted run `46098935150` is on `2e81d55f…`, with Trusted Plan failed and downstream unit checks skipped/pending at observation; the prior successful-content verdict is not a passing hosted qualification for this new head.
- Cross-validation disposition: #1881 content PASS on current head, Hosted qualification pending; #1884 original reader finding superseded, but the remote-lifecycle regression gap remains CHANGES pending the exact test recipe above.
- Ruling at current #1884 head `b25c192159f78b2e3ed4d49f0ea587e216f04ace`: finding 2 remains CHANGES because `TestRemoteApplyRouteInlineBindContractIsTruthful` (`app_candidate_consent_test.go:724-749`) checks only non-terminal refusal and neither calls `executeRemoteApplicationApply` nor verifies a terminal `y` persists consent through the actual remote `app up` route; add that remote success-path regression while retaining the fail-closed case.
- Final disposition (Option 3): because `app_remote_up_success_discriminator_test.go:21-30` documents that unit success requires an unavailable live enrolled Connector, supersede the prior CHANGES demand for a terminal-`y` test through `executeRemoteApplicationApply`; accept the route-adjacent fail-closed write test (`app_candidate_consent_test.go:724-749`) plus the terminal-`y` one-shot consent/write-boundary test (`:355-395`) as the unit contract, and track full remote-route execution as a separate E2E evidence limitation without adding a production or test-only seam.

## Cross-validation publication plan

1. Add only this read-only cross-validation record to the existing static-review akte.
2. Run Plan render/check; require zero errors.
3. Commit and push to the existing isolated branch `w267-staticreview-followup`, then verify PR #261's new exact head and terminal Plan validation.
4. Merge only the Plan evidence PR after current-main ancestry and green exact-head validation; do not merge product PRs.

END_DONE w267-0428-284-pridentity: #1881 current head content PASS; #1884 finding 1 superseded, finding 2 CHANGES for missing remote success-path regression; no product merge.

## PLAN extension for final PR #1884 review

13. Refresh Plan main and verify PR #1884 exact head `f6ebba6ecf610cccca884c2896ee69ed70b77ca6`, exact base `6944e8761af6f07b801f55e39bb9a5409226c10`, changed-path scope, and both terminal Hosted run records.
14. Review the 100-line test-only delta against the published Option-3 disposition; inspect consent validation and admission source; record a content verdict separately from CI qualification.
15. Publish this addendum through an isolated Plan PR with render/check and terminal exact-head Plan validation; do not merge product PR #1884 while the class-A lift is held.

## Final exact-head review: PR #1884 at f6ebba6ecf610cccca884c2896ee69ed70b77ca6

### Visible commit identity block and provenance

- Reviewed card owner verbatim from task frontmatter at Plan `origin/main` `7c5f2f7e508574a2b3471c250cc83415d8af3972`: `owner: w267-0428-284-pridentity` for card 0428-284.
- Git user.name: `w267-0428-284-pridentity`.
- Git user.email: `w267-0428-284-pridentity@baseharbor.local`.
- Commit invocation for this Plan evidence change: `git -c user.name='w267-0428-284-pridentity' -c user.email='w267-0428-284-pridentity@baseharbor.local' commit -m 'review #1884 final head f6ebba6ec'`.
- Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w267-0428-284-pridentity`.
- Planning remote verified before evidence change: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Exact Plan base attestation before branch creation: `7c5f2f7e508574a2b3471c250cc83415d8af3972` (`refs/heads/main`). This base is the fetched `origin/main` tip used for this evidence PR.

### Candidate, exact diff, and contract

- Fresh GitHub witnesses: base repository `refs/heads/develop` is `6944e8761af6f07b801f55e39bb9a5409226c10b`; `refs/pull/1884/head` is `f6ebba6ecf610cccca884c2896ee69ed70b77ca6`. PR #1884 is OPEN, non-draft, base `develop`.
- Diff `b25c192159f78b2e3ed4d49f0ea587e216f04ace..f6ebba6ecf610cccca884c2896ee69ed70b77ca6`: exactly one changed path, `cmd/baha/app_candidate_consent_test.go`, 100 insertions and no deletions. No production source or coverage-catalog path changed in this delta.
- The new subtests in `TestRemoteApplyRouteInlineBindContractIsTruthful` at `cmd/baha/app_candidate_consent_test.go:747-845` exercise both terminal `n` and `y` through the prompt followed by `recordDeploymentBeforeMutation` on the same route context. The refusal asserts the consent-required error and no remaining binding. The affirmative asserts persisted operator consent, digest equality with the current candidate submission and displayed confirm-hash, no obsolete re-run instruction, and one-shot binding consumption.
- This implements the accepted Option-3 test-shape decision already published in Plan main: `executeRemoteApplicationApply` success requires a live enrolled Connector responding to NodeMemory, Publish, and ApplyApplication (`app_remote_up_success_discriminator_test.go:21-30`); no production or test-only seam was added. Full remote `app up` success remains a stated E2E evidence limitation, not a claimed unit test.
- Consent protections remain intact at unchanged source: `cmd/baha/app_candidate_consent.go:163-185` rejects empty digest without consent, derives the canonical candidate digest, and uses `delivery.ConstantTimeDigestMatch` before constructing consent. `cmd/baha/deployment_record.go:404-407` retains `EvaluateDeploymentAdmission` before write; `:532-545` finalizes and rejects missing/mismatched consent at the persistence boundary. This delta does not weaken admission or digest validation.

### Hosted qualification and verdict

- Run [46102641931](https://github.com/mcpdev80/baseharbor/actions/runs/46102641931): terminal FAILURE, event `pull_request`, exact head `f6ebba6ecf610cccca884c2896ee69ed70b77ca6`. `PR · Trusted Plan` fails because its trusted base catalog has no owners for four source paths already in the full PR diff: `cmd/baha/app_candidate_consent_interactive.go`, `cmd/baha/app_candidate_consent_test.go`, `cmd/baha/app_remote_lifecycle.go`, and `cmd/baha/core_installation.go`. `PR Selected Checks` fails with `UNIT_SCOPE:` empty, `UNIT_RESULT: skipped`, and `REJECT: Go test selection missing or invalid`. The package test job is skipped; this run provides no executed unit-test receipt.
- Run [46102724251](https://github.com/mcpdev80/baseharbor/actions/runs/46102724251): terminal FAILURE, event `pull_request`, same exact head. It has the same Trusted Plan catalog failure and downstream selected-check failure; Go unit tests and other runtime gates are skipped.
- Content verdict: PASS for the exact f6ebba6ec test delta against the accepted Option-3 disposition and the scoped consent-integrity review. Qualification verdict: NOT QUALIFIED; the required test execution and `PR Selected Checks` are not green because the Trusted Plan catalog failure leaves `UNIT_SCOPE` empty. Keep #1884 unmerged and on review until the class-A base catalog is lifted and a fresh exact-head pull_request pair executes the required tests and passes.

END_DONE w267-0428-284-pridentity: PR #1884 content PASS at f6ebba6ecf610cccca884c2896ee69ed70b77ca6; hosted qualification held on class-A Trusted Plan catalog failure; product PR not merged; Plan evidence publication pending.
