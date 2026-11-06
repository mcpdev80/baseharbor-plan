# CODEX-REVIEW — registry access, round 4

- Mission: `coordinator/missions/codex-r1395d.txt`
- Role: CODEX-REVIEW (read-only; no PR action)
- Repository: `mcpdev80/baseharbor`
- PR: #1395, base `develop`
- Reviewed head: `99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c`
- Base `develop`: `af3491889ec689812b8b08d4ff379f56d82d2a49`
- Review date: 2026-11-06
- Verdict: **REJECT** — the implementation and all four null-pull behaviors pass, but the mission's required all-four-red result does not reproduce with its specified M1 fallback-row mutation.

## Candidate identity and scope

`git ls-remote origin` returned candidate `99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c` for both `refs/heads/work/r27-registry-access` and `refs/pull/1395/head`, matching the open PR API head. `origin/develop` is `af3491889ec689812b8b08d4ff379f56d82d2a49`; `git merge-base --is-ancestor origin/develop HEAD` returned 0.

Name-only diff from develop is limited to six `cmd/baha` files:

- `cmd/baha/app_broker.go`
- `cmd/baha/app_broker_pull_caller_test.go`
- `cmd/baha/app_broker_registry_negative_test.go`
- `cmd/baha/app_broker_registry_pull_test.go`
- `cmd/baha/application_registry_source.go`
- `cmd/baha/application_registry_source_test.go`

No files outside the adapter/caller and their tests changed. The isolated review worktree was clean after restoring the mutation; no product file was left modified.

## Resolver and caller path

At `resolveRegistrySourceImpl`, a `RegistrySource.Resolve` error is returned unchanged (`return "", err`), so `ErrRegistrySourceUnavailable` propagates. `pullResolvedRuntimeImage` only uses the legacy mutable reference when the error is classified as merely unavailable and `BASEHARBOR_ALLOW_MUTABLE_DEVELOPMENT_IMAGE` is explicitly enabled. Denial and public-default errors are hard rejection classes. The Docker Hub public-default check runs before the native resolver seam, so the opt-in cannot pull from it.

## Personally run baseline cells

On the exact head, twice ran the focused caller and negative-cell command (using `-p 2`, the workspace Go build cache, and a writable workspace temp directory after an initial Go temp-directory quota error):

```text
go test -p 2 ./cmd/baha -run '^(TestFailedResolvePropagatesWithZeroPulls|TestDeniedEndpointResolveCausesNoPull|TestPublicDefaultDockerHubResolveCausesNoPull|TestMissingDigestResolveCausesNoPull|TestUnavailableResolveWithOptInPullsMutableTag|TestProductionCallerPinsResolvedDigestNotMutableTag)$' -count=1
PASS (30.049s; restored rerun 30.046s)
```

Each of the four mission cells explicitly asserts `len(compose.pulled) == 0`: failed resolve, denied endpoint, Docker Hub public default, and missing digest. The explicit unavailable opt-in pulls exactly one original mutable reference. The round-3 production caller discriminator remains green and pulls the resolved immutable digest.

## M1 fallback-row mutation — required discrimination not met as written

Repeated the round-4 M1 mutation exactly in the isolated worktree, changing only the resolver error return:

```diff
- return "", err
+ return location, nil
```

The four mission cells were run together. **Three turned red**: `TestFailedResolvePropagatesWithZeroPulls`, `TestDeniedEndpointResolveCausesNoPull`, and `TestMissingDigestResolveCausesNoPull`. `TestPublicDefaultDockerHubResolveCausesNoPull` stayed green because its public-default rejection occurs earlier in `resolveRegistrySourceImpl`, before execution can reach the mutated fallback row. The immutable-caller and explicit unavailable-opt-in counterprobes passed under this mutation.

I also ran the historical M1 battery with `TestUnavailableResolveWithoutOptInFailsClosed` in place of the public-default cell. That matches the round-4 evidence: the four failures are failed, denied, missing digest, and unavailable-without-opt-in; the public-default cells are intentionally independent and stay green under M1.

Restored `application_registry_source.go`; `git diff --quiet` returned 0. Re-ran the focused baseline cells and they all passed.

### Required correction recipe

Keep the fail-closed implementation. Reconcile the acceptance gate with the guard layering: either (a) define M1's expected red set as the resolver-fallback cases it reaches (including unavailable without opt-in), and qualify the public-default cell with a separate mutation of the early public-default rejection; or (b) define a caller-wide fallback mutant that sends every resolver error, including hard public-default rejection, to a mutable pull, then require all four mission cells to turn red. As written, the specified M1 row cannot make the earlier public-default cell red.

## Hosted run

Hosted run `42168126290` is terminal `completed / success` at the exact reviewed candidate. PR Selected Checks succeeded; executed Go unit, CLI package/guided, build, vet, source-contract, source-format, workflow-policy, and trusted-plan jobs succeeded. Path-inapplicable runtime and other jobs were skipped.

## Conclusion

Resolver failure propagation, opt-in class gating, all four baseline null-pull assertions, the round-3 production caller cell, exact-head ancestry, hosted checks, and scope all pass. The explicitly requested M1 gate does not turn the public-default cell red, so **REJECT** pending an aligned discriminator criterion or a mutant that actually crosses that independent rejection path. No PR action was taken.
