# CODEX-REVIEW — PR #1736 / card 0428-055 / exact head 4c919fd61f3214fe435bafdc6281bf4bcb300022

## PLAN

1. Read the owner-directed mission and pin the review to exact head 4c919fd61f3214fe435bafdc6281bf4bcb300022.
2. Verify live refs, PR metadata, base develop 42da7128e724a533349e93d3742cbd232ea48936, author/committer, and exact hosted run 44960494316.
3. Inspect the two Coreless lifecycle execution routes, the named application test selection, and trusted-plan evidence.
4. Compare the exact hop diff `git diff 1e2ba9d57868778d7c74ef68882f61bd1b01bb33...4c919fd61f3214fe435bafdc6281bf4bcb300022` with the develop-only diff and confirm no added feature change.
5. Verify both ancestry relations: 1e2ba9d5786 is an ancestor of #1627 head 38be89aa4a0; current #1736 head 4c919fd61f3 is not.
6. Issue exact-head APPROVE or REQUEST CHANGES with terminal-green caveat; state explicitly that current #1736 head requires its own merge.
7. Publish evidence in Planning origin/main, verify path, update board, and post END; no merge or close.

## Review findings

**Final decision: APPROVE** for exact PR head `4c919fd61f3214fe435bafdc6281bf4bcb300022`, based on terminal successful run `44960494316`.


## PLAN — owner hold update

1. Read the new owner hold and remove #1627 from the active review scope; the prior conditional #1627 verdict is superseded and no current verdict is issued.
2. Refresh #1627 live head b3b0c2c9efc and exact #1736 run 44960494316.
3. Check whether #1736 head 4c919fd61f3214fe435bafdc6281bf4bcb300022 is an ancestor of the new #1627 candidate b3b0c2c9efc.
4. Finish the already assigned #1736 exact-head review and publish its conditional verdict, with no merge or close.
5. Publish evidence to Planning origin/main, verify the path, update board, and post END.

## PLAN — final #1627 head recheck

1. Mark the older ac05cc4efbc record superseded exactly as instructed; do not erase history.
2. Treat #1627 candidate b3b0c2c9efc43e9696c5eeda2a7164c88889e188 and run 44961334018 as the current acceptance target; no #1627 verdict before terminal green.
3. Verify current #1736 head 4c919fd61f3214fe435bafdc6281bf4bcb300022 is not an ancestor of b3b0c2c9efc43e9696c5eeda2a7164c88889e188; state that #1736 requires its own exact-head run and merge unless #1627 is hopped onto its branch.
4. Continue and publish only the #1736 review for its assigned exact head/run.

## PLAN — terminal #1736 verdict extension

1. Read the updated mission and pin the verdict to #1736 head 4c919fd61f3214fe435bafdc6281bf4bcb300022 and terminal run 44960494316.
2. Independently refresh refs, PR state, exact run checks, and `git cherry -v` patch-equivalence for the three #1736 commits against #1627 head b3b0c2c9efc43e9696c5eeda2a7164c88889e188.
3. State the no-merge-before condition requiring TestEnvironmentDestroyNativeLifecycle to execute on both engines in #1627’s exact terminal-green run and #1627 to land.
4. Recommend an owner decision on whether #1736 should be superseded/closed after #1627 lands or receive a separate merge; no merge or close by this reviewer.
5. Keep #1627 without verdict until exact run 44961334018 is terminal green.
6. Publish the updated evidence to Planning origin/main, verify its path, update board, and post END.


## Final #1736 exact-head review addendum

Decision: **APPROVE** for exact PR head `4c919fd61f3214fe435bafdc6281bf4bcb300022`. This is a content verdict only; no merge or close was performed.

Fresh remote witnesses from `https://github.com/mcpdev80/baseharbor.git`:

```text
42da7128e724a533349e93d3742cbd232ea48936 refs/heads/develop
b3b0c2c9efc43e9696c5eeda2a7164c88889e188 refs/pull/1627/head
4c919fd61f3214fe435bafdc6281bf4bcb300022 refs/pull/1736/head
```

PR #1736 is OPEN, non-draft, based on `develop`, head branch `codex/env-destroy-gate-routing`, author `mcpdev80`, mergeable `MERGEABLE`, merge state `CLEAN`. Exact pull_request run `44960494316` for the 40-character head above is terminal `completed/success` (updated 2026-11-21T23:25:33Z). The named Podman application job `137018078936` and Docker application job `137018079102` each completed `success`. `PR · Trusted Plan`, `PR · Validation · ci-executor-tests`, `PR · Validation · pr-planner-tests`, both selected `Core-less` application jobs for `integration/docker/coreless-lifecycle` and `integration/podman/coreless-lifecycle`, and aggregate `PR Selected Checks` completed successfully. Both engine application jobs executed; these are not skipped or queued receipts.

The environment-destroy regression is selected for both engines: `scripts/pr-gate-coverage.json:1468-1475` maps `cmd/baha/env_destroy_integration_test.go` to both Coreless lifecycle gates with required test `TestEnvironmentDestroyNativeLifecycle`. `scripts/pre-release-integration.py:73-78,91-111` assigns/selects the named application test, and `scripts/test_pre_release_integration.py:187-213` checks one application-shard assignment per runtime. The run’s exact selected Docker and Podman application jobs both succeeded.

Hop and patch evidence: head `4c919fd...` has parents `1e2ba9d57868778d7c74ef68882f61bd1b01bb33` and `42da7128e724a533349e93d3742cbd232ea48936`. The binary diff hashes for `git diff 1e2ba9d...4c919fd...` and `git diff 1e2ba9d...42da712...` both equal `50ee7b001a9c03ad8073d7ecb05921adc535c99859c44a9d72068df9151f4528`; the hop adds only the develop merge relative to the feature parent.

Current #1627 head is `b3b0c2c9efc43e9696c5eeda2a7164c88889e188`. Run `44961334018` remains `in_progress`; Docker application job `137020935578` and Podman application job `137020935792` are both completed with `failure`. The aggregate has not reached terminal status. Owner-provided hosted log evidence reports `TestEnvironmentDestroyNativeLifecycle` failing with `provider change: stale-impact-consent` on both engines. No #1627 verdict is issued here. `git merge-base --is-ancestor 4c919fd... b3b0c2c...` is false: the #1736 merge wrapper is not an ancestor of #1627. However, the feature commit `10150ee7164bbc8767136e540eb966c3baab930b` is an ancestor of #1627. A fresh `git cherry -v refs/review/codex-rev-1747/pr1627 refs/review/codex-rev-1747/pr1736` produced `- 4c919fd6...` for the merge wrapper and no content-commit lines. The owner-referenced three hashes (`8f11a34...`, `6af74dd...`, `31d8e5e...`) were not reproduced by this exact-ref comparison, so I do not attribute those minus lines to this witness. The verified patch-equivalence reason is that #1736 feature commit `10150ee7164bbc8767136e540eb966c3baab930b` is already an ancestor of #1627, and the binary tree diff hashes for the #1736 hop versus the develop-only hop both equal `50ee7b001a9c03ad8073d7ecb05921adc535c99859c44a9d72068df9151f4528`. The `4c919fd...` merge wrapper is not an ancestor of #1627; that is only the develop-hop wrapper, not missing feature content.

Recommendation to the Owner: after #1627 lands, mark #1736 superseded and close it as satisfied by the dependency, rather than separately merging its develop-hop wrapper. The functional feature commit is already an ancestor of #1627; only the wrapper is absent. Owner decides whether to close or take a separate merge action.

**Pre-merge condition:** do not merge #1736 before (a) `TestEnvironmentDestroyNativeLifecycle` has executed on both Docker and Podman in the exact #1627 run `44961334018` and that run is terminal green, and (b) #1627 has landed. Until both are true, #1736 remains unmerged.

Planning remote verified before publication: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.

## cleanliness

Read-only review; no containers or compose projects were started. `docker ps -a` with shell PID 893284 showed the same eight pre-existing exited containers (six exit 0, one exit 130, one exit 143); no container state was changed.




## PLAN — updated owner queue order

1. Refresh #1627 run `44961334018`; after terminal completion, verify Docker job `137020935578`, Podman job `137020935792`, and both artifacts prove `TestEnvironmentDestroyNativeLifecycle` executed. Publish the verdict and hand off to the merge role.
2. After #1627 lands, issue the #1736 supersede/contained disposition from exact cherry and ancestry witnesses; this reviewer does not merge or close.
3. Review #1749 head `ed9741b93c0` at exact run `44961731917`; after green, recheck `ETCDCTL_` filtering in `internal/testsupport/envpin/pin.go` against the hop.
4. Review #1723 head `5c063c7f278` at exact run `44961493271`; after green, verify `cmd/baha/workload_port_local_regression_test.go` is in an executed CI job.
5. Publish exact-head evidence and update the board after each verified event; do not merge or close.


## PLAN — final verdict and supersession correction

1. Replace the stale pending-review placeholder with the final exact-head result and terminal run/job evidence.
2. Record #1736 APPROVE with explicit no-merge-before-#1627 condition and the exact patch/ancestry explanation.
3. Supersede the prior conditional #1627 verdict for 38be head using the supplied terminal failure log evidence; preserve #1627 as no-verdict.
4. Cross-reference the separate fifth-round consent diagnosis without copying its analysis.
5. Publish the corrected evidence files to Planning origin/main and post one final END status.

END_DONE codex-rev-1747: #1736 APPROVE for exact head 4c919fd61f3214fe435bafdc6281bf4bcb300022; run 44960494316 and Docker 137018079102/Podman 137018078936 are terminal success; no merge before #1627 lands.
