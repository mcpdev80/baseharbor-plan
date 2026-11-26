# Disposition: #1835 and #1833

## PLAN

1. Read the live task contracts for cards 0428-287 and 0428-288 and their cited evidence.
2. Refresh current product develop, both PR heads, tree-delta counts, exact check runs, and the #1842 dependency state.
3. Decide #1835 against the current develop tree, not the superseded ae709 census; separate PR redundancy from card acceptance.
4. Classify #1833's failed pre-release run by its actual event and branch, inspect current path-to-runtime selection, and prescribe the post-dependency hop and qualification pair.
5. Publish this two-PR disposition in one isolated plan PR and verify the merged evidence path.

## Owner and identity ansatz

Card 0428-287 frontmatter owner, verbatim: `owner: w185-0428-287-pr1835-podman`.

Card 0428-288 frontmatter owner, verbatim: `owner: w147-0428-288-pr1833-fix`.

Evidence branch identity: `w252-1833-1835-disposition` / `w252-1833-1835-disposition@baseharbor.local`.

Literal commit invocation: `git -c user.name='w252-1833-1835-disposition' -c user.email='w252-1833-1835-disposition@baseharbor.local' commit -m 'evidence: disposition PRs 1833 and 1835'`.

Pre-push author gate: `git show -s --format=%an HEAD` must equal `w252-1833-1835-disposition`.

Planning repository remote witness before evidence commit:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Base attestation before branch creation: `origin/main` was fetched from the verified planning remote at `7e4a414f30ae82e8f0cb1e407a68e95c690e0532`. This evidence file was drafted in a detached worktree at that exact SHA before creating the branch.

## Decision table

| PR / card | Verdict | Disposition |
| --- | --- | --- |
| #1835 / 0428-287 | Current content is redundant with develop; the PR has no reviewable payload. | Do not re-hop or path-normalization re-cut an empty delta. Recommend closing this PR as superseded. Keep the card unaccepted until the existing current-develop behavior and required Docker/rootless-Podman acceptance evidence are recorded. |
| #1833 / 0428-288 | Payload remains distinct and self-contained; the old source failure is not a PR-event failure or a payload defect. | Hold for #1842 resolution, then normal-merge current develop into the existing branch and collect two distinct successful PR-event runs on the same exact head. No merge is authorized by this disposition. |

## #1835 evidence and disposition

Live PR #1835 is OPEN at `41cda5f9ff428eed147b19b0f40668060e0db8a9`, based on `develop`. The current develop tip at census was `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`. GitHub PR metadata reports `changedFiles: 0`; REST compare `develop...41cda5f9` reports `ahead_by: 10`, `behind_by: 14`, and an empty files list. `gh pr diff --name-only` is empty. The endpoints have divergent histories but the same current tree. Therefore the older w244 census against develop `ae70964d` (318 PR test-file paths absent then) is superseded by later develop content; it is not a reason to transport or normalize a now-empty branch.

Run `45698449498` is a completed `pull_request` failure at the same head. The Trusted Plan log ends with `ValueError: no independently executable PR validation checks` from `pr-stage-boundary.py:51`. `PR Selected Checks` logged blank `UNIT_SCOPE`, `UNIT_RESULT: skipped`, then `REJECT: Go test selection missing or invalid`. With no changed files, this is the expected fail-closed result; do not invent a payload, weaken empty-diff rejection, or count the run as qualification. Earlier green runs at other heads do not establish current acceptance.

Recommendation: close #1835 as a redundant PR without merge. Do not claim card 0428-287 accepted: its contract requires red-first regression proof and actual native Docker and rootless Podman behavior evidence. The empty PR cannot produce independently selected jobs. Stop if the current tree comparison changes; if it remains empty, route card acceptance through existing executable current-develop/release evidence rather than a synthetic PR diff.

## #1833 evidence and disposition

Live PR #1833 is OPEN at `a7b0a48048c11d20234160eede941532ddc33156`, based on `develop`; current develop at census is `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`. Compare `develop...head` reports 6 commits ahead, 38 behind, and exactly these three changed files: `internal/application/manifest_validation.go`, `internal/application/workload.go`, and `internal/application/workload_test.go`. They match the card-owned payload. The current base catalog rows at `scripts/pr-gate-coverage.json:2521-2542` classify all three paths to both `source.gate.atomic.docker.data.capabilities` and `source.gate.atomic.podman.data.capabilities`; no diff-selection change is indicated. `PR · Go unit · packages` and the selected Docker runtime job executed successfully in old PR run `45513816046`, but it is stale against the current base and only the Docker data-capabilities runtime job is shown in its jobs list. It is not a current-base qualification pair.

The cited run `45571699415` is a `push` event, not a `pull_request` event. Its head branch is `validation/pre-release/selected/gates/atomic/docker/guided,atomic/docker/lifecycle,atomic/docker/policy,atomic/docker/connectivity,atomic/docker/reconciliation,atomic/docker/failure`. The Source · Candidate and Gate Plan log says `cannot build complete Pre-Release reuse plan: current run is not a pre-release dispatch/call`; Source · Qualified then fails because preparation failed. Runtime matrices are downstream and skipped. This is not an ancestry artifact, but it is also not evidence that a pull-request run invokes the pre-release reuse planner.

The independent trigger-classification mismatch is visible at `.github/workflows/pre-release.yml:2180-2184` (push triggers include `validation/pre-release/**`) and `:224-242` (the runtime-reuse step calls the helper unconditionally). `scripts/pre-release-runtime-reuse.py:104-110` admits workflow_dispatch/workflow_call, or a push whose branch is exactly `release/<tag>-current`; it rejects the observed validation/pre-release selected-gates push. This is a real release-workflow routing defect, but it is outside card 0428-288's three-file PR qualification. No workflow or helper correction is authorized inside #1833 by this disposition; route it to the workflow owner if that release-push path is still required. Do not count run 45571699415 as either PR-event receipt.

## #1833 worker recipe and stop criteria

1. Do not hop while #1842 remains OPEN. First resolve and normally merge #1842; verify the resulting develop contains its approved demo-pin update.
2. In the existing `lane-0428-288-compose-ids` branch, fetch the then-current real GitHub `develop` and merge that ref normally. Do not rebase, reset, force-push, or create another candidate branch.
3. Before pushing, prove the fetched develop tip is an ancestor of HEAD. `git diff <github-remote>/develop...HEAD --name-only` must list only the three payload paths recorded above; inspect `git log --oneline <github-remote>/develop..HEAD` for only card-owned commits. Stop on conflicts, unrelated paths, changed ownership, or missing current catalog rows; report exact file and line instead of broadening scope.
4. Let the normal push create the first `pull_request` run. Require terminal SUCCESS on the exact resulting SHA with PR Trusted Plan, PR Selected Checks, package/unit coverage, and both selected runtime jobs actually executed and successful: Docker data-capabilities and rootless Podman data-capabilities. The current catalog rows should make both surfaces selectable; skipped or reuse-only runtime jobs do not pass.
5. Only after the first qualifying success, trigger the second distinct run using the mission-authorized atomic sequence: `gh pr close 1833 --repo mcpdev80/baseharbor --comment 'second exact-head hosted run trigger (coordinator-authorized)' && gh pr reopen 1833 --repo mcpdev80/baseharbor`. Confirm the PR is open and not draft. Require a second distinct run ID, event `pull_request`, same exact SHA, terminal SUCCESS, and per-page-100 jobs showing the same required jobs actually executed. A rerun or run-attempt increment is not the second receipt.
6. Stop without merging after the pair. Re-review and merge decisions are outside this mission.

If a refreshed PR run shows a missing Podman selection despite current catalog rows, report the exact `scripts/pr-gate-coverage.json` row and `scripts/pr-gate-plan.py` selection result before changing anything. If the validation/pre-release push failure recurs, report it as the separate workflow state above; do not use it as a PR-event receipt or silently add `.github/**` changes.

## Exact old-run witnesses

`gh run view 45698449498 --repo mcpdev80/baseharbor --json headSha,event,status,conclusion,url`: head `41cda5f9ff428eed147b19b0f40668060e0db8a9`, event `pull_request`, completed, failure.

`gh run view 45571699415 --repo mcpdev80/baseharbor --json event,headBranch,headSha,workflowName`: event `push`, head `a7b0a48048c11d20234160eede941532ddc33156`, workflow `Release · Pre-Release Validation`, branch `validation/pre-release/selected/gates/atomic/docker/guided,atomic/docker/lifecycle,atomic/docker/policy,atomic/docker/connectivity,atomic/docker/reconciliation,atomic/docker/failure`.

`gh run view 45513816046 --repo mcpdev80/baseharbor --json headSha,event,status,conclusion,url`: exact old #1833 head `a7b0a48048c11d20234160eede941532ddc33156`, event `pull_request`, completed, success; this does not satisfy the new-base pair.

`gh pr view 1842 --repo mcpdev80/baseharbor --json state,headRefOid,mergeCommit,url`: state OPEN, head `5d9965944ff6cd265cbd5d042d59cf522b38b76d`, no merge commit. Therefore the dependent hop must wait.

## Cleanliness and handoff

No local tests, containers, compose projects, or workflow runs were started. No product files or workflow files were edited. No product PR was merged by this review.

END_DONE w252-1833-1835-disposition: #1835 is redundant at the current tree and remains unaccepted pending behavior evidence; #1833 waits for #1842 then current-base hop and two distinct same-head PR successes.

## Branch provenance and superseded local attempt

The first isolated worktree was created detached at the then-fetched `origin/main` SHA `7e4a414f30ae82e8f0cb1e407a68e95c690e0532`; first local evidence commit was `57df17405dc9fc9e164d4c02a9338b31e2f333c1`. Before any push, a fresh ls-remote showed live `main` had moved to `12bff4d805c0ffbaddf4cd037a45b60460c05864`, and `7e4a414` was not an ancestor of it. The local branch was not pushed. To correct provenance without carrying other commits, only the single lane-authored evidence commit was rebased in the isolated worktree with `git rebase --onto origin/main 7e4a414f30ae82e8f0cb1e407a68e95c690e0532 codex/w252-1833-1835-disposition-20261126`. New local HEAD is `4b74526b23eb4e979fbc1f24166a932cddf65474`, author `w252-1833-1835-disposition`, committer `w248-coordinator`. The author admission field is the exact canonical lane name. Superseded local-only commit `57df17405dc9fc9e164d4c02a9338b31e2f333c1` is recorded here and was never pushed.

Post-rebase provenance commands:

```text
git merge-base --is-ancestor origin/main HEAD -> success
git diff origin/main...HEAD --name-only -> evidence/r28-welle6-2026-11-26/w252-1833-1835-disposition/disposition.md
git log --oneline origin/main..HEAD -> 4b74526b2 evidence: disposition PRs 1833 and 1835
git show -s --format=%an HEAD -> w252-1833-1835-disposition
```

No foreign commits are carried on the corrected evidence branch.


## Plan publication

This akte is carried by plan PR #56 from branch `codex/w252-1833-1835-disposition-20261126`. The first `Plan · validate` run was `45728090670` and passed at head `0aeba0a037dbd181efa581519a11e94d68c1a36a`; a new validation is required for this final evidence-only amendment. The product PRs #1833 and #1835 remain unmerged.

## Superseded plan branch attempt and re-land record

Plan PR #56 is marked MERGED with squash commit `f551ef1f307c5d35ed3351201b985fbb3043dcf5`, but the merged evidence is absent from live `origin/main`; therefore the PR merge state alone is not accepted as publication proof. The PR record and `refs/pull/56/head` remain the audit trail and will not be deleted. Superseded branch attempts: initial base `7e4a414f30ae82e8f0cb1e407a68e95c690e0532`; refreshed base `12bff4d805c0ffbaddf4cd037a45b60460c05864`; original local commit `57df17405dc9fc9e164d4c02a9338b31e2f333c1`; rebased commit `4b74526b23eb4e979fbc1f24166a932cddf65474`; evidence update commit `0aeba0a037dbd181efa581519a11e94d68c1a36a`; final PR #56 head `27f18c7f3f187b3cc9732d337a2c5d3157f1dd36`; merge commit `f551ef1f307c5d35ed3351201b985fbb3043dcf5`.

The first recovery tip `1a21dd3eebe93a5442383bfa08f050060e2bb974` was superseded before any commit or push: the replacement branch had been created there but contained no candidate commit. A subsequent direct `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` witness advanced to `7e9f37fd136bc33672c9aa84f3c7380c066a82dd`. This is the current cut SHA recorded before recreating the same branch name. The merge commit `f551ef1` is not an ancestor of the previous live main, and the evidence path was absent there. The branch ref for merged PR #56 is absent while its PR record and `refs/pull/56/head` remain intact. Re-land only this evidence file from the fresh `7e9f37f` main; no product files, other evidence, or foreign commits are carried. No force-push or main-branch write is used.
