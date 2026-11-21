# PR census triage - 8 old open PRs

ROLE: Worker. CARD: t-20261114-r28-cli2-app-export (0428-065). TASK: PR census triage (Owner task, mission /var/tmp/triage1625.g.md). Moved off H-V21 hunt (done, akte 7e6f661ae).
BASE: develop 42da7128e724a533349e93d3742cbd232ea48936 (measured, real github origin via `git ls-remote`).
MODE: read-only triage, NO write in baseharbor. NO close/comment/merge/push to baseharbor. NO subagents. NO .github/scripts change. NO local suite tests. NO post to other sessions.

## PLAN

1. ls-remote (double-write protection) on real github origin; confirm develop = 42da7128e72, PR heads as mission states. Read-only; no git changes to product worktree. docker ps -a BEFORE/AFTER baseline.
2. Per PR: fresh fetch `refs/pull/<n>/head:refs/temp/tri-<n>` (fresh ref names, no reused path), then `git cherry -v 42da7128e72 refs/temp/tri-<n>` ('+' = not in develop, '-' = already in) and `git log --format=%h %an`; `git merge-base --is-ancestor refs/temp/tri-<n> 42da7128e72` = whole head already in develop -> 'superseded'.
3. If not ancestor: what is missing for a merge (hop? test registration? open card?) - one sentence with file:line.
4. Check card via `python3 scripts/plan.py show <karte>` (plan-repo path) - still alive or replaced by newer PR.
5. RESULT as table in evidence/r28-welle4-2026-11-21/pr-census-triage/triage.md. H-V21 results below with one reference line each. END: one line per PR + plan-sha.

## Double-write protection (before any git action)

git remote -v (REMOTE GUARD):
origin https://github.com/mcpdev80/baseharbor.git (fetch)
origin https://github.com/mcpdev80/baseharbor.git (push)

git ls-remote BEFORE work:
42da7128e724a533349e93d3742cbd232ea48936 refs/heads/develop
074678d149e5b8d0f899c55da92debf52bf0fd46 refs/pull/1597/head

All 8 PR heads fetched to FRESH temp refs and verified against mission SHAs:
refs/temp/tri-1597 = 074678d149e5b8d0f899c55da92debf52bf0fd46
refs/temp/tri-1614 = 80d4df52e913e4472334a5f257fe868d26d5976e
refs/temp/tri-1620 = 28cb907dc0a678d1b5326df5203741c70cf84978
refs/temp/tri-1623 = 4cbf92960cb5d97077370b7da052d45523ce0043
refs/temp/tri-1645 = 4d73aa97808d000d2f70eaa193f8dbfc14e817a7
refs/temp/tri-1650 = 28c18f02039f0957544146cf5d0db2a1561a4220
refs/temp/tri-1723 = 71ac9ba51b72a386bc76ea2948b3a10e1ad76e1f
refs/temp/tri-1725 = 0208f725996dbd3dd2889c984e045a2527454499

Worktree git status after read-only investigation: clean (no staged/unstaged changes to product files).

## TRIAGE TABLE

Columns: PR | head | in develop? | klassifikation | begruendung w/ exact command witness.

Method witnesses per PR: `git cherry -v 42da7128e72... refs/temp/tri-<n>` (line count of '+'), `git merge-base --is-ancestor refs/temp/tri-<n> 42da7128e72`, card via `python3 scripts/plan.py show`.

| PR | head | in develop? | klassifikation | begruendung (command witness) |
| --- | --- | --- | --- | --- |
| #1597 | 074678d149e5 | nein | hop-noetig (lebt, card active) | cherry +1 (074678d1 "0428-076: REQUEST CHANGES fix - per-target database panel builder + resolved Perses variables"); merge-base IS_ANCESTOR=no; card t-20261114-r28-perses-tempo-source state=wait, depends perses-contract-seam/perses-runtime/perses-signal-inventory accepted (plan.py show) - work not merged, one commit pending on top of develop. |
| #1614 | 80d4df52e913 | teilweise | lebt (card active, multi-hop) | cherry +4 (eda0cd61 "feat(r28): extend app sources and unique components (0428-059)", 98877cc1 unify app status/versions, 6377f1b2 retained per-provider placement, 80d4df52 gate two native Core lifecycle tests); merge-base IS_ANCESTOR=no; card t-20261114-r28-cli2-app-status state=wait - 0428-059 line still open, 4 commits pending. |
| #1620 | 28cb907dc0a6 | nein | hop-noetig (card wait) | cherry +3 (e7eeeb58 merge into w067, fcba5d25 fail closed on reveal audit, 28cb907d test 0428-067 verified operator); merge-base IS_ANCESTOR=no; card t-20261114-r28-cli2-wizard-platform state=wait - 0428-067 reveal-work still unmerged. |
| #1623 | 4cbf92960cb5 | teilweise | lebt (partly merged) | cherry +4 / -1 (78e8257e "guided app logs/exec/urls (0428-063)", beb2ee58 exit-status preservation, AND '-' 8014d71e "ci: trigger qualifying pull_request run - card t-20261114-r28-cli2-app-interact" ALREADY IN develop); merge-base IS_ANCESTOR=no; card t-20261114-r28-cli2-app-interact state=wait - one ci.yml trigger commit already in develop, remaining 0428-063 content not yet merged. |
| #1645 | 4d73aa97808d | nein | hop-noetig (card wait) | cherry +1 (4d73aa97 "fix(0428-091): Perses Tempo datasource adapter with routable gateway-alias endpoint and enforced mTLS (r2)"); merge-base IS_ANCESTOR=no; card t-20261120-r28-valkey-dashboard-unavailable-only state=review - 0428-091 one commit pending. |
| #1650 | 28c18f02039f | nein | hop-noetig (card wait) | cherry +6 (865d4410 "fix(0428-078): verified-only identity-dashboard gate (r8)", 09933158 bind Keycloak witness to target state, 47f5953c require exact Keycloak signal, 20a35cd7 authenticate status fixture, 97aa1a86 preserve remote readiness, 28c18f02 test connect keycloak metrics producer); merge-base IS_ANCESTOR=no; 0428-078 keycloak-witness line still fully open, 6 commits pending. |
| #1723 | 71ac9ba51b72 | nein | hop-noetig (card active) | cherry +1 (26755fc1 "fix(0428-199): respect --workload-port on local apply/up path"); merge-base IS_ANCESTOR=no; card t-20261120-workload-port-flag-ignored-locally state=active - single fix commit pending. |
| #1725 | 0208f725996d | nein | hop-noetig (card wait) | cherry +1 (9bf4a72f "0428-201: name shared backend state version mismatch"); merge-base IS_ANCESTOR=no; card t-20261120-shared-backend-state-version-message state=wait - single commit pending. |

No PR head is an ancestor of develop 42da7128e72 (all IS_ANCESTOR=no): none is fully superseded / already in develop. Seven PRs have all their content pending on top of develop; #1623 is partially merged (one ci.yml trigger commit already in develop via 8014d71e). None of the eight carries a merge-ready diff against this develop head: all require a fresh hop onto 42da7128e72 (the develop head moved from the 1080986f / 513488ee era to 42da7128e72 since each PR was last open).

## What is missing for a merge (per PR)

- All 8: the PR head must be re-hopped onto develop 42da7128e72 (a no-ff merge of the current develop, preserving prior commits as SHA-identical ancestors per AGENTS 5.2). No hop has been made against this develop head - the bases are all older.
- #1623 additionally: the ci.yml qualifying-pull_request trigger (8014d71e) is already in develop, so its remaining 0428-063 commits need a hop but the trigger gap is closed.
- Test-registration / card-open status: cards #1597(0428-076) wait, #1614(0428-059/app-status) wait, #1620(0428-067) wait, #1623(0428-063) wait, #1645(0428-091) review, #1650(0428-078) open, #1723(0428-199) active, #1725(0428-201) wait - all still live cards, none replaced by a newer PR in the plan. (plan.py show per PR head above.)

## H-V21 results (prior slice, one reference line each)

- Slice 1 (#1627/#1736 env destroy, missing registry entry + existing dir tree): FAILS CLOSED - NotFound / ambiguous / damaged-state error, or idempotent "already absent" (nothing deleted, source preserved) at cmd/baha/app_context.go:360 + app_destroy_lifecycle.go:56-133. Not silent success / no-op / partial deletion. Severity: nicht-blockierend.
- Slice 2 (etcd snapshot-attest, etcdctl.go:73-78 'attest := s.Attest; if attest == nil'): attest ALWAYS runs - nil falls back to attestEndpointStatus (etcdctl.go:152-194), cluster-identity check runs at etcdctl.go:81, caller re-validates at etcd.go:168. Attest is test-only seam (runtime_integration_test.go:174). Severity: nicht-blockierend.
- Slice 3 (cli-machine-coverage, registration_ci_readiness_test.go:82): 183 command paths (incl. aliases) all covered, 0 classified 'gap'; groups without Run -> 'presentation' (machine_coverage.go:60-63). Severity: nicht-blockierend.

## repo-rule compliance

- Read-only triage only: NO commit, NO push, NO PR, NO comment, NO close, NO merge in baseharbor (mission rule; AGENTS 5.2, AGENTS 3.8 one candidate per chain).
- No subagents (AGENTS 4.8). No .github/** / scripts/** change (triage_pr.sh is evidence-only, in the own plan-worktree). No local suite tests. No post to other sessions.
- All 8 PR heads fetched to FRESH ref names (refs/temp/tri-<n>), no reused path.
- Card state via `python3 scripts/plan.py show` (plan-repo path), never a product checkout.
- Evidence written only in the own plan-worktree (baseharbor-plan, tooling #29); never in the product checkout.
- Worktree git status: clean (no product changes).

## cleanliness

- docker ps -a BEFORE: 8 containers (all pre-existing, Exited, names bh-itest-* from other lanes).
- docker ps -a AFTER: 8 containers (unchanged; no containers/compose started; triage was read-only git).
- No new networks / volumes / state directories created.
- ambient-core / fremder-carrier images: unangetastet.
- worktree git status: clean (no staged/unstaged changes).
