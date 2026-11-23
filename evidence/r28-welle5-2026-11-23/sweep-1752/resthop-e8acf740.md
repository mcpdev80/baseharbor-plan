# 0428-061/#1752 sweep: ingress PR #1792 for 9 uncataloged source-pull paths

- karte 0428-061/#1752, sitz f0f6c8b4. PR-SWEEP. develop e8acf74055.
- #1725 observation completed (run 45096961182 terminal = SUCCESS). Recorded separately.
- #1752 CI 45099674733 FAILURE: Trusted Plan fail-loud on 9 uncataloged source-pull paths (#1753 class).
- OWNER ANWORT (2026-11-23): in-PR catalog edit CANNOT admit under base-precedence (proven #1753/#1725, validator base-load). DER WEG = proven INGRESS-PR (muster 252/253, twice merged): (1) develop-only ingress PR with the 9 components-rows, CI green, NO merge -> report to owner. (2) AFTER ingress merge: #1752 final-hop onto new tip. #1725 correction stays as follow-up. Ingress first.

## PLAN

1. #1725: observe run 45096961182 terminal — SUCCESS (Trusted Plan GREEN catalog==develop, native podman runtime GREEN, PR Selected Checks GREEN).
2. #1752: re-hop branch lane-0428-061-sourcepull onto develop e8acf74055 additively (git merge --no-ff). head 63b30d54. catalog byte-identical to develop, .github untouched, vet/build/test clean. push + ls-remote witness. (34feb4934 was stale-base, overwritten.)
3. #1752 CI 45099674733 terminal = FAILURE: Trusted Plan + PR Selected Checks. fail-loud uncataloged: cmd/baha/app_pull.go + 8 more (app_pull_mcp_approval_regression_test_go, app_pull_options_test_go, app_pull_render_go, mcp_lifecycle_extra_go, internal_development_source_go, source_pull_go, source_pull_test_go, internal_machine_contract_go). Record STATE.
4. Build develop-only ingress PR #1792: 9 components-rows (mustergetreu internal.operatorauth.test.operator.go). validator local green. push + ls-remote witness. No content file, no .github. No merge.
5. #1792 CI 45101821205 = FULL SUCCESS, zero failures. Trusted Plan GREEN. Wait for owner merge (owner action per PR policy).
6. #1752 final-hop after ingress merge.

## #1725 observation — run 45096961182 (terminal = SUCCESS)

- head 3d32bc489 (branch w201-0428-201-statever, base e8acf74055). catalog byte-identical to develop.
- conclusion = success. Key gates: PR · Trusted Plan success (catalog byte-identical, no uncataloged source), PR · Selected Runtime (native podman) success, PR Selected Checks success. No failures.

## #1752 re-hop — head 63b30d54 (before ingress)

- git merge --no-ff origin/develop e8acf74055 additively. merge-base == e8acf74055 (purely additive).
- diff vs develop: ONLY 20 content files (app_pull.go +201, source_pull.go +353, source_pull_test.go +516, mcp_lifecycle_extra.go +53, mcp.go +14, etc.), all additions, no deletions. .github untouched (0 touched). catalog byte-identical to develop.
- go vet ./cmd/baha/ ./internal/development/ ./internal/machine/ clean (exit 0). go build clean. app_pull tests pass (exit 0). push 63b30d54 to lane-0428-061-sourcepull + ls-remote witness. (stale 34feb4934 overwritten.)

## #1752 CI FAILURE — run 45099674733

- conclusion = failure. FAIL: PR · Trusted Plan, FAIL: PR Selected Checks.
- Trusted Plan step failure: "Resolve exact immutable PR inputs using trusted base policy".
- Fail-loud error string (exact): `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: cmd/baha/app_pull.go (id source.cmd_baha_app_pull_go); ... app_pull_mcp_approval_regression_test_go; app_pull_options_test_go; app_pull_render_go; mcp_lifecycle_extra_go; source.internal_development_source_go; source_pull_go; source_pull_test_go; source.internal_machine_contract_go` — add each with its surfaces to scripts/pr-gate-coverage.json.

## Ingress PR #1792 (owner-route, proven muster 252/253)

- branch lane-0428-ingress-061-source-pull from develop e8acf74055. head 59b5960694d5945583675ec1efb104325199edfa.
- 9 components-rows, mustergetreu internal.operatorauth.test.operator.go:
  - cmd/baha/app_pull.go -> id source.cmd.baha.app.pull.go, [source.gate.atomic.docker.data.capabilities, source.gate.atomic.podman.data.capabilities]
  - cmd/baha/app_pull_render.go -> id source.cmd.baha.app.pull.render.go, same form
  - cmd/baha/app_pull_options_test.go -> id source.cmd.baha.app.pull.options.test.go, same form
  - cmd/baha/app_pull_mcp_approval_regression_test.go -> id source.cmd.baha.app.pull.mcp.approgression.test.go, same form
  - cmd/baha/mcp_lifecycle_extra.go -> id source.cmd.baha.mcp.lifecycle.extra.go, [gate.mcp] (matches cmd/baha/mcp.go)
  - internal/development/source.go -> id source.internal.development.source.go, [source.gate.atomic.docker.observability, source.gate.atomic.podman.observability]
  - internal/development/source_pull.go -> id source.internal.development.source.pull.go, same form
  - internal/development/source_pull_test.go -> id source.internal.development.source.pull.test.go, same form
  - internal/machine/contract.go -> id source.internal.machine.contract.go, same observability form
- release stays v0.4.27. Pure additions: 62 insertions, 0 deletions. No existing catalog entry changed. No content file touched.
- surfaces derived from closest existing siblings: cmd/baha go -> data.capabilities (app_apply/app_broker pattern); cmd/baha mcp go -> gate.mcp (mcp.go); internal/development + internal/machine -> atomic.*.observability (perses_dashboards owner pattern).
- local: validate-pr-gate-coverage.py valid (exit 0); test_pr_gate_coverage 41 OK; test_pr_native_gate_plan 13 OK; all 9 sources resolve (fail-loud unowned list empty). Only file vs develop = scripts/pr-gate-coverage.json.
- ls-remote witness refs/heads/lane-0428-ingress-061-source-pull = 59b59606.
- PR #1792: base develop, head lane-0428-ingress-061-source-pull, state OPEN, isDraft false, mergeStateStatus CLEAN. Body references karte 0428-061/#1752 + #1753 class + proven ingress route.

## #1792 CI — run 45101821205 (FULL SUCCESS)

- conclusion = success, zero failures.
- Key gates: PR · Trusted Plan success (all 9 sources admitted — the systemic fix), PR · Native gate plan success, PR Selected Checks success.
- Also success: receipt-execution-tests, pr-planner-tests, ci-policy, ci-executor-tests, Source format, Focused Python, Candidate-added checks (advisory).
- Skipped: validate, Workstation onboarding, Targeted HA docker/podman, Release Source Preflight, Selected Runtime, Runner Interface, Public Contracts, Native, Main release, Go unit shards, Exact full Pre-Release, Demo Pin, Consumer Pins.

## Merge status (PENDING — owner action)

- #1792 mergeStateStatus CLEAN, CI green, no blockers. Merge is OWNER action (PR policy 0.4.28+; directive: owner does review->merge). As of akte, develop still e8acf74055 (ingress NOT yet merged). #1752 final-hop waits for #1792 merged.

## END (partial — ingress delivered, #1752 final-hop pending ingress merge)

END_BLOCKED w27-pr1627-0428-061-pull: 0428-061/#1752 ingress PR #1792 DELIVERED (head 59b59606, CI 45101821205 FULL SUCCESS, Trusted Plan GREEN). #1752 CI 45099674733 FAILURE (fail-loud 9 uncataloged source-pull paths, #1753 class) resolved by ingress route. #1752 final-hop pending #1792 merge (OWNER action per PR policy; #1792 CLEAN + green). #1725 observation 45096961182 SUCCESS recorded. #1725 correction remains follow-up per owner directive. docker ps -a clean.
