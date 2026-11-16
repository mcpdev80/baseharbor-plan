# keycloak-metrics-signal-unregistered — round 1

Lane: lane-0428-097-keycloak-signal
Card: t-20261116-keycloak-metrics-signal-unregistered (0428-097)
Date: 2026-11-16
Owner: worker-ornith1.5 (this session)
Base attest: 13ffdd15d24fcfb4a379c834d25450ebb2737a6a (origin/main HEAD, develop)
Candidate: lane-0428-097-keycloak-signal (in progress)

## PLAN

- Investigate: confirm keycloak-metrics is declared in reference.go but never registered in the observability registry at runtime; map the loki/tempo/otel registration pattern and witness match path.
- Implement: register the keycloak-metrics native openmetrics signal in the Keycloak realization (Apply path), analogous to loki/tempo/otel, gated by metrics policy; NO new parallel resolver.
- Regression test: positive (registered signal + target-auth -> MetricPresent/MetricCurrent true) and fail-closed without registration; guard 080 non-forgeability invariant.
- build/vet/gofmt clean on changed packages.
- Commit precisely (staged), push via refspec to lane-0428-097-keycloak-signal, ls-remote witness, run CI to terminal, publish evidence + END post.

## Base attest

- develop / origin/main HEAD = 13ffdd15d24fcfb4a379c834d25450ebb2737a6a (verified via `git ls-remote origin refs/heads/develop`).
- No existing candidate branch for lane-0428-097-keycloak-signal (`git ls-remote origin` returns nothing for that ref).
- My worktree cut from develop-remote (13ffdd15d) under workers/ per workspace-layout rule.
- The planning repo is /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ONLY.

## Investigation findings

The bug is real and independent of the 078 lane's witness call-site:

- `internal/capability/reference.go:160` declares the Keycloak native openmetrics signal
  `{Name: "keycloak-metrics", Kind: ObservabilityMetrics, Status: ObservabilitySupported,
  Mode: ObservabilityNative, Protocol: "openmetrics", Verification: ObservabilityVerifyBackend,
  Port: 9000, Path: "/metrics"}`.
- Nothing registers that signal at runtime. The three existing provider metrics signals are
  registered exactly once each in their realization's Apply path:
  - OTel collector: `internal/telemetry/realization.go:191` -> `RegisterProviderSignals` (id `otel-collector-metrics:8888`)
  - Loki: `internal/logs/realization.go:227` -> `RegisterProviderSignals` (id `loki:3100`)
  - Tempo: `internal/traces/tempo.go:398` -> `RegisterProviderSignals` (id `tempo:3200`)
- `grep -rn "RegisterProviderSignals" internal/identityprovider/` => no Keycloak registration exists.
- `internal/metrics/perses_identity_witness.go:16` (078 lane) matches a real source by
  `source.Provider == capability.ProviderKeycloak && source.ID == "keycloak-metrics"` after a
  real `observability.List(SignalMetrics, ...)`. Without a registration the list is empty and the
  gate can never be true. `identity_dashboard_eligible` (cmd/baha/app_status_result.go:161) is
  therefore permanently false.

Scope decision (documented, not parked): the 078 lane adds the witness + call-site; on develop
neither exists. My card owns the registration half — wiring the reference signal into the registry.
The registration is the missing link the 078 witness reads. I do NOT add the witness/call-site
(080-scope, belongs to the resolver lane) and I do NOT touch a parallel resolver.

## Implementation

(will record diff, build/vet/gofmt, test results here)

## repo-rule compliance

- No .github/** touched. No merge. No force-push. No ready_for_review. No subagent.
- Worktree under workers/ per workspace-layout rule; staging repo = /home/marcel/dev/baseharbor-ecosystem/baseharbor (origin/main verified).
- Evidence lives only in baseharbor-plan.

## END status

- END_DONE / END_BLOCKED (to be posted last)
