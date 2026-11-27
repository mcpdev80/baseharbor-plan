# PR #1876 exact-head review evidence

## PLAN

1. Verify PR #1876 remote head/base and the card 0428-307 scope; record exact remotes and current Plan base.
2. Review the full diff against develop and verify the only edits are runtime-identity catalog/registration entries for the source and its regression test; inspect gate selection and confirm no workflow, production auth, or consent changes.
3. Verify exact-head Hosted checks and collect two distinct completed run IDs on the same head using the authorized close+reopen trigger.
4. Verify whether task 0428-307 links PR #1876 in its `prs` field; do not change the task card in this review.
5. If all required exact-head gates pass, merge normally with expected-head guard; otherwise record a concrete repair recipe for w397 and do not merge.
6. Record the verdict, both run IDs, changed paths, merge SHA or repair recipe, and publish this evidence through the Plan repository PR path.

## Visible commit identity block

- Exact task frontmatter owner, verbatim from Plan origin/main: `owner: w397-0428-307-idfallback`.
- Reviewer lane / Git `user.name`: `w267-0428-284-pridentity`.
- Git `user.email`: `w267-0428-284-pridentity@baseharbor.local`.
- Literal commit invocation: `git -c user.name=w267-0428-284-pridentity -c user.email=w267-0428-284-pridentity@baseharbor.local commit ...`.
- Pre-push identity gate: `git show -s --format=%an HEAD` must equal `w267-0428-284-pridentity`.

## Plan base attestation

- Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`; `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Exact Plan `refs/heads/main` SHA before this evidence branch: `798967d569a6ccd118ed14dbd8d50e4b60215f69`.
- Evidence branch base: `798967d569a6ccd118ed14dbd8d50e4b60215f69`; the evidence and identity block were recorded before creating the evidence branch.

## Product PR and base witnesses

- PR: https://github.com/mcpdev80/baseharbor/pull/1876
- Branch: `lane-0428-307-ci-catalog`.
- Exact PR head: `98cb8a725ac78e56959ead4dd6b7757ebabde856`.
- Exact PR base: `develop` at `ea5218d72e263f21e79853b679af50074dab8c25`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1876/head` returned the exact base and head above.
- PR state at final review: open, mergeable, `mergeStateStatus=CLEAN`; head remained stable.
- PR changed-path API reports only `scripts/pr-gate-coverage.json` (16 additions, 0 deletions). Full diff contains two catalog registrations: `cmd/baha/app_workload.go` and `cmd/baha/app_workload_runtime_identity_fallback_test.go`, both mapped to Docker and Podman `data.capabilities` surfaces. No `.github/**`, product authorization, or consent files changed.

## Hosted exact-head receipts

- Run `45993371732`: event `pull_request`, completed/success, exact head `98cb8a725ac78e56959ead4dd6b7757ebabde856`; `PR Selected Checks` check-run `140487251948` completed/success; `PR · Native gate plan` `140486554570` completed/success; `PR · Validation · pr-planner-tests` `140486638207` completed/success.
- The authorized second trigger was `gh pr close 1876 --comment 'second exact-head hosted run trigger (coordinator-authorized)' && gh pr reopen 1876`.
- Run `45996668742`: distinct event `pull_request`, completed/success, the same exact head; `PR Selected Checks` check-run `140498424289` completed/success; `PR · Native gate plan` `140497661102` completed/success; `PR · Validation · pr-planner-tests` `140497774541` completed/success.
- Both runs contain other jobs marked `skipped`; these are not counted as passes. The applicable selected aggregate and catalog/planner validation jobs executed and passed on both exact-head runs.

## Independent review findings

- Review identity: `w267-0428-284-pridentity` (Codex review lane).
- Scope: the only changed file is the catalog; no workflow, auth, or consent changes are present.
- Blocking finding: `scripts/pr-gate-coverage.json:1723-1728` registers `cmd/baha/app_workload_runtime_identity_fallback_test.go`, but GitHub Contents API returned 404 for that path at both `develop` and PR head `98cb8a725ac78e56959ead4dd6b7757ebabde856`. The PR therefore registers a regression-test source that is not in the candidate tree. The code change is catalog-only; no regression test is actually included or executed by this PR.
- Blocking finding: the only candidate commit `98cb8a725ac78e56959ead4dd6b7757ebabde856` has author and committer `w358-0428-291-1864hop` (`w358-0428-291-1864hop@users.noreply.github.com`), while task 0428-307 frontmatter owner is `w397-0428-307-idfallback`. This fails the canonical candidate-identity rule; no amend, force-push, or cherry-pick was attempted.
- Planning mapping finding: task 0428-307 at Plan main `798967d569a6ccd118ed14dbd8d50e4b60215f69` has `prs: []`; mission scope forbids this review session from editing the task card, so this remains a report-only discrepancy.
- Disposition: FAIL / HOLD; PR #1876 was not merged.
- Repair recipe for w397: stop transport on the current head and ask the Coordinator to authorize a clean candidate reissue because the existing commit is foreign-authored and cannot be corrected without rewriting history. In that authorized candidate, include the actual regression test file and ensure the catalog entry points to the exact existing path; keep changes within the task's runtime-identity scope and verify the selected gate executes the test. Do not amend, force-push, or cherry-pick this current commit. Card `prs` metadata needs a separate authorized Plan update.

## Repo-rule compliance

- No tests were run locally; Hosted CI was the verification venue.
- No workflow file, product file, task card, or PR content was edited by this review.
- No containers or compose projects were started.
- Evidence contains no Markdown checkbox lines.

## Cleanliness

- Before/after `docker ps -a`: header only, no containers. No compose projects started.

## Git diff, commit, and second-run verification

- Canonical product checkout remotes resolved to GitHub `https://github.com/mcpdev80/baseharbor.git`; `origin` is the GitHub fetch/push remote.
- Fetched PR head and exact base from that remote. `git merge-base --is-ancestor ea5218d72e263f21e79853b679af50074dab8c25 refs/remotes/origin/pr1876` succeeded.
- `git diff ea5218d72e263f21e79853b679af50074dab8c25...refs/remotes/origin/pr1876 --name-only` output: `scripts/pr-gate-coverage.json`.
- Diff stat: `scripts/pr-gate-coverage.json | 16 ++++++++++++++++` (16 insertions, 0 deletions).
- GitHub API confirms `cmd/baha/app_workload.go` exists at develop (blob `4128ed067a5da464d51c9523fcd10113f8ccdbdc`). GitHub Contents API returns 404 for `cmd/baha/app_workload_runtime_identity_fallback_test.go` at both develop and exact PR head. The mapping at `scripts/pr-gate-coverage.json:1723-1728` is therefore dangling.
- Commit `98cb8a725ac78e56959ead4dd6b7757ebabde856` has author `w358-0428-291-1864hop <w358-0428-291-1864hop@users.noreply.github.com>` and the same committer. Task 0428-307's owner is `w397-0428-307-idfallback`; this is not the authorized lane identity.
- Second exact-head run `45996668742` is distinct from `45993371732`; both `PR Selected Checks`, `PR · Native gate plan`, and `PR · Validation · pr-planner-tests` completed successfully on the same head. Other workflow jobs are listed as skipped and are not treated as passes.
- Task 0428-307 `prs` is empty at Plan main `798967d569a6ccd118ed14dbd8d50e4b60215f69`; no Planning card was edited, per mission.
- `docker ps -a` witness after review: shell PID `1335474`; output contained only the header and no containers.

## Final disposition

- Check 1, exact head and two distinct terminal runs: YES. Both runs are completed/success and exact-head `PR Selected Checks` passed.
- Check 2, allowed write scope and test registration: PARTIAL. Only the allowed catalog file changed, with no workflow/auth/consent changes; the referenced test file is absent from the candidate.
- Check 3, task 0428-307 `prs` links #1876: NO. It remains empty; this review did not edit the card.
- Merge decision: NO. The dangling regression-test registration and foreign author/committer identity block acceptance. PR remains open; no merge, amend, force-push, or cherry-pick was performed.
- Repair recipe delivered to w397: the current foreign-authored commit cannot be accepted or rewritten under this review. Stop and obtain Coordinator authorization for a clean reissue; include the actual runtime-identity regression test and an accurate catalog path in that candidate, authored under `w397-0428-307-idfallback`. Do not amend or force-push this head. Handle the missing card PR link in a separate authorized Plan update.

## END BLOCKED

PR #1876 remains open and unmerged. Repair recipe was sent to w397 session `1b636609-51a5-43e4-bb8f-9b9253678635`. Blocking findings: absent regression test at `scripts/pr-gate-coverage.json:1723-1728` and commit identity mismatch (`w358-0428-291-1864hop` vs expected `w397-0428-307-idfallback`). Exact candidate head: `98cb8a725ac78e56959ead4dd6b7757ebabde856`.

## Evidence validation and cleanliness

- Fresh Plan `origin/main` SHA at evidence-branch creation: `798967d569a6ccd118ed14dbd8d50e4b60215f69`.
- `git merge-base --is-ancestor origin/main HEAD` succeeded; before the evidence commit, `git diff origin/main...HEAD --name-only` and `git log --oneline origin/main..HEAD` were empty.
- `python3 scripts/plan.py render && python3 scripts/plan.py check`: 784 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings (historical accepted v0.4.27 dependency warnings).
- Evidence checkbox scan and `git diff --check`: clean.
- `docker ps -a` before and after: shell PID `1344420`; both outputs contained only the header and no containers. No compose project was started.
