# 0428-284 closure evidence

## PLAN

1. Confirm exact card owner, live Plan base, #105 merge, and the #1858 merge and hosted evidence.
2. Close task 0428-284 by changing only the task status, resolution, and HTTPS evidence fields; do not hand-edit generated tags or the checkbox line.
3. Regenerate derived Plan views and run the requested Plan check in a clean `/var/tmp` clone.
4. Review the source diff and generated output, commit with the lane identity below, verify authorship, and push the single scoped branch.
5. Create one Plan PR, verify exact-head Hosted Plan validation, record the review verdict before merge, then merge only after all required gates pass.
6. Read back the task and evidence blobs from current main and record the squash merge witness.

## Visible commit identity and base attestation

Task frontmatter owner copied verbatim from `origin/main` at runtime: `w198-0428-284-demo-parser`.

Base source: `https://github.com/mcpdev80/baseharbor-plan.git`, `refs/heads/main` at `be672c215fc699fdaeffc44a8d8f7995087d42aa` (`git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`). The checkout remote mapping witness was: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.

Commit identity: `w255-0428-251-demo170codex <w255-0428-251-demo170codex@baseharbor.local>`.

Literal commit invocation: `git -c user.name='w255-0428-251-demo170codex' -c user.email='w255-0428-251-demo170codex@baseharbor.local' commit -m 'w255 close card 0428-284'`.

Pre-push identity gate: `git show -s --format=%an HEAD` must print exactly `w255-0428-251-demo170codex`.

## Scope and evidence

This is a planning-only status closure for existing task `t-20261125-0428-284-1812-postretry-gate-failure`. Its exact owner remains unchanged. The basis is the completed clean successor PR #1858; #1856 remains a lineage audit and was not merged. Product PR #1650 remains open at head `37c4d847c`.

Evidence to preserve in the task metadata:

- PR #1858 merged at `2026-11-26T06:10:07Z` as `b7855f78a0253b9423e07da6ae92009b8f0fd1ae`, with parents `e176a276b2f545e6a555e58997817d8c08570da8` and `a7c7998d31bf5dc2828c3335374e96c47c21b70f`.
- Distinct exact-head `pull_request` runs `45764487288` and `45765519379`, both attempt 1, completed success on unchanged head `a7c7998d31bf5dc2828c3335374e96c47c21b70f`. Each run had 40 jobs: 21 success and 19 skipped, zero failures. `PR Selected Checks` succeeded in both runs; `PR · Exact Candidate` was skipped by the `runtime_required` condition at `ci.yml:1178`.
- ACCEPT comment `7184013952`; REVIEW+MERGE comment `7184154327` preceded the merge.
- Develop push workflows `Runtime Docker` run `45766329247` and `Runtime Podman` run `45766329222` both concluded success for merge head `b7855f78a0253b9423e07da6ae92009b8f0fd1ae`.
- The `_demo_repo` sentinel regression was added on #1858 head `a7c7998d3`; its execution witness will be recorded from the hosted focused-Python job logs.
- #1858 is the clean successor of #1856 (audit head `67457cdb3`, never merged); #1650 remains open at `37c4d847c`.

## Validation and publication record

To be completed with the clean-clone renderer/check output, exact Plan PR head and Hosted validation run, review comment/review record, squash merge metadata, and post-merge blob readback.

Hosted focused-Python job `139725464802` in run `45765519379` completed success. The exact PR diff contains both `test_demo_pin_leaves_checkout_untouched_sentinel_survives` and `test_demo_pin_leaves_preexisting_checkout_demo_repo_untouched`; the latter pre-creates `_demo_repo/inner/KEEP.txt` and asserts the sentinel remains unchanged. Both tests are in `scripts/test_pr_check_runner.py`.

The Docker and Podman develop push workflows each have overall conclusion `success` on merge SHA `b7855f78a0253b9423e07da6ae92009b8f0fd1ae` (run metadata names: `Runtime · Docker Core · develop` and `Runtime · Podman Core · develop`). The closure cites those workflow runs as assigned. Their job-level records are workflow-selected: in the Docker run `docker-runtime` was skipped and in the Podman run `podman-quadlet` was skipped; the executed job in each workflow was the successful native impact selector. This distinction is preserved here rather than implying those child jobs executed.

The live tree has no `scripts/card-status.py`; the supported repository interface is task frontmatter plus `python3 scripts/plan.py render` and `python3 scripts/plan.py check`. I changed `kanban_status`, `resolution`, HTTPS evidence, and the PR reference only; the renderer produced the checked card line and closed tags. The existing owner `w198-0428-284-demo-parser` and task ID are unchanged.

The accepted scope is recorded as the six-file #1858 candidate: the v0.4.28 Demo pin location, validation and fixtures, with the v0.4.27 active release criteria relocated without removal. Exact-head pair `45764487288` and `45765519379` both ran on `a7c7998d31bf5dc2828c3335374e96c47c21b70f`, each attempt 1 and success; each had 40 jobs with 21 success and 19 skipped, and `PR Selected Checks` succeeded. The `PR · Exact Candidate` skip is the `runtime_required` conditional in `ci.yml:1178` and the trusted plan selected no runtime gates for this workflow/scripts candidate. The focused Python job `139725464802` passed the candidate's pre-existing `_demo_repo` preservation test, which seeds `_demo_repo/inner/KEEP.txt` and checks it remains unchanged; the diff also adds the checkout sentinel regression `test_demo_pin_leaves_checkout_untouched_sentinel_survives`.

## Clean-clone Plan validation

A fresh clone at `/var/tmp/w255-0428-251-284-check` was given the card and akte source changes. `python3 scripts/plan.py render` produced matching generated files in the candidate worktree and clean clone: `releases/v0.4.28.md`, `roadmap/cards.md`, `tasks/t-20261116-r28-bug-compose-service-ids.md` generated card block, `views/overview.md`, `views/kanban-dashboard.md`, and `views/releases/v0.4.28.md`. `python3 scripts/plan.py check` reported `785 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings`. The ten warnings are the existing accepted-dependency warnings listed by the check; none was introduced by this change.

## Related batch completion: #104

The nine-blob consolidation candidate #104 was accepted and squash-merged as Plan main commit `44168d2d3cb5f11b1ac7c5d3f621d4644677b8aa` at `2026-11-26T07:49:38Z`. The exact candidate head `15ec0864eedd1bca54a9e55350db753642ff7422` passed Plan validation run `45776278633`; the only intervening main additions were two evidence akte files from separately green exact-head PRs #105 and #108. Post-merge main contains all nine #93 log blobs with the same blob IDs as `refs/pull/93/head`; it contains the canonical dated w291 path and not the placeholder path. PRs #93, #94, and #95 were closed after these witnesses at 07:50Z.

The closure branch was fast-forwarded from its initially attested base `be672c215fc699fdaeffc44a8d8f7995087d42aa` to live `origin/main` `44168d2d3cb5f11b1ac7c5d3f621d4644677b8aa` before its first content commit. The refreshed main delta consisted of #104's evidence artifacts; the 0428-284 task itself had no concurrent edits since the prior task edit at `72f2c83aa8`.

## Candidate provenance before publication

Candidate source commit `370d6ac6f2` reports `w255-0428-251-demo170codex w255-0428-251-demo170codex` from `git show -s --format='%an %cn %s' HEAD`. Before the publication-record commit, `git merge-base --is-ancestor origin/main HEAD` succeeded with live origin/main at `44168d2d3cb5f11b1ac7c5d3f621d4644677b8aa`; `git log --oneline origin/main..HEAD` listed only `370d6ac6f2 w255 close card 0428-284`. The scoped name-only candidate diff is:

- `evidence/2026-11-26/w255-0428-251-284-close/akte.md`
- `releases/v0.4.28.md`
- `roadmap/cards.md`
- `tasks/t-20261116-r28-bug-compose-service-ids.md` (generated card display only)
- `tasks/t-20261125-0428-284-1812-postretry-gate-failure.md`
- `views/kanban-dashboard.md`
- `views/overview.md`
- `views/releases/v0.4.28.md`

The task ID and owner fields are unchanged. The additional commit records the publication witnesses and uses the same lane identity.

## First branch delivery witness

The first normal push delivered commit `ac1f100d0d4f2ff255515b86a1e32e4f1bb66834`; direct GitHub transport witness from `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/w255-0428-251-284-close` was `ac1f100d0d4f2ff255515b86a1e32e4f1bb66834 refs/heads/w255-0428-251-284-close`.

## Pull-request ref delivery witness

After PR #111 was opened on head `dd37bf6eda6bbe4e49afe0361644b88c7ff62a65`, `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/pull/111/head refs/heads/w255-0428-251-284-close` returned:

`dd37bf6eda6bbe4e49afe0361644b88c7ff62a65 refs/pull/111/head`

`dd37bf6eda6bbe4e49afe0361644b88c7ff62a65 refs/heads/w255-0428-251-284-close`

Hosted run `45779132358` completed SUCCESS on this exact head. The next forward commit records these post-push transport witnesses; final acceptance will use the new exact-head Hosted Plan validation after that commit.

## Current publication hold

END_BLOCKED — PR #111 is open at the closure candidate; the owner freeze on additional plan merges is in effect until the direct-main provenance deviation akte lands. The pre-freeze review/merge record is preserved for audit but does not authorize a merge during this hold. The 0428-284 closure is not yet published on main.


## PLAN addendum: provenance freeze release and 0428-284 closure

1. Read PR #113 at its frozen exact head and independently check each of its five claims against GitHub commit, compare, and workflow APIs.
2. Include the lane-suffix versus commit-identity mismatch as a mechanical admission-rule finding; accept #113 only if the factual claims and exact-head validation pass.
3. Post both the review comment and COMMENTED review record before a normal squash merge; verify the squash landing by mergedAt, mergeCommit, and blob equality.
4. Recheck that #113's akte is present on live main, then recheck PR #111's exact head, hosted Plan validation, mergeability, and current-main ancestry.
5. Merge #111 only after the deviation record is verified in main and the owner freeze is thereby lifted; record merge metadata and post-merge task/akte blob witnesses.

## #113 deviation review and #111 refresh

PR #113 was reviewed at frozen head `106f829b12d6bc0a38ab81c44d1d85c87c621878`. Its exact-head Plan validation was run `45782065086`, pull_request event, attempt 1, completed SUCCESS. The review comment was issue comment `7189959433`; the COMMENTED review record was `6072835794`. The normal squash merge completed at `2026-11-26T10:53:03Z` as `59ab8ee2552a88e3acb663525035636f63da0f1e`. `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` returned that SHA. The akte blob on the reviewed head and on main is `6c1726a33351ec857ae1fffbd5443b69a2fccb62`.

The five reviewed factual claims were checked against GitHub APIs and commit trees:

1. Commit `2d17250b3f` is a direct child of `be672c215f` and changes only `evidence/2026-11-26/w308-0428-352-gateplanscan/akte.md`.
2. Orphan `18cefad98288a7806bdb5e9a9ed78e6c536a7c34` is not reachable from main; its author is w308 and committer is w301. GitHub compare reports diverged with `ahead_by=3`, `behind_by=1`, confirming the non-main lineage and identity collision.
3. Push runs `45777145407` (07:41:00Z, head `18cefad98`) and `45777293227` (07:42:13Z, head `2d17250b3`) match the reported replacement sequence. GitHub run metadata does not expose the force flag itself; the two timestamps and the orphan/replacement heads are the force-with-lease fingerprint recorded in the source akte.
4. Commits `4f2e01876`, `8525c6cdc`, and `ccd89bf2f` are direct-main commits whose changed paths are all under `evidence/`; their respective tree deltas are 488, 1, and 2 paths.
5. PR #1838 merged to main at `7bdeae95c` and changed only `evidence-r28/w142-0428-287-hop.md`; PR #1854 merged to main at `cddc81b34` and changed only `w219-0428-271-0428-286-1820hop-plan/evidence/2026-11-25/w219-0428-271-0428-286-1820hop.md`. Tag `v0.4.27` object `d94024608` peels to `6c40fab4d`; compare `6c40fab4d...main` reported ahead_by=5.

Identity finding: the session lane was `w311-0428-251-planpubdev`, while the commit author and committer were `w311-0428-251-pubdeviation`. Lane/card number match but suffix differs. This supports mechanically checking the canonical identity during review; no identity rewrite was made.

The merge lifted the previously recorded Plan-merge freeze. PR #111 was rechecked after #113 landed: its branch `w255-0428-251-284-close` started at `93a027518ba7ab6a2356edbdadd85a7566e5864b`, while current main was `59ab8ee2552a88e3acb663525035636f63da0f1e`. I fetched that exact `origin/main` and absorbed it with ordinary merge commit `2ac2ba4050`, author and committer both `w255-0428-251-demo170codex`. The card closure source change remains the only task source change; `python3 scripts/plan.py render` regenerated the derived views, and `python3 scripts/plan.py check` reported 785 tasks, 7 epics, 13 releases, 24 decisions, 0 errors, and 10 existing warnings. The PR remains open for independent review; this lane will not merge its own correction. A fresh Hosted Plan validation is required for the new exact head before that review.

Current state: #113 is merged and its deviation akte is present on Plan main. #111 contains the 0428-284 closure and is awaiting an independent review after its refreshed exact-head validation; it has not been merged by this lane.
