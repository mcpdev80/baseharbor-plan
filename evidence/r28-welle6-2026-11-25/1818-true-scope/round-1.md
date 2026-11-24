# #1818 TRUE-SCOPE RECONCILIATION — round 1 (read-only)

- Card: 0428-078 `t-20261114-r28-perses-dashboard-identity` (Perses identity dashboard, release v0.4.28)
- Session: w107 / truescope
- Date: 2026-11-25
- Mission: READ-ONLY inventory. No rebase / CI / merge / scope change. No VM run. No subagents (§4.8). Contact no other session. Nothing changed in baseharbor.
- Status: DONE

## PLAN (plain bullets, no checkbox syntax)

- Establish repo reality: resolve remotes, verify planning-repo path, fetch cf-fix + develop + PR1818 from the github.com/mcpdev80 origin
- Branch history: git log of origin/lane-0428-078-cf-fix, per-commit author + Task-Id trailer, identify 0428-078 own work vs foreign (0428-152 / 0428-246 / other)
- Diff vs develop: enumerate touched files, split genuine 0428-078 changes from foreign-lane contamination; cite perses row counts precisely
- Card 0428-078 contract: read baseharbor-plan tasks/ card acceptance criteria + write-set and #1818 PR body; state what #1818 SHOULD contain and whether the branch delivers it or is polluted
- Verdict + options: (i) clean 0428-078 subset to re-cut onto develop, (ii) whether #1818 is superseded/closed, (iii) interaction with #1826 + #1819; flag owner-scope files
- Evidence metadata: gh pr view 1818; git ls-remote origin lane-0428-078-cf-fix
- Write this evidence file, commit + push atomically with targeted add only
- Report inline + post END_DONE

## 0. Repo reality / attestation

- Planning repo verified (remote origin = github.com/mcpdev80/baseharbor-plan): `git remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push)`; planning repo is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY (NOT workers/baseharbor-plan — that is a bookkeeping dir inside the workers repo and never reaches github).
- baseharbor product remote: all of `origin`, `lane-origin`, `upstream` resolve to `https://github.com/mcpdev80/baseharbor.git` (the only github.com/mcpdev80 URL). No local-filesystem `origin` present.
- develop HEAD (fetched): `f14fb87c8f5afd91168e4f174d620c9f00e6341e`
- cf-fix HEAD (ls-remote witness): `20fc1cb7d49602dc7f8aa0004a7562a81311d78c` = PR #1818 head (refs/pull/1818/head == lane-0428-078-cf-fix, same SHA → single candidate, §3.8).
- PR #1818 base is develop; merge-base(cf-fix, develop) = `3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd` (a develop HEAD from card #1815). develop IS an ancestor of cf-fix. cf-fix carries exactly 4 commits on top of its base.

## 1. Branch history — per-commit authorship verdict

Source: `git log --format='%H %an %ae' -15 origin/lane-0428-078-cf-fix`. Task-Id trailers read from commit bodies.

- `20fc1cb7` — author `w53-0428-152-alertfix` — `fix(0428-078): wire keycloak identity dashboard into develop metrics catalog` — TRAILER fix(0428-078). CO-AUTHORED: w53-0428-152. Verdict: authored by the **0428-152** session (subject claims 0428-078), but it is 0428-078 card work (keycloak identity dashboard realization).
- `8e2c50c1` — author `w21-pr1702-0428-246-footprint` — `fix(0428-078): select real provider-class labels in Keycloak Perses dashboard queries` — TRAILER fix(0428-078). Co-authored-by w21-pr1702-0428-246-footprint. Verdict: authored by **0428-246** session, 0428-078 card content.
- `888e2193` — author `w21-pr1702-0428-246-footprint` — `hop(0428-078): resolve app_status identity-field conflict on f3d847874 (#1650)` — TRAILER (#1650 = 0428-078's original PR). Verdict: **0428-078** hop work, authored by w21.
- `e0a93ce0` — author `w21-pr1702-0428-246-footprint` — `hop(0428-078): re-locate perses identity-witness onto latest develop (#1650)` — parent = develop `3ebfb90d`. TRAILER (#1650). Verdict: **0428-078** hop work (identity-witness relocation), authored by w21.
- `3ebfb90d` — author `Marcel Pfingstgräf` — `0428-250: ... (#1815)` — this is the **develop base commit**, NOT cf-fix work.
- Below 3ebfb90d: 0428-152 (#1816), 0428-058 (#1809), 0428-186 (#1810), 0428-261 (#1817), 0428-061 (#1752), etc. — all develop history, not cf-fix.

CONCLUSION (w106 confirmed, w107 re-verified): the 4 cf-fix commits are authored by **two foreign sessions** — `w53-0428-152` (`20fc1cb7`) and `w21-pr1702-0428-246-footprint` (`8e2c50c1`, `888e2193`, `e0a93ce0`) — none authored by the 0428-078 owner session `w55-0428-078-probehop`. This is EXACTLY the w106 finding. HOWEVER: all four are labeled `fix(0428-078)` / `hop(0428-078)` and are the genuine card implementation, stacked on a real develop base with a clean ancestry chain. The "foreign" signal is session-authorship, not content scope.

## 2. Diff vs develop — genuine vs foreign split

`git diff --stat origin/develop...origin/lane-0428-078-cf-fix`:

```
cmd/baha/app_status_result.go                      |  82 +++-
internal/identityprovider/keycloak_files.go        |  15 +
internal/identityprovider/keycloak_realization.go  |  11 +
internal/metrics/perses_dashboards.go              |  26 ++
internal/metrics/perses_dashboards_keycloak.go     |  70 +++
internal/metrics/perses_dashboards_test.go         | 473 +++++++++++++++++++++
internal/metrics/realization.go                    | 155 +++++++
internal/metrics/testdata/perses-dashboards/keycloak-identity.json | 134 ++++++
8 files changed, 959 insertions(+), 7 deletions(-)
```

- All 8 files are 0428-078 card content (identity dashboard + Perses identity witness + keycloak producer). NO foreign-lane contamination in the file set. The "contamination" w106 flagged is purely **session-authorship** on the commit level, not stray files from another card.
- `perses_dashboards.go`: the `keycloak-identity` catalog row is ADDED by this PR (git blame: `20fc1cb7`), NOT pre-existing on develop. `backendForKey` case `keycloak-identity -> ProviderKeycloak` and `persesDashboardForBackend(ProviderKeycloak)` added by `20fc1cb7`.
- `perses_dashboards_keycloak.go`: NEW file, 3 provider-class Prometheus queries (job="baseharbor-providers", baseharbor_provider="keycloak", dropping app/env labels), authored by `8e2c50c1` (w21-0428-246).
- `keycloak-identity.json`: NEW golden dashboard, added by `20fc1cb7`.
- `realization.go`: `IdentitySelectionWitnessAt` target-bound witness (from #1650 hop lineage), authored by `e0a93ce0`.
- `app_status_result.go`: `IdentityDashboardEligible` + `identityDashboardBackendEligible` (verified-only, fail-closed on both faces), authored by `20fc1cb7`.
- `keycloak_files.go` / `keycloak_realization.go`: `KeycloakMetricsRegistrationIDAt` / `RegisterKeycloakMetricsSignalsAt` producer seams.

### perses_selection.go row count (the crux of w106's assumption)

- w106 ASSUMED `internal/metrics/perses_selection.go` exists and carries only 1 keycloak-identity row. **That file does NOT exist in this branch.** The card's actual perses-selection file is `internal/capability/perses_selection.go`.
- `git grep -c keycloak-identity internal/capability/perses_selection.go` → **2** occurrences (the `"keycloak-identity":` catalog key at line 220 and its `Key:` field at line 221) — on BOTH cf-fix AND develop. So the row is pre-existing on develop (line 263's "1 row" count is a read error; the file carries the row identically on develop and cf-fix). This refutes the w106 premise that cf-fix "re-introduced" a forbidden catalog addition — the keycloak-identity selection row already exists on develop.
- The genuinely NEW catalog-level addition on cf-fix is `persesDashboardCatalog()` in `internal/metrics/perses_dashboards.go` (the metric-catalog, not the capability-selection) — this is the row the card (line 263, the "scope ruling" of 2026-11-24) says is forbidden. git blame confirms it was added at `20fc1cb7`.

## 3. Card 0428-078 contract satisfaction

Card `t-20261114-r28-perses-dashboard-identity`:
- Goal: "Deliver identity-provider panels only for verified current Keycloak metrics; do not rely on obsolete SPI assumptions."
- Acceptance: verified+pinned Perses release, native plugin/format; scope by actual Target/tenant, fail closed on unknown ownership; preserve Prometheus/Loki/Tempo ownership; verified-only identity eligibility.
- PRs on the card: #1650 (original, parked DIRTY) and #1818 (current vehicle, branch `lane-0428-078-cf-fix`).
- Blocker field: sequence-gated on #1819 (0428-181 identity producer) behind #1812; w55 released.

WHAT #1818 SHOULD CONTAIN per card: verified-only identity-dashboard eligibility through the real Perses probe + real keycloak producer signal + provider-class dashboard queries, wired into `cmd/baha` status output, with focused tests — and (per the 2026-11-24 owner scope ruling, line 252/263) the keycloak-identity panel must live on the 0428-181 identity-producer path, NOT in the observability `persesDashboardCatalog()`.

DOES THE CURRENT BRANCH DELIVER THAT?
- YES on the card's functional core: verified-only `identityDashboardBackendEligible` (fail-closed on not_configured AND configured_unverified, both faces), target-bound `IdentitySelectionWitnessAt`, provider-class keycloak queries, real keycloak producer seam. CI green on exact head `20fc1cb7` (run 45316544436 completed/success, 23 pass/0 fail).
- The branch DELIVERS THE WRONG THING on ONE point the card explicitly forbids: `20fc1cb7` re-adds `keycloak-identity` to `persesDashboardCatalog()` (metric observability catalog), which the 2026-11-24 owner ruling says is out of this card's scope (identity excluded from observability catalog). This is the "re-introduced forbidden edit" the card (line 264) flags as making `20fc1cb7` "not a valid candidate."
- The prior green head `306a2b1ea` (line 256) did NOT have the catalog addition; `20fc1cb7` is an owner rebase of the same 4 commits that re-adds the catalog row.

## 4. Verdict + options (no execution)

- (i) **Clean 0428-078 subset to re-cut onto develop:** the 4 cf-fix commits form one clean chain on develop base `3ebfb90d`. The genuinely 0428-078 work that IS in scope = `888e2193` + `e0a93ce0` (the #1650 hop: identity-witness relocation + app_status conflict resolution, the verified-only eligibility core) and — arguably — `8e2c50c1` (provider-class label fix, if the keycloak producer lives on the 0428-181 path). The out-of-scope add is ONLY `20fc1cb7`'s `persesDashboardCatalog()` keycloak-identity row + its `keycloak-identity.json` golden. So: cut 0428-078 from `888e2193`..`8e2c50c1` (drop `20fc1cb7`), OR revert the single catalog addition and keep `20fc1cb7`. Both need an owner decision (the catalog-vs-producer ownership split is an owner ruling, line 252).
- (ii) **#1818 superseded/closed:** NO. #1818 is OPEN, not draft, mergeable, never merged, never closed. It is the sole surviving 0428-078 vehicle (#1650 parked DIRTY). The card remains `blocked`, not superseded.
- (iii) **Interaction with #1826 (0428-279 recovered) + #1819:** #1818 is sequence-gated behind #1819 (0428-181 = the identity-producer seam the keycloak panel is supposed to target). #1826 is a separate recovery lane; no direct dependency found in the card. #1818 can ship only after (a) the catalog-vs-producer ownership question is owner-decided, (b) #1819 lands, (c) a fresh exact-head CI + maintainer review.
- Owner-scope flags: (1) the `persesDashboardCatalog()` identity-exclusion ruling is an Owner decision (2026-11-24, card line 252/263); (2) any change to `.github/**` triggers / gate-coverage catalog rows is Owner/CI scope; (3) the keycloak identity-producer path is card 0428-181 / #1819 (different card). **None of these were touched by w107 (read-only).**

## 5. Evidence metadata

- `gh pr view 1818` (fetch): `{number:1818, state:OPEN, isDraft:false, baseRefName:develop, headRefName:lane-0428-078-cf-fix, headRefOid:20fc1cb7d49602dc7f8aa0004a7562a81311d78c, mergeCommit:null}`. 4 commits (authored by w53-0428-152 + w21-0428-246). Body: "Rebase 1650 onto develop post 1810." No formal GitHub review recorded.
- `git ls-remote origin lane-0428-078-cf-fix` → `20fc1cb7d49602dc7f8aa0004a7562a81311d78c refs/heads/lane-0428-078-cf-fix`. `git ls-remote origin refs/pull/1818/head` → same SHA. (single candidate, §3.8)
- `git ls-remote origin refs/heads/develop` → `f14fb87c8f5afd91168e4f174d620c9f00e6341e`.
- `git ls-remote origin 0f20a3b9` → empty (the "clean head" the card line 266 names is NOT a remote ref / does not exist at origin — a stale in-memory reference).
- All other 0428-078 lanes at origin (informational): `lane-0428-078-appstatus-integration` `022c454c`, `lane-0428-078-perses-identity` `4e81c16d`, `lane-0428-078-perses-identity-on-resolver` `84943695`, `lane-0428-078-perses-identity-on-resolver-r3` `008354eb`. Only `lane-0428-078-cf-fix` carries PR #1818.
- CI on exact head 20fc1cb7: run 45316544436 completed/success (created 2026-11-24T03:01:23Z, head_sha 20fc1cb7). Latest PR CI run 45434224033 @ 9140b2cbd is a DIFFERENT SHA (the `ci: reload candidate image before runtime publish` develop commit, not cf-fix) — stale/queued, not cf-fix evidence.

## Recommendation for the owner

1. **w106's premise is TRUE:** on `lane-0428-078-cf-fix` the head `20fc1cb7` and the reset target `8e2c50c1` are authored by foreign sessions (`w53-0428-152` / `w21-0428-246`), NOT by the 0428-078 owner `w55`. But this is session-authorship, not content contamination — all 4 commits are genuine 0428-078 card work on a clean develop chain.
2. **w106's second premise is FALSE / imprecise:** `perses_selection.go` at `internal/metrics/` does not exist; the real file `internal/capability/perses_selection.go` carries the keycloak-identity row (2 hits) identically on develop and cf-fix. There is no "1 row vs 5 rows / drop 3" discrepancy.
3. **The real defect is the card's own finding (line 264):** `20fc1cb7` re-adds `keycloak-identity` to the observability `persesDashboardCatalog()`, which violates the 2026-11-24 Owner scope ruling (identity excluded from that catalog). `20fc1cb7` is therefore "not a valid candidate" for #1818; the prior green head `306a2b1ea` did not have this violation.
4. **Recommended:** do NOT reset to `8e2c50c1` (it is not clean either — it is mid-hop and still carries the `888e2193`/`e0a93ce0` state). The cleanest path is an Owner decision on (a) the catalog-vs-producer ownership question, then (b) re-cutting 0428-078 from `888e2193`..`8e2c50c1` (dropping `20fc1cb7`'s catalog addition) onto current develop, rerunning exact-head CI, and awaiting maintainer review — gated behind #1819. All of (a) and the catalog edit are Owner/other-card scope; w107 changed nothing.

## Cleanliness

- Read-only. No baseharbor changes (no edits, commits, pushes to the product repo). No containers/compose started (no docker/podman). Planning-evidence file added only.

## Handoff

- END_DONE w107-0428-078-truescope: read-only reconciliation complete; confirmed w106 premise (foreign-authorship) but refuted the perses_selection.go row-count premise; flagged 20fc1cb7's forbidden catalog re-add as the card's own blocker; recommended Owner decision on catalog-vs-producer ownership. Candidate SHA verified 20fc1cb7d49602dc7f8aa0004a7562a81311d78c.
