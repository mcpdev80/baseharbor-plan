# W16 — Plan card-field corrections from w286 inventory

Executing lane: w255-0428-251-demo170codex. Scope: planning card metadata and derived views only; no product repository writes and no PR updates in product repositories.

Plan repository remote proof from `git remote -v`:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Base attestation: branch cut from `origin/main` at `2eb677c1e994f0e79ffe5f6061863e553177664f`; this exact SHA was the fetched live main tip before creating the worktree. Required ancestry witness before publishing: `git merge-base --is-ancestor origin/main HEAD`. Required scope witness: `git diff origin/main...HEAD --name-only` plus `git log --oneline origin/main..HEAD`.

## Visible Ansatz — owner identity and commit gate

Exact target-card owners read from frontmatter at runtime on `origin/main` `2eb677c1e994f0e79ffe5f6061863e553177664f`:

- 0428-078: `owner: w165-0428-078-pr1650-basehop`
- 0428-284: `owner: w198-0428-284-demo-parser`
- 0428-249: `owner: w170-0428-249-demo-pr175-fixup`
- 0428-288: `owner: w147-0428-288-pr1833-fix`
- 0428-250: `owner: w50-0428-250-corefixture`

The commit identity for this review/correction lane is its own canonical identity, `w255-0428-251-demo170codex <w255-0428-251-demo170codex@baseharbor.local>`. Literal commit invocation:

```text
git -c user.name='w255-0428-251-demo170codex' -c user.email='w255-0428-251-demo170codex@baseharbor.local' commit -m 'w255 W16 card field corrections'
```

Pre-push identity gate: `git show -s --format=%an HEAD` must print exactly `w255-0428-251-demo170codex`.

## PLAN

1. Refresh Plan `origin/main`, resolve its GitHub remote, and cut one isolated branch from the exact fetched main SHA.
2. Read w286's merged divergence akte in Plan PR #86 at the recorded f0109585 merge and verify current GitHub PR states for the referenced candidates.
3. Correct only the specified card PR references and state/dependency notes for cards 0428-078, 0428-284, 0428-249, 0428-288, and 0428-250; preserve every task ID and all existing evidence-file bytes.
4. Reopen 0428-249 because PR #1812 remains open and the supplied HTTPS evidence does not demonstrate closure of that exact head; state this choice and reason in the PR body.
5. Record W15's required hop plus two distinct fresh `pull_request` runs for 0428-288; do not count run 45513816046 attempt 2 as pair evidence.
6. Record demo #181's `base=main` / `CONFLICTING` state on 0428-250 without changing either product PR.
7. Run `scripts/plan.py render`, then review the complete diff to confirm generated files came only from the renderer and no unrelated task, task ID, or evidence bytes changed.
8. Run `scripts/plan.py check`, create one scoped Plan PR, and wait for one fresh Hosted Plan validation on the exact proposed head.
9. Post the lane's `ROLLE: REVIEW` comment before merge, merge only after the required checks pass, and record the resulting main SHA.

## Current witnesses

Source inventory: w286's `evidence/w286-0428-board-prdiverg/akte.md`, delivered in Plan PR #86 and merged at `f010958521a5d7a9d343f89df90befbfae9bd500`.

Current exact GitHub states observed for this work:

- BaseHarbor #1650 OPEN at `37c4d847ca377d1555163ac4791c8ba08b85de77`; #1818 OPEN at `20fc1cb7d49602dc7f8aa0004a7562a81311d78c`; clean successor #1855 OPEN at `7d805dc6bbd6df2636d1b51999f3af53b989a676`.
- BaseHarbor #1812 OPEN at `0922888af8fd70be4049cec529c69aebc057a356`.
- BaseHarbor #1833 OPEN at `a7b0a48048c11d20234160eede941532ddc33156`; run `45513816046` is `pull_request`, `success`, attempt 2, and therefore void as distinct-run pair evidence.
- BaseHarbor #1856 OPEN at `67457cdb39a6e5a34964a9b8f0a2aaa2d479c4e0`.
- Demo #170 OPEN at `b086cf58bb2f7aafee30edf52ac4b8199daf7d0d`, base `develop`.
- Demo #181 OPEN at `6d06eab0ed0cd890ab9f818100ff84698e0347f5`, base `main`, mergeability `CONFLICTING`.

## Decisions in scope

- 0428-078: list #1650 as the contaminated-lineage audit and #1855 as the clean successor; remove #1818 from the qualifying PR list and state that its old head does not qualify.
- 0428-284: replace closed unmerged #1842 with current open successor #1856.
- 0428-249: reopen to wait because #1812 remains open; do not claim accepted closure without exact-head closure evidence.
- 0428-288: require W15 hop and two distinct fresh `pull_request` runs on one exact head; attempt-2 run 45513816046 is not pair evidence.
- 0428-250: document the open demo #170 behind the closed card and demo #181's conflicting `main` base; leave both PRs untouched.

All `depends_on` decisions will remain tied to task IDs and explicit card relationships; no new task or card is created.

## Card-field decisions applied

- `tasks/t-20261114-r28-perses-dashboard-identity.md` now lists #1650 and #1855. #1650 is explicitly retained as contaminated-lineage audit; #1818 is removed from the candidate list and described as a stale, nonqualifying head. The existing `depends_on` task ID is unchanged.
- `tasks/t-20261125-0428-284-1812-postretry-gate-failure.md` now lists demo #173, demo #174, and core #1856. Closed unmerged #1842 is replaced by #1856; #1812 is omitted as another card's PR. No new task dependency is inferred for 0428-284.
- `tasks/t-20261122-runtime-image-registry-artifact-unknown.md` is reopened in `wait`, its accepted resolution is cleared, and the wait reason records that #1812 remains open at the exact observed head. This is the selected closure correction: reopen rather than cite unsupported closure evidence. The existing evidence array is unchanged.
- `tasks/t-20261116-r28-bug-compose-service-ids.md` now depends on stable task ID `t-20261125-0428-284-1812-postretry-gate-failure`, the successor card for #1856, and records W15's hop plus two distinct fresh exact-head pull_request runs. Existing evidence remains empty; no run is represented as already passing.
- `tasks/t-20261122-ci-operator-fixture-allowlist-gap.md` keeps its accepted #1815 evidence, retains the open #170 reference, adds related demo #181, and documents #181's `main` base conflict. Neither demo PR was changed.
- No task ID or existing evidence-file blob changed. The only new evidence artifact in this change is this W16 akte; no prior evidence path is modified. All generated card snippets and views were produced by `scripts/plan.py render`, including `roadmap/cards.md`, `views/overview.md`, `views/kanban-dashboard.md`, and release views; none were hand-edited.

The first `scripts/plan.py check` found one error because the reopened 0428-249 still had a populated `blocker` with `kanban_status: wait`. The blocker field was cleared; the same reason remains in `wait_reason`. The subsequent check completed with zero errors and ten pre-existing dependency-acceptance warnings on unrelated r27 cards.

## Branch provenance before publication

`git merge-base --is-ancestor origin/main HEAD` succeeded (exit 0) for base `2eb677c1e994f0e79ffe5f6061863e553177664f`. The first candidate commit's parent is exactly that base. `git log --oneline origin/main..HEAD` before this provenance-record commit listed only the lane's own commit:

```text
6e700c224 w255 W16 card field corrections
```

`git diff origin/main...HEAD --name-only` before this provenance-record commit listed only this change set:

```text
evidence/2026-11-26/w16-card-field-corrections-w255/akte.md
releases/v0.4.28.md
roadmap/cards.md
tasks/t-20261114-r28-perses-dashboard-identity.md
tasks/t-20261116-r28-bug-compose-service-ids.md
tasks/t-20261122-ci-operator-fixture-allowlist-gap.md
tasks/t-20261122-runtime-image-registry-artifact-unknown.md
tasks/t-20261125-0428-284-1812-postretry-gate-failure.md
views/kanban-dashboard.md
views/overview.md
views/releases/v0.4.28.md
```
