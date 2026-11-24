# #1818 branch contamination — owner-authorized reset evidence (2026-11-24)

Finding: PR #1818 (card 0428-078) branch `lane-0428-078-cf-fix` was contaminated by a
cross-session FORCE-PUSH from a session owned by a DIFFERENT card.

- Branch force-pushed `0f20a3b9 -> 20fc1cb7` by **w53-0428-152-alertfix** (card 0428-152 / PR #1816, unrelated to 0428-078).
- Contaminated head **20fc1cb7** re-introduces the FORBIDDEN observability-catalog edit: `keycloak-identity` entry in `internal/metrics/perses_dashboards.go` `persesDashboardCatalog()`/`backendForKey` (2 matching hits) plus a `ci_integration_operator_enabled.go` fixture (#1815) that belongs to a different lane's ownership.
- Clean head **0f20a3b9** = `0f20a3b97fa33a0c3ff1476ef32866b4fe008f5f`: 0 keycloak-identity catalog hits (real-probe consumption only), NO catalog violation.
- False-green evidence (VOID after reset): run **45316544436** (23 pass / 0 fail) and **45313048505** (20 pass / 0 fail) were GREEN ONLY because the forbidden catalog entry was present on 20fc1cb7 — "green by scope violation".
- Owner ruling (2026-11-24): #1818 reopened review->active; reset branch to 0f20a3b9; 20fc1cb7 and its derived proofs are VOID; w55 locked until C complete; re-introducing the forbidden record is prohibited (raise an open QUESTION first if C appears to need it).

Witness: `git diff --name-only origin/develop 0f20a3b9` lists #1818's files with no perses_dashboards.go catalog addition; `git show 0f20a3b9:internal/metrics/perses_dashboards.go | grep -c '"keycloak-identity":'` = 0 vs 20fc1cb7 = 2.
