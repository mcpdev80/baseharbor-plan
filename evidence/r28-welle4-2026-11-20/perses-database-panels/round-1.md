# 0428-076 Perses database dashboards — round-1 (w202-0428-076-dbpanels)

Lane: w202-0428-076-dbpanels · Card: 0428-076 · PR: baseharbor#1597 · Model: Ornith (worker-ornith1.5) · Date: 2026-11-20

## PLAN

1. Read mission + task contract, attest remote reality.
2. Investigate PR #1597 diff vs develop for scope.
3. Confirm card 0428-076 own work isolation.
4. Measure current develop for PG/Mongo metrics contract.
5. Scope-contamination decision with Owner (QUESTION).
6. Rebase lane onto fresh develop; make PR non-draft.
7. Fix failing 'validate' cell or record as STATE.
8. Smallest matching local tests + CI gate wiring.
9. One hosted run on exact head (self-run, 4.6).
10. Publish evidence to baseharbor-plan main; END.

## Remote reality witnesses (measured via git ls-remote, fresh)

- develop head (origin github): `40cb28c758b02960356434b630086a341ebe1738`
  `git -C baseharbor ls-remote lane-origin refs/heads/develop`
- PR #1597 head: `540ed13cec363a231241a17baa68c8d32ebdae63`
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1597/head`
- PR #1597: state OPEN, isDraft TRUE, title "0428-076 Perses database dashboards (prometheus/loki/tempo + explicit PG/Mongo unavailable)", base develop, head branch refs/heads/perses-dashboard-databases-lane.
- `git merge-base --is-ancestor 40cb28c758b02960356434b630086a341ebe1738 540ed13cec363a231241a17baa68c8d32ebdae63` = NEIN (stale base).
- baseharbor-plan remote: `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`

## Acceptance field (from card task note, in order)

1. Rebase the lane branch onto develop 40cb28c758b0, force-with-lease onto own lane branch; no force-push to develop/main, no merge, no second PR.
2. PR to draft=false via `gh api -X PATCH repos/mcpdev80/baseharbor/pulls/1597 -f draft=false`; title/body with card number + head SHA + evidence path.
3. Fix the failing 'validate' cell; read its own literal error line before editing. If it hangs only on a field gate (e.g. "Managed-environment machine operations require an authenticated BaseHarbor operator"): run-id + literal line into the evidence, 'GATE-FAIL 0428-198' to coordinator, and the own evidence comes from the smallest matching gate.
4. The product question: PostgreSQL/MongoDB panels appear ONLY when metrics AND permissions verified present on current develop; unsupported DBs stay explicitly unavailable.
5. Regression: one case per case via the real command surface.
6. One hosted run on the exact new head, self-monitored to terminal state.

## Scope decision, coordinator, reverse drift explained

- PR #1597 head 540ed13cec36 sits on 23 commits over develop, but the diff against develop `40cb28c758b0` is **419 files**. This is far beyond card 0428-076's write-set.
- Card 0428-076's own authored work is cleanly isolated in exactly 3 commits:
  - `2e5f8703` welle2-076 worker feat(0428-076): Perses database dashboards (10 files: app_perses_cli_test.go, app_status_result.go, perses_dashboards.go, perses_dashboards_helpers.go, perses_dashboards_test.go, 5 golden json)
  - `7c4db737` w091-0428-091 fix(0428-076): emit valid PromQL selectors
  - `540ed13c` lv4-verify fix(metrics): emit closed PromQL selectors (the current head)
- The remaining ~20 commits carry unrelated card work: keycloak HA/database reload, podman quadlet, openbao bootstrap auth, workspace wizard, mcp lifecycle, valkey HA, r27 pre-release pinning, docs (cli/targets/mcp/observability), contracts, evidence-r27/ artifacts, and the .github workflow edits. Several of these are in files the mission marks EXPRESS VER SCHLOSSEN (e.g. internal/machine/**, internal/serviceaccess/policy.go, cmd/baha/app_context.go, .github/**).

## Current-develop product measurement (card 4)

- On develop `40cb28c758b0` (measured, not trusted from cd77e20e):
  - `internal/capability/reference.go`: PostgreSQL metrics = `ObservabilityRequiresAdapter` (mode ObservabilityAdapter), MongoDB metrics = `ObservabilityUnsupported`. Both have no native metrics signal.
  - `internal/metrics/perses_dashboards.go` already emits postgresql-targets and mongodb-targets as `Unavailable` with a reason naming the missing signal, and ships Prometheus/Loki/Tempo panels only.
  - Conclusion: the existing 076 implementation is already correct for current develop. Panels must NOT appear for PG/Mongo (no verified metrics/permissions). No product code change is required by the card on the current develop HEAD.

## Failing 'validate' cell (card 3)

- Check runs on 540ed13cec36: 7 success / 1 failure / 48 skipped. Failing cell name = `validate`.
- Failing job step 15 = "Run runtime integration tests serially" (`ci.yml:353`), exit 1. It runs `go test -p 1 ./cmd/baha ./internal/application -run '^(TestRepositoryWorkflowRealLifecycle|...TestMultiInstanceComposeLifecycleInCI)$'` with `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`.
- These are native runtime integration tests requiring an isolated, verified rootless runtime (Docker/Podman). Per mission and AGENTS 3.8/5.4 these are field-gate cases (0428-198/0428-202), NOT a diff fix, and require an expensive isolated runtime. Cannot be run on the coordinator/codeman host. This must be recorded as STATE (check `validate`, failing step "Run runtime integration tests serially", exit 1) and routed to the coordinator, not patched by hand.

## Scope decision requested (QUESTION to Owner)

- PR #1597 head 540ed13cec36 is a STACKED chain: lane `perses-dashboard-databases-lane` = 075(seam) + 080(selection) + 076(dashboards). My card 0428-076 is the TOP, so its diff over develop legitimately includes 075/080 Perses work (that is expected for a stacked lane).
- BUT the lane also absorbed ~15 non-Perses r27 pre-release commits (keycloak database reload, podman quadlet, openbao bootstrap auth, workspace wizard, mcp lifecycle, valkey HA, deployment local-owner, coreinstallation locks, telemetry otlp, traces credential rotation, scripts/pr-gate-*, etc.) — OUTSIDE card 0428-076's write-set and outside the Perses chain. This is the contamination.
- Card 0428-076's OWN write-set (isolated in commits 2e5f8703, 7c4db737, 540ed13c) is exactly 6 Go files + 5 testdata json:
  - cmd/baha/app_perses_cli_test.go (added DatabaseDashboards face + TestBahaStatusDatabaseDashboardsExposesUnavailableDatabases)
  - cmd/baha/app_status_result.go (added DatabaseDashboards field + wiring)
  - internal/metrics/perses_dashboards.go (catalog: prometheus/loki/tempo panels + PG/Mongo unavailable)
  - internal/metrics/perses_dashboards_helpers.go
  - internal/metrics/perses_dashboards_promql_test.go
  - internal/metrics/perses_dashboards_test.go
  - internal/metrics/testdata/perses-dashboards/{loki-logs,mongodb-targets,postgresql-targets,prometheus-targets,tempo-traces}.json
- The scope decision (requested via QUESTION): does the Owner want PR #1597 kept as the full stacked chain (075+080+076 + carried r27, as-is) or trimmed to only 076's 6 files? Dropping other lanes' carried work from a shared PR branch would harm those lanes; a clean rebase that keeps only my 6 files would drop 075/080 that the lane depends on. This is an Owner call.

## Scope decision requested (QUESTION to Owner)

- PR #1597 head 540ed13cec36 is a STACKED chain: lane `perses-dashboard-databases-lane` = 075(seam) + 080(selection) + 076(dashboards). My card 0428-076 is the TOP, so its diff over develop legitimately includes 075/080 Perses work (that is expected for a stacked lane).
- BUT the lane also absorbed ~15 non-Perses r27 pre-release commits (keycloak database reload, podman quadlet, openbao bootstrap auth, workspace wizard, mcp lifecycle, valkey HA, deployment local-owner, coreinstallation locks, telemetry otlp, traces credential rotation, scripts/pr-gate-*, etc.) — OUTSIDE card 0428-076's write-set and outside the Perses chain. This is the contamination.
- Card 0428-076's OWN write-set (isolated in commits 2e5f8703, 7c4db737, 540ed13c) is exactly 6 Go files + 5 testdata json:
  - cmd/baha/app_perses_cli_test.go (added DatabaseDashboards face + TestBahaStatusDatabaseDashboardsExposesUnavailableDatabases)
  - cmd/baha/app_status_result.go (added DatabaseDashboards field + wiring)
  - internal/metrics/perses_dashboards.go (catalog: prometheus/loki/tempo panels + PG/Mongo unavailable)
  - internal/metrics/perses_dashboards_helpers.go
  - internal/metrics/perses_dashboards_promql_test.go
  - internal/metrics/perses_dashboards_test.go
  - internal/metrics/testdata/perses-dashboards/{loki-logs,mongodb-targets,postgresql-targets,prometheus-targets,tempo-traces}.json
- The scope decision (requested via QUESTION): does the Owner want PR #1597 kept as the full stacked chain (075+080+076 + carried r27, as-is) or trimmed to only 076's 6 files? Dropping other lanes' carried work from a shared PR branch would harm those lanes; a clean rebase that keeps only my 6 files would drop 075/080 that the lane depends on. This is an Owner call.

## Scope decision requested (QUESTION to Owner)

The lane branch `perses-dashboard-databases-lane` is contaminated with ~20 other cards' commits (419-file diff). Cleaning it to a card-076-only candidate while keeping the same PR #1597 would either (a) drop other lanes' carried work from that PR branch or (b) require touching files outside card 0428-076's write-set. This is an Owner scope decision. Options being requested in the QUESTION are listed there.

---

# 0428-076 Perses database dashboards — round-2 (w204-0428-076-hop, mechanical)

Lane: w204-0428-076-hop · Card: 0428-076 · PR: baseharbor#1597 · Model: Ornith (worker-ornith1.5) · Date: 2026-11-20

## PLAN

1. Measure develop `40cb28c758b0`; cut a fresh worktree from exactly this commit.
2. Cherry-pick `2e5f87037 7c4db737f 540ed13ce` in order; go.mod/go.sum keep develop baseline unless a real import demands it.
3. Measure `git diff --name-only 40cb28c758b0 HEAD`; expect ~8-11 files all in the 076 scope; STOP + report if any other path appears.
4. gofmt -l ., go vet ./internal/metrics/... ./cmd/baha/..., focused perses tests; record results literally.
5. Verify the product question on the cherry-picked state: PG/Mongo panels only when verified metrics/permissions; unsupported DBs stay unavailable; no additional commit unless violated.
6. force-with-lease push to lane branch only; prove PR #1597 delivery via ls-remote.
7. Undraft PR #1597 via the correct endpoint (PATCH draft:false is ignored by GitHub); verify isDraft=false.
8. Watch the hosted run at the exact new head to terminal state (self-run, 4.6); record run-id + conclusion per cell.

## Base attestation

- develop (origin github) cut-from SHA: `40cb28c758b02960356434b630086a341ebe1738`
  `git ls-remote lane-origin refs/heads/develop` = `40cb28c758b02960356434b630086a341ebe1738	refs/heads/develop`
- `git merge-base --is-ancestor 40cb28c758b02960356434b630086a341ebe1738 HEAD` = JA (ancestor confirmed).
- `git log --oneline origin/develop..HEAD` lists ONLY own commits (4):
  - `90063f6e` fix(0428-076): reconcile perses catalogs with develop selection drift
  - `3706b95d` fix(metrics): emit closed PromQL selectors, validate with real Prometheus parser
  - `170672ca` fix(0428-076): emit valid PromQL selectors in Perses database dashboards
  - `f21995f6` feat(0428-076): Perses database dashboards — prometheus/loki/tempo panels + explicit PG/Mongo unavailable
- baseharbor-plan remote: `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`

## Step 1 — fresh worktree from develop 40cb28c758b0

- Fresh worktree at /tmp/opencode/lane-0428-076-hop, branch hop-076-wt, from origin/develop = 40cb28c758b0.
- `git diff --name-only 40cb28c758b0 HEAD` at baseline = empty (fresh develop).

## Step 2 — cherry-pick 2e5f87037 7c4db737f 540ed13ce

- `git cherry-pick 2e5f87037 7c4db737f 540ed13ce` applied; one conflict in cmd/baha/app_status_result.go (HEAD has `HostContainersDashboards`, feature commit has `DatabaseDashboards`).
- Conflict resolution: the feature commit 2e5f87037's final tree (PR #1597 head 540ed13cec36) carries only `DatabaseDashboards`; PR #1597 never had the host-container dashboards (cut before develop's host-dashboards work). Resolved to the feature's own final tree (DatabaseDashboards, no host field).

## Step 3 — diff scope measurement

- `git diff --name-only 40cb28c758b0 HEAD` = 13 files, ALL within 0428-076 write-set:
  - cmd/baha/app_perses_cli_test.go
  - cmd/baha/app_status_result.go
  - go.mod, go.sum
  - internal/metrics/perses_dashboards.go
  - internal/metrics/perses_dashboards_helpers.go
  - internal/metrics/perses_dashboards_promql_test.go
  - internal/metrics/perses_dashboards_test.go
  - internal/metrics/testdata/perses-dashboards/{loki-logs,mongodb-targets,postgresql-targets,prometheus-targets,tempo-traces}.json
- No unexpected path appeared.

## Step 4 — gofmt / vet / tests (literally recorded)

- `gofmt -l .` = empty (clean).
- `go vet ./internal/metrics/... ./cmd/baha/...` = empty (clean).
- `go test ./internal/metrics/... -run TestPerses` (after fix below) = `ok github.com/mcpdev80/baseharbor/internal/metrics`.
- IMPORTANT drift found and fixed (see below): the cherry-picked `TestPersesDashboardKeysMatchSelectionCatalogKeys` failed on develop drift.

### Drift finding + fix (0428-076 write-set, in-scope)

- `TestPersesDashboardKeysMatchSelectionCatalogKeys` (perses_dashboards_test.go, part of our own 2e5f87037) asserts our metrics catalog contains every key of `capability.DefaultDashboardCatalog().Templates()`.
- Develop (0428-080, commit 409444854, now on develop) added a `keycloak-identity` template to the selection catalog. `keycloak-identity` is `DashboardBackendIdentity` (an identity backend, never a metrics/logs/traces backend), so our metrics catalog never produced a panel for it. The comparison over the full selection.Templates() set was over-broad vs that drift.
- Fix in 0428-076's own test file (line 140): scope the match to real-signal metrics backends, skipping `DashboardBackendIdentity` keys. This matches the selection-catalog contract comment that Templates() ships only real-signal backends; our metrics catalog ships only metrics backends.
- Proven not caused by my edit: a clean cherry-pick on a fresh develop worktree fails the same test before any edit.
- SECOND drift fixed (0428-076 write-set, in scope): removing HostContainersDashboards from the struct broke develop's `TestBahaStatusHostContainersDashboardsExposesUnavailable`. Reconciled by carrying BOTH faces on the status JSON: keep develop's `HostContainersDashboards` (host/container views) AND add 0428-076's `DatabaseDashboards`. Both struct literals (local return and remote-target early return) updated; `resolvedHostSignalStatus` re-declared.
- Full `cmd/baha` subset (Perses|TrustStatus|Status) diff vs a clean develop baseline: IDENTICAL failing set after my fix (only timing jitter). My edits introduced ZERO new failures.

## Step 5 — product question on current develop

- PostgreSQL/MongoDB panels: present ONLY as `DashboardUnavailable` with a reason naming the missing native signal; zero panels, no exporter. Golden files confirm:
  - prometheus-targets.json kind=Dashboard panels=[app-up]
  - loki-logs.json kind=Dashboard panels=[app-errors]
  - tempo-traces.json kind=Dashboard panels=[app-traces]
  - postgresql-targets.json kind=DashboardUnavailable panels=[]
  - mongodb-targets.json kind=DashboardUnavailable panels=[]
- Supported panels carry real backend PromQL (e.g. prometheus `up{job="baseharbor-applications",baseharbor_application="$application",baseharbor_environment="$env"}`), no fabricated queries.
- Contract satisfied: panels appear only when verified compatible metrics exist; unsupported DBs stay explicitly unavailable. NO additional commit required.

## go.mod / go.sum — required, proven (per note-076-undraft.txt)

- go.mod/go.sum ARE changed vs develop (new module github.com/prometheus/prometheus v0.54.1 added as direct dependency).
- The import that demands it: `internal/metrics/perses_dashboards_promql_test.go:17` imports `parser "github.com/prometheus/prometheus/promql/parser"` (the promqlparser-tagged real-parser witness).
- `go mod tidy` leaves go.mod AND go.sum UNCHANGED (dependency is required, not removable).
- Reverting go.mod/go.sum to develop breaks the tagged test: `no required module provides package github.com/prometheus/prometheus/promql/parser`.
- Conclusion: the go.mod/go.sum change is required by our own committed test; it is NOT develop baseline. Both files stay.

## Step 6 — push + delivery

- `git push --force-with-lease lane-origin HEAD:perses-dashboard-databases-lane` = OK; `+ 540ed13ce...90063f6ec` forced update.
- Delivery proof: `git ls-remote lane-origin refs/pull/1597/head` = `90063f6ec66cf6d249181d803293f50064c44b8d` (== new head).
- `git diff origin/develop...HEAD --name-only` = the 13 files above (all in 076 write-set).

## Step 7 — undraft PR #1597

- PATCH `.../pulls/1597 -f draft=false` returned HTTP 200 but GitHub IGNORES the field (isDraft stays true). PUT `.../ready_to_review` and POST `.../drafts` both returned HTTP 404 (auth path).
- Correct method: `gh pr ready 1597 --repo mcpdev80/baseharbor` = "marked as ready for review".
- Verify: `gh pr view 1597 --json isDraft,baseRefName,headRefOid` = `{"baseRefName":"develop","headRefOid":"90063f6ec66cf6d249181d803293f50064c44b8d","isDraft":false}`.
- NOTE to Owner: the mission's `gh api PATCH ... -f draft=false` is wrong for this repo; the working command is `gh pr ready`.

## Step 8 — hosted run at exact head 90063f6ec (self-run, 4.6)

- Run id: 44812791612, event=pull_request, head_sha=90063f6ec66cf6d249181d803293f50064c44b8d.
- Terminal conclusion: FAILURE (run reached terminal state, watched to completion).
- Required cells that RAN (not skipped, because draft=false):
  - PR · Source format = success
  - PR · Trusted Plan = success
  - PR · Native gate plan = success
  - Workflow policy = success
  - PR · Focused Python = success
  - PR · Validation · cli-gofmt = success
  - PR · Validation · go-vet = success
  - PR · Validation · go-build = success
  - PR · Go unit · owner = success
  - PR · Go unit · packages = FAILURE
  - PR · Go unit · cli-0 = FAILURE
  - PR · Go unit · cli-1 = FAILURE
  - PR · Go unit · cli-2 = FAILURE
  - PR · Go unit · cli-3 = FAILURE
- All other cells (Targeted HA docker/podman, PR · Draft Go/Main release Go, Exact full Pre-Release, Native Keycloak/Core, Exact Candidate, Consumer Pins, Runner Interface, Public Contracts, Candidate-added advisory) = skipped.
- GATE-FAIL 0428-198 / 0428-202: the four Go-unit failures all fail with the identical field-wide gate line:
  - `main_test.go:60: create failed: Managed-environment machine operations require an authenticated BaseHarbor operator.`
  - e.g. `app_repository_workflow_test.go:115: Managed-environment machine operations require an authenticated BaseHarbor operator.`
  - `application_destroy_authorization_test.go:33: destroy must produce a partial plan for the selected app: Managed-environment machine operations require an authenticated BaseHarbor operator.`
  - `core_installation_test.go:75: Managed-environment machine operations require an authenticated BaseHarbor operator.`
  - Root cause: gate in internal/operatorauth/authorization.go:285 and cmd/baha/mcp.go:301 (both outside card 0428-076's write-set; internal/serviceaccess/policy.go is 0428-198's locked path). Pre-existing on develop baseline, NOT caused by this card's diff.
- This is a field-wide gate-defect (card 0428-198, root 2af892e4e in internal/serviceaccess/policy.go), outside card 0428-076's write-set. Per mission scope split (.github/** = Owner; locked files), it is reported as STATE, not patched.

## END

END_DONE w204-0428-076-hop: hop succeeded. New head 90063f6ec66cf6d249181d803293f50064c44b8d (4 own commits, 13 files, all in 0428-076 write-set; merge-base ancestor of 40cb28c758b0 = JA; git log origin/develop..HEAD lists only own commits). PR #1597 undrafted (isDraft=false, verified). go.mod/go.sum change proven required by perses_dashboards_promql_test.go:17. Two in-scope drift fixes applied (selection-catalog keycloak-identity scoping + both dashboard faces on status JSON) with zero-new-failures proven against a clean develop baseline. Product contract verified: PG/Mongo panels only as explicitly-unavailable, no fabricated data. Hosted run 44812791612 at 90063f6ec reached terminal FAILURE = GATE-FAIL 0428-198/0428-202 (identical "Managed-environment machine operations require an authenticated BaseHarbor operator" line in locked internal/operatorauth/authorization.go:285 + cmd/baha/mcp.go:301; pre-existing on develop, not this card's diff). gofmt/vet/build/owner cells all pass. No .github/** edit, no rerun, no subagent, no git add -A. Card 0428-076 write-set isolated; field gate defect routed to 0428-198/202.

## repo-rule compliance

- No `.github/**` edits, no rerun/workflow_dispatch.
- No runner infrastructure touched; GitHub-hosted shared runners only.
- No subagents (4.8); every step in this own session.
- No `git add -A`; targeted single-file adds.
- Evidence lives only in baseharbor-plan (not in the product repo).
- go.mod/go.sum change scoped to our own test import; revert proven to break the tagged test.
- Cleanliness: no docker/podman containers, networks, volumes or state directories started (no runtime gate run locally). No compose projects to tear down. Ambient-core images untouched.

- No `.github/**` edits, no rerun/workflow_dispatch.
- No runner infrastructure touched; GitHub-hosted shared runners only.
- No subagents (4.8); every step in this own session.
- No `git add -A`; single last commit.
- Evidence lives only in baseharbor-plan (not in the product repo).
