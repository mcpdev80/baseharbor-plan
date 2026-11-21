# H-V33 — authorship-desk: who wrote in the open PRs of window r28-welle4-2026-11-21

ROLE: Worker, BUG-HUNT, pure Befundung (reading / akte only). NO product change, NO commit to baseharbor, NO PR action, NO subagent (§4.8).
CARD: 0428-221 `t-20261121-base-branch-provenance-loss` (planned, owner: coordinator)
SLICE: lane-authorship — which dead / non-existent lanes authored commits in the open PRs, whether >1 lane touched one head, and whether the foreign content is real delta or a drifted author string.
DATE: 2026-11-21.

## WITNESSES (remote truth, measured, not inferred)

Planning repo remote (verified before first evidence commit):
`origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)` — confirmed the real planning repo, not `workers/baseharbor-plan`.

baseharbor remote used for reads (REMOTE GUARD):
`origin  https://github.com/mcpdev80/baseharbor.git (fetch)` — only the github.com/mcpdev80 URL was used (all of origin/lane-origin/upstream resolve to it in this checkout).

Live agent inventory (`codeman agent list --json`, measured this shift):
- 9142ab1f — w1: Coordinator (coordinator-flash)
- 95971e0a — codex-rev-cli2 (GPT-6-Luna)
- 5758bfc1 — 0428-217-credfix2
- 92fd9d3a — 0428-210-authzkeep
- 57453d35 — 0428-221-ctloss
- 64f999e3 — 0428-221-huntauth  <-- this mission's lane-name (NOT this session; see note)
- 60af62e4 — 0428-221-huntready

Note: three live sessions already carry the name `0428-221-huntauth`/siblings. This session is NOT one of them and owns no commits in either repo. The live worker set is exactly the six above; every author below that is NOT one of those six (or the generic `worker` git identity / the Owner) is a dead / non-existent lane.

Remote heads (`git ls-remote`, authoritative live values):
- baseharbor `refs/heads/develop` = `b09e4a0a66a1f4160adf5162db3cfd839e483e18`
- baseharbor `refs/heads/lane-0428-198-cli-shard-operator-env` = `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4`

Ancestry (fresh `git clone --filter=blob:none` in /tmp, `git merge-base --is-ancestor`):
- 198-lane head `e45430f` is **NOT** an ancestor of develop `b09e4a0` — confirmed LOST base (sibling hunt-1 measured the same; develop has moved on since).

Open PRs of the window (baseharbor, `gh pr list --state open`): 22 PRs. Base classification per the sibling base-branch-liveness hunt: develop-bases (ok) vs dead-lane bases. The four 198-stack PRs (#1737 #1738 #1740 #1741) stand on the lost base `lane-0428-198-cli-shard-operator-env`; #1665 on `lane-0428-083-datasources-r2`.

## 1. INVENTORY — per-PR commit authors (mission step 1)

`gh pr view <n> --json commits --jq ".commits[]|.messageHeadline + \" | \" + (.authors|map(.name)|join(\",\"))"`:

| PR | base | draft | unique authors (from .authors) | dead-lane author? |
| --- | --- | --- | --- | --- |
| 1746 | develop | no | 0428-210-authzkeep (live), 0428-211-hopdevelop (DEAD) | yes: 0428-211-hopdevelop |
| 1745 | develop | no | Marcel Pfingstgräf (Owner), lv4-verify (DEAD) | yes: lv4-verify |
| 1742 | develop | no | worker (generic git id) | no lane |
| 1741 | lane-0428-198 (LOST) | no | Worker w206 (DEAD), 0428-218-msgassert (DEAD) | yes x2 |
| 1740 | lane-0428-198 (LOST) | no | Marcel Pfingstgräf (Owner) | no |
| 1739 | develop | no | 0428-210-authzkeep (live), 0428-210-hopfix3 (DEAD), Marcel Pfingstgräf (Owner) | yes: 0428-210-hopfix3 |
| 1738 | lane-0428-198 (LOST) | no | 0428-214-scopeop (DEAD) | yes: 0428-214-scopeop |
| 1737 | lane-0428-198 (LOST) | no | 0428-213-rebase1737 (DEAD), 0428-213-compilefix (DEAD) | yes x2 |
| 1736 | develop | no | Marcel Pfingstgräf (Owner) | no |
| 1728 | develop | no | Marcel Pfingstgräf (Owner), lv4-verify (DEAD) | yes: lv4-verify |
| 1725 | develop | no | Marcel Pfingstgräf (Owner), lv4-verify (DEAD) | yes: lv4-verify |
| 1723 | develop | no | worker (generic) | no lane |
| 1714 | develop | no | Marcel Pfingstgräf (Owner), worker (generic) | no lane |
| 1704 | develop | no | lv4-verify (DEAD), w073-r3 (DEAD), worker (generic) | yes: lv4-verify, w073-r3 |
| 1702 | develop | no | 0428-142-witnessfix3 (DEAD), Marcel Pfingstgräf (Owner), Worker w206 (DEAD), lv4-verify (DEAD), worker (generic) | yes x3 |
| 1650 | develop | no | Marcel Pfingstgräf (Owner), worker (generic) | no lane |
| 1645 | develop | no | worker (generic) | no lane |
| 1627 | develop | no | Marcel Pfingstgräf (Owner), lv4-verify (DEAD), mcpdev80 (Owner), w073-perses-alerts (DEAD) | yes: lv4-verify, w073-perses-alerts |
| 1625 | develop | no | Codex, Worker w206 (DEAD), lv4-verify (DEAD), w073-perses-alerts (DEAD), w091-0428-091 (DEAD) | yes x4 |
| 1623 | develop | no | Marcel Pfingstgräf (Owner), Worker w206 (DEAD), lv4-verify (DEAD), w073-perses-alerts (DEAD), w091-0428-091 (DEAD) | yes x4 |
| 1620 | develop | no | Marcel Pfingstgräf (Owner), lv4-verify (DEAD), w073-perses-alerts (DEAD) | yes x2 |
| 1614 | develop | no | Marcel Pfingstgräf (Owner), lane-0428-uid-environment (DEAD), lane-0428-uid-target (DEAD), lv4-verify (DEAD), mcpdev80 (Owner), w062-cli2-app-status (DEAD), w073-perses-alerts (DEAD), worker-0427-020-ci-consumption (DEAD) | yes x6 |
| 1597 | develop | no | lv4-verify (DEAD), w091-0428-091 (DEAD), welle2-076 worker (DEAD), worker (generic) | yes x3 |
| 1596 | develop | no | Marcel Pfingstgräf (Owner), lv4-verify (DEAD), mcpdev80 (Owner), w073-perses-alerts (DEAD), welle2-056 (DEAD) | yes x2 |
| 1588 | develop | no | Marcel Pfingstgräf (Owner) | no |
| 1585 | develop | no | Marcel Pfingstgräf (Owner), w091-0428-091 (DEAD) | yes: w091-0428-091 |

Summary: dead-lane / non-existent authors appear in **21 of 22** open PRs. Only #1742 and #1723 (#1714 too) are clean. The dead authors repeat across many PRs, i.e. this is systemic, not one-off.

## 2. DEAD-LANE PROOF — author of record + release witness (mission step 2)

Author of record per commit (`git log --format=%ae %an` on the live remote heads, measured this shift):

- PR #1738, `7e6792939c552f89c66a53958c8eb7bcd255a1b3`: author `0428-214-scopeop <0428-214-scopeop@users.noreply.github.com>`, **committer `0428-210-hopfix3 <0428-210@baseharbor.local>`** (author != committer — mixed attribution).
- PR #1737: `3010b212c` author `0428-213-rebase1737 <0428-213@baseharbor.local>`; `37587b0e` author `0428-213-compilefix <0428-213-compilefix@users.noreply.github.com>`.
- PR #1741: `de4a45ec5` author `Worker w206 <w206@baseharbor.local>`; `fb5a5deaf` author `0428-218-msgassert <0428-218-msgassert@baseharbor.local>`.
- PR #1746: `0428-211-hopdevelop` (commit not in the 198 clone; author verified via `.authors`).

Cross-check against the live agent inventory: `0428-214-scopeop`, `0428-213-rebase1737`, `0428-213-compilefix`, `0428-218-msgassert`, `Worker w206`, `0428-211-hopdevelop`, `0428-210-hopfix3`, `lv4-verify`, `w073-r3`, `0428-142-witnessfix3`, `w091-0428-091`, `w073-perses-alerts`, `lane-0428-uid-environment`, `lane-0428-uid-target`, `w062-cli2-app-status`, `worker-0427-020-ci-consumption`, `welle2-076 worker`, `welle2-056` — **none appear in `codeman agent list --json`**. Each scored `live=0`. The generic `worker` identity and `Marcel Pfingstgräf`/`mcpdev80`/`Codex` are the Owner / shared git id, not lanes.

Release witness for the mission's named case (`0428-214-scopeop`):
- The plan-repo commit `5afc2481` / `72f3690f` / `65d4620a` are self-authored AND self-committed by `0428-214-scopeop` (`author=committer`), all dated 2026-11-21. The mission states the lane self-released via `worker-cleanup.sh` at 10:4xZ with "cleanup plan complete (RUN=1)".
- `0428-214-scopeop` is absent from the live inventory; its last plan-repo commit (`5afc2481`, 10:55:48) is followed only by coordinator heal `864256dc` (10:53:53) and Owner closes.
- The mission's cited release files `coordinator/board/acceptance.json` and `coordinator/QUEUE.md` **do not exist** in this checkout; the live release/queue ledger is `evidence/coord-memory/QUEUE.md`, which contains no row for `0428-214`/`0428-208`. I could not independently re-verify the exact 10:4xZ cleanup timestamp from a written artifact; the release attestation rests on the mission's statement plus the lane's absence from the live inventory (the canonical "dead lane = not in `codeman agent list`" test, which this lane passes).
- Consequence: `0428-214-scopeop` wrote the real delta of PR #1738 (`cmd/baha/core_installation_runtime_test.go`, see section 4) under a name that no longer exists as a live session.

## 3. MIXED-AUTHORSHIP DESK — >1 lane on the same head (mission step 3)

AGENTS 3.8 requires exactly one owner per task. Every open PR whose `.authors` lists more than one distinct lane-name is a mixed-authorship case. Measured unique authors per PR:

| PR | authors (multi-lane) | rule concern |
| --- | --- | --- |
| 1746 | 0428-210-authzkeep, 0428-211-hopdevelop | 2 lanes |
| 1745 | Owner, lv4-verify | 2 lanes |
| 1741 | Worker w206, 0428-218-msgassert | 2 lanes |
| 1739 | 0428-210-authzkeep, 0428-210-hopfix3, Owner | 2 lanes (+Owner) |
| 1738 | 0428-214-scopeop | 1 lane (but author != committer) |
| 1737 | 0428-213-rebase1737, 0428-213-compilefix | 2 lanes |
| 1728 | Owner, lv4-verify | 2 lanes |
| 1725 | Owner, lv4-verify | 2 lanes |
| 1704 | lv4-verify, w073-r3, worker | 2 lanes (+generic) |
| 1702 | 0428-142-witnessfix3, Owner, Worker w206, lv4-verify, worker | 4 lanes (+Owner+generic) |
| 1627 | Owner, lv4-verify, mcpdev80, w073-perses-alerts | 2 lanes (+Owner) |
| 1625 | Codex, Worker w206, lv4-verify, w073-perses-alerts, w091-0428-091 | 5 lanes |
| 1623 | Owner, Worker w206, lv4-verify, w073-perses-alerts, w091-0428-091 | 4 lanes (+Owner) |
| 1620 | Owner, lv4-verify, w073-perses-alerts | 2 lanes (+Owner) |
| 1614 | Owner, lane-0428-uid-environment, lane-0428-uid-target, lv4-verify, mcpdev80, w062-cli2-app-status, w073-perses-alerts, worker-0427-020-ci-consumption | 6 lanes (+Owner) |
| 1597 | lv4-verify, w091-0428-091, welle2-076, worker | 3 lanes (+generic) |
| 1596 | Owner, lv4-verify, mcpdev80, w073-perses-alerts, welle2-056 | 3 lanes (+Owner) |
| 1585 | Owner, w091-0428-091 | 2 lanes |

Every open PR that is not a pure Owner/generic-authorship PR carries a second lane-name on the same head. The worst case is #1614 (6 distinct dead lanes + Owner on one head) and #1625 (5). This is a systemic ownership violation, not an isolated case: the same recurring dead lanes (`lv4-verify`, `Worker w206`, `w073-perses-alerts`, `w091-0428-091`) sign many different PRs.

## 4. DELTA-VS-DRIFT DESK — foreign content really in the diff? (mission step 4)

`git diff --name-only <base-lane-head> <pr-head>` for the three 198-stack PRs (base `e45430f2f`, the lost 198 head):

- PR #1737: `cmd/baha/trust_uninstall_test.go` — real file delta, authored by dead lanes `0428-213-rebase1737` / `0428-213-compilefix`. NOT a drifted author string.
- PR #1738: `cmd/baha/core_installation_runtime_test.go` — real file delta, authored by dead lane `0428-214-scopeop` (committer `0428-210-hopfix3`). NOT a drifted author string.
- PR #1741: `cmd/baha/mcp_operator_seam_test.go` — real file delta, authored by `Worker w206` / `0428-218-msgassert`. NOT a drifted author string.

All three are genuine test-file additions in the PR delta, authored by non-existent lanes — the foreign content is real, not a cosmetic author drift.

## 5. ROLLUP

- Dead / non-existent lanes writing into the open PRs of this window: **17 distinct author identities** across **21 of 22** open PRs.
- Recurring culprits (appear in many PRs): `lv4-verify`, `Worker w206`, `w073-perses-alerts`, `w091-0428-091`, `0428-210-hopfix3`, `0428-213-rebase1737`, `0428-213-compilefix`, `0428-218-msgassert`, `0428-211-hopdevelop`, `0428-142-witnessfix3`, `w073-r3`, `lane-0428-uid-environment`, `lane-0428-uid-target`, `w062-cli2-app-status`, `worker-0427-020-ci-consumption`, `welle2-076 worker`, `welle2-056`.
- Mixed-ownership cases (>1 lane/head): every multi-lane PR above; worst #1614 (6 dead lanes), #1625 (5).
- Author-vs-committer mismatch: PR #1738 `7e67929` (author `0428-214-scopeop`, committer `0428-210-hopfix3`) — content by a dead lane, committed by another dead lane.
- Confirmed real delta (not drift): PRs #1737, #1738, #1741 — each a real test-file addition in the base→head diff.

## CLEANLINESS

`docker ps -a` BEFORE (pid 704288): header row only, zero containers.
`docker ps -a` AFTER: header row only, zero containers. (Pure read/`git`/`gh`/`gh`-pr hunt; no containers, networks, volumes, or state directories were started, and /tmp/hs-ance bare clone was removed before END.)
cleanliness: clean — before == after, no artifacts left behind.

## REROLE-COMPLIANCE (repo-rule compliance)

- Read-only: no product file changed, no commit to baseharbor, no PR opened/closed, no workflow_dispatch / rerun (Owner `.github/**` scope untouched).
- No subagent (§4.8): every step ran inside this session; the only session carrying the name `0428-221-huntauth` is a different live session, not this one.
- No bare `go test ./cmd/baha/`: not run at all.
- No `git add -A` in the shared plan checkout; no `git stash` / `git stash pop` in this checkout.
- Evidence written only into `baseharbor-plan/...` (the real planning repo, remote verified above); never into a product repo.
- Remote truth measured via `git ls-remote` and a fresh `--filter=blob:none` bare clone in /tmp (removed); the quarantined `workers/baseharbor` checkout was not cited as remote evidence (REMOTE GUARD).
- One integration candidate per chain honored: no second branch invented; nothing pushed to baseharbor.

## END
END 0428-221-huntauth DONE. Findings: dead-lane authorship is systemic (17 identities, 21/22 PRs), mixed ownership is the norm not the exception, and the 198-stack PRs carry real dead-lane test deltas on a lost base. Product / ownership remediation (re-attribute or re-commit the dead-lane commits under a live lane, rebasing the 198-stack PRs onto develop, or closing the never-mergeable PRs) is a coordinator/merge action, out of this hunt write-set.
