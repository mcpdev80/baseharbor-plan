# H-V30 — base branch liveness over the open PRs of this window

ROLE: Worker, BUG-HUNT, pure Befundung (reading / akte only). NO product change, NO commit to baseharbor, NO subagent (§4.8).
CARD: 0428-221 `t-20261121-base-branch-provenance-loss` (planned, owner: coordinator)
SLICE: base-branch-liveness — which open PRs stand on a base that no longer hangs from develop.
DATE: 2026-11-21.

## WITNESSES (remote truth, measured, not inferred)

Planning repo remote (verified before first evidence commit):
`origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)` — confirmed the real planning repo, not `workers/baseharbor-plan`.

baseharbor remote used for reads:
`origin  https://github.com/mcpdev80/baseharbor.git (fetch)` — resolved via `git remote -v`; only the github.com/mcpdev80 URL was used (REMOTE GUARD).

Remote heads via `git ls-remote` (authoritative live values):
- `refs/heads/develop` = `72ebc9d10ec247f24853af579655fd95c387214b`
- `refs/heads/lane-0428-198-cli-shard-operator-env` = `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4`
- `refs/heads/lane-0428-143-verify-none` = `1531939923fa5b4d6df32c69d918a7123c4763f3`
- `refs/heads/lane-0428-083-datasources-r2` = `84102144b78bfaab8c339d36dac707d230d347c6`

Ancestry via `git merge-base --is-ancestor <base-head> <develop-head>` in a fresh bare clone (remote HEADs):
- lane-0428-198 (e45430f) **NOT** ancestor of develop (72ebc9d) — LOST base
- lane-0428-143 (1531939) **NOT** ancestor of develop — LOST base
- lane-0428-083 (8410214) **NOT** ancestor of develop — LOST base

## 1. INVENTORY (all open PRs, `gh pr list --state open --limit 60`)

29 open PRs total. Base classification per PR (class per mission step 1):

| PR | baseRefName | draft | base-branch at remote? | base-head ancestor of develop? | class |
| --- | --- | --- | --- | --- | --- |
| 1745 | develop | no | n/a (develop) | yes (is develop) | base=develop (ok) |
| 1742 | develop | no | n/a | yes | base=develop (ok) |
| 1741 | lane-0428-198-cli-shard-operator-env | no | yes | **NO** | **base=lane WITHOUT develop connection (LOST)** |
| 1740 | lane-0428-198-cli-shard-operator-env | no | yes | **NO** | **base=lane WITHOUT develop connection (LOST)** |
| 1739 | develop | no | n/a | yes | base=develop (ok) |
| 1738 | lane-0428-198-cli-shard-operator-env | no | yes | **NO** | **base=lane WITHOUT develop connection (LOST)** |
| 1737 | lane-0428-198-cli-shard-operator-env | no | yes | **NO** | **base=lane WITHOUT develop connection (LOST)** |
| 1736 | develop | yes | n/a | yes | base=develop (ok) |
| 1735 | develop | no | n/a | yes | base=develop (ok) |
| 1730 | lane-0428-143-verify-none | no | yes | **NO** | **base=lane WITHOUT develop connection (LOST)** |
| 1729 | develop | no | n/a | yes | base=develop (ok) |
| 1728 | develop | no | n/a | yes | base=develop (ok) |
| 1725 | develop | no | n/a | yes | base=develop (ok) |
| 1723 | develop | no | n/a | yes | base=develop (ok) |
| 1714 | develop | no | n/a | yes | base=develop (ok) |
| 1704 | develop | no | n/a | yes | base=develop (ok) |
| 1702 | develop | no | n/a | yes | base=develop (ok) |
| 1665 | lane-0428-083-datasources-r2 | no | yes | **NO** | **base=lane WITHOUT develop connection (LOST)** |
| 1650 | develop | no | n/a | yes | base=develop (ok) |
| 1645 | develop | no | n/a | yes | base=develop (ok) |
| 1627 | develop | yes | n/a | yes | base=develop (ok) |
| 1625 | develop | yes | n/a | yes | base=develop (ok) |
| 1623 | develop | yes | n/a | yes | base=develop (ok) |
| 1620 | develop | no | n/a | yes | base=develop (ok) |
| 1614 | develop | yes | n/a | yes | base=develop (ok) |
| 1597 | develop | no | n/a | yes | base=develop (ok) |
| 1596 | develop | no | n/a | yes | base=develop (ok) |
| 1588 | develop | no | n/a | yes | base=develop (ok) |
| 1585 | develop | no | n/a | yes | base=develop (ok) |

Class sums (29 PRs):
- base=develop: 24
- base=lebendige lane die in develop haengt (ancestor of develop, non-develop ref): 0
- base=lane OHNE verbindung zu develop (LOST): **5**  → PRs #1737 #1738 #1740 #1741 #1665 #1730 ... corrected set below
- base=branch fehlt ganz: 0

Note: #1730 is base `lane-0428-143-verify-none` (a separate lost lane, not the 198 stack). The five LOST-base PRs are: #1737, #1738, #1740, #1741 (base lane-0428-198-cli-shard-operator-env), #1730 (base lane-0428-143-verify-none), #1665 (base lane-0428-083-datasources-r2). That is six LOST-base PRs across three lost lanes. The four 198-stack PRs each declare the same dead base; #1730 and #1665 stand on the two other dead bases.

## 2. LOST AMOUNT PER LANE (mission step 2)

`rev-list --count develop..<base-head>` (commits reachable from the base head but not from develop):

| Lost lane (base) | base-head | commits over develop | PR(s) on this base | PR state (mergedAt / mergeable) |
| --- | --- | --- | --- | --- |
| lane-0428-198-cli-shard-operator-env | e45430f | 11 | #1737 #1738 #1740 #1741 | all OPEN, MERGEABLE, mergedAt=null |
| lane-0428-143-verify-none | 1531939 | 3 | #1730 | OPEN, MERGEABLE, mergedAt=null |
| lane-0428-083-datasources-r2 | 8410214 | 2 | #1665 | OPEN, MERGEABLE, mergedAt=null |

The 198-lane carries 11 genuine commits absent from develop (`e45430f test(0428-204): authenticate secure export command path` down through `798...w198-0428-198: whole-package operator-auth seam for cmd/baha CLI shard` and `8b2cb2a97 fix(0428-198): give CLI unit tests an in-test operator identity`). All four base PRs are OPEN and MERGEABLE but can never turn green against develop, because their base is not reachable from develop.

Cards hanging on the lost lanes (from `depends_on` / `prs` frontmatter in `baseharbor-plan/tasks/**`):
- Base lane-0428-198-cli-shard-operator-env (card 0428-198 `t-20261120-r28-cli-shard-operator-env`, status `closed`, resolution `accepted`; depends `t-20261120-cli-operator-entrypoints` card 0428-204, status `closed`, resolution `accepted`):
  - PR #1737 → trust card 0428-213 `t-20261121-trust-uninstall-false-green` (review), mcp card 0428-218 `t-20261121-mcp-operator-seam-uncovered` (review)
  - PR #1738 → 0428-204 (closed/accepted), 0428-210 `t-20261121-all-targets-config-loss` (active), 0428-217 `t-20261121-git-credential-fill-bootstrap-hang` (active), 0428-218 (review), 0428-219 `t-20261121-secure-profile-export-interactive-auth` (closed)
  - PR #1740 → 0428-210 (active), 0428-215 `t-20261121-cli-shard-runtime-tests` (closed/accepted), 0428-214 `t-20261121-destroy-authority-stamp` (active), 0428-209 `t-20261121-native-cell-operator-seam` (wait)
  - PR #1741 → 0428-210 (active), 0428-214 (active), 0428-212 `t-20261121-loki-verify-probe` (closed), 0428-218 (review), 0428-213 (review)
- Base lane-0428-143-verify-none (PR #1730):
  - card 0428-203 `t-20261120-verif-none-stale-target` (wait), card 0428-216 `t-20261121-stale-pr-hop-and-baserefs` (active)
- Base lane-0428-083-datasources-r2 (PR #1665):
  - card 0428-082 `t-20261114-r28-perses-dashboards` (wait), card 0428-083 `t-20261114-r28-perses-datasources` (wait), plus coordination cards 0428-114/139/140/160/176/180/205/208/216 referenced by string match only.

## 3. CONTENT PROOF (mission step 3, file:line + hit-count in both states)

fund-1 — 198-lane, `cmd/baha/app_init_wizard.go` seam `withoutOperatorAuthTestContext`:
- develop: `git show origin/develop:cmd/baha/app_init_wizard.go | grep -c withoutOperatorAuthTestContext` = **0**
- lane-0428-198 head (e45430f): same = **1**
- develop has 0 occurrences, the 198-lane has 1 → the operator-auth seam registered in the wizard is present on the lane, absent from develop.

fund-2 — 143-lane, `internal/metrics/prometheus_verify.go` `ObservabilityVerifyNone` skip in the application-source loop:
- diff of commit `809a8196e` (0428-143: skip Verification=none in application metrics verifier loop): adds
  ```go
  if source.Verification == capability.ObservabilityVerifyNone {
      continue
  }
  ```
  inside the `applicationSources` loop of `verifyProviderSourcesAt` (`internal/metrics/prometheus_verify.go`, around line 238), plus a doc comment at `internal/capability/integration_contract.go:55-61`.
- develop `internal/metrics/prometheus_verify.go`: `ObservabilityVerifyNone` hit-count = **2** (declaration only, no application-source skip)
- 143-lane head: hit-count = **3** (declaration + the new `if ... continue` in the application-source loop)
- The application-source skip is present on the lane, absent from develop → the Verification=none application-class metrics source is still awaited as a required "up" sample on develop.

fund-3 — 083-lane, `internal/application/perses_datasource_seam.go` (datasource-mount refactor, "decision b"):
- `git ls-tree origin/develop -- internal/application/perses_datasource_seam.go` = empty (file absent from develop)
- `git ls-tree 8410214 -- internal/application/perses_datasource_seam.go` = present (blob `8f3f9c1f`)
- 16 files in this lane's delta (4223 insertions / 62 deletions) including `internal/metrics/perses_prometheus_datasource.go` (+658) — a native Perses datasource that never landed on develop.

## 4. CLASS SUMS (aggregate)

| Class | count |
| --- | --- |
| base=develop (ok) | 24 |
| base=lebendige lane in develop (ancestor) | 0 |
| base=lane OHNE verbindung zu develop (LOST) | 6 (PRs on 3 lost lanes) |
| base=branch fehlt ganz | 0 |
| total open PRs | 29 |

Lost lanes: 3. Lost commits over develop: 11 + 3 + 2 = 16. Open never-merged PRs standing on lost bases: 6 (#1737 #1738 #1740 #1741 #1730 #1665). All six are MERGEABLE with `mergedAt=null`.

## 5. ROOT-CAUSE WITNESS (mission background, measured)

PR #1726 (card 0428-198) CLOSED without merge: `mergedAt` null, `closedAt` 2026-11-21T09:09:20Z, `mergeable=CONFLICTING`. Cards 0428-198 AND 0428-204 remain `closed` with `resolution: accepted` despite the content never entering develop. AGENTS 3.3.8 ("only on content, never on merges") is violated here: the content was lost while the cards were treated as accepted.

## CLEANLINESS

`docker ps -a` BEFORE (pid 506579): only the header row, zero containers.
`docker ps -a` AFTER: only the header row, zero containers. (No containers, networks, volumes, or state directories were started — this is a pure read/`git`/`gh` hunt; the daemon was not touched.)
cleanliness: clean — before == after, no artifacts left behind.

## REOLE-COMPLIANCE (repo-rule compliance)

- Read-only: no product file changed, no commit to baseharbor, no PR opened/closed, no workflow_dispatch / rerun (Owner `.github/**` scope untouched).
- No subagent (§4.8): every step ran inside this session.
- No bare `go test ./cmd/baha/`: not run at all (read-only hunt).
- Evidence written only into `baseharbor-plan/...` (the real planning repo, remote verified above); never into a product repo.
- Remote truth measured via `git ls-remote` and a fresh bare clone; the quarantined `workers/baseharbor` checkout was not cited as remote evidence (REMOTE GUARD).
- One integration candidate per chain honored: no second branch invented; nothing was pushed to baseharbor.

## PLAN (worker steps, §4.4)
- Inventar aller offenen PRs (gh pr list --state open --limit 60) — done above, 29 PRs.
- Klassierung je PR — done above table.
- Inhalts-Gegenprobe je verlorener lane — fund-1/2/3 above.
- Verlorene menge je lane — table in section 2.
- Akte geschrieben — this file.

## END
END 0428-221-basalive DONE. Findings feed card 0428-221; product recovery (re-land the 16 commits onto develop or reopen cards 0428-198/204/203/082/083 naming the lost commits) is a coordinator/merge action, out of this hunt write-set.
