# PR-sweep reconciliation 2026-11-27T03:0xZ (coordinator, owner sweep request)

Census: 19 OPEN product PRs (baseharbor): 1650 1812 1818 1819 1820 1833 1855 1860-1871. #1615 MERGED. Plan main witness at publication: origin/main 41bfea7d8-era.

## Lane assignments (live sessions reconciled)
| Card | PR | Lane | State |
| --- | --- | --- | --- |
| 0428-321 | #1866 | w345 (busy) | active - steer-5 route (a) in flight: helper into catalogued internal/cli/cli.go + cli_test.go regression, context.Canceled:130 bypass must be disproven via production path; head c0c39f3b: run 45888974142 CANCELLED AND twin run 45889015791 IN_PROGRESS attempt-1 (Trusted Plan terminal FAILURE uncataloged cmd/baha/main_test.go despite the in-PR row = bootstrap proof; Docker native PASS, Podman native running). Corrected head + fresh exact-head run owed by w345 (steer-5) |
| 0428-344 | #1871 | w343 (busy) | BLOCKED (owner correction 03:2xZ): exact-head run 45888715532 terminal FAILURE - Trusted Plan: 11 uncataloged pagination sources (same bootstrap class as #1866). w343 waits on Plan PR #155 rows; acceptance blocked until rows + fresh green exact head |
| 0428-078 | #1650 #1818 #1855 #1867 | w346 (busy, plan-side only) / parked | blocked: #1818 OWNER HOLD on #1819 producer dep (#1812 chain); #1855/#1867 freeze-lift order; w346 = akte reissue transport for plan #150 |
| 0428-326 | #1868 | w341 (idle-parked) | blocked: pr-gate-map-v1.json release label still v0.4.27 (owner scope); RESUME = map landing |
| 0428-328 | #1869 | w342 (idle-parked) | blocked: same map gate |
| 0428-288 | #1870 #1833 | - (w332 released) | wait: #1870 ACCEPT merge-ready-HELD (w267, exact head d4e6b99c33d5, run 45876467179 SUCCESS); #1833 runtime qualification NOT covered (runtime jobs skipped) |
| 0428-312/318/329/299 | #1860-1863 | - (w333 released) | blocked-baseline: catalog admission via #136 family, freeze-lift chain |
| 0428-291 | #1864 #1865 | - (released) | blocked: #1865 ACCEPT held (c651db35); #1864 candidate blocked-BASELINE; order #136 hop -> #1865 merge -> #1867 |
| #1812/#1819/#1820 | - | - | owner holds unchanged (chain gate: BASEHARBOR_PR_DEMO_SOURCE_SHA variable) |

## Free capacity
No idle worker seat: ornith 2/2, laptop 2/2, flash 1/1 busy or parked-on-external-gate. Codex: w267 idle after steer-5 decision; w255 idle RESERVED for #1866 exact-head review after w345 handoff + green. Two-Codex cap respected. candidate-count for Ready dispatch this minute = 0 (all non-conflicting backlog entries gated by freeze-lift, map landing, or owner chain holds); board-sha per table above.
