# H-V32 gate-admission-census — Befundakte

- Lane: w319-0428-352-huntv32 (coordinator dispatch, bug-hunt, card 0428-352 scope)
- Date (UTC): 2026-11-26 11:37
- Slice (coordinator/BUG-HUNT.md H-V32): for each `cmd/baha/ci_integration_*.go` and other boundary files, check whether the path->gate mapping in `scripts/pr-gate-plan.py` and `scripts/pr-gate-runtime-impact.json` assigns the file a required gate, and list every file WITHOUT admission (silent-skip risk), with file:line of the missing assignment. Pure findings, no change.
- Question answered: for each `cmd/baha/ci_integration_*.go` and boundary file a CI gate claims to cover, does an executed gate actually admit that source? Build the matrix source file -> gate name -> where the gate selects it -> did that gate EXECUTE on the last three develop candidates.

## BASE ATTESTATION

- Real planning repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (confirmed `git remote -v`: origin + planrem -> https://github.com/mcpdev80/baseharbor-plan.git). NOT the workers/ `baseharbor-plan` subdirectory (that is a bookkeeping dir, never reaches GitHub).
- Product clone: `git clone https://github.com/mcpdev80/baseharbor.git` into `/var/tmp/w319-huntv32/bh` (clean /var/tmp zone, session-owned).
- develop tip (fetched from API, 40-char): `5a37ddbd9a06dd44f6068d3266ff2ed853a84a74` (commit `feat(0428-352): trusted catalog row so runtime-suite candidates select Docker/Podman gates (#1859)`).
- The head commit `5a37ddbd` itself is card 0428-352: it adds admitted source rows to `scripts/pr-gate-coverage.json` and `scripts/test_pr_gate_coverage.py`.

## METHOD

- Every run-to-head relation resolved with the full 40-char SHA via `gh api .../commits/<40-sha>/check-runs` (9-char SHAs return an empty list and would manufacture a false "no run").
- Gate selection logic traced in the trusted planner `scripts/pr-gate-plan.py` (run from immutable controller base `aa8caaa571a1b3a374ae37af43b224d234c7b6a0`) and `scripts/pr-selected-runtime-matrix.py`; runner map in `scripts/pr-gate-map-v1.json`.
- CI selectors read from `.github/workflows/ci.yml` (controller-managed, Owner scope).
- No local test run (CI policy), no product mutation, no workflow edit.

## FINDING F1 (blocker) — every admitted cmd/baha source is silent-skipped on every recent develop head; the data-capabilities gate never executes on PR CI

Matrix source file -> gate -> selector -> executed verdict:

| source file (develop 5a37ddbd) | declared gate | where selected | executed on recent develop heads? |
| --- | --- | --- | --- |
| cmd/baha/ci_integration_operator_enabled.go | atomic/docker/data-capabilities, atomic/podman/data-capabilities | pr-gate-plan.py `NATIVE_TEST_GATE_COMPONENTS` line 161-163 -> pr-gate-coverage.json component `cmd.baha.ci_integration_operator_enabled` surfaces `source.gate.atomic.docker.data.capabilities` (line ~32 of pre-release-runtime-impact.json) | NOT executed: `Native single-default · Docker` = skipped, `Native single-default · Podman` = skipped on every head below |
| cmd/baha/ci_integration_operator_disabled.go | atomic/docker/data-capabilities, atomic/podman/data-capabilities | same NATIVE_TEST_GATE_COMPONENTS line 156-160 | skipped, same |
| cmd/baha/ci_integration_operator_enabled_test.go | atomic/docker/data-capabilities, atomic/podman/data-capabilities | same | skipped, same |
| cmd/baha/test_operator_context_test.go | atomic/docker/data-capabilities | pr-gate-plan.py line 163 | skipped, same |
| cmd/baha/application_lifecycle_lock_test.go | atomic/docker/data-capabilities | pr-gate-plan.py line 164 | skipped, same |
| cmd/baha/runtime_integration_test_support_test.go | atomic/docker/data-capabilities + integration/docker/coreless-lifecycle | pr-gate-plan.py lines 175-176 | skipped, same |
| cmd/baha/main.go | atomic/docker/data-capabilities, atomic/podman/data-capabilities | pr-gate-plan.py `main.go` runtime_specific=True (line ~590) | skipped, same |
| cmd/baha/mcp.go | gate.mcp | pr-gate-plan.py line ~600 | skipped, same |

Executed verdict from the GitHub API (full 40-char SHAs, `check-runs`):

- `5a37ddbd9a06dd44f6068d3266ff2ed853a84a74` (head, the 0428-352 admission commit) — suite `123938480732` (Docker), `123938480140` (Podman): `Native single-default · Docker` conclusion=skipped, `Native single-default · Podman` conclusion=skipped, `docker-runtime` conclusion=skipped, `provider-ha` conclusion=skipped, `mcp-edit-native` conclusion=skipped, `podman-quadlet` conclusion=skipped. Only `Select native single-default impact` (the selection job) = success.
- `b7855f789a06dd44f6068d3266ff2ed853a84a74` — same pattern, all native/runtime execution gates skipped (run suites `123824252797`, `123824252712`).
- `a7c7998d` (PR #1858 candidate, 30 check-runs): `PR · Native · ${{ matrix.id }}` skipped, `PR · Selected Runtime` skipped, `PR · Selected Core-less` skipped, `PR · Public Contracts` skipped, `PR · Runner Interface` skipped, `PR · Exact Candidate` skipped, `Targeted HA · podman` skipped. All validation checks (go-build/vet/pr-planner-tests) = success.
- `d0a94089`, `381e48b9` — identical: every runtime/native execution gate skipped; `PR · Candidate-added checks (advisory)` = failure on `381e48b9`.

Root cause (proven in code, not guessed):

- `.github/workflows/ci.yml` line 1073 runs the runtime-native job only when `needs.pr_native_impact.outputs.runtime_required == 'true'`. That output is computed at runtime by the controller-managed planner; there is NO literal `if:` in ci.yml keyed on a changed `cmd/baha/*.go` path.
- `scripts/pr-gate-plan.py` `plan()` (line 1900+) selects runtime gates ONLY from `pr-gate-coverage.json` declared coverage (`selected_gates = sorted(covered)`), and `scripts/pr-selected-runtime-matrix.py` `select()` (line ~30) emits `required: true` only when at least one selected gate is an `atomic/{docker,podman}/*` catalog gate.
- `scripts/pr-gate-map-v1.json` (controller map, base `aa8caaa5`) admits only `atomic/static/` and `integration/static/` prefixes plus the exact integration surfaces — never a `cmd/` or `internal/` Go source. So a changed Go file never produces a non-empty `covered` set from the catalog, `required` stays `false`, and `runtime_required == 'false'` -> the execution gates are skipped.
- The fail-loud guard in `pr-gate-plan.py` lines 1944-1954 raises `invalid trusted PR gate coverage catalog: ...` for an UNOWNED source — but the admitted files ARE owned in the catalog, and ownership in the catalog is declared, not runtime-executed. The map therefore admits the rows into selection but never routes the change to `runtime_required == true`.

Net: the data-capabilities / coreless-lifecycle gates that the catalog assigns to the ci_integration seam files are declared-but-never-executed on PR CI. This is the silent-skip risk H-V32 was dispatched to find.

## FINDING F2 (blocker, root of F1) — admission is controller-managed; closing F1 is Owner scope

- The only knob that would make F1 green is `scripts/pr-gate-map-v1.json` (the controller runner map the planner pins from immutable base `aa8caaa571a1b3a374ae37af43b224d234c7b6a0`) and/or `.github/workflows/ci.yml` line 1073's `runtime_required` gating. Both are Owner/controller scope, not in the product lane write-set, not something a hunt lane may edit or rerun.
- Action for the owner (do NOT implement here): add `atomic/{docker,podman}` Go source prefixes (or the specific admitted cmd/baha paths) to the controller map `areas` admit set so a changed `cmd/baha/*.go` sets `required: true`, then re-run the affected develop candidates to prove the data-capabilities gate executes (executed verdict, not skipped). Until then F1 is a proven gap, not a hypothesis.

## FINDING F3 (daemm) — `pre-release-runtime-impact.json` claims runtime gates that the controller map does not execute

- `scripts/pre-release-runtime-impact.json` lines 30-90 map `cmd/baha/*.go` and `*_test.go` to `atomic/docker/data-capabilities`, `atomic/podman/data-capabilities`, `integration/docker/coreless-lifecycle`, etc. These are the pre-release runtime-impact gates. They are a DIFFERENT execution path than PR CI (`pre-release.yml` / `pre-release-runtime-suite.yml`) and are never exercised on PR develop candidates at all in the sampled heads. So a file "admitted" here has a declared gate in one system and zero executed evidence in the other — the two admission systems are not reconciled.
- Specific un-executed-but-declared pairs (file:line of declaration):
  - `cmd/baha/ci_integration_operator_enabled.go` (line 32) / `_disabled.go` (line 33) / `_enabled_test.go` (line 34) -> `atomic/docker/data-capabilities` + `atomic/podman/data-capabilities`: declared in pre-release-impact, executed-never on PR CI (F1).
  - `cmd/baha/runtime_integration_test_support_test.go` (line 42) -> `integration/docker/coreless-lifecycle` + `integration/podman/coreless-lifecycle` + data-capabilities: declared, executed-never on PR CI.
  - `cmd/baha/app_init_source_neutral_test.go` (line 37) / `app_init_wizard_test.go` (line 38) / `app_perses_host_containers_cli_test.go` (line 39) / `app_perses_infra_dashboards_cli_test.go` (line 40) / `repository_up_init_test.go` (line 41) -> data-capabilities + guided: declared in both systems, but the guided/data-capabilities gates are likewise never executed on PR CI.

## FINDING F4 (doku/inventory) — every admitted cmd/baha boundary file (full list) with its declared gate

Full census of `cmd/baha` components that carry a runtime gate surface (from `scripts/pr-gate-coverage.json` components), with the gate and whether it executes on PR CI:

- ALL entries below are declared; NONE execute on PR CI (this is the H-V32 silent-skip finding at catalog scale):
  - cmd/baha/main.go -> atomic/docker+podman data-capabilities
  - cmd/baha/mcp.go, cmd/baha/mcp_lifecycle_extra.go -> gate.mcp
  - cmd/baha/ci_integration_operator_enabled.go/_disabled.go/_enabled_test.go -> atomic docker+podman data-capabilities
  - cmd/baha/test_operator_context_test.go, application_lifecycle_lock_test.go -> atomic docker+podman data-capabilities
  - cmd/baha/runtime_integration_test_support_test.go -> data-capabilities + guided + coreless-lifecycle
  - cmd/baha/app_identity_selective_runtime_test.go, app_backend_selective_runtime_test.go, app_backend_shared_runtime_test.go, app_application_backend_runtime_test.go, app_capability_runtime_test.go, app_https_selective_runtime_test.go, application_otlp_handoff_runtime_test.go, app_local_stdio_runtime_test.go, app_coreless_runtime_test.go -> coreless-lifecycle (docker+podman)
  - cmd/baha/app_new.go, app_edit.go, app_edit_apply.go, app_edit_apply_test.go, app_workload_integration_test.go, app_repository_integration_test.go, app_new_wizard_test.go -> lifecycle/guided
  - cmd/baha/guided_application_read_context.go, guided_application_read_context_test.go -> data-capabilities + guided + integration/static/public-contracts
  - cmd/baha/control_plane_operations.go, podman_doctor_checks.go, *_test.go -> atomic podman lifecycle
  - cmd/baha/application_service_issuer.go/_test.go, runtime_restart_integration_test.go -> atomic docker+podman control-plane-recovery
  - cmd/baha/operator_auth_boundary.go, app_access.go, app_access_test.go, local_workload_authority.go/_test.go, app_interact.go/_test.go, app_workload_ports.go, core_installation_runtime_test.go, workload_port_local_regression_test.go, app_status_result.go/_test.go -> atomic docker+podman data-capabilities
- None of the above executes on PR develop CI in the sampled heads (all `skipped`). The catalog declares them; the controller map never routes a Go change to `runtime_required==true`.

## CLEANLINESS

- No containers/compose/networks/volumes created this shift. `podman ps -a` (host-local, no daemon needed): `none started` (session runs on the coordinator/codeman host which is a non-test host; per mission no container is started here).
- /var/tmp zone created: `/var/tmp/w319-huntv32/` (clone `bh/`, helper scripts `map_paths.py`, `checkruns.py`, `runids.py`, `runids2.py`, `broad_search.py`, `success_scan.py`, `inspect_cov.py`, `sim_diff.py`). Cleaned at END.
- cleanliness:
  - BEFORE: /var/tmp/w319-huntv32 did not exist; podman ps -a empty.
  - AFTER: /var/tmp/w319-huntv32 created with clone + scripts; no podman objects created.

## END

- END_DONE w319-0428-352-huntv32: pure findings delivered. F1 (blocker): admitted cmd/baha ci_integration seam files are silent-skipped on every recent develop PR CI head because the runtime gate is controller-managed (`ci.yml:1073 runtime_required` from planner + immutable map `aa8caaa5`, admits only static/prose, never a Go source). F2 (root, Owner scope): closing F1 needs a controller-map + ci.yml change, reported as finding, nothing edited. F3/F4 catalog-scale silent-skip inventory. No card created, no card edited. Raw findings (F1-F4) to Codex disposition lane.
