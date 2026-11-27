# Claim and status reconciliation

## PLAN

1. Read the six card contracts and verify live sessions, PR state, and blockers against the current Plan main.
2. Set statuses only where the live owner and evidence justify a change; preserve prior blocker and wait text verbatim in the card history.
3. Update status, owner, and blocker fields only; regenerate derived views and run Plan check.
4. Open one scoped Plan PR and verify Hosted `Plan - validate` on its exact head; include the run ID in the PR body.
5. Merge only with zero errors and exact-head green validation; record the main commit and all before/after statuses.

## Base and repository

- Mission's cited base was `3024a3cdd`; live Plan main was rechecked before branch creation and is `ecb89fe6e8cdf6625cb051a9e818b8c5577d959c`.
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` showed `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push; `baseharbor` points to the product repo and is not used for this Plan PR.

## Visible commit identity block

Card owners as read verbatim from the live Plan main frontmatter before edits:
- 0428-078: `w385-0428-078-pr1650pre`
- 0428-216: `Coordinator (Codeman)`
- 0428-224: `w391-0428-224-commitidentity`
- 0428-275: `Coordinator (Codeman)`
- 0428-284: `Coordinator (Codeman)`
- 0428-291: empty owner

The reconciliation commit author and committer will both be `w267-0428-284-pridentity`, with email `w267-0428-284-pridentity@baseharbor.local`, invoked as `git -c user.name=w267-0428-284-pridentity -c user.email=w267-0428-284-pridentity@baseharbor.local commit ...`. Before push, run and record the gate `git show -s --format=%an HEAD` and require the output to equal `w267-0428-284-pridentity`.

## Live lane witnesses

- `w385-0428-078-pr1650pre`, session `b4274b2d-e537-42e2-a536-98daf5d28576`, busy/working, assigned to 0428-078.
- `w388-0428-329-1861recipe`, session `6fb845fc-4001-4652-9311-3eb22cb540a2`, busy/working, mission maps it to 0428-275; its earlier census is evidence for 0428-216.
- `w390-0428-216-prhopcensus`, session `a20cbb93-9376-46dd-bd42-ce0a884635b2`, idle, mission maps it to blocked 0428-291; no active status will be assigned.
- `w391-0428-224-commitidentity`, session `d655a9da-8189-4282-9bc9-14e014dbbfcb`, busy/working, assigned to 0428-224.
- `w392-0428-284-demo183fix5`, session `8873ac0c-5570-4fdf-8c15-fdb85569f8df`, idle, assigned to 0428-284; the new candidate is PR #183 head `ba14b0eed4ebd747a2eb6bd14af470b910dd541c`. Its push run `45963172402` is failure, not the owner-dispatched qualification run; no workflow dispatch will be triggered by this lane.

## Status decisions

- 0428-078 stays active under its existing live owner w385.
- 0428-216 stays wait under Coordinator; census and hop-plan delivery are complete, but outstanding PR hops still require coordinator sequencing.
- 0428-224 stays active under its existing live owner w391.
- 0428-275 moves from wait to active under the live working session mapped by the mission, w388; its previous wait explanation is retained verbatim in the card history.
- 0428-284 becomes blocked under w392 pending the owner-dispatched Hosted run for the current PR #183 candidate; the prior wait text is retained verbatim in the card history.
- 0428-291 stays blocked and is assigned to w390; its single-writer STOP and baseline dependency remain unchanged.

## Status reconciliation results

- 0428-078: active → active; owner remains `w385-0428-078-pr1650pre` (busy/working).
- 0428-216: wait → wait; owner remains `Coordinator (Codeman)`. The census/hop-plan publication is now evidenced by Plan PRs #197 and #198. Outstanding PR hops remain under coordinator sequencing. The prior wait reason is retained verbatim in the card history.
- 0428-224: active → active; owner remains `w391-0428-224-commitidentity` (busy/working).
- 0428-275: wait → active; owner is set to the exact live session name `w388-0428-329-1861recipe`, which the mission maps to the catalog-only row-diff. Prior wait reason retained verbatim in card history.
- 0428-284: wait → blocked; owner is `w392-0428-284-demo183fix5`. PR #183 is open at exact head `ba14b0eed4ebd747a2eb6bd14af470b910dd541c`; exact-head run `45963172402` is a failed `push` event and its jobs API returned `total_count=0`. The required Owner-dispatched Hosted run remains pending. No dispatch or workflow edit was made. Prior wait reason retained verbatim in card history.
- 0428-291: blocked → blocked; owner set to exact live session name `w390-0428-216-prhopcensus`. The existing single-writer STOP and baseline dependency remain unchanged; no active status was assigned to the idle session.

`python3 scripts/plan.py render` regenerated task-derived releases, `roadmap/cards.md`, and views. `python3 scripts/plan.py check` completed with 784 tasks, 7 epics, 13 releases, 24 decisions, 0 errors, 10 existing warnings.

## Provenance

- Branch: `w267-0428-284-pridentity/claim-reconcile`, cut from live `origin/main` at `ecb89fe6e8cdf6625cb051a9e818b8c5577d959c`.
- No commits exist yet; the branch began at the attested base. Before PR creation, verify `git merge-base --is-ancestor origin/main HEAD`, record `git diff origin/main...HEAD --name-only`, and ensure `git log --oneline origin/main..HEAD` contains only this lane's commit(s).
- Intended diff: four task files, generated release/roadmap/view outputs, and this akte; no product files or `.github/**`.

## First candidate commit and scope proof

- First commit: `e016c87e0 plan: reconcile active lane claims`; `git show -s --format='%h an=%an cn=%cn' HEAD` returned `e016c87e0 an=w267-0428-284-pridentity cn=w267-0428-284-pridentity`.
- `git merge-base --is-ancestor origin/main HEAD` passed with `origin/main` at `ecb89fe6e8cdf6625cb051a9e818b8c5577d959c`.
- `git log --oneline origin/main..HEAD` listed only `e016c87e0 plan: reconcile active lane claims`.
- `git diff origin/main...HEAD --name-only` listed the akte, four task files, and renderer-derived `releases/v0.4.28.md`, `roadmap/cards.md`, `views/kanban-dashboard.md`, `views/overview.md`, and `views/releases/v0.4.28.md`.
