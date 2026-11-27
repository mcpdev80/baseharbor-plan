# w267 staged Akten publication record

Lane: `w267-0428-284-pridentity`
Role: `CODEX-PUBLISH`
Repository remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push)
Base attestation: `origin/main` at branch creation was `4f2d9ab89608d559263615a88ad92bcbb74784b7`; verified with `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` and fetched in the fresh clone.

## PLAN

1. Read the staged-publication mission and applicable Plan repository policy.
2. Verify all staged source files by SHA-256, byte count, line count, and canonical target-path absence.
3. Read the affected card owner fields verbatim from `origin/main` and record the publisher commit identity.
4. Copy all three Akten unchanged into their canonical `evidence/` paths and verify destination hashes.
5. Reconcile the reported `cmd/baha/core.go:71` conflict with the published w377 Akte and the live #1861 product ref.
6. Correct the 0428-216 PR-count arithmetic in this publication record while preserving its row-level ancestry table.
7. Review the exact diff to ensure it contains evidence only and changes no card fields, views, product files, or workflows.
8. Commit the evidence with the canonical Codex-session identity, verify ancestry and commit identity, push only the branch, and open the requested Plan PR.
9. Wait for exact-head Hosted Plan validation, review and merge if all gates pass; fetch main and verify all three Akte blobs.
10. Report PR, main commit, all three blob hashes, and card-field disposition.

## Identity and card-owner record

- Card 0428-078 frontmatter owner verbatim from `tasks/t-20261114-r28-perses-dashboard-identity.md`: `owner: w165-0428-078-pr1650-basehop`.
- Card 0428-329 frontmatter owner verbatim from `tasks/t-20261126-hunt46-recovery-backup-volume-heuristic.md`: `owner: ""`.
- Card 0428-216 frontmatter owner verbatim from `tasks/t-20261121-stale-pr-hop-and-baserefs.md`: `owner: "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)`.
- This commit records staged evidence, not card content; publisher identity is this Codex session's canonical identity: `w267-0428-284-pridentity` / `w267-0428-284-pridentity@baseharbor.local`.
- Commit invocation: `git -c user.name=w267-0428-284-pridentity -c user.email=w267-0428-284-pridentity@baseharbor.local commit -m "evidence(0428-078, 0428-329, 0428-216): staged Akten"`.
- Pre-push gate: `git show -s --format=%an HEAD` must print exactly `w267-0428-284-pridentity`; author and committer must both be that identity.

## Staged Akten and destination witnesses

- Source `coordinator/evidence-staging/2026-11-27/w385-0428-078-pr1650pre.akte.md`: SHA-256 `bc74654ec73e71cb4e60e854de2cc1582e8c03c48c8b763d99a39f4d98ecacf4`, 9,893 bytes, 120 lines. Destination `evidence/w385-0428-078-pr1650pre/akte.md` has the identical SHA-256.
- Source `coordinator/evidence-staging/2026-11-27/w388-0428-329-1861recipe.akte.md`: SHA-256 `52912e16cd9291cb6af915245ef64a5e1dcc8948a32400be293e08f03f43873b`, 14,389 bytes, 122 lines. Destination `evidence/w388-0428-329-1861recipe/akte.md` has the identical SHA-256.
- Source `coordinator/evidence-staging/2026-11-27/w390-0428-216-prhopcensus.akte.md`: SHA-256 `6983e6cac5f7a69019b44bd9bcce88035a525f5bdc43c171fe0fd90ec3eba136`, 8,394 bytes, 108 lines. Destination `evidence/w390-0428-216-prhopcensus/akte.md` has the identical SHA-256.
- Before this branch, none of the three canonical destination paths was present in `origin/main`. Similar earlier 0428-078 evidence exists under other paths and is not a duplicate of the canonical destination.

## w388 conflict-report reconciliation

The w388 Akte's cited #1861 head is `ade7dab3cf06658efd9a172ce3a674b887bd3c79`. GitHub Contents API returns 404 for `cmd/baha/core.go` at that ref, while `cmd/baha/main.go` exists. The published `origin/main:evidence/w377-0428-329-1861pre/akte.md` says the attempted merge refused unrelated histories, explicitly characterizes it as not a real content conflict, and says there is no conflict file. Thus the reported `cmd/baha/core.go:71` conflict is not substantiated by those published witnesses; record it as a stale or misattributed path/line, not as a product conflict requiring a code resolution.

## w390 count correction

The staged 0428-216 Akte's tables enumerate 14 open baseharbor PRs and 3 open baseharbor-demo PRs. The combined total is 17. Its prose also says 16 and 13 in different summary locations; those totals are arithmetically inconsistent with the table and the live API counts (`gh pr list --state open --limit 100`: baseharbor 14, baseharbor-demo 3). The row-level ancestry table is unchanged by this count correction. The staged Akte is retained byte-identically; this note supplies the correction without rewriting its source.

## Card and chain disposition

These three files are evidence for existing cards 0428-078, 0428-329, and 0428-216. They do not modify card frontmatter or task contracts. The w385 Akte reports observed PR relationships and a recommended qualification sequence; it does not change the #1650/#1818/#1855 chain contract. No card fields were changed. The explicit request to place these staged Akten together in this publication PR is followed; no product files or implementation are included.

## Publication-policy correction

My earlier blocked report called plan main technically protected. That was inaccurate. The Coordinator's 2026-11-27T07:42:59Z correction states that GitHub reports `Branch not protected` for baseharbor-plan main and cites successful direct-main pushes. The earlier stop was the political Plan write freeze recorded in `coordinator/PLAN-CLEANUP-HANDOFF-2026-11-28.md`, not technical branch protection. The subsequent mission explicitly authorizes this scoped PR publication for attribution; it does not authorize a direct-main push or generalize beyond this task.

## Scope review

The intended four-file diff is limited to the three byte-identical staged Akten and this publication record under `evidence/`. It contains no task/card fields, generated views, product files, or `.github/**` workflow files. No product repository was modified and no workflow dispatch or local test was run.
