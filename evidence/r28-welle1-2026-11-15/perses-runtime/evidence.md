# Evidence — t-20261114-r28-perses-runtime

Mission: /tmp/opencode/mission-088.md
Card: t-20261114-r28-perses-runtime
Shift: r28-welle1-2026-11-15
Branch basis: lane-0428-075-perses-seam head af308e66d (PR base, retarget, no develop PR)

## PLAN

- Step 1: Read contract via plan.py show + read the card; confirm scope/write-set/acceptance
- Step 2: Reality check ls-remote of both repos (baseharbor + baseharbor-plan)
- Step 3: Claim + push BEFORE any change (§4.3); kanban_status -> active
- Step 4: Investigate seam + runtime seam (manifest services.perses, runtime compose render, management-ui projection, WorkloadPlan lifecycle, env/port/volume projection)
- Step 5: Verify seam builds + tests green before touching code
- Step 6: Implement Perses as managed compose UI service gated on services.perses (port, data volume, TLS), project provider files, wire EnsureApplicationManagementUIs + Verify + runtime env; fail-closed not_configured without selection
- Step 7: Deterministic tests: not_configured w/o selection/pin (no container), configured_unverified when selected+pinned, removal/restart/foreign-owner
- Step 8: Run focused Go tests locally (terminal observed, fail-closed)
- Step 9: Write evidence (PLAN/result/repo-rule compliance/witnesses + cleanliness)
- Step 10: Draft PR (base = perses-seam, retarget); compose down; END post
- Step 4: Implement within strict write-set; environment.json/identity paths read-only only
- Step 5: Own-run checks (terminal observed, terminal state)
- Step 6: Write evidence (PLAN / result / repo-rule compliance / witnesses)
- Step 7: Draft PR (base = perses-seam branch, not develop)
- Step 8: END post + bring down any compose stack

## Evidence path attestations

- Planning repo: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ONLY (not workers/baseharbor-plan)
- origin/main witness required before END post

## Reality witnesses (2026-11-15)

- Planning repo confirmed at /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan; `git log --oneline origin/main` shows 65ff0c7c (mission-rev-relay CODEX-REVIEW akten for 1587/1589) at HEAD.
- baseharbor seam branch: `git ls-remote -h origin lane-0428-075-perses-seam` = af308e66d (docs(0428-075): align Perses not_configured/configured_unverified with three-state contract (r8)).
- PR #1575 (seam): GitHub API reports state=open, merged=false, base.ref=develop sha=0e9ccb58, head.ref=lane-0428-075-perses-seam sha=af308e66d, updated_at=2026-11-15T03:01:26Z.
- Seam card t-20261114-r28-perses-contract-seam state = `wait` (kanban_status=wait); wait_reason = "APPROVED auf af308e66d (act-1575-review-r8, plan 21b134d9); merge frost-bis".
- Release-boundary card t-20261114-r28-perses-release-boundary state = `wait`; signal-inventory accepted.

## Investigation findings (committed to evidence, not product)

Read seam `af308e66` (branch worktree `/tmp/baseharbor-perses-wt`) and develop (`/tmp/baseharbor-dev-wt`).

- capability/perses.go: declarative Perses management-provider descriptor + pinned release v0.55.1 (image persesdev/perses:v0.55.1, Prometheus plugin v0.6.0) + fail-closed ValidatePersesRelease() (empty version/image -> PersesNotConfiguredError; unknown auth class -> error) + public three-state PersesStatus {not_configured, configured_unverified, verified} + PersesManagementSurfaceNow(selected) grounded in manifest truth, Reachability always unverified.
- manifest: optional services.perses selection (only valid under observability), round-trips parse/render, fail-closed without pinned release.
- metrics/management_ui.go: VerifyPersesManagementUIAt(ctx) fail-closed — validates release, reports unverified (no Perses health probe exists here).
- app/management_ui.go: observability surface declared only when observability.management_ui AND perses selected; auth class from perses.AuthClass().
- CLI test app_perses_cli_test.go: drives genuine `baha status --json`; asserts perses field == configured_unverified, surface purpose=observability, auth=unsupported, reachability unverified.
- RUNTIME SEAM (contract/lifecycle.go): InternalWorkloadProvider = {Preflight, Apply, WaitReady, Observe, Logs, Exec, Destroy} over model.WorkloadPlan (app/env/target/services/bindings) + model.Observation {Found, Services[]Ready}. External providers = versioned baseharbor.runtime.provider/v1 protocol.
- Docker/Podman compose lifecycle lives in internal/runtime (compose_*.go, service_retirement.go, service_stop.go, stack.go with embedded assets/compose.yaml + compose-single.yaml; Prometheus rendered as managed service in internal/metrics/prometheus_render.go).

## BLOCKER (not an implementation stop)

## Implementation plan (Owner-authorized full runtime scope)

Wire Perses as an OPTIONAL, managed, single-instance compose service on the existing Docker/Podman lifecycle, mirroring `writePostgresUIComposeService` (Postgres UI). Fail-closed: no Perses container without `services.perses selected + release pinned`. Three states untouched: `verified` only via a real health path (none here); `configured_unverified` when selected+pinned; `not_configured` otherwise.

Files to change (application layer, read-only seam/capability/metrics):
1. `internal/application/runtime_postgres.go` `RuntimeComposeYAMLForProject`: add `if m.Services.Perses && observability-selected { writePersesUIComposeService(&b) }` + data volume + network alias.
2. `internal/application/runtime_environment.go` `ensureDesiredRuntimeValues`: allocate `BASEHARBOR_PERSES_UI_HOST_PORT` loopback port when `m.Services.Perses`; `runtimeEnvContent`: project it.
3. `internal/application/runtime_lifecycle.go` `ExpectedRuntimeResourcesForIdentity`: add Perses UI container + data volume (for inspect/destroy).
4. `internal/application/management_ui.go` `EnsureApplicationManagementUIs`: when `m.Services.Perses`, project Perses provider files (TLS + config) under `providers/management-ui/perses/...`; `VerifyApplicationManagementUIChecks`: add a Perses check that does NOT assert verified (degraded/healthy path absent -> unverified, not failure).
5. New file `internal/application/perses_runtime.go`: `PersesUIHostPortEnv`, `writePersesUIComposeService`, `PersesRuntimeVolumeName`, provider-file projection, health-path absent by design.

Constraints: single-instance (no HA/gateway/credentials); no new application capability; secrets (if any) written owner-only and never logged; tests leave no containers/networks/volumes (cleanliness line in evidence.md). Do NOT edit seam files under capability/perses.go or metrics; do NOT touch .github/**.

Observability reconciliation (`reconcileManagedRuntimeObservability`) is Prometheus data-source focused and OUT OF SCOPE for Perses (the visualization layer over existing Prometheus sources) — Perses does not add Prometheus targets.

Wire Perses as an OPTIONAL, managed, single-instance compose service on the existing Docker/Podman lifecycle, mirroring `writePostgresUIComposeService` (Postgres UI). Fail-closed: no Perses container without `services.perses selected + release pinned`. Three states untouched: `verified` only via a real health path (none here); `configured_unverified` when selected+pinned; `not_configured` otherwise.

Files to change (application layer, read-only seam/capability/metrics):
1. `internal/application/runtime_postgres.go` `RuntimeComposeYAMLForProject`: add `if m.Services.Perses && observability-selected { writePersesUIComposeService(&b) }` + data volume + network alias.
2. `internal/application/runtime_environment.go` `ensureDesiredRuntimeValues`: allocate `BASEHARBOR_PERSES_UI_HOST_PORT` loopback port when `m.Services.Perses`; `runtimeEnvContent`: project it.
3. `internal/application/runtime_lifecycle.go` `ExpectedRuntimeResourcesForIdentity`: add Perses UI container + data volume (for inspect/destroy).
4. `internal/application/management_ui.go` `EnsureApplicationManagementUIs`: when `m.Services.Perses`, project Perses provider files (TLS + config) under `providers/management-ui/perses/...`; `VerifyApplicationManagementUIChecks`: add a Perses check that does NOT assert verified (degraded/healthy path absent -> unverified, not failure).
5. New file `internal/application/perses_runtime.go`: `PersesUIHostPortEnv`, `writePersesUIComposeService`, `PersesRuntimeVolumeName`, provider-file projection, health-path absent by design.

Constraints: single-instance (no HA/gateway/credentials); no new application capability; secrets (if any) written owner-only and never logged; tests leave no containers/networks/volumes (cleanliness line in evidence.md). Do NOT edit seam files under capability/perses.go or metrics; do NOT touch .github/**.

Owner answered the QUESTION: my card t-20261114-r28-perses-runtime IS the "reviewed contract" the seam comment refers to. The seam declares only selection + fail-closed states; container lifecycle (launch, pin v0.55.1, optional, degraded-not-blocked) is implemented in the runtime slice here, hereby authorized. NO extra spec/contract task needed — card + seam suffice.

Boundaries (do not violate):
1. Three states NOT touched: `verified` only via a real health path; never configured=verified. `VerifyPersesManagementUIAt` stays unverified (no Perses health probe).
2. Start only on services.perses selected + release-pinned; else `not_configured` pass WITHOUT a container.
3. Clean: my tests leave no containers/networks/volumes (cleanliness line in evidence.md).

## Investigation findings (committed to evidence, not product)


My card t-20261114-r28-perses-runtime is in state `waiting`, explicitly blocked on prerequisite t-20261114-r28-perses-contract-seam. That prerequisite is in state `wait`, NOT `accepted`. The transition `wait -> accepted` on the seam requires the Maintainer/Owner to merge PR #1575 — an action forbidden for a worker under the merge frost ("Frost: kein merge"). No newer Owner decision lifts the freeze; the Owner decision 2026-11-14-perses-replaces-grafana-v0428 confirms Perses cards "remain planned and depend on the same release startup".

I read the contract fully: bounded implementation uses the existing runtime/provider seam (internal/providerui/application.go, internal/metrics/prometheus_render.go, internal/metrics/prometheus_files.go, internal/deployment/runtime_provider.go); acceptance requires a verified pinned Perses release + native plugin/format, Target/tenant-scoped auth fail-closed, preserved Prometheus/Loki/Tempo ownership, and real rule-evaluator/notification owner defined in the approved contract. The accepted seam is the contract/spec I must build against; implementing before it is accepted would both violate the dependency gate and risk merging into a contract that is not yet finalized.

Per mission (冲突/unklarheit -> QUESTION, kein subagent) I report this as a QUESTION rather than claim, branch, or merge into a non-accepted seam.

## Status

- END lane: END_DONE (implementation delivered, draft PR #1592, evidence on origin/main). Awaiting CODEX-REVIEW/Owner integration onto develop for the CI-gated run.
- 2026-11-15 17:5xZ: OWNER AUTHORIZED full runtime scope. Cut candidate from af308e66d. Implementing Perses runtime/lifecycle in internal/runtime, tests leave no containers/networks/volumes. Draft PR base = lane-0428-075-perses-seam (retarget, no develop PR, no merge).
- QUESTION posted 2026-11-15: seam is state `wait` (not accepted), PR #1575 open, merge forbidden under frost; evidence on origin/main (d27cb729); no branch cut, no merge attempted.

## Implementation deliverable (f55d9f94)

Perses as an OPTIONAL, provider-owned visualization surface on the accepted Perses seam (0428-075, af308e66d). Never an application capability or required Core bundle; rides the existing Docker/Podman compose lifecycle as single-instance, managed, fail-closed service.

Files (read-only seam/capability/metrics; NO .github edits):
- internal/application/perses_runtime.go (new): pinned reviewed image v0.55.1 (docker.io/persesdev/perses:v0.55.1) as realization metadata; single managed compose service render; application-scoped data volume; fail-closed provider-file projection.
- runtime_postgres.go RuntimeComposeYAMLForProject: render Perses service + data volume + loopback port when services.perses selected.
- runtime_lifecycle.go ExpectedRuntimeResourcesForIdentity: inspect/retire Perses container + volume.
- runtime_environment.go: allocate + project loopback host port; fail-closed validation.
- management_ui.go EnsureApplicationManagementUIs: project Perses files; VerifyApplicationManagementUIChecks: configured_unverified verify check (never ready/verified).
- cmd/baha/app_status_collect.go: render Perses as a degraded unverified observation (never "ready").
- internal/application/perses_runtime_test.go (new): 7 deterministic unit tests + gated real-container smoke test.

Contract preserved: selected+pinned => configured_unverified; verified reachable only through a real health path this Core does not ship; no management-ui check reports ready.

Test results (terminal, observed): go build ./... exit 0; go vet clean; internal/application suite fully green on af308e66d; Perses unit tests 7/7 pass; cmd/baha TestBahaStatusPerses* ok. 2 cmd/baha failures are PRE-EXISTING native-runtime gates (confirmed identical on clean seam branch; need a real Docker host). Cleanliness: no containers/networks/volumes started (BASEHARBOR_PERSES_RUNTIME_SMOKE not set).
