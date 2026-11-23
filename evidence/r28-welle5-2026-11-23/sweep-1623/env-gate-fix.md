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

## Step 3 — BLOCKED on scope confirmation

I posted a QUESTION to the coordinator (9142ab1f) before writing the fix, because the exact mechanism (move the two tests out of `CORELESS_SHARD_TESTS['application']` vs add a skip-allowed deferred path in `checked_tests`) changes the required-PR-check semantics. Awaiting the call.

Candidate state at STOP:

- HEAD `8828ceabf` (additive hop onto `afa064519`). No scripts/catalog change applied yet (awaiting confirmation).
- No push, no CI run, no merge.

## cleanliness

- No containers/compose started on this host (no docker/podman test). `docker ps -a` witness: N/A (no daemon test).
- Worktree `0428-076-hop1597` left clean; no stray files in the ecosystem root.
