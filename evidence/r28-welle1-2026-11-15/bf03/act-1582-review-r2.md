# PR #1582 Review R2 — BF-03

ROLE: CODEX-REVIEW (no merge).

## PLAN

1. Verify exact PR #1582 head/base/ancestry, ls-remote refs, and specified pull_request run witness.
2. Review diff c678cdd0..fa3190eb for one-time legacy /tmp migration and prove no later /tmp write path.
3. Verify foreign-target symlink rejection and new-location 0700/0600 mode assertions; check for BF-01 drift.
4. Write APPROVE or REJECT with correction recipe and exact witnesses; validate and publish evidence on origin/main.

## Candidate and provenance

PR #1582 is OPEN and DRAFT, base `develop`, head branch `lane-0428-fix-bf03`, exact head `fa3190ebc968b6b2776fc6128afcc1d257df422c`. `refs/heads/lane-0428-fix-bf03` and `refs/pull/1582/head` resolve to that exact head. The fetched develop head is `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`, and it is an ancestor of the candidate. The base-to-head log contains only the three task commits `829d75bc`, `c678cdd0`, and `fa3190eb`; no foreign candidate commits are present.

Planning repository root witness (`git rev-parse --show-toplevel`):

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

Planning remote witness immediately before publication (`git ls-remote origin refs/heads/main`):

```text
16f815784d34652cc11cc257223ddc30ddbd7274	refs/heads/main
```

Product `git ls-remote` witness:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
fa3190ebc968b6b2776fc6128afcc1d257df422c	refs/heads/lane-0428-fix-bf03
fa3190ebc968b6b2776fc6128afcc1d257df422c	refs/pull/1582/head
```

PR metadata witness from `gh pr view 1582 --json number,state,isDraft,baseRefName,headRefName,headRefOid,commits`:

```json
{"baseRefName":"develop","commits":[{"oid":"829d75bc9e710daebee62ad16710dd468db1fe13","messageHeadline":"fix(BF-03): persist target selection in private user state (not world…"},{"oid":"c678cdd0a7385504be76d4acf927e47080e3db81","messageHeadline":"chore(BF-03): gofmt internal/orgconfig after world-writable fix"},{"oid":"fa3190ebc968b6b2776fc6128afcc1d257df422c","messageHeadline":"fix(BF-03): one-time migrate persisted selection off world-writable /tmp"}],"headRefName":"lane-0428-fix-bf03","headRefOid":"fa3190ebc968b6b2776fc6128afcc1d257df422c","isDraft":true,"number":1582,"state":"OPEN"}
```

The exact requested delta `c678cdd0..fa3190eb` changes only `internal/orgconfig/store.go` and `internal/orgconfig/orgconfig_test.go`; `git diff --check` passed. No BF-01 target-selection logic was changed; the candidate diff remains confined to organization-selection persistence and its tests.

## Review findings

Verdict: REJECT. The adoption path is implemented for the resolved world-writable legacy location, but two explicit test acceptance requirements are not met, and the tombstone does not enforce the claimed one-time behavior if canonical state later disappears.

1. The migration is exercised for the expected missing-private-file plus old world-writable-file case: `LoadActiveOptional` reads the private canonical path and, on not-exist, calls `adoptLegacySelection`; the test seeds a world-writable resolved `active.json`, runs `LoadActive`, then saves/reloads a new value and confirms the source contents remain unchanged (`internal/orgconfig/store.go:221-251`; `internal/orgconfig/orgconfig_test.go:328-420`). The test uses the same old XDG-resolved path, isolated under `t.TempDir`; it does not touch real `/tmp` state. However, the tombstone is only written, never read: `isWorldFrozenTombstone` exists only as a test helper (`store.go:200-206,327-334`). If the canonical file is removed after adoption, `LoadActiveOptional` calls adoption again and can re-import the retained legacy selection. Recipe: make the once-only marker durable in the private canonical namespace and consult it before any legacy-path access, or otherwise ensure a deleted canonical state cannot restore the stale legacy selection; add a second-call/restart test covering canonical-file removal. The present ordinary subsequent-write test passes its intended case but does not establish this stronger once-only invariant.

2. The implementation rejects a symlink that exists when `os.Lstat` runs (`internal/orgconfig/store.go:146-161`), but the candidate has no positive symlink regression test. `git grep -n -i symlink ... -- internal/orgconfig` returns only the source comments and implementation guard; there is no test asserting rejection of a symlink to a foreign file or unchanged foreign-target bytes/mode. Also, `Lstat` is followed by `os.ReadFile` (`store.go:147,171`), which follows a path if it is replaced between those calls in a writable directory. Recipe: add a symlink-to-foreign-file test asserting fail-closed behavior and unchanged target bytes and mode; open without following symlinks where supported and verify the opened file identity before consuming it.

3. The candidate writes the migrated active file with `0600` and creates its destination directory with `0700` (`internal/orgconfig/store.go:185-199`). The requested test assertions do not check those exact modes: `TestWorldWritableMigrationAdoptsOnceThenFreezes` checks only `info.Mode().Perm()&0o077 == 0` at `orgconfig_test.go:381-385`, which admits modes other than `0600`/`0700`; and its directory `Stat` error is silently ignored because the condition only fails when `err == nil`. Recipe: require successful stats and assert exact `Perm() == 0o600` for the migrated file and `Perm() == 0o700` for the new organization directory.

## Search, CI, and validation

The exact specified run witness from `gh run view 43672378209 --json databaseId,status,conclusion,event,headSha,workflowName` is:

```json
{"conclusion":"success","databaseId":43672378209,"event":"pull_request","headSha":"fa3190ebc968b6b2776fc6128afcc1d257df422c","status":"completed","workflowName":"CI · Source & Quality"}
```

The round-3 handoff records the relevant package job `PR · Draft Go · packages` as successful for this exact head; the native impact selection was skipped because this Draft PR did not select a runtime/native-impact test. No workflow was edited or rerun by this review.

Grep witness for filesystem mutation calls in `internal/orgconfig/store.go`:

```text
189: os.WriteFile(tmp, data, 0o600)
192: os.Chmod(tmp, 0o600)
193: os.Remove(tmp)
196: os.Rename(tmp, dst)
197: os.Remove(tmp)
202: os.Chmod(src, 0o400)
204: os.WriteFile(tomb, ...)
313: os.WriteFile(tmp, data, 0o600)
316: os.Chmod(tmp, 0o600)
317: os.Remove(tmp)
320: os.Rename(tmp, canonical)
321: os.Remove(tmp)
377: os.WriteFile(path, content, 0o600)
421: os.WriteFile(dst, data, 0o600)
```

The ordinary post-adoption `SaveActive` write targets `canonical` (`store.go:312-320`), while the migration helper still has explicit mutation operations against the legacy source and its parent (`store.go:202-206`). Those operations are intended for the first adoption; because the tombstone is not consulted, the implementation does not enforce that they can never run again if canonical state is later removed. No local tests were run in this read-only review. The exact-head hosted run is successful, but that result does not provide the missing symlink or exact-mode regression assertions.

## repo-rule compliance

Read-only review of a fresh clone at the exact PR head. No product files, workflow files, PR metadata, tests, containers, or VMs were changed or run. Review stayed within BF-03; no BF-01 files were changed. Evidence is stored only in the actual `baseharbor-plan` repository.

END mission-rev1582-r2.md DONE — REJECT; three actionable gaps remain on candidate `fa3190ebc968b6b2776fc6128afcc1d257df422c`.
