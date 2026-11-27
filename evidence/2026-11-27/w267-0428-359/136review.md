# Plan PR #136 exact-head review

Date: 2026-11-27
Lane: `w267-0428-284-pridentity`
Role: `REVIEW`
Verdict: **HOLD — do not merge this head**

## PLAN

1. Verify the live PR head, base, merge state, branch ref, current plan main, and exact-head Hosted Plan check/run records.
2. Compare the PR tree with live main; inspect the 0428-359 baseline card and related family-card blocker states.
3. Verify whether the product develop catalog contains the four sets' source rows.
4. Post the exact-head HOLD review on #136; do not merge while scope, ancestry, and evidence conditions fail.
5. Publish this review record through an isolated evidence-only plan PR; do not write directly to main.

## Source and remotes

- Planning repository: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.
- Verified GitHub remotes: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push); `upstream2 https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push).
- Planning evidence branch was created from `origin/main` `0e0c1480d7e803687e97a70d71ea9891efd57eaa`, then fast-forwarded without a commit to `598c4cee0c247167a8d041b93d6aa4cd0dd54b52` before this Akte commit.
- PR #136 base is `main`; exact head and `refs/pull/136/head` are `c4e4400174dc3fe5c04082c7c85483db9b82543f`.
- The initial compare/comment observed main at `6d4e82c82ea1c69953c05cc6496910d9537dc6f8`; subsequent refreshes observed `0e0c1480d7e803687e97a70d71ea9891efd57eaa` and now `598c4cee0c247167a8d041b93d6aa4cd0dd54b52`. At the latest refresh, main is still not an ancestor of the PR head: 27 commits behind and 105 ahead; merge-base `ef0bcfbcf55ad0e0aaaa552c3f2b42d9f72dc6f8`; `git merge-base --is-ancestor origin/main origin/pr-136` exits 1.

## Exact-head Hosted evidence

- Current head run: `45937240521`, attempt 1, event `workflow_dispatch`, completed `SUCCESS`, head `c4e4400174dc3fe5c04082c7c85483db9b82543f`; commit check-run `Plan · validate` is completed success (check-run ID `140303176964`).
- Prior-head run: `45858842634`, attempt 1, `SUCCESS` on predecessor `fe586a8da1f4a3b64b69c39f02960666d4443bee`; it is superseded and cannot qualify the current head.
- The Actions API query by the full current SHA returns only run `45937240521`; no pull_request run exists for this head. Do not present two run IDs as two qualifying executions on the same head.

## Content and scope review

The card 0428-359 text in the PR tree lists seven exact source IDs/paths for the #1860 recovery-manifest, #1862 runtimeexecutor compose, #1861 repository-volume-inventory, and #1863 stableid lock-probe sets. Each required row specifies the existing Docker and Podman `data.capabilities` surfaces and `runtime_specific: true`. This is an accurate plan-side description of the baseline intent and does not authorize a candidate to self-admit.

That card text does not mean the product catalog rows have landed. In product `develop`, none of the seven named IDs appears in `scripts/pr-gate-coverage.json`. The family cards remain blocked: 0428-312/#1860 awaits its recovery-manifest row; 0428-318/#1862 its runtimeexecutor rows; 0428-329/#1861 its repository-volume-inventory rows; and 0428-299/#1863 its stableid rows. The plan PR itself cannot clear those product Trusted Plan blockers.

The claim that this PR changes only the catalog-family card and generated views is contradicted by the tree comparison against current plan main: 593 paths changed, 12,726 insertions and 887 deletions. The delta includes extensive historical evidence, mission, coordinator-memory, and unrelated task content; `evidence/coord-memory/QUEUE.md` alone has a large unrelated change. No `.github/**` or `scripts/**` path appears in the current tree delta, and I found no product consent/auth implementation change, but the overall plan diff is still outside the claimed narrow scope. GitHub now reports `mergeStateStatus: DIRTY`.

## Verdict and required next state

HOLD. Do not merge `c4e4400174dc3fe5c04082c7c85483db9b82543f`. The branch is not based on current main, its live tree diff is not confined to the 0428-359 task and generated views, and its only current-head run is a single `workflow_dispatch` execution. Preserve run `45937240521` as the exact-head validation witness and `45858842634` as predecessor-only evidence. A corrected candidate must be forward-consistent with current main, have a tree diff limited to the intended 0428-359 card and renderer-generated views, and receive fresh Hosted Plan validation on that exact head. The product rows must still land on develop before the four owning product PRs can requalify.

Review comments: ROLLE: REVIEW HOLD posted on #136 at exact head `c4e4400174dc3fe5c04082c7c85483db9b82543f`; records `6083578167`, `6083592787`, and `6083596824` (the latter is the latest current-main refresh). No merge performed.

END_DONE w267-0428-284-pridentity: #136 reviewed and held; exact head c4e4400174dc3fe5c04082c7c85483db9b82543f.
