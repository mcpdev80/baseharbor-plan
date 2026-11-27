# w267 staged Akten publication record

Lane: `w267-0428-284-pridentity`
Role: `CODEX-PUBLISH`
Repository remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push)
Base attestation: `origin/main` at branch creation was `4f2d9ab89608d559263615a88ad92bcbb74784b7`; verified with `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` and fetched in the fresh clone. Before the second push, live main was `b02f9d04a0fc4d32e2a69470e9776f37a8011873`; forward-merged by ordinary merge commit `39f2cdbde` with canonical author and committer identity. `git merge-base --is-ancestor origin/main HEAD` succeeded after that merge.

## PLAN

1. Read the staged-publication mission and applicable Plan repository policy.
2. Verify all staged source files by SHA-256, byte count, line count, and canonical target-path absence.
3. Read the affected card owner fields verbatim from `origin/main` and record the publisher commit identity.
4. Copy staged Akten unchanged into their canonical `evidence/` paths and verify destination hashes.
5. Incorporate later staged Akten for 0428-284 and the 0428-216 hop plan into the same already-open Plan PR, then revalidate its final head.
6. Reconcile the reported `cmd/baha/core.go:71` conflict with the published w377 Akte and the live #1861 product ref.
7. Correct the 0428-216 PR-count arithmetic in this publication record while preserving its row-level ancestry tables.
8. Review #183 correction evidence: distinguish the real `drive.run_tty` final-drain code path from the synthetic fake-Core fixture and inspect the owner-dispatched exact-head run.
9. Review the exact diff to ensure it contains evidence only and changes no card fields, views, product files, or workflows.
10. Commit the evidence with the canonical Codex-session identity, verify ancestry and commit identity, push only the branch, and update the existing Plan PR.
11. Wait for exact-head Hosted Plan validation, review and merge if all gates pass; fetch main and verify all five staged Akte blobs.
12. Report PR, main commit, all five blob hashes, and card-field disposition.

## Identity and card-owner record

- Card 0428-078 frontmatter owner verbatim from `tasks/t-20261114-r28-perses-dashboard-identity.md`: `owner: w165-0428-078-pr1650-basehop`.
- Card 0428-329 frontmatter owner verbatim from `tasks/t-20261126-hunt46-recovery-backup-volume-heuristic.md`: `owner: ""`.
- Card 0428-216 frontmatter owner verbatim from `tasks/t-20261121-stale-pr-hop-and-baserefs.md`: `owner: "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)`.
- Card 0428-284 frontmatter owner verbatim from `tasks/t-20261125-0428-284-1812-postretry-gate-failure.md`: `owner: w374-0428-284-demo183fix`.
- This commit records staged evidence, not card content; publisher identity is this Codex session's canonical identity: `w267-0428-284-pridentity` / `w267-0428-284-pridentity@baseharbor.local`.
- Commit invocation: `git -c user.name=w267-0428-284-pridentity -c user.email=w267-0428-284-pridentity@baseharbor.local commit -m "evidence(0428-078, 0428-329, 0428-216, 0428-284): staged Akten"`.
- Pre-push gate: `git show -s --format=%an HEAD` must print exactly `w267-0428-284-pridentity`; author and committer must both be that identity. First-push witness recorded from the pre-push transcript: `57c2b0255 an=w267-0428-284-pridentity cn=w267-0428-284-pridentity`.

## Staged Akten and destination witnesses

- Source `coordinator/evidence-staging/2026-11-27/w385-0428-078-pr1650pre.akte.md`: SHA-256 `bc74654ec73e71cb4e60e854de2cc1582e8c03c48c8b763d99a39f4d98ecacf4`, 9,893 bytes, 120 lines. Destination `evidence/w385-0428-078-pr1650pre/akte.md` has the identical SHA-256.
- Source `coordinator/evidence-staging/2026-11-27/w388-0428-329-1861recipe.akte.md`: SHA-256 `52912e16cd9291cb6af915245ef64a5e1dcc8948a32400be293e08f03f43873b`, 14,389 bytes, 122 lines. Destination `evidence/w388-0428-329-1861recipe/akte.md` has the identical SHA-256.
- Source `coordinator/evidence-staging/2026-11-27/w390-0428-216-prhopcensus.akte.md`: SHA-256 `6983e6cac5f7a69019b44bd9bcce88035a525f5bdc43c171fe0fd90ec3eba136`, 8,394 bytes, 108 lines. Destination `evidence/w390-0428-216-prhopcensus/akte.md` has the identical SHA-256.
- Source `coordinator/evidence-staging/2026-11-27/w392-0428-284-demo183fix5.akte.md`: SHA-256 `042e52d59a2d9f755ad8f1a27bb174bd0516c49232b64a10bb7495557ee9d28d`, 6,821 bytes, 72 lines. Destination `evidence/2026-11-27/0428-284/exact-head-183-335ef5e54.md` has the identical SHA-256.
- Source `coordinator/evidence-staging/2026-11-27/w390-0428-216-hopplan.akte.md`: SHA-256 `66e7a7c3e23189b9abbcc21efe0b143a2f85f04cc3aaff284b1dbfa00ec723b4`, 9,354 bytes, 104 lines. Destination `evidence/w390-0428-216-hopplan/akte.md` has the identical SHA-256.
- Before this branch, none of the five canonical destination paths was present in `origin/main`. Similar earlier 0428-078 evidence exists under other paths and is not a duplicate of the canonical destination.

## w388 conflict-report reconciliation

The w388 Akte's cited #1861 head is `ade7dab3cf06658efd9a172ce3a674b887bd3c79`. GitHub Contents API returns 404 for `cmd/baha/core.go` at that ref, while `cmd/baha/main.go` exists. The published `origin/main:evidence/w377-0428-329-1861pre/akte.md` says the attempted merge refused unrelated histories, explicitly characterizes it as not a real content conflict, and says there is no conflict file. Thus the reported `cmd/baha/core.go:71` conflict is not substantiated by those published witnesses; record it as a stale or misattributed path/line, not as a product conflict requiring a code resolution.

## w390 census corrections

Both staged 0428-216 Akten enumerate 14 open baseharbor PRs and 3 open baseharbor-demo PRs. The combined total is 17. The census Akte's prose has inconsistent totals (16 and 13); the hop-plan Akte correctly states 17. Live API counts at review were baseharbor 14 and baseharbor-demo 3. The row-level ancestry table is unchanged by this count correction. Both source Akten are retained byte-identically; this note supplies the correction without rewriting either source.

The hop-plan Akte states `git push --force-with-lease` as an allowed transport for lane branches. That operational suggestion is not authorized by the staged-publication mission, which forbids force-push/history rewrite; readers must follow the current no-force rule. No force operation was executed.

## w392 #183 final-drain review

The incremental compare `d5b44c46c694c3099408939ec962cd723505003c...335ef5e54c59d109837cb6ba9cd00a382b3e611f` reports exactly one changed file: `tests/guided/test_consent_capture.py` (+39/−7). The full PR also contains earlier changes to `tests/guided/drive.py`; the staged Akte concerns only the incremental test correction.

Point 1 is correct: test_24 now passes an integer `already_read = len(buffer)` as the third argument at test lines 703–710, matching `reconcile_capture_from_log`'s integer offset and `log_tail[already_read:]` in `drive.py:293`. The owner-dispatched exact-head run confirms test_24 passes.

Point 2 uses the real `drive.run_tty` final-drain branch: `run_capture` calls it with `capture=True` (test lines 108–120 and 808–810), the test resets `drive.FINAL_DRAIN_CHUNKS` at line 805, and production increments it only in the post-exit drain loop (`drive.py:409–427`). However, the test's branch-forcing precondition is constructed with a fake Core and zero final delay. On exact head `335ef5e54c59d109837cb6ba9cd00a382b3e611f`, owner-dispatched workflow_dispatch run `45961168355` attempt 1 completed FAILURE: `test_24` passed, but `test_25` failed at `tests/guided/test_consent_capture.py:821` with `AssertionError: 0 == 0` (“at least one final-drain chunk must be read after process exit”). The branch was not reached in that observed run, so the claim that the >4096-byte fixture deterministically forces the digest-bearing tail through the final-drain branch is not established. The `FINAL_DRAIN_CHUNKS` assertion is not a constructed counter—it reads the production counter—but the fixture's intended precondition did not hold under Hosted CI. The additional exact-head push run `45960524146` also completed FAILURE. This evidence does not qualify #183; no product change or new trigger was made by this lane.

## Card and chain disposition

These five files are evidence for existing cards 0428-078, 0428-329, 0428-216, and 0428-284. They do not modify card frontmatter or task contracts. The w385 Akte reports observed PR relationships and a recommended qualification sequence; it does not change the #1650/#1818/#1855 chain contract. The two w390 Akten add census/hop-plan evidence; the w392 Akte records a test-only correction round. No card fields were changed. The explicit request to place these staged Akten together in this publication PR is followed; no product files or implementation are included.

## Publication-policy correction

My earlier blocked report called plan main technically protected. That was inaccurate. The Coordinator's 2026-11-27T07:42:59Z correction states that GitHub reports `Branch not protected` for baseharbor-plan main and cites successful direct-main pushes. The earlier stop was the political Plan write freeze recorded in `coordinator/PLAN-CLEANUP-HANDOFF-2026-11-28.md`, not technical branch protection. The subsequent mission explicitly authorizes this scoped PR publication for attribution; it does not authorize a direct-main push or generalize beyond this task.

## Scope review

The intended six-file diff is limited to five byte-identical staged Akten and this publication record under `evidence/`; no other files are included. It contains no task/card fields, generated views, product files, or `.github/**` workflow files. No product repository was modified and no local test or workflow trigger was run by this lane. Owner workflow_dispatch run `45961168355` on exact head `335ef5e54c59d109837cb6ba9cd00a382b3e611f` was observed to terminal failure; it is recorded as evidence, not triggered by this lane.

## Final publication witness for PR #197

- PR #197 head: `693b4776652dfa423df7f87ea19a0d9ae52bf5d7`; exact-head Plan Validate run `45961984187`, attempt 1, `pull_request`, SUCCESS; review record `6085078369` (COMMENTED, ROLLE: REVIEW+MERGE).
- PR #197 merged at `2026-11-27T07:59:11Z`; squash merge commit and resulting Plan main tip: `4a855876fc188d90c2d39cc5b972fd7b9374d5ed`.
- GitHub Contents blob witnesses on main: `evidence/w385-0428-078-pr1650pre/akte.md` = `bbd1b4d02e7743032f8b143cb926e42a713acb5f`; `evidence/w388-0428-329-1861recipe/akte.md` = `519e52c8f4934e6f9b9854c768e849b9d16c4937`; `evidence/w390-0428-216-prhopcensus/akte.md` = `abc289598ac87cc86b1329cf7de5327ca33a6dd7`; `evidence/2026-11-27/0428-284/exact-head-183-335ef5e54.md` = `c39bf1a74ad15d7f908548d4a8b105f9395651b5`; `evidence/w390-0428-216-hopplan/akte.md` = `fb0923404071d999121ae85082ec63b8511f6cb0`.
- SHA-256 of all five blobs matches their staged source files; no card fields were changed.

END_DONE w267-0428-284-pridentity: staged Akten are published by PR #197; main `4a855876fc188d90c2d39cc5b972fd7b9374d5ed`; five staged blob witnesses verified; card fields unchanged.
