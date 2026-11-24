# 0428 Backlog Eligibility Triage — round 1

**Lane:** w108-0428-216-backlog
**Card:** 0428-216 (triage only)
**Type:** READ-ONLY eligibility map. No product write, no PR, no CI, no claim, no subagent.
**Base:** `origin/main` (planning repo) pulled `--rebase` before first evidence commit. Planning remote: `https://github.com/mcpdev80/baseharbor-plan.git`.
**Base attestation (product):** `git ls-remote origin develop` = `f14fb87c8f5afd91168e4f174d620c9f00e6341e`. All open PR heads measured against this.
**Remote witnesses:** `git ls-remote origin develop` = `f14fb87c8`; `git ls-remote origin refs/pull/{1812,1820,1819,1818,1650,1826}/head` as in §6.

## PLAN

- Confirm planning remote (mcpdev80/baseharbor-plan), pull --rebase origin main.
- Enumerate every v0.4.28 card in tasks/ with kanban_status planned/ready/backlog OR a title/body referencing an open PR.
- Classify each as DISPATCHABLE-NOW / GATED / OWNER-SCOPE / SUPERSEDED-STALE.
- Settle the mission's named set (0428-224/220/264/265/251/221/182).
- First-action + CI for each DISPATCHABLE-NOW so the coordinator can spin a real lane.
- Count DISPATCHABLE-NOW for the coordinator's hold decision.
- Commit+push atomically, targeted add only, verify evidence on origin/main.

## Method

- Read every v0.4.28 card frontmatter (card_number, kanban_status, depends_on, owner, prs).
- Enumerated 6 open product PRs live via `gh`-equivalent REST (`api.github.com/.../pulls/{N}`) and confirmed heads with `git ls-remote`.
- Resolved depends_on chains against task ids to find gated prerequisites.
- READ-ONLY throughout: created the evidence file only; touched nothing product-side.

## Open PRs (live, measured 2026-11-24)

| PR # | head | state | draft | base | commits behind develop |
| --- | --- | --- | --- | --- | --- |
| #1812 | 9140b2cdf | open | no | develop | 1 |
| #1819 | 17381017b | open | no | develop | — (11 behind, carried on #1812 stack) |
| #1820 | 28803d110 | open | no | develop | 0 |
| #1826 | 6589a37b0 | open | no | develop | 0 |
| #1650 | 84943695b | open | no | develop | 18 |
| #1818 | 20fc1cb7d | open | no | develop | — (rebased on #1650's lane, on-stack) |

All six are Owner-author, none merged. #1819 and #1818 are not measured individually (11/18 commits behind develop, carried on the frozen #1812→#1819→#1820 stack); only #1812/#1820/#1826 are independent heads.

## Eligibility table

| card | status | depends_on | class | write-set conflict? | first-action-or-blocker |
| --- | --- | --- | --- | --- | --- |
| 0428-224 | planned | none | DISPATCHABLE-NOW | none | Coordinate authorship normalization across open candidates; needs a coordination task, no single write-set |
| 0428-220 | closed/dropped | — | SUPERSEDED/STALE | — | already closed, resolution=dropped |
| 0428-264 | planned | 0428-263 | GATED | — | wait for 0428-263 (status probe verifier) |
| 0428-265 | planned | 0428-142 | DISPATCHABLE-NOW | none | witness producer in internal/metrics; CLI call sites; cmd/baha regression |
| 0428-251 | closed/accepted | — | SUPERSEDED/STALE | — | merged in #1780 |
| 0428-221 | active | none | DISPATCHABLE-NOW (coord) | none | reopen lost cards or re-land #1726 content; plan-repo guard |
| 0428-182 | closed/accepted | — | SUPERSEDED/STALE | — | merged in #1716 |
| 0428-003..007 | planned | release sub-tasks | GATED | — | v0.4.28 release sequence; pre-tag |
| 0428-043 | planned | 0428-final-acceptance | GATED | — | CLI harmonization |
| 0428-064 | planned | audit-events | DISPATCHABLE-NOW | none | unify app data + TLS, cmd/baha + tests |
| 0428-066 | planned | audit-events | DISPATCHABLE-NOW | none | env-setup wizards |
| 0428-069 | planned | cli2-audit-* | GATED | — | register unified command tree |
| 0428-070 | planned | cli2-cli-integration | GATED | — | document/test guided paths |
| 0428-071 | planned | r31-manpage | GATED | — | final review coordination |
| 0428-072 | planned | none | DISPATCHABLE-NOW (coord) | none | coordinate five workers |
| 0428-087 | planned | dashboard-* | GATED | — | Perses native monitoring proof |
| 0428-162 | planned | r28-orgconfig | DISPATCHABLE-NOW | none | redact env key errors |
| 0428-189..194 | planned | dashboard-identity | DISPATCHABLE-NOW | none | prune-key / signal-state / registry-lock |
| 0428-235 | planned | none | DISPATCHABLE-NOW | none | catalog + planner |
| 0428-253 | planned | none | DISPATCHABLE-NOW | none | candidate planner mishandling |
| 0428-263 | planned | r28-perses-status | DISPATCHABLE-NOW | none | status probe verifier |
| 0428-266..268 | planned | witness-producer | GATED | — | Perses status sequels |
| 0428-272 | planned | none | DISPATCHABLE-NOW | none | authority seam runtime gate |
| 0428-278 | planned | none | DISPATCHABLE-NOW | none | gate-plan ghost source rows |
| 0428-279 | blocked | — | OWNER-SCOPE (demo) | — | demo destructive set, #1826 in flight |
| 0428-283 | blocked | — | OWNER-SCOPE | — | static-mcp operator gap, .github/** |
| 0428-284 | blocked | — | OWNER-SCOPE (consent) | — | #1812 post-retry gate fail, consent |
| 0428-271 | active | — | DISPATCHABLE-NOW (coord) | none | broker identity version-only, #1820 stack |
| 0428-273..275 | active | — | DISPATCHABLE-NOW (coord) | none | catalog rows 1819/1820 |
| 0428-078 | blocked | — | OWNER-SCOPE | — | Perses identity dashboard, #1818 on #1650 |
| 0428-249 | blocked | — | GATED | — | light-runtime blob, #1812 stack |

## Named-card settle (mission §4)

- 0428-224: planned, no depends_on, no write-set. DISPATCHABLE-NOW as a coordination task (authorship normalization across open candidates). No single product write-set.
- 0428-220: closed/resolution=dropped on witness `46017060d`. Not lane work.
- 0428-264: planned, depends_on 0428-263. GATED. First action after 0428-263 lands: cmd/baha regression asserting the two Perses faces agree; "PR · Go unit" group.
- 0428-265: planned, depends_on 0428-142 (already accepted). DISPATCHABLE-NOW. Concrete first action: witness producer in internal/metrics (perses_dashboards_hosts.go family), replace zero-value literal at cmd/baha/perses_lifecycle.go:366, app_status_result.go:328/436, add cmd/baha regression. CI: "PR · Go unit" group covering cmd/baha.
- 0428-251: closed/resolution=accepted, merged in #1780. Not lane work.
- 0428-221: active (coordinator-owned, high). Real lane work exists: re-land #1726's 11 lost commits onto develop or reopen cards 0428-198/204, plus a plan-repo machine guard. Write-set: task cards + baseharbor-plan scripts (Owner-scope; report file:line if guard lives in product scripts). DISPATCHABLE-NOW as a coordinator task.
- 0428-182: closed/resolution=accepted, merged in #1716. Not lane work.

## DISPATCHABLE-NOW list (coordinator hold decision)

Candidate-count: **9** independent, conflict-free, ready-now:

1. 0428-224 — coordination task (authorship normalization), no single write-set. CI: none yet (coordination).
2. 0428-221 — re-land #1726 or reopen 0428-198/204 + plan-repo guard. Coordinator task.
3. 0428-265 — witness producer (internal/metrics) + cmd/baha call-site fix + cmd/baha regression. CI: "PR · Go unit".
4. 0428-064 — app data/TLS unification (cmd/baha + tests). CI: "PR · Go unit".
5. 0428-066 — env-setup wizards (cmd/baha). CI: "PR · Go unit".
6. 0428-072 — coordinate five workers (coordinator). CI: none.
7. 0428-162 — redact env key errors (cmd/baha). CI: "PR · Go unit".
8. 0428-189..194 — prune-key / signal-state / registry-lock (cmd/baha). CI: "PR · Go unit".
9. 0428-235 — catalog + planner (planner). CI: "PR · Go unit".
10. 0428-253 — candidate planner (planner). CI: "PR · Go unit".
11. 0428-263 — status probe verifier (internal/metrics). CI: "PR · Go unit".
12. 0428-272 — authority seam runtime gate (planner/product). CI: "PR · Go unit".
13. 0428-278 — gate-plan ghost source rows (planner). CI: "PR · Go unit".

(Note: items 1-13 are the full DISPATCHABLE-NOW set; 0428-271/273-275 and 0428-216 are coordinator-owned and tracked separately on active lanes.)

True DISPATCHABLE-NOW now (independent, no open depends_on, disjoint from frozen chain): 0428-224, 0428-221, 0428-265, 0428-064, 0428-066, 0428-072, 0428-162, 0428-189..194, 0428-235, 0428-253, 0428-263, 0428-272, 0428-278.

## GATED (cannot start without a prerequisite)

- 0428-264 ← 0428-263
- 0428-266 ← 0428-265/0428-263
- 0428-267 ← 0428-265/0428-263
- 0428-268 ← 0428-152
- 0428-003..007, 0428-043, 0428-069, 0428-070, 0428-071, 0428-087 (release / cli2 / dashboard sequels)

## OWNER-SCOPE / BLOCKED (stop and report)

- 0428-279 (blocked) — demo destructive set, #1826 in flight. Owner-demo scope.
- 0428-283 (blocked) — static-mcp operator gap. `.github/**` + product env contract + demo; needs fresh owner decision.
- 0428-284 (blocked) — #1812 post-retry gate fail. Consent/demo-operator harness; needs fresh owner decision.
- 0428-078 (blocked) — Perses identity dashboard, #1818 stacked on #1650 (18 commits behind develop).
- 0428-249 (blocked) — light-runtime blob, #1812 stack.

## SUPERSEDED/STALE

0428-220, 0428-251, 0428-182, 0428-281, 0428-282 (all closed/resolution-settled).

## Counts

- Total v0.4.28 cards enumerated: 175+
- DISPATCHABLE-NOW (independent, ready now, disjoint from frozen chain): ~13
- GATED (await prerequisite): ~12
- OWNER-SCOPE / BLOCKED: 4-5
- SUPERSEDED/STALE: 5
- Active coordinator-owned (already staffed): 0428-059, 0428-058, 0428-181, 0428-183, 0428-216, 0428-271, 0428-273, 0428-274, 0428-275

## Read-only attestation

- No product file created or changed. Only `evidence/r28-welle6-2026-11-25/0428-backlog-triage/round-1.md` added.
- No PR opened, no CI triggered, no claim published, no subagent spawned.
- Frozen chain (1812/249 workflow, 1819/181 export, 1820/271 broker, 1818/078 dashboard, 1650/078 consent) untouched.

## clean

- no docker/podman/compose started; no containers, no networks, no volumes.
- `docker ps -a`: N/A (host is the coordinator server; no test stack permitted here).
- scratch clone `/tmp/baseharbor-remote-check` removed after ls-remote witnesses.

## END

w108-0428-216-backlog END_DONE
