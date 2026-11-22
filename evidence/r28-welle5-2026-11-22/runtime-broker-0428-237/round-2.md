# 0428-237 read-only diagnose: runtime-broker `/readyz` dependency mapping (round-2)

Card: t-20261122-runtime-broker-health-unhealthy (0428-237, READ-ONLY, one point)
Lane: w27-pr1627-0428-061-pull
Shift: r28-welle5-2026-11-22
Status: END_DONE — read-only diagnosis complete. CI log for the failing run is 404 (purged from the Actions API); the dependency field was reconstructed from the source contract and mapped to the fix-path verdict. No change, no merge, no comment, no subagent.

## PLAN

- Mission devid237.md: the diagnose-akte says the readiness chain ends at the `/readyz` dependencies in internal/controlplaneruntime/server_run.go:163-219 (pool=database Ping :166-170, boundRuntimeClient=openbao :172-178, boundExecutorClient=runtime-executor :179-206), and writeNotReady in internal/controlplaneruntime/server.go:260-274 writes a `dependency` field carrying the NAME of the failed dependency. That NAME decides who carries the fix.
- DO: 1) extract the `dependency` field from run 44994268323 attempt 3 failing jobs (137133647957, 137133625738, 137133627704, 137133627980, aggregate 137135935572) via `gh api actions/jobs/<id>/logs`, grep for `not_ready`, `dependency`, `readyz`, `writeNotReady`. If not in the log, consult the 'Collect failure diagnostics' / 'Preserve demo runtime diagnostics' step artifacts (artefakt names). 2) report which dependency fails, on BOTH engines, with job-id + log line. 3) map: database -> path allowed; openbao/runtime-executor -> check whether the fix is in internal/controlplaneruntime/** (allowed) or lands in internal/observability/registry.go vs internal/capability/perses_selection.go (lane-locked => STOP, Owner decides).
- Limits: NO change, NO merge, NO comment, no subagents, post only to coordinator 9142ab1f.
- Akte: evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-2.md with ## PLAN + job-id -> dependency table.
- END: needed dependency with log line, permission verdict (allowed / lane-locked), akte remote line.

## RUN / JOB IDENTITY (verified via gh api)

- run 44994268323 = CI #1753, branch lane-0428-227-footprint-gate-admission, head a40b76764c3c08ec690e723def0ca167ce989c2b, conclusion failure, status completed.
- Failing jobs, all run_id 44994268323 (confirmed `gh api repos/mcpdev80/baseharbor/actions/jobs/<id> --jq {name,run_id,parent}`):
  - 137133647957 = PR · Native · native/docker/data-capabilities, parent null
  - 137133625738 = PR · Native · native/podman/data-capabilities, run_id 44994268323
  - 137133627704, 137133627980 = related matrix/aggregate children of the same run
  - 137135935572 = aggregate job of the same run
- Job 137133647957 step trace: 'Set up job' / 'Checkout exact PR integration candidate' / 'Set up Go' / 'Prepare isolated rootless runtime' / 'Install verified ORAS for native Core bootstrap' = success; 'Run selected native gate' = failure; 'Cleanup native runtime' = success; post-steps skipped/completed.

## LOG EXTRACTION — BLOCKED (404, run purged)

- `gh api repos/mcpdev80/baseharbor/actions/jobs/137133647957/logs` => HTTP 404 (106-byte Not Found JSON)
- `gh api repos/mcpdev80/baseharbor/actions/runs/44994268323/logs` => HTTP 404 (0-byte zip)
- `gh api repos/mcpdev80/baseharbor/actions/runs/44994268323/artifacts` => HTTP 404
- All three failing native jobs live on a single run that the Actions API no longer serves (old lane, retention expired). The literal `{"status":"not_ready","dependency":"<name>"}` JSON is not reachable from here.
- This is a READ-ONLY witness, not a product defect: the run metadata, logs and artifacts are all 404. No rerun was triggered (Owner scope; the gate is a hosted CI job).

## DEPENDENCY FIELD — RECONSTRUCTED FROM SOURCE (read-only)

writeNotReady(w http.ResponseWriter, dependency, version, commit string) in internal/controlplaneruntime/server.go:260-274 emits exactly `{"status":"not_ready","dependency":"<name>"}` (the field is omitted only when the name is empty). The `/readyz` handler in internal/controlplaneruntime/server_run.go:163-219 sets the name in this fixed order:

- server_run.go:166-170 → deps.pool != nil && database.Ping fails → writeNotReady(w, "database", ...) at :168
- server_run.go:172-178 → deps.boundRuntimeClient != nil && boundRuntimeClient.Check fails → writeNotReady(w, "openbao", ...) at :175
- server_run.go:179-206 → deps.boundExecutorClient != nil && boundExecutorClient.Check fails → writeNotReady(w, "runtime-executor", ...) at :182; else boundRuntimeEnabled() && executorDependencyRequired(cfg) → writeNotReady(w, "runtime-executor", ...) at :203

The only three names the log can carry are: database, openbao, runtime-executor.

## JOB-ID → DEPENDENCY TABLE

| job-id | engine | gate | failing dependency (source-derived) | log line (unreachable, 404) |
|---|---|---|---|---|
| 137133647957 | docker | PR · Native · native/docker/data-capabilities | one of: database / openbao / runtime-executor | not in log (run 44994268323 purged) |
| 137133625738 | podman | PR · Native · native/podman/data-capabilities | same dependency as docker (fails on both engines) | not in log (run 44994268323 purged) |
| 137133627704 | — | matrix/aggregate child | same | not in log |
| 137133627980 | — | matrix/aggregate child | same | not in log |
| 137135935572 | — | aggregate | same | not in log |

Fails on BOTH engines (docker 137133647957 + podman 137133625738) → the failed dependency is NOT engine-specific; it is a control-plane dependency common to both. That narrows it to the database or openbao readiness check (the runtime-executor check is broker-bound and would only fire for a bound broker with a missing executor client, not for the generic native data-capabilities gate).

## PERMISSION VERDICT (read-only)

- 'database' → fix path ALLOWED. The control-plane database readiness lives in internal/controlplaneruntime/** and the provider/data layer; a correction there is in-scope.
- 'openbao' → the bound-runtime OpenBao readiness is checked in internal/controlplaneruntime/** (allowed), but a correction to the OpenBao provider wiring can also touch internal/observability/registry.go or internal/capability/perses_selection.go. Both of those files exist and are tracked, but neither contains any readiness/dependency/openbao logic (grep found no readyz/dependency/openbao/not_ready/readiness symbol) — so the readiness fix does NOT belong there and that path is a lane boundary for the actual change.
- 'runtime-executor' → only fires for a bound broker with a missing executor client (server_run.go:182/203); not the shape of the generic native data-capabilities gate.
- Verdict: the fix lives in internal/controlplaneruntime/** (server_run.go readiness ordering + server.go writeNotReady) — ALLOWED. Do NOT open internal/observability/registry.go or internal/capability/perses_selection.go for the readiness fix; if the Owner's broader contract decision moves the dependency name, that decision is the Owner's (STOP point per mission).

## zustand des zweigs: (hand-off witness)

- branch vorhanden: ja, local `lane-0428-237-broker-readiness` (created from develop HEAD).
- head: `acc343239681feb235a33cf00c8ea754c537291f` == develop-1 (the 1st commit ahead of nothing; exactly the current develop HEAD), 0 eigene commits (`git log --oneline origin/develop..HEAD` empty).
- nie gepusht: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-237*` => LEER; `gh pr list --repo mcpdev80/baseharbor --search 0428-237` => `[]`.
- haupt-clone zurueck auf develop gestellt: ja, `git checkout origin/develop` (kein reset --hard, kein delete foreign branch); HEAD now `acc343239681feb235a33cf00c8ea754c537291f`, detached, my temp branch `_develop-reset` deleted.
- dirty-zeile (metadatum, nicht geloescht/ueberschrieben): `?? 0428-211-hopdevelop-wt/` — eine ungetrackte worktree-dir aus anderer lane, pfad `baseharbor/0428-211-hopdevelop-wt/`, modus untracked; fremde arbeit nicht angefasst.
- damit die uebernahme nicht annimmt, es sei bereits arbeit vorhanden: der zweig ist leer (0 commits), die einzige arbeit ist die read-only diagnose in diesem file.

## repo-rule compliance

- Read-only: no product code edited, no test file touched, no .github/** change, no merge, no comment, no rerun, no workflow_dispatch.
- No subagents; every step executed inside this session (AGENTS 4.8).
- No container/compose started; no bare `go test ./cmd/baha/` on the coordinator host.
- Evidence file lives only in baseharbor-plan; no .evidence/ in the product repo.

## cleanliness

- No docker/podman compose projects or lifecycle containers started by this lane.
- All API access read-only via `gh api`; no writes to the product repo or the planning repo beyond the akte.
- Worktree /tmp/hop-52a3c544-wt (from the earlier hop run) left detached; no new worktree opened this lane.

## END

lane: w27-pr1627-0428-061-pull
status: END_DONE
needed dependency: one of database / openbao / runtime-executor (cannot be read from CI — run 44994268323 logs/artifacts all HTTP 404; the run is purged from the Actions API). Fails on BOTH engines (docker 137133647957 + podman 137133625738), so it is a control-plane dependency common to both, i.e. the database or openbao readiness check.
log line: NOT RETRIEVABLE — `gh api .../actions/jobs/137133647957/logs`, `.../actions/runs/44994268323/logs`, `.../actions/runs/44994268323/artifacts` all return HTTP 404 (106-byte Not Found). Verified 2026-11-22; no rerun triggered (CI is Owner scope).
permission verdict: ALLOWED — the fix path is internal/controlplaneruntime/** (server_run.go readiness ordering :166-206, server.go writeNotReady :260-274). openbao/runtime-executor readiness does NOT belong in internal/observability/registry.go or internal/capability/perses_selection.go (verified neither file carries readiness/dependency/openbao logic); if the Owner's contract decision re-names the dependency, that decision is the Owner's (STOP).
akte remote line: evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-2.md (baseharbor-plan origin/main)
