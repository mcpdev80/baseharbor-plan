# Independent read-only review — PR #1650 / 0428-078

Reviewed 2026-11-19.

- Head `022c454ce482cce51cab47b4797caaaccd0bc175`, base `907f16713cbf38693d30c9dadaad7fe299759219`; open and not mergeable.
- Exact-head run `44400488202` failed `PR · Validation · ci-executor-tests` and `PR · Focused Python`. Go shards/build/vet passed. The PR changes five `.github/workflows` files despite its body saying no `.github/**` edits; workflow changes conflict with `scripts/test_pr_selected_runtime_matrix.py:96-125`, including max-parallel expectations, coreless integration dispatch and gate/runtime concurrency key.
- No edits/comments/claim/merge by this review.

## Finding

`cmd/baha/app_status_result.go:150-165` computes `IdentityDashboardEligible` only from `IdentitySelectionWitnessAt(...).NonForgeableAvailable()`. The separately computed Perses status is not included. Status can therefore report the dashboard eligible when Perses is unselected or unverified. Add selection/current-state gating and a status-seam regression.

The witness non-forgeability claim also appears stronger than its public constructor/exported evidence booleans, but this may be inherited from the base; verify before attributing it to this PR.
