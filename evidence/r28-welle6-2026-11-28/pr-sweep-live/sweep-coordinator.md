# PR Sweep - live GitHub reconciliation (coordinator; REPUBLISHED 2026-11-28 12:3xZ - original commits edd6533f9/6e23dd519 LOST from origin/main in the 99a43a598-era merge churn; content reconstructed + revalidated)

develop = 99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82. 8 open core PRs (#1615 merged, out of sweep). No merge without exact-current-base Hosted CI + independent Codex review. No local tests as evidence; auth/consent preserved.

| PR | head | state | qualifying? | disposition / owning lane |
| --- | --- | --- | --- | --- |
| #1842 | 50c6d84e6 | UNSTABLE | Selected Checks PASS (45626853905+45631228584) BUT Demo Pin SKIPPED + candidate-added advisory FAILED; pin dispatch 45627034676 FAILED (8/14 light gates docker+podman policy/connectivity/reconciliation/full-destroy; Aggregate runtime-light FAIL) | NOT ACCEPTED. w198 chain: real-stream fixture fix -> Hosted Demo CI -> demo merge -> PIN ADVANCE -> requal w/ EXACT required runtime gates + 2 fresh PR greens on new head. Dependent hops stay blocked until then. |
| #1650 | 903991f3b | BLOCKED | 45632065203 FAILS Trusted Plan (uncataloged internal/metrics/identity_dashboard_witness.go); dispatch 45636081059 CANCELLED all-acceptance-jobs-skipped = VOID | w165: minimal catalog row scripts/pr-gate-coverage.json (docker+podman data.capabilities) + env-isolation fix already ordered; fresh pair after; acceptance refresh behind #1842 gate. |
| #1835 | 736750fb0 | BEHIND | old 45621130912 passed - behind, nonqualifying | WAIT: ONE refresh after #1842 merge (red-first + serial docker->podman + status.md). |
| #1833 | a7b0a4804 | BEHIND | 45571699415/45573394850 FAILED | WAIT: fresh-lane requal after pin advance. |
| #1820 | 28803d110 | BEHIND | 45382404741 cancelled | WAIT: clean fresh cut after #1819 merge. |
| #1819 | 17381017b | BEHIND | 45380314808 cancelled | WAIT: after #1812 merge. |
| #1818 | 20fc1cb7d | BEHIND | 45316544436 green on CONTAMINATED base - void | OWNER PRE-AUTHORIZED: after #1819 merge, clean reset/rebuild from 0f20a3b97fa33a0c3ff1476ef32866b4fe008f5f; verify C = TestPersesKeycloakDashboardQueriesSelectRealProviderLabels via persesDashboardProvisionForLifecycle producer seam (not direct catalog/write projection) + target-bound eligibility regression + candidate-digest consent; prohibited dataset stays prohibited. |
| #1812 | eafd5e6d6 | BEHIND | 45515177008 pass, dispatch 45515666142 FAILED | WAIT: hop after #1842 merge; first commit identity w198-0428-284-demo-parser (transfer record 0428-284 body), body link update. |

## card->PR canonical map (prs-field scan)
#1650+#1818 -> t-20261114-r28-perses-dashboard-identity | #1833 -> t-20261116-r28-bug-compose-service-ids | #1835 -> t-20261116-r28-bug-installation-reset-recovery | #1819 -> t-20261120-r28-identity-dashboard-catalog-consumer | #1820 -> t-20261124-r28-broker-build-identity-commit | #1842+#1812 -> t-20261125-0428-284-1812-postretry-gate-failure (0428-249 historical CLOSED).

## 0428-224 step-4 status (w119b, END_BLOCKED accepted 12:0xZ)
5 fix-rows MISMATCH awaiting OWNING requal commits (#1812 lv4-verify vs w198 owner; #1833 w124; #1820 lv4-verify; #1819 0428-061-sourcepull; #1818 w53-0428-152-alertfix); #1842 withheld pending demo/pin path; #1650 identity OK. Rows re-qualify automatically once owner lanes land frontmatter-exact commits + CI + review. Staging: workers/w119b-0428-224-step4/evidence/akte-step4.md (freeze-honored local zone).

## sequencing (simplest-to-hardest)
1. #1650 catalog+isolation commit (fix-ready work). 2. #1842 via w198 (gates everything). 3. GO-wave: #1835 refresh, #1812 hop, #1819, #1820 fresh cut, #1818 pre-authorized reset, #1833 post-pin. 4. Freeze-staged intakes (H-V47 10 cards, H-V52 4 findings) publish at owner lift.

## VERIFICATION ANSWERS (owner status query, 2026-11-28 14:0xZ)
- FRESH #1842 CODEX VERDICT EXISTS: 'CODEX REVIEW DISPOSITION - CHANGES REQUESTED' on exact head 50c6d84e6 (PR #1842 comment 2026-11-25T15:19:27Z + supplemental merge-gate note 15:20:31Z, %an check included). Reviewer: w136-codex lane (session 8c2a0c10 - roster-verified alive/busy; 'gone' report was stale). Separate merge NOT granted by that verdict; requested fix = selector/runner agreement for EVERY active release with standalone .demo-ref pin: scripts/pr-check-runner.py:383-392 (trusted side still v0.4.27-era) + scripts/pr-gate-plan.py:1182 regex (27/28-only vs test comment 'ANY active release') + resulting Demo-Pin-skip in PR runs.
- => #1842 status: CHANGES (not accepted, no merge on advisory alone - matches owner instruction); remedy lies inside card 0428-284's authorized scope (w198's running mission covers selector work; no NEW dispatch needed - verdict akte is the input at next contact-allowed moment).
- #1615: already CLOSED on plan with evidence - cards t-20261114-r28-cli2-identity-secrets (accepted, owner-direkt) and t-20261120-r28-ci-stacked-base-conditions (accepted, Codex pr-sweep path) reference it; merge witness: develop ancestor chain per earlier sweep (merged before this shift's tip moves).
- Pool: Coordinator + w198 'suspend' reports in OpenCode-DB NOT confirmed via codeman roster (both respond; w198 busy) - treated as DB-view artifact, watch item only.

## #1842 EVIDENCE UPDATE + ADMISSION-RAIL CROSS-CHECK (2026-11-28 14:4xZ, owner relayed)
- w136 CHANGES comment now COMPLETE on PR. Required fix (stays in EXISTING w198 lane, no new dispatch): trusted scripts/pr-check-runner.py + selector for ALL active releases with .demo-ref + regression tests v0.4.22/.23/.27/.28 + non-pin/inactive cases; acceptance then = exact-head PR 'Demo Pin' SUCCESS + relevant explicit-demo_ref dispatch slices SUCCESS.
- Identity admission rail (separate w136 note 15:20Z): head author currently w177-0428-284-demo-pin-1812, canonical owner w198-0428-284-demo-parser; merge only after DOCUMENTED admission rail, no history rewrite.
- CROSS-CHECK vs 0428-284 transfer record (published in card body, recovery transfer 2026-11-28): CONSISTENT - the transfer record already states exactly this rail: historical w177 commits stay untouched (no rewrite), the NEXT commit on #1842/#1812 must carry 'w198-0428-284-demo-parser' verbatim via git -c + %an gate. So the rail = w198's fix-forward commit + %an witness in round-akten + this sweep entry; w136 re-review verifies .commit.author.name==w198-string on the fix head before any merge.
- Sequencing unchanged: #1842 fix -> pair+dispatch greens -> w136 verdict/merge -> GO-wave (#1835 refresh, #1650 refresh, #1812 hop identity w198, then #1819/#1820/#1818/#1833).
