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

Root cause + fix (see round-1 for investigation): `reference.go:160` declares the keycloak-metrics
native openmetrics signal but nothing registers it at runtime, so `observability.List(SignalMetrics)`
returns no Keycloak source and the 078 witness (`source.ID == "keycloak-metrics"`) can never match.

Fix in `internal/identityprovider/keycloak_realization.go`: added
`registerKeycloakSignals()`, called at the end of `localKeycloakRealization.Apply`, mirroring the
Loki (`logs/realization.go`), Tempo (`traces/tempo.go`) and OTel (`telemetry/realization.go`)
registration: the reference descriptor is the path, the deployment metrics policy is the gate.
`Enabled[SignalMetrics]=metricsEnabled` gates the source so a Target without metrics collection
keeps every gate fail-closed (no 080 non-forgeability regression).

CRITICAL ID MATCH: the registration `ID` MUST be the literal `"keycloak-metrics"` (NOT
`"keycloak:<project>"`). The witness iterates `observability.List` results and matches on
`source.ID == "keycloak-metrics"`; the registry stores `SignalSource.ID = registration.ID` and the
shared-scope dedup (`registry.go:245`) removes prior sources with the same ID+provider before
appending. A project-suffixed ID would register a source that the witness never matches. This is the
actual bug surface, not only "not registered".

Chain note (mission item 3): #1650 (0428-078) consumes this via
`internal/metrics/perses_identity_witness.go:118` — `IdentitySelectionWitnessAt` ->
`keycloakMetricSignals` -> `observability.List(SignalMetrics, ...)` then matches
`source.Provider == capability.ProviderKeycloak && source.ID == "keycloak-metrics"`. My registration
provides exactly that source. The production call-site wiring (app_status_result.go) is still the
078 lane's; my card only supplies the registered signal it reads.

## Implementation

(will record diff, build/vet/gofmt, test results here)

## repo-rule compliance

- No .github/** touched. No merge. No force-push. No ready_for_review. No subagent.
- Worktree under workers/ per workspace-layout rule; staging repo = /home/marcel/dev/baseharbor-ecosystem/baseharbor (origin/main verified at 13ffdd15d).
- Evidence lives only in baseharbor-plan.
- Full `go test ./...` run: my changed packages pass — identityprovider 139.8s, metrics 1.7s, observability 0.19s, runtimeobservability cached. The failing packages (cmd/baha, internal/controlplaneruntime, internal/database, internal/development, internal/machinehttp) are UNRELATED to my change and FAIL identically on clean develop (13ffdd15d) due to the local environment: no runtime executor (HTTP 503 / AppRole login failed), no native Core network, and "signal: killed"/XDG_DATA_HOME resource failures. Not a regression.

## Commit + push (DONE)

- Branch `lane-0428-097-keycloak-signal` cut from develop 13ffdd15d24fcfb4a379c834d25450ebb2737a6a
  (confirmed ancestor of the commit via `git merge-base --is-ancestor`).
- Commit f709e14b58f55be9e6ef93323e31bb9166aa04e8: "fix(0428-097): register keycloak-metrics native
  observability signal" — exactly ONE commit on top of the develop base, two files:
  `internal/identityprovider/keycloak_realization.go` (registration method + call in Apply) and
  `internal/identityprovider/keycloak_signal_registration_test.go` (positive + fail-closed regression).
- Pushed via refspec to lane-origin; ls-remote witness:
  f709e14b58f55be9e6ef93323e31bb9166aa04e8 refs/heads/lane-0428-097-keycloak-signal.
- PR #1660, base develop, head f709e14b5, **DRAFT/OPEN**. CI run 43929204510: all non-SKIPPED draft
  jobs (source-and-routing, Draft Go cli-0..3, Draft Go packages) COMPLETED/SUCCESS — run-id
  43929204510. (Draft PR policy skips the release/native/contract gates; this is the focused draft gate.)

## END status

- PRODUCTION registration DONE, PR #1660 OPEN/DRAFT/base develop, CI green @ f709e14b5 (run 43929204510).
- Evidence path lives only in baseharbor-plan (this akte); no product-repo evidence written.
