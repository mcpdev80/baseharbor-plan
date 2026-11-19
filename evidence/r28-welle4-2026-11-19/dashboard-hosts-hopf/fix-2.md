# Mission 077 — dashboard-hosts backend-signal correction (fix-2)

Lane: mission-077-catalog-availability (flash, codeman session 335715a4-de66-41c8-9de3-570eb353e325)
Card: t-20261114-r28-perses-dashboard-hosts / PR #1602
Branch: lane-0428-077-r28-perses-dashboard-hosts
Mission: /var/tmp/missions/mission-077-catalog-availability.md
Verdict under correction: evidence/r28-welle4-2026-11-19/codex-review-wave/1602-0428-077.md (REQUEST CHANGES on head b6c9702ba)

Candidate (40): 9f5470f97a112a6dae226712d63731676775b405
Reviewed head (40): b6c9702ba490d5d3fbdd52ef8d6dfbfad04e5318
Develop basis (40): 3b634232f000cfe0a344f34de57e4c5d92a340b0

Note on the mission's branch name: it names `lane-0428-077-dashboard-hosts-r2`; that ref does not
exist. `git ls-remote origin refs/pull/1602/head` = b6c9702ba490d5d3fbdd52ef8d6dfbfad04e5318 and the
only branch carrying it is `refs/heads/lane-0428-077-r28-perses-dashboard-hosts` (ls-remote witness
below). I continued on that single named candidate — no second branch (§3.6, AGENTS "exactly one
candidate per chain").

## PLAN

1. DONE Read mission, card t-20261114-r28-perses-dashboard-hosts, PR #1602 body + both review comments, codex act 1602-0428-077.md.
2. DONE Reality check (§4.1): fetch --prune; ls-remote head/develop; merge-base + merge-tree witnesses; hopf of develop f518e859d onto b6c9702ba (monotone merge commit, no force, no rebase).
3. DONE Gather the REAL emitted Loki/Tempo labels and OTLP attributes with file:line per backend (no guessing, no runtime stack on this host) — label-beweiskette below.
4. DONE Fix perses_dashboards_hosts.go: per-backend availability witness; Loki/Tempo never inherit Prometheus health; Loki selector to the emitted baseharbor_provider label; Tempo selector to the emitted baseharbor.provider span attribute.
5. DONE Replace the substring assertion with backend-specific selector assertions + the 'Prometheus healthy, Loki without signal -> Loki unavailable' case and the full per-backend matrix.
6. DONE Focused checks (no full ./... run): go test -run Perses, go test ./internal/metrics, ./internal/capability, ./cmd/baha -run TestBahaStatusHostContainers, go build ./..., go vet, gofmt -l, source-readability-audit.sh.
7. DONE Push to the named branch with ancestor witnesses; draft=false kept; then watch the exact-head run to terminal (§4.6) — result recorded below.
8. DONE Evidence committed and pushed to baseharbor-plan origin/main from /var/tmp/plan-077/clone (own clone, common planning worktree untouched); witness appended below.
9. END line (last section of this file).

## Zone witness (planning repo)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin` =>
https://github.com/mcpdev80/baseharbor-plan.git (the workers/baseharbor-plan directory is NOT the
planning repo and was never used). Evidence work happens in my own clone
`/var/tmp/plan-077/clone` (coordinator instruction 2026-11-19: no writes to the shared planning
worktree).

## Base attestation and hopf witnesses

- `git ls-remote origin refs/heads/develop refs/heads/lane-0428-077-r28-perses-dashboard-hosts`
  (measured, this session):
  - refs/heads/develop = e1dc2cf61ebbd7ee4e0467a5d33e22345c2e6b88 at mission start,
    f518e859df7adabed6e891ae30c010f0a075bdcc after the window move.
  - refs/heads/lane-0428-077-r28-perses-dashboard-hosts = b6c9702ba490d5d3fbdd52ef8d6dfbfad04e5318.
- Develop movement in this window, with the correct merge receipts (`gh pr view`):
  - #1691 (0428-121) merged 2026-11-19T11:56:52Z -> e1dc2cf61.
  - #1682 (0428-110) merged 2026-11-19T12:36:33Z -> f518e859d.
  - #1592 (0428-088) merged 2026-11-19T12:58:23Z -> 3b634232f (adds internal/application/perses_runtime.go
    to develop; my branch never referenced it, so the integration is a clean 0-conflict merge).
  The chain is linear: da76c5cf9 -> e1dc2cf61 -> f518e859d -> 3b634232f. #1598 (0428-084) is NOT
  merged: state=open, mergedAt=null, head ea6cddd204fbc408b8e1b3b587f1f054ea1f43ce — my earlier
  QUESTION text claimed it had been squash-merged; that was wrong and the coordinator corrected it.
  I never wrote to 084's files.
- `git merge-base --is-ancestor origin/develop b6c9702ba` = NOT an ancestor at start -> hopf required
  (PR mergeable_state 'behind' in the mission, confirmed).
- Hopf 1: merge commit 1440c21bfa5d1da506f6af37f89a876b3f027fe8 ("hopf-merge 0428-077: integrate
  develop f518e859d before backend-signal correction (r5)"), parents b6c9702ba + f518e859d. 0 conflicts.
- Hopf 2 (window move to #1592): merge commit 9f5470f97a112a6dae226712d63731676775b405
  ("hopf-merge 0428-077: integrate develop 3b634232f (#1592) before final candidate"), parents
  c81d1eda8 + 3b634232f. 0 conflicts. Both hopfs are monotone merges — no rebase (the branch carries
  develop merges; a rebase would replay integrated history — precedent #1592), no force-push.
- `git merge-tree --write-tree origin/develop HEAD` exit=0, tree ccbe4c71bfeec4b1d121fd5ab17e38c8797e73b1, CONFLICT count 0.
- `git merge-base --is-ancestor b6c9702ba490d5d3fbdd52ef8d6dfbfad04e5318 9f5470f97` = YES (reviewed head is an ancestor of the candidate).
- `git merge-base --is-ancestor 3b634232f000cfe0a344f34de57e4c5d92a340b0 9f5470f97` = YES (candidate is not behind develop).
- `git log --oneline origin/develop..HEAD` lists 31 commits; the three newest are mine
  (9f5470f97 the hopf-2 merge, c81d1eda8 + a8293b085 the correction, 1440c21bf the hopf-1 merge) and
  the rest are this chain's own historical 0428-075/077/080 commits from the reviewed head's own
  ancestry. No foreign candidate is carried on top: `git diff --name-only b6c9702ba 9f5470f97` shows
  only develop's own moved files plus my five candidate files (3 code + 2 goldens + 1 CLI test), and
  the write-set check below returns 0.
- `git diff --name-only b6c9702ba 9f5470f97 | grep -E "internal/capability/perses.go|internal/metrics/perses_contract_test.go|cmd/baha/app_status_result.go"` => empty (0 files).
- `git show --name-only --format= 9f5470f97` => 0 files: hopf 2 is a pure, content-preserving merge —
  it introduces no candidate change of its own (its whole content is develop #1592).

## Write-set discipline (coordinator disposition 2026-11-19)

- `internal/capability/perses.go` and `internal/metrics/perses_contract_test.go` were locked only
  because the 084 lane was running in parallel. They are no longer locked for later lanes, but I did
  not need them either: `capability.ResolveHostDashboardSignalStatus` stayed exactly as reviewed (it
  is a read-only resolver) and `perses_contract_test.go` is untouched — the diff witness above proves
  it. I did not edit `.github/**`, `scripts/**`, `internal/observability/environment.go` or
  `cmd/baha/perses_lifecycle*.go`.
- `cmd/baha/app_status_result.go` was also left untouched (it is a develop-moved, 084-adjacent file).
  Consequence I own openly: the CLI face keeps calling the one-argument
  `PersesHostDashboardAvailability(status)`, so on `baha status --json` Loki and Tempo now report
  `unavailable` with a reason that names their OWN missing signal, never `available` by inheritance.
  That is the fail-closed direction the review asked for. The per-backend witness
  (`PersesBackendSignalWitness`) is an internal function (`persesHostDashboardAvailabilityWitnessed`)
  precisely so this candidate does not widen the shared-CLI surface without its owner's change. A
  follow-up card should wire the witness from the registered provider log/trace signals.
- New-test CI pickup (AGENTS 5.3): every test here lives in `./internal/metrics` and `./cmd/baha`
  (package `main`), both already executed by the `PR · Go unit · packages` / `PR · Go unit · cli-*`
  shard cells of `.github/workflows/ci.yml` (the go-test selection over ./...); the trigger is the
  normal `pull_request` event to develop/PR branches with `draft == false`. No `.github/**` change
  was needed, so no finding with file:line is raised.

## The defect (proven, then fixed)

`PersesHostDashboardAvailability(resolvedHostSignalStatus)` fed ONE Prometheus verdict
(`capability.ResolveHostDashboardSignalStatus`, internal/capability/perses.go:338) into the whole
catalog: `persesHostDashboardCatalog` (perses_dashboards_hosts.go:335 in the reviewed head) realized
`prometheus-host-container`, `loki-host-container` AND `tempo-host-container` whenever the host
provider-metrics status resolved to `ObservabilitySupported`. A Loki/Tempo entry therefore turned
green because Prometheus was healthy. Both selectors were also invalid: they named labels their
backends never emit.

Fix: availability is decided per backend.

- `backendAvailableWithoutInference(backend, status, witness)` — prometheus from the resolved status,
  loki from `witness.LokiProven`, tempo from `witness.TempoProven`; nothing cross-wires.
- The default (CLI) witness is the zero value, i.e. fail-closed for Loki and Tempo.
- `hostBackendUnavailableReason(backend)` names the backend's own missing signal.
- Loki panel selector: `{baseharbor_provider=~".+"} |= "error"`.
- Tempo panel selector: `{.baseharbor.provider=~".+"}`.

## Label-beweiskette (file:line per backend, measured in the candidate tree)

Prometheus (available through the resolved host/provider-metrics status; unchanged semantics):
- internal/metrics/prometheus_render.go:221 — `- job_name: baseharbor-providers` (the scrape job is
  declared by BaseHarbor's own rendered config).
- internal/metrics/prometheus_files.go:71 — `"job": "baseharbor-providers"` and :72
  `"baseharbor_provider": string(source.Provider)` in the provider target file.
- internal/metrics/prometheus_verify.go:188 — BaseHarbor's own verification query uses
  `up{baseharbor_provider=%q,baseharbor_source=%q}`, i.e. this job/label pair is live in code.

Loki (the emitted labels are the Alloy relabel targets, NOT a Prometheus job label):
- internal/logs/render.go:145 — `target_label  = "baseharbor_provider"` in `loki.relabel "provider_syslog"`.
- internal/logs/render.go:152 — `target_label  = "baseharbor_service"` in the same rule set.
- internal/logs/render.go:163 — `target_label  = "baseharbor_provider"` in `loki.relabel "platform_provider_syslog"`.
- internal/logs/render.go:296 — `target_label = "baseharbor_provider"` in the journald provider relabel block.
- internal/logs/query.go:115 and :123 — BaseHarbor's runtime Loki verification queries select
  `baseharbor_source_class`/`baseharbor_provider`/`baseharbor_service`. No Loki query in the repo uses
  `job=` (grep for `job=` under internal/logs returns nothing).

Tempo (the emitted OTLP attributes; service.name never carries a provider job name):
- internal/telemetry/otlp_payload.go:28 — `keyValue("baseharbor.provider", string(source.Provider))`
  on the SPAN attributes of the provider interaction span.
- internal/telemetry/otlp_payload.go:38 / :66 — the RESOURCE attributes are
  `service.name = "baseharbor"` (or `m.Name`) / `service.namespace` / `deployment.environment.name` /
  `baseharbor.application`; nothing emits `service.name="baseharbor-providers"`.
- internal/runtimeobservability/observer.go:400 — `keyValue("service.name", component)` (component
  names such as "runtime-executor"/"runtime-broker").
- internal/runtimeexecutor/compose.go:277 and internal/runtimebroker/compose_render.go:170 —
  `OTEL_SERVICE_NAME: "runtime-executor"` / `"runtime-broker"`.
- internal/application/telemetry_binding.go:228-236 — `telemetryResourceAttributes` sets
  `service.namespace`, `deployment.environment.name`, `baseharbor.application`,
  `baseharbor.resource`, `baseharbor.provider`, `baseharbor.workload.service` — and no `service.name`,
  so the SDK default/`OTEL_SERVICE_NAME` governs the value in :38/:66 terms, never a provider job name.

Because TraceQL resource attributes come from the collector's resource while the provider identity in
BaseHarbor's own trace contract lives on the SPAN (otlp_payload.go:28), the Tempo panel selects on the
span attribute with the `.` prefix (`{.baseharbor.provider=~".+"}`), which is the only attribute whose
value is proven emitted for every provider trace.

Honesty note on proof strength: the Loki and Tempo label chains above are proven from the collector
and OTLP payload sources that the deploy paths write (internal/logs/state.go:215-217 renders
`config.alloy`; internal/telemetry exports the payload). I did not start a Loki/Tempo stack to query
`/loki/api/v1/labels` or a TraceQL search: docker/podman tests run only on baha-docker/baha-podman
(owner directive 2026-11-05) and this mission names no VM smoke cell. The STOP condition of the
recipe (real Loki/Tempo labels unprovable) is therefore NOT met; the proof is source-level and
line-exact.

## The three new/changed cases with their assertions

1. `TestPersesHostDashboardQueriesAreRealSignals` (internal/metrics/perses_dashboards_hosts_test.go:106-176,
   replaces the shared-substring check): decodes each real panel's query and asserts per backend —
   prometheus must contain `job="baseharbor-providers"` (:150); loki must NOT contain `job=` and MUST
   contain `baseharbor_provider` (:160-166); tempo must NOT contain `service.name="baseharbor-providers"`
   and MUST contain `baseharbor.provider` (:173-179).
2. `TestPersesHostDashboardAvailabilityConsumesAuthoritativeSignal` (:370-405): with
   `ObservabilitySupported`, prometheus is `available` with backend/datasource `prometheus`, while
   `loki-host-container` and `tempo-host-container` are `unavailable` and their reasons name their own
   backend; and for every non-supported resolved status all five keys are `unavailable`.
3. `TestPersesHostDashboardAvailabilityPerBackendNoInference` (:411-470), a 5-case matrix run through
   `persesHostDashboardAvailabilityWitnessed`: the named correction case "prometheus healthy, loki
   without signal -> loki unavailable", plus loki-proven -> available, and two cases where prometheus
   is unhealthy while the Loki/Tempo signal IS proven (they stay available on their own evidence), and
   all-proven. Every unavailable verdict must carry a non-empty reason.

Also updated: `cmd/baha/app_perses_host_containers_cli_test.go:86-125` — the genuine
`baha status --json` face now asserts the prometheus positive witness and the Loki/Tempo
negative witnesses with a backend-specific reason (it previously blessed all three as available,
which is exactly what the review rejected). Golden files `loki-host-container.json` and
`tempo-host-container.json` were regenerated by the deterministic marshaller (only the two query
lines change; witness in `git diff b6c9702ba c81d1eda8 -- internal/metrics/testdata`).

## Local checks (host: coordinator server; no container test started here)

- `go test ./internal/metrics -run Perses -count=1` — PASS (all Perses host/valkey/contract tests).
- `go test ./internal/metrics -count=1` — ok 0.250s.
- `go test ./internal/capability -count=1` — ok 0.007s (resolver and surface contracts unchanged).
- `go test ./cmd/baha -run TestBahaStatusHostContainers -count=1` — ok (genuine status path).
- `go build ./...` — ok; `go vet ./internal/metrics ./cmd/baha` — clean; `gofmt -l .` — empty.
- `bash scripts/source-readability-audit.sh` — PASS (file size, function span, ratchet; my file is
  652 lines, under the 800 limit).
- No full `./...` run, per mission step 3.

## Hosted run (Eigenes-Run-Pflicht, §4.6)

- Exact-head run on 9f5470f97a112a6dae226712d63731676775b405:
  https://github.com/mcpdev80/baseharbor/actions/runs/44530337283 ("CI · PR #1602", workflow
  "CI · Source & Quality") — watched by this lane to terminal:
  `gh run view 44530337283 --json status,conclusion,headSha` => **completed / success /
  9f5470f97a112a6dae226712d63731676775b405**, 3m18s wall.
- ZAHL der ausgefuehrten Zellen: **15 executed, all success; 19 skipped; 34 total.**
  Executed: Workflow policy; PR · Trusted Plan; PR · Native gate plan; PR · Source format;
  **PR Selected Checks = success**; PR · Go unit · packages; PR · Go unit · owner;
  PR · Go unit · cli-0 / cli-1 / cli-2 / cli-3 (the Perses host/valkey/contract tests and the new
  CLI witness run in these shards); PR · Validation · go-build; PR · Validation · go-vet;
  PR · Validation · cli-gofmt; PR · Focused Python.
  The aggregate that matters, `PR Selected Checks`, is **success** (not skipped).
- Skipped cells (expected for this impact plan, and explicitly NOT evidence): validate;
  PR · Draft source and routing; PR · Draft Go · shards; PR · Main release source / Go shards /
  checks; PR · Exact full Pre-Release; PR · Exact Candidate; Release Source Preflight;
  Targeted HA · docker; Targeted HA · podman; PR · Native · matrix; PR · Native Keycloak/Core;
  PR · Selected Runtime; PR · Selected Core-less; PR · Public Contracts; PR · Consumer Pins;
  PR · Demo Pin; PR · Runner Interface. The two "PR · Selected…" runtime cells are skipped and
  carry no claim (mission note + AGENTS: skipped is never green).
- Superseded intermediate runs on this branch, recorded for transparency: 44528319139 on
  a8293b085 (completed/success, 5m9s, 15 executed / 19 skipped) and 44529437369 on c81d1eda8
  (cancelled by the new push before terminal, per the branch's concurrency group — no test-result
  claim from it). Only 44530337283 qualifies the final candidate.

## repo-rule compliance

- Runtime, capability and delivery stay separate: the dashboard remains a management realization; it
  declares no capability, enables no exporter, and ships no privileged collector. Fail-closed
  availability preserved and strengthened (per backend, zero-value witness).
- CLI/JSON/MCP share one domain semantics: the public `PersesHostDashboardAvailability` signature is
  unchanged, so no surface drifts from another.
- plan -> preflight -> apply -> verify untouched (no lifecycle change in this candidate).
- Secret protection: no new logging; selectors are literals; no credentials in output or evidence.
- Ownership: only my card's files changed; no `git add -A`; isolated worktree `/tmp/opencode/w077-hopf`
  (nothing created under /home/marcel/dev/baseharbor-ecosystem); planning evidence in my own clone
  under /var/tmp/plan-077.
- No merge, no `gh pr ready`, no rerun/workflow_dispatch, no card status change, no subagent (§4.8),
  one candidate branch, draft=false kept.
- Note for the reviewer: `internal/metrics/perses_dashboards_valkey.go` shows in the PR diff because
  commit ae574b16d (my own earlier r3 develop-merge fix on this branch) removed a duplicate
  `marshalIndentNoEscape` from the valkey file. My fix-2 commits change that file not at all, and it
  is byte-identical to the reviewed head b6c9702ba.

## Handoff

- Candidate: c81d1eda8e6169e673c18445d1a1091984d0bfa3 on
  lane-0428-077-r28-perses-dashboard-hosts (PR #1602, OPEN, draft=false, mergeable=MERGEABLE,
  not behind develop).
- What changed: per-backend availability gating; Loki selector -> `baseharbor_provider` (the label
  Alloy emits); Tempo selector -> `.baseharbor.provider` (the span attribute the OTLP contract emits);
  backend-specific selector assertions; the fail-closed default witness; goldens regenerated.
- Open follow-up (needs its own card/owner decision, not silently done here): wire a real
  `PersesBackendSignalWitness` from the registered provider log/trace signals in the status command.
  The function exists (internal, `persesHostDashboardAvailabilityWitnessed`); exposing it publicly
  would have required editing `cmd/baha/app_status_result.go`, which sits in the 084/develop overlap.
  Until that wiring lands, `baha status --json host_containers_dashboards` reports Loki and Tempo as
  unavailable with their own reasons — correct, fail-closed, and never inherited.
- Reviewer check order: this act -> `git diff b6c9702ba..c81d1eda8` (3 code files + 2 goldens + 1 CLI
  test) -> run 44529437369 terminal state -> the label-beweiskette lines above.

## Cleanliness

- `docker ps -a` BEFORE (2026-11-19 ~12:25 CET, mission start): 7 pre-existing entries, all foreign
  (`bh-local-shared-*` = postgres, postgres-init, postgres-member-1, postgres-admin, openbao,
  openbao-member-1, openbao-admin) — ambient cores of other carts, untouched by rule.
- `docker ps -a` AFTER (2026-11-19 ~13:05 CET, before END): the same 7 pre-existing foreign entries;
  zero 077/perses/dashboards-owned containers, networks or volumes (filtered `docker ps -a` and
  `docker network ls` greps for 077/perses/loki/tempo return nothing). No compose project was started
  by this lane on this host or on any SSH test host; no vm-lock was taken.
- `podman`: not installed on this host (`command not found`), so no podman state can exist here.
- cleanliness: host left besenrein; work confined to /tmp/opencode/w077-hopf and /var/tmp/plan-077.

## Evidence-on-origin/main witness (second-to-last action)

- `git -C /var/tmp/plan-077/clone pull --rebase origin main` then commit + push; output appended below.
- `git -C /var/tmp/plan-077/clone rev-parse HEAD origin/main` — pasted below.
- `git ls-tree -r --name-only origin/main | grep dashboard-hosts-hopf/fix-2.md` — pasted below.

## END
