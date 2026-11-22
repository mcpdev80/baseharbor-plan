# 0428-242 - Catalog + fail-loud PR gate guardian, fix on develop for #1768 (round 1)

Card 0428-242, Owner role-switch directive 22.11. This card owns the ONE bottleneck: PR #1768
(0428-242) must land its catalog + fail-loud on develop before card 0428-237 (#1770) can open
its skipped native matrix. Session ffe7611b. Round 1 of the develop fix.

## PLAN

1. Recover a clean branch: confirm origin/develop ancestor, cut lane-0428-242-catalog-guardian
   from develop 8629450ef3c5198bb675331c12f56b2c9377aa1c, only scripts/**, no .go product
   changes, no .github.
2. Fix the ci-executor-tests break: test_reviewed_cli_candidate_resolves_under_v0427 used the
   uncataloged internal/openbao/bootstrap.go (aborts exit != 0 under the new guard). Switch it
   to the cataloged internal/openbao/bootstrap_auth.go and assert the correct new resolution
   (atomic/docker/control-plane-recovery).
3. Rebase #1768 onto develop 64eab13e2 so the branch carries #1766's assertion fix. This also
   resolves the native TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork message mismatch
   that develop HEAD already fixed (test expects "no verifiable protected Core", product says
   "has no verifiable protected Core").
4. Verify the fail-loud contract end to end: uncataloged source aborts exit != 0 with path +
   catalog id + exact next action; cataloged app_broker.go resolves.
5. Trigger one terminal CI run on the rebased branch, record run-id + terminal status + failed
   count + the four job witnesses.

## native-keycloak-core-vor-rebase vs nach-rebase:

VOR rebase (branch head b986dfb07, base develop 8629450ef):
- Native Keycloak/Core docker + podman (run 45022626810, job 137208721156) FAILED:
  TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork failed. Test asserted substring
  "existing native network lacks a protected Core or shared backend owner" but product
  (cmd/baha/core_network_binding.go:71) returns "existing native network has no verifiable
  protected Core or shared backend owner". Mismatch because the branch carried a stale test
  from an earlier develop fork.
- ci-executor-tests FAILED: test_reviewed_cli_candidate_resolves_under_v0427 used uncataloged
  internal/openbao/bootstrap.go -> fail-loud raised ValueError exit 1.
- pr-planner-tests: runner-context tests fixed (cataloged CLI source), but v0427 still broken.

NACH rebase onto develop 64eab13e2 (run 45025980169):
- Native Keycloak/Core jobs SKIP (owner_node_required not set for this lane PR; correct - the
  gate only opens for the release candidate). The develop HEAD test matches develop HEAD product;
  the message mismatch is resolved by inherit, not by a product edit.
- ci-executor-tests: 18 suites executed, 0 failed.
- pr-planner-tests: executed, 0 failed.
- Run 45025980169 conclusion=success, status=completed.

## ci-executor-registrat: scripts/ci-native-pr-gate.sh = ci-executor

The catalog (scripts/pr-gate-coverage.json) records scripts/ci-native-pr-gate.sh as a
ci-executor source. With the live release (v0.4.27) this lets the native Keycloak/Core matrix
resolve instead of the fail-loud guard aborting on an unowned source. The fail-loud guard
(source_unowned filter) only fires for uncataloged cmd/ or internal/ product sources; docs/
release pins and the now-cataloged ci-native-pr-gate.sh stay out of the abort path.

## fail-loud proof (end to end)

- uncataloged source (internal/runtime/new_feature.go) -> planner raises ValueError, exit 1:
  "uncataloged source change, no declared runtime gate owner: internal/runtime/new_feature.go
  (id source.internal_runtime_new_feature_go): add this source with its surfaces to
  scripts/pr-gate-coverage.json, e.g. {\"id\": \"source.internal_runtime_new_feature_go\",
  \"path\": \"internal/runtime/new_feature.go\", \"surfaces\": [\"source.gate.atomic.docker.data.capabilities\",
  \"source.gate.atomic.podman.data.capabilities\"]}"
- cataloged source (cmd/baha/app_broker.go) -> planner coverage_status=resolved, exit 0.

## GRENZEN

- Only scripts/** + the v0427 test changed. No .go product edits, no .github edit, no
  app_broker.go content, no control_plane/runtime. No amend/force on a develop-descendant;
  the only force-push was on my own already-pushed branch (b986dfb07 -> 0331ec6f7), a rebase,
  not a rewrite of shared work. No merge, no comment, no subagent.
- baseharbor branch lane-0428-242-catalog-guardian, base develop 64eab13e2, PR #1768.
- CI run: 45025980169 (created 2026-11-22T13:09:22Z), terminal status success, failed count 0.
  Four witnesses: native Keycloak/Core docker+podman SKIP (owner_node_required not set);
  Validation ci-executor-tests job SUCCESS (18 suites, 0 failed); Validation pr-planner-tests
  job SUCCESS; PR · Focused Python SUCCESS.
- git diff origin/develop...HEAD --name-only:
  scripts/pr-gate-coverage.json
  scripts/pr-gate-plan.py
  scripts/test_ci_v0427_gate_catalog.py
  scripts/test_pr_ci_fallback.py
  scripts/test_pr_gate_coverage.py
  scripts/test_pr_gate_plan.py
  scripts/validate-pr-gate-coverage.py
- git log --oneline origin/develop..HEAD (only my commits):
  0331ec6f7 test(v0427): use cataloged openbao candidate under fail-loud guard
  23844ecdb test(ci-planner): cataloged CLI source for runner-context fallback tests
  41343f638 scripts: catalog cmd/baha/app_broker.go + fail-loud PR gate guard

## run-id

45025980169

## cleanliness

docker ps --format '{{.Names}}' (no daemon on this host; container work is on named
aiossh hosts only). No docker/podman compose project started this shift.

END lane-0428-242-catalog-guardian DONE
