# Authorized follow-up work

## PLAN

1. Merge Plan PR #201 only after exact-head Hosted validation verification; record merge commit and contents-API evidence.
2. Publish the corrected 0428-235 akte byte-for-byte in its own narrow Plan PR, recording source and published SHA-256 before/after.
3. In a separate Plan PR, transition 0428-078 from active to wait while preserving unrelated card fields, if OQ-3 and laptop-capacity conditions remain true.
4. Validate and merge each authorized Plan PR normally; verify exact main commit, PR head/run, and final card status.

## Base and remote attestation before branch creation

- Plan remote: `origin https://github.com/mcpdev80/baseharbor-plan.git`.
- Exact base ref `origin/main`: `1e67a5dfb41ee2fe369700baf338dc614fe7d8af`.
- Owner frontmatter for 0428-235, fetched from `origin/main`: `owner: ""` in `tasks/t-20261122-native-plan-self-selection.md`.
- Commit author and committer: `w267-0428-284-pridentity`, email `w267-0428-284-pridentity@baseharbor.local`.
- Invocation: `git -c user.name=w267-0428-284-pridentity -c user.email=w267-0428-284-pridentity@baseharbor.local commit ...`.
- Pre-push gate: `git show -s --format=%an HEAD` must print `w267-0428-284-pridentity`.

## PR #201 verification

- PR #201 was OPEN, not draft, at exact head `5edbda07587399fe247c05ed7c86037f2d0e766b`; validation run `45967369044` was pull_request, terminal success, on that exact head.
- It merged normally at `2026-11-27T08:53:11Z` as `1e67a5dfb41ee2fe369700baf338dc614fe7d8af`.
- GitHub contents API confirms `evidence/2026-11-27/0428-284/exact-head-183-ba14b0eed.md` on main, blob `3696925ed9a28153c1cf3df0ee97d06cd644d7b3`, size 9611 bytes.

## Corrected 0428-235 akte publication

Source: `workers/worktrees/w392-0428-235-selfselect-baseharbor/evidence/w392-0428-235-selfselect/akte.md`; source SHA-256 `8c5df43ff5f90b6e8ea2f88dbd0c9c61ee3fa76de9066cc2dc59f9cfe3ecc1b0`.
- New canonical `evidence/w392-0428-235-selfselect/akte.md` SHA-256 `8c5df43ff5f90b6e8ea2f88dbd0c9c61ee3fa76de9066cc2dc59f9cfe3ecc1b0`; `cmp` result: identical.
- The old main blob SHA-256 was `6583a27a2a8153759ebde01cc3aebc70488254d77e0089b7d9e61084d01600c3`. The correction says trusted develop contains `scripts/pr-gate-coverage.json` (blob `792a767aa`, 137751 bytes, 4389 lines, 78 `runtime_specific` rows); it removes the false “develop has NO file” assertion.
- PR evidence file also documents the exact source/published hashes; this is the publication provenance for this one-file content correction.

## Validation and publication

Plan render/check, PR head, Hosted validation run, merge commit and origin/main blob verification are pending.
