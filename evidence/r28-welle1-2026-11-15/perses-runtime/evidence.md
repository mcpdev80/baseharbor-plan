# Evidence — t-20261114-r28-perses-runtime

Mission: /tmp/opencode/mission-088.md
Card: t-20261114-r28-perses-runtime
Shift: r28-welle1-2026-11-15
Branch basis: lane-0428-075-perses-seam head af308e66d (PR base, retarget, no develop PR)

## PLAN

- Step 1: Read contract via plan.py show + read the card; confirm scope/write-set/acceptance
- Step 2: Reality check ls-remote of both repos (baseharbor + baseharbor-plan)
- Step 3: Claim + push BEFORE any change (§4.3)
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

## Owner authorization (2026-11-15, 17:5xZ) — FULL RUNTIME SCOPE

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

- END lane: BLOCKED (awaiting seam acceptance / Owner decision on the merge-frost window)
- 2026-11-15 17:5xZ: OWNER AUTHORIZED full runtime scope. Cut candidate from af308e66d. Implementing Perses runtime/lifecycle in internal/runtime, tests leave no containers/networks/volumes. Draft PR base = lane-0428-075-perses-seam (retarget, no develop PR, no merge).
- QUESTION posted 2026-11-15: seam is state `wait` (not accepted), PR #1575 open, merge forbidden under frost; evidence on origin/main (d27cb729); no branch cut, no merge attempted.
