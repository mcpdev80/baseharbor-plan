# 0428-082 Perses infrastructure dashboards — round-2 (handoff takeover)

Lane: flash takeover of the vanished session 267d1555's card (mission-082-perses-dashboards-r2-handoff).
Round-1 record: [round-1.md](round-1.md). This round is a takeover verification round; see the PLAN and decisions below.

## PLAN

- [PLAN-1] Reality witnesses: remote lane branch, PR #1665 state, old worktree — done
- [PLAN-2] Inventory the "uncommitted files" of mission point (c) — lost; reconstructed from local objects — done
- [PLAN-3] .gitignore decision — no product change needed — done
- [PLAN-4] perses_prometheus_alerts.* scope decision vs #1613/073 — done
- [PLAN-5] Dashboards completeness vs mission-082-original — done (candidate already complete)
- [PLAN-6] build / go vet / gofmt / tests — done
- [PLAN-7] Push decision (refspec + ls-remote before/after) — done (no push: remote unchanged)
- [PLAN-8] Exact-head CI run observation to terminal state — done
- [PLAN-9] Evidence commit + push to origin/main — this file
- [PLAN-10] Cleanup + END post

## Wrong-zone checkout attestation (mandatory)

Planning repo verified before first evidence commit:

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main
3523685f1ba48c7e119c9347e2c604604ea3b8c6	refs/heads/main
```

This is the real baseharbor-plan repo (`/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`), NOT the
quarantined `workers/baseharbor-plan` directory.

## Reality witnesses at start (measured via `git ls-remote` / `gh`)

- Remote truth (`git ls-remote origin`, run from a live baseharbor clone, refs freshly fetched):
  - `3a45995396ddbff9bd3cc9ccb59e77384b1145ef  refs/heads/lane-0428-082-perses-dashboards`
  - develop tip: `f590fbf0f1d103fce238b64d9f1b31c329a524ae`
  - There is NO remote `lane-0428-082-perses-dashboards-clean` branch (the `-clean` name exists only as the local hub checkout's checked-out branch — see hoof-regel note below).
- Point (a) verified: 3a4599539 is the feat commit stacked on the merge of the two approved content heads:
  - `fd82668f1` (selection, PR #1590) — `git merge-base --is-ancestor fd82668f1 3a4599539` => yes
  - `8b00fe2c8` (datasources, PR #1608) — `git merge-base --is-ancestor 8b00fe2c8 3a4599539` => yes
  - Log: `3a4599539 feat(0428-082)` / `76d9f0e12 merge(0428-082): Merge commit '8b00fe2c8'` / `fd82668f1 …` / `8b00fe2c8 docs(0428-083)` — correct stacking.
  - 3a4599539 is NOT an ancestor of origin/develop (PR still open) — correct.
- Point (b) verified: PR #1665 `base=develop, head=lane-0428-082-perses-dashboards, headRefOid=3a4599539…, isDraft=true, state=OPEN`.
- Point (c) — the old worktree is GONE (coordinator correction 2026-11-16): `baseharbor/worktrees/` is an empty
  directory, `git worktree list` shows no 082 entry. The uncommitted files (M .gitignore, M perses_infra_dashboards.go+test,
  A perses_prometheus_alerts.go+test) were never committed and are LOST with the deleted worktree. Loss noted per instruction.

## Reconstructed inventory of the lost working state (read-only forensics, nothing restored)

The lost dirty state is reconstructible from local git objects for inventory purposes ONLY (the coord correction says
not to reconstruct it as work product):

- Dangling commit `4f874f7ac1efdc70432c5ad2e7764a5cfb8e1848` (2026-11-16 21:23, parent `129a94a0`) is an earlier lineage of
  this card that contained `internal/metrics/perses_prometheus_alerts.{go,_test.go}` and an older dashboards.go/test.
- The alerts files in `4f874f7ac` are byte-identical (sha256 `c23a68cb…`) to the files already pushed on
  `w073-perses-alerts @ 470735c1d` = PR #1613 (0428-073). So the uncommitted `A` files were a duplicate of #1613's write-set.
- `.gitignore` diff in that lineage: added a line `worktrees/` (from `273695530 chore(0428-082): ignore worktrees zone`).
- The dashboards.go/test delta (4f874f7ac → 3a4599539) is doc-comment formatting and stronger fail-closed assertions
  (`res.Dashboard.ID != ""` checks) — the tip 3a4599539 is the STRICTER, final form.

## Decision (2) — .gitignore: REVERTED (nothing to revert)

The `worktrees/` ignore line belongs to operational bookkeeping, not the dashboards card; it is NOT committed on the
remote candidate (`.gitignore` at 3a4599539 has no such line, verified via `git show 3a4599539:.gitignore`). Not
required by the card. No action was needed — the remote tip is already clean of it. Per the workspace-layout rule,
scratch/ignore patterns stay out of the product repo.

## Decision (3) — perses_prometheus_alerts.*: EXCLUDED from this branch

The alerts surface belongs to the 0428-073 domain and ALREADY ships there as PR #1613
(`w073-perses-alerts @ 470735c1d`, files `internal/metrics/perses_prometheus_alerts.{go,_test.go}` — byte-identical to
the lost uncommitted copies). One PR per card: the dashboards card must not occupy the alerts surface. The remote
candidate 3a4599539 already excludes these files (verified: they exist in tree `4f874f7ac` but NOT in `3a4599539`;
`git ls-tree` witness above). No change needed; the exclusion stands. This is a pure dashboard-realization file set:
`perses_infra_dashboards.go`, its test, and `testdata/perses-infra-dashboard/prometheus-targets.json`.

## Decision (4) — dashboards completeness vs mission-082-original

Checked the committed candidate at 3a4599539 against every acceptance point:

- Verified metrics only: `BuildPersesInfraDashboard[WithProbe]` builds solely on `BuildPersesPrometheusDatasource`
  (lane-083, read-only consumption); `MissingSignal` derives from the datasource `Reachability`, never a
  caller-supplied boolean (perses_infra_dashboards.go:250,286).
- Explicit missing-signal: verified datasource + down probe → dashboard object with `MissingSignal=true` (visible gap,
  no silent 0, no invented path); unverified/unselected/unpinned → `*PersesInfraDashboardError`, no dashboard at all.
- Positive regression: `TestPersesInfraDashboardPositiveFilledSignal` (up=1 → filled, MissingSignal=false, 4 panels).
- Negative regressions: `TestPersesInfraDashboardNegativeMissingSignal` plus three fail-closed tests
  (unpinned / unselected / no provider), which at the tip are stronger than round-1 (they also assert the fail-closed
  result carries no dashboard id).
- Golden witness: `TestPersesInfraDashboardJSONGolden` vs committed `testdata/perses-infra-dashboard/prometheus-targets.json`.
- No 080 weakening: 080's non-forgeability work (fd82668f1) is an ancestor and untouched; the candidate never references
  or modifies the identity witness; `TestPersesInfraDashboardNoCapabilityClaim` pins the no-capability-claim boundary.
- Catalog seam: the dashboard id `prometheus-targets` is exactly the `internal/capability/perses_selection.go`
  catalog key for `DashboardBackendPrometheus` (perses_selection.go:196-201). The dashboard document format is the
  repo-native struct-first format, consistent with the datasource (083) precedent.

Verdict: the remote candidate is COMPLETE. The lost dirty work added no required behavior (alerts = other card,
gitignore = operational, dashboards delta = already present in stricter form). This round therefore makes NO product
change; the exact candidate remains `3a45995396ddbff9bd3cc9ccb59e77384b1145ef`.

## Local checks (my own runs, at 3a4599539)

- Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/.w082-r2-wt` (detached at 3a4599539, created by me under
  the workers zone per the flash-lane precedent; the hub checkout `baseharbor/` on
  branch `lane-0428-082-perses-dashboards-clean` was NOT touched for any product work — hoof rule respected).
- `go build ./internal/metrics/... ./internal/capability/...` — pass (full `go build ./...` blocked first by a
  host `/tmp` quota exhaustion from another lane's caches; reran with TMPDIR in my own zone).
- `go vet ./internal/metrics/ ./internal/capability/` — clean.
- `gofmt -l internal/metrics/ internal/capability/` — no output (clean).
- `go test ./internal/metrics/ -run PersesInfra -v` — 7/7 PASS.
- `go test ./internal/metrics/ ./internal/capability/` — both ok (full package suites).

## CI (Eigenes-run-pflicht)

I did NOT trigger any new hosted run: this round changed no inputs (no commit, no push; PR stays draft; `.github/**`
untouched; no workflow_dispatch — Owner scope + mission limits). Per the CI-reuse rule (5.4) the existing same-SHA
result is authoritative:

- Run `43951946780` (CI · PR #1665 · Source & Quality), headSha `3a4599539…`, status `completed`, conclusion `success`.
- Job-level witness: `PR · Draft Go · cli-0/1/2/3`, `PR · Draft Go · packages`, `PR · Draft source and routing` all
  `completed/success`; heavyweight PR/runtime jobs `skipped` by draft design.
- The new infra-dashboard tests are captured by the `PR · Draft Go · packages` job
  (`go test ./contracts/... ./internal/... ./spec/...`) on every draft-PR push — no `.github/**` change needed
  (CI-Aufnahmepflicht satisfied by the existing group).

## Push / PR state witnesses

No push this round (no new commits on top of 3a4599539). Remote-state verification:

```
$ git ls-remote origin refs/heads/lane-0428-082-perses-dashboards
3a45995396ddbff9bd3cc9ccb59e77384b1145ef	refs/heads/lane-0428-082-perses-dashboards
$ gh pr view 1665 --json isDraft,state,headRefOid
isDraft=true  state=OPEN  headRefOid=3a45995396ddbff9bd3cc9ccb59e77384b1145ef
```

Exactly one candidate on this chain (AGENTS 3.8): `lane-0428-082-perses-dashboards` @ 3a4599539, PR #1665 stays DRAFT.

## repo-rule compliance

- Product repo: zero writes this round; no `.github/**` edits; no merge, no ready_for_review, no force-push, no subagent (§4.8).
- Evidence lives only in baseharbor-plan (`evidence/r28-welle3-2026-11-16/perses-dashboards/`); no `.evidence/` dir in any product repo.
- Reality witnesses only via `git ls-remote` / `gh` / local git objects; the quarantined `workers/baseharbor` checkout was used
  only as a fetch-enabled clone to reach the same remote (its refs are never cited as remote truth).
- Lost-work disclosure: the uncommitted working state of the vanished session is unrecoverable and documented above; it
  contained no required card behavior.
- No docker/podman/compose project was started this round (nothing to tear down; ps-witness: not applicable).

## Loss note (per coord correction)

The old worktree `baseharbor/worktrees/lane-0428-082-perses-dashboards` no longer exists (owner removal of the vanished
session swept it, second such incident). Its uncommitted files are LOST and were NOT reconstructed as work product;
they were only inventoried read-only from local git objects to answer mission point (c), and every element of them was
shown to be either duplicated on the correct card (#1613), operational-only (.gitignore), or already present in
stricter committed form at 3a4599539.

## END

END_DONE mission-082-perses-dashboards-r2-handoff.md: takeover verified — candidate 3a45995396ddbff9bd3cc9ccb59e77384b1145ef (PR #1665 draft, run 43951946780 success), lost dirty state inventoried and excluded, no product change required.
