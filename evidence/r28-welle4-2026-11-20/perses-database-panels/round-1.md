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

## Scope investigation (the blocker)

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

The lane branch `perses-dashboard-databases-lane` is contaminated with ~20 other cards' commits (419-file diff). Cleaning it to a card-076-only candidate while keeping the same PR #1597 would either (a) drop other lanes' carried work from that PR branch or (b) require touching files outside card 0428-076's write-set. This is an Owner scope decision. Options being requested in the QUESTION are listed there.

## END

END_BLOCKED w202-0428-076-dbpanels: awaiting Owner scope decision on PR #1597 branch contamination (QUESTION posted to coordinator, run id 9142ab1f-c464-4f2f-abc8-d6997d8655ae). Card 0428-076 own write-set isolated and measured (6 files); branch also carries ~15 non-Perses r27 commits that are outside card 076's write-set. No product change, no push, no .github edit.

## repo-rule compliance

- No `.github/**` edits, no rerun/workflow_dispatch.
- No runner infrastructure touched; GitHub-hosted shared runners only.
- No subagents (4.8); every step in this own session.
- No `git add -A`; single last commit.
- Evidence lives only in baseharbor-plan (not in the product repo).
