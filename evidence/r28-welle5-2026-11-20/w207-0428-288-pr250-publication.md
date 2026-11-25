# w207 lane evidence — Publication PR for demo pr-config-matrix workflow (0428-250)

- Lane: w207-0428-288-pr250-publication
- Mission: /home/marcel/dev/baseharbor-ecosystem/coordinator/missions/w207-170-publication.txt
- Source of truth (read-only): workers/w200-codex-disposition/170/delivery-block.md, pr-config-matrix-draft.yml, card-addendum-draft.md
- END: STATE (awaiting coordinator — workflow absent from develop, no run receipts possible)

## ANSATZ BLOCK (visible commit-identity block, per owner directive 2026-11-28)

- Governing card: 0428-250, task `tasks/t-20261122-ci-operator-fixture-allowlist-gap.md`. Runtime frontmatter owner (fetched from baseharbor-plan origin/main at runtime): `w50-0428-250-corefixture`. Card already links demo PR #170.
- git user.name: lane-0428-250-config-matrix-workflow
- git user.email: lane-0428-250-config-matrix-workflow@baseharbor.local
- literal commit invocation: `git -c user.name=lane-0428-250-config-matrix-workflow -c user.email=lane-0428-250-config-matrix-workflow@baseharbor.local commit ...`
- pre-push gate line: `git show -s --format=%an HEAD` must equal `lane-0428-250-config-matrix-workflow`; on mismatch STOP + report (no silent amend)

## BASE ATTESTATION

- Product repo: baseharbor-demo. Remote verified: `origin https://github.com/mcpdev80/baseharbor-demo.git` (contains github.com/mcpdev80). This is the only remote used.
- Base ref cut from: origin/develop = `486c48be56f996fe976e0881a63e64bb7de92eb2` (witnessed via `git ls-remote origin refs/heads/develop`).
- PR #170 (the card's Demo PR): state OPEN, isDraft false, base develop, head `0249c9f73c21f46ba532fddc94a764e772f69acf`. Only changed file: `tests/config-matrix/run.sh`.
- Existing working-tree dirty file `tests/test_fixture_consent.py` stashed to a clean tree before branching.

## SCOPE

- Add ONLY `.github/workflows/pr-config-matrix.yml` verbatim per `pr-config-matrix-draft.yml`. No other file changed, no `tests/config-matrix/run.sh` change, no production code, no Core allow-list change.
- PR against DEMO DEVELOP.
- Owner-scope workflow file belongs to Owner; this PR publishes the workflow to develop so it can later self-trigger on PR #170. No workflow_dispatch, no draft-toggle qualification claims (the workflow is absent from develop, so it cannot self-trigger yet — see STATE below).

## PLAN

- Read mission + source-of-truth files; confirm scope (owner 0428-250, workflow file only).
- Attest develop tip SHA via ls-remote; verify clean tree; confirm PR #170 state.
- Create branch `lane-0428-250-config-matrix-workflow` off origin/develop tip.
- Write ONLY `.github/workflows/pr-config-matrix.yml` verbatim per draft; commit with lane identity; verify `%an` gate.
- Open PR #171 against develop, set draft=false immediately.
- Report STATE with PR number only (no run receipts: workflow absent from develop -> no pull_request run possible).
- Await coordinator: after PR #171 merged, head-hop PR #170 via `gh pr update-branch 170`; watch PR #170 pull_request run where config-matrix job executes at checkout==new exact head; report H + run ID.

## BRANCH PROVENANCE

- Branch cut from origin/develop tip `486c48be56f996fe976e0881a63e64bb7de92eb2`.
- Ancestor test: `git merge-base --is-ancestor 486c48be56f996fe976e0881a63e64bb7de92eb2 HEAD` -> pass.
- `git diff origin/develop...HEAD --name-only` -> only `.github/workflows/pr-config-matrix.yml`.
- `git log --oneline origin/develop..HEAD` -> only own commits.

## PUBLICATION RESULT (END_DONE)

- Branch `lane-0428-250-config-matrix-workflow` pushed to origin at HEAD `6d06eab0ed0cd890ab9f818100ff84698e0347f5` (witnessed: `git ls-remote origin refs/heads/lane-0428-250-config-matrix-workflow` -> `6d06eab0...`).
- PR #177: `https://github.com/mcpdev80/baseharbor-demo/pull/177`, base develop, head `6d06eab0...`, state OPEN, isDraft false (ready for review), single changed path `.github/workflows/pr-config-matrix.yml`.
- Commit content: single path, hash `7108cf69...` == w200 draft, `git show -s --format=%an HEAD` == `lane-0428-250-config-matrix-workflow` (%an gate pass).
- Isolated worktree (my zone, detached @6d06eab): `workers/w207-0428-250-config-matrix-workflow-wt`, HEAD `6d06eab0...`, clean, no extra commit.
- SHARED CHECKOUT UNTOUCHED: shared HEAD `6d06eab0...`, branch `lane-0428-250-config-matrix-workflow`, staged file frozen at blob `7108cf69...`, WIP stash `stash@{0}` intact, untracked `.tools/` + pycache intact.
- PR #170 untouched at head `0249c9f73c21f46ba532fddc94a764e772f69acf`, open, ready, base develop.

## STATE / BLOCKER (why no run receipts)

- PR #177 is the publication PR. EXPECT NO Hosted run on this publication PR: the workflow is absent from demo `develop` until PR #177 merges, so it cannot self-trigger. Zero receipts claimed here.
- Qualification happens later on PR #170 after merge + head-hop (w200 validation sequence): `gh pr update-branch 170` -> synchronize event -> `pull_request` run on PR #170/base develop where the config-matrix job checks out the new exact head and executes `bash scripts/acceptance.sh config-matrix` with `DEMO_SUITE` unset.
- w200 reviews the exact head `6d06eab0...` before any merge decision. No merge by this lane.

- The workflow file `pr-config-matrix.yml` is ABSENT from demo `origin/develop` (verified: `git show origin/develop:.github/workflows/pr-config-matrix.yml` -> path does not exist). It is therefore NOT yet active on the PR base.
- Per the mission amendment: HOLD all green/qualification claims for the self-triggering PR; build the branch + PR (workflow file only, per draft) but do NOT expect or assert any run receipts; report STATE with PR number only.
- The workflow can only self-trigger a pull_request run AFTER the owner merges this PR into develop and a later #170 head-hop produces a synchronize event. No run exists for the publication PR itself; that is expected and not a failure.

## CLEANLINESS

- Worktree: baseharbor-demo (shared checkout beside working directory).
- No docker/podman compose projects started; no containers. `docker ps -a` N/A.
- Dirty file restored: stash dropped after branch/PR created so the product tree returns to prior state.
