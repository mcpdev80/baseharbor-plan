# Merge record — BaseHarbor PR #1377

Role: CODEX-MERGE. This records the authorized connection of the already accepted exact candidate; no new technical review was performed.

## Pre-merge identity and gates

- `gh pr view 1377 --repo mcpdev80/baseharbor`: state `OPEN`, `isDraft=false`, `mergeable=MERGEABLE`, `mergeStateStatus=CLEAN`, base `develop`, head `work/r27-ci-delivery-dsn` at `5b2fbb65c356fb977baa5dcb6d8e6804a90f4fe9`.
- Head matched the ACCEPT in [review-1377b.md](review-1377b.md) exactly. The merge command also used `--match-head-commit 5b2fbb65c356fb977baa5dcb6d8e6804a90f4fe9` as a race guard.
- Before merge, live `develop` was `ecbb88545f96473986f8f41394cffce58b97d2df`; the accepted head had it as an ancestor.
- Pre-merge `git ls-remote`:

  ```text
  ecbb88545f96473986f8f41394cffce58b97d2df refs/heads/develop
  5b2fbb65c356fb977baa5dcb6d8e6804a90f4fe9 refs/heads/work/r27-ci-delivery-dsn
  ```

- Exact-head run `41878182617`: completed success; `PR Selected Checks` success from GitHub Actions app 15368. The recorded rollup was 8 success / 0 failure / 10 skipped; skips were not treated as passes.
- The two-file diff against develop contained only `internal/database/identity_tenant_resolver_integration_test.go` and `internal/database/tenant_integration_test.go`.

## Merge and post-merge proof

- Executed: `gh pr merge 1377 --repo mcpdev80/baseharbor --squash --delete-branch --match-head-commit 5b2fbb65c356fb977baa5dcb6d8e6804a90f4fe9`.
- PR API confirms state `MERGED`, mergedAt `2026-11-04T18:06:07Z`, merge commit `2ea2c6f1d344cca2b21c17e7acbebf711b1511a1`.
- Post-merge `git ls-remote`:

  ```text
  2ea2c6f1d344cca2b21c17e7acbebf711b1511a1 refs/heads/develop
  ```

  The former `refs/heads/work/r27-ci-delivery-dsn` ref is absent.
- On a fresh temporary Git fetch of remote `develop` and PR #1377 head, `git diff --exit-code refs/remotes/origin/pr1377 refs/remotes/origin/develop -- internal/database/identity_tenant_resolver_integration_test.go internal/database/tenant_integration_test.go` returned 0 with no diff (`two_file_diff=EMPTY`). This verifies content equality after squash; ancestry was not used as the proof.
- `git log -1 refs/remotes/origin/develop --format='%H%an%x09%s'`:

  ```text
  2ea2c6f1d344cca2b21c17e7acbebf711b1511a1Marcel Pfingstgräf\ttest(database): read test DSN from env, drop hardcoded DB address (#1377)
  ```

No workflow rerun, release, tag, or product change was made as part of this merge action.

`END_DONE codex-m1377: head=5b2fbb65 entwickelt=2ea2c6f1 inhaltsgleich=ja zweig=geloescht pr=MERGED | Squash-Commit 2ea2c6f1 ist Develops Kopf; die beiden geprueften Tests sind inhaltsgleich zum ACCEPT-Kopf.`
