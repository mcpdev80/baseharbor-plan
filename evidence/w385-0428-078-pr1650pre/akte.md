# w385-0428-078-pr1650pre — Disjunktive Vorarbeit: PR-Zeugen + lokales develop-Merge

LANE w385-0428-078-pr1650pre. KARTE 0428-078. REPO baseharbor. MISSION 2026-11-27.
ART: DISJUNKTE VORARBEIT (lokales Hoppen + Feststellung). Kein Push, kein hosted Run, kein Merge, keine PR-Close.

## Git identity (visible ansatz block)

- Card frontmatter owner (verbatim, fetched from origin/main at runtime): `(lane w385-0428-078-pr1650pre)` — owner value `w385-0428-078-pr1650pre`.
- Git user.name / user.email for this lane: `w385-0428-078-pr1650pre` / `w385-0428-078-pr1650pre@baseharbor.local`.
- Commit invocation template: `git -c user.name=w385-0428-078-pr1650pre -c user.email=w385-0428-078-pr1650pre@baseharbor.local commit ...`.
- Pre-push gate line: `git show -s --format=%an HEAD` must equal `w385-0428-078-pr1650pre` exactly.
- No commit was created in this lane (task is local hop + findings only, no push). The worktree HEAD at 37c4d847c is the pre-existing candidate commit authored by `w165-0428-078-pr1650-basehop` (the original #1650 lane), which is correct — this lane must not alter the candidate.

## Planning-repo remote attestation

- `git -C baseharbor-plan remote -v`: `origin  https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push). This is the planning repo. The `baseharbor` remote here points at `https://github.com/mcpdev80/baseharbor.git` (product repo, blobless).
- origin/main head at time of work: `06da93be2 0428-271 claimed by w386`.

## Base attestation (exact cut SHA)

- #1650 remote branch `lane-0428-078-perses-identity-on-resolver`: `37c4d847ca377d1555163ac4791c8ba08b85de77` (`git ls-remote baseharbor refs/heads/lane-0428-078-perses-identity-on-resolver`).
- This SHA is the HEAD of the created worktree; `git merge-base --is-ancestor 37c4d847... HEAD` confirms ancestor.
- develop base head: `ea5218d72e263f21e79853b679af50074dab8c25` (`git ls-remote baseharbor refs/heads/develop`).

## Own worktree

- `git worktree add workers/worktrees/w385-0428-078-pr1650pre 37c4d847ca377d1555163ac4791c8ba08b85de77`.
- Worktree is detached at 37c4d847c. No commit created; local develop-merge attempted and aborted clean (no conflict, no push).

---

## (a) PR witnesses — three PRs, same card content, same base (develop)

# gh pr view witnesses (mcpdev80/baseharbor):

- #1650: headRefName `lane-0428-078-perses-identity-on-resolver`, headRefOid `37c4d847ca377d1555163ac4791c8ba08b85de77`, base `develop`, state `OPEN`, mergeable `MERGEABLE`.
- #1818: headRefName `lane-0428-078-cf-fix`, headRefOid `20fc1cb7d49602dc7f8aa0004a7562a81311d78c`, base `develop`, state `OPEN`, mergeable `MERGEABLE`.
- #1855: headRefName `w279-0428-078-pr1650-reissue`, headRefOid `d18e4b367940ad5ee36862dbda1eea2d7a605db0`, base `develop`, state `OPEN`, mergeable `MERGEABLE`.

merge-base vs develop + develop-commits-ahead:

- #1650 37c4d847: merge-base `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`; develop commits ahead `4262` (raw count; its true candidate-specific product delta is only 4 files — see below).
- #1818 20fc1cb7: merge-base vs develop EMPTY (no shared ancestor with current develop). Raw develop-ahead `4232`.
- #1855 d18e4b36: merge-base `c167fa5dd323ae0746385caa2bdb8364ec7ad03f`; develop commits ahead `18`; own (not-on-develop) commits `18`.

---

## (c) Local develop-merge — #1650 candidate

Worktree at 37c4d847c. `git fetch --no-tags baseharbor develop` -> `ea5218d7...`.
`git merge --no-commit --no-ff baseharbor/develop`:

- Result: **clean**, auto-merged only `scripts/pr-gate-coverage.json`. No conflict. No file left unmerged.
- Aborted the in-progress merge (`git merge --abort`) so the candidate head is untouched. No push, no force, no commit.

---

## (d) Content overlap — which PRs carry the same content; superseded check

All three are `OPEN`, base `develop`, none is an ancestor of develop (none already merged → none superseded-by-merge):

- `git merge-base --is-ancestor <head> develop` for all three -> **false** for each. None is already in develop.

Content overlap (per-file diff md5 vs develop, common files):

- #1650 vs #1855: `cmd/baha/app_status_result.go` **IDENTICAL**, `cmd/baha/app_perses_cli_test.go` **IDENTICAL**, `contracts/...`, `docs/spec/...`, `internal/apierror/pagination.*`, `internal/application/*`, `internal/machine/*`, `internal/sourcetransfer/*`, `mkdocs*.yml`, `internal/machinehttp/source_transfer.go`, `internal/machinereadmodels/artifacts.go` — all IDENTICAL.
  - Only two files DIFFER between #1650 and #1855:
    - `internal/metrics/identity_dashboard_witness.go`: #1650 = 155 lines; #1855 = 491 lines (Keycloak attribution bound in).
    - `scripts/pr-gate-coverage.json`: #1855 removed the CI-script-only rows #1650 still lists.
- #1855 is a strict superset of #1650: every product file #1650 carries is byte-identical in #1855, plus #1855 adds `internal/identityprovider/keycloak_realization.go`, `internal/identityprovider/keycloak_signal_attribution_test.go`, `internal/metrics/identity_dashboard_witness_test.go`, `internal/metrics/perses_dashboards.go`, `internal/metrics/testdata/perses-dashboards/keycloak-identity.json`, `internal/runtime/project_names.go`.
- #1650's unique files (not in #1855) are ALL Owner-scope CI/script files: `.github/workflows/ci.yml`, `scripts/pr-check-runner.py`, `scripts/pr-gate-plan.py`, `scripts/test_pr_check_runner.py`, `scripts/test_pr_gate_coverage.py`. No product content.
- #1818 shares ancestry with #1650/#1855 only at the `0428-250` base commit `3ebfb90da` (its head has no common ancestor with current develop; it is a broad "hop onto develop" branch). Its `app_status_result.go` differs from #1650 by 226 lines (earlier pre-revision), its `app_perses_cli_test.go` by 22 lines. It carries the same Perses identity-dashboard core lineage but on a divergent history.

True candidate-specific product deltas (vs merge-base with develop):

- #1650: **4 files**, 244 insertions / 39 deletions — `cmd/baha/app_perses_cli_test.go`, `cmd/baha/app_status_result.go`, `internal/metrics/identity_dashboard_witness.go`, `scripts/pr-gate-coverage.json` (last one = trailing-newline only).
- #1855: 11 files, 1549 insertions / 40 deletions (superset incl. Keycloak).
- #1818: broad hop branch (68 files vs #1650), no clean single candidate delta.

Overlap conclusion: **three distinct candidate branches, same card #1650/#1818/#1855 content, same develop base; #1650 and #1855 carry byte-identical Perses identity-dashboard core with #1855 the strict superset (Keycloak); #1818 is a divergent hop branch of the same lineage.**

---

## (e) Trusted-plan coverage (scripts/pr-gate-coverage.json)

- `internal/metrics/identity_dashboard_witness.go` is already cataloged on develop at line **2659** (`scripts/pr-gate-coverage.json`):
  ```json
  {
    "id": "source.internal_metrics_identity_dashboard_witness_go",
    "path": "internal/metrics/identity_dashboard_witness.go",
    "surfaces": [
      "source.gate.atomic.docker.data.capabilities",
      "source.gate.atomic.podman.data.capabilities"
    ],
    "runtime_specific": true
  }
  ```
  This is a `data.capabilities` runtime-gate source entry. `#1650`'s coverage.json delta vs develop is a trailing-newline only — the entry already exists on develop; #1650 does **not** add a new stableid row.
- The Perses dashboards source entries (keycloak + non-keycloak) already exist on develop (lines 1759 `source.internal_metrics_perses_dashboards_keycloak_go`, 1741 `source.internal_metrics_perses_dashboards_go`).
- Stableids the Planner would close from these PRs: none new for #1650 (entry pre-exists). #1855's Keycloak attribution change reuses the same existing identity-dashboard stableid `source.internal_metrics_identity_dashboard_witness_go` (runtime_specific data.capabilities) — no new catalog row required. #1818 touches no new stableid source row beyond its broad scope.
- NOTE for the Coordinator (Owner-scope finding, not edited here): the data-capabilities native gate that this entry feeds is a shared planner/CI route under `.github/**` and shared check files. Per the gate rule, the minimal route must exist in this PR; if the identity-dashboard source is not currently reachable by a live check, that is the one shared-file case to report with file:line — no edit to `.github/**` or shared `scripts/ci-*.py` by this lane.

---

## Recommended qualification order

1. **#1855** (`w279-0428-078-pr1650-reissue` @ `d18e4b36`) first — superset of the Perses identity-dashboard core plus the Keycloak attribution (the full #0428-078 deliverable), 18 clean develop-mergeable commits.
2. **#1650** (`lane-0428-078-perses-identity-on-resolver` @ `37c4d847`) — earliest still-open single-lane reissue; its content is fully contained in #1855. Qualify the shared core once (via #1855) or close #1650 as superseded-after-#1855 per the two-distinct-run pair rule (close+reopen exact-head trigger). This lane does NOT close it — report to the Coordinator.
3. **#1818** (`lane-0428-078-cf-fix` @ `20fc1cb7`) — divergent hop branch (no develop ancestor, broad 68-file scope incl. AGENTS.md/scripts); same lineage but not a clean single candidate. Lowest priority; needs a coherence review before it qualifies as THE candidate.

---

## Cleanliness

- Worktree created at `workers/worktrees/w385-0428-078-pr1650pre`; no containers/compose started this lane; nothing to tear down.
- `git worktree list` will show the detached worktree at 37c4d847c; left for the Coordinator to remove on next tick (no push, no merge performed).

## END

`w385-0428-078-pr1650pre: END_DONE local hop clean (auto-merged scripts/pr-gate-coverage.json only), #1650/#1855 byte-identical Perses core with #1855 superset incl. Keycloak, #1818 divergent hop branch; no PR superseded (none in develop); recommended order #1855 → #1650 → #1818 — candidate SHA 37c4d847ca377d1555163ac4791c8ba08b85de77`
