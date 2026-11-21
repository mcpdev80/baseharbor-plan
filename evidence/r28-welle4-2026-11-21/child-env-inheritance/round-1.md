# round-1: child-env-inheritance (0428-222)

Card: t-20261121-child-env-inheritance (0428-222)
Mission: coordinator/missions/0428-222-child-env-inherit.md
Candidate branch: `lane-0428-222-child-env` base `develop`
Base head attestation (git ls-remote): `ddfa80f7202a0aca3cf68c4542158132c0c2795b` refs/heads/develop
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

## Implementation (applied, not yet committed)

All five sites changed to `cmd.Env = append([]string{ ...pinned keys... }, os.Environ()...)` so the pinned etcdctl/etcdutl keys come first and os.Environ() is inherited after. (Exact diffs recorded in git after commit.)

## Regression tests (one per changed package)

`etcd` package: a new test builds `EtcdctlSource.Snapshot` / `attestEndpointStatus` with an env-capturing stub binary that writes its inherited env to a file, sets `os.Setenv("BASEHARBOR_0428_222_SENTINEL","1")` before the call, and asserts the child-side captured value. Mutation: removing the heredoc line makes the assertion fail (test goes red).

`coreupdate` package: a new test drives `EtcdBootProbe.Verify` with the same env-capturing stub and asserts the sentinel is inherited by the child. Mutation: removing the heredoc line makes the test fail (red).

## CI wiring

New tests live in packages `internal/corebackup/etcd` and `internal/coreupdate`, both of which are covered by the standard `go test ./...` group in GitHub CI. State in the run section which CI job runs them and under which trigger.

## Cleanliness

docker ps -a before: (none started this lane - no container/compose work)
docker ps -a after: (none)
