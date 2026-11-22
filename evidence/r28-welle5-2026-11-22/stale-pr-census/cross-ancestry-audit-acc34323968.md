# Cross-ancestry audit

Session role: CODEX-REVIEW, read-only census; no product verdict.

## PLAN

1. Read the cross-ancestry audit handoff and record its scope, evidence path, and read-only limits.
2. Enumerate every currently open mcpdev80/baseharbor PR and refresh its head, base pointer, and current develop ref.
3. Compare each open PR head against all other open PR heads for ancestry; classify foreign commits against develop and reconcile changed paths with Planning card PR links.
4. Publish the evidence-only census to Planning origin/main, update the board, and post END to the Coordinator.

## Method and snapshots

- Product remote resolved as `https://github.com/mcpdev80/baseharbor.git`; Planning remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Census snapshot: 2026-11-22; `gh api repos/mcpdev80/baseharbor/pulls?state=open&per_page=100` returned 16 PRs. Every API head was matched to `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/<N>/head` and fetched before ancestry checks.
- Current develop: `acc343239681feb235a33cf00c8ea754c537291f` (`refs/heads/develop`).
- `back` is the count of commits in develop not reachable from the PR head (`git rev-list --count <head>..develop`). `diff` is `git diff --name-only develop...<head>`. Foreign ancestry uses pairwise `git merge-base --is-ancestor <other-open-PR-head> <head>` for all ordered pairs.
- Card links and intended scope were read from `tasks/` in the Planning repo. “Yes” means the current develop-to-head path set aligns with linked card scope; “No” records concrete paths outside the linked card scope.

## Open PR census

| PR | Head SHA | Base pointer (ref @ SHA) | Back | Foreign open-PR heads | Develop diff paths | Card-only diff |
|---:|---|---|---:|---:|---:|---|
| 1761 | `d275e50c5ba0245b6ab8a42f9655c9bef1bb2bd0` | develop @ `52a3c5446f41a1dd8678d99875e4cb1eee67874c` | 24 | 0 | 6 | Yes — 0428-231 |
| 1753 | `a40b76764c3c08ec690e723def0ca167ce989c2b` | develop @ `52a3c5446f41a1dd8678d99875e4cb1eee67874c` | 24 | 0 | 2 | Yes — linked 0428-227 and 0428-237 |
| 1752 | `34feb493480ec3b2703681bf576ce41e3904995b` | develop @ `82825e95a6f6083702d0ba5401d97f356085c722` | 34 | 0 | 19 | No — includes reserved/shared CLI and generated-contract paths beyond 0428-061; see findings |
| 1746 | `e455302f1a89d17d9fae2f532ebb803f479a0994` | develop @ `52a3c5446f41a1dd8678d99875e4cb1eee67874c` | 24 | 0 | 12 | Yes — linked 0428-205 and 0428-208 |
| 1741 | `fb5a5deaf36ba160b527019a3ef4eea85060905d` | lane-0428-198-cli-shard-operator-env @ `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4` | 270 | 0 | 30 | Yes — 0428-218 plus inherited 0428-198 stack |
| 1740 | `0ffe093357d9f7fb52f5e7542f4ade41e48fab1b` | lane-0428-198-cli-shard-operator-env @ `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4` | 270 | 0 | 31 | Yes — 0428-209 plus inherited 0428-198 stack |
| 1738 | `7e6792939c552f89c66a53958c8eb7bcd255a1b3` | lane-0428-198-cli-shard-operator-env @ `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4` | 270 | 0 | 30 | Yes — 0428-214 and 0428-218 plus inherited 0428-198 stack |
| 1737 | `37587b0ed6fc8803856f3b394ae37b2ff4a03f47` | lane-0428-198-cli-shard-operator-env @ `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4` | 270 | 0 | 30 | Yes — 0428-213 plus inherited 0428-198 stack |
| 1725 | `d65e9a25419798950a01676ab259967345721a25` | develop @ `acc343239681feb235a33cf00c8ea754c537291f` | 0 | 0 | 7 | No — four workload-port paths are outside linked 0428-201 and 0428-233 |
| 1723 | `9355afe129b9fa7e11837b9fcbe5b7fc40c3d2e9` | develop @ `acc343239681feb235a33cf00c8ea754c537291f` | 0 | 0 | 4 | Yes — four paths match 0428-199 |
| 1650 | `28c18f02039f0957544146cf5d0db2a1561a4220` | develop @ `40cb28c758b02960356434b630086a341ebe1738` | 270 | 0 | 6 | Yes — 0428-078 |
| 1645 | `326ca9005267c135feb31cdfde8ac69a3c17508e` | develop @ `52a3c5446f41a1dd8678d99875e4cb1eee67874c` | 24 | 0 | 35 | Yes — 0428-091 |
| 1623 | `4cbf92960cb5d97077370b7da052d45523ce0043` | develop @ `9bd76324ec6d1364f512d718cb82f1fffc9105a4` | 581 | 0 | 20 | Yes — 0428-063 |
| 1620 | `28cb907dc0a678d1b5326df5203741c70cf84978` | develop @ `40cb28c758b02960356434b630086a341ebe1738` | 270 | 0 | 2 | Yes — 0428-067 |
| 1614 | `80d4df52e913e4472334a5f257fe868d26d5976e` | develop @ `15727ca8878938df7e924319c236c0bcc4a4201c` | 589 | 0 | 37 | Needs card-scope confirmation — 0428-062 current diff exceeds the previously recorded 14-file write-set |
| 1597 | `074678d149e5b8d0f899c55da92debf52bf0fd46` | develop @ `e6c199e7b7dd7d076a776d11c3ba16f25e59c254` | 73 | 0 | 15 | Yes — 0428-076 |

## Findings

- No live open PR head is an ancestor of another live open PR head in this refreshed snapshot. The earlier #1723→#1725 exact-head ancestry pair no longer exists: their live heads changed, and each now includes current develop. The known closed #1627 head `0768274c6f692bc0779202a1b9dc1fb222fce2ef` is an ancestor of current develop, so that historical content is safe.
- #1725 still has a card-scope mismatch after its develop hop. Its seven-path develop diff contains the four #1723 workload-port paths (`cmd/baha/app_apply.go`, `cmd/baha/app_workload_ports.go`, `cmd/baha/runtime.go`, `cmd/baha/workload_port_local_regression_test.go`) plus three shared-backend state-version paths. Those workload-port paths match 0428-199, not #1725's linked 0428-201/0428-233. The current exact #1723 head is not an ancestor of #1725; this is carried content without exact-head ancestry.
- #1752's 19-path diff exceeds its 0428-061 scope. It includes reserved/shared `cmd/baha/commands.go`, `cmd/baha/mcp.go`, `cmd/baha/mcp_lifecycle_extra.go`, machine coverage/contract paths, generated EN/DE command indexes, and other CLI documentation. Planning's historical exception allowed a narrow machine-coverage/docs slice; it did not authorize the entire current set. Scope needs coordinator reconciliation before review relies on the full diff.
- #1614 has 37 develop-diff paths against the 14-file write-set recorded in its linked task. Treat the card-only assertion as unconfirmed and reconcile before a full-content review.
- #1741/#1740/#1738/#1737 share the declared 0428-198 base. Their larger develop diffs include that stack; no open-head ancestry contamination was found among these four candidates.

## Konsequenz

Hop/re-cut only #1725 next: first establish a clean candidate containing 0428-201/0428-233 alone on current develop, then resume its review. #1723 is already based on current develop and its four-path diff matches 0428-199, so it needs no hop. Separately reconcile #1752's expanded write-set and #1614's 37-path diff against their card owners before treating those diffs as card-only. No unsafe open-PR-head ancestry pair remains in the current census.

## cleanliness

- `docker ps -a --no-trunc` before audit work: no containers listed.
- No containers, compose projects, or VM test stacks were started by this read-only audit.

## Planning remote witness

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Repo-rule compliance

- Read-only CODEX-REVIEW scope followed: no product files, PR state, comments, merges, closes, workflow runs, or tests were changed or triggered.
- Planning evidence is stored only in the canonical Planning repository. Shared untracked Planning files were left untouched.

- `docker ps -a --no-trunc` after audit work: no containers listed.


## Origin/main tree witness

Exact output of `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep 'evidence/r28-welle5-2026-11-22/stale-pr-census/cross-ancestry-audit-acc34323968.md'` after fetching origin/main:

```text
evidence/r28-welle5-2026-11-22/stale-pr-census/cross-ancestry-audit-acc34323968.md
```

END_DONE codex-rev-1747: 16 open PRs audited; zero live foreign-head ancestry pairs; #1725 is the next clean re-cut; Planning remote origin https://github.com/mcpdev80/baseharbor-plan.git.
