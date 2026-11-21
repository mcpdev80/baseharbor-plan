# round-1: child-env-inheritance (0428-222)

Card: t-20261121-child-env-inheritance (0428-222)
Mission: coordinator/missions/0428-222-child-env-inherit.md
Candidate branch: `lane-0428-222-child-env` base `develop`
Base head attestation (git ls-remote): `22fc68ebc0655874bc3f6aa886ff356dcad79624` refs/heads/develop (develop advanced from the dispatch value `ddfa80f7202a0aca3cf68c4542158132c0c2795b` mid-lane; re-based onto new head before commit, target files unchanged in the old->new diff)
Real planning remote (git -C .../baseharbor-plan remote -v): `origin https://github.com/mcpdev80/baseharbor-plan.git`

## PLAN

1. Reality check: show task, gh pr view, ls-remote develop, verify real git remotes.
2. Inspect all 5 sites individually and decide each intentional or not, with evidence (file:line).
3. Extend env (append os.Environ()) at each non-intentional site, preserving any existing secret-scrubbing.
4. One regression test per changed site proving env inheritance via a sentinel, plus a mutation test (remove heredoc -> must go red).
5. Four prove-or-fix witnesses at develop head.
6. Hosted CI run to terminal at exact base-head.
7. Write this akte, repo-rule compliance, cleanliness.

## repo-rule compliance

Write-set of card = the three source files (`internal/corebackup/etcd/etcdctl.go`, `internal/corebackup/etcd/etcdutl.go`, `internal/coreupdate/dcs_boot_probe.go`) + their tests + one new `internal/*/*0428-222*_test.go` per changed package. No `.github/**`, no `scripts/**`, no `internal/operatorauth/**`, no `internal/identityprovider/**`, no `internal/serviceaccess/**`, no `internal/observability/registry.go`, no `internal/capability/perses_selection.go`, no `cmd/baha/**`. Commit author = `0428-222-childenv`.

## Decision per site (prove-or-fix)

Desk H-V47 (akte hunt-1.md, plan f12821ac0) reports five product-reachable places that build the child env as a literal list with no `os.Environ()`. The intended contract: a child of the `baha` CLI inherits the parent environment (exported variables) while pinning only the security-sensitive etcdctl/etcdutl keys. The repo's own convention (PR #1742 fix, `cmd/baha/app_inspect_remote.go:72-74` and `app_update.go:493`) derives from `os.Environ()`.

- Site 1 `internal/corebackup/etcd/etcdctl.go:95` (`EtcdctlSource.Snapshot`, `etcdctl snapshot save`): literal `cmd.Env = []string{"PATH=...", "ETCDCTL_API=3", ..., TLS *_CERT/*_KEY}`. Only approved endpoints, no token/cert bytes in argv (line 93 comment). Inheriting the parent env is correct and intended; the security model is argv-only, not env-exclusion. **NOT intentional -> FIX (append os.Environ()).**
- Site 2 `internal/corebackup/etcd/etcdctl.go:114` (snapshot status verify via `etcdutl`): literal `cmd.Env = []string{"PATH=/usr/bin:/bin"}`. Same argv-only security model. **NOT intentional -> FIX (append os.Environ()).**
- Site 3 `internal/corebackup/etcd/etcdctl.go:156` (`attestEndpointStatus`, `etcdctl endpoint status`): literal env with PATH, ETCDCTL_API, TLS certs. **NOT intentional -> FIX (append os.Environ()).**
- Site 4 `internal/corebackup/etcd/etcdutl.go:95` (`IsolatedEtcdutl.RestoreIsolated`, `etcdutl snapshot restore`): literal `cmd.Env = []string{"PATH=/usr/bin:/bin"}`. The type name `IsolatedEtcdutl` and comments (lines 13-14, 87-88) mean *filesystem/container isolation* (never execute inside the running distroless etcd container, isolated target data-dir) per the `Restorer` interface doc (etcd.go:263-264). This is orthogonal to the inherited process env. Env inheritance does not weaken the isolation contract. **NOT intentional -> FIX (append os.Environ()).** Decision recorded here per mission step 1 special-case for the "isolated" name.
- Site 5 `internal/coreupdate/dcs_boot_probe.go:59` (`dcsBootProbe`, etcd boot probe): literal env with PATH, ETCDCTL_API, TLS certs. Same argv-only security model. **NOT intentional -> FIX (append os.Environ()).**

No site performs secret scrubbing on the env list (grep for scrub/token/password/secret in internal/corebackup/etcd/ and internal/coreupdate/ shows only argv-path security and the cluster-token arg). So appending os.Environ() preserves every existing security property.

## Chosen sentinel

`BASEHARBOR_0428_222_SENTINEL=1` (unique to this card, will not collide with real CI/parent env).

## Implementation (applied, committed)

Commit `a513af08a` on branch `lane-0428-222-child-env`, author `0428-222-childenv`, base `22fc68ebc`. All five sites changed to `cmd.Env = append([]string{ ...pinned keys... }, os.Environ()...)` so the pinned etcdctl/etcdutl keys come first and os.Environ() is inherited after.

## Four witnesses at develop head

- `git merge-base --is-ancestor lane-origin/develop HEAD` = JA (develop `22fc68ebc` is ancestor of `a513af08a`)
- `git rev-list --count lane-origin/develop..HEAD` = 1 (only my commit)
- `git rev-list --count HEAD..lane-origin/develop` = 0 (no foreign commits carried)
- `git diff --name-only lane-origin/develop..HEAD`:
  - `internal/corebackup/etcd/etcdctl.go`
  - `internal/corebackup/etcd/etcdutl.go`
  - `internal/coreupdate/dcs_boot_probe.go`
  - `internal/corebackup/etcd/child_env_inheritance_0428_222_test.go`
  - `internal/coreupdate/child_env_inheritance_0428_222_test.go`
- `git log -1 --format=%an HEAD` = `0428-222-childenv`

## Local test results (on develop `22fc68ebc`)

Form used (TEST RUNNER RULE, no bare package test):
`go test ./internal/corebackup/etcd/ -count=1 -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` -> `ok github.com/mcpdev80/baseharbor/internal/corebackup/etcd`
`go test ./internal/coreupdate/ -count=1 -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` -> `ok github.com/mcpdev80/baseharbor/internal/coreupdate`
`go vet ./internal/corebackup/etcd/` clean; `go build ./internal/corebackup/etcd/... ./internal/coreupdate/...` clean.

## Mutation test (criterion 3)

Removing `os.Environ()...` from `etcdctl.go` (site 1) makes `TestEtcdEnvInheritsParentEnv/snapshot-save` FAIL with "sentinel BASEHARBOR_0428_222_SENTINEL=1 not inherited by child". Verified the test goes red on the mutation, then restored the fix.

## CI wiring

New tests live in packages `internal/corebackup/etcd` and `internal/coreupdate`, both covered by the standard `go test ./...` group. They run under the CI group that runs the full Go build/test matrix (the repository's `go test ./...` invocation), triggered by the normal branch-push / PR selected-checks flow. Hosted run pending (see run section).

## Cleanliness

docker ps -a before: (none started this lane - no container/compose work)
docker ps -a after: (none)
