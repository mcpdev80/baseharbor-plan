# Akte — compliant akte-only reissue of plan PR #132 (identity incident chain)

- Card: t-20261126-hunt46-collectable-orphans-reserved-namespace (0428-327)
- Lane: w339-0428-327-reissue132 (author AND committer)
- Date: 2026-11-26
- Scope: single evidence file, `evidence/2026-11-27/w339-0428-327-reissue132/akte.md`
- Commit: akte-only, no product code, no other repos, no merges, no close of #132
- Branch provenance: cut from LIVE origin/main; base sha below is an ancestor of the head commit

## Incident chain (read-only evidence, no cherry-pick, never push here)

| Object | SHA | Author / Committer | Role / note |
| --- | --- | --- | --- |
| Contaminated branch `w322-hunt46-orphans` (correction + head merge) | `9629d6e60882ca9e6e3e39185fb3541027d22b75` (correction) + `fe79bb3c03bfe45a4dbc6c77afe91db5d5d686eb` (head) | `w322-0428-249-pr1812gate` | Implementing session was w322; both objects carry the foreign-lane identity `w322-0428-249-pr1812gate` |
| Original #132 akte commit (the HOLD candidate) | `8d9c79c472f1c9b0421375b886a62735005e907e` | `w322-0428-249-pr1812gate` | Parent `e62533ee1a03e85efff683b14258e60ea0e484cc` (PR base snapshot main); Hosted run 45832831998 SUCCESS |
| Frozen audit branch `w340-0428-327-aktefix-r2` (right work, wrong name) | `6f00698b32f45e8ec70bb24e9cc73e3f4dd3646e` | `w340-0428-327-reissue132` (per PR #146 title) | Read-only audit evidence; superseded by THIS lane per amendment 7197979554 |

All three SHAs are remote-verified:

```
git ls-remote origin 2>&1 | grep -E "9629d6e6|fe79bb3c|6f00698b"
fe79bb3c03bfe45a4dbc6c77afe91db5d5d686eb	refs/heads/w322-hunt46-orphans
6f00698b32f45e8ec70bb24e9cc73e3f4dd3646e	refs/heads/w340-0428-327-aktefix-r2
fe79bb3c03bfe45a4dbc6c77afe91db5d5d686eb	refs/pull/132/head
6f00698b32f45e8ec70bb24e9cc73e3f4dd3646e	refs/pull/146/head
```

## Verdict witnesses (fetched live via `gh api repos/mcpdev80/baseharbor-plan/issues/comments/<id>`)

- **Comment 7197905382 (ROLE: REVIEW — HOLD, foreign-lane authorship finding only; no content verdict):** reviewed head `fe79bb3c03bfe45a4dbc6c77afe91db5d5d686eb`; both the correction `9629d6e60882ca9e6e3e39185fb3541027d22b75` and the head merge `fe79bb3c03bfe45a4dbc6c77afe91db5d5d686eb`, and the akte commit `8d9c79c472f1c9b0421375b886a62735005e907e`, carry author AND committer `w322-0428-249-pr1812gate`. The implementing session is w322, so the candidate fails the candidate identity rule (both author and committer must be the executing lane's canonical identity). Recovery path: publish an akte-only reissue from a fresh clean branch under the executing lane's correct canonical identity, no rewrite or cherry-pick; then close #132 with a cross-link to the compliant replacement (close is not merge).
- **Comment 7197979554 (ROLE: REVIEW — REISSUE SPEC AMENDMENT):** the fresh reissue identity is assigned as **w339-0428-327-reissue132** as both author and committer on its akte-only commit; supersedes any earlier placeholder identity wording; w335 remains parked; the foreign `w322-0428-249-pr1812gate` identity is inadmissible for the reissue. Once the fresh PR head has its own green Hosted Plan validation, the exact-head review verifies this identity and the corrected 0428-327 conclusion. No merge.
- **Comment 7197353979 (ROLE: REVIEW — HOLD, evidence content):** exact head `8d9c79c472f1c9b0421375b886a62735005e907e`; Hosted run 45832831998, pull_request, SUCCESS on this exact head; scope one evidence file. Content hold: the akte concludes "NO PRODUCT LEAK FOUND IN RESERVED-NAMESPACE ORPHAN SURFACE" and classifies `CollectableOrphans` as safely guarded by `DeploymentID==folder` and Target matching. That conflicts with card 0428-327 (`Goal`/`Acceptance` lines 44, 50, 56-58 and `Task` line 73): the crafted `never-delivered/deployment.json` with `DeploymentID=="never-delivered"` and matching Target was reproduced as a collectable orphan, and the card requires an explicit reserved-directory skip regardless of contents. Reconcile the census conclusion with this live card finding (including the relevant source revision/context) before acceptance; evidence-content issue, not a request for product edits.

## Never-delivered-orphan census (card t-20261126-hunt46*, 0428-327)

The H-V46 reserved-namespace orphan surface spans four never-delivered cards, each a distinct seam over the same `never-delivered/<applicationID>/<environment>.json` namespace the adoption writer creates:

- **0428-327 — collectable orphan skip dir:** `CollectableOrphans` (`internal/deployment/deployment_list.go:185`) iterates each direct child directory of `deployments/`. The reserved `never-delivered/` directory is a direct child, so it is enumerated; it is only not listed as an orphan by accident (a missing `never-delivered/deployment.json` read bails early). A crafted `never-delivered/deployment.json` whose `DeploymentID=="never-delivered"` and `Target==target` was reproduced as a collectable orphan. Fix: explicit reservation skip of `never-delivered` at the enumeration loop, before `deploymentOwnerMissingForDetach`.
- **0428-326 — consume never-delivered proof:** on the never-delivered destroy/retire path (`cmd/baha/app_runtime_retirement.go:57-86`) the proof is verified (`VerifyNeverDeliveredProof`, `internal/deployment/never_delivered_proof.go:72`) but never consumed (`ConsumeNeverDeliveredProof` is only called from `internal/deployment/deployment_store.go:562`). A stale one-shot witness makes the next O_EXCL adoption fail "already exists".
- **0428-328 — skip reserved damaged scan:** `DamagedDeploymentNamespace` (`internal/deployment/damaged_state.go:266`) flags a protected-state file placed directly under `never-delivered/` as damaged; the proof-exclusion guard skips a damaged directory only when a proof for THIS repository app exists, not when the namespace itself is reserved.
- **0428-329 — tighten recovery/backup volume match:** `InventoryRepositoryVolumes` classifies a volume as shared/preserved by a case-insensitive substring heuristic (`repository_volume_inventory.go:73-77`), so a mislabeled recovery/backup volume is wrongly deleted under `destroy --all`.

All four cards were cast from H-V46 on origin/main `62de9bb74`, anchor develop `2a141387d`; intake re-verified against develop `384d857b5` (per card Task sections). The census is consistent across the four: every one of the reserved `never-delivered/` surface is handled only by accident or by a content-dependent guard, not by an explicit reserved-namespace reservation.

## Conclusion

- The original #132 akte (commit `8d9c79c472f1c9b0421375b886a62735005e907e`, identity `w322-0428-249-pr1812gate`) concluded "NO PRODUCT LEAK FOUND IN RESERVED-NAMESPACE ORPHAN SURFACE" and classified `CollectableOrphans` as safely guarded. That conclusion is **inconsistent with card 0428-327**, which reproduces the crafted `never-delivered` record as a collectable orphan and requires an explicit reserved-directory skip (Goal/Acceptance lines 44, 50, 56-58; Task line 73). The census, read across 0428-326/327/328/329, shows the reserved `never-delivered/` namespace is only incidentally avoided by content-dependent guards — the surface is **not** explicitly reserved. Corrected conclusion: **a product gap is confirmed on the reserved-namespace orphan surface; every seam (0428-327, 0428-328, 0428-326) needs an explicit reservation skip, and 0428-329 needs an authoritative volume-label match.**
- The original #132 was also inadmissible on identity: both author and committer were the foreign-lane `w322-0428-249-pr1812gate`, failing the candidate identity rule (verdict witness 7197905382), and the fresh identity was explicitly reassigned to **w339-0428-327-reissue132** as author AND committer on the akte-only commit (verdict witness 7197979554).
- **Replacement line for #132:** PR #132 is superseded by the compliant akte-only reissue of THIS lane, branch/PR `w339-0428-327-aktefix` under canonical lane identity `w339-0428-327-reissue132` (author AND committer), whose corrected 0428-327 census conclusion reconciles the reserved-namespace orphan surface with the live card finding. #132 is to be closed (not merged) with a cross-link to this replacement; close is routed by the Coordinator after review.

## Branch provenance

```
git ls-remote origin refs/heads/main
f54f6ad5aebbf3daa61a05b74f028c2c69c9338f	refs/heads/main
```

Base sha `f54f6ad5aebbf3daa61a05b74f028c2c69c9338f` (LIVE origin/main at branch cut). The single akte commit will have this base as an ancestor and `git log --oneline origin/main..HEAD` will list only this lane's one commit.

## Stops honored

No close of #132, no merges, no other repos, no local tests, no subagents, never push to w340/w322 branches.
