# Board follow-up PR evidence

## PLAN

1. Confirm the exact #221 head and terminal Plan validation, independently inspect candidate changes, and verify actual merge state.
2. Refresh origin/main in an isolated clone, attest the exact base SHA, and record this plan and identity block before creating the candidate branch.
3. Apply only the authorized updates to 0428-250, 0428-306, and 0428-271, plus this deviation evidence; preserve unrelated main changes.
4. Run Plan render and check; require zero errors.
5. Verify ancestry, changed paths, own-only commit log, and canonical identity; push a normal branch and open one Plan PR.
6. Wait for terminal Plan validation on the exact PR head and merge normally only if validation succeeds.
7. Verify the remote merge and report PR, exact head, validation run, and main merge SHA.

## Visible commit identity block

- Exact card owner from origin/main frontmatter, verbatim: `owner: w267-0428-284-pridentity`.
- Git `user.name`: `w267-0428-284-pridentity`.
- Git `user.email`: `w267-0428-284-pridentity@baseharbor.local`.
- Literal commit invocation: `git -c user.name=w267-0428-284-pridentity -c user.email=w267-0428-284-pridentity@baseharbor.local commit ...`.
- Pre-push identity gate: `git show -s --format=%an HEAD` must equal `w267-0428-284-pridentity`.

## Base and repository

- Plan remote: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`; `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Exact fetched `refs/heads/main` base SHA: `7b1f6cd7b6d63f2d9e6aaf2689fd38ad5b162626`.
- Main commit `53c5fe97423475fe3c7c2c1b7a8d0dc30637ac4b` was checked with `git -C <clone> log --format=%H -1 53c5fe97423475fe3c7c2c1b7a8d0dc30637ac4b`; output was that exact SHA. GitHub commit-to-PR lookup returned an empty result. The main update is retained; this follow-up uses the PR path.

## #221 review receipt

- PR #221 head `031f0129c22afef60220236c73001f2baefbc807`.
- `Plan · validate` run `45989905766`: completed/success on that exact head.
- Remote PR state: merged at `2026-11-27T11:25:44Z`, merge commit `7b1f6cd7b6d63f2d9e6aaf2689fd38ad5b162626`.
- Independent review of #221: pass; exact-head records and body/history update were reviewed before normal merge.

## Authorized write set and evidence

- 0428-250: move closed/accepted to wait because Demo #170 remains open and carries a distinct payload. #170 head `b086cf58bb2f7aafee30edf52ac4b8199daf7d0d`; failed run `45663390190` is on that exact head. Its `tests/config-matrix/run.sh` blob is `a14357f35b77917163a00f845852b821150e8e29`, distinct from develop blob `620b09b57703f8c9ed7d60018cad7d26869ee45b`. Core #1815 merge `3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd` changes only Core files and does not supersede this Demo file. Wait reason records pending Owner/Codex disposition; `partial: follow-up tracked by #170` belongs in the card body, since `resolution` is restricted by schema to terminal accepted/superseded/dropped values.
- 0428-306: preserve active owner `w396-0428-306-goldenhelp`; add `mcpdev80/baseharbor#1874` and exact head `60d4d4906c686aa867f1c8d5f3d910ddba769999`. Run `45987934493` completed/failure on that exact head. The run's failing selection reports uncatalogued sources `cmd/baha/testdata/cli-help-golden.txt` and `internal/cli/help_surface_test.go`, then `REJECT: Go test selection missing or invalid` (`UNIT_SCOPE` blank, `UNIT_RESULT=skipped`).
- 0428-271: move blocked to wait because dependency 0428-274 is wait, and qualification of #1820 is sequenced after #1812. Clear `blocker`; retain PR #1820 and prior-head evidence without presenting it as current qualification.
- Deviation section: `main 53c5fe974 (board: reconcile 0428-284 to review) landed without Plan PR (commit->PR lookup empty) — useful work retained, PR path continuous from now on`.

## PR claim mappings

- `w255 = authorised #170-disposition review (plan-side duty, no product card claim)`
- `w267 = 0428-284 exact-head review CURRENTLY IN FLIGHT (plan-side duty)`

## Repo-rule compliance

- Planning-only card metadata and evidence; no tests run locally and no product files changed.
- No direct main write, force-push, workflow dispatch, or changes under `.github/**`.
- Evidence contains no Markdown checkbox lines.

## Cleanliness

- This task created no containers or compose project.

## END BLOCKED

Pending branch validation, hosted Plan validation, and normal merge.

## Precommit verification

- Fresh `git fetch origin main` resolved `origin/main` to `7b1f6cd7b6d63f2d9e6aaf2689fd38ad5b162626`.
- `git merge-base --is-ancestor origin/main HEAD` succeeded before candidate changes were committed.
- `git diff origin/main...HEAD --name-only` and `git log --oneline origin/main..HEAD` were empty before commit; this branch contains no inherited candidate commits.
- Current intended write set: `tasks/t-20261122-ci-operator-fixture-allowlist-gap.md`, `tasks/t-20261125-hunt36-golden-help-guard.md`, `tasks/t-20261124-r28-broker-build-identity-commit.md`, generated `views/kanban-dashboard.md`, `views/overview.md`, `views/releases/v0.4.28.md`, `releases/v0.4.28.md`, `roadmap/cards.md`, and this evidence file.
- `python3 scripts/plan.py render && python3 scripts/plan.py check`: 784 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings. Warnings concern historical accepted v0.4.27 cards with unaccepted dependencies.
- Evidence checkbox scan: clean.
- `docker ps -a` before editing showed no containers.

## PR body text

This PR contains only the three authorized task-state updates and the 53c5fe974 deviation record documented above.

- `w255 = authorised #170-disposition review (plan-side duty, no product card claim)`
- `w267 = 0428-284 exact-head review CURRENTLY IN FLIGHT (plan-side duty)`

Deviation: `main 53c5fe974 (board: reconcile 0428-284 to review) landed without Plan PR (commit->PR lookup empty) — useful work retained, PR path continuous from now on`

## Candidate provenance

- Candidate branch: `w267-0428-284-pridentity-followup-board`, cut from exact `origin/main` `7b1f6cd7b6d63f2d9e6aaf2689fd38ad5b162626`.
- `git merge-base --is-ancestor origin/main HEAD`: success.
- `git diff origin/main...HEAD --name-only` lists only the three authorized task files, generated Plan views/release files, and this evidence file.
- First candidate commit identity line: `3dcb51d1b an=w267-0428-284-pridentity cn=w267-0428-284-pridentity`.
- `git show -s --format=%an HEAD` returned `w267-0428-284-pridentity`.
- `git log --oneline origin/main..HEAD` listed only `3dcb51d1b Reconcile #170, #1874, and #1820 board states` at this checkpoint.
