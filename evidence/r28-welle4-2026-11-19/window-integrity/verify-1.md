# Window integrity verify — card t-20261119-r28-window-integrity-verify (0428-150)

Mission `x-150v2.txt`. Role: verification worker. No product code changed, no PR opened on baseharbor, no edit to baseharbor/**. Read-only remote verification against GitHub via `gh api` + `git ls-remote origin` and a fresh clone in `/tmp/150v2-baha` (product) and `/tmp/150v2-plan` (planning). No subagents (§4.8). No rerun, no `workflow_dispatch`, no `.github/**` edit.

## PLAN

- Fetch remote witnesses at start (develop head, plan main).
- V1 merge acceptance: blob-identity of every merged PR in the wave against develop.
- V2 verdict-chain: codex verdict SHA equals the merged SHA.
- V3 exact-head runs: a terminal `pull_request` run at the current head, and lane-base -> develop free of the planner files.
- V4 skipped-balance: skipped cells counted per run, no SKIPPED reported as pass.
- V5 board-truth: kanban_status vs real PR state; planned cards in the releases view.
- V6 double-work: two open PRs touching the same file same direction.
- Write this evidence file, push to origin/main, post END.

## Remote witnesses (self-measured, §4.1)

- develop head at start: `git ls-remote origin refs/heads/develop` -> `4b3a3559070e9b81b1886a357f6a46bc6dfce790` (baseharbor clone `/tmp/150v2-baha`). Moved during the run; at end `15727ca8878938df7e924319c236c0bcc4a4201c`. Confirmed the "develop moves every few minutes" note.
- plan main at start: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main` -> `e9c851c2e29166ac99e7fdab0a6097a44fd7adc5`; at end `/tmp/150v2-plan git rev-parse origin/main` -> `281c02f18d304f814ab4eea9bb2b9a130bbf2de6`.
- Plan repo correct zone attested: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` -> `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, remote `https://github.com/mcpdev80/baseharbor-plan.git`.

## V1 — Merge acceptance: blob-identity, not ancestry

Every named PR was checked two ways: (a) its merge commit is an ancestor of develop, (b) its own content diff against its merge-parent lists only the files it claims. Method witness (baseharbor clone `/tmp/150v2-baha`, develop `4b3a3559`):

- `gh api repos/mcpdev80/baseharbor/pulls/<n> --jq '.state,.merged,.merge_commit_sha,.head.sha'` for each of #1705, #1589, #1697, #1581, #1703, #1599, #1693, #1692, #1691, #1682, #1592, #1602, #1685, #1694, #1696, #1663, #1677, #1686, #1687, #1688, #1689.
- `git merge-base --is-ancestor <merge_commit> origin/develop` -> TRUE for all 21 merge commits.
- `git show --format='%P' <merge_commit>` and `git diff --name-only <commit>^1 <commit>` per PR -> each PR changed exactly its own files (1-2 for the fix PRs; #1599 a larger Perses runtime set), content consistent with the PR title.
- Merge-commit parent chain is contiguous (each `^1` == the previous PR's merge commit), proving the wave landed linearly on develop.

Result: all 21 named PRs are genuinely in develop by real merge commit. No V1 finding. (Note: squash-merge ancestry checks would be worthless here; the merge-commit containment + own-content-diff method is the blob-identity proof.)

## V2 — Verdict chain (the reported case)

PR #1697 (0428-131) — verdict-chain break:

- Merged commit on develop: `4b3a3559070e9b81b1886a357f6a46bc6dfce790` (this is the develop head at the time). Witness: `gh api .../pulls/1697 --jq '.merge_commit_sha'` and `git merge-base --is-ancestor 4b3a3559 origin/develop`.
- Reviewed head named in the verdict: `708f5c5c8acee5133e480d151544cb139bb3ded3`. Witness: evidence file `evidence/r28-welle4-2026-11-19/codex-review-wave/1697-0428-131-independent-review.md` line 5 ("Head `708f5c5c8acee5133e480d151544cb139bb3ded3`").
- PR head at merge time: `d1f97a63a38271a1326b5b49faf114028e67a26a` (already rebased onto a newer develop tip than the review).
- Tree witness: `git rev-parse 4b3a3559^{tree}` -> `a4cd61e72c8244f27f72dd3baeadbba30c0f8963`; `git rev-parse 708f5c5c8^{tree}` -> `861191a1050d829258126a805cc86da5b480a603`. The merged tree (a4cd61e7) != the reviewed tree (861191a1). `git merge-base --is-ancestor d1f97a63 origin/develop` -> TRUE.
- No verdict file exists at the merged SHA `4b3a3559`. The only #1697 verdict names head `708f5c5c8`; the content that actually merged is the rebased `d1f97a63`/tree `a4cd61e7`.

Verdict: BROKEN CHAIN for #1697. The verdict was written against a head that never merged, and no verdict was written at the merged SHA `4b3a3559`. This matches the reported fall exactly. Non-blocking (the three one-word replacements are identical in effect across both trees and the content diff is scoped), but it violates §5.2 (no self-acceptance: acceptance evidence at `708f5c5c8` was never reviewed at the SHA that landed). A corrective action would be a re-run of the exact-docs gate on the refreshed head, or at minimum a verdict file written against `4b3a3559`.

## V3 — Exact-head runs on the current head

Method witness: `gh api repos/mcpdev80/baseharbor/pulls/<n> --jq '.head.sha'` then `gh api .../actions/runs?event=pull_request&per_page=100 --jq '[.workflow_runs[]|select(.head_sha=="<head>")]...'` scoped to each PR head.

- PR #1702 (0428-142) head `6740299f91c040af7b1357d63be898eac57669f5`: run `44621032956` `success`, `pull_request`, 2026-11-19T21:39:56Z. base_sha `28fb427f`. lane-base -> develop range free of `.github/workflows/ci.yml`, `scripts/pr-gate-plan.py`, `scripts/plan.py`, `scripts/test_pr_*`/`test_ci_*` -> empty (clean). Valid exact-head run.
- PR #1693 (0428-123) head `93eea495437f2f9b4683211f9aafb24fd1798839`: run `44621387502` `success`, `pull_request`, 2026-11-19T21:42:02Z. base_sha `28fb427f`. lane-base -> develop range clean. Valid exact-head run.
- PR #1684 (0428-083) head `92509fde1929976e569b1fb5e9a8d401cbaaf413`: run `44631856770` `failure`, `pull_request`, 2026-11-19T22:47:19Z, head_branch `lane-0428-083-datasources-r2`. Failing job `PR · Source format` (job id `135940274702`), log line `##[error]Process completed with exit code 1` at `2026-11-19T22:47:40.6246921Z`, from `bash scripts/source-readability-audit.sh` + `gofmt -l` on the PR's own `.go` files (`git diff --name-only --diff-filter=ACMRT "$format_base" "$INTEGRATION_SHA" -- '*.go'`). `PR Selected Checks` aggregate = `failure`. Many release/draft/native cells `skipped` by CI-policy selection (not by an ORAS error). STATE only — per the scope split I do not rerun, repair, or touch `.github/**`. The gofmt failure is on the PR's own changed files, not the planner files, so it is a genuine format defect on head `92509fde`, not a planner-vs-develop base difference.

## V4 — Skipped-balance

- Review of the wave akten (e.g. `regvisibility-r3/fix-3.md`, `perses-alerts-hopf/fix-2.md`, `appclass-writer/fix-1.md`) shows they all state `SKIPPED != pass` explicitly and enumerate which mandatory jobs (Go build/vet/unit) actually executed. No SKIPPED cell is reported as pass in the sampled akten.
- Run `44631856770` (#1684): the `skipped` cells are release/draft/native-targeted runtime gates (Targeted HA docker/podman, PR · Main release Go/source, Draft shards, Native · matrix.id, Runner Interface, Exact Candidate, Candidate-added advisory, Consumer Pins, Native Keycloak/Core, Demo Pin, Public Contracts, Selected Runtime, Selected Core-less, Main release checks) — 20 cells skipped by path-based CI-policy selection, none covering the `internal/metrics` diff path. The mandatory Go build/vet/shard paths all executed. This is a correct skip, not an ORAS precondition failure.
- The mission's specific concern (docker-runtime-acceptance.yml lines 174-330 vs 127-128) is a path-selection difference between the two workflow shapes; it does not surface as a skipped cell being counted as pass in the sampled evidence. No V4 finding.

## V5 — Board truth

- All 172 tasks tagged `release: v0.4.28` are present as links in `views/releases/v0.4.28.md` — 0 missing. The release-view renderer (`scripts/plan.py` line 1024: `items = [t for t in vault.tasks.values() if t["release"] == r["id"]]`) filters only by release, not by status. The mission's "planned cards excluded from the releases view" claim does not hold under the current render code. Witness: a per-card grep for each `t-...` id against the rendered view returns present for all 172.
- My own card `t-20261119-r28-window-integrity-verify` has `kanban_status: active` and appears in the releases view (line 180: active, owner `w150-pr0428-150-windowverify`).
- The `review-compliance` audit (card 0428-139, same window) independently corroborates the board-truth class: draft PRs (`draft=true`) sit on `review` with skipped cells (#1625/#1623/#1614/#1595/#1580/#1597), a `dirty` mergeable_state (#1580/#1597/#1665), and closed PRs still on `review` (#1603/#1619/#1610). These are coordination facts for the Maintainer; I did not change any card status.

## V6 — Double-work

- The reported case: 0428-152 hangs off 0428-142 because both touch `cmd/baha/app_status_collect.go`. Checked the live PRs: PR #1693 (0428-123) and PR #1704 (0428-073).
- Witness via GitHub `/files` API (clean, no local-tree pollution):
  - PR #1693 files: `internal/metrics/prometheus_files.go`, `internal/metrics/prometheus_render.go`, `internal/metrics/regvisibility_regression_test.go`.
  - PR #1704 files: `internal/metrics/perses_prometheus_alerts.go`, `internal/metrics/perses_prometheus_alerts_test.go`.
- Neither PR touches `cmd/baha/app_status_collect.go`. Their changed files are disjoint (metrics vs perses-alerts). No same-file-same-direction overlap between #1693 and #1704 in current source.
- The reported overlap does not hold: `app_status_collect.go` is not in either PR's file list. If 0428-152 still intends to share that file with an 0428-142 workstream, that is a forward-dependency concern for the Maintainer to sequence, not an active collision between two open PRs. No V6 finding (reported case not reproduced).

## Befunde

1. #1697 verdict-chain break — non-blocking. PR merged at `4b3a3559`, verdict written for head `708f5c5c8` (tree `861191a1`), merged tree is `a4cd61e7` (rebased `d1f97a63`), and no verdict exists at the merged SHA. Corrective: re-run the exact-docs gate on the refreshed head `d1f97a63`/`4b3a3559`, or write a verdict file against `4b3a3559` before treating #1697 as accepted (§5.2). Does not block the wave (content is identical in effect), but it is exactly the acceptance-evidence gap V2 asks for.
2. PR #1684 (0428-083) exact-head run `44631856770` FAILED — SOURCE (per scope split, no rerun). Job `PR · Source format` (id `135940274702`), `##[error]Process completed with exit code 1` at 2026-11-19T22:47:40.6246921Z from `bash scripts/source-readability-audit.sh` + `gofmt -l` on the PR's own changed `.go` files. Aggregate `PR Selected Checks` = failure. Head `92509fde` is the current #1684 head. The failure is a real format defect on the PR, not a planner-vs-develop base difference (planner files are excluded from the gofmt diff). Left for the lane to fix; not touching `.github/**` or rerunning.
3. No board-truth defect (V5): all 172 v0.4.28 tasks render in the releases view; planned cards are not excluded under the current `scripts/plan.py` line 1024 logic. The planned-card-exclusion hypothesis from the mission is not reproduced.
4. No double-work defect (V6): the reported `cmd/baha/app_status_collect.go` collision between the 0428-142/0428-152 workstreams does not exist as an open PR-vs-PR overlap in current source (#1693 and #1704 are disjoint metrics files).
5. Coordination facts (not blocking, for the Maintainer): draft PRs on `review` with skipped cells (#1625/#1623/#1614/#1595/#1580/#1597), a `dirty` mergeable_state (#1580/#1597/#1665), and closed PRs still on `review` (#1603/#1619/#1610). Corroborated by the 0428-139 review-compliance audit in the same window.

## Formal

- No PR opened, no merge, no push on baseharbor. baseharbor/** untouched. No `.github/**` edit. No rerun/dispatch. No card status changed. No subagent.
- Evidence zone: `/tmp/150v2-plan` (fresh clone, `git rebase origin/main` before writing) and `/tmp/150v2-baha` (fresh baseharbor clone). The quarantined checkout `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` was not cited. Remote truth came only from `gh api` + `git ls-remote origin`.
