# 0428-227 / #1753 dedup-hop onto develop: catalog byte-identical to develop

lane: w21-pr1702-0428-142-compat
session: 0847d100
card: 0428-227 / PR #1753 — register internal/operatorauth/local_runtime.go in the PR gate catalog
candidate head: ba2c11b6f340fb5c937603e1cc472ab1b2ac06e2 (additive merge commit: ae0caf9bc + develop b9e69b14)
base develop SHA: b9e69b14a7c8c7e1ccf9176b0762bacecdecee5e (#1790 ingress; lineage cace61802)
PR #1753: https://github.com/mcpdev80/baseharbor/pull/1753 (open / READY, base develop)
hosted CI run: 45091758273 (head ba2c11b6f) — FULL required plan, SUCCESS
status: END_DONE (dedup-hop complete; PR Trusted Plan now green base-side)

## PLAN

1. Read mission m_0847_1753d.md.g (dedup-hop, #1765-pattern): my #1753 head ae0caf9bc still carries my PR-side catalog row for internal/operatorauth/local_runtime.go. Develop carries the same base-side row (ingress #1790: TWO rows — local_runtime.go AND local_runtime_test.go). My PR-head catalog edit falls away. git merge --no-ff origin/develop (NO force/rebase/amend).
2. IF catalog conflict: git checkout --theirs scripts/pr-gate-coverage.json (develop 1:1), git add. MUST: catalog byte-identical to develop, my product/test diff preserved, diff origin/develop HEAD -- scripts/pr-gate-coverage.json == EMPTY, no duplicate ids.
3. push + ls-remote refs/pull/1753/head witness. NO merge, PR open/ready.
4. EXACT hosted to terminal: TP now base-side green expected + selected data-caps + native.
5. STOP if catalog not byte-identical, .github touch, TP-fail on other source.

## BEFUND — what I did

The #1753 governance-finding freeze (PR head ae0caf9bc still carried a PR-side catalog row for internal/operatorauth/local_runtime.go that the trusted base did not see) is resolved by a dedup-hop onto the current develop tip, where the same base-side row now lives (ingress #1790).

My PR head ae0caf9bc carried ONE local_runtime row with id `internal.operatorauth.local.runtime.go` (dot between local and runtime). Develop c6a7138ce / b9e69b14 carries the same registration plus the partner row under id `internal.operatorauth.local_runtime.go` (underscore) and a second row `internal.operatorauth.local_runtime_test.go`. So my PR-head catalog edit is now redundant: develop already registers both files base-side.

I merged develop onto my #1753 branch:
- Branch (dedicated worktree at ae0caf9bc) `git merge --no-ff origin/develop` (b9e69b14).
- CONFLICT (content) in scripts/pr-gate-coverage.json (my typo id + my row vs develop's two rows). Resolved by `git checkout --theirs scripts/pr-gate-coverage.json` (develop 1:1) — the catalog becomes byte-identical to develop, and my product/test diff survives untouched.
- Merge commit ba2c11b6f, parents ae0caf9bc + b9e69b14 (proper additive merge).

## CATALOG PROOF — byte-identical to develop

- git diff origin/develop HEAD -- scripts/pr-gate-coverage.json == 0 content lines.
- git diff --name-only origin/develop HEAD -- excluding the catalog lists ONLY my #1753 product files:
  - cmd/baha/app_broker.go
  - cmd/baha/ci_integration_operator_enabled.go
  - cmd/baha/ci_integration_operator_enabled_test.go
  - internal/operatorauth/local_runtime.go
  - (plus develop's two new test files pulled in by the hop: cmd/baha/control_plane_single_native_ci_test.go, cmd/baha/runtime_integration_test_support_test.go; cmd/baha/core_installation_runtime_test.go — all from develop, not my catalog)
- No duplicate ids (218 unique). JSON valid (218 components). Catalog regression test OK.

## LOCAL CHECKS

- go build ./cmd/baha/ ./internal/operatorauth/ : ok
- go vet ./internal/operatorauth/ : clean
- JSON valid (218 comps), catalog regression OK
- Key #1753 tests PASS with tag baseharbor_ci_operator_testonly:
  - TestCIIntegrationOperatorAdmitsFootprintShowOnlyOnDataCapabilitiesGate — PASS (cmd/baha)
  - TestCheckLocalRuntimeGrantAdmitsFootprintShowReadOperation — PASS (internal/operatorauth)

## HOSTED CI — run 45091758273 (head ba2c11b6f)

REQUIRED GATES — all success:
- PR · Trusted Plan -> success (the previously-reported uncataloged-source error for internal/operatorauth/local_runtime.go is GONE: base b9e69b14 now carries both local_runtime rows, so the trusted-plan catalog read is satisfied base-side — the dedup-hop resolved the governance finding)
- PR · Go unit · cli-0 / cli-1 / cli-2 / cli-3 / owner / packages -> success
- PR · Validation · go-build -> success
- PR · Validation · go-vet -> success
- PR · Validation · authority-package-tests -> success
- PR · Validation · ci-integration-operator-seam-tests -> success
- PR · Native gate plan -> success
- PR · Source format -> success
- PR · Focused Python -> success
- PR · Exact Candidate -> success
- PR · Runner Interface -> success
- PR · Workflow policy -> success
- PR · Demo Pin -> success

No source other than the resolved catalog changed. No .github touch. No go.mod change.

## WHY THIS RESOLVES THE PRIOR GOVERNANCE FINDING

The prior finding (1753-cat-add.md): my PR-head catalog row was invisible to the trusted-plan policy because the policy reads the catalog from the checked-out base. The base (c6a71382 / b9e69b14 lineage) did not carry the row, so TP failed uncataloged. The base-side catalog now carries BOTH local_runtime rows via ingress #1790, so the dedup-hop (my branch folded onto develop) makes the catalog base-side-satisfied: TP reads the base catalog, it has the rows, TP passes. No .github change, no base edit outside the develop lineage — the fix is a pure additive hop onto develop.

## END lane

END_DONE (dedup-hop complete) — PR #1753 / card 0428-227. My PR-head catalog row for internal/operatorauth/local_runtime.go fell away by folding the #1753 branch onto develop b9e69b14 (the base-side #1790 rows now cover the same registration). New head ba2c11b6f, catalog byte-identical to develop (0 content lines vs develop, no duplicate ids), my #1753 product diff preserved (5 files). Pushed to lane-0428-227-footprint-gate-admission. PR #1753 stays OPEN/READY (draft=false). Hosted CI run 45091758273 (full required plan) SUCCESS: PR · Trusted Plan green base-side (the prior uncataloged-source finding resolved), Go unit (cli-0..3, owner, packages) and all Validation gates green. No merge. akte published to baseharbor-plan origin/main.

## cleanliness

- Hop worktree: /tmp/opencode/1753-dedup-hop-wt (dedicated, outside ecosystem root). Removed at END.
- No content edit to local_runtime.go, no .github touch, no go.mod change. Catalog resolved to develop 1:1; product diff (5 #1753 source files) preserved.
- No docker/podman compose projects started (git/gh read-only verification of hosted CI; no containers on the coordinator host).
- git ps -a witness: none started (no docker/podman daemon contact).
- Temporary CI log files fetched via gh api to /tmp/opencode (outside ecosystem root).
