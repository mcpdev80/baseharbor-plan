---
id: t-20261125-hunt-v51-ambient-test-env-leak
card_number: "0428-331"
card_short_title: "Ambient os.Setenv leaks"
type: task
areas: [test-isolation, lifecycle]
release: v0.4.27
version: ""
parent: ""
owner: "lane-0428-192-hunt-v51-testenv"
kanban_status: planned
kanban_lane: ready
kanban_summary: "Every raw os.Setenv call in a test.go file carries a paired restore (t.Setenv, defer os.Setenv, or os.Unsetenv), so no ambient…"
kanban_title: 0428-331 · Ambient os.Setenv leaks
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261125-hunt-v51-ambient-test-env-leak · 0428-192 · Ambient os.Setenv leaks BASEHARBOR_* across tests (#1650 class) #task #release/v0-4-27 #status/planned #view/ready #area/lifecycle #area/test-isolation #kind/task
    <!-- generated:card -->
    **Owner:** lane-0428-192-hunt-v51-testenv · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:card -->
**Owner:** lane-0428-192-hunt-v51-testenv · **Priority:** normal  
**Source:** [H-V51 akte](../evidence/r28-welle6-2026-11-27/bughunt-hv51-config-env/w196-0428-224-hunt-v51.md)  
<!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-0428-192-hunt-v51-testenv  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Every raw `os.Setenv` call in a `_test.go` file carries a paired restore (`t.Setenv`, `defer os.Setenv`, or `os.Unsetenv`), so no ambient `BASEHARBOR_*` / XDG / PATH value leaks across parallel or sequential tests. The build fails on any unpaired raw `os.Setenv` until the six known sites are remediated.

## Scope

- In scope:
  - A CI-native lint/audit test in the `cmd/baha` test group that FAILS on any raw `os.Setenv` in a `_test.go` without a paired restore.
  - Remediation of the six known raw `os.Setenv` sites:
    - `cmd/baha/runtime_integration_test_support_test.go:110` (`BASEHARBOR_CI_RUNTIME_INTEGRATION`)
    - `cmd/baha/runtime_integration_test_support_test.go:123` (`XDG_DATA_HOME`)
    - `cmd/baha/runtime_integration_test_support_test.go:692,696` (`XDG_CONFIG_HOME` / `XDG_DATA_HOME`)
    - `cmd/baha/runtime_integration_test_support_test.go:747` (`BASEHARBOR_TARGET`)
    - `cmd/baha/shared_core_dedup_runtime_test.go:124` (`application.ProviderScopeEnv(capability.ProviderPostgreSQL)`)
    - `internal/telemetry/otlp_test.go:96` (`application.OTLPEndpointEnv` bad value)
  - The helper idiom at `runtime_integration_test_support_test.go` (return-value-as-error for `os.Setenv`) switched to `t.Setenv` + `defer` or a cleanup func.
- Out of scope:
  - Any `.github/**` change. The audit test runs in the existing `cmd/baha` CI group that already covers `_test.go` files; register it there (no new engine). If the exact trigger must be confirmed, state it in the card and do not edit the workflow.
  - F1 (generic config validation error), F2 (doc drift), F4 (precedence fact): separate dispositions, see below.

## Acceptance

- The `cmd/baha` CI test group runs the audit test that asserts every `os.Setenv` in the package's `_test.go` files has a paired restore; the build currently fails on the six known sites and passes after remediation.
- All six raw `os.Setenv` sites carry `t.Setenv`, `defer os.Setenv`, or `os.Unsetenv`, verified by the audit test and by `grep`.
- No production code path is touched; the change is test-only.
- The audit test is a durable GitHub CI check, not a local-only/VM-only test.

## Cross-check #1650 (decision record)

#1650 (OPEN, head `lane-0428-078-perses-identity-on-resolver`, diff touches `internal/metrics/identity_dashboard_witness.go`, `cmd/baha/app_status_result.go`, `cmd/baha/app_perses_cli_test.go`) is a **Perses identity-keycloak dashboard availability** fix (real-metric witness). It is a DIFFERENT defect class than F3's test-suite ambient `os.Setenv` leakage. F3 does NOT generalize into #1650's in-lane fix; this card does not duplicate #1650's files or fix. The #1650 leakage-class category is the umbrella this card closes across ALL `_test.go` files.

## Dispositions for the other H-V51 findings

- F1 (config validation error quality): generic "runtime PostgreSQL configuration is incomplete" hides the missing credential key (`internal/runtime/config.go:59-95`). Separate minor DX card; add per-key `BASEHARBOR_<KEY> is required` errors mirroring the port path. Not in this write-set.
- F2 (doc drift): documented-but-absent provider keys (`docs/spec/service-access.md:30`, release notes). Doc-hygiene note / generated env-key registry. Not in this write-set.
- F4 (env-var precedence fact): documented precedence for Target (explicit), implicit/flag-absent for `serve.go` (`cmd/baha/context_terminal.go:204-236`, `serve.go:147-174`). No bug; recorded precedence-surface fact. No card.

## Required checks

- **Modified features:** Audit every raw `os.Setenv` in the `cmd/baha` `_test.go` files; add a regression test that fails the build on any unpaired call.
- **New features (test-isolation guard):** Register the audit test in the `cmd/baha` package test inventory and the existing CI group that covers `_test.go` files — the route already exists, no new engine, no `.github` edit. If the trigger must be confirmed, state it in the card and do not edit the workflow.
- **Hard acceptance gate:** For the audit test provide exact SHA -> test ID -> mapped CI check -> trigger -> actual run outcome. Missing registration, selection, trigger or real passing execution BLOCKS acceptance.

## Dependencies and file ownership

- Owned files: the six `_test.go` sites above plus the new audit test in `cmd/baha`.
- Shared files: none outside the test-only write-set.

## Handoff

- State: planned (intake pour). No candidate commit, no PR, no `.github` change. Reproduced vs develop tip `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82`. Full source: akte [w197-0428-224-intake](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv51-config-env/w197-0428-224-intake.md).
