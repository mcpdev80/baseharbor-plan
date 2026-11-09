# CODEX-REVIEW 0427-173 r7 — PR #1505

ROLLE: REVIEW
URTEIL: KORREKTUR

## PLAN

1. Verify the live PR head, exact run, selected-check provenance, current develop, and current integration state.
2. Compare the r7 delta to the r6 stop criterion and trace the registered MCP handler's authorization, injection, and mutation order.
3. Verify the drift refusal and byte-preservation assertions, then confirm the neighboring storage guards remain present.
4. Record the verdict and exact correction needed before this candidate can pass the r6 stop criterion.

## Candidate and hosted evidence

- Repository: `mcpdev80/baseharbor`, PR #1505.
- Live PR head and `refs/pull/1505/head`: `67e723fbc1c8402d785f5ef4b2089a31de4f6b59`.
- Current develop at review: `942111d5a1c43f5257bf1627a966fa9e6c6f24bd`.
- Exact-head run 42581112177: `completed/success`, event `pull_request`, head `67e723fbc1c8402d785f5ef4b2089a31de4f6b59`.
- `PR Selected Checks` job 129043775700 passed and is from GitHub Actions app 15368. `go-unit-tests` job 129039853028, `deployment-package-tests` job 129039852956, build, vet, format, docs, and wizard-registration checks passed. Native destroy-retry Docker and Podman jobs 129039851874 and 129039851850 passed. Native Keycloak/Core, Selected Runtime, and HA cells were skipped; they are not counted as passes.
- No unresolved review threads were reported. The PR API currently reports `MERGEABLE/CLEAN`.

## R7 delta against the r6 stop criterion

The r7 delta from `df9af471dc0b058ed7a59a36e6cb41279ed54475` is one file, `cmd/baha/app_prune.go`. It moves the authorization call before `pruneDriftHook`, then calls `executeApplicationPruneResolved` after the hook. At the exact candidate, the registered handler performs:

- `cmd/baha/app_prune.go:419-422`: captures the resolved identity and requires `authorizeResolvedMCPOperation` to succeed.
- `cmd/baha/app_prune.go:435-437`: invokes the package-internal hook only after successful authorization.
- `cmd/baha/app_prune.go:438-443`: calls the handler's own mutation using the pinned authorized identity.

The regression `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation` uses a live in-memory MCP client and calls the registered `baseharbor.app.prune` handler at `cmd/baha/app_prune_test.go:718-765`. The test seam replaces the on-disk identity after the authorization call and before the handler mutation. The handler returns an `IDENTITY_DRIFT` refusal at `:774-781`; the test reads the replacement record and compares its hash to the captured bytes at `:783-790`. The test does not directly call the mutation helper. The round-7 dossier also records the counterfactual: disabling the on-disk guard makes the handler delete the drifted record and fail the refusal assertion; restoring the guard passes.

This closes the r6 ordering defect. The exact candidate run executes the test in `go-unit-tests`; `deployment-package-tests` covers the on-disk guard.

## Neighboring safeguards

The r7 delta changes only `app_prune.go`; the storage guard is unchanged by that delta. In the candidate source, `internal/deployment/deployment_store.go:628` checks on-disk identity before removal, `:641-647` treats an already-absent record as idempotent, and `:650-657` keeps malformed/version errors distinct from `IDENTITY_DRIFT`. The separate registered-handler happy path remains in `TestAppPruneMCPHappyPathRemovesUniquelyResolvedRecord` at `cmd/baha/app_prune_test.go:794-850`.

These neighboring source protections were present in r6 and are unchanged in r7. The r6 act noted that it had not found dedicated regressions for repeated deletion of an absent record or the `DEPLOYMENT_RECORD_VERSION` cause; r7 does not add those tests. This review does not recast that coverage limitation as a newly introduced r7 code regression.

## Blocking integration state

The r6 stop criterion explicitly requires refreshed develop ancestry and exact-head checks after that refresh. The current candidate does not meet it:

- The candidate's merge base with current develop is `b3a8042d18ea60f162a32a51df34a499cad6a237`; current develop `942111d5a1c43f5257bf1627a966fa9e6c6f24bd` is not an ancestor of the candidate.
- Since the r7 run, develop has incorporated #1502, #1504, and #1506. Those commits change paths that overlap #1505, including `cmd/baha/app_context.go` and `internal/deployment/deployment_store.go`.
- A read-only `git merge-tree --write-tree origin/develop origin/pr1505` completed without textual conflict, and GitHub currently reports mergeable/clean. That does not make run 42581112177 evidence for the combined tree: the run preceded those changes, and the storage implementation overlaps #1506.

## Verdict and correction recipe

**KORREKTUR** for landing readiness. The r7 injection order and registered-handler regression satisfy the remaining r6 code-path finding, and run 42581112177 is terminal success on the exact r7 head. The r6 stop criterion remains unmet because the candidate and its successful run do not include current develop.

Correction recipe:

- Rebase or integrate the existing `fix/0427-173-app-prune` candidate onto current develop `942111d5a1c43f5257bf1627a966fa9e6c6f24bd`; retain this single candidate chain.
- Recheck the overlap in `internal/deployment/deployment_store.go` and preserve the #1506 owner-classification changes together with the prune identity guard, idempotent missing-record behavior, and distinct malformed/version/drift errors. Recheck `cmd/baha/app_context.go` against the #1506 CLI classification changes.
- Keep `pruneDriftHook` after successful `authorizeResolvedMCPOperation` and immediately before the handler's own mutation. Keep the registered MCP regression and its post-authorization counterfactual on the resulting candidate.
- Require terminal `go-unit-tests`, `deployment-package-tests`, and `PR Selected Checks` from app 15368 on the resulting exact SHA. Report skipped native cells as skipped; do not reuse the old SHA's green run as current integration evidence.
- Stop if the new head is not based on current develop, either storage guard is lost, the handler test no longer injects after authorization, or a required exact-head check fails, is pending, or is absent.

## Repository-rule compliance

- Review was read-only against the product candidate. No product code, branch, PR, workflow, or CI run was changed or triggered.
- Evidence is stored only in the canonical `baseharbor-plan` repository.
- Exact candidate head was re-read from GitHub before publishing this act.

END_DONE 0427-173-r7-review: KORREKTUR — r7 code-path blocker is resolved, but the r6 refreshed-develop/exact-head integration stop criterion remains unmet.
