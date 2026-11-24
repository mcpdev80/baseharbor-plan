# #1818 clean-candidate reconciliation (read-only desk, round-1)

Shift: r28-welle6-2026-11-25 | Card: 0428-078 | Branch: `lane-0428-078-cf-fix`
Mission: `coordinator/missions/w88-0428-078-1818reconcile.txt`
Nature: Befund only. No branch writes / push / merge / subagents (§4.8). #1812/#1819/#1820/#1650/#1826 untouched.

## PLAN

- Establish remote reality via `git ls-remote` (only valid witness), fresh clone under /tmp/opencode.
- Verify reachability of BOTH candidate SHAs against branch tip `20fc1cb7`.
- Determine which candidate is newer / closer to develop and is the true parent lineage of the intended 19-file diff.
- `git diff --name-only origin/develop <sha>` per candidate: clean head must equal the #1818 write-set with ZERO `keycloak-identity` catalog() rows; the contaminated tip adds the forbidden row.
- Decide + justify the single canonical clean head; confirm `20fc1cb7` is VOID.
- Restate the C/#1819 retarget test dependency.

## Base attestation

- develop (current origin/develop) tip:
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2`
- branch tip (lane-0428-078-cf-fix):
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-078-cf-fix` -> `20fc1cb7d49602dc7f8aa0004a7562a81311d78c`
- Worktree: `/tmp/opencode/w88-0428-078-1818reconcile-wt`, remote `origin` = `https://github.com/mcpdev80/baseharbor.git` (github.com/mcpdev80 confirmed). No writes made.
- The w75 candidate `0f20a3b97fa33a0c3ff1476ef32866b4fe008f5f` does NOT exist on the remote (git cat-file rev-parse unknown) — it was a phantom from the earlier desk that ran off the quarantined stale checkout. Only `8e2c50c1...` is real.

## Remote reality (ls-remote witnesses)

- `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2	refs/heads/develop`
- `20fc1cb7d49602dc7f8aa0004a7562a81311d78c	refs/heads/lane-0428-078-cf-fix`

## Analysis

### 1. Reachability against branch tip `20fc1cb7`

- `8e2c50c10a537c00e30d62a47f29638a0f14d5ff`:
  `git merge-base --is-ancestor 8e2c50c1... 20fc1cb7...` -> **YES, is an ancestor** of branch tip.
  Branch ancestry (branch tip -> ...): `20fc1cb7` -> `8e2c50c1` -> `888e2193` -> ... So the branch descends:
  `8e2c50c1` -> `888e2193` (hop #1650) -> `20fc1cb7` (contaminated tip).
- `0f20a3b9...`: **does not exist on the remote** (rev-parse unknown). Not reachable, not real.

### 2. Which is newer / closer to develop

- `8e2c50c1` sits 3 commits ahead of origin/develop (`46d3dccc`), and the branch descends directly from it.
- `20fc1cb7` sits exactly 1 commit above `8e2c50c1`. So `20fc1cb7` is newer than `8e2c50c1` but is the contaminated tip, not the clean candidate.
- `0f20a3b9` is a phantom (no remote object).

### 3. Write-set / forbidden keycloak-identity catalog row

`git diff --name-only 46d3dccc... 8e2c50c1...` (the intended #1818 19-file write-set):

- `.github/workflows/pre-release.yml`
- `cmd/baha/app_status_result.go`
- `cmd/baha/env_destroy_integration_test.go`
- `internal/deployment/environment_destroy_scope.go`
- `internal/deployment/environment_destroy_scope_test.go`
- `internal/identityprovider/keycloak_files.go`
- `internal/identityprovider/keycloak_realization.go`
- `internal/metrics/perses_dashboards_keycloak.go`  <- NEW file, holds keycloak identity logic
- `internal/metrics/perses_dashboards_test.go`
- `internal/metrics/realization.go`
- `internal/metrics/testdata/perses-dashboards/keycloak-identity.json`
- `internal/operatorauth/authorization.go`
- `internal/operatorauth/config.go`
- `scripts/pr-gate-coverage.json`

Clean check for `8e2c50c1`:
- `git show 8e2c50c1:internal/metrics/perses_dashboards.go | grep -niE keycloak` -> **empty**. The `persesDashboardCatalog()` body at `8e2c50c1` contains ZERO `keycloak-identity` catalog keys and ZERO `ProviderKeycloak` cases. All keycloak identity logic lives in the new file `perses_dashboards_keycloak.go` (70 insertions), NOT as a catalog() row.
- `git diff 46d3dccc... 8e2c50c1... -- scripts/pr-gate-coverage.json | grep -iE keycloak-identity|catalog` -> **no keycloak-identity catalog row**.

Contamination check for `20fc1cb7`:
- `git show 20fc1cb7:internal/metrics/perses_dashboards.go | grep -nE "keycloak-identity|DashboardBackendIdentity"` -> **5 hits**, the forbidden row:
  ```
  +		"keycloak-identity": {
  +			Key:            "keycloak-identity",
  ...
  +			Dashboard:      persesDashboardForBackend(resolved, "keycloak-identity"),
  +	case "keycloak-identity":
  +		return capability.ProviderKeycloak
  ...
  +			Metadata: PersesDashboardMetadata{Name: "keycloak-identity", Version: 0},
  ```
- The row was introduced solely by commit `20fc1cb7 fix(0428-078): wire keycloak identity dashboard into develop metrics catalog` (the w53 cross-session force-push).

## Verdict table

| SHA | reachable-from-branch `20fc1cb7`? | diff==#1818 write-set? | has keycloak-identity catalog() row? | verdict |
| --- | --- | --- | --- | --- |
| `8e2c50c10a537c00e30d62a47f29638a0f14d5ff` | YES (ancestor, branch descends from it) | YES (19-file write-set, no scripts/pr-gate-coverage keycloak row) | NO (0 literals in perses_dashboards.go; logic in new perses_dashboards_keycloak.go) | **Canonical clean candidate** |
| `0f20a3b97fa33a0c3ff1476ef32866b4fe008f5f` | NO (phantom; no object on remote) | N/A | N/A | Rejected — not a real remote object (w75 phantom) |
| `20fc1cb7d49602dc7f8aa0004a7562a81311d78c` (branch tip) | n/a (it IS the tip) | NO — tip = clean write-set + forbidden row | YES — 5 keycloak-identity literals in perses_dashboards.go catalog() | VOID (contaminated tip, w53 force-push) |

## Recommended reset target

Force-push `lane-0428-078-cf-fix` to **`8e2c50c10a537c00e30d62a47f29638a0f14d5ff`** (clean). This strips the forbidden `keycloak-identity` catalog row introduced by `20fc1cb7`, leaving the exact intended 19-file #1818 write-set with all keycloak identity logic in `perses_dashboards_keycloak.go` and ZERO catalog() rows.

## C / #1819 retarget test dependency (restated)

The acceptance test `TestPersesKeycloakDashboardQueriesSelectRealProviderLabels` (named at `cmd/baha/perses_dashboards_test.go:766` in the #1819 task) and its seam `persesDashboardProvisionForLifecycle` **do not yet exist** on the current branch — they are #1819's producer code. Therefore #1818's final clean form must be **re-targeted against #1819's `persesDashboardProvisionForLifecycle` seam** after #1819 merges: the clean `8e2c50c1` baseline must absorb #1819's `TestPersesKeycloakDashboardQueriesSelectRealProviderLabels` gate, which keys the Keycloak identity dashboard on the provider-class job + provider label (the same contract the forbidden `20fc1cb7` row tried to hard-code directly into `persesDashboardCatalog()`). Reset + retarget order: #1819 merge (producer) -> reset lane-0428-078-cf-fix to `8e2c50c1` -> rebase onto post-#1819 develop -> absorb the C test -> re-verify ZERO catalog rows.

## Cleanliness

- No product files touched. No card/branch/state changed.
- Worktree `/tmp/opencode/w88-0428-078-1818reconcile-wt` is read-only for this desk; left as-is for the coordinator's later force-push (not deleted, since the reset is a later owner-authorized action).

## Evidence

- Evidence file (this doc), committed to baseharbor-plan origin/main.
- ls-remote witnesses above.
