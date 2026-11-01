# deps-gatemap — Evidence

**Lane:** deps-gatemap · **Owner:** Ornith-Worker · **Task:** t-20261101-deps-gatemap-1160
**Repo:** mcpdev80/baseharbor · **PR:** #1260 `ci(gate-map): bind go.mod/go.sum to build-test gates`
**Candidate SHA:** `ea6b75e2` (branch `work/deps-gatemap-1160`, base develop `46307b75`)
**Status:** END deps-gatemap DONE — implementation + tests + hosted CI all complete; pending CODEX-REVIEW + merge.

## PLAN

1. Reproduce the BLOCKED: go.mod/go.sum on PR #1160 diff → `unknown impact` → coverage-unresolved. DONE (reproduced live).
2. Create + claim task card t-20261101-deps-gatemap-1160 in baseharbor-plan. DONE (pushed main 8783ea7).
3. Add go.mod/go.sum classification branch in scripts/pr-gate-plan.py (bind CODE_CHECKS+CLI_CHECKS, before scripts/-catch-all). DONE.
4. Extend planner tests (dependabot-only → resolved; mixed → unresolved) + retire 3 stale fail-closed assertions. DONE.
5. 175+ planner tests locally green. DONE (177 green; 3 pre-existing external failures unrelated).
6. Branch + PR #1260 against develop; watch PR Selected Checks to terminal. DONE (SUCCESS, run 41346617200).
7. evidence.md + ## PLAN + HANDOFF post. This step.

## 1. Blocker reproduced (before change)

`/home/marcel/dev/baseharbor-ecosystem/baseharbor` (remote `git@github.com:mcpdev80/baseharbor.git`),
branch `pr-1160-rerun`. Fetched PR #1160 head as `pr-1160-live` (`88604ee6`
`chore(deps): bump github.com/go-jose/go-jose/v4`).

`git diff --name-status origin/develop pr-1160-live`:
```
M	cmd/baha/docker_engine.go
D	cmd/baha/docker_engine_podman_test.go
M	go.mod
M	go.sum
M	scripts/pr-gate-plan.py
M	scripts/test_pr_gate_plan.py
```

`pr-diff-base.py --target-base origin/develop --head pr-1160-live` yields changes
`go.mod` (modified), `go.sum` (modified), `broad_required=false`.

Planner output on this diff (BEFORE change):
```
coverage_status : unresolved
unresolved_coverage : ['unknown impact for go.mod', 'unknown impact for go.sum']
selected_gates        : []
broad_required        : True
```
Exactly the coverage-unresolved block described in the mission (Live-Log of #1160
Run 4134xxxx 18:55Z). Cause: the per-path classification chain in
`scripts/pr-gate-plan.py` (lines ~1358–1639) has no branch for go.mod/go.sum, so
they fall to the `else` → `area='unresolved'` → `unknown impact for <path>`.

## 2. Fix (before change → after change)

Inserted a new `elif` branch in the per-path classification chain of
`scripts/pr-gate-plan.py`, before the `scripts/ci-|pr-|test_pr_|verify-|evidence`
catch-all and the final `else`:
```python
elif path in ('go.mod', 'go.sum'):
    # Module and dependency files: a bump changes exactly the Go build and
    # test surface, never product or gate behaviour. Bind it to the same
    # Go build/test validation checks the CI matrix runs for a Go change
    # (source-contracts, cli-build, cli-vet, cli-guided-tests, cli-gofmt)
    # -- no new gate, no widening. Without this branch a Dependabot-only
    # go.mod/go.sum diff fell to the 'unknown impact' catch-all and left
    # PR Selected Checks coverage-unresolved (#1160).
    area = 'go-module-dependency'
    require(CODE_CHECKS)
    require(CLI_CHECKS)
```
`CODE_CHECKS` = `source-contracts` (`go test ./internal/application/... ./contracts/...`);
`CLI_CHECKS` = `cli-guided-tests`, `cli-vet`, `cli-build` — the existing Go
build/test validation checks the CI matrix runs for a Go change. Same
smallest-group pattern as the `#1259` `observability-acceptance` binding.

Planner output AFTER change (same #1160 diff):
```
coverage_status    : resolved
unresolved_coverage: []
selected_gates     : []
broad_required     : False
required_validation_checks: ['cli-build', 'cli-guided-tests', 'cli-vet', 'source-contracts']
```

Mixed diff (`go.mod`+`go.sum` + an unreviewed product file) → stays `unresolved`
(fail-closed preserved). Unknown path alone → still `unresolved` (existing
fail-closed preserved).

## 3. Tests

`scripts/test_pr_gate_plan.py` — 5 additions inside `SharedBackendResolutionMappingTests`:
- `test_dependabot_only_go_mod_go_sum_resolves_with_go_build_test_checks` — resolved, requires source-contracts/cli-build/cli-vet.
- `test_go_mod_go_sum_bundled_with_unreviewed_stays_unresolved` — unresolved.
- `test_go_mod_alone_still_resolves` / `test_go_sum_alone_still_resolves`.
- `test_dependabot_go_mod_go_sum_missing_gate_fails_closed` — area reason `go-module-dependency`.

Retired 3 stale assertions that hard-coded go.mod as `unknown`:
- `test_unknown_never_auto_selects_full_release_catalog` — removed `go.mod` from the unknown list.
- `test_rename_and_delete_paths_are_not_lost` — renamed go.mod now resolves; assert build/source-contracts checks present.
- `test_actual_repository_release_catalog` — swapped `go.mod` for `config/deleted.yaml` as the unknown representative.

Local run: **177** planner tests, all green (was 172). The only remaining
failures in the aggregated runner are 3 pre-existing, out-of-scope failures
(`baseharbor-plan` `plan.py` check failing on release-cycle prerequisites;
`receipt_writer` remote-token test) — verified identical on the clean baseline
before any change.

## 4. Hosted CI (Eigenes-Run-Pflicht)

PR #1260, branch `work/deps-gatemap-1160`, after merging develop:
- Candidate SHA (head): `ea6b75e2` (merge of develop); implementation commit `9fb8d22f`.
- CI run **41346617200** (`CI · PR #1260`), event `pull_request`, terminal status
  **completed / conclusion success**, `2026-11-01T20:23:34Z`.
- Relevant jobs: `PR Selected Checks` = success; `pr-planner-tests` = success;
  `ci-policy` = success; `ci-executor-verifier-tests` = success;
  `receipt-execution-tests` = success; `Targeted HA · docker`/`podman` = skipped
  (correct — only `scripts/` changed).

URL: https://github.com/mcpdev80/baseharbor/actions/runs/41346617200

## repo-rule compliance

- Only `scripts/pr-gate-plan.py` (11 +) and `scripts/test_pr_gate_plan.py` (52 +, 5 −) touched.
- No `.github/*`, no `scripts/ci-*`, no `ci.yml`, no product code.
- No new gate; binds to existing Go build/test validation checks.
- No merge performed; no subagent/task spawned; no `codeman agent spawn/rm/send`.
- Fail-closed contract preserved for unknown paths and mixed diffs.

## Handoff

- Branch `work/deps-gatemap-1160`, commit `ea6b75e2` (base develop `46307b75`).
- PR #1260 `ci(gate-map): bind go.mod/go.sum to build-test gates` → develop. Head `ea6b75e`.
- CI run 41346617200 terminal: PR Selected Checks SUCCESS.
- Evidence: `baseharbor-plan/evidence/board-2026-11-01/deps-gatemap/evidence.md`.
- Next: CODEX-REVIEW of #1260 against this contract, then CODEX-MERGE (owner-autorisiert) + Planning publish.
