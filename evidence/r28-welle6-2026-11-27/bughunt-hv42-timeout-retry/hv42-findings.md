# HV42 — timeout/retry/cancel semantics bug hunt (slice H-V42)

- Task card: 0428-224 (bug-hunt slice)
- Slice: H-V42 — timeout/retry/cancel semantics
- Anchor: develop `a87da7d179e08d43e8987885c38ab459ff1d887d` (verified `git ls-remote` origin develop)
- Clone: `/tmp/hv42-src` (fresh clone, `origin` = `https://github.com/mcpdev80/baseharbor.git`), checked out origin/develop
- State: PARTIAL — read-only findings; product changes NOT made (scope: pure finding)
- Owner stop: meldefrist issued 2026-11-25; investigation stopped, writeout delivered

## Method
- `grep -rn 'context.WithTimeout\|context.WithDeadline' internal/ cmd/baha/` (non-test)
- `grep -rn 'cancel()\|ctx.Err()'` apply/reconcile/backup paths
- retry loop / backoff scan in internal/ and cmd/baha
- timeout const/var inventory across packages

## FINDINGS (per-row file:line)

### F1 — Cancel called in loops without defer, leak risk on repeated iteration
- `internal/telemetry/otlp.go:735` — `cancel()` inside a loop body (not defer). If the loop re-enters, the previous ctx's cancel may fire after the loop exits; verify each iteration registers its own cancel and none outlives its use.
- `internal/runtimeobservability/observer.go:252` — `cancel()` without defer; confirm the cancel is scoped to the single probe and the ctx is not reused afterward.
- `internal/targetsession/session.go:107` — `cancel()` inside a loop (`context.WithTimeout(s.ctx, 2*time.Second)` at :105, cancel at :107). Repeated checks that cancel without defer can cancel the parent-derived ctx repeatedly.

### F2 — Nested/overlapping WithTimeout on the same ctx
- `internal/objectstorage/seaweedfs.go:84` `reconcileCtx, cancel := context.WithTimeout(ctx, sharedProviderReconcileTimeout)` then :126 `readinessCtx := context.WithTimeout(reconcileCtx, providerReadinessTimeout)`. Nested deadlines — the inner (90s) is smaller than outer (120s) so it binds; fine, but the outer reconcileCtx is never independently cancelled except via reconcileCancel at :85. Verify reconcileCancel fires on all return paths.
- `internal/logs/query.go:165-172` and `:204,260` — `probeCtx := context.WithTimeout(deadline, 20*time.Second)` then `probeCtx = context.WithTimeout(deadline, 3*time.Second)` reassigning the same name; the 20s deadline ctx is replaced by a 3s one. Ensure the 20s probeCtx cancel is invoked before reassignment or it leaks.
- `internal/machinehttp/terminal.go:47` — `context.WithDeadline(context.WithoutCancel(streamCtx), deadline)` builds an anonymous parent; if the returned cancel is never called the streamCtx-derived deadline is orphaned.

### F3 — Retry budget large / fixed with no context awareness
- `internal/deployment/environment_identity.go:240` and `environment_association.go:247,335` — `for attempt := 0; attempt < 4096; attempt++` — fixed 4096-iteration budget, no context deadline inside; a stuck lock spins up to 4096 iterations of the cheap command with no upstream cancel. Candidate for context-aware break.
- `internal/application/runtime_contract.go:751` — `for attempt := 0; attempt < 16; attempt++` bounded but no per-attempt timeout check; slow backends consume wall-clock beyond caller ctx.

### F4 — Timeout constant inconsistency (same logical phase, different magnitudes)
- reconcile/readiness across packages: objectstorage `sharedProviderReconcileTimeout=120s`, `providerReadinessTimeout=90s`, `existingProviderProbeTimeout=3s`; metrics `providerReconcileTimeout=60s`. No shared constant for "provider reconcile" — drift risk if one is tuned.
- `internal/metrics/perses_tempo_datasource.go:66` `tempoTraceQueryTimeout=10s` vs `internal/metrics/perses_tempo_verify.go:98` uses the same const but `internal/logs/query.go` uses a raw `45*time.Second` for log queries — query-phase timeouts diverge by package.
- `internal/identityprovider/keycloak_driver.go:704` `identityEndpointReadyTimeout=4*time.Minute` vs `keycloakClientSecretPropagationTimeout=30s` — endpoint-ready (4m) far exceeds secret-propagation (30s); a caller expecting both to bound the same readiness may be surprised.

### F5 — Context created from context.Background() for probes (no cancel propagation from caller)
- `internal/telemetry/otlp.go:726`, `internal/runtimeobservability/observer.go:250`, `internal/traces/tempo.go:360,644` (644 uses ctx but 360 uses Background), many `context.WithTimeout(context.Background(), 5*time.Second)` sites. Probes born from Background ignore caller cancellation/deadline. Low severity but systematic (269 hardcoded `X * time.Second` literals across internal/).

### F6 — Hardcoded durations instead of named constants
- `internal/machinehttp/handler.go:314,356` use `executionMaxRuntime` (good, named) but `internal/runtimeexecutor/server.go:105` uses `3*time.Second` inline for checkCtx, `internal/traces/credential_rotation.go:164` 45s, etc. Recommend extracting named vars to match the established `*Timeout` pattern.

## PROPOSED CARDS
- C1: add context-aware cancel break + per-attempt ctx deadline to `environment_identity.go:240` and `environment_association.go:247,335` retry loops (orphaned-spin risk, F3).
- C2: audit non-defer `cancel()` in loops — `otlp.go:735`, `observer.go:252`, `session.go:107` (F1).
- C3: dedupe provider-reconcile/readiness timeout constants into one named var (F4).
- C4: replace `context.Background()` probes with ctx-derived where a deadline is meaningful (F5).

## CLEANLINESS
- No containers/compose started by this lane. `docker ps -a` empty before and after (own pid 736875).
- Worktree clone `/tmp/hv42-src` removed after writeout; no stray files in ecosystem root.
- Read-only: no product files changed.

## STATUS
- Slice PARTIAL. Findings delivered above. Per-row card lines drafted (C1-C4).
- Evidence must reach baseharbor-plan origin/main before END accepted.
