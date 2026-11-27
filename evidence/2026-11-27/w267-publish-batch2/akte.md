# Staged akte publication, batch 2

## PLAN

1. Inventory every staged akte in the designated staging folder; compute SHA-256 and compare with the mission note.
2. Copy each present file byte-for-byte to its canonical evidence path and review for checkbox/plan validation hazards.
3. Use a fresh isolated worktree from current Plan main; include no unrelated card or product changes.
4. Render/check, open one scoped Plan PR, and verify Hosted `Plan - validate` on its exact head; record run ID in PR body.
5. Merge only with 0 errors and exact-head green validation; record PR, main SHA, run ID, and all path/blob SHA-256 pairs.

## Status

No staged files inspected or copied yet.

## Base and remote attestation before branch creation

- The Plan remote is `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push); `baseharbor` is the product repository and will not be used.
- `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` returned `d6d917c7b6f5378f5c355081afff0f5f0fc059c7`.

## Staging inventory and byte verification

The four specifically listed mission files matched the supplied SHA-256 prefixes before copying:
- `w390-0428-175-integrity.akte.md` -> `evidence/w390-0428-175-integrity/akte.md` -> `840e971e4851fc2a89bd303dbc13b84e8fc67acf4485ef318fc104ec94a5a25e` (mission prefix `840e971e4851fc2a`).
- `w388-0428-274-1820check.akte.md` -> `evidence/w388-0428-274-1820check/akte.md` -> `05cdce5fded530db11f66b3b6811aceb778e4ba796237f314ebc8130700a1806` (mission prefix `05cdce5fded530db`).
- `w388-0428-275-rowdiff.akte.md` -> `evidence/w388-0428-275-rowdiff/akte.md` -> `f96f2a920a1986a117cd6efc5d329c1c1a851654ff9aed937277f71705f88c2a` (mission prefix `f96f2a920a1986a1`).
- `w392-0428-284-round6.akte.md` -> `evidence/2026-11-27/0428-284/round-6-ba14b0eed.md` -> `616f6dfbf3ea1be87ed3c50faffebcc7c03999cdffaf6d7cdd55c5273bd5c9a0` (mission prefix `616f6dfbf3ea1be8`).

Additional staged files present and absent from main were also included byte-for-byte:
- `w388-0428-216-blobcensus.akte.md` -> `evidence/w388-0428-216-blobcensus/akte.md` -> `06dab181ef58179d234d5fc52e403d711a9b08369a7343504989148187178190`.
- `w391-0428-224-commitidentity.akte.md` -> `evidence/w391-0428-224-commitidentity/akte.md` -> `9cdb038fa6b84e1e5c418080865332e3ac78482a45fa93de7f2f20864332f563`.
- `w392-0428-235-selfselect.akte.md` -> `evidence/w392-0428-235-selfselect/akte.md` -> `6583a27a2a8153759ebde01cc3aebc70488254d77e0089b7d9e61084d01600c3`.
- The staging directory contains `w385-0428-078-pr1855step.akte.md` (not the mission's named `pr1855hop` file); it is included under `evidence/w385-0428-078-pr1855step/akte.md`, SHA-256 `65ccb4471b6568ad7cc177b69f7e524608bc9a91a5b9d8117ca5f6b2ddd03eef`.

Five other staged items already existed on main with exact matching blobs and were not duplicated: w385 `pr1650pre` (`bc74654ec73e71cb4e60e854de2cc1582e8c03c48c8b763d99a39f4d98ecacf4`), w388 `1861recipe` (`52912e16cd9291cb6af915245ef64a5e1dcc8948a32400be293e08f03f43873b`), w390 `hopplan` (`66e7a7c3e23189b9abbcc21efe0b143a2f85f04cc3aaff284b1dbfa00ec723b4`), w390 `prhopcensus` (`6983e6cac5f7a69019b44bd9bcce88035a525f5bdc43c171fe0fd90ec3eba136`), and w392 round-5 demo akte (`042e52d59a2d9f755ad8f1a27bb174bd0516c49232b64a10bb7495557ee9d28d`).

`rg -n -- '- \[ xX]\]'` over all eight newly included staged files returned no matches. The copied file hashes match their source hashes exactly.

## Visible commit identity block

The lane's associated 0428-284 card owner as currently recorded on `origin/main` is `w392-0428-284-demo183fix5`; this is an evidence-only publication and changes no card fields. Commit author and committer will both be `w267-0428-284-pridentity`, email `w267-0428-284-pridentity@baseharbor.local`, via `git -c user.name=w267-0428-284-pridentity -c user.email=w267-0428-284-pridentity@baseharbor.local commit ...`. Pre-push gate: `git show -s --format=%an HEAD` must print `w267-0428-284-pridentity`.

## END

END_DONE w267-0428-284-pridentity: staged batch published through scoped Plan PR; final candidate and merge witnesses are recorded in the PR body.
