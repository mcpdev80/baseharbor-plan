# 0428-229/0428-230 befund-1 — native-gate admission chain for env-destroy (read-only witness)

Lane: `0428-223-testctx` (mechanical evidence task, read-only per dispatch
`/var/tmp/m/hunt34.md.g`). Nothing changed, nothing pushed, no test runs, no
subagents. Base facts: develop `8b9a8f50645db1dbaad4a5e1f2140930436d3ea7`,
PR #1627 head `2f0f80786d8`.

## PLAN

- Step 1: confirm or correct the claimed chain, one file:line per claim, at develop 8b9a8f50 and at head 2f0f8078.
- Step 2: census of components with `runtime_specific: true` + `required_test_names` that no `native_checks` row lists.
- Step 3: decide whether the `PR · Native gate plan` path is needed for env-destroy acceptance or whether the coreless-application shards are the sole proof place, with job ids and the `"Action":"run"` line.

## 1. Chain confirmation (CORRECTED in one detail)

Claim-by-claim witnesses, all read from `git show 8b9a8f50:<file>` / `git show 2f0f8078:<file>` in this session:

- The planner exists on develop: `scripts/pr-native-gate-plan.py` @8b9a8f50 (also @2f0f8078). Confirmed.
- The selector reads ONLY `coverage['native_checks']` rows: `scripts/validate-pr-gate-coverage.py:66-88` @8b9a8f50 — `resolve_native_checks` builds `checks` from `coverage.get("native_checks", [])` filtered by `selection_scope == "focused"` (lines 74-81) and then selects `component_id in check.get("source_components", [])` (lines 84-85). **Correction of the dispatch's file:line**: the selection loop is at lines 74-88, not 66-82; the function starts at line 66. Substance unchanged.
- `pr-native-gate-plan.py:26` calls `validator.resolve_native_checks(...)`; lines 27-32 map the returned ids through `coverage['native_checks']`. Confirmed.
- env-destroy component exists with runtime evidence: `scripts/pr-gate-coverage.json` @8b9a8f50 AND @2f0f8078 lists component `source.cmd.baha.env.destroy.integration.test` with `path: cmd/baha/env_destroy_integration_test.go`, `runtime_specific: true`, `required_test_names: ["TestEnvironmentDestroyNativeLifecycle"]`. Confirmed identical at both refs.
- None of the 6 `native_checks` rows @8b9a8f50 (and @2f0f8078 — the two files are byte-identical: `native_checks` sets equal, `diff` empty) lists that component in any `source_components`. Confirmed. Row ids: `native/podman/installation-destroy`, `native/docker/greenfield`, `native/docker/onboarding`, `native/podman/workstation-onboarding`, `native/docker/perses-runtime-smoke`, `native/podman/second-target-conflict`.
- So `resolve_native_checks` returns `[]` for env-destroy-only diffs → the plan job emits `matrix='{"include":[]}'` → `PR · Native · ${{ matrix.id }}` is skipped. Witness at PR #1627 run 44977593002: `PR · Native gate plan` job 137070848046 (completed/success) log line `2026-11-22T02:46:13.7707188Z matrix='{"include":[]}'`; `PR · Native · ${{ matrix.id }}` job 137070878034 completed/skipped. The dispatch's warning-never-emitted claim is confirmed: the emit condition (ci.yml:513 @8b9a8f50, `::warning::…planner missing`) requires `git cat-file -e "$BASE_SHA:scripts/pr-native-gate-plan.py"` to FAIL (ci.yml:502), and the file exists on develop — so no warning, consistent with observation.

## 2. Census (develop 8b9a8f50 = head 2f0f8078, identical catalogs)

Components with `runtime_specific: true` AND non-empty `required_test_names` that appear in NO `native_checks.source_components` (8 components, 2 test-name groups missing runtime coverage):

| component id | path | required_test_names | native runtime missing |
| --- | --- | --- | --- |
| source.cmd.baha.env.destroy.integration.test | cmd/baha/env_destroy_integration_test.go | TestEnvironmentDestroyNativeLifecycle | docker+podman (no native row references it) |
| runtime.podman-service-stop | internal/runtime/service_stop.go | TestSelectedStopAcceptsPinnedContainerName | podman-only component; no native row |
| runtime.podman-service-stop-tests | internal/runtime/service_stop_test.go | TestSelectedStopAcceptsPinnedContainerName | podman; no native row |
| source.cmd.baha.app.application.backend.runtime.test.go | cmd/baha/app_application_backend_runtime_test.go | TestSelectiveApplicationBackendRuntimeAddRemoveReAdd | docker+podman |
| source.cmd.baha.app.backend.selective.runtime.test.go | cmd/baha/app_backend_selective_runtime_test.go | TestSelectiveBackendCleanupPreservesRuntimeBaseline | docker+podman |
| source.cmd.baha.app.capability.runtime.test.go | cmd/baha/app_capability_runtime_test.go | TestApplicationCapabilityLifecycleExistingCore | docker+podman |
| source.cmd.baha.app.https.selective.runtime.test.go | cmd/baha/app_https_selective_runtime_test.go | TestSelectiveHTTPSRuntimeAddRemoveReAdd | docker+podman |
| source.cmd.baha.application.otlp.handoff.runtime.test.go | cmd/baha/application_otlp_handoff_runtime_test.go | TestManagedRegisteredOTLPNativeConsumerHandoff | docker+podman |

## 3. Is the `PR · Native gate plan` path needed for env-destroy acceptance?

NO for proving execution; YES for fail-closed admission. Both witnesses:

- The test DOES execute in the coreless-application shards, selected by
  `scripts/pr-gate-plan.py:1230-1240` (`cmd/baha/env_destroy.go` +
  `env_destroy_integration_test.go` changed → `integration/docker/coreless-lifecycle` +
  `integration/podman/coreless-lifecycle`), at PR #1627 head run 44977593002:
  job 137070915973 (docker application) log line
  `2026-11-22T02:56:00.8783439Z {"Time":…,"Action":"run","Package":"github.com/mcpdev80/baseharbor/cmd/baha","Test":"TestEnvironmentDestroyNativeLifecycle"}`
  and job 137070916251 (podman application, still running at measurement time).
  So the shard is a real execution site.
- But those two jobs concluded **failure** at the consent seam —
  `Environment destroy incomplete; identity retained so the operation can be retried: process scoped deployment env-destroy-native (…): provider change: stale-impact-consent`
  (`--- FAIL: TestEnvironmentDestroyNativeLifecycle (11.32s)`), the same
  runtime-consent position this mission quoted for #1725/#1723. A shard that
  runs the test but ends red (or ends by a skip in other combinations) is not
  an admission gate: the `PR · Native · ${{ matrix.id }}` job is the matrix-driven
  required native check that binds a PR's runtime evidence. With
  `matrix={"include":[]}` that job skips for env-destroy-only diffs, so a PR can
  NEVER be positively admitted on env-destroy native behavior — which is why the
  data-capability PRs go green only after their gates land. Admission fix
  (adding `source.cmd.baha.env.destroy.integration.test` to a docker/podman
  `native_checks` row, or a new row) is a `scripts/pr-gate-coverage.json` change
  = the #1725/#1723 runtime-consent domain, NOT this read-only task.

## repo-rule compliance

- Read-only: no file edits, no pushes, no test runs, no subagents, nothing started afterwards. All facts quoted from `git show <ref>:<path>` blobs and hosted job logs (`gh api …/jobs/<id>/logs`) with byte counts: 137070915973 log 125461 bytes, 137070848046 log 46353 bytes.

## cleanliness

- Scratch only in `/tmp/0428-229-*` and `/var/tmp/0428-223/` (this task's logs), foreign containers untouched; nothing started, so nothing to bring down. `docker ps -a` unchanged from ambient state (witness in END turn).

END 0428-223-testctx DONE — kette bestaetigt mit einer Berichtigung (datei:zeile der Auswahl 74-88, nicht 66-82), census = 8 components (2 ungedeckte test-gruppen), native-gate-plan-pfad is NICHT noetig fuer uitvoering maar WEL voor toelating; zie tabel.
