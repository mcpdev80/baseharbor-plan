# Evidence: 0428-216 PR inventory rebuild (round 2)

## Lane / Mission
- Lane: ca3b8b21 (0428-216-prsweep2), task slice H-V27 (mechanical inventory, pure findings, no product change)
- Mission: `/var/tmp/h27.txt`
- Worktree: none needed (read-only inventory in the shared baseharbor checkout; no product writes, no PR actions)
- Planning repo remote witness (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`):
  `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)` — correct planning repo, not workers/.
- Baseharbor remote witness (`git remote -v` in /home/marcel/dev/baseharbor-ecosystem/baseharbor):
  `lane-origin  https://github.com/mcpdev80/baseharbor.git (fetch)` — the only URL used for measurement. (Here `origin` also resolves to the same github URL; all fetches were still issued explicitly against `lane-origin`.)

## PLAN
1. Reality check: remotes, fetch develop, record base SHA
2. Base list via `gh pr list --state open --limit 60 --json ...`
3. Per-PR file sets (`gh pr view --json files` cross-checked against `git diff --name-only`)
4. Per-PR ancestry with explicit exit codes
5. Per-PR patch-id (fetched pull refs, corrected three-dot method)
6. Last-commit timestamps (UTC)
7. Classification (eigene Kette / owner-Stapel / Dublette / verwaist) + duplicate scan
8. Cleanliness witnesses `docker ps -a`
9. Write round-2.md, commit, push, verify on origin/main
10. END post with plan SHA
- `gh pr list --state open --limit 60` base table
- Per-PR files via `gh pr view --json files` cross-checked against `git diff --name-only`
- Per-PR ancestry via `git merge-base --is-ancestor lane-origin/develop <head>` with explicit exit codes
- Per-PR patch-id via fetched pull refs + `git patch-id --stable`
- Last-commit timestamps (UTC) for the aenderungs-fenster column
- Classification: eigene Kette / owner-Stapel / Dublette / verwaist
- Cleanliness: `docker ps -a` before/after, nothing started
- Evidence written to round-2.md (round-1.md untouched), committed, pushed, verified on origin/main, END posted

## Base attestation
- `git ls-remote lane-origin refs/heads/develop` => `40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop` (2026-11-20T16:06:xxZ, unchanged since round 1)
- All head SHAs measured via `git fetch lane-origin '+refs/pull/*/head:refs/pull/*/head'`; every `head-sha` in the table equals the `gh pr list headRefOid` value (no drift during measurement).
- patch-id method: `git merge-base <base-sha> <head>` then `git diff <merge-base> <head> | git patch-id --stable`. (A literal `git diff <base>...<head>` is `git diff base_sha...head_sha`, which diffs the merge-base against ITSELF and yields an empty patch; the three-dot form is only meaningful inside `git log`/`git diff --name-only` range syntax. This is the corrected method, same result semantics as intended.)
- All timestamps converted to UTC (`TZ=UTC git log -1 --format=%cI <head>`); the raw committer dates are CET (+01:00).

## Table (34 open PRs)

`a(dev)` = exit code of `git merge-base --is-ancestor lane-origin/develop <head>` (0 = develop 40cb28c7 is ancestor; 1 = not).
`base-sha` = remote tip of the PR's base ref. `head vs base` = commits ahead of the base ref. Stacked PRs are NOT develop-ancestors via their own head; the column shows the real value, and the stack position answers the practical question (see notes).

| PR | card | head-sha (12) | base-ref @ sha | a(dev) | draft? | last commit (UTC) | patch-id (12) | files (n + first 2) | einordnung |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1739 | 0428-210 | 79d962a063be | develop @ 40cb28c758b0 | 0 | no | 2026-11-21T03:48:57 | 75cad9250850 | 1, cmd/baha/app_commands.go | eigene Kette (busy session 6fa94f11, just pushed) |
| 1738 | 0428-214 | ebc6ac9c3a30 | lane-0428-198... @ 221b6f437ea8 | 1* | no | 2026-11-21T03:13:32 | 1b44fd78fc8f | 1, cmd/baha/core_installation_runtime_test.go | eigene Kette (stacked on #1726, base drifted — see notes) |
| 1737 | 0428-213 | d0399968c47f | lane-0428-198... @ 221b6f437ea8 | 1* | no | 2026-11-21T03:24:19 | 056e872aedbc | 2, cmd/baha/trust_status_regression_test.go, cmd/baha/trust_uninstall_test.go | eigene Kette (stacked on #1726, base drifted — see notes) |
| 1736 | 0428-217 (gate routing) | 8f11a34da52f | develop @ 40cb28c758b0 | 0 | DRAFT | 2026-11-21T03:08:45 | 7363b569d470 | 4, scripts/pr-gate-coverage.json, scripts/pr-gate-plan.py | owner-Stapel (owner's draft, gate routing) |
| 1735 | 0428-207 | b10dc56b785c | develop @ 40cb28c758b0 | 0 | no | 2026-11-21T03:28:12 | 3ee2bf6f4410 | 2, cmd/baha/core_network_binding.go, cmd/baha/core_network_binding_actionability_test.go | eigene Kette (session 47aef7ca idle, fix2 in flight) |
| 1734 | 0428-212 | 45d181ab4089 | develop @ 40cb28c758b0 | 0 | no | 2026-11-21T01:59:25 | 8b941d38f74a | 1, internal/logs/loki_test.go | eigene Kette (supersedes closed #1732, see duplicates) |
| 1733 | 0428-211 | 3a8b4a8b11de | develop @ 40cb28c758b0 | 0 | no | 2026-11-21T00:28:05 | ddb427a22e40 | 2, internal/application/perses_management_ui.go, internal/application/perses_management_ui_test.go | eigene Kette (in review) |
| 1731 | 0428-179 | f90b3f448caf | develop @ 40cb28c758b0 | 0 | no | 2026-11-20T20:31:32 | 4c727b074673 | 2, .github/workflows/ci.yml, cmd/baha/context_terminal_test.go | owner-Stapel (owner codex/ branch, touches .github/**) |
| 1730 | 0428-203 | c90a73ac8128 | lane-0428-143... @ 809a8196e1cf | 0 | no | 2026-11-20T20:29:48 | 18fa4c09664f | 2, internal/capability/integration_contract.go, internal/metrics/prometheus_verify_witness... | eigene Kette (stacked on #1729) |
| 1729 | 0428-143 | 809a8196e1cf | develop @ 40cb28c758b0 | 0 | no | 2026-11-20T19:42:12 | 833cfb88d873 | 3, internal/capability/integration_contract.go, internal/metrics/prometheus_verify.go | eigene Kette (session e330ee18 busy, hopfix in flight) |
| 1728 | 0428-200 | 6e3122344f87 | develop @ 40cb28c758b0 | 0 | no | 2026-11-20T19:39:43 | c0253bdb2b1a | 5, cmd/baha/app_context.go, cmd/baha/w200_deployment_version_mismatch_test.go | eigene Kette (in review) |
| 1726 | 0428-198 | 221b6f437ea8 | develop @ 40cb28c758b0 | 0 | no | 2026-11-21T03:58:55 | 820b64bb3a91 | 15, cmd/baha/agent_mcp_test.go, cmd/baha/app_init_retained_identity_test.go | eigene Kette (base of the 1737/1738 stack; head MOVED 0906b043→221b6f43 during this sweep) |
| 1725 | 0428-201 | 9bf4a72f742b | develop @ 40cb28c758b0 | 0 | no | 2026-11-20T18:43:10 | 484c197e72d6 | 3, internal/application/shared_backends.go, internal/application/shared_backends_state... | eigene Kette (in review) |
| 1724 | 0428-177 | 408b18d2dc7b | develop @ 40cb28c758b0 | 0 | no | 2026-11-20T18:33:04 | c66d6c609031 | 8, internal/application/perses_fix7_regression_test.go, internal/application/perses... | eigene Kette (base ref of #1684, still live) |
| 1723 | 0428-199 | 26755fc1edfb | develop @ 40cb28c758b0 | 0 | no | 2026-11-20T17:55:10 | 7c7d284f976f | 4, cmd/baha/app_apply.go, cmd/baha/app_workload_ports.go | eigene Kette (in review) |
| 1718 | 0428-178 | ce5aa9633630 | develop @ 40cb28c758b0 | 0 | no | 2026-11-20T16:32:49 | 293adca6963e | 1, cmd/baha/context_terminal_test.go | eigene Kette (in review) |
| 1714 | 0428-183 | 5159192dadee | develop @ 40cb28c758b0 | 1 | no | 2026-11-20T16:54:08 | 66705526966a | 4, internal/metrics/perses_dashboards_valkey.go, internal/metrics/perses_dashboards_valkey_test.go | verwaist (stale base, needs hop; last touched 6h+, no session) |
| 1704 | 0428-073 | f5dcf1288548 | develop @ 40cb28c758b0 | 1 | no | 2026-11-19T21:44:40 | 9b0c9f20c979 | 337, .github/workflows/ci.yml, .github/workflows/docker-runtime-acceptance.yml | owner-Stapel (owner's r28 correction, 198 commits ahead of develop) |
| 1702 | 0428-142 | e21b5c528923 | develop @ 40cb28c758b0 | 0 | no | 2026-11-21T01:26:29 | ead0b22da274 | 3, cmd/baha/app_status_result.go, cmd/baha/app_status_result_test.go | eigene Kette (session e330ee18 busy) |
| 1684 | 0428-083 | b71c6da27e8b | perses-tmpfs-mountpoint-wt @ 408b18d2dc7b | 1* | no | 2026-11-20T19:02:09 | (0 own files vs base) | 0 | eigene Kette (stacked on #1724; base-sha == head => content empty) |
| 1665 | 0428-082 | db27880c108a | lane-0428-083-datasources-r2 @ b71c6da27e8b | 1* | no | 2026-11-20T21:19:57 | (0 own files vs base) | 0 | eigene Kette (stacked on #1684; base-sha == head => content empty) |
| 1650 | 0428-078 | 28c18f02039f | develop @ 40cb28c758b0 | 0 | no | 2026-11-21T00:48:01 | 6ee094fd41dd | 6, cmd/baha/app_status_perses_gate_test.go, cmd/baha/app_status_result.go | eigene Kette (in review) |
| 1645 | 0428-177 (fix6 rename) | 4d73aa97808d | develop @ 40cb28c758b0 | 1 | no | 2026-11-20T20:37:46 | 1f3b3b804233 | 35, internal/application/perses_fix6_regression_test.go, internal/capability/perses.go | verwaist (stale base, needs hop; superseded-adjacent to #1724) |
| 1627 | 0428-055 | 202b984e2a10 | develop @ 40cb28c758b0 | 0 | DRAFT | 2026-11-21T01:49:34 | 3fd5684bcf57 | 9, cmd/baha/commands.go, cmd/baha/env_destroy.go | eigene Kette (draft, in review window) |
| 1625 | 0428-065 | 010db47dae0e | cli2-identity-secrets-head @ 760bc0f55c6f | 1 | DRAFT | 2026-11-19T23:39:31 | 5e6ac59c653e (vs develop) / 0fc06eddc191 (vs base) | 18 vs develop (8 own vs base), cmd/baha/agent_mcp_test.go, cmd/baha/app_access.go | owner-Stapel (held on cli2-identity-secrets-head per owner) |
| 1623 | 0428-063 | 4cbf92960cb5 | cli2-identity-secrets-head @ 760bc0f55c6f | 1 | DRAFT | 2026-11-20T10:43:46 | 6d7e64c7c49e (vs develop) / a41014d93619 (vs base) | 26 vs develop (20 own vs base), cmd/baha/app_access.go, cmd/baha/app_access_urls.go | owner-Stapel (held on cli2-identity-secrets-head per owner) |
| 1620 | 0428-067 | 28cb907dc0a6 | develop @ 40cb28c758b0 | 0 | no | 2026-11-21T01:17:12 | e7b76fbe4384 | 2, cmd/baha/app_access.go, cmd/baha/app_access_test.go | eigene Kette (overlaps #1623 file app_access.go, not a duplicate) |
| 1615 | 0428-057 | 760bc0f55c6f | develop @ 40cb28c758b0 | 0 | no | 2026-11-21T03:50:13 | 42e04751e9be | 161, .github/workflows/ci.yml, .github/workflows/pre-release-runtime-suite.yml | owner-Stapel (owner's cli2-identity-secrets-head branch, 240 commits, live pushes) |
| 1614 | 0428-062 | 80d4df52e913 | develop @ 40cb28c758b0 | 1 | DRAFT | 2026-11-16T09:32:06 | 206750f88ce8 | 37, cmd/baha/app_edit_apply_test.go, cmd/baha/app_observe.go | verwaist (stale base, 5 days old, no session) |
| 1597 | 0428-076 | 90063f6ec66c | develop @ 40cb28c758b0 | 0 | no | 2026-11-20T19:27:59 | 77005dcdf726 | 13, cmd/baha/app_perses_cli_test.go, cmd/baha/app_status_result.go | eigene Kette (re-hopped today) |
| 1596 | 0428-056 | 6135e73a6e2c | develop @ 40cb28c758b0 | 0 | no | 2026-11-21T00:57:04 | 5b55fd4a4a43 | 4, internal/orgconfig/effective.go, internal/orgconfig/model.go | eigene Kette (in review) |
| 1588 | 0427-186 | 9534edd49c20 | develop @ 40cb28c758b0 | 1 | DRAFT | 2026-11-15T15:30:23 | 7f1a412b48f6 | 7, cmd/baha/app_remote_lifecycle.go, cmd/baha/deployment_record.go | verwaist (stale base, 6 days, no session) |
| 1587 | 0427-169 | 20e0537cc333 | develop @ 40cb28c758b0 | 1 | DRAFT | 2026-11-15T11:29:10 | 8202a280cb8f | 9, cmd/baha/serve.go, docs/cli/automation-agents.md | verwaist (stale base, 6 days, no session) |
| 1585 | 0428-bf01-fix | b50bc6a8053d | develop @ 40cb28c758b0 | 0 | DRAFT | 2026-11-20T23:13:12 | e6176c83caee | 6, cmd/baha/target.go, cmd/baha/target_selection.go | eigene Kette (re-hopped today, draft) |

`1*` = the head is NOT a direct descendant of develop 40cb28c7 because it sits on a stacked base branch. Stack health per pair (measured): #1730 is a true child of #1729's head (0 commits behind its base). #1737 and #1738 are each exactly 1 commit ahead of #1726's HEAD-at-PR-creation (0906b043), but #1726's branch moved to 221b6f43 at 03:58Z — the two stacked PRs are now BEHIND their base head (base drift; `221b6f43` is not an ancestor of either). GitHub shows them mergeable only via the PR-creation base. Practical consequence for merge order: #1726 → #1737 → #1738 (or a rebase of the children), and the child diffs above their own creation base stay valid.

## Dubletten-und-verwaiste

- No two open PRs share a patch-id (against develop, and against their own base refs). The only identical pair are #1684 and #1665, whose own-diff is EMPTY (head == base ref tip, see below) — a degenerate equality, not a content duplicate.
- Headline case #1732 vs #1734 (75770bd2d043 vs bddb27e6251): both are heads of PR #1732, which is now CLOSED (merged via #1734). #1734's head 45d181ab touches the same file, internal/logs/loki_test.go. None of the three is an ancestor of another (checked pairwise), and all three patch-ids differ (75770bd2 → d00847f19fd8, bddb27e6 → c5161717889b, 45d181ab → 8b941d38f74a). #1734 supersedes both #1732 heads; no duplicate remains open.
- #1684 (0428-083) and #1665 (0428-082): the remote branch tips of perses-tmpfs-mountpoint-wt and lane-0428-083-datasources-r2 EQUAL their PR heads (ls-remote witness: 408b18d2.../b71c6da2.../db27880c...), i.e. head == base-tip for the lower PR of each pair, so the incremental diff against their base is empty. #1665's head adds nothing over #1684's head, which adds nothing over #1724's head at this moment. Merge-order observation: #1724 → #1684 → #1665 is a true chain; the two upper PRs are currently placeholders (0 own files).
- File overlaps (not duplicates): #1623 touches cmd/baha/app_access.go which also appears in #1620 and in the #1615 diff; #1627 shares commands.go/machine_coverage.go/command-index docs with BOTH cli2-stack PRs #1623 and #1625; #1739's single file cmd/baha/app_commands.go also appears in #1615's diff. These bind merge order, not supersession.
- #1625 and #1623 share the identical merge-base ae2d022c8dc9 against develop (their heads are not ancestors of one another) — parallel children of one older cli2 snapshot, both carried under the owner's cli2-identity-secrets-head hold. #1627 (head 202b984e) IS a develop-descendant (a(dev)=0); its overlap with them is file-level only.
- Stale bases (a(dev)=1, not stacked): #1714 (6h), #1645 (merge-base 96f2ae11, i.e. cut before #1712 merged), #1614 (5 days), #1588 (6 days), #1587 (6 days), plus the cli2-stack heads #1625/#1623 (a(dev)=1 because their base branch sits on an older snapshot — owner decides hop vs hold). These are the hop candidates for the owner. #1704 (a(dev)=1, 337 files) stays owner-Stapel by round-1 precedent; #1615 is a develop-descendant but likewise owner-held.
- Abandoned check: every a(dev)=1 row except #1704 has no live session in `codeman agent list` (live: coordinator 9142ab1f, codex-rev-cli2b 95971e0a, 0428-207-appedit-fix2 47aef7ca, 0428-210-alltargets 6fa94f11 busy, 0428-142-hopfix e330ee18 busy, 0428-204-huntnumbers d23205ac busy, this lane ca3b8b21).

## Was sich seit 0428-216 (round 1, table eb3d13d7 / merge 5b1bf3f2) geaendert hat

Round 1 counted 30 open PRs; now 34. develop is unchanged (40cb28c7 both times), so "null hops" still holds — the delta is entirely new PRs and stacked pushes:
- NEW: #1737 (0428-213) and #1738 (0428-214), both stacked on lane-0428-198-cli-shard-operator-env (#1726 head 0906b043, pushed today 03:58Z).
- NEW: #1736 (DRAFT, owner, pr-gate routing files) — first non-product draft on scripts/** gate planner.
- NEW heads: #1739 (0428-210 all-targets, first fresh-branch candidate on develop, pushed 03:48Z).
- CORRECTION heads: #1735 (0428-207 fix2, 03:28Z) and #1734 (0428-212, 01:59Z) moved after round 1; #1732 closed/merged meanwhile (its two heads 75770bd2/bddb27e6 are now the supersession case).
- Owner hold restated: #1615 (head moved 03:50Z), #1625/#1623 remain base=cli2-identity-secrets-head; #1704/#1731 owner codex branches.
- Round-1 "no hop needed" rows that are still true: all a(dev)=0 develop-based rows. Round-1 rows now stale-base: none newly — #1714/#1645/#1614/#1588/#1587 were already the non-ancestor set.
- Stacked pushes on #1729→#1730 and #1726→#1737/#1738 mean the chain heads advanced after round 1; bases stayed develop-ancestors via their base branches.

## Command witnesses

- `gh pr list --repo mcpdev80/baseharbor --state open --limit 60 --json number,headRefOid,baseRefName,isDraft` => 34 rows (values embedded in table; full list retained at /tmp/opencode/prlist.json in this lane's scratch zone).
- `git fetch lane-origin '+refs/pull/*/head:refs/pull/*/head'` => 1361 pull head refs resolved.
- Ancestry: `git merge-base --is-ancestor lane-origin/develop <head>` per row, exit codes in column a(dev).
- File sets: `git diff --name-only <base-sha>...<head>` per PR; #1732 status: closed (not in open list; its heads measured for the duplicate section).
- ls-remote witness for base refs (final re-pull after the 1726 race): cli2-identity-secrets-head=760bc0f55c6f, lane-0428-143-verify-none=809a8196e1cf, perses-tmpfs-mountpoint-wt=408b18d2dc7b, lane-0428-083-datasources-r2=b71c6da27e8b, lane-0428-198-cli-shard-operator-env=221b6f437ea8, and refs/pull/1726/head=221b6f437ea8. The second `gh pr list` pass showed exactly one moved head (1726: 0906b043→221b6f43); every other row is stable across both passes.
- Live-session witness (`codeman agent list --json`): 9142ab1f idle (coordinator), 95971e0a idle (codex-rev-cli2b), 47aef7ca idle (0428-207-appedit-fix2), 6fa94f11 busy (0428-210-alltargets), e330ee18 busy (0428-142-hopfix), d23205ac busy (0428-204-huntnumbers), ca3b8b21 busy (this lane). No other live sessions exist; rows classified verwaist have no owner among them.

## cleanliness

- Before (this host is the coordinator/codeman server; nothing started by this lane):
  `docker ps -a` => `de40a6c61cef bh-docker-dev-edit-runtime-integration-dev-api-1 Exited (0) 38 minutes ago`
- After: identical (witness below). No container, network, volume or compose project was created by this lane; no `go test` was run on this host per mission.

## END
END_DONE 0428-216-prsweep2: inventory rebuilt — 34 open PRs tabled, no duplicate patch-ids, hop candidates 1714/1645/1614/1588/1587, plan SHA in END post.
