# CODEX-REVIEW — registry access, round 5

- Mission: `coordinator/missions/codex-r1395e.txt`
- Role: CODEX-REVIEW (read-only; no PR action)
- Repository: `mcpdev80/baseharbor`
- PR: #1395, base `develop`
- Reviewed head: `99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c`
- Base `develop`: `af3491889ec689812b8b08d4ff379f56d82d2a49`
- Review date: 2026-11-06
- Verdict: **ACCEPT** — the round-5 per-layer matrix matches the reproduced M1 and M7 outcomes; the round-4 matrix-only blocker is resolved.

## Candidate and hosted state

`git ls-remote origin` returned `99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c` for both `refs/heads/work/r27-registry-access` and `refs/pull/1395/head`, equal to the PR API head. `origin/develop` is `af3491889ec689812b8b08d4ff379f56d82d2a49`; `git merge-base --is-ancestor origin/develop HEAD` returned 0.

The name-only diff from develop remains six files, all under `cmd/baha`: `app_broker.go`, `app_broker_pull_caller_test.go`, `app_broker_registry_negative_test.go`, `app_broker_registry_pull_test.go`, `application_registry_source.go`, and `application_registry_source_test.go`. The candidate worktree was clean after each mutation was restored.

Hosted run `42168126290` is terminal `completed / success` at the exact head; PR Selected Checks and all executed selected jobs succeeded. No code was added to the candidate in this round.

## M1 — resolver fallback layer

Repeated the resolver fallback-row mutation at `application_registry_source.go:303`:

```diff
- return "", err
+ return location, nil
```

The three resolver cells requested in this mission turned **RED**:

- `TestFailedResolvePropagatesWithZeroPulls`
- `TestDeniedEndpointResolveCausesNoPull`
- `TestMissingDigestResolveCausesNoPull`

The counterprobes `TestUnavailableResolveWithOptInPullsMutableTag` and `TestProductionCallerPinsResolvedDigestNotMutableTag` stayed **GREEN** under M1. The mutation was restored and `git diff --quiet` returned 0.

The fourth M1-negative in the matrix, `TestUnavailableResolveWithoutOptInFailsClosed`, was independently measured with M1 in the preceding review and is recorded in `review-1395d.md`: it is RED. As previously measured, the public-default cells remain GREEN under M1 because their earlier preflight rejects docker.io before this resolver fallback row executes.

## M7 — public-default class gate at the pull site

Mutated only the pull-site class gate at `application_registry_source.go:337`:

```diff
- if resolveUnavailable(err) && allowMutableDevelopmentRuntimeImage() {
+ if allowMutableDevelopmentRuntimeImage() {
```

Both matrix public-default cells turned **RED**:

- `TestPublicDefaultDockerHubResolveCausesNoPull`
- `TestPublicDefaultRejectedBeforeNativeTool`

For diagnostics only, I temporarily added the recorded pull slice to each test's failure message. The first cell reported `pulls=[docker.io/library/app:edge]`; the second independently reported the same pull. The native-tool stub in the second cell was not called: the M7 failure was the opt-in fallback pulling the raw public-default location after the hard-rejection class gate was removed.

Restored both the source gate and temporary diagnostic text. `git diff --quiet` returned 0. Re-ran both public-default cells and `TestUnavailableResolveWithOptInPullsMutableTag` on the unmutated candidate: PASS.

## Matrix comparison

The relevant rows in `round-5.md` match these measurements:

| Cell | Mutation | Observed result |
| --- | --- | --- |
| Failed resolve | M1 resolver fallback restored | RED |
| Denied endpoint | M1 resolver fallback restored | RED |
| Missing digest | M1 resolver fallback restored | RED |
| Unavailable without opt-in | M1 resolver fallback restored | RED (recorded in the preceding exact-head review) |
| Public default | M1 resolver fallback restored | GREEN; earlier preflight handles it before M1 |
| Public default | M7 pull-site class gate removed | RED; recorded mutable pull is `docker.io/library/app:edge` |
| Public default before native tool | M7 pull-site class gate removed | RED; same recorded mutable pull |

This per-layer table resolves the prior review's mismatch: M1 proves resolver propagation, and M7 proves the independent pull-site class gate. The public-default behavior is independently fail-closed on the restored candidate.

## Regressions and decision

The 1395d findings were read against the unchanged candidate: resolver failures propagate, all four caller cells assert zero pulls on the baseline, the explicit unavailable opt-in is class-gated, and the round-3 production-caller discriminator is preserved. The mutations were confined to the isolated review worktree and fully restored. No PR action was taken.

The requested matrix is now discriminating at each relevant layer, and its required M1/M7 entries agree with the observed failures, pull record, and restored green counterprobes. **ACCEPT**.
