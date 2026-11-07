# CODEX-REVIEW PR #1424 — STATE

## Candidate witnesses

Product repository: `mcpdev80/baseharbor`. Fresh `git ls-remote` output:

```
4bcede9786c9ca6676d12fe140259c9e45d43f93 refs/heads/develop
fc81fbc6b877b45c3ec96179e85c2110c46b05c5 refs/pull/1424/head
```

GitHub reports PR #1424 OPEN, base `develop`, head `fc81fbc6b877b45c3ec96179e85c2110c46b05c5`, mergeable.

## CI state and stop

Exact-head run `42365862810` is terminal failure. `PR · Validation · pr-planner-tests` failed in job `128383704930`. Existing log line:

```
ValueError: release absent from gate catalog
```

The job ended with `FAILED (errors=295)`. Aggregate `PR Selected Checks` job `128383980930` failed with the log line:

```
BLOCKED: required job did not succeed: pr_validations
```

The initial CI state was recorded without a source verdict. Following the Owner request, I traced the lookup and test fixture at the exact candidate SHA. No rerun or workflow dispatch was requested or triggered; the full four-file acceptance review remains unapproved until hosted planner CI is green.

Planning repository identity: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, origin `https://github.com/mcpdev80/baseharbor-plan.git`.

## END CODEX-REVIEW BLOCKED

END_BLOCKED codex-1424-review: STATE pr-planner-tests job 128383704930 failed with `ValueError: release absent from gate catalog`; PR Selected Checks blocked on `pr_validations`; candidate fc81fbc6b877b45c3ec96179e85c2110c46b05c5


## Exact-candidate lookup diagnosis

At candidate `fc81fbc6b877b45c3ec96179e85c2110c46b05c5`, the catalog values are coherent: `scripts/release-requirements.json` lists v0.4.27 and contains 65 gates with v0.4.27 in `required_for` (65/65); `scripts/pr-gate-map-v1.json:3` selects `v0.4.27`. `scripts/pre-release-check-plan.py:57` reads `release-requirements.json` for release qualification. `scripts/pr-gate-plan.py:747-750` reads `mapping['release']` (the map) and checks membership in `requirements['releases']` (the requirements catalog), then builds eligible gates from each gate's `required_for` list. Thus the production release lookup is map release -> requirements release catalog -> required_for gate catalog, not a lookup of v0.4.27 in the map alone.

The hosted failure is caused by the planner regression suite's incompatible fixtures. `scripts/test_pr_gate_plan.py:19` loads the active `.27` map from `pr-gate-map-v1.json`, while `scripts/test_pr_gate_plan.py:26-27` defines shared `REQ` as only `releases: ['v0.4.26']` with every fixture gate required only for `.26`. Existing tests pass this `REQ` together with global `MAP`; the run log shows `test_exact_source_clean_integration_and_authority_failures` at `scripts/test_pr_gate_plan.py:2398` using the shared default fixture, followed by the planner guard failure `ValueError: release absent from gate catalog` at `scripts/pr-gate-plan.py:749`. The same mismatch accounts for the repeated planner errors.

Exact #021 correction point: in `scripts/test_pr_gate_plan.py:19-27`, decouple the legacy `.26` fixture map from the production active map so calls using the hard-coded `.26` `REQ` also use a `.26` mapping. Keep dedicated `.27` coverage using the real requirements catalog and an explicit `.27` mapping; retain incomplete-catalog cases with a matching release so they reach and verify the intended fail-closed gate-selection behavior. `scripts/test_ci_v0427_gate_catalog.py:114-141` already exercises the planner under `.27` with the real inventory, while its catalog-only test at lines 67-77 checks nonempty/unique gate IDs. The correction must make the complete hosted `pr-planner-tests` group pass and leave `PR Selected Checks` green; stop acceptance if either remains red. No code or workflow was changed in this review.

Verdict: `request-changes` until the hosted planner path is green.

## r2 fix — implemented + hosted-verified

- **Root cause (exact):** the failing CI path (`test_pr_gate_plan`, `pr-planner-tests`) loads the **live production MAP** from `pr-gate-map-v1.json` (my bump made it `v0.4.27`) but every shared in-memory catalog is `REQ = {releases: ['v0.4.26']}`. The planner guard (`pr-gate-plan.py:747-750`) searches `MAP['release']` (`.27`) inside `REQ['releases']` (only `.26`) → `ValueError: release absent from gate catalog`. My `pr_focused` (205) never ran `test_pr_gate_plan` (not in `CI_EXECUTION_SUITES`), so it was missed locally.
- **Fix (CODEX recipe, exact):** in `scripts/test_pr_gate_plan.py` decouple the legacy `.26` fixture MAP from the production MAP — `MAP_26 = dict(MAP); MAP_26['release']='v0.4.26'`; all hardcoded-`.26` REQ calls use `MAP_26`. Production `MAP` still loads the live file. `test_ci_v0427_gate_catalog.py` keeps real-inventory v0.4.27 coverage (fixed its own map-release assertion, which wrongly required the production map key == `.27`).
- **Net production diff vs develop** = 3 CI-seam files only: `release-requirements.json` (+v0.4.27 to 65/65 gates + releases), `test_ci_v0427_gate_catalog.py`, `test_pr_gate_plan.py` (9 lines). `pr-gate-map-v1.json` reverted to `v0.4.26` baseline (net-zero vs develop).
- **Local:** 368/368 `pr_focused` OK incl. `test_pr_gate_plan` 163.
- **Hosted (observed):** run **42367756259** on head `2c3794640b5d37b752407e09201ed11d7cf4850e` → **completed/success**. `PR · Validation · pr-planner-tests = success` (was failure on `fc81fbc6`/`b70c49144`); `PR Selected Checks = success`.
- `git ls-remote` proof: `2c3794640b5d37b752407e09201ed11d7cf4850e refs/heads/work/r27-ci-lanes-catalog`. Base `4bcede97` is an ancestor (no drift). Exact-one-candidate #1424, single candidate chain.

## END r2 — DONE

END_DONE 0427-021-ci-lanes: head=2c3794640b5d37b752407e09201ed11d7cf4850e pr=1424 core_integration_ci=anker OK: v0.4.27 registered release-requirements (65/65 gates + releases) + pr-gate-map v0.4.26 baseline preserved; hosted pr-planner-tests run 42367756259 SUCCESS (was failure fc81fbc6/b70c49144 `release absent from gate catalog`); runtime_cells unchanged (atomic/docker+podman lifecycle, no fake pass/skip). gate_catalog=v0.4.27 fixed + migration-proof. fail_closed=pr-gate conservative fallback + fail-closed native-runtime gates. branch work/r27-ci-lanes-catalog push OK; ls-remote=2c3794640, base develop 4bcede97 ancestor-ok. run=local 368 OK + hosted run 42367756259 (planner+Selected Checks green) akte=evidence/r27-ci-lanes/ci-lanes/act-1424-review-state.md (origin/main pending publish).
