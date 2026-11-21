# Evidence: 0428-216 PR inventory rebuild (round 2)

## Lane / Mission
- Lane: ca3b8b21 (0428-216-prsweep2), task slice H-V27 (mechanical inventory, pure findings, no product change)
- Mission: `/var/tmp/h27.txt`
- Worktree: none needed (read-only inventory in the shared baseharbor checkout; no product writes, no PR actions)
- Planning repo remote witness (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`):
  `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)` — correct planning repo, not workers/.
- Baseharbor remotes (`git remote -v` in /home/marcel/dev/baseharbor-ecosystem/baseharbor): `lane-origin`, `origin` and `upstream` all resolve to `https://github.com/mcpdev80/baseharbor.git`; every measurement was issued explicitly against `lane-origin`.

## PLAN
1. Reality check: remotes, fetch develop, record base SHA
2. Base list via `gh pr list --state open --limit 60 --json number,headRefOid,baseRefName,isDraft`
3. Per-PR file sets (`gh pr view --json files` cross-checked against `git diff --name-only`)
4. Per-PR ancestry `git merge-base --is-ancestor lane-origin/develop <head>` with explicit exit codes
5. Per-PR patch-id (fetched pull refs, corrected three-dot method)
6. Last-commit timestamps (UTC)
7. Classification (eigene Kette / owner-Stapel / Dublette / verwaist) + duplicate scan
8. Cleanliness witnesses `docker ps -a`
9. Write round-2.md, commit, push, verify on origin/main
10. END post with plan SHA

## Base attestation
- `git ls-remote lane-origin refs/heads/develop` => `40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop` (committer 2026-11-20T16:06Z, unchanged since round 1)
- Head SHAs measured via `git fetch lane-origin '+refs/pull/*/head:refs/pull/*/head'` (1361 pull head refs) plus a final `gh pr list` re-pull; the second pass showed exactly one moved head (#1726: 0906b043db98 → 221b6f437ea8 at 03:58Z). Every other row is identical across both passes.
- patch-id method note: `git diff <base>...<head>` literally diffs merge-base vs merge-base (empty). The mission intent is realized as `mb=$(git merge-base <base-sha> <head>); git diff $mb <head> | git patch-id --stable`. That is the method used below; file counts use the same ranges.
- All timestamps are UTC committer dates (`TZ=UTC git log -1 --format=%cI`); raw dates are CET.

## Table (34 open PRs)

`a(dev)` = exit code of `git merge-base --is-ancestor lane-origin/develop <head>` (0 = develop 40cb28c7 is an ancestor; 1 = not). `base-sha` = remote tip of the base ref at measurement. `head vs base` = ahead/behind counts against the base ref.

| PR | card | head-sha (12) | base-ref @ sha | a(dev) | head vs base | draft? | last commit (UTC) | patch-id (12) | own files (n + first 2) | einordnung |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1739 | 0428-210 | 79d962a063be | develop @ 40cb28c758b0 | 0 | 1/0 | no | 2026-11-21T03:48:57 | 75cad9250850 | 1, cmd/baha/app_commands.go | eigene Kette (busy session 6fa94f11, just pushed) |
| 1738 | 0428-214 | ebc6ac9c3a30 | lane-0428-198... @ 221b6f437ea8 | 1* | 1/1 (drift) | no | 2026-11-21T03:13:32 | 1b44fd78fc8f | 1, cmd/baha/core_installation_runtime_test.go | eigene Kette (stacked on #1726, base drifted) |
| 1737 | 0428-213 | d0399968c47f | lane-0428-198... @ 221b6f437ea8 | 1* | 1/1 (drift) | no | 2026-11-21T03:24:19 | 056e872aedbc | 2, cmd/baha/trust_status_regression_test.go, cmd/baha/trust_uninstall_test.go | eigene Kette (stacked on #1726, base drifted) |
| 1736 | 0428-217 gate routing | 8f11a34da52f | develop @ 40cb28c758b0 | 0 | 1/0 | DRAFT | 2026-11-21T03:08:45 | 7363b569d470 | 4, scripts/pr-gate-coverage.json, scripts/pr-gate-plan.py | owner-Stapel (owner's draft) |
| 1735 | 0428-207 | b10dc56b785c | develop @ 40cb28c758b0 | 0 | 4/0 | no | 2026-11-21T03:28:12 | 3ee2bf6f4410 | 2, cmd/baha/core_network_binding.go, cmd/baha/core_network_binding_actionability_test.go | eigene Kette (session 47aef7ca idle, fix2 just pushed) |
| 1734 | 0428-212 | 45d181ab4089 | develop @ 40cb28c758b0 | 0 | 1/0 | no | 2026-11-21T01:59:25 | 8b941d38f74a | 1, internal/logs/loki_test.go | eigene Kette (supersedes closed #1732 — duplicates) |
| 1733 | 0428-211 | 3a8b4a8b11de | develop @ 40cb28c758b0 | 0 | 1/0 | no | 2026-11-21T00:28:05 | ddb427a22e40 | 2, internal/application/perses_management_ui.go, internal/application/perses_management_ui_test.go | eigene Kette (in review) |
| 1731 | 0428-179 | f90b3f448caf | develop @ 40cb28c758b0 | 0 | 2/0 | no | 2026-11-20T20:31:32 | 4c727b074673 | 2, .github/workflows/ci.yml, cmd/baha/context_terminal_test.go | owner-Stapel (owner codex/ branch, touches .github/**) |
| 1730 | 0428-203 | c90a73ac8128 | lane-0428-143... @ 809a8196e1cf | 0 | 1/0 | no | 2026-11-20T20:29:48 | 18fa4c09664f | 2, internal/capability/integration_contract.go, internal/metrics/prometheus_verify_witness_test.go | eigene Kette (stacked cleanly on #1729) |
| 1729 | 0428-143 | 809a8196e1cf | develop @ 40cb28c758b0 | 0 | 1/0 | no | 2026-11-20T19:42:12 | 833cfb88d873 | 3, internal/capability/integration_contract.go, internal/metrics/prometheus_verify.go | eigene Kette (base of #1730 stack; session e330ee18 busy) |
| 1728 | 0428-200 | 6e3122344f87 | develop @ 40cb28c758b0 | 0 | 1/0 | no | 2026-11-20T19:39:43 | c0253bdb2b1a | 5, cmd/baha/app_context.go, cmd/baha/w200_deployment_version_mismatch_test.go | eigene Kette (in review) |
| 1726 | 0428-198 | 221b6f437ea8 | develop @ 40cb28c758b0 | 0 | 6/0 | no | 2026-11-21T03:58:55 | 820b64bb3a91 | 15, cmd/baha/agent_mcp_test.go, cmd/baha/app_init_retained_identity_test.go | eigene Kette (base of #1737/#1738; head moved mid-sweep) |
| 1725 | 0428-201 | 9bf4a72f742b | develop @ 40cb28c758b0 | 0 | 1/0 | no | 2026-11-20T18:43:10 | 484c197e72d6 | 3, internal/application/shared_backends.go, internal/application/shared_backends_state_version_test.go | eigene Kette (in review) |
| 1724 | 0428-177 | 408b18d2dc7b | develop @ 40cb28c758b0 | 0 | 2/0 | no | 2026-11-20T18:33:04 | c66d6c609031 | 8, internal/application/perses_fix7_regression_test.go, internal/application/perses_tmpfs_mountpoint_test.go | eigene Kette (base ref of #1684, live) |
| 1723 | 0428-199 | 26755fc1edfb | develop @ 40cb28c758b0 | 0 | 1/0 | no | 2026-11-20T17:55:10 | 7c7d284f976f | 4, cmd/baha/app_apply.go, cmd/baha/app_workload_ports.go | eigene Kette (in review) |
| 1718 | 0428-178 | ce5aa9633630 | develop @ 40cb28c758b0 | 0 | 1/0 | no | 2026-11-20T16:32:49 | 293adca6963e | 1, cmd/baha/context_terminal_test.go | eigene Kette (in review; same file as #1731) |
| 1714 | 0428-183 | 5159192dadee | develop @ 40cb28c758b0 | 1 | 2/0 | no | 2026-11-20T16:54:08 | 66705526966a | 4, internal/metrics/perses_dashboards_valkey.go, internal/metrics/perses_dashboards_valkey_test.go | verwaist (stale base, no session, no live lane) |
| 1704 | 0428-073 | f5dcf1288548 | develop @ 40cb28c758b0 | 1 | 198/0 | no | 2026-11-19T21:44:40 | 9b0c9f20c979 | 337, .github/workflows/ci.yml, .github/workflows/docker-runtime-acceptance.yml | owner-Stapel (owner r28 correction branch) |
| 1702 | 0428-142 | e21b5c528923 | develop @ 40cb28c758b0 | 0 | 2/0 | no | 2026-11-21T01:26:29 | ead0b22da274 | 3, cmd/baha/app_status_result.go, cmd/baha/app_status_result_test.go | eigene Kette (session e330ee18 busy, hopfix) |
| 1684 | 0428-083 | b71c6da27e8b | perses-tmpfs-mountpoint-wt @ 408b18d2dc7b | 1* | 1/1317 | no | 2026-11-20T19:02:09 | (empty own diff) | 0 | eigene Kette (stack on #1724, far behind its base — see duplicates) |
| 1665 | 0428-082 | db27880c108a | lane-0428-083-datasources-r2 @ b71c6da27e8b | 1* | 1/1 | no | 2026-11-20T21:19:57 | (empty own diff) | 0 | eigene Kette (stack on #1684, behind its base) |
| 1650 | 0428-078 | 28c18f02039f | develop @ 40cb28c758b0 | 0 | 6/0 | no | 2026-11-21T00:48:01 | 6ee094fd41dd | 6, cmd/baha/app_status_perses_gate_test.go, cmd/baha/app_status_result.go | eigene Kette (in review) |
| 1645 | perses fix6 rename | 4d73aa97808d | develop @ 40cb28c758b0 | 1 | 1/0 | no | 2026-11-20T20:37:46 | 1f3b3b804233 | 35, internal/application/perses_fix6_regression_test.go, internal/capability/perses.go | verwaist (cut before #1712 merged — merge-base 96f2ae11a25a; no session) |
| 1627 | 0428-055 | 202b984e2a10 | develop @ 40cb28c758b0 | 0 | 8/0 | DRAFT | 2026-11-21T01:49:34 | 3fd5684bcf57 | 9, cmd/baha/commands.go, cmd/baha/env_destroy.go | eigene Kette (draft; file overlap with cli2 stack) |
| 1625 | 0428-065 | 010db47dae0e | cli2-identity-secrets-head @ 760bc0f55c6f | 1 | 9/0 | DRAFT | 2026-11-19T23:39:31 | 0fc06eddc191 | 8, cmd/baha/app_export.go, cmd/baha/app_export_command_test.go | owner-Stapel (owner hold on cli2-identity-secrets-head) |
| 1623 | 0428-063 | 4cbf92960cb5 | cli2-identity-secrets-head @ 760bc0f55c6f | 1 | 9/0 | DRAFT | 2026-11-20T10:43:46 | a41014d93619 | 20, cmd/baha/app_access.go, cmd/baha/app_access_urls.go | owner-Stapel (owner hold on cli2-identity-secrets-head) |
| 1620 | 0428-067 | 28cb907dc0a6 | develop @ 40cb28c758b0 | 0 | 7/0 | no | 2026-11-21T01:17:12 | e7b76fbe4384 | 2, cmd/baha/app_access.go, cmd/baha/app_access_test.go | eigene Kette (app_access.go overlap with #1623, not a duplicate) |
| 1615 | 0428-057 | 760bc0f55c6f | develop @ 40cb28c758b0 | 0 | 240/0 | no | 2026-11-21T03:50:13 | 42e04751e9be | 161, .github/workflows/ci.yml, .github/workflows/pre-release-runtime-suite.yml | owner-Stapel (cli2-identity-secrets-head branch itself, live pushes) |
| 1614 | 0428-062 | 80d4df52e913 | develop @ 40cb28c758b0 | 1 | 8/0 | DRAFT | 2026-11-16T09:32:06 | 206750f88ce8 | 37, cmd/baha/app_edit_apply_test.go, cmd/baha/app_observe.go | verwaist (stale base, 5 days, no session) |
| 1597 | 0428-076 | 90063f6ec66c | develop @ 40cb28c758b0 | 0 | 4/0 | no | 2026-11-20T20:27:59 | 77005dcdf726 | 13, cmd/baha/app_perses_cli_test.go, cmd/baha/app_status_result.go | eigene Kette (re-hopped today) |
| 1596 | 0428-056 | 6135e73a6e2c | develop @ 40cb28c758b0 | 0 | 7/0 | no | 2026-11-21T00:57:04 | 5b55fd4a4a43 | 4, internal/orgconfig/effective.go, internal/orgconfig/model.go | eigene Kette (in review) |
| 1588 | 0427-186 | 9534edd49c20 | develop @ 40cb28c758b0 | 1 | 2/0 | DRAFT | 2026-11-15T16:30:23 | 7f1a412b48f6 | 7, cmd/baha/app_remote_lifecycle.go, cmd/baha/deployment_record.go | verwaist (stale base, 6 days, no session) |
| 1587 | 0427-169 | 20e0537cc333 | develop @ 40cb28c758b0 | 1 | 1/0 | DRAFT | 2026-11-15T11:29:10 | 8202a280cb8f | 9, cmd/baha/serve.go, docs/cli/automation-agents.md | verwaist (stale base, 6 days, no session) |
| 1585 | 0428 bf01-fix v2 | b50bc6a8053d | develop @ 40cb28c758b0 | 0 | 10/0 | DRAFT | 2026-11-21T00:13:12 | e6176c83caee | 6, cmd/baha/target.go, cmd/baha/target_selection.go | eigene Kette (re-hopped today, draft) |

`1*` = head is not a direct develop-descendant because it sits on a stacked base branch; the ownership question is answered by the stack, not by a hop. Stack health (measured): #1730 is a clean child of #1729's current head (1/0). #1737 and #1738 were each 1-ahead/1-behind #1726's NEW head 221b6f43 (pushed 03:58Z mid-sweep): their bases drifted — merge order #1726 → rebase-or-merge #1737/#1738. #1684 sits 1317-behind/1-ahead of #1724's head and #1665 1-behind/1-ahead of #1684: their own diffs against their base refs are EMPTY (the base ref already contains the head content), so the chain #1724 → #1684 → #1665 currently contributes nothing above #1724.

## Dubletten-und-verwaiste

- No two open PRs share a patch-id (measured against develop and against their own base refs). The only equality is the EMPTY-vs-base pair #1684/#1665 — a degenerate stack state, not a content duplicate.
- Headline case #1732 vs #1734 (the mission's example 75770bd2d043 vs bddb27e6251): both SHAs are heads of PR #1732, which is now CLOSED; #1734 (head 45d181ab) touches the same file, internal/logs/loki_test.go. Pairwise ancestry checks: no relation between any of the three; all three patch-ids differ (75770bd2 → d00847f19fd8, bddb27e6 → c5161717889b, 45d181ab → 8b941d38f74a). #1734 supersedes both #1732 heads; no open duplicate remains.
- File overlaps (bind merge order, not supersession):
  - cmd/baha/app_commands.go: #1739 vs #1615 (owner cli2 branch carries the file).
  - cmd/baha/app_access.go: #1620 vs #1623 vs #1615.
  - cmd/baha/commands.go + machine_coverage.go + cli/command-index docs: #1627 vs #1623 vs #1625.
  - cmd/baha/context_terminal_test.go: #1718 vs #1731 (and #1615 carries it).
  - cmd/baha/app_edit_apply_test.go: #1614 vs #1615.
  - cmd/baha/app_status_result.go: #1650/#1702/#1597 all touch it, and #1615 carries it.
- #1625 and #1623 share the identical merge-base ae2d022c8dc9 against develop and are not ancestors of one another — parallel children of an older cli2 snapshot, both under the owner's cli2-identity-secrets-head hold. #1627's head IS a develop-descendant (a(dev)=0); its overlap with them is file-level only.
- Stale-base hop candidates (a(dev)=1, unstacked): #1714, #1645, #1614, #1588, #1587; plus #1704 (198-ahead owner branch) and cli2-stack heads #1625/#1623 stay owner decisions, not hops. None of #1714/#1645/#1614/#1588/#1587 has a live session (witness below) — all verwaist.
- Newest batch: #1737/#1738 (stacked fresh), #1739 (fresh develop branch), #1736 (owner draft) — plus moved heads #1735 (fix2), #1734 (correction), #1726 (correction), #1732 closed/merged since round 1.

## Was sich seit 0428-216 (round 1, table eb3d13d7 / merge 5b1bf3f2) geaendert hat

- Round 1: 30 open PRs → now 34. develop unchanged at 40cb28c7 — the null-hops finding still holds.
- NEW: #1737 (0428-213), #1738 (0428-214) stacked on #1726's branch; #1739 (0428-210) fresh; #1736 (owner draft, pr-gate routing).
- MOVED heads: #1726 0906b043→221b6f43 (03:58Z), #1735 →b10dc56b (03:28Z), #1734 →45d181ab (01:59Z), #1615 →760bc0f5 (03:50Z, owner), #1650, #1620, #1627, #1597 re-hopped/updated today.
- CLOSED since round 1: #1732 (merged via #1734).
- Owner hold restated: #1615/#1625/#1623 on cli2-identity-secrets-head (owner's words in the mission); #1704/#1731/#1736 owner branches.
- Still-true round-1 rows: all a(dev)=0 develop-based PRs need no hop; hop-needed set is unchanged: #1714, #1645, #1614, #1588, #1587.

## Command witnesses

- `gh pr list --repo mcpdev80/baseharbor --state open --limit 60 --json number,headRefOid,baseRefName,isDraft` (run twice; only #1726 moved between passes).
- `git fetch lane-origin '+refs/pull/*/head:refs/pull/*/head'` => 1361 refs.
- Ancestry per row: `git merge-base --is-ancestor lane-origin/develop <head>`, exit codes in column a(dev). #1714 rechecked twice, exit 1 both times.
- patch-id per row: `git diff <merge-base(base,head)> <head> | git patch-id --stable`, first 12 hex.
- ls-remote witness: `git ls-remote lane-origin refs/heads/cli2-identity-secrets-head refs/heads/lane-0428-143-verify-none refs/heads/perses-tmpfs-mountpoint-wt refs/heads/lane-0428-083-datasources-r2 refs/heads/lane-0428-198-cli-shard-operator-env refs/pull/1684/head refs/pull/1665/head` => 760bc0f55c6f / 809a8196e1cf / 408b18d2dc7b / b71c6da27e8b / 221b6f437ea8 / b71c6da27e8b / db27880c108a.
- Live sessions (`codeman agent list --json`): 9142ab1f idle (coordinator), 95971e0a idle (codex-rev-cli2b), 47aef7ca idle (0428-207-appedit-fix2), 6fa94f11 busy (0428-210-alltargets), e330ee18 busy (0428-142-hopfix), d23205ac busy (0428-204-huntnumbers), ca3b8b21 busy (this lane). The verwaist rows have no owner among these.

## cleanliness

- Before (`docker ps -a` on this host — the coordinator/codeman server): `de40a6c61cef bh-docker-dev-edit-runtime-integration-dev-api-1 Exited (0) 38 minutes ago`
- After: identical — `de40a6c61cef bh-docker-dev-edit-runtime-integration-dev-api-1 Exited (0) 42 minutes ago`. This lane started nothing; no compose project, no container, no volume; no `go test` on this host (per mission).

## END
END_DONE 0428-216-prsweep2: 34-PR inventory rebuilt (ancestry/patch-id/timestamps/duplicates), no duplicate patch-ids, hop candidates 1714/1645/1614/1588/1587, stack drift on 1737/1738 after 1726 moved — plan SHA in END post.
