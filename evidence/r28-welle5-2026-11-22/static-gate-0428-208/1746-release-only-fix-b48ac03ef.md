## 0428-208 / PR #1746 — release-only ci-fast-check catalog fix

Lane: `lane-0428-208-static-release-gate` (owner-delegated, ledger 1291). Session: w1625-pr1723-0428-199-workloadport (my own session; no subagents).

## Reality

- Remote guard: `lane-origin = https://github.com/mcpdev80/baseharbor.git`.
- Branch head before hop: `208ee7607`. Current develop: `ef73b50b` (was `cace61802` at mission write; develop advanced). PR #1746 head: `208ee7607`.
- Mission `m_seat_1746fix.md.g`: owner-delegated catalog fix ONLY in `scripts/pr-gate-coverage.json`. Give `ci-fast-check` its own `atomic/static/ci-fast-check` gate with `selection_scope="release-only"`, remove it from the focused `shell-ux` gate. No new PR-CI routes, no `.github`, no merge. Push new head + `ls-remote refs/pull/1746/head` witness. Hosted CI aggregate must go gone-green.

## PLAN

- no-ff hop onto current develop `ef73b50b` (HEAD `be5c8ddc`, parents `208ee7607` + `ef73b50b`). Catalog diff vs develop empty before fix. No `.github` touched by hop.
- Surgical catalog fix: remove `source.gate.atomic.static.ci.fast.check` from focused `shell-ux` covers; add dedicated `atomic/static/ci-fast-check` gate (`selection_scope="release-only"`).
- Validate: focused selection must exclude ci-fast-check; release executor must select it; `validate-pr-gate-coverage.py` must pass; lane test suites must pass.
- Push new head + ls-remote witness. Hosted CI observation. Evidence + END.

## Progress

- Hop done: `be5c8ddc`, parents `208ee7607` (1746 before) + `ef73b50b` (develop). Catalog diff vs develop = 0 lines before fix. No `.github` in hop diff.
- Catalog fix applied (surgical, 14 insertions / 2 deletions, exact formatting preserved):
  - `shell-ux` covers now `["capability.profile.shell-interface", "gate.shell-ux"]`.
  - New gate `atomic/static/ci-fast-check` (`runtime: static`, `scope: pr`, `covers: ["source.gate.atomic.static.ci.fast.check"]`, `selection_scope: release-only`).
  - Catalog `release` stays `v0.4.27`.
- Focused selection now excludes ci-fast-check: `resolve_covered_gates(['scripts/ci-fast-check.sh'])` returns `[]`. PASS.
- Dedicated release-only gate present and correct.
- RELEASED: production validator `validate-pr-gate-coverage.py` FAILS: `coverage catalog includes gates outside active release catalog: atomic/static/ci-fast-check`. Lane test `test_ci_v0427_gate_catalog.py::V0427PrGateDedupRegression::test_reviewed_cli_candidate_resolves_under_v0427` and `test_unknown_path_selects_conservative_fallback_under_v0427` FAIL with the same `extra` error.

## Blocker

Design tension, unresolvable within my write-set (`scripts/pr-gate-coverage.json` only):

- `release-requirements.json` declares `atomic/static/ci-fast-check` with `required_for: ["v0.4.28"]` only (and `dependencies: ["core"]`). This entry arrived from the #1746 target head `208ee7607` (earlier lane attempt `f48a4a478`); current develop `ef73b50b` has NO v0.4.28 and no such gate, so the no-ff hop left it orphaned.
- The validator computes `required_ids` from gates whose `required_for` includes `release` = `v0.4.27` (catalog tag). `ci-fast-check` (v0.4.28-only) is flagged `extra`.
- The lane test `test_ci_v0427_gate_catalog.py:52` asserts `ci-fast-check` must NOT include `v0.4.27` (it is a v0.4.28 gate). `test_ci_v0427_gate_catalog.py:166` asserts `selected_gates == ['atomic/docker/control-plane-recovery']` for a v0.4.27 OpenBao candidate.

Both in-scope resolutions violate a constraint:
- Option A — bump catalog `release` to `v0.4.28`: validator passes, but the planner (`pr-gate-plan.py:1822`) compares `coverage['release'] == result['release']` where `result['release'] = mapping['release'] = v0.4.27`. `v0.4.28 != v0.4.27` → targeted coverage path skipped → `selected_gates=[]` → `test_reviewed_cli_candidate_resolves_under_v0427` :166 fails.
- Option B — add `ci-fast-check` to `required_for v0.4.27` in `release-requirements.json`: violates `test_ci_v0427_gate_catalog.py:52`. Also `release-requirements.json` is out of my write-set.

Files needing change to resolve: `scripts/release-requirements.json` (out of write-set) and/or `scripts/validate-pr-gate-coverage.py` (production, out of write-set), plus possibly the mapping release or the lane test. This is a scope decision for the Owner/Coordinator.

## Next

Await Owner/Coordinator decision on the release-tag tension. Options: (1) align `release-requirements.json` so `ci-fast-check` is `required_for v0.4.27` (needs lane test update, out of scope), (2) add a `release-only` scope filter to the validator's `extra`/`missing` check (production change, out of scope), or (3) a mapping/catalog release alignment coordinated across repos. Do NOT push the current candidate until resolved.

## repo-rule compliance

- Write-set: `scripts/pr-gate-coverage.json` only (owner-delegated ledger 1291). No `.github`, no product code, no release-requirements.json, no validator, no test files.
- No force/rebase/amend; no-ff hop only. No subagents. All edits via edit tool + python heredoc in the #1746 worktree `/var/tmp/0428-208-static-gate`.

## END

END_BLOCKED — catalog fix applied and verified (focused excludes ci-fast-check, dedicated release-only gate present), but production validator + lane test fail on the release-tag tension. Coordinator `9142ab1f` posted QUESTION. Head `be5c8ddc`, branch `lane-0428-208-static-release-gate`. No push, no merge.
