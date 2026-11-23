# #1623 env-gate localization + fix

Shift r28-welle5-2026-11-23. Card 0428-063 / env-gate mission `/tmp/opencode/m_1623_env.md.g`.

## PLAN

- Step 1 LOCALIZE: where are the acceptance markers set in .github/ and scripts/, and why does the application shard FAIL instead of clean SKIP.
- Step 2 CLASSIFY a/b/c.
- Step 3 re-hop my candidate onto the CURRENT develop tip (mission base ddbed16 was stale), apply the catalog/harness fix, single push, single PR-triggered run to terminal, END.

## Reality witnesses

- Remote only github.com/mcpdev80 (remote guard): `lane-origin` / `upstream` all `https://github.com/mcpdev80/baseharbor.git`.
- Current develop tip (via `git ls-remote`): `afa064519a859fbfa6e171c749a911301b9522b7` (0428-258 #1803).
- MISSION BASE RECONCILE: the mission's tip `ddddbed16` (0428-199 #1723, `ddddbed16e34638f35968e2dc99921f970ba3720`) is STALE — develop has moved past it. Confirmed `ddddbed16` is still an ancestor of `afa064519` and my product base `f174513c4` merge-bases with current develop at `826d498f` (#1797). Re-hop onto `afa064519`, not `ddddbed16`.
- My candidate HEAD after additive `merge --no-ff afa064519`: `8828ceabf06bd26f20c4d292e7569afcabd92e01` (parents `93f787ec1` + `afa064519`). Delta vs develop = only my 19 #1623 product files (catalog rows already on develop via ingress #1799).

## Step 1 LOCALIZE (file:line)

Acceptance markers set in:

- `BASEHARBOR_OTLP_HANDOFF_ACCEPTANCE`:
  - `.github/workflows/targeted-integration.yml:138` — a push-only OTLP job.
  - `scripts/pre-release-integration.py:269` — harness `os.environ`.
  - `scripts/ci-native-pr-gate.sh:129` — native gate.
- `BASEHARBOR_ENV_DESTROY_ACCEPTANCE`:
  - `scripts/pre-release-integration.py:97` (mapping) + `:270-272` (harness).
  - `scripts/ci-native-pr-gate.sh:133` — native gate.

Root cause of FAIL-vs-SKIP:

- `configure_runtime_environment()` (`pre-release-integration.py:262-275`) sets BOTH markers into `os.environ` for every `/coreless-lifecycle` gate.
- `checked_tests()` (`pre-release-integration.py:206`) spawns `go test` via `subprocess.Popen(command, ...)` WITHOUT `env=`, so the subprocess INHERITS `os.environ` — markers reach the test.
- The tests then no longer skip (`application_otlp_handoff_runtime_test.go:61-63`, `env_destroy_integration_test.go:24-26`), and proceed to `detectRuntimeForTarget` + `assertCorelessHost` + a second fixture (OTLP receiver compose `UpProject`, or env-destroy KEEP retention). They t.Fatal where the host/runtime cannot satisfy the exact fixture.
- Locally confirmed: both tests SKIP cleanly without the marker (PASS overall); they RUN and hang/fail with the marker set (need a live runtime).
- Each shard test is its own `checked_tests()` call (`main()` line 317-319 list-comprehension). `checked_tests()` rejects ANY skip (`:246`). In hosted PR CI the harness sets the markers, so otlp + env-destroy RUN instead of skip, and their per-test `checked_tests()` raises `ValueError` -> the application-shard matrix job FAILS (backend/https pass their own calls).

## Step 2 CLASSIFY: (b) catalog/harness-side, within write-set

- (a) scripts-harness sets markers but shard path not reaching them: NOT this — markers ARE set AND inherited.
- (b) the two acceptance-only tests are gated as a PR-executed integration gate that hosted PR CI cannot run: YES. The `integration/{docker,podman}/coreless-lifecycle` gate is selected in PR CI via `resolve_covered_gates` routing `env_destroy.go` / `commands.go` / `machine_coverage.go` (my #1623 diff files) to that gate. The application shard then lists `TestManagedRegisteredOTLPNativeConsumerHandoff` and `TestEnvironmentDestroyNativeLifecycle` in `CORELESS_SHARD_TESTS['application']`. Both are acceptance-only (require a live coreless runtime + published `baseharbor-runtime:coreless-lifecycle` image + a second fixture). The gate stays selected; only the two acceptance tests must stop being PR-gated.
- (c) needs a `.github/workflows` change: NOT this — gate selection is catalog-driven (`scripts/pr-gate-coverage.json`), the shard test list is harness-driven (`scripts/pre-release-integration.py`). Both files are in `scripts/**` = my write-set. No workflow edit needed.

The 1797 precedent: commit `48488e65b` (0428-208, reclassify `atomic/static/mcp` as deferred release-only gate) — the gate stays selected/recorded, is pulled out of the PR-executed list, no silent skip-cover, honest carry to the release/qualify window.

## Step 3 — DECISION (c) from coordinator: no branch change; hold final state.

Coordinator 9142ab1f QUESTION ruling: Option (c) — NO change. My head `521d76812` sits on the exact base with 0 failures (the coreless-lifecycle application class went green with clean skip-as-success, no gate-drop needed). A harness deferral (`pre-release-integration.py`) would be an unnecessary change with drop risk. Hold the branch as-is; the skip-semantics question is the reviewer's to decide at the candidate (1450), verdict is decisive, request-changes if needed. END with run line + link.

## Scope reconciliation (OwnerFernkorrektur)

The pending run at the new head `213ca5195` (a merge `521d76812 x ff4cdf509`) carries 4 files beyond my #1623 delta. Verified write-set attribution:

- `cmd/baha/app_exec.go` (1 line) + `docs/cli/command-index.md` + `docs/de/cli/command-index.md` (1 line each): MINE — the Owner's `213ca5195` merge commit "docs: match guided exec command syntax" edits the #1623 guided-exec path + its docs. Belongs to card 0428-063 write-set (PR-doc-consistency: the command-index must match the guided-exec command syntax that `app_exec.go` produces). Fine to keep.
- `cmd/baha/app_new_wizard.go` + `cmd/baha/app_new_wizard_org_default_test.go`: NOT MINE — Owner's card **0428-258** (#1802, commit `ff4cdf509` "fix(0428-258): org-default missing-stack returns usageError parity"). These entered my lane branch via the Owner merging their 1802 fix into this lane. Documented as a cross-card write-set carry-in; not something this lane authored. No action without Owner confirmation — scope churn was the RC reason on 1801, so flagged, not silently reverted.

My #1623 delta vs develop (`afa064519`) = 19 files (product + docs + contracts). No harness/catalog change applied.

## cleanliness

- No containers/compose started on this host (no docker/podman test). `docker ps -a` witness: N/A (no daemon test).
- Worktree `0428-076-hop1597` left clean; no stray files in the ecosystem root.
