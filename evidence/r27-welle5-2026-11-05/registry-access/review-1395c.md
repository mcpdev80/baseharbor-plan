# CODEX-REVIEW 1395c — registry access round 3

- Mission: `coordinator/missions/codex-r1395c.txt`
- Role: CODEX-REVIEW (read-only; no PR action)
- Repository: `mcpdev80/baseharbor`
- PR: #1395, base `develop`
- Reviewed head: `2f073f5149b0d5742a8aa6a4d949e58f396de514`
- Base `develop`: `f01d2fbdea6b93af6e06ca6297d04065b6acf701`
- Review date: 2026-11-06
- Verdict: **REJECT**

## Candidate identity and prior review points

`git ls-remote origin` returned
`2f073f5149b0d5742a8aa6a4d949e58f396de514` for `refs/pull/1395/head` and
`f01d2fbdea6b93af6e06ca6297d04065b6acf701` for `refs/heads/develop`.
`git merge-base --is-ancestor origin/develop origin/pr/1395` returned 0.
The PR API reported the exact head, base `develop`, and an open, mergeable PR.

The two prior 1395b findings are fixed at this candidate:

- The production seam at `cmd/baha/app_broker.go:58` calls
  `pullResolvedRuntimeImage`, which goes through `resolveRegistrySource` and
  `RegistrySource.Resolve` before the image pull.
- In an isolated detached worktree at the exact head, I replaced that line's
  resolver call with `compose.PullImage(ctx, runtimeImage)`. The diff showed
  exactly that caller mutation. The new test
  `TestProductionCallerPinsResolvedDigestNotMutableTag` failed with
  `production caller did not drive the artifact resolve invocation through
  resolveRegistrySourceImpl` (exit 1). I restored the source; the same test
  passed (30.046s, exit 0), and the worktree was clean.
- Current `develop` is an ancestor (rc=0).

## Scope and predecessor state

Name-only diff from `origin/develop` to the reviewed head:

- `cmd/baha/app_broker.go`
- `cmd/baha/app_broker_pull_caller_test.go`
- `cmd/baha/app_broker_registry_pull_test.go`
- `cmd/baha/application_registry_source.go`
- `cmd/baha/application_registry_source_test.go`

The changed files are limited to the registry adapter, the authorized caller
seam, and their tests; there are no `.github` or unrelated lifecycle-handler
edits. The four task dependencies (`t-20261017-release-0-4-27-updates`,
`t-20261018-r27-candidate-contract`, `t-20261018-r27-native-auth`, and
`t-20261022-r27-ci-delivery`) are all `closed` with accepted resolutions. No
predecessor implementation is modified in this diff.

## Hosted checks

Hosted run `42152771162` was independently checked at exact head
`2f073f5149b0d5742a8aa6a4d949e58f396de514`: terminal `completed / success`.
`PR Selected Checks` is terminal success. Workflow policy, source format,
trusted plan, Go unit tests, vet, and source contracts succeeded; runtime and
other path-inapplicable jobs were skipped.

## Blocking finding: caller suppresses resolver failure and pulls mutable input

`RegistrySource.Resolve` deliberately returns `ErrRegistrySourceUnavailable`
for denied/unreachable endpoints, missing digests, and public Docker Hub default
hosts. But `resolveRegistrySourceImpl` catches every such error and returns the
original mutable `location` with a nil error. `pullResolvedRuntimeImage` then
passes that reference to `compose.PullImage` as though resolution succeeded.

This defeats the resolver's fail-closed behavior at the production caller. In
particular, a Docker Hub location rejected by `Resolve` can still be pulled by
the caller, and a denied or unreachable endpoint can proceed with an unpinned
mutable tag. The task requires a failed/private/unavailable endpoint not to
fall back and requires recording an exact resolved identity. The caller test
only exercises successful digest resolution; it does not assert that a failed
resolve prevents `PullImage`.

### Required correction recipe

Do not turn `ErrRegistrySourceUnavailable` into a successful mutable reference
in the production caller. Propagate the resolution failure for rejected,
denied, or unavailable sources. If the legacy mutable development-image path
must remain, make its fallback a separate explicit opt-in that cannot bypass
the enterprise endpoint and public-default rejection rules. Add a caller-level
negative test proving that a failed resolve causes zero runtime pulls, including
the public Docker Hub rejection case. Re-run focused caller/adapter tests and
the required hosted checks on the corrected exact head.

## Repository-rule compliance

Read-only review only. The source mutation was confined to a detached temporary
worktree and restored; the PR branch and product worktree were not edited. No
approval or merge action was taken.

## Conclusion

The caller discriminator is now real and mutation-sensitive, the ancestry
refresh is valid, and hosted checks are green. However, the production wrapper
still converts resolver failures into a successful mutable-tag pull, bypassing
the adapter's fail-closed checks. **REJECT** until resolution failure blocks the
pull and the negative caller case is covered.
