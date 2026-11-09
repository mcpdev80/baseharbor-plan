# CODEX-REVIEW 0427-159 r3 — PR #1499

## PLAN

1. Verify the live PR head, develop SHA, base ancestry, commit chain, and exact-head run.
2. Compare the round-3 rebuttals for F2, F3, and F4 with source on the candidate and current develop.
3. Trace registry and repository-up production paths to determine whether a damaged directory is bound to the requested application before network enrichment.
4. Check the regression assertions and hosted CI routing, then record exact remaining findings and stop criteria.
5. Publish this SHA-specific verdict to Planning and post END.

## Verdict

**ROLLE: REVIEW — KORREKTUR; approval withheld.** The round-3 candidate adds network enrichment to the registry error and the Go gates pass, but the rebuttals do not establish the directory-to-application binding needed to avoid false attribution. F2's UUID-format concern remains; F3 remains a production-path defect; F4's CI routing is real but the relevant tests do not prove the claimed no-false-attribution contract. The exact-head run is terminal failure only because the separate 0427-172 marker test fails in the native Keycloak/Core jobs; record that as external STATE, not as a 0427-159 regression.

### Exact candidate and remote state

- Repository: `mcpdev80/baseharbor`; PR #1499 is open at exact head `9e211715187534d9939a39702cd28a726d83581e`, base branch `develop`, `mergeable=MERGEABLE`, `mergeStateStatus=UNSTABLE`.
- `git ls-remote` returned develop `20902f0a6ab016fd8fe6a501751e1becc5f334dd` and `refs/pull/1499/head` `9e211715187534d9939a39702cd28a726d83581e`.
- Base `3187cea15728143146905c7238ad6e280ca11b3e` is an ancestor of the candidate (exit 0), as reported. Current develop `20902f0a6ab016fd8fe6a501751e1becc5f334dd` is not an ancestor (exit 1); the branch has not integrated the current develop tip. `develop..head` contains only the chain's two commits, `b68092b2` and `9e211715`; no foreign candidate commit appears in that range.
- Changed paths are the 13 paths shown by `gh pr view`; there is no `.github/**` change. The PR itself and product worktree were not modified.

### F2 — The UUID design rationale does not justify scanning arbitrary directory names

The rebuttal is partly right that a newly created repository deployment gets a fresh per-deploy UUID and therefore need not reuse an orphan's UUID. `NewDeploymentIdentity` creates a UUIDv4 (`internal/deployment/deployment_store.go:218-233`), and both `DeploymentIdentity.Validate` and `DeploymentRoot` enforce it (`:332-363`). That proves the expected directory-name format; it does not prove that filtering existing namespace entries by that format would break fresh-ID creation.

The production damaged scan does not apply that existing invariant: `listDeploymentRecords()` accepts every directory entry and calls `DamagedDirectoryState()` before owner verification (`internal/deployment/deployment_list.go:67-95`); `DamagedDirectoryState()` checks only for a missing `deployment.json` plus retained artifacts (`internal/deployment/damaged_state.go:159-185`). The tests intentionally use non-UUID directory names such as `foreign-orphan` (`internal/deployment/damaged_namespace_network_test.go:146-153`). Thus the rebuttal's statement that a UUID validation gate would break the re-derived-ID path is unsupported: validating the old entry's shape does not require reusing that ID for the next deployment.

**Disposition:** F2's narrow “must equal the newly generated UUID” interpretation is not required, but its canonical directory-name invariant is still open. More importantly, UUID format alone cannot recover the deleted record's app owner; F3 must not be waived on the strength of the UUID-design explanation.

**Correction recipe:** In `internal/deployment/deployment_list.go:67-88` / `internal/deployment/damaged_state.go:211-233`, validate each scanned `deploymentID` against `ValidateDeploymentID` before classifying it as a deployment directory. Add valid-UUID damaged, malformed-name, and existing-record/path-mismatch regressions. For a valid UUID whose record is gone, keep ownership explicitly unknown unless a retained source proves its app identity; do not fill identity from an unrelated current request. Stop when malformed entries cannot become deployment damage and valid orphans are not mislabeled as belonging to the selected app.

### F3 — Registry and scoped paths still attribute an orphan to the selected app

The rebuttal correctly observes that `DamagedDeploymentNamespaceScoped()` derives the workload-network name from the resolved manifest (`internal/deployment/damaged_state.go:246-295`). But its returned `root` comes from a target-wide scan that returns the first damaged directory, without its owner (`:199-235`). The current selected manifest does not prove that this root belongs to that app.

The registry path makes the misattribution explicit. `FindDeployment()` calls `ListDeployments()` and only filters records by application ID/environment after the complete list succeeds (`internal/deployment/deployment_store.go:622-659`). The new `listDeploymentRecords()` path returns immediately for any damaged directory, before owner verification or application filtering (`internal/deployment/deployment_list.go:71-95`). `resolvedRepositoryApplication()` then fills the resulting error's empty app identity from the request and attaches that request app's absent network (`cmd/baha/app_context.go:214-248`). The comment at `:224-234` says the damage is in the requested “target/app,” but the listing error only proves target + deployment ID. A different application's orphan can therefore be returned as the current app's missing record and, if the current app's network is absent, as that app's record-plus-network damage.

The scoped path has the same ownership gap: `DamagedDeploymentNamespaceScoped()` can return a foreign directory at `:215-233`, while `resolvedRepositoryApplication()` constructs the error identity from the requested manifest (`cmd/baha/app_context.go:288-305`). The test `TestDamagedDeploymentNamespaceScopedNoFalseAttributionToForeignApp` explicitly expects `root == foreignDir` while using the selected app identity (`internal/deployment/damaged_namespace_network_test.go:146-176`); it checks only that a **present** selected-app network is not called absent. It does not prove the orphan belongs to that app or cover the case where the selected app's network is absent.

The new registry test is not the production-path regression claimed in its comment. `TestRegistryUpFailsClosedNamingRecordAndNetworkAbsent()` constructs a synthetic `DamagedDeploymentError`, manually assigns `reg-app` identity, and enriches it with a fake absent-network inspector (`cmd/baha/app_lifecycle_damaged_state_test.go:336-377`). It never calls `FindDeployment()` or `resolvedRepositoryApplication()`. Its “foreign” case uses a fake **present** state and checks only `Network != Absent` (`:379-395`), so it cannot falsify the production misattribution above.

**Disposition:** F3 remains open. The fact that the inspected network name is derived from the request proves which network was inspected, not that the damaged directory belongs to that request.

**Correction recipe:** In `cmd/baha/app_context.go:214-248,288-305` and the deployment-list seam, preserve the orphan's owner as unknown until a trusted retained identity binds it to the requested app. Do not attach the requested app's network half to a target-wide listing error based only on request parameters. Either match a damaged entry using a retained identity source before returning an app-specific error, or return an explicit target-level/unknown-owner damaged-state conflict without naming another app's record or network. Add a real `resolvedRepositoryApplication`/`FindDeployment` regression with app A requested and a damaged directory belonging to app B, including the case where A's workload network is absent; assert no app-A attribution. Also prove the BF-03 owned-app case still reports the exact missing network. Stop when both paths establish ownership before producing the app-specific record-plus-network diagnosis.

### F4 — CI selection is valid; the tests do not establish the rebuttal's semantic claim

The run's `PR · Validation · go-unit-tests` job `128908126408` and `deployment-package-tests` job `128908126387` both succeeded on this exact head under the `pull_request` trigger. They execute the new `cmd/baha` and `internal/deployment` package tests, so the test-to-job routing part of the rebuttal is substantiated.

The tests' assertions do not cover production ownership attribution, as detailed under F3. Passing selected tests therefore proves the code is CI-executed, not that foreign-orphan attribution is closed. The helper test checks only a non-absent enum when the selected app's fake network is present; the registry test bypasses both production lookup functions.

**Correction recipe:** Keep the new production-path regressions in the existing `go-unit-tests` / `deployment-package-tests` groups; no workflow change is requested. Assert the error identity, directory root, and network attribution through the actual resolver/listing path for owned and foreign orphans. Stop when the exact-head hosted jobs pass those counterexamples.

### Exact-head hosted state

Run [42538516181](https://github.com/mcpdev80/baseharbor/actions/runs/42538516181) is terminal `completed/failure` on exact head `9e211715187534d9939a39702cd28a726d83581e`. The relevant Go jobs (`go-unit-tests`, `deployment-package-tests`, build, vet, format, runtime-provider package) passed. Both `PR · Native Keycloak/Core · docker` (`128908126340`) and `· podman` (`128908126390`) fail at `TestControlPlaneSingleDefaultNativeRuntimeInCI`, `cmd/baha/control_plane_single_native_ci_test.go:31`, with `prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open /tmp/baseharbor-ci-data-<id>/baseharbor-bootstrap-cleanup-pending: no such file or directory`. The selected-check aggregate is failed as well. The failing test is the reported 0427-172 marker issue and is outside this PR's changed paths; classify it as **external STATE 0427-172**, not a 0427-159 product finding. It remains a red check and is not approval evidence. No workflow rerun or edit was made.

### Required next checks and stop criterion

- Integrate current develop `20902f0a6ab016fd8fe6a501751e1becc5f334dd` into the same candidate chain, then review/run checks on the resulting exact head; the current develop SHA is not an ancestor of `9e211715`.
- Add canonical-ID and real production-path owner-attribution regressions as above; use the existing Go CI jobs and `pull_request` trigger.
- Do not approve until a valid damaged deployment is attributed only to its proven owner, foreign or unknown-owner directories do not acquire the requested app's record/network identity, malformed directory names do not masquerade as valid deployment IDs, and the corrected exact-head Go/selected checks are terminal pass. Track the independent 0427-172 native failure as STATE until its owner-scoped resolution is observed; do not count it as green.

## repo-rule compliance

Read-only review of the product candidate; no local tests, VM smoke, containers, workflow dispatch/rerun, product edits, or PR state changes. Evidence is stored only in the Planning repository. No `.github/**` files were edited.

Planning repository witness: `origin` is `https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push. `origin/main` was `ece010ba87fd782da6d547cf0f035c12daafdeae` before this evidence commit. The evidence path did not exist on `origin/main` before this review.

## END

END_DONE 0427-159-r3-review — KORREKTUR; F3 remains open; F2 remains partly open; F4 routing confirmed but semantic coverage insufficient; exact head `9e211715187534d9939a39702cd28a726d83581e`; run `42538516181` terminal FAILURE with external 0427-172 native STATE.
