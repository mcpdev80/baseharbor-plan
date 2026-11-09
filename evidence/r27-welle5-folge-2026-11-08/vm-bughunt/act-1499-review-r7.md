# CODEX-REVIEW 0427-159 r7 — PR #1499

ROLLE: REVIEW

URTEIL: korrektur

## PLAN

1. Verify the live PR head, its develop base, exact-head CI run, and current develop ancestry.
2. Inspect r7's namespace-scoped regressions, trust-boundary ordering, retained-band producer, and damaged-state-before-budget path.
3. Record findings and a concrete correction recipe in this evidence file.
4. Publish the review to canonical baseharbor-plan main and verify the remote evidence path.

## Exact candidate and hosted state

Repository: mcpdev80/baseharbor; PR #1499; task 0427-159.

- Live PR head: 8b7fbaee0e3527e96674856cfb2d1025ae42fbd5.
- PR API base SHA: 942111d5a1c43f5257bf1627a966fa9e6c6f24bd.
- Current origin/develop from ls-remote: e072e142ec9511f3cc86ffa67c7debd022d7760a.
- Current develop is not an ancestor of this PR head: merge-base is 942111d5a1c43f5257bf1627a966fa9e6c6f24bd; develop...head counts 1 6; merge-base --is-ancestor origin/develop origin/pr1499 exits 1. The candidate is behind current develop by one commit and needs a fresh base/required-check observation before landing.
- Live remote refs agree on PR head: refs/heads/0427-159-damagedstate and refs/pull/1499/head both resolve to 8b7fbaee0e3527e96674856cfb2d1025ae42fbd5.
- PR is open and GitHub reports mergeable CLEAN, but that does not remove the observed develop drift.

Run 42591040401 is completed/success on the exact PR head, triggered by pull_request. go-unit-tests, deployment-package-tests, go-build, go-vet, cli-gofmt, runtime-provider-package-tests, source format, focused Python, native destroy-retry Docker and Podman, and PR Selected Checks passed. Native Keycloak/Core and Targeted HA Docker/Podman were skipped; they are not counted as green executions. No failure or pending job was reported in this run.

## Review findings

### Namespace-scoped regression tests remain

The r7 commit changes only internal/deployment/damaged_state.go and leaves the three regressions that failed on r6 intact in internal/deployment/damaged_namespace_network_test.go:

- TestDamagedDeploymentNamespaceScopedNamesNetworkWhenAbsent at line 30.
- TestDamagedDeploymentNamespaceScopedPresentNamesOnlyRecord at line 69.
- TestDamagedDeploymentNamespaceScopedNoFalseAttributionToForeignApp at line 142.

The r7 hosted run's deployment-package-tests and go-unit-tests are green, so the unchanged tests are exercised in CI. TestDamagedDeploymentNamespaceScopedNoRuntimeFallsBackToRecordOnly at line 109 is also retained.

### Trust boundary is fail-closed and correctly placed before outward attribution

In cmd/baha/app_context.go, resolvedRepositoryApplication starts the damaged-state path before the generic repository-inspection budget branch (lines 265-284). It calls LoadRetainedOwnerBand at line 299 before constructing the requested application's identity at lines 314-325. Missing, unreadable, malformed, or nonmatching band data returns an unknown-owner identity and blank network fields at lines 300-312. The resolver therefore does not emit a requested-app label or network diagnosis before the band check.

The lower-level namespace scan at internal/deployment/damaged_state.go:320-361 intentionally retains its app-scoped network derivation. The CLI resolver gates the returned attribution, so moving the band check out of that scan preserves the three namespace-scope assertions without weakening the outward trust boundary.

### Blocking gap: no production writer creates the ownership band

The reader and trust check are present, but the production tree has no writer for RetainedOwnershipBandName or the ".owner" file. In the PR tree, references to RetainedOwnershipBandName are limited to the constant and loader in internal/deployment/damaged_state.go:206-226, the CLI reader in cmd/baha/app_context.go:299, and a test-only os.WriteFile in cmd/baha/app_lifecycle_damaged_state_test.go:458. That fixture manually creates the band. Consequently, the passing owned-app regression proves the reader accepts a hand-seeded marker; it does not prove the real lifecycle writes a marker that survives loss of deployment.json. Without such a production write, real damaged directories cannot pass the new ownership gate and will remain unknown-owner/record-only, so the promised record-plus-network diagnosis is not demonstrated for a genuinely owned damaged deployment.

This is the code blocker. The passing exact-head run does not cover this missing production path.

### Damage-before-budget behavior remains in the resolver

The damaged namespace scan remains before the generic repository-inspection budget decision in resolvedRepositoryApplication (cmd/baha/app_context.go:265-284). The earlier precedence behavior is retained. It should be preserved while adding the writer; the production writer must not defer damage detection until after the generic budget failure.

## Actionable correction recipe

- In the production lifecycle path that creates and persists deployment state, write the retained ownership band at the point where the canonical application/environment identity is trusted, before the deployment record can be lost or truncated. Use the protected deployment directory and fail closed on write/permission errors. The record and band must be created/updated consistently; never infer ownership from a UUID directory or the current requesting manifest.
- Replace or supplement the manually seeded fixture in cmd/baha/app_lifecycle_damaged_state_test.go:455-459 with a production-path regression: create a real deployment through the lifecycle, cause the test to remove/truncate only deployment.json while leaving retained state, then resolve the same app through the CLI resolver and assert exact app/environment/network attribution. Also assert that a missing, malformed, unreadable, or foreign band remains unknown-owner with no network attribution.
- Keep the three namespace-scoped tests and their current expectations. Keep damaged-state detection ahead of the generic repository-inspection budget.
- Refresh PR #1499 onto the current develop head e072e142ec9511f3cc86ffa67c7debd022d7760a, then observe required checks on the new exact head. Do not count skipped runtime cells as passes.
- Stop only when the genuine lifecycle writes the durable band, the production-path damaged fixture proves it survives record loss and is correctly read, unbound/foreign markers remain fail-closed, the three namespace regressions remain green, and the refreshed exact-head required checks are terminal with no failures.

## repo-rule compliance

- Product repository and PR were read-only; no product files, refs, or checks were changed or rerun.
- No local tests were run for this review.
- Evidence is being published only in canonical baseharbor-plan, whose origin is https://github.com/mcpdev80/baseharbor-plan.git.

END_DONE 0427-159-r7-review: KORREKTUR PR #1499 head 8b7fbaee0; namespace regressions remain and outward attribution is gated, but no production .owner-band writer exists; candidate also trails develop e072e142.
