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
