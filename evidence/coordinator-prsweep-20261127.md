# PR-sweep reconciliation 2026-11-27T03:0xZ (coordinator, owner sweep request)

Census: 20 OPEN product PRs (baseharbor): 1650 1812 1818 1819 1820 1833 1855 1860-1872 (#1872 = baseline catalog act for 0428-344, added 26.11 sweep). #1615 MERGED. Plan main witness at publication: origin/main 41bfea7d8-era.

## Lane assignments (live sessions reconciled)
| Card | PR | Lane | State |
| --- | --- | --- | --- |
| 0428-321 | #1866 | w345 (busy) | active - steer-5 route (a) in flight: helper into catalogued internal/cli/cli.go + cli_test.go regression, context.Canceled:130 bypass must be disproven via production path; head c0c39f3b: run 45888974142 CANCELLED AND twin run 45889015791 TERMINAL FAILURE attempt-1 (Docker AND rootless Podman data-capabilities PASSED on exact head; Trusted Plan + PR Selected Checks failed SOLELY for uncataloged cmd/baha/main_test.go despite in-PR row = bootstrap proof). Corrected head + fresh exact-head run owed by w345 (steer-5) |
| 0428-344 | #1871 | w343 RELEASED (absent from /api/sessions) | BLOCKED (owner correction 03:2xZ): exact-head run 45888715532 terminal FAILURE - Trusted Plan: 11 uncataloged pagination sources (same bootstrap class as #1866). w343 waits on Plan PR #155 rows; acceptance blocked until rows + fresh green exact head |
| 0428-078 | #1650 #1818 #1855 #1867 | w346 (busy, plan-side only) / parked | blocked: #1818 OWNER HOLD on #1819 producer dep (#1812 chain); #1855/#1867 freeze-lift order; w346 = akte reissue transport for plan #150 |
| 0428-326 | #1868 | w341 (idle-parked) | blocked: pr-gate-map-v1.json release label still v0.4.27 (owner scope); RESUME = map landing |
| 0428-328 | #1869 | w342 (idle-parked) | blocked: same map gate |
| 0428-288 | #1870 #1833 | - (w332 released) | wait: #1870 ACCEPT merge-ready-HELD (w267, exact head d4e6b99c33d5, run 45876467179 SUCCESS); #1833 runtime qualification NOT covered (runtime jobs skipped) |
| 0428-312/318/329/299 | #1860-1863 | - (w333 released) | blocked-baseline: catalog admission via #136 family, freeze-lift chain |
| 0428-291 | #1864 #1865 | - (released) | blocked: #1865 ACCEPT held (c651db35); #1864 candidate blocked-BASELINE; order #136 hop -> #1865 merge -> #1867 |
| #1812/#1819/#1820 | - | - | owner holds unchanged (chain gate: BASEHARBOR_PR_DEMO_SOURCE_SHA variable) |

## Free capacity
Seats 5/5 after reconciliation: ornith 2/2 (w345, w346), laptop 2/2 (w341/w342 idle-PARKED on blocked cards 326/328 - external map gate, sessions alive), flash 1/1 (w347, NEW base-act lane replacing released w343). No free seat; no Ready card exists to reassign to (all backlog entries gated by freeze-lift, map landing, or owner chain holds). Codex: w267 idle after steer-5 decision; w255 idle RESERVED for #1866 exact-head review after w345 handoff + green. Two-Codex cap respected. candidate-count for Ready dispatch this minute = 0 (all non-conflicting backlog entries gated by freeze-lift, map landing, or owner chain holds); board-sha per table above.

## Baseline-family assignment (w255 disposition b, owner-confirmed 04:3xZ)
- Write-set: 10 catalog rows in scripts/pr-gate-coverage.json vs develop - belongs to EXISTING family 0428-359/#136 (card file t-20261126-trusted-catalog-baseline-recovery-manifest.md rides plan #136 branch; lands there on freeze-lift, no duplicate card).
- Lane record: w347-0428-344-baseline (session 1580581f), parked worktree at 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74, resumed 04:3xZ with corrected real-path mission.
- #1871: remains BLOCKED + catalog-free until baseline PR lands on develop AND owner requalifies exact head. Precedent: #1865 ACCEPT 7199319282 (row-before-candidate supported); w255 verdict comment 7202869676.

## W46 baseline act live (05:1xZ)
- #1872 OPEN vs develop, head 2a645d157c1849778caf01d6fa2532479b0cb972 (author=committer w347-0428-344-baseline), Hosted run 45893486909 IN_PROGRESS; predecessor 45893473011 CANCELLED (Draft-Go failures there are NOT results). Single lane assignment per owner (w347, no duplicate). #1871 stays blocked until #1872 lands AND fresh exact-head requalification.

### 1872 HOLD round (05:5xZ)
- w255 REVIEW-HOLD comment 7203179302: 9 rows vs claim 10; >=5 further uncataloged #1871 sources (applicationruntimeapi/handler.go, applicationsecretapi/handler.go, machine/navigation.go, machinereadmodels/artifacts.go, sourcetransfer/transfer.go). w347 correction round dispatched (mechanical diff-list method). Family trail note: plan #147 comment 7203181689. #1871 stays blocked.

## Idle-claim disposition + rule-gap register (owner consistency finding 20:57Z GitHub-time)
- w341/w342: cards 326/328 already blocked (map gate); owner fields blanked with RESUME triggers - idle parked sessions no longer masquerade as live claims. Sessions stay alive for fast resume.
- 0428-324: NOT dispatched - shares docs/reference/cli.md + errors.md write-set with active #1866 (conflicting). Register only.
- RULE GAP (to Codex disposition AFTER #1872 review, do NOT reinterpret silently): (i) TICK-DUTIES mandates claim-reconcile.py per tick but nothing calls it (basics-check/coord-tick-once lack it); script matches owner-name presence, not isWorking, and counts Codex sessions as workers; pool-reconcile counts all OpenCode sessions regardless of isWorking -> idle claims invisible, parked sessions = phantom capacity. (ii) doc conflicts: AGENTS 3.3 BUG-HUNT filler vs TICK-DUTIES hunt hold (owner); baseharbor-plan/AGENTS.md:45 maintainer-reserved assignment vs coordinator dispatch; lane naming AGENTS 3.6 (wNNN-prNNN) vs RUNBOOK 2.1 (wNNN-kartennr) unresolved; owner-rule dated 2026-11-28 while host date 26.11 (host clock ahead of GitHub time - known skew, label only).
- Plan shared checkout: untouched, nothing published from it (detached 4542ba252).

### 1872 ACCEPT (06:3xZ)
- w255 ACCEPT merge-ready-HELD: #1872 comment 7203347331 (exact head 3ed6882e010f0e9a33011be71740f64675d57527, run 45894876938 SUCCESS, base 5a37ddbd ancestor, 15/15 paths mechanically matched, one-file shape). Family trail recorded at plan #147 comment 7203349796. Lane w347 released. #1871: blocked until #1872 lands (owner merge at freeze lift) + fresh exact-head requalification. No merges by lanes.

## Owner-verified ACCEPT/dependency order (06:5xZ)
| Baseline PR | exact head | hosted run | review verdict | consumer |
| --- | --- | --- | --- | --- |
| #1872 | 3ed6882e010f0e9a33011be71740f64675d57527 | 45894876938 SUCCESS | ACCEPT 7203347331 (merge FORBIDDEN by PR body) | #1871 |
| #1865 | c651db35f34ae7f1d11279e0edb67171d2e3d200 | 45868149534 SUCCESS | ACCEPT 7199319282 HELD | #1864 |
| #1867 | 8b0eb51a12320acb8987aee1729c9a820d4d573e | 45872485574 SUCCESS | ACCEPT HELD | #1855 |
| #1870 | d4e6b99c33d52868409df445ea76d83d21bd7543 | 45876467179 SUCCESS | ACCEPT 7202318240 HELD | #1833 |
Rule: consumers requalify ONLY after actual baseline landing (owner merge at freeze lift) + fresh consumer exact-head Hosted CI. No double reviews, no new cards.
- Plan-side evidence: baseharbor-plan PR #156 (head 91187c329, OPEN, hosted validate; freeze-lift hop+squash-merge pending - admin, not by lanes).
