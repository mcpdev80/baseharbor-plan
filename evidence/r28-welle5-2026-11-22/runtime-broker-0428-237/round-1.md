# 0428-237 runtime-broker-health-unhealthy — diagnose akte

Card `t-20261122-runtime-broker-health-unhealthy`, lane `0428-237`. Diagnose only; **no product change** (no edits to any product file). Read-only chain trace to `datei:leile`.

## PLAN

- Rerun 44994268323 --failed on head a40b76764c3 (no push/force); follow run to terminal — per-job new job-id + status
- Classify deterministic vs transient
- Read-only `## Kette` trace: where the runtime broker starts, where the test waits for readiness, where 503 not_ready arises
- LANE-GESPERRE: `internal/observability/registry.go` + `internal/capability/perses_selection.go` — trace to them, STOP at `datei:leile`, no edit
- Write akte, publish to origin/main

## Evidence location

baseharbor-plan ONLY, never in a product repo. Verify with `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep runtime-broker-0428-237`.

## Base attestation

- develop head fetched (remote via `origin https://github.com/mcpdev80/baseharbor.git`): `33f5827788662b668f9f5b9d86767116e359612e`
- Run 44994268323 head = `a40b76764c3c08ec690e723def0ca167ce989c2b` (confirmed via `gh run view --json headSha`). This is the exact mission head.

## Rerun: run table

Rerun of the whole run (`gh run rerun 44994268323 --failed`) is rejected by GitHub: *"run 44994268323 cannot be rerun; its workflow file may be broken"* (HTTP 403, `POST /actions/runs/44994268323/rerun-jobs`). Rerun of an individual job (137130201480) is also rejected: *"The workflow run containing this job is already running"*. The run was observed terminal **completed/failure** twice (a second instance ran in the meantime). Job tally for run 44994268323:

| conclusion | count |
| --- | --- |
| success | 12 |
| skipped | 14 |
| failure | 4 |

The 4 failed jobs are exactly the data-capabilities native/runtime gates:

| job-id | job name |
| --- | --- |
| 137130201386 | PR · Native · native/docker/data-capabilities |
| 137130201480 | PR · Native · native/podman/data-capabilities |
| 137130201636 | PR · Selected Runtime (atomic/podman/data-capabilities…) / Executed podman · data-capabilities |
| 137130201640 | PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities) / Executed docker · data-capabilities |

Native gate planner is absent from the PR base (pre-planner develop): the native matrix `{include:[]}` is empty and the planner logs *"PR base does not contain trusted native gate planner"* → matrix job SKIPPED. This is a STATE finding (0428-235), not a defect for this card.

## Deterministic vs transient

**Deterministic broker-readiness block (card 0428-237).** The 503 `not_ready` appears in BOTH the docker and podman data-capabilities gates (run 44994268323 and its follow instance), on the same test `TestApplicationCapabilityLifecycleExistingCore` and the same readiness path. Same error pattern across runs = deterministic.

Cross-check (docker gate, job 137130201640): the docker data-capabilities fixture `tests/data-capabilities/new_edit.py` additionally raises `RuntimeError: actual native CLI JSON/MCP Footprint contracts differ` at `new_edit.py:282` (via `tests/guided/new_edit.py:63 footprint_parity(ROOT)`). That is a separate footprint-parity failure in the docker fixture, not the 503; the podman gate fails on the 503 directly.

## Kette (read-only trace to datei:leile)

Worktree: `workers/0428-237-wt` (detached HEAD at develop `33f5827788662b668f9f5b9d86767116e359612e`). **Read-only; no edits.** `git status` clean before and after.

1. **Test waits for runtime broker readiness.** podman data-capabilities gate log, job 137130201480, lines 406-410: the Quadlet `bh-docker-dev-capability-secrets-dev-broker.service` is started, then the test probes `/readyz`; the broker replies `"status":"not_ready"`. Log line 410:

   ```
   "ExitCode":1,"Output":"{\"status\":\"not_ready\"}\\ncurl: (22) The requested URL returned error: 503\\n"
   ```

2. **Broker starts.** `internal/controlplaneruntime/server.go:200-206` `serveControlPlane` → `newControlPlaneServer(cfg, handler)` → `serveControlPlaneServers(ctx, cfg, server, docsServer, …)`. The `/healthz` and `/readyz` handlers are registered in `internal/controlplaneruntime/server_run.go:157` `registerHealthHandlers(mux, cfg, deps)`.

3. **`/readyz` readiness checks.** `internal/controlplaneruntime/server_run.go:163-219`. The handler opens a 2s timeout (`server_run.go:164`) and checks each bound dependency in order:
   - `internal/controlplaneruntime/server_run.go:166-170` — `deps.pool` (database) via `database.Ping`; on failure `writeNotReady(w, "database", …)` at line 168.
   - `internal/controlplaneruntime/server_run.go:172-178` — `deps.boundRuntimeClient` (openbao) via `deps.boundRuntimeClient.Check`; on failure `writeNotReady(w, "openbao", …)` at line 175, logged at line 174.
   - `internal/controlplaneruntime/server_run.go:179-206` — `deps.boundExecutorClient` (runtime-executor); on failure `writeNotReady(w, "runtime-executor", …)` at line 182; the `else if cfg.boundRuntimeEnabled()` branch at line 185 falls through to the fail-closed `writeNotReady(w, "runtime-executor", …)` at line 203 when `brokerRequiresExecutor(cfg)` (server_run.go:235) is true.
   - Only when all present dependencies pass does it write `{"status":"ready"}` at `internal/controlplaneruntime/server_run.go:207-218`.

4. **503 not_ready arises.** `internal/controlplaneruntime/server.go:260-274` `func writeNotReady(w http.ResponseWriter, dependency, version, commit string)`:

   ```go
   func writeNotReady(w http.ResponseWriter, dependency, version, commit string) {
       w.Header().Set("Content-Type", "application/json")
       w.WriteHeader(http.StatusServiceUnavailable)   // 503
       response := map[string]string{"status": "not_ready"}
       if strings.TrimSpace(dependency) != "" {
           response["dependency"] = strings.TrimSpace(dependency)
       }
       if strings.TrimSpace(version) != "" {
           response["version"] = strings.TrimSpace(version)
       }
       if strings.TrimSpace(commit) != "" {
           response["commit"] = strings.TrimSpace(commit)
       }
       _ = json.NewEncoder(w).Encode(response)
   }
   ```

   The 503 with `{"status":"not_ready"}` (and a `dependency` field naming the failed bound dependency) is produced here, invoked from `internal/controlplaneruntime/server_run.go:168` (database), `:175` (openbao), `:182` and `:203` (runtime-executor).

## LANE-GESPERRE (trace to the gate, STOP)

The readiness chain terminates at the dependency checks above (`server_run.go:166-206`). The failed dependency is the **bound runtime client** (`deps.boundRuntimeClient`, openbao) or the **bound executor client** (`deps.boundExecutorClient`), both built by the broker's bound-runtime setup. That bound-runtime wiring — `internal/observability/registry.go` and `internal/capability/perses_selection.go` — is **lane-garded**.

Trace stops here at `datei:leile`:

- `internal/observability/registry.go` — lane-garded, **do not edit**.
- `internal/capability/perses_selection.go` — lane-garded, **do not edit**.

The evidence for the exact failed dependency (openbao vs runtime-executor vs database) lives in the broker's `/readyz` `dependency` field and the `runtime broker readiness failed: dependency=…` log emitted at `internal/controlplaneruntime/server_run.go:174` / `:181` / `:202` and captured in the job log line 410. Reading the failing dependency field in the run log is the next read-only step; it does not require touching the garded files.

## Cleanliness

`git status` clean in `workers/0428-237-wt` (no product edits, read-only trace). No containers/networks/volumes/state created by this lane. `docker ps -a` (own pid): none started here.

## END

`END_DONE w21-pr1702-0428-142-compat: 0428-237 diagnose round-1 done — 503 not_ready traced to server.go:260 (writeNotReady) invoked from server_run.go:168/175/182/203; lane-garded stop at registry.go + perses_selection.go; candidate SHA a40b76764c3; evidence on origin/main`.
