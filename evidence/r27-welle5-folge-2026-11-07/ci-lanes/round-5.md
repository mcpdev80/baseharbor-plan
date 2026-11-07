# ROUND 5 — CI-Naht r5 (card t-20261018-r27-ci-lanes #0427-021, PR #1424)

**Lane:** 0427-021-r5-ci-lanes (fresh laptop lane 246fa998, inherits r1-r4 context)
**Date:** 2026-11-07
**Write-set:** `scripts/*` ONLY — no `cmd/baha`, no `.github` workflow file.

## Goal (what is being built)

Finish CODEX r4's two request-changes on the CI seam so PR #1424 is re-reviewable:
1. **Diff honesty** — every `scripts/*` file in the candidate diff mapped to exactly one
   intentional, card-owned change; no accidental/undocumented files carried along; report the
   exact file list with reason per file.
2. **Regression protection** — the durable catalog test `scripts/test_ci_v0427_gate_catalog.py`
   must explicitly assert that the production `scripts/pr-gate-map-v1.json` release == `v0.4.27`,
   so a rollback to `.26` (the r3 stash-dance regression) yields a RED test cell; remove the stale
   `.26` comment. The catalog-only (nonempty/unique gate ids) check stays.

## Reality witnesses (remote truth)

Product repo `mcpdev80/baseharbor`. The workers/baseharbor checkout was **QUARANTINED** (its
candidate head `1f2c890f` reported `release: v0.4.26` in `pr-gate-map-v1.json` and
`release-requirements.json`, contradicting the remote) — so all truth below is measured on a fresh
clone in my persistent zone, per the wrong-zone / stale-ref directives.

Fresh clone `/tmp/opencode/0427-021-r5-ci-lanes-wt`:

```
1f2c890f75cf2d64e9b90a0623d671e18ed4bdaa refs/heads/work/r27-ci-lanes-catalog   (git ls-remote origin)
beb923fe6c4d8ede4d397a87490f3ac2eb2e65cc refs/heads/develop
cad06b1598ba8b7d0107fd05e672af27a027f82d origin/main (baseharbor-plan)
```

Base attestation:

```
$ git merge-base --is-ancestor origin/develop HEAD && echo OK
OK   # origin/develop (beb923fe6) is an ancestor of the exact candidate head 1f2c890f7
```

Remote production state at `1f2c890f7` (verified on the fresh clone, NOT the quarantined checkout):
- `scripts/pr-gate-map-v1.json` `"release": "v0.4.27"`
- `scripts/release-requirements.json` releases `[..., "v0.4.26", "v0.4.27"]`, 65/65 gates list
  `v0.4.27` in `required_for`
- `scripts/pr-check-runner.py` `CI_EXECUTION_SUITES` includes `'test_ci_v0427_gate_catalog'`

Exact-one-candidate #1424, single chain. Branch `work/r27-ci-lanes-catalog` carried no foreign
commit; the only ancestor test is develop (beb923fe6), which is the required integration base.

## Point 1 — DIFF HONESTY (exact file list, reason per file)

Net candidate diff vs `origin/develop` touches EXACTLY SIX `scripts/*` files. Every one maps to
one intentional, card-owned change. None is accidental or an undocumented carry-along:

| # | File | Net change vs develop | Intentional card link |
|---|------|----------------------|------------------------|
| 1 | `scripts/pr-check-runner.py` | add `'test_ci_v0427_gate_catalog'` to `CI_EXECUTION_SUITES` (line 109) | CI wiring so the new durable test runs in the hosted `pr_planner` seam (Owner directive 2026-11-07: a new test must run in GitHub CI) |
| 2 | `scripts/pr-gate-map-v1.json` | `"release"` `v0.4.26` → `v0.4.27` | production map targets the released candidate |
| 3 | `scripts/release-requirements.json` | register `v0.4.27` (add to `releases` + every gate `required_for`; 65/65) | migration/regression proof, card Owner-required backfill (task §Owner-required CI coverage backfill) |
| 4 | `scripts/test_ci_v0427_gate_catalog.py` | NEW durable catalog regression test | card core: proves v0.4.27 registered + PR planner resolves reviewed exact-path candidates |
| 5 | `scripts/test_pr_gate_plan.py` | decouple legacy `.26` fixture map → `MAP_26` (all hardcoded-`.26` REQ calls) | fixes hosted `pr-planner-tests` `ValueError: release absent from gate catalog` (CODEX r1/r4 fix) |
| 6 | `scripts/test_pr_registration_ci.py` | decouple legacy `.26` fixture map → `mapping_26` (`plan()` helper passes `mapping_26`) | same fail-closed decoupling, consistent coverage of the registration seam |

**Why the r4 message said 4, reality is 6:** the r4 commit (`8bf52f028`) named only the 4 files it
authored directly (files 1-4). The MAP_26 decoupling in files 5 and 6 landed in the same r4
candidate (`1f2c890f`) and is part of the exact same card, so the honest net-diff total is 6. No
file is outside the card and none is an accidental/undocumented carry-along. End report carries
this exact list.

## Point 2 — REGRESSION PROTECTION (fix applied)

The r4 candidate had RE-INTRODUCED the failure CODEX r4 point (2) flagged: `test_v0427_is_registered_as_candidate_release`
no longer asserted the production map release, and carried a stale comment ("…stays pinned to the
tested v0.4.26 baseline"). r5 restores the assertion and deletes the stale comment:

```diff
 def test_v0427_is_registered_as_candidate_release(self):
-    # v0.4.27 is proven by its registration in the release gate catalog
-    # (release-requirements.json releases + every gate's required_for), not
-    # by the production pr-gate-map-v1.json release key, which stays pinned
-    # to the tested v0.4.26 baseline. The catalog is what the planner and
-    # pre-release check now discover for v0.4.27.
+    # The production pr-gate-map-v1.json release key MUST be v0.4.27, so a
+    # rollback to the tested v0.4.26 baseline (the r3 stash-dance that
+    # regressed this in r3) fails this cell red. v0.4.27 is proven by that
+    # production map key AND by its registration in the release gate catalog
+    # (release-requirements.json releases + every gate's required_for).
+    self.assertEqual('v0.4.27', self.mapping['release'])
     self.assertIn('v0.4.27', self.inventory['releases'])
     for gate in self.inventory['gates']:
         with self.subTest(gate=gate['id']):
             self.assertIn('v0.4.27', gate.get('required_for', []))
     self.assertEqual('baseharbor.pr-gate-map/v1', self.mapping['schema'])
```

**Red-cell proof (fail-closed verified):** with `scripts/pr-gate-map-v1.json` temporarily set to
`"release": "v0.4.26"` the cell goes RED:

```
$ python3 -m unittest scripts.test_ci_v0427_gate_catalog.V0427GateCatalogTests.test_v0427_is_registered_as_candidate_release
AssertionError: 'v0.4.27' != 'v0.4.26'   #   - v0.4.27   + v0.4.26
FAILED (failures=1)
```

Production map restored after the proof (`git diff` clean). Catalog-only check
(`test_v0427_release_catalog_feeds_pr_gate_planner_catalog`: nonempty + unique gate ids) retained.

## Local checks (self-run, on the fresh clone at the fixed state)

```
python3 -m unittest scripts.test_ci_v0427_gate_catalog   -> Ran 7 tests, OK
python3 scripts/test_pr_check_runner.py                   -> Ran 32 tests, OK
python3 scripts/test_pr_gate_plan.py                      -> Ran 142 tests, OK   (hosted pr-planner-tests seam)
python3 scripts/test_pre_release_check_plan.py            -> Ran 3 tests, OK
python3 scripts/test_ci_check_routes.py                   -> Ran 4 tests, OK
go build ./...                                            -> exit 0
go vet ...                                                -> clean
```

Notes: `scripts/test_pr_registration_ci.py` fails 7 failures/8 errors LOCALLY on a fresh clone —
this is PRE-EXISTING on true head `1f2c890f7` (verified by `git stash`: same 7/8 without my change)
because several of its cases assert real committed runtime-receipt artifacts that a fresh clone does
not contain. It is not in the `pr_focused`/`pr_validations` CI matrix I must keep green and my change
introduces no new failure.

## CI-wiring finding — REPORTED, NOT EDITED (Owner scope .github/**)

`scripts/test_ci_v0427_gate_catalog.py` is in `CI_EXECUTION_SUITES` (pr-check-runner.py:109), so the
hosted `pr_planner` seam whitelists it and it executes as a `PR · Validation` cell under the umbrella
`PR · Focused Python`. HOWEVER the `pr_focused` job in `.github/workflows/ci.yml` runs a HARDCODED
script list at lines **734-758** and does **not** include `test_ci_v0427_gate_catalog` (the list
runs `test_pr_check_runner.py` at line 738 but never the new catalog test). Per Owner directive
2026-11-07 the durable test must also run under GitHub CI; the needed change is under
`.github/workflows/ci.yml` `pr_focused` (insert
`python3 scripts/test_ci_v0427_gate_catalog.py` into the line 734-758 block). That is Owner scope;
reported here as a finding with file:line, not edited.

## Repo-rule compliance

- Write-set `scripts/*` only. No `cmd/baha`, no `.github`. No product-repo evidence dir. No
  workflow edit, no rerun, no workflow_dispatch.
- Exact-one-candidate #1424; branch `work/r27-ci-lanes-catalog` from origin/develop (beb923fe6,
  ancestor-ok). No foreign commit carried.
- No subagents (AGENTS 4.8). All checks self-run.

## Hosted-run watch — PENDING (next action)

Push r5 fix to real GitHub on `work/r27-ci-lanes-catalog`, then observe
`pr-planner-tests` + `PR Selected Checks` + the new red-cell assertion on the final SHA
(run-id + status recorded here). No CI rerun workflow_dispatch (Owner scope).

## Status

IN PROGRESS — local fix + local verification complete; hosted-run watch pending; END not yet posted.
