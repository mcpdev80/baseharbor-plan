git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1512/head => fea92f379e55bbe6e143a095d7c2e6c16e0b3a06 refs/heads/develop; a6afd633ce38a4cedfb74bc71d6703d3df56312b refs/pull/1512/head
gh pr view 1512 --repo mcpdev80/baseharbor --json state,mergeCommit => {"baseRefName":"develop","headRefOid":"a6afd633ce38a4cedfb74bc71d6703d3df56312b","mergeCommit":null,"state":"OPEN"}

# CODEX-REVIEW 0427-175 r3 — PR #1512

ROLLE: REVIEW

URTEIL: KORREKTUR

## PLAN

1. Verify live refs, PR state, candidate ancestry, and the terminal run attached to the exact head.
2. Diff the r3 candidate against the r2-reviewed head and inspect the recovery advice in both languages.
3. Recheck the actual destroy parser, poison-recovery test, and concurrent-init assertions against the r2 stop criteria.
4. Publish this exact-head verdict and correction recipe to canonical baseharbor-plan.

## Exact remote state and run

- `git ls-remote` returned develop `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` and PR head `a6afd633ce38a4cedfb74bc71d6703d3df56312b`.
- `gh pr view 1512 --json state,mergeCommit,headRefOid,baseRefName` returned PR OPEN, base `develop`, exact head `a6afd633ce38a4cedfb74bc71d6703d3df56312b`, mergeCommit null.
- The exact candidate is based on current develop; remote comparison reports zero base-only commits.
- `gh run view 42606542313` returned completed/success on exact head `a6afd633ce38a4cedfb74bc71d6703d3df56312b`: https://github.com/mcpdev80/baseharbor/actions/runs/42606542313. `go-unit-tests`, deployment-package-tests, vet, build, gofmt, documentation validations, both native destroy-retry cells, and PR Selected Checks completed successfully. Native Keycloak/Core, targeted HA and other unrelated cells were skipped; skips are not passes.

## Review against r2 findings

The diff from prior reviewed head `135c8be1abd80b7351432d7ffe0ffb886ace0d5f` to this head changes only `docs/cli/applications.md` and `docs/de/cli/applications.md` (23 added lines in each). It adds the recovery paragraph but does not change the product implementation or regression tests.

1. The registry conflict guidance still recommends `baha app destroy --uuid <deployment-uuid> --full-reset` in both language pages (`docs/cli/applications.md:175-179`; `docs/de/cli/applications.md:147-154`). This is not an executable command path: `cmd/baha/app_lifecycle.go:329-348` accepts only `--yes` and `--full-reset`, and rejects `--uuid` at lines 339-340. Further, `cmd/baha/app_destroy_lifecycle.go:51-66` only forwards a positional name to resolution. R3 therefore does not fix finding 1; the added documentation makes the unsupported recovery advice more prominent.

2. The poison-recovery test remains `TestPoisonedTargetRemainsReachableByUUID` in `cmd/baha/app_registry_poison_recovery_test.go:146-200`. It calls `resolveApplication` for `status --uuid` at lines 182-185, not the destroy command. Lines 186-195 explicitly accept `deployment.ErrRegistryConflict` as a successful test outcome. It neither executes the real destroy path nor proves that a selected twin is removed while the other is preserved. Finding 2 remains open.

3. `TestConcurrentInitAcrossRealProcessesIsSerializedOrRefused` remains unchanged at `cmd/baha/app_init_concurrent_race_test.go:141-170`. It starts the child process while the first registration is parked, but discards the child result (`cmd/baha/app_init_concurrent_race_test.go:150-162`, `_ = out`) and then relies on the final registry count. A child that exits before reaching the registration seam can therefore satisfy the assertion. The r2 requirement for a bounded, asserted contender outcome and the interrupted/incomplete-write boundary remains unmet.

## Correction recipe and stop criteria

- In `cmd/baha/app_lifecycle.go` and `cmd/baha/app_destroy_lifecycle.go`, implement UUID selection for destroy and carry the selected deployment identity unchanged through authorization, preflight, and mutation; alternatively, replace the conflict remediation with an already-supported and safe recovery path. Do not document `--uuid` until the actual CLI accepts and routes it.
- Add a production CLI regression that invokes `app destroy --uuid <one-id> --full-reset` on a poisoned registry. Assert that only the selected twin is removed, the other is preserved byte-for-byte, and list becomes healthy. Assert omission and invalid UUID fail closed. The test must fail if UUID parsing or routing is disabled; a conflict error must fail the recovery test, not satisfy it.
- Tighten `cmd/baha/app_init_concurrent_race_test.go`: prove the child reached the registration seam, assert its expected busy/duplicate refusal or valid convergence, and fail on unrelated child errors. Add the competing-registration versus interrupted/incomplete-record case and assert no duplicate is persisted and the partial state is reported.
- Stop review until these code and regression changes land and their exact-head checks are terminal-success. Keep skips explicitly distinct from passes. No merge or approval was performed.

## Repo-rule compliance

- Product candidate and GitHub were read-only; no tests, reruns, workflow dispatches, approvals, or merges were performed.
- No `.github/**` files were changed.
- Evidence was authored in canonical planning repository `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, remote `https://github.com/mcpdev80/baseharbor-plan.git`; no product checkout was modified.

END_DONE 0427-175-r3-review: KORREKTUR PR #1512 head a6afd633ce38a4cedfb74bc71d6703d3df56312b; exact-head run 42606542313 succeeded, but r3 is documentation-only and retains the unsupported UUID destroy advice, a non-destroy test that accepts conflict as success, and unasserted child-race outcome.
