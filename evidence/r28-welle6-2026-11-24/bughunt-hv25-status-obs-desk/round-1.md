# BUG-HUNT H-V25 — Status / Observability / Env-Desk (round 1)

Lane: w56-0428-265-huntstatusdesk
Type: read-only Befundung. No product changes, no commits/pushes, no PR, no hosted runs.
Develop anchor: 3ebfb90d (v0.4.28). Read from origin/develop via a detached mirror worktree.
Findings: 9.

## PLAN

- Setup: verify remotes, fetch develop, confirm anchor 3ebfb90d, locate baseharbor-plan repo.
- Area A #1816 (0428-152): read Perses alert-verifier 3-state machine, hunt False-Green/False-Red combos.
- Area B #1810 (0428-186): read PersesBackendAnswersStatusNow probe, guard order, fail-closed, Target binding, consumers.
- Area C #1809 (0428-058): read env-operations reveal-success-after-read, secret runtime-actor/allow, env_destroy consent + abort state.
- Cross-check duplication rule (skip registry.go/consent areas already in 0428-189..194, note "other spot").
- Write dossier with per-finding file:line, trigger, expected vs actual, severity, card ref.
- Persist to baseharbor-plan origin/main, verify with ls-tree, post END.

## Remote witness (planning repo, per mission)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`
origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

Develop truth: `git -C baseharbor ls-remote`/fetch -> origin/develop = 3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd (matches anchor).

## Method

Pure static code reading of the merged develop implementation. No build, no local test,
no VM used (none required: every claim is decidable from the source). No hosted runs
triggered (this is a read-only hunt, no PR).

## Findings

### F1 — `PersesBackendAnswersStatusNow` runs the dashboard build, not the documented real HTTP probe (Area B, medium)

- File:line: internal/metrics/perses_backend_status.go:49-60 (doc claims "real HTTP round trips ... httpClientSeriesProbe.querySeries"); the call chain reaches internal/metrics/perses_infra_dashboards.go:652 `BuildPersesInfraDashboardWithProbe`, whose per-panel probe is the build-time signal probe at perses_infra_dashboards.go:119-121.
- Trigger: `baha app status --json` on an applied Perses surface (app_status_result.go:314).
- Expected (per doc + card 0428-186): a per-target backend probe against this manifest's materialized Prometheus datasource endpoint, pinned release, authorized metrics policy (persesPrometheusDatasourceEndpoint + providerHTTPClient), returning verified only when the backend answers.
- Actual: it uses `BuildPersesInfraDashboardWithProbe`, i.e. the datasource-independent dashboard build, NOT the `VerifyPersesInfraDashboard` path that the same file's own sibling (PersesInfraDashboardAvailability, perses_infra_dashboards.go:189-231) uses and that the comment at app_status_result.go:306-307 names as the "real" probe ("only ... VerifyPersesInfraDashboard can"). Two different "real probe" definitions coexist in the same codebase for the same surface.
- Severity: medium (misleading contract; the status three-state is not derived from the endpoint/authorization path the doc pins).
- Refs: card 0428-186 / #1810.

### F2 — `PersesBackendAnswersStatusNow` and `PersesInfraDashboardAvailability` can disagree on the same manifest (Area B, medium)

- File:line: internal/metrics/perses_backend_status.go:81 (`BuildPersesInfraDashboardWithProbe`) vs internal/metrics/perses_infra_dashboards.go:208 (`VerifyPersesInfraDashboard`). Both called in the same status render at cmd/baha/app_status_result.go:314 and :317.
- Divergence drivers:
  - Endpoint resolution: VerifyPersesInfraDashboard calls `persesPrometheusDatasourceEndpoint` + `providerHTTPClient` and fails closed to all-unavailable if the datasource/endpoint is missing or unauthorized (perses_infra_dashboards.go:129-149); the status-probe path takes the datasource error to configured_unverified but otherwise probes via the build path.
  - All-missing semantics: `VerifyPersesInfraDashboard` errors when NO panel answered (perses_infra_dashboards.go:145-147) → availability = all-unavailable; `PersesBackendAnswersStatusNow` maps all-missing to configured_unverified (perses_backend_status.go:85-87).
  - Partial-missing: build path leaves `result.Signals` populated with `MissingSignal` flags; the probe result may not (per-panel vs endpoint query family).
- Trigger: applied Perses surface, materialized endpoint, partial panel gap.
- Expected: the two faces agree (same surface, same backend).
- Actual: `perses.status` and `infrastructure_dashboards` may report verified vs all-unavailable simultaneously for one manifest.
- Severity: medium (observability self-consistency defect).
- Refs: card 0428-186 / #1810.

### F3 — `baha app status --json` runs a live HTTP probe with no operator context (Areas A+B, low/medium)

- File:line: cmd/baha/app_status_result.go:294-317; `collectApplicationStatus` (cmd/baha/app_observe.go:32) issues no `authorize*`/`operatorauth` check; PersesBackendAnswersStatusNow performs HTTP at perses_backend_status.go:52-60.
- The Perses status contract (internal/capability/perses.go:213-214) says "verified" requires "an authenticated operator context"; the code path has no such gate.
- Mission A claim: "Status nur mit authentifiziertem Operator-Kontext." The `reportPersesSurfaceStatus` seam (cmd/baha/perses_lifecycle.go:351-358, for `baha app perses status`) DOES call `authorizeApplicationOperation`, but `baha app status` (the machine-JSON surface, cmd/baha/app_status_result.go:294+) does not gate.
- Trigger: `baha app status --json` in a managed environment without operator session and without a verified local runtime authority.
- Expected: probe runs only in an authorized/verified context, or a documented allow-anonymous-read contract.
- Actual: HTTP probe runs without any authorization; verified/configured_unverified reported in a context the contract says cannot promote to verified.
- Severity: low/medium (information-disclosure risk on a read surface; contract/code drift).
- Refs: cards 0428-152 (#1816), 0428-186 (#1810).

### F4 — `PersesBackendSignalWitness` in `reportPersesSurfaceStatus` is always the zero-value (Area A, medium)

- File:line: cmd/baha/perses_lifecycle.go:366.
- The call passes a literal `metricsprovider.PersesBackendSignalWitness{}`. All three Proven fields (internal/metrics/perses_dashboards_hosts.go:546-555) are bool zero-values false. `persesBackendSignalWitnessFromManifest` (cmd/baha/app_status_result.go:117) cannot report "configured" (requires PrometheusProven / LokiProven / TempoProven = true) — it returns every declared signal as "unreachable", never "configured".
- Trigger: `baha app perses status` on an applied, fully working observability stack.
- Expected: the human `perses status` surface shows backend witness from real observation.
- Actual: every declared backend appears "unreachable" because the witness is hard-coded empty. The comment at app_status_result.go:112-116 claims this is "card 0428-143" — but #1816 is merged, so this is now stale: the surface should be wired to a probe.
- Severity: medium (False-Red on human surface; card-level gap: 0428-143 not landed yet #1816 merged).
- Refs: cards 0428-143 (unlanded), 0428-152 (#1816).

### F5 — `PersesBackendSignalWitness` never populated anywhere on the machine-JSON path either (Areas A/B, medium)

- File:line: cmd/baha/app_status_result.go:328 (remote face) and :436 (local face) — same zero-value literal.
- Consequence: even `baha app status --json` never reports `prometheus`=configured, `loki`=configured, `tempo`=configured — always "configured_unverified" or "unreachable".
- Combined with F4: the entire PersesBackendWitness JSON field on every status surface is a fixed-shape output independent of the real backend (only manifest declaration decides "configured vs not-configured").
- Trigger: any status command against a working stack.
- Expected: the `configured` verdict is reachable via real observation.
- Actual: unreachable in code — no call site produces `PersesBackendSignalWitness{PrometheusProven: true, ...}`.
- Severity: medium (False-Red at the machine consumer).
- Refs: card 0428-143 / #1816 (the "witness producer" the surface claims to consume).

### F6 — `deploymentApplied` fail-open on unreadable runtime tree (Area A, low/medium)

- File:line: cmd/baha/perses_lifecycle.go:343-346.
- `deploymentApplied` returns true iff `ExistingRuntimeFiles(...) == nil`. Any transient IO error, permission error, or corrupt runtime tree returns an error → treated as not-applied, but on the applied branch the state comes from `persesAlertEvaluatorObservation` which calls `BuildPersesAlertEvaluator` (manifest-only, no runtime reading).
- Trigger: applied deployment with manifest selecting Perses, runtime files temporarily unreadable (e.g. store locked, IO error).
- Expected: fail-closed to "not configured" (the doc at perses_lifecycle.go:340-342 says exactly that).
- Actual: if `ExistingRuntimeFiles` succeeds but returns stale/incomplete files (e.g. prior deployment's files still on disk), `deploymentApplied` is true and `persesAlertEvaluatorObservation` reports the applied verdict based only on the manifest — the applied verdict can reflect a different deployment than the current runtime.
- Severity: low/medium (edge-case; only when store returns non-ErrRuntimeNotApplied for wrong deployment).
- Refs: card 0428-152 / #1816.

### F7 — `VerifyPersesAlertEvaluatorHealth` is unreachable from any CLI/MCP path (Areas A/B, medium)

- File:line: internal/metrics/perses_prometheus_alerts.go:90-115 (production path, per-panel health API verification).
- Only callers (grep -r): perses_prometheus_alerts.go itself and its test file. No `cmd/baha` or `internal/mcp` call site.
- Mission A explicitly asks: applied-but-failing must show "observed" vs. "configured_unverified". `BuildPersesAlertEvaluator` returns always `configured_unverified` (perses_prometheus_alerts.go:83); the `Verify*Health` function that could distinguish them is not called by the CLI.
- Trigger: `baha app perses status` on a broken live alert evaluator (Prometheus loaded but rule health != ok).
- Expected: reported as observed-failing per mission A contract.
- Actual: reported as configured_unverified because the health-verify path is never invoked.
- Severity: medium (False-Green: contract states 3-way observation, code produces 2-way only, no probe of the rule health).
- Refs: card 0428-152 / #1816.

### F8 — Documentation references a non-existent symbol `metrics.PersesBackendAnswers` (Areas A/B, low)

- File:line (all comments/doc, no code path):
  - internal/application/perses_lifecycle.go:162
  - internal/capability/perses.go:213 and :252
  - internal/metrics/perses_backend_status.go:18 (misses the `StatusNow` suffix — says "real HTTP round trips ... querySeries" without the exact name)
- The real exported symbol is `PersesBackendAnswersStatusNow` (internal/metrics/perses_backend_status.go:38). Grep confirms `PersesBackendAnswers` appears ONLY inside these comments; no definition, no call.
- Trigger: any developer navigating via the doc references.
- Expected: comments name the actual function.
- Actual: stale symbol name in four doc references.
- Severity: low (documentation drift, not behavior).
- Refs: card 0428-186 / #1810 (introduced the real function name; earlier docs not aligned).

### F9 — Perses surface-status naming drift: underscore vs hyphen across two surfaces (Area A, low)

- File:line: `application.PersesLifecycleStatus` returns `not_configured` / `configured_unverified` (underscores, internal/application/perses_lifecycle.go:166-171 via capability.PersesStatusNow at internal/capability/perses.go:265-283).
- `persesAlertEvaluatorObservationWithApplication` returns `not configured` (SPACE, cmd/baha/perses_lifecycle.go:234) / `unavailable (owner-gated evaluator contract)` (:235) / `configured_unverified` (from BuildPersesAlertEvaluator reachability constant, internal/metrics/perses_prometheus_alerts.go:21).
- `persesBackendSignalVerdict` returns `configured` / `unreachable` / `not-configured` (HYPHEN, cmd/baha/app_status_result.go:76-80).
- Same "surface" concept, three different string shapes for the three-state values, in the SAME JSON output (Perses.State, Perses.AlertEvaluator.State, PersesBackendWitness[].State).
- Trigger: parse `baha app status --json` or `baha app perses status --json` and match the three-state value.
- Expected: one canonical spelling for the three states (mission wording uses "not configured" and "configured_unverified" — the codebase has more than these).
- Actual: `not_configured` (underscore) vs `not configured` (space) vs `not-configured` (hyphen); `configured_unverified` (underscore) vs `configured` (unqualified); `unreachable` — a value the mission contract doesn't list at all.
- Severity: low (functional but consumer-parsing fragile and spec drift from mission A wording).
- Refs: cards 0428-152 (#1816), 0428-186 (#1810).

## Areas confirmed clean (no finding)

- Area A False-Green/False-Red: `persesAlertEvaluatorReachabilityVerified` defensive map-to-unavailable at cmd/baha/perses_lifecycle.go:282-284 correctly prevents a hypothetical "verified" reachability string from ever surfacing as healthy. `VerifyPersesAlertEvaluatorHealth` is not on the consumer path, so a false "verified" cannot fall out. Fail-closed contract HOLDS for alert-verifier.
- Area B fail-closed for unselected surface: perses_backend_status.go:43-48, :69-74 correctly return not_configured before any endpoint setup, matching "Setup-vor-Guards-Reihenfolge" reversed claim (guards before setup IS correct fail-closed).
- Area B Target binding: the probe uses the resolved manifest (perses_backend_status.go:52, :81), and per-target HTTP through providerHTTPClient (perses_backend_status.go:56, perses_prometheus_alerts.go:110) is target-scoped — no static reference-catalog scan.
- Area C reveal-success-after-read: cmd/baha/environment_operations.go:52-56 records success only after `ExistingRuntimeFiles` + `os.Stat` + `loadApplicationEnv` all succeed; three explicit failed-reveal audit points at :30-35, :40-42, :47-49. HOLDS.
- Area C secret runtime-actor/allow: cmd/baha/secret_operations.go:71-83 correctly distinguishes runtime actor (trusted-local) from cli/local-operator, and `AuthorizationResult` matches outcome ("success"→allow, other→deny). HOLDS. (Note: pattern is duplicated with env_destroy audit at cmd/baha/env_destroy.go:360-370 — as expected, "wie 0428-1xx, andere stelle".)
- Area C env_destroy consent: cmd/baha/env_destroy.go:149-164 requires explicit separate confirmation for `--delete-data` before ANY destructive apply.
  - Interactive path: `confirmedDataDeletion` prompts typed "DELETE" (:323-329), `strings.EqualFold(strings.TrimSpace(answer), "DELETE")` correctly rejects whitespace/case variants.
  - Non-interactive path: only `--confirm-delete-data` satisfies it (:320-322), enforced by parse-time validation at :426-428 ("--confirm-delete-data requires --delete-data"). HOLDS.
  - Flag parsing at :397-429 accepts both `--yes` and `--no-input`; `--no-input` is consumed and non-interactivity is set from the global context (main.go:210-211). HOLDS.
- Area C abort leaves deletable/non-corrupt state: cmd/baha/env_destroy.go:284-295 `applyAndRemoveEnvironmentIdentity` calls the per-deployment apply loop FIRST, then `DestroyEnvironmentIdentity`. Any mid-loop failure returns an error WITHOUT touching identity state (:175-178 prints "Environment destroy incomplete; identity retained so the operation can be retried"). Identity retained → retry works. Partial retire of some deployments is inherent to multi-deployment destroy and is honestly reported. HOLDS.
- Duplication check (mission 13): cmd/baha/app_client_consent.go:28 (`actor := "trusted-local"`) is the consent flow already covered by cards 0428-189..194, no new finding there.

## cleanliness

No product changes. No builds. No hosted runs. No VM/container/compose projects created or started by this lane (static reading only).

Before (pid 2297395): `docker ps -a` = 0 containers; networks = 32; volumes = 31.
After: `docker ps -a` = 0 containers; networks = 32; volumes = 31 (identical — nothing added or removed by this lane).

cleanliness: besenrein — this lane started and stopped nothing; ambient baseharbor-*/bh-*/bh-docker-dev-shared-* images, networks and volumes (other cards' karren) untouched. Worktree mirror at /tmp/opencode/w56-0428-265-huntstatusdesk-wt (detached HEAD 3ebfb90d) to be released at END.

END_DONE w56-0428-265-huntstatusdesk: 9 findings (F1-F9), no product changes; dossier evidence/r28-welle6-2026-11-24/bughunt-hv25-status-obs-desk/round-1.md.
