---
card: 0428-108
task: t-20261117-trace-probe-adapter-gap
lane: mission-108-traceprobe
release: v0.4.28
---

# 0428-108 fix-1: trace-consumer probe adapter gap

## PLAN

1. Read mission, task card, base refs; publish claim
2. Reality sync: ls-remote develop + planning origin/main witnesses
3. Isolated worktree from develop@bcae1e8c1, branch lane-0428-108-traceprobe
4. Neutral reproduction of the failing test on develop
5. Source diagnosis: registry site + probe adapter switch
6. Fix part A: workload trace source registered under the OTLP receiver, not Prometheus
7. Fix part B: adapter dispatch routes receiver-owned sources to an OTLP export
8. Fix part C: receiver transitions, unbind, disabled-policy and legacy-signal reclaims
9. Focused regression tests (fail-first on base) + unit/vet/build
10. Provenance checks, commit, refspec push, PR onto develop (READY)
11. Exact-head CI run to TERMINAL (Eigenes-run-pflicht)
12. Evidence to origin/main + END post

## Base attestation

- Product repo remote truth: `git ls-remote origin refs/heads/develop` ->
  `bcae1e8c1261c9e44db03fe285a5d090c532dfcd  refs/heads/develop` (measured from
  /home/marcel/dev/baseharbor-ecosystem/baseharbor, 2026-11-17).
- Branch cut: `lane-0428-108-traceprobe` at exactly `bcae1e8c1` (the mission's
  declared basis). Ancestry witness: `git merge-base --is-ancestor bcae1e8c1 HEAD`
  -> true; `git log --oneline bcae1e8c1..HEAD` lists ONLY this lane's own commits.
- Planning repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`
  (`git rev-parse --show-toplevel` confirmed; NOT workers/baseharbor-plan).
  origin/main before evidence commit: `4c4ad559ba9df2985f07833f17725adc684cc266`.
- Claim published first: `4142c3db` (plan.py claim, task note owner + kanban sync).

## Reality reproduction (neutral develop@bcae1e8c)

A local neutral reproduction was attempted and is BLOCKED by this host, not by
the code: rootless Docker here still runs a Core backend (`bh-local-shared-*`
containers are live), so `assertCorelessHost` fails at runtime_test.go:94 before
the probe code is reached. Every `go build`/`go test` link step also dies with
`error writing long arguments to response file: write /tmp/args...: disk quota
exceeded` until /tmp was cleared; test hosts remain the named SSH gates.

Authoritative reproductions used instead (both pre-existing, remote):

- Hosted develop evidence, quoted in the task's diagnose file
  evidence/r28-welle3-2026-11-16/i18n-abachtung/rebase-window-1.md:
  neutral develop@bcae1e8c, same command path as CI:
  `BASEHARBOR_OTLP_HANDOFF_ACCEPTANCE=1 BASEHARBOR_TEST_RUNTIME=docker go test
  ./cmd/baha -run TestManagedRegisteredOTLP...` ->
  `runtime_test.go:94: live runtime inventory: Core containers=0 total containers=7`
  and `runtime_test.go:120: shared Identity apply: Verifying trace ingestion:
  native OTLP trace source prometheus:bh-docker-dev-otlp-handoff-dev has no runtime probe adapter`.
- Independent second witness (Codex, read-only) on develop@4bab986dc, Docker
  observability job 133865952530, guided-up-consented path: same failure with
  source `prometheus:bh-atomic-docker-observability-demo-dev`, pre-existing on
  develop, not introduced by #1677.

Fail-first witness for this fix's regressions was produced locally on base
@bcae1e8c1 (worktree /var/tmp/w108-traceprobe/basecheck): the base registry
yields `provider=prometheus id=prometheus:baseharbor-zzbase-dev class=application-provider
scope=application` for a workload trace signal, and every new receiver-scoped
assertion fails on base while passing on the candidate.

## Root cause

cmd/baha/app_traces.go:150 (`runtimeComponentTraceProbe`) only adapts
`runtime-broker` and `runtime-executor`; anything else falls to
"has no runtime probe adapter". That switch was not wrong in itself - the bug is
what reached it. internal/application/runtime_observability.go
(`reconcileApplicationMetricsSource`, introduced by PR #1676 on develop@bcae1e8c)
registers the workload's SignalTraces source under `Provider:
capability.ProviderPrometheus` with `Mode: ObservabilityNative, Protocol: otlp`.
Prometheus is a metrics backend (capability.ProviderPrometheus supports Metrics
only; its change contract is metrics.ingest/query/rules), so no probe adapter
can honestly serve that pairing. The OTLP handoff gate reaches it through
`app apply` -> convergeApplicationRuntime -> "Verifying trace ingestion"; the
guided-up-consented path reaches the same code through app_up_lifecycle.

## Fix (write-set: cmd/baha/app_traces.go + internal/application/runtime_observability.go + internal/observability/registry.go + internal/telemetry/otlp_interaction_trace.go)

- The workload trace signal is registered under the OTLP receiver the
  deployment policy actually selects (`TelemetryProviderForDeployment()` -
  managed collector, or registered external OTLP), never under the Prometheus
  metrics identity. The receiver identity is `<provider>:<runtime project>`, the
  same composition the Prometheus and Loki realizations already use for
  application-scoped sources.
- `nativeTraceSourceProbe` dispatches receiver-owned sources to a real OTLP
  export (telemetry.ExportNativeReceiverTraceAt, which reuses the production
  VerifyApplicationAt path: transport, mTLS material, external headers) and
  component sources to the existing runtime probe. The fail-closed default now
  names both halves of the mistake.
- New `observability.PruneSignals(id, kinds...)` removes one signal kind of one
  identity while keeping its other signals; registry entries are whole-file
  records and `Remove(id)`/`ReconcileSignals(id, ...)`/`UpdateSignal` all key on
  ID, so identity-exact pruning is the only safe reclaim primitive here.
- Reclaims (all bounded to the reconciled project's own identity): receiver
  transition collector<->external; return to managed transport after an
  external registration; traces-disabled policy (managed collector case; the
  external case intentionally leaves the collector-transport signal alone
  because `requiresManagedTraceStorage` is false for external deployments);
  and the legacy `prometheus:<project>` SignalTraces signal, reclaimed before
  the metrics-policy early return so it cannot survive a metrics-off apply.
  Metrics and log signals of every identity stay intact.

## Review findings incorporated (one batch, per coordinator)

1. Receiver-transition prune originally covered only the collector identity;
   now both receiver kinds are reclaimed on every transition/unbind path
   (TestWorkloadTraceSourceReclaimsBothReceiversWhenUnbound).
2. Legacy Prometheus workload trace signal could survive when the metrics
   policy turned off (early return before reconciliation); targeted reclaim +
   TestLegacyPrometheusTraceSignalIsReclaimedWithoutMetricsPolicy prove the
   trace signal goes and metrics/logs stay.
3. The no-receiver early return for `tracesEnabled=false` left a registered
   receiver trace in place; bounded prune added on that path plus the
   managed/external split in
   TestWorkloadReceiverTraceSignalsReclaimedWhenTracesDisabled.
4. The attribute-based prune keyed on (provider, class, scope, owner) across
   all projects/environments; replaced with exact-identity pruning
   (`<receiver>:<project>`), guarded by
   TestReceiverTracePruneIsScopedToReconciledProject (dev disabled, prod stays).

## Tests

- internal/application: TestWorkloadTraceSourceNeverAttributedToPrometheus
  (managed-collector, registered-external),
  TestWorkloadTraceSourceFollowsTelemetryReplacement,
  TestWorkloadTraceSourceReclaimsBothReceiversWhenUnbound,
  TestReceiverTracePruneIsScopedToReconciledProject,
  TestWorkloadTracePruneKeepsForeignSources,
  TestLegacyPrometheusTraceSignalIsReclaimedWithoutMetricsPolicy,
  TestWorkloadReceiverTraceSignalsReclaimedWhenTracesDisabled
  (managed_collector, registered_external),
  TestWorkloadTraceSourceRequiresMaterializedReceiver.
- cmd/baha: TestNativeTraceSourceProbeAdapterRouting (opentelemetry-collector,
  external-otlp, prometheus, runtime-broker, runtime-executor) - the adapter
  contract itself, no container needed.

Test -> check -> trigger: all new tests are ordinary Go package tests and run
in the existing PR CI Go-unit selection (`go list ./...` discovery, no
per-test registration) on every pull_request of this PR, and in the develop
push selection after merge. The named runtime gate that uniquely proves the
fixed production path is `PR · Selected Core-less · docker / coreless-lifecycle ·
application` -> TestManagedRegisteredOTLPNativeConsumerHandoff
(BASEHARBOR_OTLP_HANDOFF_ACCEPTANCE=1, TEST_RUNTIME=docker), executed by the
coreless shard jobs on PR/push; the podman cell runs the same test in its own
cell and is observed, not duplicated as a duty. The guided-up-consented docker
observability cell (second witness) runs in the same PR selection.

## Checks (local, candidate SHA)

- `go build ./...` OK; `go vet ./...` clean; `gofmt -l internal cmd` clean.
- `go test ./internal/application/ -run '^(TestWorkloadTraceSource...|TestLegacy...|TestWorkloadReceiver...|TestReceiverTracePrune...)'` -> all PASS (fail-first on base proven).

## Candidate and PR

- Branch: lane-0428-108-traceprobe (exactly one candidate; refspec push).
- Base at branch creation: bcae1e8c1 (develop, fetched). Rebased during work
  onto develop@6cf12152; final ancestry witness below.

## Process error found in review (fund -> Lernpflicht)

The first push, `af2fb5f6f`, carried ONLY the two test files: the three
production files (cmd/baha/app_traces.go, internal/observability/registry.go,
internal/telemetry/otlp_interaction_trace.go) were still unstaged in the
worktree. The cause was my own `git commit --amend` after a rebase: I staged
the test file with `git add` and amended, but a `git checkout HEAD -- <paths>`
line I ran on the *shared main repository* (`.../baseharbor`, a different
worktree) had clobbered my lane worktree's tracked files back to HEAD content
while the build/vet/test I ran afterwards passed against the then-dirty
tree  -  so "green locally" was measured against content that was not on the
candidate. The pushed head therefore could not compile (the committed adapter
test referenced `nativeTraceSourceProbe`, which the head did not contain).

Learning recorded here: (a) never run history or checkout commands against
another worktree of the same repository to inspect state  -  use a temporary
worktree with an explicit revision; (b) before any push, verify the commit
content itself (`git cat-file -p <commit>:<path>`) and build the pushed head in
a clean checkout  -  worktree status is not the candidate.

## Restoration and final candidate (additive, no reset, no force)

- Complete pre-amend commit `01c72e97f` (visible in reflog) carried all six
  files; production files were restored from it with explicit-path
  `git show 01c72e97f:<path> > <path>` and committed additively as
  `1b5a0df37` ("production adapter + registry prune apis").
- Fifth review item (OTLP-intent removal left `collector:<project>` registered
  because the project-scoped prune sat behind the early return) fixed with the
  prune moved ahead of the return +
  TestWorkloadTraceSignalReclaimedWhenOTLPIntentRemoved, committed as
  `4809c8648`. Fail-first witness: with the prune moved back behind the return
  in an isolated copy, the test fails with
  `collector trace identity survived the OTLP intent removal`.
- Reviewer findings 1-5 are therefore ONE batch in this section: (1) both
  receiver kinds reclaimed on transitions/unbind, (2) legacy Prometheus signal
  reclaimed before the metrics-policy early return, (3) bounded prune on the
  traces-disabled path (managed/external split), (4) exact-identity (project-
  scoped) pruning so dev-disable cannot touch prod, (5) prune moved ahead of
  the no-intent early return.
- Sixth review item (acceptance-blocking, resolved as ONE batch across three
  reviewer addenda) on head `082cefab`, committed additively as `39810520b`
  "key registry mutations on provider, not ID alone":
  - 6a: `pruneWorkloadTraceSignals` used ID-only `PruneSignals` while
    `RegisterProviderSignals` keys replacement on ID+provider - a same-ID
    source under another provider/owner could be co-deleted. Fixed with
    `PruneProviderSignals(id, receiver, kinds...)` (ID AND provider key).
  - 6b: `ReconcileSignals` (registry.go) deleted EVERY same-ID entry
    regardless of provider, so the same co-deletion existed on the reconcile
    path before any prune ran. Fixed: provider-scoped removal.
  - 6c (completion check): ownership derived from the desired set alone would
    silently keep stale entries when desired is legitimately EMPTY (disabled
    policies; `ReconcileRuntimeComponentObservability` reaches that state).
    Fixed with the explicit `ReconcileProviderSignals(id, owned, desired)`
    and the runtime-component caller now passes
    `map[ProviderKind]struct{}{component.Provider: {}}`, preserving the old
    stale-reclaim semantics for empty desired while sparing foreign providers.
    The dead `PruneOwnedProviderSignals` export is removed (finding: unused
    export). `RegistryHasSignal` exposes exact registrations for contract
    checks, immune to listing filters (which deliberately hide foreign
    same-ID records - reviewer addendum 2).
  - Regressions: `TestWorkloadTracePruneKeepsSameIDUnderOtherProvider`
    (application pkg; both paths - reconcile + intent-removal prune - assert
    via `RegistryHasSignal`); `TestRuntimeComponentReconcileEmptyDesiredKeeps
    ForeignSameID` (application pkg; real disabled-component caller path);
    `TestReconcileProviderSignalsEmptyDesiredPrunesOnlyOwnedProvider`
    (observability pkg; API boundary, incl. rejecting a desired signal whose
    provider is outside the owned set).
  - Fail-first witnesses (isolated /var/tmp worktrees against the current
    tree): (a) reverting the reconcile provider-scope fails path-one with
    `same-ID trace source under another provider died during reconciliation`;
    (b) keying the prune on the wrong provider fails with
    `workload's own external-receiver trace identity survived the intent
    removal`; (c) reverting the component caller to derived ownership fails
    with `disabled policies left the component's stale metrics signal
    registered`.

## Remote head + clean-checkout witness (mandatory)

Final head after the finding-6 batch:

    $ git ls-remote origin refs/heads/lane-0428-108-traceprobe
    39810520b5b1b7859faee4d9b489a4864a150948  refs/heads/lane-0428-108-traceprobe

Clean checkout of exactly that SHA (`git worktree add --detach ... 39810520b`,
`git status --porcelain` empty, rev-parse confirms the SHA):

    go build ./...      -> OK (no output)
    go vet ./cmd/baha ./internal/observability ./internal/telemetry ./internal/application -> OK
    go test ./internal/observability -count=1 -> ok 0.133s
    go test ./internal/application -run '^Test(WorkloadTrace|WorkloadReceiver|LegacyPrometheus|ReceiverTracePrune|RuntimeComponentReconcile)' -> ok 1.640s

Provenance: `git log --oneline origin/develop..HEAD` lists only this lane's
commits; `git merge-base --is-ancestor origin/develop HEAD` -> true against
origin/develop@409444854.

## Process error: PR opened before the clean-checkout witness (Lernpflicht)

PR #1679 was opened while the pushed head `af2fb5f6f` was still the incomplete
(tests-only) candidate, i.e. BEFORE the mandated clean-checkout build witness
existed. That left a red PR occupying the review queue. Corrected sequence,
applied for every head since: commit -> push -> `git ls-remote` -> clean
detached worktree of the remote head -> build/vet/test witnesses -> only then
PR/CI evidence. The earlier runs on superseded heads (44040963470 failure on
af2fb5f6, 44042182261 cancelled) are explicitly NOT counted as evidence.

## PR and CI run

- PR: #1679 (base develop, head lane-0428-108-traceprobe, READY).
- Exact-head run for `39810520b`: 44046875648 (CI - Source & Quality,
  pull_request), started 2026-11-17T08:27:25Z; outcome recorded in the END
  section once terminal (Eigenes-run-pflicht).
- The prior green run 44042477049 proves only the superseded head `082cefab`
  and is not acceptance evidence for the current code.

## VM/compose cleanliness

No container, compose project, network, volume or state directory was created by
this lane on any host; the local reproduction attempt was blocked before
starting any project (host not coreless). `docker ps` before/after shows only
the pre-existing ambient `bh-local-shared-*` Core containers of this machine,
untouched. cleanliness: clean (no lane-owned residue).

## repo-rule compliance

- No `.github/**` change; no workflow_dispatch or rerun; security.go untouched;
  no merge; no force-push; no subagent (§4.8); tmp under /var/tmp only;
  evidence only in baseharbor-plan; worktree under ecosystem worktrees/
  (/tmp/opencode was disk-quota blocked).
- Write-set respected: no touches to internal/capability/perses.go,
  perses_contract_test.go or 0428-092 files.
