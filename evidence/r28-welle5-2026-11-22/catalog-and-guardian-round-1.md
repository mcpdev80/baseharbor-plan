# 0428-242 - Catalog + fail-loud PR gate guardian (round 1)

Card 0428-242, Owner-approved `scripts/**` scope. Session ffe7611b. Combined (A) catalog
entry and (B) fail-loud guard for uncataloged source changes.

## PLAN

1. Add catalog entry for `cmd/baha/app_broker.go` to `scripts/pr-gate-coverage.json`
   (id `source.cmd.baha.app.broker.go`, two `data.capabilities` surfaces) + its test file,
   resolving to the atomic data-capabilities gate.
2. Add the fail-loud guard: a changed source component (cmd/ or internal/) with no declared
   catalog owner aborts the planner with exit != 0 (never an empty/gray matrix that passes),
   naming the missing catalog id/path and the exact next action.
3. Extend `scripts/test_pr_gate_coverage.py` with both cases (cataloged -> resolved,
   uncataloged -> exit != 0 with precise spec) and register the suite in
   `scripts/test_pr_gate_plan.py` (CI pr-planner-tests job) so it runs directly by CI.
4. Update tests that encoded the OLD soft-behavior (uncataloged -> broad fallback false-pass)
   to assert the new fail-loud contract.
5. Publish evidence, report CI job + trigger, and the #1763 handoff line.

## katalog:

- Added `source.cmd.baha.app.broker.go` to `scripts/pr-gate-coverage.json`:
  `{"id":"source.cmd.baha.app.broker.go","path":"cmd/baha/app_broker.go",
  "surfaces":["source.gate.atomic.docker.data.capabilities",
  "source.gate.atomic.podman.data.capabilities"]}`.
- app_broker.go is a runtime-broker lifecycle/observability file (imports runtimebroker,
  openbao, objectstorage, observability) — NOT a Keycloak/core production path. Keycloak/core
  lives in internal/coreinstallation/stableid/serviceaccess/installauthority, untouched by
  app_broker.go. So NO Keycloak/core surface was added; the two data.capabilities surfaces
  match the existing app_apply.go pattern.
- Catalog still validates clean (`python3 scripts/validate-pr-gate-coverage.py` exit 0).
- resolve_covered_gates(["cmd/baha/app_broker.go"]) -> selected ["atomic/docker/data-capabilities"],
  unresolved [].
- Did NOT change app_broker.go, control_plane, runtime, or any .github file.

## waechter:

- Added `unresolved_source_error(unowned)` to scripts/validate-pr-gate-coverage.py. The
  fail-loud message names the uncataloged path, its derived source.* catalog id, the two
  data.capabilities surfaces, and the exact next action ("add this source ... to
  scripts/pr-gate-coverage.json, e.g. {...}").
- Wired into scripts/pr-gate-plan.py plan(): for each uncataloged path under cmd/ or
  internal/, raise ValueError before the catalog resolves. docs/release pins and other
  legacy-handled paths stay out of this guard.
- End-to-end: an uncataloged internal/runtime path -> planner raises, exit 1, message names
  path + next action. A cataloged app_broker.go path -> resolved, selected
  atomic/docker/data-capabilities, broad go-unit/vet/build fallback checks.

## test:

- Added 3 cases to scripts/test_pr_gate_coverage.py:
  test_app_broker_catalog_entry_resolves_to_data_capabilities_gates (catalog entry exists,
  resolves, not empty/gray), test_planner_catalogs_app_broker_as_resolved (planner resolves),
  test_uncataloged_source_is_rejected_with_precise_next_action (exit != 0, message names
  path + scripts/pr-gate-coverage.json + derived id + surface).
- Registered the suite in scripts/test_pr_gate_plan.py via
  PRGateCoverageGuardianDiscoveryTests.test_coverage_guardian_suite_runs, which loads and
  executes test_pr_gate_coverage.py. This runs directly by CI in the pr-planner-tests job
  (ci.yml: "python3 -m unittest scripts/test_pr_gate_plan.py
  scripts/test_pre_release_runtime_reuse.py"). No .github change needed.
- Updated tests that encoded the OLD soft-behavior to the new fail-loud contract:
  test_unreviewed_runtime_file_is_rejected_not_falled_back,
  test_unknown_source_is_rejected_not_falled_back,
  test_runtime_hint_without_catalog_owner_is_rejected,
  test_unknown_product_is_rejected_not_falled_back (test_pr_ci_fallback.py),
  test_broad_fallback_subsumes_only_identical_small_go_checks,
  test_broad_fallback_keeps_broad_go_checks_for_cataloged_cli_source,
  test_legacy_base_fallback_passes_broad_checks_when_candidate_adds_new_vocabulary.
  test_known_docs_remain_targeted_and_unknown_metadata_does_not_boot_runtimes,
  test_v0427_demo_pin_uses_only_exact_source_validation,
  test_v0427_demo_pin_rename_or_mixed_change_stays_conservative,
  test_uncataloged_source_is_rejected_by_the_planner_cli.
- 63 tests green across test_pr_gate_coverage, test_pr_native_gate_plan, test_pr_ci_fallback.
- CI job/trigger: pr-planner-tests job runs test_pr_gate_plan.py (which now self-runs the
  coverage guard suite); pr-focused source-regression job runs test_pr_ci_fallback.py. Both
  trigger on pull_request draft=false, base develop/lane-/cli2-/w0. No .github edit.

## erwartung #1763:

- Follow-up PR #1763: the catalog surfaces for app_broker.go (the two data.capabilities)
  should be confirmed against the real lifecycle/observability gate owner; if a dedicated
  runtime-broker gate exists, bind app_broker.go (and its test file) to that gate instead
  of the generic data-capabilities gate. No change required before #1763.
- Card 0428-237 (Codex Runner 0428-237) owns the app_broker.go content and control_plane/
  runtime changes; this card only added the catalog entry and the fail-loud guard.

## GRENZEN

- Only scripts/** + their tests changed. No .github, no app_broker.go content, no
  control_plane/runtime files, no internal/product changes. No amend/force, no merge/
  comment, no subagents.
- baseharbor branch: lane-0428-242-catalog-guardian, cut from develop 8629450ef3c5198bb675331c12f56b2c9377aa1c,
  origin/develop ancestor of HEAD.
- CI run: <to fill with run-id + terminal status + failed count>.
