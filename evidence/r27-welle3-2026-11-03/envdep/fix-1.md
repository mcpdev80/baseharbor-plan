# Fix w38 — t-20261023-appid-test-env-dep (provider-registry ownership-unverifiable)

- Role: Worker, lane w38. Coord f49a3303. Task: t-20261023-appid-test-env-dep (release v0.4.27).
- Branch / worktree: `work/r27-envdep-ab` in `/tmp/opencode/w38-envdep-wt`, based on origin/develop.
- Head SHA: `b2c2979cbbefa46f3f24eae99b8ec529f6ebe692` (merge of 6304922a into develop@1706272c authority-contract; confirmed `git ls-remote origin work/r27-envdep-ab` == head).
- DRAFT PR: #1351 (https://github.com/mcpdev80/baseharbor/pull/1351), base `develop`, head `work/r27-envdep-ab`, draft=true.

## Root cause

- `TestExternalProviderRemoval*` (cmd/baha/provider_external_removal_test.go) failed with
  `provider change: provider-registry-ownership-unverifiable` on a clean `develop` checkout.
- The test seeds provider-registry ownership via `BASEHARBOR_STATE_DIR=<tmpdir>` (a `t.TempDir()`),
  then `PlanExternalProviderRemovalAt` -> `ApplyExternalProviderRemovalAt` calls
  `verifyExternalRemovalRegistryOwner(store.Path)`.
- That check (internal/application/external_provider_scope.go:200) fails when ANY parent directory
  of the registry is group-writable (`info.Mode().Perm()&0022 != 0`).
- The workspace tmp `/tmp/opencode` is group-writable (`775 marcel:marcel`), so the seeded state
  dir's ancestor failed the ownership check. This is an environment artifact, not a defect in the
  ownership logic (whose intent — registry file owned and unshared — is correct).
- Matrix probe (internal/application zzz_envdep_probe_test.go, deleted after verification):
  - root 0755/dir 0775/file 0664 -> fail; root 0775/dir 0700/file 0600 -> pass; root 0755/dir 0711/file 0600 -> pass;
  - conclusion: group-writable parent dir is the trigger, regardless of file perms.

## Change

- In-scope file only: cmd/baha/provider_external_removal_test.go, `externalRemovalTransportFixture`.
- Added `os.Chmod(root, 0o700)` on the seeded state dir before `t.Setenv("BASEHARBOR_STATE_DIR", root)`,
  so ownership is seeded explicitly and verifiable from the fixture alone (no reliance on CI-runner
  ambient tmp perms). Added `os` import.
- Diff: 1 file, +9 / 0. No deletions of existing behavior. `.github/scripts` untouched (write-set grep clean).
- No product runtime behavior change; the fix is test-fixture state seeding under the in-scope
  `internal/**` ownership path.

## Local runs (output)

- `TMPDIR=/tmp/opencode go test ./cmd/baha -run 'TestExternalProviderRemoval' -count=1`
  -> `ok github.com/mcpdev80/baseharbor/cmd/baha 0.045s` (was: 4 FAIL subtests, all unverifiable).
- Same command under clean `0700` tmp -> `ok` (no regression).
- Full `go test ./cmd/baha -count=1` shows pre-existing host-environment failures NOT caused by this
  change and NOT in scope (confirmed identical on unmodified develop):
    - Docker endpoint `unix:///var/run/docker.sock is unavailable` (no daemon on host).
    - OpenBao recovery output collisions at host `~/.local/share/baseharbor-recovery/...` (leftover
      host state, not TMPDIR-dependent).
  These are exactly the CI-runner-ambient artifacts this task must not depend on.

## Acceptance (card)

- Local green, no CI-only skips: PASS (command above).
- Ownership seeded by fixture, no ambient CI markers: DONE (fixture chmod + comment).
- Evidence lists local run output: this file. Hosted run id/url: to be recorded after a hosted PR
  run of the identical head (6304922) completes; the local run already removes CI-marker reliance.
- Reviews' "pre-existing env fail, equal on clean develop" resolved: clean develop now green for the
  fixed test under a group-writable tmp.

## Nachbesserung (coordinator f49a3303 request — only missing step)

- develop merged authority-contract (#1348) to 1706272c after the first DONE post.
- Applied: `git fetch origin develop` + `git merge --no-edit origin/develop` (FF) into work/r27-envdep-ab;
  head now `b2c2979c` (contains original fix 6304922a).
- `TMPDIR=/tmp GOCACHE=/tmp/opencode/gc go build ./...` -> exit 0 (clean).
- `TMPDIR=/tmp GOCACHE=/tmp/opencode/gc go test ./cmd/baha -run TestExternalProviderRemoval -count=1` -> `ok ... 0.050s` (local green retained).
- `git push` FF 6304922a..b2c2979c; `git ls-remote origin work/r27-envdep-ab` == head.
- `git merge-base --is-ancestor 1706272c3e8d53d37cf4da8f9f1411e5fe419a94 HEAD` -> rc=0 (END proof that develop is contained).
- No force; PR #1351 remains DRAFT.

## Repo-rule compliance

- Write-set limited to in-scope test fixture; `.github/scripts` untouched (grep clean).
- No skip-by-env trick (skip is not a fix); the ownership is now explicitly seeded.
- app.id parser (t-20261020), planner-lane (#1047), and product runtime behavior out of scope and untouched.
- Draft PR on own branch; `git ls-remote == head`.

## END

- END f49a3303 lane w38 DONE: w38-envdep-fix: fixture seeds ownership explicitly -> local green; candidate SHA 6304922; DRAFT PR #1351.
