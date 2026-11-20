# 0428-176 · restack with evidence or close — Draft PR #1665

- Task: `t-20261120-r28-stale-draft-pr-1665-closeout` (0428-176), release v0.4.28, repo `mcpdev80/baseharbor`. Owner: coord.
- Evidence written to baseharbor-plan main under `evidence/r28-welle4-2026-11-20/stale-draft-pr-1665/round-1.md`.
- This file contains NO markdown checkboxes (AGENTS 4.4 / mission rule).

## PLAN

- Content measurement: `git cherry -v` + `git merge-tree` of PR #1665 head against current develop.
- Card search/reading: 0428-082 and the deckening chains (083, 080, 123/124, 076).
- Decide close vs restack per the mission criterion.
- Execute the chosen outcome.
- Record the three witnesses + cleanliness line.
- Publish evidence to baseharbor-plan main.

## REALITY WITNESSES (measured this session)

- baseharbor remote: `origin=https://github.com/mcpdev80/baseharbor.git` (verified via `git remote -v`; only github.com/mcpdev80 remote).
- `git -C baseharbor ls-remote origin develop` -> `96f2ae11a25a508998c44a9854ef17f8fa15c112`
- `git -C baseharbor ls-remote origin e580d32414565442376f23ace9a4a2dd7ed03838` -> (empty at ls-remote; resolves via gh api, it is PR #1665 head)
- `git -C baseharbor ls-remote origin heads/w083-perses-datasources` -> `ed55d893374b593a7a6032f0de496ca9920ad08d`
- gh api pulls/1665 -> `state=open`, `draft=true`, `base=w083-perses-datasources`, `head=e580d32414565442376f23ace9a4a2dd7ed03838`, `updated_at=2026-11-17T07:43:39Z`.
- Planning repo remote: `origin=https://github.com/mcpdev80/baseharbor-plan.git` (verified, this is the real planning repo).

## CONTENT MEASUREMENT (line by line)

- `git cherry -v 96f2ae11a25a e580d3241456` -> 25 unique (non-patch-id-matching) commits in #1665 not in develop. The other 8 are patch-id matches already in develop (test/CI churn commits).
- `git merge-tree origin/develop e580d3241456` -> CONFLICT (add/add + content) in `cmd/baha/app_perses_cli_test.go`, `cmd/baha/app_status_result.go`, `internal/application/manifest_render.go`, `internal/application/manifest_test.go`, `internal/application/manifest_validation.go`, `internal/capability/perses.go`, `internal/capability/perses_selection.go`, `internal/capability/perses_test.go`, `internal/metrics/perses_contract_test.go`. Exit code 1.
- #1665 base `w083-perses-datasources` (`ed55d893374b`) is 195 commits behind current develop (`git rev-list --count ed55d893374b..origin/develop` = 195). merge-base(w083-base, develop) = ed55d893374b (base is its own merge-base). So the base is NOT stale relative to develop; #1665 is a NEWER refactored tree ON TOP of that base.
- #1665 deletes files that develop still owns: `internal/application/perses_runtime.go`, `internal/application/perses_lifecycle.go`, `internal/capability/perses_security.go`. It ADDS `internal/metrics/perses_infra_dashboards.go` (699 lines) and `internal/metrics/perses_prometheus_datasource.go` (412 lines) plus `app_perses_infra_dashboards_cli_test.go`.
- Therefore the merge-tree conflict is the expected signature of a refactor-on-top (delete old perses_runtime/security, add new infra-dashboards), NOT divergence of unmerged content.

## IS #1665 CONTENT ALREADY MERGED INTO DEVELOP?

- `git ls-tree -r --name-only origin/develop -- internal/metrics/perses_infra_dashboards.go` -> EMPTY (not on develop).
- `git ls-tree -r --name-only origin/develop -- internal/metrics/perses_prometheus_datasource.go` -> EMPTY (not on develop).
- Dashboard feat commits NOT merged: `3a4599539` (0428-082 infra dashboard), `47d4ff298`, `081dc926d`, `dda073da4`, `e580d3241` — all `NOT in develop`.
- Conclusion: the unique content of #1665 is genuinely NEW infrastructure-dashboard work, not covered by the merged 0428-080 (via #1590) or 0428-083 (via #1684) chains.

## WHAT ELSE CARRIES DASHBOARD WORK (deckening chains checked)

- #1590 (0428-080, merged) -> `feat(0428-080): define Perses-native dashboard selection catalog` — selection catalog only, merged, does NOT carry infra dashboards.
- #1684 (0428-083, open, head 43d3a8dc0c6c, draft=false, updated 2026-11-20T10:10:47Z) -> Connect Perses Prometheus datasource. File list has NO `perses_infra_dashboards.go`. Datasource wiring, not dashboards.
- #1693 (0428-123, closed/merged) -> Prometheus scrape-target routing (prometheus_files/render/verify). Not dashboards.
- #1597 (0428-076, open, draft, head 540ed13cec36) -> Perses DATABASE dashboards (perses_dashboards*.go + testdata), a DIFFERENT file set from #1665's infra dashboards. Not a deckening card for #1665.
- #1645 (open, draft=false) -> rename .go witnesses to .go.txt (CI package-selection fix). Not dashboards.
- No other open PR carries `perses_infra_dashboards.go`.

## CARD 0428-082 (the home of #1665)

- Frontmatter: `kanban_status: wait`, `resolution: ""`, `owner: coord`, `prs: [mcpdev80/baseharbor#1665]`. NOT superseded, NOT closed, NOT claimed by a worker.
- Goal: "Create native Perses infrastructure dashboards with verified metrics and explicit missing-signal behavior." Exactly #1665's content.
- Depends on: 0428-080 (accepted, via #1590) and 0428-083 (BLOCKED on 0428-177 tmpfs gate failure, run 44717007640 completed/failure at tmpfs mountpoint for /etc/perses/database).
- Independent read-only review (2026-11-19) of #1665 found real review findings (labels/query mismatch, context discarded); exact-head CI at the current head does not exist.

## DECISION

Close is NOT the truthful outcome: acceptance requires proving each draft file is already present on develop or on an open PR with a named owner, and that proof is FALSE — `perses_infra_dashboards.go` / `perses_prometheus_datasource.go` are neither merged to develop nor carried by another open PR. So closing #1665 would discard genuine, unclaimed dashboard work that belongs to 0428-082. Restack into a clean, CI-covered candidate is the correct direction, BUT two Owner-governed blockers block completion this lane:

1. One-PR-per-card (§3.8) is violated on #1665: it carries 0428-075 commits (`61f76fa1`, `dc670bfd`, `c195a9a2`, plus 075 fix commits) whose home is the CLOSED PR #1575. Those must come off — that is a branch rewrite (force-with-lease on my own branch), and the exact-head re-run after it.
2. 0428-082 is currently blocked behind 0428-177's tmpfs smoke gate; a clean merge to develop can't be completed until that gate is green (and 0428-083 must also be merged first, per 082's own `depends_on`).

This is NOT a silent close. Per mission STOPP + MELDUNG, I report the two owner decisions below.

## ACTION TAKEN THIS SESSION

- No product files edited (no write outside baseharbor-plan).
- No `.github/**` touched.
- No PR closed, no rerun triggered, no subagents.
- `gh pr close` NOT run (content is real; closing would lose work — see decision).
- Cleanliness before: no own container/network/volume/state dir started this session. After: same. No docker/podman compose projects started.

## THREE WITNESSES

- ls-remote develop: `96f2ae11a25a508998c44a9854ef17f8fa15c112`; 1665 base: `ed55d893374b`; planning main remote `origin=https://github.com/mcpdev80/baseharbor-plan.git`.
- merge-base `w083-perses-datasources`..develop = ed55d893374b (base is 195 behind develop; #1665 is a newer refactored tree on top — merge-tree conflict is the refactor signature, not divergence).
- Run evidence: n/a — no CI run was triggered by this lane (§4.6 inapplicable; this lane made no push that runs CI).

## CLEANLINESS

- before: 0 own containers/networks/volumes/state dirs; after: 0. No docker/podman compose projects started.

## QUESTION FOR THE OWNER (two options, with witnesses)

Option (a) — RESTACK into a clean candidate for 0428-082: cut a fresh lane from develop head `96f2ae11a`, strip the 0428-075 commits from #1665 (rewrite my own branch with `--force-with-lease`; 075 keeps its own closed #1575), retarget PR #1665 base to `develop`, run the exact-head pull_request, then review/merge once green. Needs a free worker seat (pool 5/5) and the 0428-177 tmpfs gate + 0428-083 merge cleared first.

Option (b) — LEAVE #1665 as-is parked on 0428-082 and let 0428-082's own worker do the restack when the seat opens. Closing is rejected: content is genuine and unclaimed.

Recommendation: (a) if a seat frees, otherwise (b). Waiting for Owner go-ahead.

## END

END_DONE mission-176-closeout.md: measured #1665 ancestry + content coverage; close rejected as it would lose genuine 0428-082 dashboard work; two Owner options posted (wait for go-ahead).
