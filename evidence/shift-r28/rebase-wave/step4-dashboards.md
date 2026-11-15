# Akte — rebase-welle r28 SCHRITT 4: four dashboard followers <- new Perses selection-head

**Mission:** mission-rebase-step4.md
**Shift/evidence root:** `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/shift-r28/mission-rebase-step4.md`
**Product repo:** `mcpdev80/baseharbor` (https://github.com/mcpdev80/baseharbor)
**Working zone (own persistent shallow clone):** `/tmp/opencode/step4-wt`
**Planning repo (evidence source of truth):** `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY (NOT `workers/baseharbor-plan`)
**Base ref cut from:** current remote selection head `8ce0df9148e4f388ba18386e3b731f1fc2cbd500` (verified via ls-remote before first push)

## 1. Protocol (from mission)

- working-branch from the old head, plain MERGE of the selection head (NO rebase/force)
- conflicts handled minimally, bidirectionally preserving both sides, file-by-file
- per branch: `go build` + targeted perses/metrics tests, verbatim
- normal merge-commit-push (PR heads follow; drafts stay drafts)
- deliver akte + END with all four NEW head SHAs
- No `.github/**` edits, no reruns/workflow_dispatch, no force-push, no develop-merge, no ready_for_review, no feature additions, no subagents (§4.8).

## 2. Remote-state verification BEFORE merge (ls-remote, fresh)

All five SHAs matched the mission exactly:

- Selection target `lane-0428-080-r28-perses-selection` = `8ce0df9148e4f388ba18386e3b731f1fc2cbd500`
- (A) `perses-dashboard-databases-lane` (#1597) = `7f3a25a0b454adec9fba3beb5b0e3d0e2ba6b89f`
- (B) `lane-0428-077-r28-perses-dashboard-hosts` (#1602) = `ca8181c0eccbaa5a9541307171b0e64a302e30a0`
- (C) `lane-0428-079-r28-perses-messaging` (#1603, headRefName via `gh pr view 1603`) = `c385abe4e451ff50df997c86d7420dcb2c4bb1aa`
- (D) `wt-0428-081` (#1604 valkey, headRefName via `gh pr view 1604`) = `8221f51b60415ecf7d28adc9bd56debf798023f8`

Selection head is a merge-commit `8ce0df9` = merge(`a270725` + seam head `492b8e8f`). The selection only ever adds three files vs `a270725`:
`internal/capability/perses.go`, `internal/capability/perses_test.go`, `internal/metrics/perses_contract_test.go`.

## 3. Merge-base / disjoint analysis (each follower)

| Branch | merge-base | selection adds | lane adds (vs merge-base) | overlap? |
| --- | --- | --- | --- | --- |
| (A) databases | `a270725` | 3 perses files | 10 (dashboards*, status_result*, cli_test*, testdata) | none — clean |
| (B) hosts | `85b4cbb` | 3 perses files | 10 (hosts* dashboards, status_result*, cli_test*, testdata) | none — clean |
| (C) messaging | `0e9ccb5` (older) | 3 perses files (+ accumulated selection) | 3 (messaging*, testdata) | none — clean |
| (D) valkey | `a270725` | 3 perses files | 3 (valkey*, testdata) | none — clean |

Pre-check with `git merge-tree --write-tree` returned exit 0 (no conflict markers) for all four.

## 4. Per-branch results (before → after, ls-remote)

### (A) perses-dashboard-databases-lane (#1597)
- before: `7f3a25a0b454adec9fba3beb5b0e3d0e2ba6b89f`
- after: `6699325d763dc42b2ee1c2cdd923e13e8bf553fe`
- merge commit `6699325d` parents: `7f3a25a0` (old) + `8ce0df91` (selection)
- selection `8ce0df91` confirmed ancestor of new head. Working tree clean after merge.

### (B) lane-0428-077-r28-perses-dashboard-hosts (#1602)
- before: `ca8181c0eccbaa5a9541307171b0e64a302e30a0`
- after: `3634321d7ebc5227c1d3086009ee1fb610b88885`
- merge commit `3634321d` parents: `ca8181c0` (old) + `8ce0df91` (selection)
- both old head and selection confirmed ancestors. Working tree clean.

### (C) lane-0428-079-r28-perses-messaging (#1603)
- before: `c385abe4e451ff50df997c86d7420dcb2c4bb1aa`
- after: `62c35c9a4505fd195a2b500530dc338150698c9a`
- merge commit `62c35c9a` parents: `c385abe4` (old) + `8ce0df91` (selection)
- both confirmed ancestors. Working tree clean.

### (D) wt-0428-081 (#1604, valkey)
- before: `8221f51b60415ecf7d28adc9bd56debf798023f8`
- after: `d681e181079152e4577328b22ae39c98a0b67253`
- merge commit `d681e181` parents: `8221f51b` (old) + `8ce0df91` (selection)
- both confirmed ancestors. Working tree clean.

## 5. Builds + tests (verbatim)

Run from `/tmp/opencode/step4-wt` on each branch's merge commit. No conflicts occurred, so no bidirectional conflict resolution was needed.

(A) databases:
- `go build ./...` → exit 0
- `go test ./internal/capability/ -run Perses` → ok
- `go test ./internal/metrics/ -run 'Perses'` → ok (11 PASS incl. TestPersesDashboardGoldenFiles, TestPersesDashboardKeysMatchSelectionCatalogKeys)
- `go test ./cmd/baha/ -run 'Perses'` → ok (9 PASS incl. TestBahaStatusPersesSurfaceFailsClosedAndUnverified, TestPersesReleaseFailClosedOnUnknownAuthClass)

(B) hosts:
- `go build ./...` → exit 0
- `go test ./internal/capability/ -run Perses` → ok
- `go test ./internal/metrics/ -run 'Perses'` → ok (0.005s)
- `go test ./cmd/baha/ -run 'Perses'` → ok (8.835s)

(C) messaging:
- `go build ./...` → exit 0
- `go test ./internal/capability/ -run Perses` → ok
- `go test ./internal/metrics/ -run 'Perses'` → ok (0.005s)
- `go test ./cmd/baha/ -run 'Perses'` → ok (8.534s)

(D) valkey:
- `go build ./...` → exit 0
- `go test ./internal/capability/ -run Perses` → ok
- `go test ./internal/metrics/ -run 'Perses'` → ok (0.004s)
- `go test ./cmd/baha/ -run 'Perses'` → ok (7.720s)

## 6. PR state after push (verified via `gh pr view`)

All four PRs remain OPEN and DRAFT (not promoted):
- #1597 `perses-dashboard-databases-lane` draft=true state=OPEN
- #1602 `lane-0428-077-r28-perses-dashboard-hosts` draft=true state=OPEN
- #1603 `lane-0428-079-r28-perses-messaging` draft=true state=OPEN
- #1604 `wt-0428-081` draft=true state=OPEN

## 7. Scope / repo-rule compliance

- No subagent invoked (§4.8): every merge, build, test and push ran in this session.
- No `.github/**` file touched; no rerun / workflow_dispatch.
- No force-push; normal merge commits only.
- No develop-merge; no ready_for_review; no feature additions.
- One integration candidate per chain: only the four named follower branches worked.
- Reality witnesses via `git ls-remote` and the fresh shallow clone in `/tmp/opencode/step4-wt` only. The quarantined `workers/baseharbor` checkout was never cited.
- Evidence files live only in baseharbor-plan; nothing committed to a product repo.
- Working tree stayed under `/tmp/opencode/step4-wt` (fixed workspace layout).

## 8. Cleanliness

- No docker/podman containers or compose projects were started in this lane (pure git + go build/test). Nothing to bring down.
- Local working branches retained in `/tmp/opencode/step4-wt`: `perses-db-working`, `hosts-working`, `messaging-working`, `valkey-working`. These are local-only and do not affect any daemon.
- No stray files created in `/home/marcel/dev/baseharbor-ecosystem` itself.

## 9. SHAs (before → after, ls-remote)

| # | branch | before | after |
| --- | --- | --- | --- |
| A | perses-dashboard-databases-lane | `7f3a25a0b454adec9fba3beb5b0e3d0e2ba6b89f` | `6699325d763dc42b2ee1c2cdd923e13e8bf553fe` |
| B | lane-0428-077-r28-perses-dashboard-hosts | `ca8181c0eccbaa5a9541307171b0e64a302e30a0` | `3634321d7ebc5227c1d3086009ee1fb610b88885` |
| C | lane-0428-079-r28-perses-messaging | `c385abe4e451ff50df997c86d7420dcb2c4bb1aa` | `62c35c9a4505fd195a2b500530dc338150698c9a` |
| D | wt-0428-081 | `8221f51b60415ecf7d28adc9bd56debf798023f8` | `d681e181079152e4577328b22ae39c98a0b67253` |

Selection target unchanged: `lane-0428-080-r28-perses-selection` = `8ce0df9148e4f388ba18386e3b731f1fc2cbd500`.

## Evidence on origin/main (required before END)

`git ls-remote origin HEAD` (planning repo mcpdev80/baseharbor-plan):
```
55d20758fe96823216169dc73d8d3279c66bc019	refs/heads/main
```
Commit `55d20758` = "evidence r28 step4: four dashboard followers merged with Perses selection head".
Evidence path present on origin/main: `evidence/shift-r28/rebase-wave/step4-dashboards.md`.

## END

STATUS: DONE
All four dashboard follower branches merged with the new Perses selection head via clean plain merges (no conflicts, no rebase/force). Each: build passes, perses/metrics/cmd perses tests pass, both parents present (old head + selection `8ce0df91`), PRs remain OPEN/draft. Four new head SHAs above.
