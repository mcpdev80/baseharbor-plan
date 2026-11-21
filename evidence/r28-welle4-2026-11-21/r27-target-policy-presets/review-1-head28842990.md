# CODEX-REVIEW — 0427-186 / PR #1588

Candidate: `28842990d8fe86cc9090b1867c6b503b57adccdc`
Verdict: REQUEST CHANGES

## PLAN

1. Verify exact remote head, develop base, diff, commit identities, and terminal hosted run.
2. Trace deployment policy fields, provenance construction, policy edit path, and remote apply admission.
3. Check paired policy-edit tests and inspect exact hosted CLI and documentation-audit job logs.
4. Record findings with file-level repair recipes, repository-rule compliance, and cleanliness evidence.
5. Render/check Planning, publish this evidence file to Planning origin/main, and verify its remote path.

## Remote and candidate provenance

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1588/head` returned `d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3 refs/heads/develop` and `28842990d8fe86cc9090b1867c6b503b57adccdc refs/pull/1588/head`.
- `gh pr view 1588` reports OPEN, non-draft, base `develop`, head `28842990d8fe86cc9090b1867c6b503b57adccdc`, merge state CLEAN; ancestry reports back=0, ahead=3, no merge commits.
- Diff: `cmd/baha/app_remote_lifecycle.go`, `cmd/baha/deployment_record.go`, `cmd/baha/machine_coverage.go`, `cmd/baha/target_deployment_policy_edit_b_test.go`, `docs/reference/cli-machine-coverage.md`, `internal/deployment/immutable_provenance.go`, `internal/deployment/immutable_provenance_test.go` (+371/-6).
- All three commits have author and committer `Marcel Pfingstgräf`: `28c582ff11c4247244b575ae2882289b5516bab1`, `f360d72c80cceffc0c9909ce8cfa24569ab3ea8d`, and `28842990d8fe86cc9090b1867c6b503b57adccdc`.

## Findings

- BLOCKING — a production policy can create its own approval evidence. `internal/deployment/immutable_provenance.go:91-95` defines `ConfirmApproved` as binding the operator-authorization flag, but `:125-133` invokes it solely when `requireApproval` is true. `cmd/baha/deployment_record.go:414-418` and `cmd/baha/app_remote_lifecycle.go:95-100` pass the policy's `RequireApproval` bit, not a verified consent. The actual candidate consent is finalized and validated later in `cmd/baha/deployment_record.go:553-576`, after `recordDeploymentBeforeMutation` already calls `EvaluateDeploymentAdmission` at lines 427-430. The available owner-pattern does a separate authorization and approval check, for example `cmd/baha/machine_http_executor_lifecycle.go:488-493` and `cmd/baha/mcp_control_plane_tools.go:99-104,119-123`. Recipe: verify the genuine candidate consent/operator authorization before admission, bind it to the candidate and operation, and pass that verified result to provenance construction; never derive approval from the policy bit. Add a fail-first test with `RequireApproval=true`, all other required proof satisfied, and no verified consent, asserting admission rejects. At the exact current head that regression must fail because the helper sets `approvalVerified=true` and the policy-only evidence is accepted; the existing `TestAdmissionEvidenceForRemoteApplyBindsApproval` is not proof of this because the production preset also has an allowlisted branch while the helper leaves `Branch` empty, so its expected error can come from the branch check. Stop until the test is red before the fix and green after it. This is the first and independent merge blocker.
- BLOCKING — the new provenance adapter also manufactures other old admission facts instead of deriving them from independently verified values. `internal/deployment/target_deployment_policy_admission.go:12-20` contains the existing private admission fields (`sourceVerified`, `branch`, `dirty`, `commitVerified`, `remoteCommitVerified`, `imageDigestVerified`, `approvalVerified`). The new `internal/deployment/immutable_provenance.go:59-88` sets them from a caller-supplied boolean and non-empty strings: repository input asserts clean tree, verified commit, and verified remote without checking a commit, worktree, or remote; OCI input asserts verified image digest from a non-empty digest string. The identity check at lines 63-65 also accepts either missing application ID because it rejects only when both are non-empty and unequal. This changes the trust boundary: restrictive policies can consume assertions not bound to the exact current candidate. Recipe: accept a Core-owned, typed verification result bound to the current candidate and exact non-empty application identity; populate each proof field only from the corresponding verification result. Add negative tests for absent/mismatched IDs, dirty source, unverified remote commit, and OCI digest that is merely present. Stop until forged or incomplete source data cannot satisfy restrictive policy.
- BLOCKING — branch-restricted presets cannot admit repository candidates because the new repository path never populates `ImmutableProvenance.Branch` (`internal/deployment/immutable_provenance.go:71-76`), while the evaluator rejects an empty branch for any non-empty allowlist (`internal/deployment/target_deployment_policy_admission.go:44-47`). `test`, `staging`, and `production` presets all configure branch allowlists (`internal/deployment/target_deployment_policy.go:31-46`). Recipe: bind a Core-verified branch to the exact verified candidate and add positive and negative admission tests for relevant presets; stop while valid allowed branches are always denied or an unverified branch can pass.
- BLOCKING — an apply can use a stale Target policy snapshot if policy changes after resolution. `cmd/baha/target_deployment_policy_edit.go:98-100,164-167` uses expected-version persistence for the edit, but `cmd/baha/app_remote_lifecycle.go:95-100` evaluates the already-resolved `resolved.Target.DeploymentPolicy` and does not reload/compare policy generation at the admission boundary. I found no test that edits/tightens the preset between resolution and admission. A concurrent edit can therefore leave an in-flight apply evaluated against the old policy without identifying that result as stale. Recipe: re-read the owner-authoritative Target policy at the final admission boundary or carry and compare an immutable policy revision; add a race regression that tightens policy after initial resolution and proves no runtime effect is admitted under the stale value. Stop until the test demonstrates fail-closed behavior.

## Immutable fields and edit directions

- The Target policy contains `AllowedBranches`, `AllowDirty`, `RequireCommit`, `RequireRemoteCommit`, `RequireApproval`, and `RequireImageDigest` in `internal/deployment/target_deployment_policy.go:13-20`. These are deliberately editable policy values, not deployment-source identity fields. The target edit code changes only `current.DeploymentPolicy` and saves with the expected config version (`cmd/baha/target_deployment_policy_edit.go:123-167`); it does not rewrite deployment source/commit/digest records. The critical change is that new code fills the previously Core-owned admission evidence fields above with synthetic claims.
- A paired positive/negative edit direction exists. `TestExistingTargetPolicyPreservesOverridesAndCoreBinding` in `cmd/baha/target_deployment_policy_edit_test.go` covers an allowed local policy edit and binding preservation; `TestRemoteTargetPolicyEditRefusesLocalSubstitution` in `cmd/baha/target_deployment_policy_edit_b_test.go` covers refusal of a local edit for a remote Target. The same `_b_` file also verifies local production policy persistence without changing tenant/runtime/access binding. Invalid local policy edits are covered by `TestExistingTargetPolicyInvalidEditCannotMutate`.
- The remote edit path correctly refuses workstation-local substitution, but the accepted task still requires an authorized Core mutation route before claiming remote policy edit support. The edited-between-resolution-and-admission race above has no regression case.

## Hosted checks and receipts

- Exact run `44945612280` targets this head and completed success: 42 jobs, 25 success, 17 skipped, 0 failures. `PR Selected Checks` completed success. Skipped jobs are not passes.
- The CLI tests are reachable through `PR · Go unit · cli-0..cli-3` for this PR path. Those jobs log shard aggregates (`PASS cli-N: ...`) but not individual policy-edit test names or per-case duration. This is an open item, owner-scope receipt-tooling; the candidate is already REQUEST CHANGES for candidate-owned provenance/admission defects.
- No CI job semantically isolates the approval invariant. Although the packages cell executes `TestAdmissionEvidenceForRemoteApplyBindsApproval`, its use of the production preset also triggers the empty-branch rejection, so it does not prove that approval is independently verified. The corrected fail-first regression belongs in the existing deployment-package-tests mapping and should be reached on the PR trigger for `internal/deployment/**`.
- `PR · Validation · documentation-audit`, job `136972201579`, completed success. Its log records EN/DE coverage OK for 172 matched Markdown pages, 6 audit tests in 2.151s, and `Documentation audit`; this job covered the changed `docs/reference/cli-machine-coverage.md` and `cmd/baha/machine_coverage.go` paths.
- Selected runtime cell `PR · Selected Runtime (atomic/docker/lifecycle, docker, lifecycle) / Executed docker · lifecycle`, job `136972600634`, completed success at `2026-11-21T20:26:48Z`.
- Trusted plan artifact `pr-plan.json` SHA-256: `fed0737e5e8c4cc969df36d711fe8593ea4f1e5eb8a8b46a36661c7713c778b8`. It targets the exact head and base, records `fallback_used:true`, and selects broad required unit/vet/build checks plus deployment, docs, and lifecycle validation.

## repo-rule compliance

- Reviewer-only and read-only against GitHub candidate state. No product files, `.github/**`, or `scripts/**` were changed; no product push, merge, workflow dispatch, or local suite test was run; no credential files were read.
- Planning repository remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- Evidence path: `baseharbor-plan/evidence/r28-welle4-2026-11-21/r27-target-policy-presets/review-1-head28842990.md`.

## cleanliness

- PID 1 docker snapshot before this review: 8 exited `bh-itest-*` containers listed; no container started/stopped by this review.
- PID 1 docker snapshot after this review: same 8 exited `bh-itest-*` containers; before/after state matched.

## END codex-rev-1747 DONE

Review completed. Verdict remains REQUEST CHANGES because the candidate overstates Core provenance and approval, leaves branch-restricted presets without verified branch evidence, and has no stale-policy race guard/test.

approval: self-satisfying | core-verified

## Planning publication witness

- Review evidence commit `246616fa71db3694793383f3cc9bda9cf89b276f` was delivered to `https://github.com/mcpdev80/baseharbor-plan.git` `refs/heads/main`.
- Exact output of `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle4-2026-11-21/r27-target-policy-presets/review-1-head28842990.md`:

```text
evidence/r28-welle4-2026-11-21/r27-target-policy-presets/review-1-head28842990.md
```
