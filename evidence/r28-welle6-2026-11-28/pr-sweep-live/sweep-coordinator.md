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
